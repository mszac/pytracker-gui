"""Single best-effort append-only project log, independent of PsychoPy and Tk.

Only the low-priority writer thread does project-file I/O. The producer does
bounded RAM operations; when storage cannot keep up, recent messages win.
"""
from __future__ import annotations

from collections import deque
import os
from pathlib import Path
import threading
import time

PENDING_BYTES = 262144                 # Preserve the existing 256 KiB limit.
WRITE_INTERVAL = 15.0                 # Not an every-two-seconds filesystem poll.
WRITE_WATERMARK = 196608              # 75% pressure triggers early scheduling.
MIN_WRITE_SPACING = 5.0               # Even under buffer pressure, avoid 2-second writes.
WRITE_BATCH = 65536                   # At most 64 KiB per physical write.


class IncrementalExperimentLog:
    def __init__(self, run_dir, run_id, stamp=None, *, interval=WRITE_INTERVAL):
        self.run_dir = Path(run_dir)
        self.run_id = run_id
        stamp = stamp or time.strftime('%Y%m%d_%H%M%S', time.localtime())
        name = f'experiment_{stamp}_{run_id}.log'
        self.partial_path = self.run_dir / (name + '.part')
        self.complete_path = self.run_dir / name
        self.interval = interval
        self._pending = deque()
        self._pending_bytes = 0
        self._dropped_bytes = 0
        self._total_dropped = 0
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._finishing = False
        self._interrupted = False
        self._closed = False
        self._thread = None
        self.error = None
        self.final_path = None

    @property
    def dropped_bytes(self):
        with self._lock:
            return self._total_dropped

    def start(self):
        self._thread = threading.Thread(target=self._worker,
                                        name='pytracker-log-io', daemon=True)
        self._thread.start()

    def _bound_locked(self):
        while self._pending_bytes > PENDING_BYTES:
            old = self._pending.popleft()
            self._pending_bytes -= len(old)
            self._dropped_bytes += len(old)
            self._total_dropped += len(old)

    def append(self, line):
        """No disk calls, no waiting for the writer, no unbounded allocations."""
        data = str(line).encode('utf-8', errors='replace')
        with self._lock:
            if self._closed:
                return
            if len(data) > PENDING_BYTES:
                drop = len(data) - PENDING_BYTES
                self._dropped_bytes += drop
                self._total_dropped += drop
                data = data[-PENDING_BYTES:]
            before = self._pending_bytes
            self._pending.append(data)
            self._pending_bytes += len(data)
            self._bound_locked()
            pressure = before < WRITE_WATERMARK <= self._pending_bytes
        if pressure:
            self._wake.set()

    def finish(self, *, interrupted=False):
        with self._lock:
            self._finishing = True
            self._interrupted = interrupted
        self._wake.set()

    def wait(self, timeout=2.0):
        if self._thread is not None:
            self._thread.join(timeout)
        return self.final_path

    def _take_batch(self):
        with self._lock:
            data = bytearray()
            while self._pending and len(data) < WRITE_BATCH:
                item = self._pending[0]
                space = WRITE_BATCH - len(data)
                if len(item) <= space:
                    data.extend(self._pending.popleft())
                    self._pending_bytes -= len(item)
                else:
                    data.extend(item[:space])
                    self._pending[0] = item[space:]
                    self._pending_bytes -= space
            lost = self._dropped_bytes
            self._dropped_bytes = 0
            finishing = self._finishing
            interrupted = self._interrupted
        return bytes(data), lost, finishing, interrupted

    def _restore_failed(self, remaining, dropped):
        with self._lock:
            if remaining:
                self._pending.appendleft(remaining)
                self._pending_bytes += len(remaining)
            self._dropped_bytes += dropped
            self._bound_locked()   # overwrite oldest, not newest, under I/O failures

    @staticmethod
    def _low_priority():
        if os.name == 'nt':
            try:
                import ctypes
                api = ctypes.windll.kernel32
                api.SetThreadPriority(api.GetCurrentThread(), -1)  # BELOW_NORMAL
            except Exception:
                pass
        # On Linux no process-wide nice change: idle/sleeping worker is adequate.

    def _worker(self):
        self._low_priority()
        stream = None
        try:
            # Create the recovery marker as early as the background worker can.
            # Exclusive create prevents accidental overwrite of another run.
            stream = self.partial_path.open('xb', buffering=0)
        except OSError as exc:
            self.error = str(exc)
            # The parent directory is already reserved by prepare_run. Retry
            # opening at the next scheduled opportunity without blocking stdout.
        last_attempt = time.monotonic()
        while True:
            self._wake.wait(self.interval)
            self._wake.clear()
            # Never write at high frequency during active acquisition; the
            # bounded ring replaces stale unpersisted messages under pressure.
            with self._lock:
                is_finishing = self._finishing
            if not is_finishing and time.monotonic() - last_attempt < MIN_WRITE_SPACING:
                time.sleep(max(0, MIN_WRITE_SPACING - (time.monotonic() - last_attempt)))
            last_attempt = time.monotonic()
            data, lost, finishing, interrupted = self._take_batch()
            if not data and not lost and not finishing:
                continue
            marker = (f'\n[LOG] BUFFER_OVERFLOW: {lost} oldest unpersisted bytes lost\n'
                      .encode('utf-8') if lost else b'')
            try:
                if stream is None:
                    stream = self.partial_path.open('ab', buffering=0)
                # Write marker and data separately; retain unwritten tail on error.
                for piece in (marker, data):
                    while piece:
                        count = stream.write(piece)
                        if not count:
                            raise OSError('zero-byte log write')
                        piece = piece[count:]
                self.error = None
            except (OSError, ValueError) as exc:
                self.error = str(exc)
                # At worst an OS-level partial write may leave a partial record;
                # archive stays .part for later inspection/repair.
                self._restore_failed(data, lost)
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass
                stream = None
                if finishing:
                    break
                continue
            if finishing:
                # Finishing is a second phase: drain whatever arrived while I/O
                # was pending. Only this daemon may block on final fsync/rename.
                with self._lock:
                    more = self._pending_bytes or self._dropped_bytes
                if more:
                    self._wake.set()
                    continue
                try:
                    if interrupted or self._total_dropped:
                        reason = ('INTERRUPTED' if interrupted else 'INTERRUPTED: BUFFER_OVERFLOW')
                        stream.write((f'\n[LOG] {reason}: ' +
                                      f'{self._total_dropped} bytes lost from bounded RAM buffer\n').encode('utf-8'))
                    stream.flush()
                    os.fsync(stream.fileno())  # never during active acquisition
                    stream.close()
                    stream = None
                    if not interrupted and self._total_dropped == 0:
                        os.replace(self.partial_path, self.complete_path)
                        self.final_path = self.complete_path
                    else:
                        # Interrupted or incomplete logs await future recovery.
                        self.final_path = self.partial_path
                except OSError as exc:
                    self.error = str(exc)
                    self.final_path = self.partial_path
                break
        if stream is not None:
            try:
                stream.close()
            except OSError:
                pass
        with self._lock:
            self._closed = True

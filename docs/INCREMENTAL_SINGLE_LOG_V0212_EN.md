# v0.2.12 — single low-priority append-only experiment log

## Contract

Each run in `projects/<project>/experiments/<timestamp>_<ID>/` has exactly one persistent experiment journal, `experiment_<start_timestamp>_<ID>.log.part`. No separate `console_*.log` is produced. The same ordered stream includes `[RUN]`, `[STATUS]`, child stdout/stderr, `[PROCESS]`, and `[FINAL]`. Following successful completion and persistence without data loss, the writer atomically renames `.log.part` to `.log`. A `.part` remains after cancellation, unexpected termination, buffer overflow, I/O error, or crash; **recovery and repair are deferred**. Controlled cancellation also records `[LOG] INTERRUPTED` and the usual `CANCELLED` status remains in `result.json`.

## Scheduling and safety

The subprocess stdout reader never touches project-disk files; it submits messages into a bounded 256-KiB FIFO byte ring. The **existing 256-KiB ceiling is preserved**. Under sustained backpressure, the oldest *not yet persisted* messages are replaced by new ones. A resumed writer emits a `[LOG] BUFFER_OVERFLOW` byte count and leaves the journal as `.part`, avoiding an unjustified completeness claim. A separate daemon writer has BELOW_NORMAL Windows thread priority and sleeps when idle. It attempts I/O approximately every 15 seconds or when the queue reaches 192 KiB, with at least roughly 5 seconds between writes under pressure. Writes are sliced into up to 64-KiB batches. `fsync()` and the final rename happen only after run completion in the writer thread.

This is **best-effort low-priority I/O**, not a guarantee that the storage device is idle. A stalled/unavailable disk can cause loss of old unpersisted entries; power loss may also lose recently buffered data, and a fully inaccessible volume may prevent creation of even `.part`.

## Scope frozen

GUI retains its 256-KiB `SpooledTemporaryFile` and 256-KiB/2000-line visual preview, Auto-show Logs, and Copy entire log. It does not create a second persistent journal. Measurement data, run metadata formats, session-ID binding, PsychoPy launch/adapters, project layout, UI/manual and visual theme remain unchanged. Real Windows/PsychoPy/Tobii physical acceptance is pending.

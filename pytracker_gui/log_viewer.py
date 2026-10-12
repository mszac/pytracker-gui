"""Bounded, strictly read-only GUI-owned console journal reader.

No watchers, mmap, background threads, measurement paths, or whole-file reads.
All offsets are bytes; UTF-8 pages terminate at a line break where possible.
"""
from __future__ import annotations

import os
from pathlib import Path
import stat

PAGE_BYTES = 64 * 1024
PAGE_LINES = 2000


def journal_for_run(run):
    """Return (path, integrity) only for the exact selected GUI run journal.

    Legacy/foreign experiment_*.log names are NOT inferred to belong to a run.
    If both a completed and partial journal exist, show the incomplete one.
    """
    directory = Path(run.directory)
    name = f'experiment_{run.timestamp}_{run.run_id}.log'
    partial = directory / (name + '.part')
    complete = directory / name
    for path, integrity in ((partial, 'partial'), (complete, 'complete')):
        if path.is_symlink():
            raise ValueError('Linked log file is not allowed: ' + path.name)
        if path.is_file():
            return path, integrity
    return None, 'none'


def _open_journal(path):
    """Only regular non-linked local files; protect against symlink swapping."""
    path = Path(path)
    if path.is_symlink():
        raise ValueError('Linked log file is not allowed')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('Log is not a regular file')
        if path.is_symlink():
            raise ValueError('Linked log file is not allowed')
        return os.fdopen(fd, 'rb')
    except BaseException:
        os.close(fd)
        raise


def read_page(path, offset=0):
    """At most 64 KiB payload, return (text, offset, next_offset, size).

    Pages end on the last newline available in the window so ordinary UTF-8
    log lines are not broken. Extremely long lines still use a hard byte cap.
    """
    if not isinstance(offset, int) or offset < 0:
        raise ValueError('Invalid log offset')
    with _open_journal(path) as stream:
        size = os.fstat(stream.fileno()).st_size
        offset = min(offset, size)
        stream.seek(offset)
        data = stream.read(min(PAGE_BYTES, size - offset))
        # A short-line flood must not create tens of thousands of Tk.Text rows.
        # Prefer a line boundary; for giant single lines retain the byte limit.
        if data.count(b'\n') > PAGE_LINES:
            end = 0
            for _ in range(PAGE_LINES):
                end = data.find(b'\n', end) + 1
            data = data[:end]
        elif offset + len(data) < size:
            end = data.rfind(b'\n')
            if end >= 0:
                data = data[:end + 1]
        return data.decode('utf-8', errors='replace'), offset, offset + len(data), size


def tail_offset(path):
    """Seek to a bounded, line-aligned recent tail without reading old logs."""
    with _open_journal(path) as stream:
        size = os.fstat(stream.fileno()).st_size
        if size <= PAGE_BYTES:
            return 0
        start = size - PAGE_BYTES
        stream.seek(start)
        data = stream.read(PAGE_BYTES)
        # Choose the most recent at-most 2,000 complete lines as well as
        # at-most 64 KiB. Compute only within the bounded last-byte window.
        lines = data.count(b'\n')
        if lines > PAGE_LINES:
            offset = len(data)
            for _ in range(PAGE_LINES + 1):
                offset = data.rfind(b'\n', 0, offset)
                if offset < 0:
                    break
            return start + offset + 1 if offset >= 0 else start
        end = data.find(b'\n')
        return start + end + 1 if end >= 0 else start


def preceding_offset(path, current):
    """Find a nearby earlier page using no more than 64 KiB of I/O."""
    if current <= 0:
        return 0
    start = max(0, current - PAGE_BYTES)
    if start == 0:
        return 0
    with _open_journal(path) as stream:
        stream.seek(start)
        data = stream.read(min(PAGE_BYTES, current - start))
        first = data.find(b'\n')
        return min(current, start + first + 1) if first >= 0 else start

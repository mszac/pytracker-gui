# ADR-0030 — low-priority single incremental experiment journal (2026-10-12)

**Context:** v0.2.11 persisted duplicated `console_*.log` and `experiment_*.log` only at completion. A crash before finalization could discard both. PsychoPy must have priority over UI and logging I/O. The user specifically retained the 256-KiB RAM buffer ceiling and rejected 2-second periodic writes.

**Decision:** single on-disk journal with `.log.part` while running and `.log` only after a durable clean finish. One background low-priority writer drains a 256-KiB bounded recent-message FIFO in up to 64-KiB writes, normally after 15 seconds or early at 192 KiB, not more often than about 5 seconds during acquisition. No child stdout read waits for disk. Overrun drops oldest *pending* records and marks the log as interrupted/incomplete, never certified as complete. Failed storage operations cannot change PsychoPy run result. Retain `.part` for cancellation and crash; automated repair is outside scope.

**Alternatives rejected:** per-line synchronized writing, two redundant completed files, unbounded RAM queues, forcing writes every 2 seconds, blocking stdout on file locks, and changing global OS process priority.

**Limits:** No reliable OS-neutral signal that disks are idle; best-effort scheduling and Windows thread priority are used. On power loss the last unflushed segment may be missing. `fsync` on finalization can stall the daemon but does not block acquisition. Preexisting `.part` files are not migrated or repaired.

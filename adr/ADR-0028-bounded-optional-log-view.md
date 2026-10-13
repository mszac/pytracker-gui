# ADR-0028 — Opt-out live log viewer and bounded preview

**Status:** accepted for v0.2.9. **Context:** default automatic log viewer can cost Tk redraw time during lengthy experiments, while the previous `_run_display_lines` list was unbounded. Users need an explicit switch without losing final logs or changing the runner.

**Decision:** use a default-ON, locally persisted Auto-show logs setting. Suppress only automatic popup creation and text updates when OFF. Keep manual Show Logs. Use a 2,000-line/256-KiB bounded preview and a separate 256-KiB RAM-to-temporary-disk spool for the complete ordered GUI log, written to project storage once after session completion. Preserve native `console_*.log` separately. Copy entire log explicitly reads the full source on demand.

**Alternatives rejected:** hiding the window while accumulating unlimited RAM, truncating final logs, writing permanent project logs for every subprocess line, changing process stdout, adding new processes/timers or modifying measurement semantics.

**Risks:** event-queue growth under extreme output is not eliminated, full clipboard copying may temporarily require more RAM, complete GUI log still depends on the final event, OS temp can incur I/O when exceeding its in-memory threshold. Windows/PsychoPy physical validation remains pending.

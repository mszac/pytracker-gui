# ADR-0035 — GUI Documentation and local Environment button width

Date: 2026-10-12. Status: accepted for v0.2.17.

## Decision

1. Preserve each of the four classic v0.2.16 Environment buttons exactly except for horizontal stretching in their existing grid cells (`sticky='ew'`). Tk assigns the column the width requested by the widest button (Load repository in English). Do not use uniform ttk styles, explicit button height/width in character units, change icons, or modify the editor footer.
2. Add an independent, lazy **Manual → GUI Documentation** tab. It indexes only an explicit allowlist of current local pytracker-gui Markdown guides, grouped by English/Polish and by current/feature instructions. No upstream/demo filesystem traversal, project histories, runs, log files or ADR history are indexed.
3. Reuse the existing native Tk markdown formatter and explicit dark `Treeview` colors, with a 1 MiB file bound and plaintext fallback above 256 KiB. No additional threads, packages, timers, network, subprocesses or writes.
4. Preserve the three existing Manual tabs and the `man` link to Index; no YAML commit/navigation semantics are changed.

## Scope and validation

Only `pytracker_gui/app.py`, `pytracker_gui/screens.py`, new `pytracker_gui/gui_docs.py`, release identity, narrowly related current EN/PL guides, ADR/tests and append-only development logs may change. PsychoPy runtime/runner/adapter, incremental writer, storage, Logs, colors, icons, fonts, layout sashes, parameter manual payloads and all other existing source must remain byte-identical with v0.2.16 Documentation Sync.

Physical Windows/HiDPI rendering remains an external validation gate. Verify that all four Environment buttons have equal pixel width in PL and EN and retain their native height/icon/style; verify the four Manual tabs, bounded read-only document selection and parameter deep-link return to Index.

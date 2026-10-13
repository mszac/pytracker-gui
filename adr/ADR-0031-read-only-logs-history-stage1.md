# ADR-0031 — Read-only project/run Logs dashboard (2026-10-12)

Status: accepted for implementation, Windows visual evaluation pending.

## Context

The user wants a lightweight combination of dashboard and hierarchical project/run chooser, replacing the inert Logs placeholder. GUI's responsibility is to preserve console logs and launch configurations, **not** to own or interpret recorded experiment measurements. Stage 1 explicitly excludes the future console-log viewer.

## Decision

Separate a stdlib-only read model (`log_history.py`) from a lazy Tkinter dashboard (`logs_screen.py`). Discover histories via `projects/<project>/experiments/` and strict run directory names. Read immutable run metadata and a bounded set of YAML snapshots only upon selection. Use two nested chooser lists rather than Manual's flat document tree. Render six small cards plus collapsed details; local subdued blue / orange and green / amber journal-status colors. No update timers, other threads, data schema changes or additional file writes. Preserve project selection on refresh.

## Alternatives considered

- SQLite historical index: rejected as unnecessary durable state and migration burden.
- Global theme redesign: rejected because v0.2.6 appearance is approved.
- Reuse Manual Treeview document explorer: rejected because project/run chronology and configuration categories have different UX.
- Load full logs or output.csv for summaries: rejected as outside stage 1 and measurement ownership.
- Proactive periodic scanning: rejected due to resource contention with PsychoPy.

## Caveats

`result.json` status is process-level only, not scientific result validity; `.log.part` denotes incomplete log (which may still be actively recording). Large YAML and JSON receive conservative size limits; malformed saved files produce a visible unavailable-report notice or partial report. The second stage should add chunked `.log`/`.log.part` preview without changing these contracts.

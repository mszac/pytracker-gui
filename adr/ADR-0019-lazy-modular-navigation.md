# ADR-0019 — independent lazily instantiated application screens

Date: 2026-10-11
Status: Accepted for v0.1.8

## Context
The accepted v0.1.7 Experiment editor/launcher has six configuration tabs and is comparatively stable. New features (log browser, diagnostics, statistics) will eventually require separate screens, but adding them to the existing Notebook or eagerly initializing their data readers would increase coupling, UI startup cost and regression risk.

## Decision
Introduce a separate lightweight `AppShell` with top-level navigation and a single screen host; embed the existing `PytrackerGUI` as a persistent Experiment screen. Future module screens are separate `ttk.Frame` classes with no service calls and are created lazily on first selection. Switching uses widget visibility only and does not commit YAML, reload an editor, scan files or affect the experiment subprocess. The shell observes the selected project name and GUI language via existing Tk state/callback; it does not own project profiles or runner lifecycle. Main-window close delegates to the original editor safeguards.

## Alternatives rejected
- Growing the editor's `ttk.Notebook` to include log/diagnostic/statistics tabs: these are separate modules with different lifecycles, not experiment configuration fields.
- Reconstructing the Experiment editor each time: would discard unsaved values and add initialization I/O/CPU latency.
- Separate root windows or embedded Chromium/web UI: unnecessarily heavy and complicates event/process ownership.
- An eager service layer for unopened future modules: unneeded disk I/O and potentially expensive imports.

## Consequences, risks and gates
One additional Tk navigation frame and lightweight project label are present from startup; the three placeholders are absent until selected. Existing Experiment implementation remains its own class and continues unchanged apart from being embeddable under a nested Tk container and emitting a presentation-only language update callback. Independent module implementations can later replace placeholders without touching the launcher. Test lazy construction, no side effects on navigation, PL/EN switching, unsaved invalid YAML, close delegation, and all previous regressions. Physical Windows size/focus/fullscreen behavior and PsychoPy hardware remain external gates.

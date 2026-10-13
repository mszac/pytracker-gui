# ADR-0034 — Restore v0.2.14 action appearance and retain native sash resizing

Status: Accepted for v0.2.16 (2026-10-12).

Context: User rejected v0.2.15 equal-sized action buttons as visually worse, while explicitly retaining adjustable panel borders. Three specific missing icons were requested.

Decision: Rebuild **from exact v0.2.14**, not from the v0.2.15 release tree. Port only two visual layout changes implementing three `tk.PanedWindow` boundaries. Preserve the original single-row editor action footer and native `TButton` styles, widths, and padding. Add opt-in 20px icons only to Check Python, Detect layout, and Apply changes, using the already bundled assets; no new image files, package dependencies, filesystem writes, render timers or settings persistence.

Rejected alternatives: Retain the equal-sized action controls, two-row action grouping, alter global ttk styles, implement resize tracking/persistence, or modify workflow/runtime code.

Constraints: Original v0.2.14 footer can be wider than a user-reduced editor pane; this is intentionally unchanged rather than silently reintroducing unrequested visual changes. Minima prevent total collapse. Behavior to be checked on real Windows/HiDPI.

Verification: Targeted Tk tests assert 3 icon placements, original action hierarchy, three draggable sash boundaries, language changes, run history, minimum sizes and navigation. Full pre-existing suites plus exact-parent patch and manifests validate unchanged code.

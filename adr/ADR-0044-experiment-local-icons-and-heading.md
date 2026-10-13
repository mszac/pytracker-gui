# ADR-0044 — Experiment-only icon default and stable panel title

**Date:** 2026-10-12. **Parent:** exact v0.2.26 Full.

**Decision:** Defer native title-bar styling entirely, because the user explicitly rejected Windows API-specific code. Reuse the cached `theme.icon(..., color=...)` tint helper to give unselected icons in the Experiment view local factory tint `#A46628` while leaving global `ICON_COLOR` and the app's editable palette unchanged. An explicitly saved user-wide icon color overrides this local default; selected orange and ink-on-accent variants are not recolored. Replace only the changing demo caption with static `Experiment setup` in the existing `Heading.TLabel` style.

**Alternatives avoided:** changing global `ICON_COLOR` (would recolor other screens); adding a GUI Settings color key (out of scope); duplicating icons as new PNG assets; native Windows title-bar APIs; rebuilding the header or navigation widgets. No new threads/timers/runtime dependencies.

**Validation:** focused Tk icon/cache/title/selection tests, inherited regressions, exact-parent frozen-scope and fresh-archive manifest checks. Real Windows/HiDPI/hardware testing remains external.

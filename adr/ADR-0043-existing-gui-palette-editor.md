# ADR-0043 — Use existing theme palette parameters in GUI Settings

**Date:** 2026-10-12. **Status:** accepted in v0.2.26.

**Decision:** Keep `theme.ICON_COLOR` and every existing `theme.COLORS` member as the only editable GUI color parameters. The idle-icon default is RGB(34,40,155) / `#22289B`; selected orange PNG assets retain their existing behavior. Expose these values in a single bottom GUI Settings panel. Persist under the identical names `ICON_COLOR` and `COLORS` within the existing private settings file, using the existing atomic writer. Validate full hex input before writing and do not accept other keys.

**Reason:** The user asked for configurable existing colors, not an additional palette abstraction. Applying saved values once before `apply_theme` / widget construction is consistent across native ttk style, existing custom Tk widgets and lazy icon cache, with no per-frame processing during PsychoPy execution. A restart-only apply avoids complex partial live reconfiguration and associated risk. The Settings screen uses a native scrollable canvas only because the bottom panel would otherwise be inaccessible on small displays.

**Tradeoffs:** Dynamic live preview is not supported. Users can reduce text/background contrast; Restore defaults (then Save colors, restart) provides recovery. Runtime icon PNG sources, graphics and all experiment/runner/storage code remain frozen. Tests run under Linux/Xvfb; physical Windows/HiDPI is pending.

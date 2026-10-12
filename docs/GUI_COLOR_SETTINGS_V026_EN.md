# v0.2.26 — Existing GUI palette editor and new icon default

**Parent:** exact v0.2.25 release. The functional scope is limited to icon tint and the existing GUI Settings screen.

## New idle icon default

`pytracker_gui/theme.py` still owns the single existing user-visible `ICON_COLOR` parameter. Its default is `#22289B` (RGB 34, 40, 155). Selected navigation/notebook icons remain the original orange `*-orange.png` assets, with orange labels. Ink icons on orange action buttons remain untouched. The alpha-mask renderer, per-root cache, original assets, and all image dashboard PNGs remain unchanged.

## Bottom palette panel

**GUI Settings → Interface colors** exposes the existing `ICON_COLOR` and every existing `COLORS` dictionary key (`window`, `surface`, `surface_alt`, `field`, `hover`, `border`, `text`, `muted`, `accent`, `accent_hover`, `accent_text`, `selection`, `success`). All entries accept strict `#RRGGBB` values. No additional color parameter was introduced. A small swatch shows the currently loaded/saved value; **Save colors** persists all entries atomically in the application's already-existing private `settings.json` using the existing parameter names `ICON_COLOR` and `COLORS`. **Restore defaults** fills the inputs with the built-in values; use Save colors to persist the reset. Invalid values stop the entire save, leaving settings unchanged.

**Restart is required** before color edits take effect. Startup reads the same settings file once, validates only existing known parameters, then installs the palette before any themed widgets/icons are created. Corrupt/unknown parameters do not override defaults. This avoids Tk recoloring, periodic work, or cache thrashing during an active PsychoPy session. The native vertically scrollable GUI Settings content allows access to the bottom card even with a small application window.

The user can change orange palette entries deliberately, but by default all existing orange accents stay byte-identical to v0.2.25. No Pillow runtime dependency, network calls, background threads or polling are introduced. Experiment/YAML, GUI logs, history and session measurement binding are unchanged.

## Validation boundary

Targeted checks cover the new icon value, orange selected icons, valid/invalid inputs, atomic persistence, restart application, defaults reset, a smaller window and previous GUI Settings window-size preference. Linux Python 3.13/Xvfb automated validation is not a substitute for a Windows/HiDPI physical check.

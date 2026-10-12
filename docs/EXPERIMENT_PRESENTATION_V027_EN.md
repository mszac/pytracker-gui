# v0.2.27 — Experiment presentation only

**Exact parent:** v0.2.26 Full. This release deliberately does not change the native Windows title bar or introduce a title-bar setting or Windows API call.

## Inactive icons within Experiment

Inactive small icons in the **Experiment** screen (including Monitor, YAML and action buttons) use `#A46628` by default. Selected notebook icons continue using their original orange artwork, and `active='ink'` icons on filled orange buttons retain their dark artwork. This is a scoped default: the existing application-wide `ICON_COLOR` factory default (`#22289B`), `COLORS`, other screens, GUI Settings and top navigation are unchanged. If a user has explicitly saved a custom `ICON_COLOR` in GUI Settings, that preference continues to take precedence in Experiment.

The implementation reuses the existing one-time color rendering and per-Tk-root cache. It adds no new runtime dependency, polling, thread, file write, runtime image resizing or color setting.

## Static panel heading

The dynamic starter demo label (for example, `Test Demo · EN`) at the top of the right-hand Experiment panel is replaced by the fixed `Experiment setup` caption using the existing `Heading.TLabel` style, visually matching the nearby Starter projects heading. Switching demos or changing the application language no longer overwrites this caption. The separate existing demo description, Block and Project controls and all selection/launch logic are unchanged.

## Scope and test boundary

The only production paths changed relative to v0.2.26 are `pytracker_gui/theme.py`, `pytracker_gui/app.py`, `pytracker_gui/__init__.py` and `VERSION`. Original PNGs and the remaining runtime files remain byte-identical. The one prior icon-state assertion is adjusted for the explicitly local color, and a focused test verifies orange active icons, global navigation defaults, heading stability across demo switches, and custom `ICON_COLOR` overrides.

Linux/Xvfb regression is not a substitute for real Windows/HiDPI visual testing. No PsychoPy, Tobii or measurement hardware test is performed by this styling iteration.

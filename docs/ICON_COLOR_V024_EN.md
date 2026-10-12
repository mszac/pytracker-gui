# Icon-only color parameter — v0.2.24

This release changes only the color of the small Tk/ttk navigation, Experiment tab, and action-button icons to light burgundy **`#C77D8F`**. Orange selection text, focus highlights, orange action buttons, all other global palette values, the project logo, and the four photographic Home tiles are **unchanged**. Dark `ink` icons on orange buttons remain dark for contrast.

The separate `ICON_COLOR = '#C77D8F'` parameter lives in `pytracker_gui/theme.py`. It accepts a `#RRGGBB` hexadecimal value; changing the parameter before constructing the GUI changes the tint of all small interface icons. This prepares future integration into GUI Settings, but **does not yet add a GUI setting, persist a user preference or recolor running widgets automatically**.

To keep runtime light, a 16 KiB package-local `pytracker_gui/assets/icon-alpha-masks.json` stores the existing 40×40 anti-aliased icon alpha silhouettes compressed with the Python standard library. Each icon/color/state is converted to a small in-memory RGBA PNG only on its first request and cached for the lifetime of its Tk root. No Pillow, graphics redraw loop, timer, background worker or per-frame resizing is required. The original icon PNGs and image-backed dashboard assets remain intact.

Only the presentation layer and release identity changed. PsychoPy, experiment workflows, data/configuration persistence, Logs, Manual, GUI Settings, navigation routes and window geometry remain unchanged. Hardware Windows/HiDPI verification is a separate gate.

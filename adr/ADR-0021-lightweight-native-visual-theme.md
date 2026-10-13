# ADR-0021 — Lightweight static charcoal/orange Tk appearance

- **Status:** accepted, v0.2.0, 2026-10-11.
- **Context:** the functional v0.1.9 editor is stable but its default native Tk styling looks dated. The approved mockup uses dark charcoal surfaces, restrained orange emphasis and cleaner navigation/icons. Performance and behavior must not change.
- **Decision:** retain tkinter/ttk and the existing widget tree, install a once-per-root `clam` style palette, style the few classic Tk controls explicitly and attach small packaged 20×20 PNG icons. Cache `PhotoImage` instances in the root lifetime. Keep all other runtime and storage components unchanged.
- **Presentation boundary:** only `app.py`, `shell.py`, `help_widgets.py`, `theme.py`, packaged icon assets, tests, release documentation and version identity are modified. No new GUI screens, data features, theme selection, runtime dependencies, timers or worker processes.
- **Alternatives rejected:** Qt/Chromium (extra runtime, packaging and memory), Tkinter replacement/widget rewrite (regression risk), ttkbootstrap/other third-party themes (unnecessary dependency), animated canvases (rendering overhead).
- **Risks:** native OS titlebar remains platform-colored; Windows DPI and ttk theme variation require physical inspection. Small screens may use list scrollbars as before. Modern imagery does not guarantee exact Figma-style rounded corners.
- **Validation gate:** all inherited tests, targeted visual invariants, real Tk screenshot, fresh-unpack checks, exact direct-parent patch and byte-identical audit of runtime/storage/demo code.

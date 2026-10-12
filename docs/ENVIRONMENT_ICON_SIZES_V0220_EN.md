# v0.2.20 — Environment icon sizes only

The application retains the v0.2.19 UI layout, style, button placement, labels and functions. In **Experiment → Environment and repositories** only two icons change:

- **Save paths:** existing 40×40 image canvas remains the same; the save symbol is enlarged *inside* that canvas and remains cached in the Tk root. The other save icons in the app are unchanged.
- **Detect layout:** use the packaged full-size 40×40 folder icon, the same icon as **Load repository**, instead of the former 20×20 reduced version.

The **Check Python** icon is still 20×20. All Environment buttons keep their existing style and equal column widths. There is no Pillow requirement at GUI runtime, image resizing timer, new thread or new experimental workflow. No other module, YAML, logs, projects, Manual or dashboard functionality changes. Visual confirmation on physical Windows/HiDPI is pending.

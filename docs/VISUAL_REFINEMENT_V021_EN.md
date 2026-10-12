# pytracker-gui v0.2.1 — visual refinement and module dashboard

## Scope
Presentation and navigation only. The Experiment screen, forms, PsychoPy launcher,
YAML editor, profiles, project storage and log history remain functionally unchanged.

- The original `◈` mark is back with a larger 17 pt Tk-styled `pytracker-gui` brand at
  the top. Clicking the mark or the name opens a module chooser dashboard.
- The chooser has four tiles: Experiment, Logs, Diagnostics, and Statistics. Tile
  selection uses **the same screen-switching path** as the top navigation controls.
  The dashboard is created lazily on first use and reused thereafter.
- The orange accent is lighter (`#ff9d45`), with matching hover/selection shades.
- Navigation/action PNG icons have been regenerated at 28×28 px instead of 20×20 px.
  No runtime resampling, graphics framework or dependency is needed.
- Horizontal inset for the **selected** configuration tab is halved from 12 to 6 px.
  Inactive-tab padding and existing form text sizes are preserved.

## Performance and boundaries
The dashboard reads no logs, datasets or project folders and creates no timers,
threads or subprocesses. PNG assets remain cached per Tk root. Returning to Experiment
preserves its widgets, unsaved YAML and active session. Logs, Diagnostics and Statistics
are still separate, lazy placeholders; no new data analysis features have been added.

## Validation
Tested with Tkinter on Linux/Xvfb. Captured real-window previews are
`docs/images/v021-dashboard-xvfb.png` and `docs/images/v021-experiment-xvfb.png`.
Windows-specific DPI behaviour still needs physical testing. Higher-resolution icons
do not change Windows' native font rasterization.

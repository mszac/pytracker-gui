# v0.2.25 — Darker burgundy idle icons; orange selected icons

Small icons that are **not selected** use `pytracker_gui/theme.py` `ICON_COLOR = '#A9526B'` (formerly `#C77D8F`). This remains the sole future-configurable icon tint parameter; it is not yet an interactive GUI Settings preference.

The **selected** navigation item and Experiment notebook tab now use the existing packaged `*-orange.png` variant, restoring orange icon alongside the orange selected label. Filled orange action buttons continue using their dark `*-ink.png` icon variant. Each asset is cached per Tk root; only unselected icons are tinted from the previously bundled alpha masks, once per distinct icon/color.

No changes to orange style constants, focus/selection behavior, panel dimensions, labels, image dashboard, experiment launcher, log persistence, or configuration formats. Windows/HiDPI appearance remains to be checked on the target system.

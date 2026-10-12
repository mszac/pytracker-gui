# v0.2.16 — original v0.2.14 buttons with resizable panels

## Scope and authority

The **exact v0.2.14 archive** is the direct source baseline. v0.2.15 uniform action-button sizes, forced equal widths, two-row editor footer, globally downsized group icons, and `ExperimentAction.*` styles are **not inherited**. Default button layout, original v0.2.14 sizes, and the global palette remain intact.

Only **three** pre-existing button icons are added: **Check Python** (`diagnostics`), **Detect layout** (`folder`), and **Apply changes** (`check`). Original bundled 40px PNG assets are cached as 20×20 native `PhotoImage.subsample(2, 2)` objects. All other action icons and styling remain identical to v0.2.14.

Three `tk.PanedWindow` separators are selectively retained from v0.2.15: Experiment starter projects / configuration editor (minimum widths 220/650px); Logs selector / report or console (228/390px); and Logs projects / runs vertically (minimum heights 120/140px). Sashes stay adjustable during screen navigation, without persisted sizes, polling, threads or third-party dependencies.

`theme.py`, Manual, project and YAML storage, PsychoPy and subprocess runtime, journal writer, read-only logs, and other features are byte-frozen to exact v0.2.14. Only the two scoped GUI modules, version, tests and development documentation differ.

## Windows acceptance

Confirm the natural, unequal button sizes and original single-row footer; inspect three new icons at Windows HiDPI; drag all three separator handles at normal and minimum window sizes. The original one-row footer may require horizontal space if the editor is narrowed. Physical Windows/PsychoPy/Tobii tests have not been executed here.

Linux Python3.13/Xvfb regression groups: **181 test executions PASS**, including **7/7** targeted tests. Manifest/patch/fresh ZIP verified by release packaging.

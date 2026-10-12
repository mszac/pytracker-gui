# v0.2.22 — Logs home tile and GUI Settings

This iteration is limited to the approved home **Logs** image and the new **GUI Settings** navigation page, positioned immediately to the right of Manual. The other four dashboard actions and their fixed 546×365-pixel geometry are unchanged.

## GUI Settings, first version

The page is constructed on demand, without background workers or periodic filesystem scans. Its compact read-only rows display the GUI data directory, project history directory, current demo/upstream repository paths, Python interpreter, interface/tooltip language, Auto-show Logs state, and the single incremental console journal contract. Repository paths still have one editing and persistence owner: **Experiment → Environment**.

The page also permits selecting a default window size from **940×650**, **1100×800**, **1300×960**, **1429×1097** (default), and **1600×1000**. Clicking **Save window size** writes only `window_size` to the existing GUI-local `settings.json`, preserving the other settings and updating the Experiment screen's cached settings dictionary. The new size applies on the **next** application start; it does not resize the current session. Screen-space clamping still applies. The selection does not edit experiment profiles, YAML, results, source repositories, or logs.

The Logs background was resized from the exact user-approved 1448×1086 image to the existing 546×365 home tile; no other home asset or navigation action was changed.

## Validation

Targeted Tk/Xvfb tests cover default size, persisted re-launch size, lazy navigation, read-only paths, localization and unchanged four home actions. Target build and physical Windows/HiDPI remain separate checks.

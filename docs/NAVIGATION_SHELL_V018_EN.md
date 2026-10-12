# Modular navigation — pytracker-gui v0.1.8

## Scope
A persistent **top-level navigation bar** switches between four independent screens: **Experiment**, **Logs**, **Diagnostics**, and **Statistics**. These are *application modules*, not replacements for the existing six Experiment tabs (Data, Monitor, Appearance, Instructions, YAML, Launch). Polish remains the default UI language; navigation labels, placeholders, and project context also support English.

## What works
- **Experiment**: the unchanged configuration and launch interface, including profiles, help icons, `Experiment log` popup, runtime controls, and validation.
- **Logs**: an independent placeholder for a later run-history viewer. It does not scan project directories or automatically open any files.
- **Diagnostics**: an independent placeholder for future reports. Existing Check Python and Validate configuration functions remain within Experiment.
- **Statistics**: an independent placeholder; it does not compute statistics, read CSV results, or import analysis frameworks.
- The **project context** in the navigation bar displays the selected project name. It is read-only and does not duplicate project state.

## Architecture and performance contract
`pytracker_gui/shell.py` implements `AppShell`, which owns only the navigation controls, project label, and screen host. The existing `PytrackerGUI` class in `pytracker_gui/app.py` stays responsible for all Experiment features and is mounted as the `experiment` screen. `pytracker_gui/screens.py` contains the independently implemented placeholder screens. No cross-screen process-management logic is introduced.

Experiment is created once at startup because it is the initial view. Every additional screen is constructed **only on first selection** and then reused on subsequent visits (`pack_forget`/`pack`, never rebuild). Switching screens causes **no** profile save, edit commit, YAML validation, process start/stop, folder scans, new threads, or `after()` callbacks. Unsaved field or YAML text remains in the same editor widget while switching. Any invalid YAML will be checked by the existing apply/tab-change/launch workflow, not by navigation.

Closing the main window delegates to the unchanged `PytrackerGUI.request_close()` flow, including the existing active-run and unsaved-change safeguards. The existing Experiment log popup remains owned by Experiment.

## Starting and verifying
In the canonical `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui,projects}` layout:

```bash
conda activate pytracker-env
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Select Logs, Diagnostics, Statistics, then return to Experiment. Switch PL/EN, check unsaved YAML remains intact, and confirm that the Launch tab is unchanged. On Windows, also check the layout at smaller resolutions and run an existing demonstration. Automated Linux/Xvfb coverage uses `python -m unittest discover -s tests -v`.

## Deliberately unchanged and deferred
No changes to upstream, demo adapters, process runner, profiles, YAML, `projects/` storage, configuration snapshots, run IDs, log formats, validators, or the six existing tabs. **Log browsing, diagnostic tools and statistical analysis are not implemented in this release.** They will be delivered independently in later versions with separate tests.

Actual Tkinter screenshot from the Linux/Xvfb test: [`docs/images/v018-navigation-xvfb.png`](images/v018-navigation-xvfb.png). This does not constitute a physical Windows display validation.

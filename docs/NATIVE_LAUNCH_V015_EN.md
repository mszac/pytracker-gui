# pytracker-gui v0.1.5 — launching existing demonstrations (Windows / Linux)

## Scope

Version v0.1.5 adds **Start demo** and **Stop demo** for the existing seven demonstration variants and eight YAML configurations. Time-Series Noise runs **Machine → PV** as two separate sequential processes. The GUI does not create new experiments, modify ioHub YAML internals, launch Docker, or modify either `sbobek/tobii-pytracker` or `mszac/tobii-pytracker-demo` source repository.

## Required layout

```
tobii-pytracker/                  # git clone sbobek/tobii-pytracker
├── src/tobii_pytracker/
├── configs/
├── tobii-pytracker-demo/         # git clone mszac/tobii-pytracker-demo
│   ├── examples/
│   └── tools/demo_runtime_adapters.py
└── pytracker-gui/               # this independent project, distributed as ZIP for now
    └── run_gui.py
```

Activate your working `pytracker-env` (Python 3.10). The chosen **experiment interpreter** must have Python 3.10, `tobii_pytracker`, and `psychopy`; otherwise, the GUI blocks launch. Set valid upstream, demo, Python, and ioHub YAML paths. `--check-layout` checks source locations only, not PsychoPy readiness or a physical eye tracker.

## How to launch

1. Start the GUI and select one of the seven demo variants; its YAML or saved profile will load.
2. Edit Data, Monitor, Appearance, Instructions, or raw YAML. **Apply changes** commits the current edit in memory, **Save profile** persists the profile privately, and **Export YAML** exports a separate copy. None of these commands starts PsychoPy.
3. Choose **NO_GAZE**, **MOUSEGAZE**, or **TOBII**, and select the appropriate ioHub YAML. NO_GAZE still permits mouse responses. TOBII requires a connected compatible device and configuration; preflight does not detect physical readiness.
4. On **Launch**, choose the trial count *for the current block*, log level, and optional Voice/Raw data. Raw data requires active gaze.
5. Click **Start demo**. The GUI commits the active edit, probes the interpreter, checks source paths/YAML/data files, and snapshots current YAML for each block outside the repositories.
6. The run log opens in a separate window. **Stop demo** terminates the current experiment process and its descendants; an interrupted session may contain partial data.

Avoid starting `run-demo.sh` simultaneously with a GUI run: the two sessions could contend for the eye tracker, display, or output directory. The GUI prevents two sessions being launched from the same window.

## Runtime and files

The Tkinter GUI never imports PsychoPy or the demo adapters. It starts `pytracker_gui.launch_child` with the selected Python 3.10 as an isolated child process and sets the working directory to `tobii-pytracker-demo`. UX A/B, Text Search, and Image Semantic use the original `tools/demo_runtime_adapters.py`; gaze, voice, raw data, trial count, logging level, and YAML filenames are passed dynamically to upstream `main.main`.

Each launch creates an application-private run directory such as Windows `%LOCALAPPDATA%/pytracker-gui/runs/<timestamp>_<id>` or Linux `~/.config/pytracker-gui/runs/<timestamp>_<id>` (override the root with `PYTRACKER_GUI_HOME`). It stores `run.json`, one YAML per block, `console.log`, and `result.json`. Original source YAML and code are never overwritten. The experimental data go to the `output.folder` specified in YAML; relative paths resolve against the demo repository root.

## Result meanings

- **PROCESS COMPLETE — COLLECTION VALIDATED:** all blocks exit with code 0 and the original collection validator passes for each block. This is not independent certification of the connected Tobii hardware.
- **PROCESS COMPLETE — COLLECTION NOT VERIFIED:** all blocks exit with code 0, but original collection validation was skipped (e.g., NO_GAZE, partial trials, changed stimulus dataset/output structure, or missing validator).
- **FAILED:** the process, adapter, or validator fails; subsequent Time-Series blocks are not started.
- **CANCELLED:** the user stopped the run and data may be incomplete.

Original demo validators assume a full trial count and the original stimulus dataset. The GUI never reports their success for unsupported changes. No physical PsychoPy/Tobii session was executed in the v0.1.5 development environment: automated tests use fake subprocesses and a mock upstream runtime.

## Windows / Git Bash smoke test

```bash
cd /d/pytracker/tobii-pytracker
conda activate pytracker-env
python --version
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Begin with **Test Demo [EN]**, MOUSEGAZE, three trials, and its default dataset. Before attempting hardware Tobii, establish the MouseGaze path. When reporting any failure, include `result.json`, `console.log`, and `git rev-parse HEAD` from both repositories.

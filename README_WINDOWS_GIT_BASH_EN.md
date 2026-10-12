# pytracker-gui v0.2.17 — Windows / Git Bash setup and update

This is the **current English installation guide**. Polish edition: [README_WINDOWS_GIT_BASH_PL.md](README_WINDOWS_GIT_BASH_PL.md). For features and day-to-day operation, read the [English user guide](docs/USER_GUIDE_EN.md). Earlier versioned documentation files remain available as historical records.

## 1. Requirements and repository layout

Use Git for Windows, Git Bash, a working Conda `pytracker-env` with **Python 3.10 for the experiment runtime**, and the two independent checkouts:

```text
tobii-pytracker/                       # sbobek/tobii-pytracker
├── src/tobii_pytracker/
├── configs/
├── tobii-pytracker-demo/             # mszac/tobii-pytracker-demo
│   ├── examples/
│   └── tools/
├── pytracker-gui/                   # ZIP distribution of this GUI
└── projects/                        # GUI projects/history: keep during upgrades
```

Example location: `E:\pytracker\tobii-pytracker`. If the repositories are missing, clone them from Git Bash:

```bash
mkdir -p /e/pytracker
cd /e/pytracker
git clone https://github.com/sbobek/tobii-pytracker.git tobii-pytracker
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git tobii-pytracker-demo
```

**Do not re-clone over existing directories.** `tobii-pytracker-demo` is the expected demo checkout; another similarly named example repository is not a substitute. Keep the original source repositories unmodified.

## 2. Install or update the GUI ZIP

The full ZIP has a top-level `pytracker-gui/` directory. Download the supplied `pytracker-gui-v0.2.17-gui-documentation.zip` to Windows **Downloads**. If you are replacing a previous GUI release, **back up `pytracker-gui/` first**, and ensure there is no active experiment. **Never delete `projects/`**, which is separate from GUI source.

```bash
cd /e/pytracker/tobii-pytracker
# Back up an existing GUI folder only if it is present:
if [ -d pytracker-gui ]; then
  cp -a pytracker-gui "$HOME/pytracker-gui-backup"
fi
GUI_ZIP_WIN="$(cygpath -w "$HOME/Downloads/pytracker-gui-v0.2.17-gui-documentation.zip")"
ROOT_WIN="$(cygpath -w "$PWD")"
powershell.exe -NoProfile -Command \
  "Expand-Archive -LiteralPath '$GUI_ZIP_WIN' -DestinationPath '$ROOT_WIN' -Force"
```

Change `/e/pytracker` to your location if needed. The filename above belongs to the **v0.2.17 GUI Documentation package**; for another package use its actual downloaded filename. Upgrades do not require overwriting upstream/demo checkouts or project histories.

## 3. Python environment and preflight

```bash
cd /e/pytracker/tobii-pytracker
conda activate pytracker-env
python --version
python -m pip install -r pytracker-gui/requirements-gui.txt
python -m tkinter
python pytracker-gui/run_gui.py --check-layout
```

Close the small Tk test window opened by `python -m tkinter`. If Conda is not available in Git Bash, initialize its Bash support and reopen the shell, or use `conda run --no-capture-output -n pytracker-env python` in place of `python`. The GUI's small dependency set does not by itself install/configure PsychoPy, ioHub or a physical tracker. The **experiment interpreter** must have the original framework and the required research dependencies installed.

`--check-layout` checks the expected paths and demo source files. It cannot certify the availability of a compatible eye tracker, PsychoPy GUI/display operation or measurement correctness.

## 4. Start, configure and run

```bash
cd /e/pytracker/tobii-pytracker
conda activate pytracker-env
python pytracker-gui/run_gui.py
```

In **Experiment**, check `Demo root`, `Upstream`, `Python`, and the ioHub YAML path; **Detect layout** and **Check Python** are available. Choose or create a GUI **Project**, load one of the seven existing demo variants, edit YAML/forms, then **Apply changes** and optionally **Save profile**. Choose the gaze mode and runtime parameters in **Launch**, and use **Start demo** / **Stop demo**. The GUI launches an isolated child Python/PsychoPy process rather than modifying original repositories.

**Auto-show logs** defaults to ON. Disable it for long sessions if you do not want the pop-up console to render automatically; logging continues. Each run has an incremental `experiment_*.log.part` which becomes `.log` after clean, complete finalization. A `.part` can indicate an interrupted/incomplete history; its repair is not implemented yet. The **Logs** screen selects a project/run, displays the saved settings, and can read console journals in small pages. Measurement output remains the responsibility of the original experimental code.

The **Manual** screen has Index, upstream RST Documentation, and a grouped Demo Project Documentation tree. **Statistics** remains a placeholder. Panel boundaries in Experiment/Logs can be dragged, but their positions are not saved between application launches. More detail: [USER_GUIDE_EN.md](docs/USER_GUIDE_EN.md).

## 5. Run history and original baseline comparison

GUI histories are stored in `tobii-pytracker/projects/<name>/experiments/<YYYYMMDD_HHMMSS>_<ID>/`, not the historical `runs/` folder. Each run contains configuration snapshots and metadata (`run.json`, `result.json`); the GUI's single console journal is `.log.part` during execution. The code of the selected demo owns the actual experiment measurements and writes them below the configured output root, in isolated per-run directories. **Do not erase or rename a run folder while it is active.**

For an *independent baseline* using the original demo configuration, you can launch:

```bash
cd /e/pytracker/tobii-pytracker
bash tobii-pytracker-demo/tools/run-demo.sh test_demo
```

This command **does not use a saved GUI project profile**. Avoid simultaneous baseline/GUI acquisition on the same device or output path.

## 6. Checks and troubleshooting

From `pytracker-gui/`, optional source checks include `python -m unittest discover -s tests -v` and `python tools/render_parameter_manual.py --check`. A test suite may need a graphical session for its Tk tests. If the launcher reports a problem, check the selected research Python interpreter, project snapshots, `result.json` and the run's `.log` or `.log.part` first.

- **Conda unavailable:** initialize Git Bash for Conda or use `conda run`.
- **Tk does not open:** run `python -m tkinter` in the same environment.
- **LAYOUT BLOCK:** check the original and nested demo repository paths before starting a study.
- **Missing `ruamel.yaml`:** reinstall `pytracker-gui/requirements-gui.txt` with the interpreter used to start the GUI.
- **PsychoPy/Tobii launch failure:** verify the *experiment interpreter*, its dependencies and ioHub configuration; a layout check alone is insufficient.
- **`.log.part` remains:** the run may have been interrupted or log persistence incomplete. Retain the file; automatic repair is not available.

**Validation caveat:** the development regression tests were performed on Linux/Xvfb. Real Windows HiDPI, PsychoPy and Tobii acquisition still require local verification.

**Bilingual parameter references:** [PARAMETER_MANUAL_EN.md](docs/PARAMETER_MANUAL_EN.md) and [PARAMETER_MANUAL_PL.md](docs/PARAMETER_MANUAL_PL.md). The archived **v0.1.4** installation instructions described a configuration-only GUI; that is no longer the v0.2.17 scope.

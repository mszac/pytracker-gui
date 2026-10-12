# pytracker-gui v0.1.1 — canonical Git Bash setup (Windows)

**Current instructions supersede v0.1.0's external-sibling examples.** Original history remains in `docs/INSTALL_AND_USE_V010.md`.

## A. Clone real public repositories in the required nested layout

Choose one absolute workspace, for instance `D:\pytracker` (`/d/pytracker` in Git Bash). Replace it with `~/pytracker` if there is no D: volume. Do **not** run `rm -rf` on an existing checkout. Do **not** clone the fork `tobii-pytracker-examples`: the correct demo is `mszac/tobii-pytracker-demo`.

```bash
mkdir -p /d/pytracker
cd /d/pytracker
# Only if directory 'tobii-pytracker' is absent:
git clone https://github.com/sbobek/tobii-pytracker.git tobii-pytracker
cd tobii-pytracker
# Only if directory 'tobii-pytracker-demo' is absent:
git clone https://github.com/mszac/tobii-pytracker-demo.git tobii-pytracker-demo

# Record exact Git revisions on your Windows installation:
git rev-parse HEAD
git -C tobii-pytracker-demo rev-parse HEAD
```

## B. Install the independent GUI from the released ZIP

We have not published `pytracker-gui` to a remote Git repository. The next line extracts the released ZIP into the upstream root; the ZIP **already contains** a single top-level `pytracker-gui/` directory. Do not extract into a second `pytracker-gui` directory.

Copy `pytracker-gui-v0.1.1-nested-repository-layout.zip` to your Windows Downloads folder, and from the `tobii-pytracker` root run:

```bash
GUI_ZIP_WIN="$(cygpath -w "$HOME/Downloads/pytracker-gui-v0.1.1-nested-repository-layout.zip")"
UPSTREAM_WIN="$(cygpath -w "$PWD")"
powershell.exe -NoProfile -Command "Expand-Archive -LiteralPath '$GUI_ZIP_WIN' -DestinationPath '$UPSTREAM_WIN' -Force"
test -f pytracker-gui/run_gui.py && echo 'GUI file present'
```

Final structure:

```text
tobii-pytracker/                   # Git: sbobek/tobii-pytracker
    pyproject.toml
    src/tobii_pytracker/
    configs/mouse_eyetracker_config.yaml
    tobii-pytracker-demo/         # nested Git: mszac/tobii-pytracker-demo
        tools/run-demo.sh
        examples/... (7 variants / 8 YAML files)
    pytracker-gui/                # ZIP now, future standalone Git repo
        run_gui.py
        pytracker_gui/
        tests/
```

When our GUI Git remote exists, future installation will replace only the ZIP step with `git clone <future-official-GUI-URL> pytracker-gui`. **No public GUI URL is claimed today.**

## C. Run on existing Conda environment (Python 3.10)

```bash
# From /d/pytracker/tobii-pytracker:
conda activate pytracker-env
python --version
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

`--check-layout` works without an active graphical display, PsychoPy or Tobii. Expect `LAYOUT PASS` if upstream, demo and eight YAML files exist. It reports `BLOCK` and exits with status 2 if the structure is incomplete. `run_gui.py` works from the upstream directory **or another CWD**, because paths are derived from its actual installed location.

If `conda activate` is not available in Git Bash, use Anaconda Prompt to initialize Conda for Bash (`conda init bash`, then restart Git Bash), or replace the last four Python calls with `conda run --no-capture-output -n pytracker-env python ...`.

If upstream has not yet been installed into your `pytracker-env`, inside the upstream root run `python -m pip install .` as per the original upstream installation guide. Do not recreate or delete the existing Conda environment just to run this GUI.

## D. First-run GUI validation

- Default Upstream = parent of installed `pytracker-gui`; Default Demo root = its `tobii-pytracker-demo` neighbor, auto-discovered without choosing either manually.
- Use **Wykryj układ** to restore the canonical paths if you selected another directory earlier, then **Wczytaj repo**.
- Default MouseGaze ioHub points to `<upstream>/configs/mouse_eyetracker_config.yaml`; Tobii uses `<upstream>/configs/eyetracker_config.yaml`.
- Choose one of seven demo variants. Time-Series has two YAML blocks (Machine / PV). Check and save configuration profiles without changing either Git checkout.
- **Sprawdź konfigurację** is static; **Podgląd kontraktu uruchomienia** shows the original dispatcher command but does not run it. No GUI runtime experiment launch exists in v0.1.1.

Optional manual baseline of the original demo, independently of GUI-generated profiles:

```bash
# From tobii-pytracker/ and with pytracker-env available:
bash tobii-pytracker-demo/tools/run-demo.sh test_demo
```

**This manual command uses the existing demo scripts and their own original settings, NOT the edited GUI profile.** Before hardware studies check PsychoPy/ioHub, the selected monitor, eye-tracker and permissions. If the baseline command fails, consult the demo repo `README_TESTING.md` and `tools/preflight.py`.

## E. Validate code without running experiments

```bash
cd pytracker-gui
python -m unittest discover -s tests -v
```

Windows GUI, ioHub, PsychoPy and physical tracker integration still require user machine checks; the release cannot claim them based on Linux tests.

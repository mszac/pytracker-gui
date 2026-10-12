# pytracker-gui v0.1.6 — demo adapter loading and full log copy (Windows / Linux)

## Root cause and fix

Version v0.1.5 loaded special demo adapters with `from tools.demo_runtime_adapters import ...`. The original `tobii-pytracker-demo/tools` directory does not require an `__init__.py`, and Python can resolve the generic `tools` name to an unrelated installed package. This produced `ModuleNotFoundError: No module named 'tools.demo_runtime_adapters'` **before** PsychoPy started for **UX A/B Text, Text Search, and Image Semantic**. Test Demo and Time-Series do not load these adapters and therefore do not reproduce this specific error.

In v0.1.6 the child process loads the adapter from the **selected demo checkout** at `<Demo root>/tools/demo_runtime_adapters.py` using `importlib.util.spec_from_file_location`. This avoids ambiguity with any installed `tools` package. The GUI checks that the adapter file exists **before** starting a demo that requires it. The log shows `[ADAPTER] Loaded from ...` and `[ADAPTER] Applied text/image adapter`. The source repositories remain unchanged, and no adapter copy is bundled into the GUI.

## Copying the complete visible experiment log

The **Experiment log** window (PL: **Dziennik eksperymentu**) now includes **Copy entire log** (PL: **Kopiuj cały log**). It copies the complete accumulated contents of the log window to the system clipboard, not just selected text. This includes `[RUN]`, `[STATUS]`, `[PROCESS]`, `[COLLECTION]`, and `[FINAL]` messages already displayed when clicked. Paste with `Ctrl+V`. Closing and reopening the window preserves the accumulated view for the current session; starting a new experiment starts a new view. Raw child stdout/stderr remains available in the session's `console.log` file. Copying does not stop or modify the experiment.

## Windows / Git Bash update

Close the GUI and make sure no experiment is active before updating. Profiles are stored outside the GUI source folder. Extract the complete ZIP into the upstream `tobii-pytracker/` directory. The archive already contains a `pytracker-gui/` directory. Prefer backing up the old directory rather than merging two versions.

```bash
cd /e/pytracker/tobii-pytracker   # adjust the drive letter
mv pytracker-gui "$HOME/pytracker-gui-v0.1.5-backup"
GUI_ZIP="$(cygpath -w "$HOME/Downloads/pytracker-gui-v0.1.6-demo-adapter-import-log-copy.zip")"
DEST="$(cygpath -w "$PWD")"
powershell.exe -NoProfile -Command "Expand-Archive -LiteralPath '$GUI_ZIP' -DestinationPath '$DEST' -Force"
conda activate pytracker-env
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Check that the demo adapter file exists:

```bash
ls tobii-pytracker-demo/tools/demo_runtime_adapters.py
```

In the GUI, choose **Text Search EN**, `MouseGaze`, and the appropriate ioHub YAML file, then click **Start demo**. Expect `[ADAPTER] Loaded from ...` and `[ADAPTER] Applied text adapter` before PsychoPy begins. These lines confirm adapter loading, **not** successful data collection. Repeat with UX A/B and Image Semantic. Test Demo remains available; Time-Series still runs Machine → PV in two separate processes.

Any `RequestsDependencyWarning` mentioning `chardet`/`charset_normalizer` is unrelated to the adapter import failure. This release does not change PsychoPy or Python dependencies. If a demo fails after loading its adapter, use **Copy entire log** and keep the session's `run.json`, `console.log`, and `result.json` files under `%LOCALAPPDATA%/pytracker-gui/runs/`.

## Validation boundary

Automated tests use fake upstream child processes to cover a conflicting `tools` package, missing `tools/__init__.py`, all five adapter-backed demo variants, missing-adapter preflight, clipboard behavior, and both GUI languages. An additional isolated check loaded the **real adapter source from the supplied v1.17.0 demo archive** with stubbed dependencies. Actual Windows/PsychoPy/Tobii sessions were not run in the development environment. The user's successful Test Demo is separate Windows runtime evidence for that demo only.

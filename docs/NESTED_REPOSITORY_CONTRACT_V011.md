# Canonical nested Git checkout contract — v0.1.1

## Trigger and source observation

Previous GUI instructions described the demo repository next to the original engine. The real demo `tools/run-demo.sh` and `examples/*/run_native.sh` require `tobii-pytracker-demo` **inside** the original `tobii-pytracker` checkout. Original project README_TESTING also clones `https://github.com/mszac/tobii-pytracker-demo.git` in the upstream directory. A different fork (`tobii-pytracker-examples`) is not this demo project.

## Decision

Make the independent GUI another **child** of `tobii-pytracker`, not a package placed inside `src/` or a patched upstream file. `pytracker-gui` detects `Path(__file__).resolve()` so shell current directory does not matter; chooses real adjacent checkouts before stale saved settings; and reports missing/incorrect checkout layout through `python run_gui.py --check-layout`. Explicit manual paths remain possible for static editing but validation blocks a noncanonical nested arrangement.

## User data and boundaries

Settings/profiles stay app-private in `%LOCALAPPDATA%/pytracker-gui` (Windows) or `$XDG_CONFIG_HOME/pytracker-gui` (Linux; default `~/.config`). No copy of dataset or firmware; no writes to demo/upstream originals. Profile YAML has source SHA provenance from the previously implemented system.

## Launch semantics

Do not conflate `cwd` (demo root) and `repo parent` (upstream). Original public shell dispatcher is invoked from upstream root with `bash tobii-pytracker-demo/tools/run-demo.sh ...` and delegates to demo native scripts, which `cd` into demo root. Preview now reports both directories and the original command, explicitly warning that original wrappers do NOT consume GUI profiles or dynamically selected gaze flags. Real configuration-aware child bridge is a future release, not supplied here.

## Acceptance/test matrix

- Canonical upstream with `pyproject.toml`, `src/tobii_pytracker/` and `configs/mouse_eyetracker_config.yaml` must exist.
- Exact `upstream/tobii-pytracker-demo/` directory with `tools/run-demo.sh`, `examples/` and all 8 cataloged YAMLs must exist.
- GUI remains independent; no checkout modification by program, profile export refuses overwriting original configs.
- Invalid/missing demo root must give actionable BLOCK; retained old external config cannot override actual neighbor layout.
- All 7 variants load and Time-Series Machine/PV remain independent; default gaze config path changes with gaze selection.
- Tests: Linux+Xvfb GUI, synthetic canonical file tree, no network dependency; Windows/native experiment/hardware not tested.

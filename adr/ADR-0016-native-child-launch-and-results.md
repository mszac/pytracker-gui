# ADR-0016 — Native demo launch, app-private snapshots and results (2026-10-11)

**Status:** accepted for v0.1.5, pending physical Windows/Linux integration.

**Problem:** v0.1.4 edited YAML and saved gaze/voice/raw preferences but did not run experiments. Three original demo wrappers hard-coded those flags; invoking the old `run-demo.sh` would ignore the GUI state.

**Decision:** Tk stays a lightweight controller. It validates the nested repositories, selected Python 3.10 and the current YAML, then creates an immutable run snapshot under the application-private `runs/` directory. A native Python child imports the original `tobii_pytracker.main` and applies the **existing** `tools/demo_runtime_adapters` when required. It forwards current config, ioHub file, gaze/voice/raw, loop count and log level dynamically, without modifying upstream or demo repository files. Each Time-Series block uses its own child process.

**Lifecycle:** `ExperimentRunner` serializes execution, reads subprocess stdout/stderr via a background thread, logs results and supports process-tree termination on Windows (`taskkill /T /F`) and POSIX (process-group SIGTERM, SIGKILL fallback). Stop, nonzero exit, or validation failure prevents later blocks. A second GUI run is rejected while one is active.

**Result authority:** normal process return is not proof of collected gaze. The original demo validator is invoked only for full-length sessions with compatible original dataset/output layout and active gaze. If skipped, the result is `PROCESS COMPLETE — COLLECTION NOT VERIFIED`; validator failure is `FAILED`. `CANCELLED` means partial data are possible. `result.json` and `console.log` remain in a private run folder; experiment output stays in YAML `output.folder`.

**Alternatives rejected:** directly running immutable shell wrappers (ignores selected preferences), changing the sbobek runtime (ownership conflict), changing original demo scripts (introduces fork drift), running PsychoPy in Tk process (UI blocking and lifecycle coupling), treating return code 0 as validated gaze.

**Open gates:** exact upstream/demo Git SHA on actual Windows; Python 3.10/PsychoPy/ioHub native launch; MouseGaze samples/response buttons; Tobii device; microphone/raw data; collection validators with live output; Windows process tree stop; Linux session/focus behavior. No physical tests were performed in the assistant runtime.

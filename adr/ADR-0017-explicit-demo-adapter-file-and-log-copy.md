# ADR-0017 — Explicit adapter source path and lossless GUI log clipboard

**Status:** accepted for v0.1.6. **Parent:** v0.1.5 native demo launcher.

**Observed field failure (Windows):** Test Demo completed and its validator passed, while Text Search EN stopped in `launch_child.py` with `ModuleNotFoundError: No module named 'tools.demo_runtime_adapters'`. The original demo adapter file exists in `tools/`, but this directory is not guaranteed to be an importable regular package; the generic module name may collide with an installed `tools` package.

**Decision:** Resolve `<plan.demo_root>/tools/demo_runtime_adapters.py` explicitly and load it in the child via `importlib.util.spec_from_file_location`. No `sys.path` manipulation and no edits to either upstream repository. Keep dynamic flags and existing adapter application unchanged. Preflight checks presence of the adapter only for adapter-backed demos, with an actionable error. The log records the exact adapter source path and selected text/image patch. This is intentionally a child-only dependency: the GUI process still must not import PsychoPy or the demo adapter.

**Alternatives rejected:** Add `__init__.py` into the cloned demo repository (mutates external checkout); globally insert demo root into `PYTHONPATH` (does not eliminate installed regular-package collisions); bundle a copy of the adapter (causes code drift). The explicit file approach preserves provenance and works on both Windows and Linux.

**Log copy:** The log popup must copy exactly the complete current content of its Tk text widget, including GUI-only status and final lines. Keep the assembled view in app memory across closing/reopening the popup for the duration of a session; reset on starting the next session. Child stdout/stderr still goes to `console.log`; no changes to experiment results, dataset, or existing run manifest schema. Clipboard failure is reported without modifying the experiment.

**Verification:** Host Xvfb process tests with a foreign conflicting `tools` package and a demo `tools/` directory lacking `__init__.py`; five adapter-backed variant launches; adapter missing preflight; Tk clipboard PL/EN and popup re-open. Additional separate integration check loaded original demo v1.17.0 adapter source with simulated PsychoPy/upstream modules. Real Windows mouse/Tobii checks remain an external gate.

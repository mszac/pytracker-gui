# ADR-0012: independent GUI as nested checkout under tobii-pytracker

Status: accepted in v0.1.1 (2026-10-11).

**Problem:** v0.1.0 documentation positioned the demo as a sibling checkout outside upstream, contradicting real `run_native.sh` checks and the demo's Git clone instructions. That would cause experiments to fail before a runtime even starts.

**Alternatives:** (A) standalone workspace with three siblings; (B) inject demo into upstream package; (C) engine root plus independently owned `tobii-pytracker-demo/` and `pytracker-gui/` child folders. **Choice: C.** The original demo scripts work in the canonical tree, upstream runtime stays unmodified, GUI can later have its own Git remote. Both nested subtrees have independent `.git` histories, with no Git submodule contract implied.

**Implementation:** read-only layout discovery and validation module, CLI gate, GUI auto-populated paths, gaze config defaults, corrected Git Bash docs, untouched profile persistence location.

**Non-goals:** experiment process control, modified adapter runtime semantics, automatic Git checkout/network operations or Git remote creation. **Next gate:** Windows machine actual SHA/provenance, Python 3.10 and ioHub; native child launch bridge with dynamic flags and immutable session configs.

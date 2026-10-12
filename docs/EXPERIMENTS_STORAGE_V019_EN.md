# v0.1.9 — separating project state from experiment executions

## Current storage contract

```text
tobii-pytracker/
├── tobii-pytracker-demo/
├── pytracker-gui/
└── projects/
    └── <experiment_name>/
        ├── project.json                # project identity and demonstration variant
        ├── current-settings.json       # most recent launch settings
        ├── profiles/
        │   └── <demo_key>/
        │       ├── profile.json         # reusable profile
        │       └── main.yaml           # or machine.yaml and pv.yaml
        └── experiments/                # created lazily on first launch
            ├── 20261011_194500_aB9z0/
            │   ├── run.json            # execution manifest / historical paths
            │   ├── gui-settings.json   # GUI settings snapshot at launch
            │   ├── main.yaml           # YAML snapshot; Machine/PV for Time-Series
            │   ├── eyetracker.yaml      # ioHub snapshot
            │   ├── result.json         # execution status, not measurement data
            │   ├── console_20261011_194530_aB9z0.log
            │   └── experiment_20261011_194531_aB9z0.log
            └── 20261011_195000_Q7mX2/
                └── ...
```

`<experiment_name>` is the user-created **project name**, not an individual execution. The project-level metadata and reusable profile remain at the project root. Each Start action creates a new directory under `experiments/`, with local creation time to the second and a random, case-sensitive, five-character `[A-Za-z0-9]` ID. Directory creation is exclusive to prevent overwrites. A Time-Series Machine → PV session still belongs to one GUI execution, with separate YAML snapshots for both blocks.

Exact configuration snapshots are written **before** launching a child process. `console_*.log` is published after the child exits; `experiment_*.log` after the GUI receives `[FINAL]`, including `[RUN]`, `[STATUS]`, and `[PROCESS]` messages. Both filenames carry their write time to the second and the execution's shared ID. No permanent per-line project logging is performed while PsychoPy runs: the pre-existing in-memory 256 KiB spool with OS-temporary overflow is retained, and a log-write failure does not abort the experiment.

**Measurements and analysis results** (such as CSV) continue to use the demo's configured `output.folder` and are never redirected into `projects/` or `experiments/`. Global project files retain their original paths; only individual execution histories live in `experiments/`.

## Compatibility policy

The run-history path changes directly from `projects/<name>/runs/` to `projects/<name>/experiments/`. **No migration or reading of the old `runs/` directory is implemented.** New executions are written only to `experiments/`. Existing old directories are not deleted automatically, preventing accidental historical-log loss; archive or relocate them manually with the GUI closed if desired. Older v0.1.7/v0.1.8 documentation is historical, not the current directory specification.

Demo adapter code, PsychoPy launching, gaze flags, existing log buffering and names, UI, and profile YAML schema are unchanged. No extra dependencies, timers, or processes are introduced. Real Windows/Tobii execution remains an external validation gate.

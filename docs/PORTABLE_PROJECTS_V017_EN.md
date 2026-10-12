# pytracker-gui v0.1.7 — portable projects and experiment logs

## Location and project selection

Under the standard installation, `tobii-pytracker/` contains three sibling directories: `tobii-pytracker-demo/`, `pytracker-gui/`, and the new **`projects/`**. The GUI creates `projects/` on first use. Projects remain separate from application code, so replacing the GUI checkout does not delete them. Do not add projects to the upstream Git repository unless you intend to version them there.

For each of the seven demo variants, the GUI offers a **Project** selector and a **New project…** button. The default project uses the variant's technical key (for example, `search_en`). You can maintain multiple independent projects for the same variant; switching projects reloads its profile, or the original YAML if no profile has been saved. Project names contain 1–64 ASCII characters (`A–Z`, `a–z`, `0–9`, `_`, `-`) and must start with a letter or digit. A project is associated with one demo variant; it cannot silently import another variant's profile.

## Example directory layout

```text
tobii-pytracker/
├── tobii-pytracker-demo/          # unchanged
├── pytracker-gui/                # separate GUI source
└── projects/
    └── SearchStudy/
        ├── project.json          # project identity and assigned demo variant
        ├── current-settings.json # most recent launch configuration
        ├── profiles/
        │   └── search_en/
        │       ├── profile.json
        │       └── main.yaml
        └── runs/
            └── 20261011_192210_aB9z0/
                ├── run.json
                ├── gui-settings.json
                ├── main.yaml
                ├── eyetracker.yaml
                ├── result.json
                ├── console_20261011_192245_aB9z0.log
                └── experiment_20261011_192245_aB9z0.log
```

Each run has a randomly generated, exactly five-character alphanumeric **ID** (`A–Z`, `a–z`, `0–9`); case matters. The run directory contains its **creation** timestamp; both log filenames carry their **save/completion** timestamp to second precision. Logs from the same run share the same ID even if their save timestamps differ by a second. Exclusive directory creation prevents accidental overwrite on collisions.

`experiment_*.log` is the entire displayed Experiment log, including `[RUN]`, `[STATUS]`, `[PROCESS]`, and `[FINAL]`. `console_*.log` is the captured raw child-process output. `result.json` records completion status, not measurement data. Current main and ioHub YAML snapshots are copied **before** the run. The GUI also updates the project's saved profile so the launch configuration is available when work resumes.

## Resource use and failure handling

While PsychoPy runs, the GUI displays events from its existing in-memory queue. The subprocess supervisor uses a `SpooledTemporaryFile` (up to 256 KiB in RAM, with excess spilling into OS temporary storage). It does **not** append each new console line to permanent project log files. The raw log is saved once after the child exits, and the complete GUI log is saved once the `[FINAL]` event has been processed. No new processes, periodic timers, database, or dependencies are introduced. A log-writing failure must not terminate the experiment; it may leave an incomplete local archive, which should be checked after the run.

Measurement output and analysis artifacts **stay outside `projects/`**, at `output.folder` as defined by the original demo configuration.

## Moving a project to another clone

1. Close the GUI after ensuring that no experiment is active.
2. Copy the entire `tobii-pytracker/projects/SearchStudy/` directory to `projects/SearchStudy/` inside the new upstream checkout, alongside its new `pytracker-gui/` and `tobii-pytracker-demo/`.
3. Start the GUI, select the same demo variant, then select `SearchStudy` in the Project selector. Its profile and logs remain available.
4. Verify your local Python interpreter, demo repository, and any external dataset paths; these might have to be reselected on the new machine. Standard ioHub configs under upstream `configs/` are stored as checkout-relative references.

Historical `run.json` files intentionally retain the exact absolute paths used during their original execution for diagnostic provenance; they are **not** portable replay manifests. Profiles, `current-settings.json`, and copied YAML/ioHub are the portable resume configuration. Matching upstream/demo versions and external input data must be made available separately.

On an existing v0.1.6 installation, old `%LOCALAPPDATA%/pytracker-gui/profiles/<demo_key>/` profiles are **copied once** into the appropriate default project when first opened; the originals are never removed. Existing `%LOCALAPPDATA%/pytracker-gui/runs/` logs are kept untouched and are not automatically migrated or overwritten.

## Scope

Only project directory organization, portable configuration snapshots, and post-run log persistence have changed. PsychoPy runtime, adapter selection, gaze/voice/raw parameters, validators, seven demo variants, YAML editor, GUI languages, and parameter documentation are unchanged. Automated validation used fake child processes on Linux/Xvfb; Windows and physical Tobii remain device-level verification gates.

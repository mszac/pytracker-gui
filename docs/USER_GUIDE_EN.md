# pytracker-gui — user guide (reviewed for v0.2.33)

**Current, English-language guide.** Polish counterpart: [USER_GUIDE_PL.md](USER_GUIDE_PL.md). For installation on Windows/Git Bash, see [README_WINDOWS_GIT_BASH_EN.md](../README_WINDOWS_GIT_BASH_EN.md). Earlier version-specific documents remain historical snapshots; this guide describes the current **v0.2.33** interface while retaining historical feature notes where explicitly dated.

## 1. Purpose and boundaries

pytracker-gui is a lightweight, bilingual, Tkinter/ttk **configuration editor and launcher of existing demonstrations** from `mszac/tobii-pytracker-demo`, running the original `sbobek/tobii-pytracker` PsychoPy/ioHub framework in an independent Python process. It does not create new experimental paradigms, edit the source repositories, or replace the experimental code that **produces and saves measurement data**. The GUI manages its own project profiles, run-specific configuration snapshots, console journals, and execution-status metadata. It does not analyse measurement CSV files in the Logs screen.

The top navigation contains **Experiment**, **Logs**, **Statistics**, and **Manual**. The brand/logo opens the four-tile home dashboard. **Statistics is currently a placeholder**; Diagnostics was removed from the top-level navigation, but Python and configuration checks remain inside Experiment. Other screens are created lazily when first opened, and switching screens does not apply or discard YAML edits.

## 2. Required layout and quick start

```text
tobii-pytracker/                   # original sbobek/tobii-pytracker checkout
├── tobii-pytracker-demo/         # separate mszac/tobii-pytracker-demo checkout
├── pytracker-gui/               # GUI ZIP, including run_gui.py
└── projects/                    # GUI-owned project profiles and run history
```

Activate a usable Conda environment (`pytracker-env`; the experiment runtime expects Python 3.10 with the upstream framework and PsychoPy/ioHub). From the **upstream root**:

```bash
conda activate pytracker-env
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

`--check-layout` checks repository/configuration structure; it does **not** demonstrate that PsychoPy, an ioHub device or a physical Tobii tracker is operational. The GUI itself has a small Tk/ruamel.yaml dependency set; the research runtime must be configured separately to launch experiments.

## 3. Projects, variants and configuration editing

A **Project** is a reusable GUI workspace and must be selected before editing/launching. Project files reside under `projects/<project>/`; this directory is **outside** `pytracker-gui/` and must be retained during upgrades. **New project…** creates a project for an existing demonstration variant.

| Demonstration | Selectable variants | Run blocks |
| --- | --- | --- |
| Test Demo | EN | Test Demo |
| UX A/B Text | EN / PL | One block per selected language |
| Time-Series Noise | Machine Vibration → PV Power | Two sequential, separately configured blocks |
| Text Search | EN / PL | One block per selected language |
| Image Semantic | EN | One block |

There are **seven selectable variants** backed by **eight source YAML configurations**. EN/PL in demo names means the language of experimental materials, not the GUI language.

In **Experiment**, select the Demo root, original Upstream root and experiment Python interpreter; use **Detect layout**, **Check Python**, **Load repository** or **Save paths** when necessary. The editor exposes dataset, monitor, appearance, instructions and raw YAML fields present in the selected source document. The ioHub configuration selector chooses a YAML path; it does not edit the device configuration internally.

- **Apply changes** applies the active editor changes to the working configuration in memory.
- **Save profile** persists a reusable project profile; it does not overwrite upstream/demo YAML.
- **Restore original** restores the selected source configuration in memory, without deleting stored profiles.
- **Export YAML** saves a separate YAML copy, without overwriting original demo YAML.
- Unsaved changes are protected by the existing confirmation safeguards.

The traditional, naturally sized buttons and **single-row editor footer from v0.2.14** are retained. v0.2.16 adds small icons **only to Check Python, Detect layout and Apply changes**; it does not inherit the uniform-size/two-row button design from the rejected v0.2.15.

## 4. Start/stop and automatic log display

On **Experiment → Launch**, choose the gaze mode (**NO_GAZE**, **MOUSEGAZE** or **TOBII**), the ioHub YAML, trial count per block and available voice/raw-data/log-level options. MouseGaze simulates gaze through ioHub; TOBII requires a compatible device and tested local configuration. Preflight does not certify hardware readiness.

**Start demo** creates an exclusive run directory, saves immutable launch-time configuration snapshots, then starts an isolated child Python/PsychoPy process. In Time-Series, Machine is followed by PV as separate processes. **Stop demo** requests termination of the active run; partial experimental outputs are possible. Original demonstration code, not pytracker-gui, controls measurement generation and saving.

**Auto-show logs** (default **ON**) opens the live console window automatically. Turn it **OFF** for long-running experiments to avoid automatic Tk text rendering; **Show Logs** remains available manually. This preference is stored in local application settings, not experimental YAML. The on-screen console preview is limited to **2,000 lines or 256 KiB**, whichever comes first; **Copy entire log** is separate from that preview limit.

The incremental journal writer is isolated from the subprocess output reader and uses best-effort low-priority I/O. It has a **256 KiB pending-data limit**; the oldest *not yet saved* entries can be replaced if storage falls behind. This protects the running experiment but can leave the journal incomplete. It does not guarantee that the disk is idle or that data survive a power failure.

## 5. Run directories and the single console journal

```text
projects/<project>/
├── project.json
├── current-settings.json
├── profiles/<variant>/...
└── experiments/
    └── YYYYMMDD_HHMMSS_aB9z0/
        ├── run.json
        ├── gui-settings.json
        ├── main.yaml                 # or machine.yaml / pv.yaml
        ├── eyetracker.yaml           # when applicable
        ├── result.json               # execution/validation metadata, not measurements
        └── experiment_YYYYMMDD_HHMMSS_aB9z0.log.part
```

The five-character alphanumeric Run ID is **case-sensitive**. A run creates **one** durable console journal, not separate `console_*.log` and `experiment_*.log` files. While recording, messages are appended in batches to `.log.part`. A cleanly finalized, complete journal is renamed to `.log`; a cancelled, interrupted or incomplete journal remains `.log.part`, possibly with an `INTERRUPTED` or `BUFFER_OVERFLOW` notice. **Repair/recovery of `.part` files has not been implemented.** A complete `.log` does *not* mean that the experimental results were successful.

The runner reserves a unique output subdirectory incorporating the Run ID and block name under the configured `output.folder`; the **original experimental code** creates its own measurement session directory and writes the measurement files there. GUI `run.json` and `result.json` provide provenance/status and can record exact session paths, but the GUI does not write or analyse the measurements. Old `projects/<project>/runs/` directories are not migrated automatically to `experiments/`.

## 6. Logs screen — history and read-only configuration report

**Logs** discovers projects containing a real `experiments/` directory. Select a project, then an individual run (newest first). The dashboard reads **historical snapshots**, not the current YAML editor values, and presents six compact groups: identification, environment, execution, input data, display/appearance and configuration. Expand additional YAML details when needed. The journal indicator distinguishes **complete** `.log`, **incomplete** `.log.part` and **missing** logs; this is **not** a measure of experimental success.

Switch to **Console Log** to inspect the selected run's journal. **First / Previous / Next / Latest**, **Refresh log**, and **Copy page** operate on **at most 64 KiB and 2,000 lines per page**. An active `.log.part` is refreshed manually. There is no automatic polling, file repair, CSV inspection, or write-back. The Logs screen uses slightly larger fonts and a light-orange selection for readability.

## 7. Manual and languages

**Manual** contains four tabs:

- **Index** (default): 87 parameters with searchable, bilingual extended help; the orange **man** link in a parameter tooltip opens its exact Index entry.
- **Documentation**: read-only viewer for local `*.rst` files from the **original upstream** `tobii-pytracker/docs/`.
- **Demo Project Documentation**: a grouped, expandable **project → Markdown files** tree using local `.md` instructions from `tobii-pytracker-demo`, with applicable example guides.
- **GUI Documentation**: read-only, English/Polish tree of current documentation included with this pytracker-gui installation, rendered on demand with the existing lightweight Markdown viewer. This tab does not read upstream/demo documents or experiment outputs.

Markdown/reStructuredText headings, lists and code are rendered with lightweight native Tk text formatting. This is **not** a complete CommonMark/Sphinx renderer; complex tables, pictures and directives may remain simplified. Documents are read on demand and large documents use a plain-text fallback. No web engine is installed.

The interface language (default Polish) and parameter-help language can be selected independently. Switching language does not write YAML. A tooltip's blue `i` gives brief help; the **man** link opens extended help without committing unsaved editor changes.

## 8. Movable panel boundaries

Drag the native separators to resize **Experiment: starter-project list ↔ editor**, **Logs: selector ↔ report/console**, and **Logs: projects ↕ runs**. Minimum panel sizes prevent complete collapse. The proportions remain during navigation within the same application session but **are not saved across restarts**. There are no additional timers, worker threads or third-party layout dependencies.

### Parameter availability markers

The 87-entry parameter reference uses these classification labels: `gui` (editable in GUI), `yaml-only` (documented YAML without a dedicated control), `iohub-only` (internal ioHub configuration), `reference` (upstream/CLI information), and `future` (not implemented by the GUI). A `gui` label does not automatically guarantee that every experimental adapter consumes the setting. See both [English parameter manual](PARAMETER_MANUAL_EN.md) and [Polish parameter manual](PARAMETER_MANUAL_PL.md).

## 9. Limitations, verification and safety

Configuration validation and collection checks do not establish scientific validity or real eye-tracker accuracy. External PsychoPy/demo processes own experiment results; avoid running the independent original `tools/run-demo.sh` concurrently against the same equipment/output. The **Statistics** screen is not yet implemented. Windows/HiDPI, physical PsychoPy and Tobii workflows still need workstation testing; Linux/Xvfb automated GUI tests alone do not prove device operation.

**More details:** [documentation index](DOCUMENTATION_INDEX_EN.md), [native launch](NATIVE_LAUNCH_V015_EN.md), [single incremental log](INCREMENTAL_SINGLE_LOG_V0212_EN.md), [Logs history](LOGS_HISTORY_STAGE1_V0213_EN.md), [Console Log viewer](LOGS_CONSOLE_VIEWER_V0214_EN.md), [Manual document tree](MANUAL_DEMO_TREE_V0210_EN.md), [resizable panels and classic buttons](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_EN.md).

**Historical correction:** The archived v0.1.4 description **“not yet an experiment launcher”** is obsolete; v0.2.17 launches the existing supported demos.

**v0.2.17:** The four Environment buttons now share the width set by Load repository, with all other button appearance unchanged. [GUI Documentation notes](GUI_DOCUMENTATION_V0217_EN.md).

## GUI Settings and interface help (v0.2.33)

**GUI Settings** displays startup window sizing, fixed Home tile dimensions, application/repository paths, current preferences and a palette editor. The path and preference summary fields on this page are **read-only**; use the appropriate **Experiment → Environment** controls for supported path changes. The blue **i** icons show concise descriptions and their **man** links open the extended **GUI Settings reference** under **Manual → GUI Documentation**. They do not open or modify experiment-parameter YAML.

**Save window size** affects the next GUI launch (the screen may constrain the requested size). The four Home tile images remain at their original pixel size. Color entries accept six-digit `#RRGGBB` values; **Save colors** validates and persists the complete palette, which takes effect after restarting the GUI. **Restore defaults** changes only the values shown in the editor until **Save colors** is pressed. Icon tint applies to theme-supported icons, not necessarily selected-state icons or pre-rendered tile art.

The **Manual → Experiment parameter** documentation is separate from **GUI Documentation**. The former describes experiment configuration parameters; the latter describes GUI-only behavior and local application settings. Language selection for interface labels is separate from help language and from the language of stimuli in starter experiments.

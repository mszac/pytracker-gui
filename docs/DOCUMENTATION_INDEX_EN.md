# pytracker-gui v0.2.17 — documentation index (English)

**Use these current documents first.** Polish counterpart: [DOCUMENTATION_INDEX_PL.md](DOCUMENTATION_INDEX_PL.md). Older version-specific pages are intentionally preserved as historical release notes; they may mention features that were not available *at that time* (or old file locations such as `runs/`).

| Topic | Current English guide | Polish counterpart |
| --- | --- | --- |
| Windows / Git Bash install and updates | [README_WINDOWS_GIT_BASH_EN.md](../README_WINDOWS_GIT_BASH_EN.md) | [README_WINDOWS_GIT_BASH_PL.md](../README_WINDOWS_GIT_BASH_PL.md) |
| GUI operation, navigation, projects, runs | [USER_GUIDE_EN.md](USER_GUIDE_EN.md) | [USER_GUIDE_PL.md](USER_GUIDE_PL.md) |
| Extended reference for 87 parameters | [PARAMETER_MANUAL_EN.md](PARAMETER_MANUAL_EN.md) | [PARAMETER_MANUAL_PL.md](PARAMETER_MANUAL_PL.md) |

## Feature-specific documentation (chronological)

| Feature | English | Polish |
| --- | --- | --- |
| Native demo process launch | [v0.1.5](NATIVE_LAUNCH_V015_EN.md) | [PL](NATIVE_LAUNCH_V015_PL.md) |
| Current `projects/*/experiments/` directory hierarchy | [v0.1.9](EXPERIMENTS_STORAGE_V019_EN.md) | [PL](EXPERIMENTS_STORAGE_V019_PL.md) |
| Manual Index and upstream `.rst` viewer | [v0.2.6](MANUAL_UPSTREAM_RST_V026_EN.md) | [PL](MANUAL_UPSTREAM_RST_V026_PL.md) |
| Run ID and reserved measurement output folder | [v0.2.8](SESSION_MEASUREMENT_BINDING_V028_EN.md) | [PL](SESSION_MEASUREMENT_BINDING_V028_PL.md) |
| Optional Auto-show logs | [v0.2.9](AUTO_LOG_DISPLAY_V029_EN.md) | [PL](AUTO_LOG_DISPLAY_V029_PL.md) |
| Manual demo Markdown tree and lightweight viewer | [v0.2.10](MANUAL_DEMO_TREE_V0210_EN.md) | [PL](MANUAL_DEMO_TREE_V0210_PL.md) |
| One incremental `.log.part` journal | [v0.2.12](INCREMENTAL_SINGLE_LOG_V0212_EN.md) | [PL](INCREMENTAL_SINGLE_LOG_V0212_PL.md) |
| Logs history and settings report | [v0.2.13](LOGS_HISTORY_STAGE1_V0213_EN.md) | [PL](LOGS_HISTORY_STAGE1_V0213_PL.md) |
| Logs paged read-only console | [v0.2.14](LOGS_CONSOLE_VIEWER_V0214_EN.md) | [PL](LOGS_CONSOLE_VIEWER_V0214_PL.md) |
| Classic action buttons, three icons and native resizable panels | [v0.2.16](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_EN.md) | [PL](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_PL.md) |
| GUI Documentation tab and Environment button widths | [v0.2.17](GUI_DOCUMENTATION_V0217_EN.md) | [PL](GUI_DOCUMENTATION_V0217_PL.md) |

## Important current distinctions

- **Experiment** can launch and stop existing PsychoPy demos. **Statistics** is still a placeholder. **Diagnostics** is not a top-level tab, but Experiment retains Python/configuration validation.
- **Manual** has four working tabs: **Index** (87 parameters), upstream **Documentation** (`.rst`), and **Demo Project Documentation** (`.md` grouped by project), and **GUI Documentation** (current pytracker-gui manuals grouped EN/PL). The `man` tooltip link opens Index.
- **Logs** reads saved GUI metadata, YAML snapshots and a bounded view of one `experiment_*.log` or `.log.part`. It **does not read measurement CSVs**; original experiment code is responsible for experimental results.
- The **single incremental journal** from v0.2.12 supersedes historical descriptions of two separate log files. `experiments/` supersedes `runs/`. v0.2.16 uses **v0.2.14 classic buttons**, not the rejected uniform-button appearance of v0.2.15.
- Real Windows/HiDPI, PsychoPy and Tobii workflows remain device-level validation gates. Historical ADRs and six development logs retain the earlier decision/implementation record and are not rewritten as user instructions.

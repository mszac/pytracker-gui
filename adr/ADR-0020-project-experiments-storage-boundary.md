# ADR-0020 — Project-global settings versus per-execution experiments directories

- **Status:** accepted, v0.1.9, 2026-10-11
- **Context:** `projects/<name>/runs/` in v0.1.7–v0.1.8 mixed terminology: `projects/` already identifies reusable study configurations, while each run contains only historical execution context. The required term for these independent executions is `experiments`.
- **Decision:** keep `projects/<experiment_name>/project.json`, `profiles/`, `current-settings.json` and the GUI project selector intact. Allocate execution snapshots, `run.json`, `result.json`, and both deferred logs at `projects/<experiment_name>/experiments/<start_timestamp>_<5char_id>/`.
- **Performance and stability:** retain the existing exclusive directory allocation, per-run manifest and read-only YAML snapshots, 256 KiB spooled console output and post-run/post-final publication. No extra threads, callbacks, watchers or source repo modifications.
- **Explicit incompatibility:** no `runs/` migration, legacy alias, read fallback or automatic deletion. Old histories may remain on disk but are not part of the current app's storage contract.
- **Alternatives not chosen:** moving all project state into executions (destroys the project-global boundary), flattening files under `experiments/` (loses per-execution isolation), moving measurements/analyses into projects (violates demo output ownership), and adding a database (unnecessary overhead).
- **Validation:** verify two executions of one project, two independent projects, both kinds of final logs, source tree immutability, five-character ID and second-resolution timestamps, and absence of new `runs/` trees. Physical Windows tests remain external.

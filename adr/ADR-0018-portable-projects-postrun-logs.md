# ADR-0018 — Portable project folders and post-run logs

Status: accepted for v0.1.7. Direct parent: exact v0.1.6-demo-adapter-import-log-copy.

**Problem:** v0.1.6 saved profiles and console traces under user-private `%LOCALAPPDATA%/pytracker-gui`, which is not a standalone portable research project. Continuous file opening/writing for every console line in the process reader thread could raise an I/O exception and abort the supervisor.

**Decision:** create `tobii-pytracker/projects/<name>/` sibling to independent demo/GUI checkouts; one project is owned by one of the seven existing variants, with independent saved profile, portable ioHub reference, last launch settings, and per-run immutable YAML/ioHub snapshots. Allow multiple projects per variant using a minimal Tk project selector and New project dialog. Default project name = variant key. Migrate old profiles once by **copy**, never delete or rewrite old runs. Project identity is not an experiment dataset.

**Run identity:** independent timestamp + 5-character cryptographically randomized `[A-Za-z0-9]` code. Exclusive directory creation prevents case-insensitive Windows collisions; five characters are kept unambiguous in log filenames as well as run directory. Log filename timestamps reflect completion/save, not run start.

**Logging:** maintain current GUI event queue and screen log, but replace per-line permanent file writes with 256-KiB memory spool (larger data spills to OS temporary file). Publish raw console file only after child exit, and publish exact GUI log after `[FINAL]` (including GUI-only messages). Log write failure is isolated from experiment execution and preserves result status. `run.json` keeps historical absolute paths intentionally; `profile.json`, copied YAML and checkout-relative standard ioHub references support resuming on a different clone. Never move measurement/analysis output from `output.folder`.

**Risks/tradeoffs:** copied projects need matching upstream/demo runtime and access to external data files; absolute paths in historical manifests are diagnostic only. If the GUI crashes before processing `[FINAL]`, a complete GUI log may be absent even though the raw process log can be saved by the supervisor. The spool may use OS temporary disk for large outputs. Do not promise lossless persistence during OS/process failure. No extra dependencies, tasks, watchers, engines or edits to original Git checkouts.

**Gate:** fake-child cross-platform contract tests, GUI project isolation, old-profile migration, portable path rebasing, all prior smoke and language tests, release manifest/patch reconstruction; physical Windows remains external.

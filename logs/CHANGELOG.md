# CHANGELOG (append-only)

## v0.0.0-plan — 2026-10-10
- Utworzono nowy projekt `pytracker-gui` jako samodzielny plan, bez runtime/source code.
- Skatalogowano demo ZIP v1.17.0 i historyczne lessons learned.
- Zdefiniowano funkcje F01..F20, ekran główny, RunSpec, fazy M0..M5 oraz walidację.
- Przygotowano proponowane ADR-0001..0006 i narastające logi.

## v0.0.1-upstream-demo-control-plan — 2026-10-10
- Przeanalizowano publiczne oryginalne upstream `main`, `CustomConfig`, `eyetracker.py`, `gui.py`, oba ioHub yaml, config.yaml i pyproject.toml; źródło zmienne main, SHA nadal niepobrany.
- Przyjęto zmianę scope: M1 wyłącznie istniejące demo/ścieżki/config/wybór NO_GAZE-MOUSEGAZE-TOBII, odroczono kreator nowych eksperymentów.
- Potwierdzono z repo v1.17.0 7 publicznych wariantów (5 dem), dual-block time-series; wykryto 3 wrappery hardcoded gaze/voice/raw.
- Dopisano source/launch/config/UI/phase plan i ADR-0007..0010. Nie implementowano GUI, nie zmieniano upstream/demo.

## v0.1.0-ui-config-prototype — 2026-10-10
- Added executable Tkinter/ttk frontend (`run_gui.py`, `pytracker_gui/`), 7 variants, 8 native config fixtures, explicit time-series 2-block selection.
- Added form+raw YAML editing via `ruamel.yaml`, profile provenance hashes/backups, static preflight, selection of gaze mode, interpreter probe, dry-run-only run contract.
- Added regression tests (13 checks including Tk+Xvfb), install/use documentation and captured UI screenshot.
- Engine launch/stop remains explicitly disabled; M1 not complete.

## v0.1.1-nested-repository-layout — 2026-10-11
- Corrected layout to original `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}`; verified public clone URL mszac/tobii-pytracker-demo, not mszac/tobii-pytracker-examples.
- Added `layout.py`: autodetect based on actual GUI source directory, repo signatures, 8-config inventory, stale saved path handling, read-only strict nested layout preflight, and gaze-specific upstream ioHub defaults.
- Added `run_gui.py --check-layout` (no graphical or runtime imports), `Wykryj układ`, strict save/validation and corrected manual original demo command in dry-run preview.
- New canonical Windows Git Bash setup, ADR-0012, independent repository contract, fixture-backed nested layout regressions. Existing profile/write safety, 7 variants, raw/form YAML unchanged.
- GUI still does NOT run experiments; using original run-demo.sh manually does not honor GUI profiles or alternate gaze flags. Windows/Tobii NOT RUN locally.

## v0.1.2-parameter-help-manual — 2026-10-11
- Added standalone `README_WINDOWS_GIT_BASH_EN.md` with complete Windows clone/nested-GUI install/Conda/Tk/validation instructions, based on canonical v0.1.1 layout.
- Reviewed original upstream README/main config/MouseGaze and Tobii ioHub YAML plus all 8 demo fixture configs; added 87-entry single-source parameter catalog with brief and detailed Polish descriptions, scoped provenance and editability status.
- Added deterministic `docs/PARAMETER_MANUAL_PL.md` and renderer with a sync check. Do not introduce a manual hyperlink into the GUI at this stage.
- Added lightweight blue circular `i` icon next to current environment, YAML form, instruction, gaze and runtime preference parameters; click opens a short Tk speech bubble, with toggle/X/Escape/outside-click closing.
- Added GUI and non-GUI help coverage regressions, screenshot, ADR-0013, scope/docs and append-only logs. Original upstream/demo source, YAML/profile semantics, experiment start/stop status unchanged.

## v0.1.3 — bilingual UI / independent tooltip language (2026-10-11)
- Added Polish/English interface switch and independent short-tooltip language choice; Polish default and existing full Polish manual retained.
- Added English title/short overlays for all 87 help records; no English long manual and no in-app manual link.
- UI-only persistent settings and safe language switching; original YAML/profile/demo/runtime APIs unchanged.
- Added 7 localization tests, Tk PL/EN screenshots, ADR-0014 and docs/UI_LANGUAGE_V013.md.

## v0.1.4-bilingual-documentation — 2026-10-11
- Expanded English parameter overlay to 87 detailed descriptions, refined ambiguous PL/EN tooltip and manual wording, preserved 87 stable keys/statuses/sources and source YAML identifiers.
- Rebuilt deterministic Polish reference and added the full English `PARAMETER_MANUAL_EN.md` with identical coverage; `--check` verifies both manuals.
- Added PL/EN installation guides, current user guides, paired documentation indexes and bilingual parity contract; updated versioned README pointers and marked older release-specific notes historical.
- GUI-only presentation adjustment: top informational label now names both manual files, without opening or linking manuals. No change to demo selection, YAML/profile formats, gaze/runtime behavior or experiment launch.
- Added ADR-0015, bilingual documentation tests and append-only logs. Windows native and Tobii hardware testing remain open.

## v0.1.5 — native demo launch (2026-10-11)
- Added `runtime.py`, `launch_child.py`, `runner.py` for app-private YAML snapshots and genuine subprocess launch of all seven variants; Time-Series uses Machine then PV in separate children.
- Added Start/Stop buttons and live/persistent run log, selected gaze/voice/raw/trials/logging propagation, preflight errors, collection-vs-process status and cancellation.
- Updated bilingual launch docs/help, eight fake-runtime regressions, ADR-0016, and retained older decisions/history. Original source repositories remain untouched.

## v0.1.6 — explicit demo adapter import and complete log copy (2026-10-11)
- Fixed `ModuleNotFoundError: No module named 'tools.demo_runtime_adapters'` reported on Windows for adapter-backed UX A/B, Text Search and Image Semantic. Child now loads `demo_root/tools/demo_runtime_adapters.py` by exact file path, not generic Python package name; prints source and adapter kind.
- Added missing-adapter preflight for special demos; Test Demo and Time-Series unaffected by adapter requirement.
- Added PL/EN **Copy entire log / Kopiuj cały log** button to Experiment log window; complete visible text including GUI `[STATUS]`/`[FINAL]` is copied. Popup reopen retains session log view; next run starts fresh.
- Added PL/EN issue/retest guides, ADR-0017 and adapter/clipboard regression tests. Original repo sources, runtime YAML schemas, profiles, gaze mode and trial sequencing unchanged.

## v0.1.7-portable-project-storage — 2026-10-11
- New sibling `tobii-pytracker/projects/<project>/` folders, one per independent project; GUI Project chooser and New project action, with Polish and English captions. Saved profiles migrate by copy from the old app-private store into each variant's default project.
- Each launch writes project-current and per-run GUI configuration, exact main/ioHub YAML copies, immutable run manifest and completion result; datasets/analysis still use the configured `output.folder`.
- Cryptographically random 5-character case-sensitive `[A-Za-z0-9]` execution ID with exclusive run directory creation. Raw and GUI log filenames carry completion timestamp to the second plus the shared ID. Full GUI log includes `[STATUS]` and `[FINAL]`.
- Removed per-line permanent console.log writes during experiment: 256-KiB memory spool with temporary overflow, one write after child exit, and one complete GUI log write after final status. Logging I/O cannot abort the child. Process flags/adapter code frozen.

## v0.1.8 — lazy modular navigation (2026-10-11)
- Added a small, permanent top navigation bar (Experiment / Logs / Diagnostics / Statistics) with shared read-only project context and Polish/English labels.
- Embedded the existing Experiment screen as a persistent `PytrackerGUI` child of `AppShell`, without changing its six tabs, YAML/profile semantics, run launch/stop or source/demo code.
- Added three independent placeholder screens in `screens.py`; they are instantiated only on their first visit, retained afterward, and perform no I/O, polling or analysis.
- Preserved unsaved edits, project selection, tooltips and existing Experiment log popup through screen switching. Main-window close still delegates to the Experiment owner.
- Added v0.1.8 PL/EN architecture guides, ADR-0019, five navigation regression tests and a real Tk/Xvfb preview. All historical logs are append-only.

## v0.1.9 — `experiments/` execution history directory (2026-10-11)
- Changed only execution-history directory allocation from `projects/<name>/runs/<time>_<ID>/` to `projects/<name>/experiments/<time>_<ID>/` (also `home/experiments/` for isolated non-project test callers); no backward-compatibility alias or migration.
- Retained project-global `project.json`, `profiles/` and `current-settings.json`; per-execution YAML/ioHub snapshots, manifests, process result and deferred console/GUI logs retain filenames, ID policy, ownership and timing.
- Added paired PL/EN storage guides, ADR-0020 and focused layout/nonregression tests. Original repos, GUI navigation, PsychoPy process control and data `output.folder` remain unchanged.

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- Appearance-only refresh of navigation, editor, lists, ttk buttons/tabs/fields, dark Tk text editors and help popovers. Small icon assets cached once per root. No feature, storage, runtime or language behavior changes.
- Version incremented, PL/EN visual docs, ADR-0021 and targeted regression tests added. Existing historical log content retained.

## v0.2.1 — lighter accent, larger icons and lazy module dashboard (2026-10-11)
- Restored the original ◈ brand icon with a larger clickable product name; brand click opens a lazily created four-tile chooser using existing screen selection.
- Lightened orange, regenerated cached PNG icons at 28×28 and halved selected-tab horizontal padding (12→6 px); kept form font sizes.
- Added PL/EN change documentation, ADR-0022, real Tk screenshots and focused navigation/appearance tests. Experiment logic, YAML, projects and launcher unaffected.

## v0.2.2 — brand logo beside title (2026-10-11)
- Minimal visual-only update: added a packaged eye-tracking logo icon next to the top-left `pytracker-gui` brand, keeping the existing ◈ mark, click-to-dashboard behavior and all other UI logic unchanged.
- Added one lightweight cached PNG asset and a tiny theme helper for loading it once per Tk root. No runtime, storage, launch or navigation logic changes.

## v0.2.3 — HiDPI text and icon sharpening (2026-10-11)
- Appearance-only refinement: enabled native Windows HiDPI awareness before Tk startup and applied runtime Tk scaling from the actual monitor DPI for crisper text rendering on high-resolution displays.
- Regenerated packaged UI icons at larger native resolutions (40×40, brand logo 36×36) to reduce blur when displayed on dense screens, with no functional changes to launcher, storage, YAML or navigation.

## v0.2.4 — contextual manual and round brand (2026-10-11)
- Replaced the top-left historical ◈ sign with a white circular backing around the existing logo while keeping its home/dashboard click action.
- Added a lazily created Manual screen to top navigation and dashboard; all 87 pre-existing bilingual extended descriptions are searchable.
- Added the orange `man` deep link to existing help popovers; it opens the matching parameter directly without touching Experiment state. No launcher, profile, YAML or project storage changes.

## v0.2.5 — project terminology and English option reference (2026-10-11)
- Updated user-facing GUI starter-demo labels and launch/stop wording to **starter projects/projects** while retaining all existing source names, run identifiers, configurations and behavior.
- English manual is now the editorial baseline. Added 28 English option sections documenting 70 discrete values, shared by Markdown and the in-app searchable Manual. Polish parameter catalogue and manual remain byte-identical.
- Added regression tests, ADR-0024 and English option-reference checkpoint. Runtime process and project-storage code were not changed.

## v0.2.6 — green option values and original upstream RST manual (2026-10-11)
- Retained the existing Manual parameter catalogue as the default Index tab and added a separate on-demand Documentation tab browsing only original upstream `docs/**/*.rst`.
- Colored English selectable option values green while leaving the `Available options` heading muted. Tooltip `man` links continue to select Index.
- Source RST is viewed read-only; no Sphinx, demo docs, network or runtime changes. Added ADR-0025 and paired user guides.

## v0.2.8 — exact run ID → measurement session binding (2026-10-12)
- Isolated every block’s native measurement output beneath its originally configured folder using the existing five-character run ID; original profile/YAML/upstream are unchanged.
- Validated exact-session locations instead of selecting newest results by timestamp. Persisted block-level output-to-CSV metadata in `result.json`; ambiguity fails closed.
- Added focused provenance tests, PL/EN docs and ADR-0027. Visual theme remains exactly v0.2.6. Deferred any log-memory limit changes.

## v0.2.9 — optional automatic log display (2026-10-12)
- Added default-ON Auto-show logs toggle beside Show Logs (PL/EN), stored only in app-private settings. OFF suppresses automatic popup/Tk console redraw while preserving manual Show Logs.
- Bound the visible log tail to 256 KiB / 2,000 lines and retained the complete ordered GUI log in a separate 256-KiB spill-to-OS-temp spool; final `experiment_*.log` remains complete and is published only after session completion. Copy entire log reads full spool or finalized archive on demand.
- Did not change v0.2.6 palette, PsychoPy runtime, source adapters, measurement-ID binding, project/YAML formats or any other screens. Documentation PL/EN and regression tests added.

## v0.2.10 — Manual demo-project tree and lightweight formatting (2026-10-12)
- Removed Diagnostics from the top navigation and dashboard only; existing Experiment preflight checks are unchanged.
- Added a lazily constructed Demo Project Documentation tab with project-grouped Markdown tree from the original demo checkout, preserving Index as default and tooltip `man` deep links.
- Applied optional light native-Tk heading/list/code formatting to local Markdown and upstream RST (no added parser or web engine; large docs have unstyled fallback).
- Added bilingual documentation, ADR-0029 and focused regression tests. No changes to launchers, measurement binding, projects, log buffering, or theme.

## v0.2.11 — Manual tree text contrast (2026-10-12)
- Scoped dark `DemoDocs.Treeview` style fixes unreadable light-on-light project tree rows on Windows. The Markdown/RST preview, all other widgets and functionality remain unchanged.
- Added direct style-contrast regression, bilingual fix note, and append-only verification history.

## v0.2.12 — single incremental low-priority run journal (2026-10-12)
- Replaced two end-only per-run `.log` files with one background-written `experiment_<start>_<ID>.log.part`. A complete, lossless finish is renamed to `.log`; cancelled/crashed/overflowed runs retain `.part` as interrupted evidence.
- 256-KiB byte-ring keeps the latest unpersisted entries under disk backpressure; low-priority writer batches 64 KiB, schedules at 15 s or 192 KiB pressure, with minimum 5 s I/O spacing during acquisition. No child reader disk I/O, no new runtime dependencies.
- GUI copy/full preview, PL/EN Manual, project data, runtime, IDs and appearance unchanged. See ADR-0030 and new bilingual documentation.

## v0.2.13 — Logs read-only history and settings dashboard, stage 1 (2026-10-12)
- Replaced inert Logs placeholder with a lazy project/run chooser, read-only six-category configuration dashboard, and folded YAML details. Uses existing experiments folders and immutable run snapshots; complete/incomplete journal state separate from process status.
- Stage 2 Console Log control deliberately disabled. No data.csv, PsychoPy/runtime, logging, global palette, Manual, editor, project storage or source repository changes. No periodic scans/writes/threads.
- Added `log_history.py`, `logs_screen.py`, scoped tests, bilingual docs and ADR-0031. Validation results in VALIDATION_LOG.

## v0.2.14 — Logs stage 2, bounded console viewer and legibility (2026-10-12)
- Enabled archived Console Log for an exact run ID: lazy read-only `.log` / `.log.part` pages capped at 64 KiB and 2,000 lines; First/Previous/Next/Latest, manual refresh and Copy page. No measurement reads or background polling.
- Increased Logs-only fonts by one step; lightened local selection to `#FFC187` with dark text. All other GUI styles remain v0.2.6/v0.2.13.
- Added exact run journal name checking, bilingual docs, ADR-0032 and 12 targeted stage-2 tests; no change to PsychoPy, YAML, runner, journal writer, project storage or Manual.

## v0.2.16 — Classic action buttons, native resizable panels (2026-10-12)
- Rebased directly to exact v0.2.14. Rejected v0.2.15 equal-sized button experiment; original environment and editor footer button layout, styles and dimensions restored.
- Retained only three draggable `tk.PanedWindow` separators from v0.2.15 (Experiment sidebar/editor; Logs selector/content; Logs projects/runs).
- Added existing compact PNG icons only to Check Python, Detect layout and Apply changes; no added assets, dependencies or global theme changes.
- Added targeted regression, bilingual notes and ADR-0034. Runtime and logging v0.2.14 stay frozen.

## v0.2.17 — Environment button widths and GUI Documentation (2026-10-12)
- Existing Save paths, Check Python, Load repository and Detect layout buttons now fill their shared grid column width only; all styling, heights, icons, padding, commands and footer layout remain as v0.2.16.
- New lazy read-only Manual → GUI Documentation tab with EN/PL project guides grouped by current/feature docs; explicit file allowlist, Markdown viewer and bounded reads. Earlier three tabs and parameter `man` deep links unchanged.
- Current EN/PL guides and documentation indexes updated; no PsychoPy, YAML, run ownership, logs or global theme changes.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
v0.2.18: Home-only fixed 546×365 image buttons from four approved images; no resizing at runtime; overflow-only scrollbars, unchanged navigation.

## v0.2.19 — Default window size (2026-10-12)
v0.2.19: increased the default application window size to screenshot-derived 1429×1097 (screen-constrained); no other runtime/layout changes.

## v0.2.20 — Environment icons (2026-10-12)
v0.2.20: enlarged the Save paths icon artwork within its 40×40 image box and changed Detect layout icon from 20×20 to existing full-size 40×40 folder asset; no other runtime changes.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
v0.2.22: Finalized the scoped GUI Settings screen after Manual (window-size presets, existing path/preference summary) and installed the user-approved Logs artwork on the Home tile. No other runtime behavior changed.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: replaced four static 546×365 Home PNGs from user-supplied recolored images, without changing UI layout, actions or runtime asset-loading logic.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: independent light-burgundy (`#C77D8F`) small-icon tint parameter and one-time stdlib alpha-mask rendering, retaining orange selections, ink icons, Home PNGs and all experiment features.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
v0.2.25: darkened the configurable idle small-icon tint to `#A9526B`; restored original orange icon artwork for selected navigation and Experiment tabs. No other GUI behavior changed.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: Experiment-only default idle icon tint `#A46628` with orange selected icons preserved; static `Experiment setup` panel heading replaces the dynamic demo name. Native Windows title bar unchanged.

## v0.2.34 — Polish language alignment (2026-10-13)

- Updated Polish GUI Settings labels, 31 help snippets, the Polish GUI Settings reference and User Guide based on the accepted English v0.2.33 baseline.
- GUI Settings `man` links select the guide matching the interface language; Polish headings use `Opcja:` while stable option identifiers remain unchanged.
- Added Polish descriptions for all 70 discrete values across 28 experiment parameters; the local Manual Index and generated Polish parameter manual now display these choices. English descriptions and all experiment/runtime behavior remain unchanged.
- Added targeted Polish-help parity/navigation tests. No changes to experiment execution, storage, controls, icons, or new settings.

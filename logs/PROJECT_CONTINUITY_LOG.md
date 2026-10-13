# PROJECT_CONTINUITY_LOG.md — public resume ledger

**Project:** pytracker-gui
**Current checkpoint:** v0.0.0-plan (2026-10-10)
**State:** architecture/documentation only; nothing executable.
**Parent project:** inspired by tobii-pytracker-demo v1.17.0; independent repository and versioning.
**Accepted requirements from user:** lightweight Windows/Linux GUI, configure application, input new experiment data, invoke existing runtime rather than reimplement, cumulative decision/debug records.
**Proposed decisions (not user-approved yet):** Tkinter/ttk, separated runtime process, native-first with Docker adapter later, 3 built-in modality wizard.
**Evidence:** delivered ZIPs; source audit in `docs/SOURCE_AUDIT.md` and user-supplied release logs. Missing exact upstream SHA and physical acceptance.
**Modules/files in scope now:** README, docs, adr, logs, VERSION, MANIFEST; no source/runtime tree.
**Last completed action:** produced planning package and source audit; verify ZIP manifest/build result before release.
**Exact next action:** gate M0: get exact upstream tree and certify version/CLI/config before starting M1 native launcher code.

## CURRENT CHECKPOINT — v0.0.1-upstream-demo-control-plan (2026-10-10)
**Source of truth supersession:** wcześniejszy v0.0.0 wizard jest historyczny; M1 dotyczy tylko existing demos and config. Current docs: PROJECT_CURRENT_SCOPE, M1_SCOPE_AND_ACCEPTANCE, DEMO_LAUNCH_MATRIX, CONFIG_CONTROL_MATRIX, M1_PHASED_IMPLEMENTATION_AND_GATES.
**Kod GUI:** brak. **Known blocker:** exact SHA upstream z publicznego `main` nie jest przypięty, nie mamy runtime Windows/Linux/HW. **High priority defect to avoid:** UX/Text/Image wrappers hardcode gaze=true, voice=false, raw=false; bridge musi realnie obsługiwać kontrolki. **Next phase:** v0.1.0 env+demo registry, P0 provenance, fake-process/OS test. **Preserve all prior logs append-only.**

## CURRENT CHECKPOINT — v0.1.0-ui-config-prototype (2026-10-10)
**State:** functional standalone Tk GUI for DEMO configuration; M1 incomplete. **Active source:** `pytracker_gui/{catalog,app,fields,yamlconfig,profiles,storage,validation,environment}.py`, `run_gui.py`, `requirements-gui.txt`, `tests/`. **Functional:** 7 selector variants (8 configs), no engine, 3-mode gaze choice, IOHub file path, source-derived main YAML forms/raw editing, profiles, static validator, interpreter probe. **Safety:** source files remain unchanged, no psychopy import. **Validation:** 13/13 tests PASS Linux Python 3.13 under Xvfb; no real Windows or Tobii test. **Deferred:** full ioHub forms, child bridge, collection checks, installer/executable. **Next exact action:** pin upstream SHA + environment parity, build fake child executor (Windows/Linux argv,CWD,lifecycle), then child adapter parity for 3 hardcoded demos, followed by run integration.

## CURRENT CHECKPOINT — v0.1.1-nested-repository-layout (2026-10-11)
**Parent:** exact v0.1.0-ui-config-prototype. **Change:** corrected Windows clone tree and installation to `tobii-pytracker/` with two independent nested folders `tobii-pytracker-demo/` (mszac official) and `pytracker-gui/` (ZIP now, future remote). **Code:** `pytracker_gui/layout.py` discovers from source location; `run_gui.py --check-layout` validates upstream/demo/eight YAML without Tk; GUI auto-populates paths, restores defaults and selects upstream mouse/Tobii YAML. **Scope:** UI configuration-only; no subprocess launch or original changes. **Test:** host Linux Python 3.13/Xvfb 17 tests PASS; Windows not run. **Current setup:** `docs/INSTALL_AND_USE_V011_GIT_BASH_WINDOWS.md`; historical v0.1.0 instructions superseded. **Next exact action:** real Windows Git clones, save both HEAD SHA hashes, `--check-layout`/Tk/profile dry run, then process adapter simulator and native child bridge in a later release.

## CURRENT CHECKPOINT — v0.1.2-parameter-help-manual (2026-10-11)
**Parent:** exact v0.1.1 ZIP. **New state:** environment/form/instructions/run preference labels have clickable blue `i` icons with short help. One source file `pytracker_gui/parameter_help.json` stores 87 brief and long Polish descriptions, with each setting linked to upstream/demo source provenance and editability; generated `docs/PARAMETER_MANUAL_PL.md` is synchronized by tool/test. `README_WINDOWS_GIT_BASH_EN.md` gives independent English Windows Git Bash instructions. **No manual hyperlink and no ioHub internal editor.** **Architecture:** stdlib Tk only, cached static JSON, no new GUI dependencies, no changes to original two Git checkouts or profile semantics. **Gates:** 23/23 Linux Xvfb tests; screenshot of real help bubble; schema/manual sync checks. **Still NOT RUN:** Windows/Conda Python 3.10, PsychoPy/ioHub runtime, Tobii hardware, real Git clone HEAD provenance. **Exact next step:** have user clone both repositories on Windows, capture HEAD SHA and test `--check-layout`, `python run_gui.py`, click every help category and save a profile; if confirmed, proceed with fake child process and native adapter launch bridge as previously planned.

## CURRENT CHECKPOINT — v0.1.3-bilingual-ui (2026-10-11)
**Parent:** v0.1.2 parameter-help-manual. **Change:** presentation-only PL(default)/EN interface and independently selectable short popover language, user preference under private settings JSON. `pytracker_gui/i18n.py` maps visible UI text; `parameter_help_en.json` covers 87 English popup titles/short explanations without modifying `parameter_help.json` or `docs/PARAMETER_MANUAL_PL.md`. Source/demo repos, seven variants, YAML/profile semantics, ioHub path, and launch-disabled state unchanged. **Guards:** active edits committed in memory before rebuild; malformed YAML rejects switch. **Verification:** inherited 23 tests plus 7 new tests (30/30) Linux/Xvfb; full Polish manual sync; PL/EN real-window screenshots. **Open:** physical Windows/Tobii NOT RUN; no English full manual or in-GUI manual link; native child launch remains deferred. **Exact next step:** on Windows with pytracker-env check `--check-layout`, open GUI in PL, switch to EN, set Polish tooltip preference, edit/save profile, restart and verify persisted language and unchanged YAML; then return to previously planned child launch bridge.

## CURRENT CHECKPOINT — v0.1.4-bilingual-documentation (2026-10-11)
**Parent:** exact v0.1.3-bilingual-ui ZIP. **Functional state unchanged:** Tkinter editor, 7 variants/8 YAML, PL(default)/EN GUI and separate PL/EN short popovers, profile/YAML editing, static checks; no native experiment launch. **Documentation:** 87/87 PL and EN short + extended help entries, deterministic two-manual generator, paired current PL/EN setup and user guides, paired indexes, ADR-0015. **Presentation only:** top informational label identifies both manual paths, without an in-app document viewer. **Validation:** bilingual sync + full Linux Python 3.13 Xvfb 35 tests PASS; fresh packaging/manifest recorded in validation log. **Risk:** no Windows/Conda Python 3.10/PsychoPy/ioHub/Tobii testing, upstream HEAD needs pinning. **Next:** real Windows GUI/tooltip/manual parity and profile smoke; then fake child subprocess and native adapter launch bridge.

## CURRENT CHECKPOINT — v0.1.5-native-demo-launch (2026-10-11)
**Direct parent:** v0.1.4 bilingual documentation. **New capability:** real start/stop via isolated Python 3.10 child using app-private YAML snapshots. Seven variants supported; two Time-Series children in Machine → PV order. Existing original `demo_runtime_adapters` installed only in child; dynamic gaze/voice/raw/loops/log-level passed to upstream `main.main`. App-private per-run `run.json`, copied YAML, `console.log`, `result.json`. Process completion, collection validation, cancellation and failure are separate statuses; no false hardware PASS. **Frozen ownership:** no upstream/demo source changes, GUI remains independently deployable. **Tests:** Linux Python3.13 Xvfb 43/43 fake/mock + inherited; real Windows/PsychoPy/Tobii not run. **Exact next action:** Windows in `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}`, capture both `git rev-parse HEAD`, `--check-layout`, start Test Demo MouseGaze default 3 trials, inspect csv/log/result, stop/relaunch, then variants and physical Tobii. **Unresolved:** focus, Windows tree stop, audio/raw hardware gate, pinned upstream identity.

## CURRENT CHECKPOINT — v0.1.6-demo-adapter-import-log-copy (2026-10-11)
**Direct parent:** exact v0.1.5 native-demo-launch. **User evidence:** real Windows Test Demo MouseGaze finished 3 trials and `NATIVE_TEST_DEMO_COLLECTION_PASS`, whereas Text Search EN failed before PsychoPy on `from tools.demo_runtime_adapters import ...`; user explicitly excluded the prior fullscreen issue. **Fix:** child-only file-origin adapter loader in `launch_child.py`, missing-adapter preflight in `runtime.py`. **UI:** `app.py` copies full current Experiment log to clipboard with PL/EN button; session text persists when popup closes/reopens. **Frozen boundaries:** upstream/demo repos untouched; no YAML/profile schema changes, no gaze/voice/raw/trial behavior changes, no emergency-stop work. **Evidence:** original v1.17.0 adapter used in isolated fake upstream+PsychoPy check for five variants; automated host Xvfb regressions, two manual languages. **Not proved:** real Windows runtime for adapter-backed demos and hardware. **Next exact action:** user installs ZIP under `tobii-pytracker/pytracker-gui`, runs `--check-layout`, selects Text Search EN MouseGaze 12 trials and observes adapter source/GUI log/csv status, then UX EN/PL, Search PL, Image Semantic; copy log on any failure, capture Git SHAs.

## CURRENT CHECKPOINT — v0.1.7-portable-project-storage (2026-10-11)
**Parent:** exact v0.1.6-demo-adapter-import-log-copy. **User requirement:** put everything required to resume a configured study (excluding measurements/analyses) under one lightweight, copyable project folder, with full post-run GUI console and five-character case-sensitive run ID plus save-time timestamp.
**Current architecture:** real installation uses `tobii-pytracker/projects/<name>/` sibling to `pytracker-gui/` and `tobii-pytracker-demo/`. Project selector+New, per-variant isolation, `project.json`, `profiles/<variant>/*.yaml`, `current-settings.json`, `runs/<starttime>_<ID>/{run.json,main/machine/pv.yaml,eyetracker.yaml,gui-settings.json,result.json,console_<endtime>_<ID>.log,experiment_<endtime>_<ID>.log}`. Other project names are valid. Old app-private profiles are copied once into default project; old run logs left intact.
**I/O policy:** only prelaunch YAML/settings and post-exit raw/post-final UI log writes inside projects; bounded 256-KiB spool while running. Logs never abort a running experiment. GUI log contains GUI-only STATUS/FINAL. `output.folder` unchanged. Original upstream/demo sources untouched.
**Open:** actual Windows/Conda/Physical Tobii checks, new-checkout copy exercise with external absolute dataset paths, disk failure after process exit. **Next exact gate:** install v0.1.7 ZIP beside original repos on Windows, create two projects for Text Search EN, configure/save separately, run Test Demo MouseGaze, check five-character ID in both log files and exact GUI output; copy one project to fresh upstream clone, validate profile/ioHub path rebasing and logs.
**Release closure:** full ZIP 118 files, 117 manifest entries; fresh extraction + 66/66 fake-runtime/Xvfb tests + byte/mode patch reconstruction PASS. Parent unchanged beyond requested project storage, project chooser, and log persistence scope. Physical Windows validation still pending.

## CURRENT CHECKPOINT — v0.1.8-lazy-navigation-shell (2026-10-11)
**Parent:** exact accepted v0.1.7-portable-project-storage. **Requested scope:** independent screens, lazy construction, low CPU overhead and stable existing Experiment behavior; no implementation of future log/diagnostic/statistic features yet.
**Current UI:** `AppShell` (`pytracker_gui/shell.py`) owns only top-level navigation, a readonly project name, the display host and close delegation. `PytrackerGUI` in `app.py` stays the stateful Experiment owner and retains its original six tabs. `PlaceholderScreen` in `screens.py` is a separate, minimal module for each future screen; created on first selection only. Project label observes existing Tk variable; UI language switch sends a presentation-only callback. No new threads/timers/processes/file watchers/scanners. Navigation does not commit YAML and does not stop/restart sessions.
**Preserved:** all seven demos, profiles, `projects/` run/log formats and IDs, full Experiment log copy, adapter file import, bilingual parameter help/manuals and existing launcher functions.
**Validation:** host regression 71/71 Linux Python3.13/Xvfb PASS, real Tk screenshot, PL/EN 87/87 manual sync. Release artifact manifest/patch/fresh verification tracked in VALIDATION_LOG. Windows/Conda/PsychoPy/Tobii not executed for this version.
**Next gate:** Windows update in the same nested checkout; navigate four views with unsaved settings and active sessions, verify PL/EN, project context, existing Start/Stop/Experiment log and monitor geometry. Add real Logs screen only after separate requirements and tests.

## CURRENT CHECKPOINT — v0.1.9-experiments-directory (2026-10-11)
**Parent:** exact v0.1.8-lazy-navigation-shell. **Scope:** only project execution history directory placement. `projects/<experiment_name>/` still holds project metadata, reusable profiles and `current-settings.json`; the new canonical location is `projects/<experiment_name>/experiments/<YYYYMMDD_HHMMSS>_<ID>/` for all execution snapshots, `run.json`, `result.json` and both timestamped five-character-ID logs. Project names are independently user-selected, not hardcoded `MyResearch`. No old `runs/` compatibility, automatic migration or deletion. CSV and analysis remain under the configured demo `output.folder`. Existing lazy AppShell, editor, launcher, buffered post-completion log writes, bilingual manuals and upstream adapters are untouched.
**Verification checkpoint:** local host tests and fresh-archive/patch gates must pass; physical Windows/PsychoPy/Tobii gate remains external. **Next user action:** update `pytracker-gui/` only, leave `projects/` and repositories in place, create/start an experiment, inspect new folder, paired logs and unchanged data output. Historic runs remain untouched unless user manually archives them.

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- Latest snapshot: v0.2.0-dark-orange-theme, direct parent v0.1.9-experiments-directory. `theme.py` owns the palette and caches packaged tiny icons on the root; `AppShell` owns nav icon state; `PytrackerGUI` styles existing controls. All screens and per-project execution paths remain unchanged.
- Resume by inspecting Windows rendering first, then develop future Logs screen as a separate iteration only after explicit user approval. Keep test and release gates and append-only logs.

## Continuation after v0.2.1 (2026-10-11)
- Current visual shell: original ◈ mark and larger clickable name -> lazy 4-tile chooser -> existing `AppShell.select_screen`; existing Experiment is always persistent. 28px static PNGs and lighter orange. Selected tab x-padding 6 rather than 12; form fonts unchanged.
- Next user hardware gate: Windows Git Bash `pytracker-env`, click brand and tiles in PL/EN, check selected tab and higher-DPI icons, verify intact Experiment settings and real demo launch. Future screen features stay out of current scope.

## CURRENT CHECKPOINT — v0.2.4-manual-logo (2026-10-11)
**Parent:** v0.2.3-hidpi-sharpening. **Scope:** only a white-roundel brand asset, retirement of the old ◈ glyph, a fifth lazy Manual screen, and per-tooltip `man` deep links. **Manual source:** existing 87 parameter records, PL/EN. **Frozen:** experiment runner, seven demo variants, project storage, YAML/profile formats, gaze and history logging. **Next step:** Windows smoke: help popover `man`, PL/EN help preferences, high-DPI logo contrast, 5 dashboard tiles, and real demo launch regression.

## v0.2.5 checkpoint (2026-10-11)
- Current visual/manual feature: GUI uses project/starter-project labels; internal seven demo keys and source repository paths are frozen.
- The English manual JSON is the editorial source for selectable-value descriptions. Its Markdown and in-app Manual presentations must stay synchronized. Polish manual remains unchanged until a subsequent translation iteration.
- Exact next step: verify project labeling and English option sections on Windows at the installed UI scale; then add a reviewed PL translation if requested.

## v0.2.6 — continuity
- Manual now has Index (original default) and Documentation (local upstream `.rst` reader) tabs. Tooltip `man` always targets Index. `Available options` values are green; English option descriptions and Polish manual source unchanged.
- Upstream docs come exclusively from the user-selected original `tobii-pytracker/docs/` tree, not the nested demo repo. The viewer is read-only and lazy, with no external dependencies.
- Remaining physical gate: Windows display / docs browsing / previous starter-project launch.

## v0.2.8 — provenance contract checkpoint
- Built directly from accepted v0.2.6 ZIP (v0.2.7 Soft Depth remains rejected). One output root per run+block with exact CSV association in `result.json`. Next physical Windows gate: Test Demo/UX/Time-Series output and CSV association; future independent task: cap visible GUI log memory while retaining complete archives.

## v0.2.9 — handoff
Parent: exact v0.2.8 release (which retains v0.2.6 palette). New PL/EN default-ON Auto-show logs toggle, app-private setting, manual popup override. Bounded live preview and full post-run spool/archive; runner and YAML/storage/measurement provenance unchanged. Validate on Windows: toggle OFF, long UX, no popup, manually open viewer, stop/complete, check `experiment_*.log` full and `console_*.log` present. Review ADR-0028 and docs/AUTO_LOG_DISPLAY_V029_PL.md / _EN.md. Do not adopt v0.2.7 palette.

## v0.2.10 checkpoint — manual documentation tree
- Direct parent v0.2.9. Current module routes: Experiment, Logs, Statistics, Manual, plus brand-activated Home dashboard; Diagnostics deliberately removed from these routes, not from Experiment preflight tools.
- Manual Index/deep links, upstream RST Documentation and new lazy Demo Project Documentation remain separate. Source of demo Markdown is the runtime-selected demo-root checkout, never bundled copied documents.
- Next optional work: validate tree readability on Windows HiDPI and expand renderer only if user requests it. Do not alter PsychoPy/runner/data-plane in this checkpoint.

## v0.2.11 checkpoint
- Exact direct parent v0.2.10. Only the demo documentation `Treeview` visual style is changed in production code. Renderers, source discovery, lazy behavior, launchers, projects, runtime and theme remain unchanged.
- A local regression checks default and selected ttk style colors. Preserve current 0.2.6-derived palette.

## 2026-10-12 — v0.2.12 handoff
Project runs now use one append-only `experiment_*.log.part` during acquisition, instead of two distinct final log files. It becomes `.log` after clean, lossless finalization. On interruption, `.part` persists for future inspection (no recovery code yet). Existing 256-KiB RAM limit, 2,000-line GUI preview, run IDs, exact measurement binding and all demo functionality remain intact. Next Windows hardware gate: live log, clean finish, Stop -> .part, disk pressure, and logging with Auto-show OFF.

## 2026-10-12 — v0.2.13 handoff
Base: byte-exact v0.2.12 incremental single log. Scope: read-only Logs project/run settings summary only; console content browser postponed. Production changed: `shell.py` routing, new `log_history.py`, `logs_screen.py`, and version. All other production files frozen. UI states and data sources documented in `LOGS_HISTORY_STAGE1_V0213_PL/EN.md`; subsequent stage is chunked read-only console viewer.

## v0.2.14 — checkpoint
Base exact v0.2.13. Logs stage 2 archived Console Log read-only viewer is enabled. Selector lists/cards/controls now use slightly larger type and lighter scoped orange highlight. Pure `log_viewer.py`, updates to `logs_screen.py` and exact journal classification in `log_history.py`, targeted regression and paired docs/ADR. Other application modules and GUI theme frozen. Next: Windows visual check and real growing `.part` during an active UX run; interrupted-log repair remains explicitly deferred.

## v0.2.16 checkpoint — Classic buttons with adjustable panel boundaries
- Exact parent: v0.2.14 Logs Console Viewer; v0.2.15 equal-sized action-bar design superseded/rejected.
- Runtime/persistence and all code outside Experiment `app.py` and Logs `logs_screen.py` frozen from exact v0.2.14.
- Next external gate: verify original buttons + three opt-in icons + sash limits on Windows before any further UI work.

## v0.2.17 checkpoint — 2026-10-12
- Direct parent: complete v0.2.16-documentation-sync (code lineage v0.2.14; not the rejected v0.2.15 button redesign).
- Added only equal horizontal widths to four existing Environment actions and a lazy read-only Manual GUI Documentation tab. All other production behavior is frozen. See ADR-0035 and GUI_DOCUMENTATION_V0217_{EN,PL}.md.
- Next external gate: Windows mouse/HiDPI and local guide viewing, PL/EN labels; no feature work beyond approved scope.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
Parent exact v0.2.17 Full; new Home screen-only changes in screens.py, four 546×365 PNGs, tests and documents. Next gate: Windows Home click/resize/overflow.

## v0.2.19 — Default window size (2026-10-12)
v0.2.19 derives directly from exact v0.2.18. Runtime delta: only numeric initial size caps in shell.py and version identity. Preserve all previously frozen modules.

## v0.2.20 — Environment icons (2026-10-12)
v0.2.20 derives from exact v0.2.19; only Environment icons changed: Save paths local enlarged glyph, Detect layout full-size folder. Runner, GUI screens and logging frozen.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
v0.2.22 is a narrowly scoped successor to v0.2.21: replacement Home Logs PNG, compact GUI Settings UI/persistent window-size choices; all previous PsychoPy, Logs, Manual and project behavior remains frozen.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: direct successor to exact v0.2.22. Future work continues with original GUI Settings and unchanged experiment/logging/navigation behavior.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: continue mainline from exact v0.2.23. Only icon tint implementation, small alpha masks, targeted tests, documentation, ADR-0041 and release identity. Do not alter orange theme, dark ink assets, dashboard or runtime logic.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
v0.2.25 is a direct successor to exact v0.2.24. Only default inactive tint and active-orange selection behavior changed in theme.py; all other production modules and assets are frozen.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: continue from exact v0.2.26 with only Experiment presentation + version changes. PsychoPy, logs, storage, Manual, GUI Settings, other screens and images byte-frozen. Next step: Windows visual check and reject unrelated edits.

## v0.2.34 — Polish localization (2026-10-13)

Scope: translate English v0.2.33 GUI Settings help and documentation, expose Polish option explanations in Experiment Manual. Stable keys/values preserved; runtime remains unchanged. Test gate: focused Tk/interpreter checks and regenerated PL/EN manuals, full ZIP manifest.

# VALIDATION LOG (append-only)

## 2026-10-10 — v0.0.0-plan
- CHECK: dwa dostarczone archiwa można odczytać i wypakować (PASS).
- CHECK: repo payload 104 files (PASS).
- CHECK: SHA-256 dostarczonego repo ZIP `f0c383851426437124c04aa629ab3ea617147740685307a3f662ab41bab48465` zgodny z raportem `release_aux/FINAL_RELEASE_VALIDATION_V1.17.0.md` (PASS).
- CHECK: dataset paths 9 YAML są rozwiązywalne względem demo root (PASS, static).
- CHECK: doktryna upstream config/launcher/validacja w README i historycznych logach (REVIEWED, nie wykonany build).
- NOT_RUN: actual tobii-pytracker runtime, GUI, image display, MouseGaze ioHub, fizyczny Tobii, Docker/VNC, post-hoc notebook.
- NOT_RUN: target Windows/Linux GUI packaging i install.
- CHECK: nowy ZIP i MANIFEST powinien być zweryfikowany przez builder na zakończenie.

## 2026-10-10 — v0.0.1-upstream-demo-control-plan
- STATIC_REVIEW: live public upstream raw source 8 paths + docs = REVIEWED; no pinned git commit; NOT_RUN actual checkout executable.
- STATIC_REVIEW: 9 native YAML files parsed with PyYAML (PASS); config modality paths/output and extra text fields inspected.
- STATIC_REVIEW: 5 demos 7 public variants with time-series sequential blocks, 3 dynamic-flag blockers found (PASS evidence in sources).
- DOCUMENTATION: only planning/log updates + ADR-0007..0010, no runtime/gui code modified.
- NOT_RUN: GUI, native subprocess launch, Windows/Linux, MouseGaze ioHub, Tobii hardware, voice, raw data, data validator integration.
- PACKAGE_GATE: manifest, append-only log preservation, exact-parent patch reconstruction, fresh ZIP integrity to be recorded when built.

## v0.1.0 (2026-10-10)
- Host: Linux, Python 3.13; `python -m compileall -q pytracker_gui tests`: PASS.
- `xvfb-run -a python -m unittest discover -s tests -v`: 13/13 PASS (11 core, 2 GUI integration).
- Catalog unique seven records and eight original YAML fixtures: PASS.
- Comment/unknown-field preservation under ruamel round-trip: PASS (fixtures and custom comment case). Files source unchanged by saving GUI profiles: PASS in GUI smoke.
- Time-series Machine/PV independence and profile save: PASS.
- UI launch under virtual Linux display and PNG capture: PASS.
- Windows, native Python3.10/PsychoPy/ioHub, Tobii, gaze quality, actual collections: NOT RUN.

## v0.1.1 (2026-10-11)
- Source-grounded paths: upstream src/configs/pyproject and demo run-demo.sh, example native YAML names verified against supplied v1.17.0; public demo main config.native.yaml + tools/run-demo.sh confirmed online.
- Linux Python 3.13, Xvfb: `python -m unittest discover -s tests -v` 17/17 PASS (11 inherited core, 2 inherited GUI now using nested repo, 4 new nested-layout regressions).
- Linux `/mnt/data` has no network DNS access; real Git `clone`, Windows native, Python 3.10 PsychoPy/ioHub, hardware Tobii/MouseGaze, session data collection: NOT RUN.
- Current v0.1.1 ZIP/package manifest, append-only logs, direct-parent patch reconstruction and fresh-extract gates: see release closure appended below.

### v0.1.1 release closure (2026-10-11)
- Unit/core/Tk integration Linux Xvfb: 17/17 PASS, including all 7 variants and independent Machine/PV YAML editing.
- Installed-layout synthetic check (`python run_gui.py --check-layout` from unrelated `/tmp` CWD): LAYOUT PASS, all 8 YAML paths detected, default ioHub YAML in upstream configs.
- Historical log prefix checks: CHANGELOG, DECISION_JOURNAL, KNOWN_ISSUES, PROJECT_CONTINUITY_LOG, VALIDATION_LOG, WORK_SESSION_LOG all append-only relative to exact v0.1.0 ZIP.
- Source release diff: git diff --check PASS. Direct exact v0.1.0 + patch reconstruction byte+mode PASS. Packaged ZIP fresh-unpack byte+mode PASS, fresh MANIFEST 70/70 PASS (71 packaged files including MANIFEST).
- Fresh unpack under synthetic canonical upstream + nested demo: no-Tk `--check-layout` PASS, 17/17 tests PASS on Linux Xvfb, post-test MANIFEST 70/70 PASS.
- Deliberately NOT RUN: real Git clone/network access from execution container, Windows Git Bash/Conda activation, native Python 3.10 and PsychoPy/ioHub, Tobii hardware, actual data collection or GUI-based experiment launch.

## v0.1.2 (2026-10-11) — parameter reference and UI controls
- Public source inspection: original sbobek/tobii-pytracker README usage and configuration; RAW upstream general/mouse/Tobii YAML; mszac demo public version 1.17.0; supplied demo ZIP eight exact YAML fixtures. Exact Git main commit SHA not resolved in offline container.
- One-source documentation: 87 short + long entries, unique stable keys, provenance URLs, explicit editable/reference/ioHub-only status; all 25 main form field declarations plus all 27 distinct leaf YAML paths across eight demo fixtures covered. `python tools/render_parameter_manual.py --check`: PASS.
- Linux Python 3.13 under Xvfb: `python -m unittest discover -s tests -v` **23/23 PASS**, including inherited 17 tests and 6 new help coverage/Tk popover tests. Real GUI screenshot with clicked blue `i` generated to `docs/images/v012-linux-xvfb-parameter-help.png`.
- Documentation scope checks: added English Git Bash README; source-only parameters not presented as editable; no manual hyperlink or experiment runner added. Existing app-private profile handling and demo YAML files preserved.
- Release gates: source append-only logs, direct-parent patch byte+mode reconstruction, manifest, fresh ZIP and fresh-unpack test execution verified by release builder; see generated release identity. Actual Windows, Python 3.10/ioHub, Tobii hardware, git clone from container: NOT RUN.

## v0.1.3 language-only validation — 2026-10-11
- Inherited 23 tests + 7 new language/tooltip tests: 30/30 PASS (Linux Python 3.13 + Xvfb).
- 87/87 English short popovers and Polish catalog/manual consistency PASS.
- UI toggle PL→EN→PL and explicit EN GUI+PL help PASS; saved preferences survive GUI re-open; schema/path/profile unchanged.
- Malformed YAML blocks language switching and remains in editor; unsaved valid monitor edit survives switch and saves normally.
- Screenshots from real Tk: docs/images/v013-polish-help.png and v013-english-help.png.
- Full Windows/Conda Python 3.10/PsychoPy/ioHub/Tobii runtime NOT RUN. Release packaging and manifest reported separately at closure.

## v0.1.4 bilingual documentation/source gates — 2026-10-11
- Linux Python 3.13/Xvfb: 35/35 unittest PASS (30 inherited incl. GUI language switch and 5 bilingual documentation parity gates).
- Both current Markdown manuals deterministic with all 87 same identifiers: BILINGUAL_MANUAL_SYNC_PASS 87/87 PL+EN.
- Clarified default GUI vs upstream CLI/ioHub-only scope, schema-key invariance, no experiment start/stop; fresh release ZIP/patch/manifest and immutable-source gates checked at final packaging.
- Real Windows Git Bash/Python 3.10/PsychoPy/ioHub/Tobii/physical MouseGaze: NOT RUN; documentation-only test is not hardware evidence.

## v0.1.5 local validation — 2026-10-11
Linux Python 3.13/Xvfb; original installed PsychoPy/ioHub/Tobii unavailable. Unit tests: 43/43 PASS (35 inherited plus eight new). New fake-native tests exercise immutable snapshots and source immutability for seven variants, preflight errors, dynamic mouse/Tobii/voice/raw flags, two distinct sequential Time-Series child processes, simulated failure blocking PV, user stop blocking PV, and process results in app-private files. `BILINGUAL_MANUAL_SYNC_PASS 87/87` PL/EN. Full parent patch/fresh ZIP/manifest gates recorded in release verification script results. **No native PsychoPy trial, no actual Windows/Tobii runtime performed.**

## v0.1.6 regression evidence — 2026-10-11
- Root cause inspection: child previously imports `tools.demo_runtime_adapters` by generic package name. Original demo v1.17.0 zip has `tools/demo_runtime_adapters.py` but no requirement for a `tools/__init__.py`; Python regular package collision can shadow namespace imports. Public upstream adapter source also checked.
- Host: Linux Python 3.13/Xvfb, 47/47 tests PASS (43 inherited + 4 new). Five adapter-backed variants run with fake native child and adversarial foreign `tools` regular package, with the demo tools `__init__.py` removed. Missing-adapter preflight tested; Test Demo independently remains valid. Tk PL/EN clipboard copies `[RUN]`, `[STATUS]`, `[FINAL]`, and reopening log popup preserves text.
- Additional isolated source test: loaded actual 6,861-byte `tools/demo_runtime_adapters.py` from supplied demo v1.17.0 archive for ux_en/ux_pl/search_en/search_pl/image_en with fake `psychopy.visual` and upstream datasets; all five child processes completed (`REAL_ADAPTER_FAKE_ENV_PASS`). Actual PsychoPy/ioHub/Tobii were NOT invoked.
- PL/EN manual 87/87 determinism expected unchanged; package gates (manifest/fresh ZIP/exact-parent patch) to be confirmed by release builder. Real Windows GUI clipboard and all adapter-backed sessions NOT RUN here; user Windows Test Demo success is separate field evidence.

## v0.1.7 — host regression and packaging gate (2026-10-11)
- Linux Python 3.13 / Xvfb: all 66 test executions PASS, including inherited v0.1.6 launch/adapter/GUI/language suites and new portable project identity, profile isolation, one-time migration, cloned checkout ioHub rebasing, timestamp/ID filenames and post-exit-only log tests. Experiment subprocess tests use fake upstream/PsychoPy; not hardware validation.
- Native experimental runtime, seven-variant registry, gaze/voice/raw/adapter code, original YAML demo fixtures and both parameter manuals remain unchanged.
- Release packaging/integrity results recorded in terminal release closure below, following clean unpack, manifest and exact direct-parent patch verification.

### v0.1.7 final closure (2026-10-11)
- Clean extraction of parent v0.1.6 + `git diff --binary` direct-parent patch: exact byte + file-mode reconstruction PASS.
- Working release vs freshly unpacked final rootless ZIP: exact byte + file-mode identity PASS.
- `tools/verify_manifest.py`: 117/117 non-manifest payload paths PASS, 118 total files.
- `tools/render_parameter_manual.py --check`: 87/87 PL and EN PASS; language manuals unchanged.
- Fresh-unpack Linux Python 3.13/Xvfb unittest suite: 66/66 PASS; post-test manifest and tree identity PASS.
- Scope freeze: 21 non-storage/core source, original adapter, original demo fixtures and bilingual parameter manuals byte-identical with v0.1.6; 6 development logs append-only PASS.
- Actual Windows Git Bash/Conda Python3.10/PsychoPy/Tobii run: NOT RUN for v0.1.7. Physical validation is an external gate.

## v0.1.8 lazy navigation shell — initial host validation (2026-10-11)
- Linux Python 3.13 / Tk under Xvfb: 71/71 tests PASS, including all 66 inherited tests and five new checks for first-open-only construction, view reuse, unsaved invalid YAML, no commit/save/runner side effects, English/Polish navigation and close delegation.
- A real 1190×880 Tk screenshot shows top navigation above the preserved Experiment form; only Experiment is instantiated at startup (`created_screens == ('experiment',)`).
- Bilingual manuals: 87/87 PL+EN entries PASS, unchanged. No PsychoPy or Tobii hardware runtime tests performed for this UI-only release.
- Final manifest, direct-parent patch reconstruction and fresh archive checks are recorded in release closure below.

### v0.1.8 release closure (2026-10-11)
- Exact v0.1.7 full-ZIP source + generated direct-parent Git binary patch reconstructs the v0.1.8 tree byte-for-byte and file-mode-for-file-mode: PASS (125 total files).
- Six cumulative development logs retain their exact v0.1.7 byte prefixes: 6/6 append-only PASS.
- Core `runner.py`, `runtime.py`, launch adapter bridge, project/profile storage, original YAML support, two manual JSON sources and PL/EN parameter manuals are frozen: 14/14 exact byte PASS.
- Final manifest and clean-archive identity are verified during fresh-ZIP gate; host GUI regressions use fake/fixture demo environment only. No target Windows/real PsychoPy hardware runtime executed in this environment.

## v0.1.9 experiments-directory — host validation and release closure (2026-10-11)
- Exact accepted parent source: v0.1.8 full ZIP. The only production logic delta is the new `projects.EXPERIMENTS_DIR` constant and execution parent path selection in `runtime.prepare_run`. No changes to subprocess supervisor, child adapters, ProjectStore project metadata, profile data, AppShell/navigation, PsychoPy options, or demo output ownership.
- Linux Python 3.13 / Xvfb: 87/87 test executions PASS (71 inherited, 5 focused v0.1.9 test methods plus shared inherited methods invoked by fixture subclassing); includes multiple runs/projects, snapshot files, raw console and final GUI logs, no new legacy `runs/`, status handling and launcher smoke. Tests use fake native runtime, not real PsychoPy hardware.
- PL/EN parameter-manual synchrony: 87/87 entries PASS. Older v0.1.7 project guide is preserved as historical; new paired v0.1.9 guides supersede `runs/` for current behavior.
- Exact v0.1.8 → v0.1.9 direct-parent binary patch byte/file-mode reconstruction, fresh ZIP byte/file-mode comparison, fresh 87-test suite, post-test manifest, frozen source boundaries and six append-only development logs are release gates; final command output is the authority for PASS status.
- Real Windows/Conda/PsychoPy/ioHub/Tobii physical validation: NOT RUN in this environment.

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- Linux Python 3.13/Xvfb: 92/92 unittest PASS, including all 87 inherited tests and five v0.2.0 visual regressions. Screenshot captured from real Tk widgets at 1380×960. Final fresh ZIP/manifest/patch gates documented in the release response.
- Windows, PsychoPy, physical Tobii and monitor DPI scaling: NOT RUN; not implied by host UI validation.

## v0.2.1 — 2026-10-11
- Linux/Python 3.13/Xvfb: inherited test suite PASS; focused tests confirm dashboard laziness, tile routing, PL/EN, unsaved YAML preservation, no new navigation timer and native icon cache/size.
- Source identity, append-only logs, manifest, fresh ZIP and parent-patch reconstruction validated as release gates. Windows/PsychoPy/Tobii physical tests NOT RUN.

## v0.2.4 — Manual/navigation gate (2026-10-11)
- Added Tk test coverage for lazy fifth screen, brand icon, contextual `man` navigation, manual selection/search, language and untouched invalid YAML.
- Real Windows/PsychoPy/Tobii hardware testing not performed locally.

## 2026-10-11 — v0.2.5 validation
- Automated gates: 87/87 English and Polish descriptions present, English discrete options and in-app Manual coverage, source project catalog keys unchanged, and existing runtime/storage tests. See release test results.
- Physical Windows/PsychoPy/Tobii testing remains a separate external gate, not claimed by these host regressions.

## v0.2.6 — RST documentation/manual regression (2026-10-11)
- Targeted local GUI tests: Index default, green option values, RST-only upstream folder including nested pages, absence of demo docs, safe symlink handling, lazy Documentation creation, language switch, deep links back to Index, unsaved YAML preservation: PASS (18/18 combined targeted suite).
- Full inherited test groups, direct-parent patch reconstruction and fresh-unpack verification: recorded on release closure below. Windows/PsychoPy/Tobii actual run: NOT RUN for this GUI-only change.
- Grouped inherited host/Tk regression PASS: GUI 44/44, runner/project 39/39, and core/documentation 23/23 test executions; total 106 test executions across three independent groups. The first parallelized combined run timed out; re-running the launcher-heavy group separately finished 39/39, and the two isolated launcher checks also finished PASS.
- Frozen-scope audit PASS: `app.py`, `runtime.py`, `runner.py`, `launch_child.py`, `projects.py`, profile/YAML code, help JSON catalogs, generated PL/EN manuals and `help_widgets.py` are all byte-identical with exact v0.2.5.
- Release reconstruction PASS: git binary patch replays to 207/207 byte+mode-identical files from exact v0.2.5; fresh ZIP extraction 207/207; manifest 206/206. Windows/PsychoPy/Tobii physical tests remain NOT RUN.

## v0.2.8 — session binding evidence
- Unit/child-process tests must verify unique per-block output roots, exact validator arguments, no newest/mtime selection, `result.json` binding, and fail-closed zero/multiple candidate behavior. Full Windows PsychoPy collection is an external gate.

## v0.2.9 — optional automatic log viewer, host test checkpoint (2026-10-12)
- Parent authority: exact v0.2.8, retaining v0.2.6 visual palette. Changed only GUI log display/control and local preference, plus documentation/tests/version identity; `runner.py`, runtime, project storage, output-ID binding, fixture YAML and Manual remain unchanged.
- Linux Python 3.13/Xvfb: 45 GUI/manual/navigation/language tests PASS; 8 native launcher tests PASS; 21 adapter/portable-project tests PASS; 38 experiments/session-ID tests PASS; 30 remaining core/layout/help/visual tests PASS (142 executions in validated groups).
- New focused tests additionally verify: default ON and persisted OFF, absence of automatic popup and Tk text rendering, manual Show Logs, full 2,300-line archive after preview exceeded 2,000 lines/256 KiB, full clipboard despite bounded preview, toggle OFF closing live viewer, and spool temp creation failure not retried for every line.
- `SpooledTemporaryFile` GUI spool threshold 262,144 B RAM; final `experiment_*.log` created only after finished status. Long logs are streamed in bounded chunks to the project folder. Existing runner post-process console archival unchanged.
- Physical Windows/Python 3.10/PsychoPy/ioHub/Tobii session NOT RUN in this environment. Release patch/fresh-manifest gates recorded separately at packaging closure.

## v0.2.10 — Pre-package regression, Linux Python 3.13/Xvfb
- Group A core/docs/profiles/auto-log: 54/54 PASS.
- Group B GUI/manual/navigation/theme: 44/44 PASS.
- Group C native launch: 8/8 PASS; adapter import/log copy: 4/4 PASS; experiments layout: 16/16 PASS; session measurement binding: 22/22 PASS.
- Total 148 test executions in separate groups. One combined process group exceeded timeout, so it was re-run per test module and all four modules passed. Physical Windows/PsychoPy/Tobii NOT RUN.

## v0.2.11 — Tree contrast regression (2026-10-12)
- Linux Python 3.13/Xvfb, six separately invoked test groups: GUI/manual 52/52 PASS; core/profiles/docs 47/47 PASS; native launch 8/8 PASS; adapters 4/4 PASS; experiments 16/16 PASS; session binding 22/22 PASS = 149/149 PASS.
- One combined subprocess-heavy attempt exceeded timeout; all affected modules subsequently passed when run independently. Physical Windows/PsychoPy/Tobii testing NOT RUN.

## v0.2.12 incremental journal validation (2026-10-12)
- New focused tests cover one archive, interruption marker, 256-KiB newest-wins overflow and diagnostic gap, short no-I/O producer path, and unmodified limits. Legacy tests updated to assert the intentionally changed one-log contract.
- Host regression and fresh-archive validation outcomes are recorded with the release artifact; Windows/PsychoPy/Tobii physical acceptance remains NOT RUN.

## v0.2.13 — validation record (2026-10-12)
Tests: see final release closure in appended validation lines. Required gates: selected-run snapshot fidelity, fail-closed metadata, absent/partial/complete journal states, no stdout/log/data-output access in stage 1, GUI navigation PL/EN, fresh ZIP/manifest and exact v0.2.12 parent patch reconstruction. Windows/PsychoPy physical test not performed locally.
- Host Python 3.13/Xvfb targeted: `test_logs_history_stage1_v0213.py` 8/8 PASS; `test_navigation_shell_v018.py` 5/5 PASS; Manual group 18/18 PASS; visual/smoke/language/demo-docs/autolog groups 32/32 PASS; native launcher 8/8, adapter 4/4, portable project 19/19, experiments directory 16/16, session binding 22/22, incremental journal 5/5 PASS; core/help/parameter/layout/bilingual/project naming 30/30 PASS (project naming 5 included within 18 Manual executions). All test groups executed independently to avoid unrelated aggregate-process timeout.
- Confirmed no production changes to `runner.py`, `runtime.py`, `incremental_log.py`, `app.py`, YAML/profile/storage, Manual, source repositories or `theme.py`.
- Windows physical visual/large-directory performance not executed. See final packaging tool output for manifest, patch reconstruction and fresh-unpack identity.

## v0.2.14 — validation (Linux Python 3.13/Xvfb)
- Focused stage-1/stage-2 log history 20/20 PASS; stage-2 tests exercise strict run-ID filename, symlink rejection, 64-KiB paging, UTF-8, growing `.part`, read-only toggling/clipboard and PL/EN.
- 47/47 Manual/navigation/theme/auto-show, 33/33 core/help/layout/manual sync, 31/31 native/adapter/portable and 43/43 experiment/session/GUI/help PASS, each executed with Xvfb as required (total 174 executions, with inherited duplicates). Manual 87/87 PL/EN sync PASS.
- No physical Windows/PsychoPy/Tobii validation. Final manifest/patch/fresh ZIP identity recorded at package gate.

## v0.2.16 — Scoped UI reversal and panel test (2026-10-12)
- 7/7 targeted Tk/Xvfb tests PASS: unmodified button styles, five original footer actions in one row, exactly three compact icons, all 3 sashes, navigation, localization, minimum window.
- Regression 181 test executions PASS: 38 GUI, 44 Logs/Manual, 25 core/help/layout, 31 native/adapter/project, 43 experiment/session/journal; large combined process group was timeout and was rerun in separate successful modules.
- Package acceptance: direct-parent exact git binary patch reconstruction, fresh ZIP byte+mode identity, SHA-256 MANIFEST and CRC verified in release pack gate.
- Physical Windows, PsychoPy and Tobii not run.

## v0.2.17 — Scoped validation and release gate (2026-10-12)
- New tests cover equal pixel widths in PL/EN without icon/style changes; lazy fourth Manual tab, EN/PL document discovery, read-only bounded renderer, missing/symlink cases, unsaved YAML/navigation and `man` Index deep link.
- Inherited unit suites run under Linux Python 3.13/Xvfb in bounded groups. Exact source freeze, patch reconstruction, archive manifest and fresh-unpack checks documented by final release tooling. Physical Windows/PsychoPy/Tobii not run.
- Actual grouped Linux Python 3.13/Xvfb suite results: 37 + 28 + 28 + 31 + 63 = **187 test executions PASS**. `test_gui_documentation_v0217.py`: 6/6 PASS including EN/PL equal-width Tk widget measurement, four tabs, lazy documentation tree, safe read-only selection and YAML preservation. Prior monolithic suite was not used.
- Final ZIP/manifest/reconstruction will be checked separately after all tests are complete; Windows/PsychoPy/Tobii physical NOT RUN.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
v0.2.18 tests: targeted Home and GUI/navigation/manual regression PASS on Linux/Xvfb. Full/fresh manifest and package tests recorded in release verification.
- Final recorded gates: 59 GUI/navigation/manual tests PASS and 39 Logs/journaling/panels PASS (separate Xvfb groups); native launcher 8/8 PASS; adapter 4/4 PASS. Larger merged process-test invocations exceeded environment timeouts and were NOT counted.
- Fresh v0.2.18: exact-parent binary patch reconstruction 256/256 files byte-exact PASS; Full manifest 255/255 PASS; Commit Ready manifest 162/162 PASS; new Home/navigation test group from fresh Full 19/19 PASS; Commit Ready Tk Home + GUI Documentation smoke PASS.
- Remaining external gate: real Windows/HiDPI display, fixed-size image click targets, and resized-window scrollbars. No physical Tobii/PsychoPy measurement test performed for this UI-only update.

## v0.2.19 — Default window size (2026-10-12)
v0.2.19: targeted GUI geometry and regression tests plus manifest/full/commit-ready package audits performed in release closure; physical Windows NOT RUN.

## v0.2.20 — Environment icons (2026-10-12)
v0.2.20: icon-specific GUI checks and fresh-archive manifest audits are release gates; no Windows/PsychoPy physical test.
Validation closure: new/legacy environment+panels+docs+default-window 16 PASS; dashboard 10 PASS; navigation 5 PASS; Logs viewer 12 PASS (43 passed in separate bounded invocations). Broad combined and upstream-manual module invocation timed out and are not counted. Full+Commit Ready fresh-unpack identity/manifest/CRC audits PASS; Windows physical NOT RUN.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
v0.2.22: targeted GUI Settings + dashboard behavior and persistence tests required; manifest/ZIP/frozen-scope checks for both Full and Commit Ready; Windows real hardware NOT RUN.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: checks include exact 546×365 optimized assets, four screen commands, source freeze, manifest, full and commit-ready fresh ZIPs; Windows external.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: focused pixel/color/cache navigation, no-Pillow, orange accent and scope-frozen audits plus fresh Full/Commit Ready unpack/manifest gates. Windows/Tobii/PsychoPy physical not run.
- v0.2.24 Linux Python 3.13/Xvfb (1920×1200): 30/30 icon/theme/gui-settings/navigation/panels/default-window regressions PASS; 59/59 Logs, incremental journal, Manual, gui docs, locale and popover PASS; 31/31 core/layout/help/Home/dashboard regressions PASS. Dedicated mask/hex/cache/ink tests 6/6 included in first group. Source freeze: 267 existing parent files byte-identical; only original runtime `theme.py`, `__init__.py` and VERSION changed, all old image assets 1:1. Inherited historic v0.2.0/v0.2.1 icon-count assertion expects 52 PNGs; the exact v0.2.23 parent already has 56 PNGs (with GUI Settings icons), so this remains obsolete and is intentionally not patched in the icon-only iteration. A mistaken test selector caused one non-product unittest loader error, corrected by running the three existing named tests. Windows/PsychoPy/Tobii physical not run.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
v0.2.25: focused pixel/cache/state/nav/tab checks and existing GUI regressions; exact v0.2.24 parent source/asset freeze and both Full/Commit Ready fresh-unpack manifest gates. Windows/PsychoPy/Tobii physical NOT RUN.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.

### v0.2.26 supplemental host evidence
- New theme palette tests: 4/4 PASS under Linux Python 3.13/Xvfb.
- Earlier v0.2.24/v0.2.25 icon tests: 9/9 PASS after superseding exact default color assertion.
- GUI Settings v0.2.22: 4/4 PASS at 1920×1200; default Xvfb 1280×1024 cannot satisfy its explicit 1429×1097 assertion.
- Session binding regression: 22/22 PASS when executed as `python -m unittest tests.test_session_binding_v028` (the module's relative import requires package execution).
- Additional targeted GUI, Manual, Logs, Home, locale and inherited experiment tests PASS in separate groups. The old `test_visual_theme_v020` 52-icon count assertion is inherited obsolete since 56 assets existed before this iteration; no runtime icon files were added in v0.2.26.
- Full target Windows/HiDPI and physical PsychoPy/Tobii not executed here.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: targeted Experiment icon/header cases plus v0.2.25/v0.2.26 icon/nav/GUI Settings and inherited Manual/Logs/Home tests PASS under Linux Python/Xvfb 1920x1200. Final fresh ZIP/manifest gates documented in delivery; Windows/hardware NOT RUN.

## v0.2.34 — Polish localization (2026-10-13)

Scope: translate English v0.2.33 GUI Settings help and documentation, expose Polish option explanations in Experiment Manual. Stable keys/values preserved; runtime remains unchanged. Test gate: focused Tk/interpreter checks and regenerated PL/EN manuals, full ZIP manifest.

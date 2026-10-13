# WORK SESSION LOG (append-only)

## 2026-10-10 — S0001: analiza i planning checkpoint
**Cel:** zaplanowanie lekkiego Windows/Linux GUI do zarządzania tobii-pytracker i nowymi eksperymentami.

**Zbadane źródła:** obydwa archiwa v1.17.0 (repo 104 files i logs/helpers), README/README_TESTING, 9 YAML, demo runners, `native_preflight.py`, `demo_runtime_adapters.py`, Docker Compose, historyczne audit/decision/log policy, publiczne docs upstream (informacyjnie).

**Wyniki:** 5 demo, 7 publicznych wariantów startowych (count EN/PL i double time series jako jeden), trzy typy dataset, oddzielna ścieżka native/Docker, CWD jest wymagany, różne runner commands, output validity nie równa się exit code.

**Decyzje wstępne:** samodzielny control plane, Tkinter/ttk jako domyślna technologia do potwierdzenia, subprocess launcher, osobny projekt JSON i generated YAML, append-only technical logs. Nie modyfikowano żadnego pliku w archiwach wejściowych.

**Wykonane:** przygotowano dokumenty i checklisty planu, nie kod GUI. **Testy:** hash dostarczonego REPO ZIP zgodny z release report; konfiguracje dataset/path zostały przeczytane/zinwentaryzowane; GUI runtime, native collection i hardware: NOT RUN.

**Blokery:** brak dostarczonego exact upstream checkout SHA oraz realnego Windows/Linux hardware. 

**Dokładny next action:** pozyskać/testować upstream checkout, wypisać `tobii-pytracker --help` i runtime import/CLI, sprawdzić Tkinter/ttk na obu OS, następnie założyć kod v0.1.0 i zaimplementować stub/fake-process launcher z RunSpec.

## 2026-10-10 — S0002: upstream + focused scope
**Wejście:** nowy link https://github.com/sbobek/tobii-pytracker, instrukcja pominięcia projektowania nowych eksperymentów i uruchamiania dem z kontrolą konfiguracji, ścieżek i mysz/no mouse.
**Sprawdzono:** live RAW `main.py`, `custom_config.py`, `eyetracker.py`, `gui.py`, `pyproject.toml`, 3 publiczne yaml upstream, publiczną konfigurację/CLI; fizycznie obecne pliki repo v1.17 i wszystkie `run_native*.sh`, `run_experiment.py`, 9 yaml.
**Wyniki:** Python 3.10 cli, 8 flags, trzy tryby gaze (off/mouse/tobii), validation/folder cwd contract; 7 wariantów w 5 demos; dla UX/Text/Image wrappery ignorują przyszłe GUI voice/raw/off bo hardcoded. Time series 2 × 9, dwa validators.
**Rozstrzygnięcia:** M1 supersedes new experiment wizard; GUI-only child bridge preserves upstream/demo authority, no bash dependency; immutable profiles, no silent flag ignored; collection vs gaze statuses separate.
**Testy:** lokalny parsing 9 native YAML oraz audyt source/static PASS; upstream exact SHA, native PsychoPy/Tobii, GUI/Windows/Linux: NOT_RUN; nie wolno ogłaszać ukończenia M1.
**Dokładny następny krok:** pobrać dwie autentyczne referencje Git SHA (upstream i demo) na maszynie z siecią i Windows/Linux, uruchomić provenance preflight, następnie dodać registry 7 wariantów + test fake subprocess i Tk shell jako v0.1.0.

## 2026-10-10 — S0003: v0.1.0 interface build
**Goal:** implement M1 UI with YAML and 7 demo variants, retaining all earlier plans/logs. **Input:** exact user-provided demo v1.17.0 native configs + approved v0.0.1 plan; upstream SHA missing. **Implementation:** Tk side demo registry, layout, gaze choice, repository paths; 8 config loader, structured fields + YAML editor, instructions, independent machine/PV states, ruamel round-trip, app-private profile and checksum, read-only preflight/probe, launch preview. **Problem→fix:** Linux ruamel scalar integer subclass caused false display_number BLOCK; changed validator to isinstance(int) excluding bool. Another test exposed potential cross-writing when switching time-series blocks; added explicit active_block_key before saving previous tab. **Validation:** 13 tests core + GUI/Xvfb PASS; all eight baseline YAML fixtures read; screenshot captured; Windows and real hardware NOT RUN. **Known limits:** start disabled, full ioHub YAML editing later, atomic per file not whole profile, YAML style normalization possible. **Next:** exact upstream SHA/provenance, Windows physical GUI and fake process harness, then full bridge.

## 2026-10-11 — S0004: repository layout correction
**Input:** request to change GUI installation to original prescribed clone workflow and house independently versioned GUI as another folder inside tobii-pytracker. **Evidence:** supplied demo v1.17.0 README_TESTING, public mszac/tobii-pytracker-demo README and raw tools/run-demo.sh, original native run_native.sh; public upstream sbobek/tobii-pytracker. **Fault:** v0.1.0 path instructions assumed three sibling directories and required manual path selection; mouse ioHub default was empty. **Design choice:** one engine parent with two nested Git-independent child projects, path detection tied to GUI source path, non-destructive fail-closed layout gate, profile data remaining outside Git tree. **Implementation:** layout module, CLI preflight, GUI autodetect & validation, gaze defaults, corrected preview and docs, tests; original engine/demo never edited. **Scope restriction:** GUI remains config-only; original bash runner doesn't apply GUI profiles. **Tests:** record exact outcome in VALIDATION_LOG at release. **Next:** Windows user checks with exact Git revisions/Python 3.10 and native child bridge planning.

## 2026-10-11 — S0005: English readme, upstream parameter audit, M1 help bubbles
**Input:** request for a new English standalone run README and two-level explanations next to GUI parameters (blue circular click `i`), with no manual link. **Evidence:** live upstream project README config/CLI; upstream RAW general/mouse/Tobii YAML; eight supplied v1.17.0 demo configurations; exact parent v0.1.1 ZIP. **Working hypothesis:** source-only ioHub fields must be documented but not mislabeled editable. **Implementation:** 87-key JSON with short/long Polish descriptions and status/source, deterministic Markdown generator, small stdlib-only Tk Canvas/Toplevel help widget, icons on all currently exposed parameter groups, English setup README. **Encountered issue:** inherited GUI tests require an active X display; bare host has DISPLAY=:0 but no actual server, so run GUI tests under `xvfb-run -a` rather than treat this as application failure. **Tests:** full 23/23 under Xvfb; eight config fixture leaf keys covered; real Tk `i` click/popover/toggle/switch tested; manual sync PASS and preview screenshot. **Remaining risks:** no network git clone and no Windows high-DPI/hardware tests. **Next:** user Windows smoke and Git SHA recording, then fake-child process bridge work to actually launch demos using profiles. See final release validation log and ADR-0013.

## Session 2026-10-11 — v0.1.3 language preference
**Input:** preserve Polish GUI/docs, add English UI selection and bilingual short tooltips, defer English long manual, forbid other functional changes.
**Completed:** inspected v0.1.2; added English UI strings and 87 English popup overlays; added two Tk selectors and isolated settings persistence; kept Polish manual untouched; validated live Tk PL/EN screens and 30 test cases.
**Risk mitigations:** no YAML key translation, no profile migration, no hidden change to launch or adapter logic; invalid edited YAML stops language switch without losing input.
**Next:** fresh ZIP and patch reproduction + manifest, then physical Windows tests in pytracker-env.

## Session 2026-10-11 — S0007: language parity, semantic precision, read-only functionality
**Input:** update remaining documentation for equivalent coverage of current PL/EN functionality and clarify ambiguous parameters without extending the runtime. **Reviewed:** exact parent ZIP/87-entry help catalogs/manual generator/current GUI, demo registry (7 variants/8 configs), public upstream readme/config and demo landing page. **Work:** added 87 English extended descriptions, clarified selected PL/EN definitions, paired manuals/installation/user guides/indexes, small informational label update, parity tests and ADR. **Finding:** v0.1.3 English overlay had only short help and existing readme/version references were historical. **Regression:** 35/35 Xvfb; bilingual manual sync 87/87. **Next:** verify bytes/mode versus parent, fresh ZIP and manifest; physical Windows test remains external.

## v0.1.5 work session — 2026-10-11
Analyzed exact locally uploaded v0.1.4 ZIP/demo v1.17.0 and public upstream CLI/CustomConfig/dataset interfaces. Implemented immutable run manifest/YAML, native per-block child bridge, background supervisor, logs/cancel UI, tests for all seven variants, flag transfer and failure/stop sequence. Updated PL/EN launch manuals/readmes and historical docs supersession. Next on real Windows: clone repos, capture HEAD, install selected Python 3.10, test Test Demo MouseGaze + samples/answers and failure/stop, then UX/Text/Image, Time-Series, voice/raw and Tobii separately.

## v0.1.6 session — 2026-10-11
**Input:** user copied two Text Search EN failures (same adapter `ModuleNotFoundError`) and successful Test Demo MouseGaze collection validator log, requested fix and full Experiment log copy button; user explicitly set aside unrelated fullscreen/focus problem. **Reviewed:** exact v0.1.5 ZIP `launch_child.py`, `runner.py`, `runtime.py`, `app.py`, i18n and tests, plus original demo adapter source. **Work:** explicit file-spec adapter loader; preflight for missing adapter; diagnostic adapter log; PL/EN copy button; log view retention across reopen; focused docs and four new regression tests. **Why:** avoid generic `tools` namespace collisions without editing outside Git repositories. **Local results:** 47 host Xvfb tests PASS plus 5 actual-adapter-source/fake-dependency launches PASS. **Open risks:** no physical Windows launch done in this environment; hardware/collection not certified. **Next:** release-manifest/parent patch/fresh tests, then user's Windows Text Search EN and other special variants with log copy, collect exact Git HEAD and full log for any remaining failure.

## v0.1.7 portable-project implementation — 2026-10-11
1. Audited exact v0.1.6 runtime, ProfileStore, GUI event queue and per-line console.log writes. Chose `tobii-pytracker/projects/` alongside independent GUI/demo checkouts to keep projects across GUI replacement.
2. Implemented project metadata and selection/creation, default per-demo project, per-project profiles and optional legacy profile copy; preserved all seven variants and existing YAML editor.
3. Implemented per-run 5-character case-sensitive alphanumeric ID with collision-safe mkdir, copied current YAML/ioHub/GUI launch settings, relative standard ioHub reference, history metadata and output-folder separation.
4. Replaced per-line permanent log writes with bounded memory/temporary spool, post-run raw console log and post-final complete GUI log. Protected log I/O failures, close/stop finalization and added test cases for resource timing/portability/log identity.
5. Appended PL/EN documentation, current README notice and ADR-0018; next gate: fresh-unpack full regression and physical Windows project-copy smoke.

## v0.1.8 lightweight screen architecture — 2026-10-11
1. Audited the exact v0.1.7 full ZIP, especially `app.py` Tk ownership, popover, unsaved YAML, ExperimentRunner, existing tests and docs. Selected an outer shell so existing experiment logic stays an independent persistent class with minimal integration edits.
2. Implemented `AppShell` with four top navigation entries, Tk project-label observer, language refresh and delegated close. Kept the existing editor instance alive and added lazily created independent placeholder frames for Logs/Diagnostics/Statistics, with no data readers or timers.
3. Verified that returning from other screens preserves live widget identity and invalid YAML text without triggering `_commit_tab`, profile save, process control or active-tab reconstruction. Updated PL/EN guide, ADR, status history and dedicated tests.
4. Full inherited and new Linux/Xvfb regression: 71/71 PASS, parameter manuals synchronized, real GUI screenshot captured. Next: package/manifest/direct-parent patch/fresh-unpack closure and Windows GUI screen-switch smoke.

## v0.1.9 — project versus experiment execution storage (2026-10-11)
1. Opened the exact accepted v0.1.8 ZIP; traced ProjectStore, ProfileStore, prepare_run, ExperimentRunner, full Experiment log handling and previous 71 tests. All per-run output already follows the manifest's parent directory; no change needed in process logging or GUI.
2. Defined a single new execution parent `EXPERIMENTS_DIR = 'experiments'`, retained project-global files and the original per-execution five-character ID and second-precision filenames. No `runs/` alias, migration or deletion.
3. Updated existing path assertions and added focused tests for project separation, repeated executions, post-run console log/result and post-final full GUI log. Updated project boundary docs in both languages, ADR-0020 and append-only release logs.
4. **Next exact validation:** complete full host suite under Xvfb, manifest and fresh unpack identity, byte/mode exact reconstruction from v0.1.8. Then Windows user smoke (create project, launch Test Demo, verify `projects/<name>/experiments/` and measurement CSV unchanged).

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- Started from exact v0.1.9 ZIP; inventoried ttk and classic Tk controls, layout owner and existing smoke tests. Applied static native theme, packaged PNG vector-like icons, list/text/popover colors, and kept existing language/tooltips and run controller. Confirmed actual Tk screenshot and existing test suite.
- Risk handling: did not introduce third-party UI runtime, custom process, timer, filesystem watcher, extra settings or alternative render owner. Next gate: Windows visual smoke + existing Test Demo regression, then accept/revise appearance separately.

## v0.2.1 visual polish session — 2026-10-11
- Read exact v0.2.0 ZIP and inspected selected-tab screenshot. Implemented clickable original brand mark/name, lazy four-tile chooser, palette/icon and selected-tab inset refinements.
- Verified tests and Tk preview of dashboard and Experiment; no runtime-source changes. Final artifact and integrity gates documented in VALIDATION_LOG.

## 2026-10-11 — v0.2.4 manual/brand
- Inspected v0.2.3 code and existing localized parameter catalogs. Added a small white-roundel brand asset and removed the historic diamond; added one fifth screen built only on demand and linked it from existing popovers.
- Kept the current experiment view, config and subprocess code unchanged. Next: physical Windows smoke and manual navigation test with both languages.

## 2026-10-11 — v0.2.5 session
- Read exact v0.2.4 release and existing catalogs/UI/manual renderer. Reviewed available upstream values and local GUI selectors.
- Reworded user-facing project terminology, added English option-level descriptions and propagated them into the in-app Manual.
- Confirmed Polish Manual is unchanged; executed targeted and regression tests. No runtime integration or storage work.

## 2026-10-11 — v0.2.6 session
- Inspected exact v0.2.5 Manual, 87-entry PL/EN help registry, source-root selection, and frozen launcher.
- Built Index/Documentation tabs in ManualScreen; added a small read-only RST file browser and exact `man` deep-link-to-Index contract. Implemented focused tests for nested upstream docs, exclusion of demo docs, green option names, no YAML commit, language switch and lazy loading.
- Next gates: grouped inherited host/Tk tests, exact parent reconstruction, fresh ZIP manifest and Windows upstream docs smoke.
- Completed three bounded regression groups (44 GUI, 39 runner/storage, 23 core). Checked frozen production scope and all six append-only log prefixes against v0.2.5. Built and reconstructed a binary patch from the exact direct-parent ZIP and verified final full ZIP fresh identity + manifest.

## v0.2.8 — measurement provenance checkpoint
- Scoped change to unique session-to-run-ID mapping plus targeted regression tests and docs. No UI color/layout change and no log-buffer implementation.

## v0.2.9 — execution checkpoint (2026-10-12)
Implemented only optional experiment-log automatic display and bounded preview. Default ON, app-private persistence, manual Show Logs preserved. GUI per-run spool has 256 KiB RAM threshold and streams the full archive after `[FINAL]`; recent display tail is bounded. Existing native runner spooling and project log naming remain. Dedicated fake-GUI tests verify opt-out, clipboard, persistence and lengthy transcript. Host/Windows validation status is recorded in VALIDATION_LOG.md.

## v0.2.10 — Implementation session
- Inspected exact v0.2.9 archive, existing Manual/UpstreamRstBrowser/shell, and real demo v1.17.0 Markdown layout. Established two-level grouped tree with optional per-project matching guide.
- Implemented route removal, native ttk tree/browser, bounded Markdown/RST formatting, lazy file opening and path safety checks, plus targeted regression tests. No upstream files were modified.
- Tests and packaging gates are recorded in VALIDATION_LOG; Windows runtime remains a user-machine gate.

## v0.2.11 — contrast repair
- Reproduced the style contract mismatch from the user screenshot and upstream code. Added an explicit scoped style for the Demo Project Documentation tree, including selected-state colors; no document discovery/render changes.
- Grouped tests PASS; build and manifest validation recorded in the release checkpoint.

## 2026-10-12 — single-journal iteration
Inspected exact v0.2.11 runner/UI log paths, added independent bounded append-only journal, redirected runner output/statuses, removed post-run duplicate GUI archive, adapted regression tests, wrote ADR-0030 and bilingual documentation. No dataset, session-binding or visual changes.

## 2026-10-12 — Logs stage 1 implementation
Inspected exact v0.2.12 source and `prepare_run`/`result.json` metadata contracts. Designed pure on-demand history model and independent lazy Logs UI with project selector, run chooser and compact six-card configuration report; limited reads to immutable GUI-owned snapshots. Added per-screen information colors and explicit stage 2 disabled log-content control. Next: grouped regressions, patch/manifest reconstruction, fresh-unpack tests, Windows UX acceptance.

## 2026-10-12 — v0.2.14 Logs stage 2
Inspected exact v0.2.13 GUI, history index and v0.2.12 journal writer; implemented native bounded read-only console by selected run, user-triggered page/Latest/manual Refresh, horizontal and vertical scroll and page clipboard. Scoped font increase and lighter selection to Logs, leaving global theme unchanged. Added exact-identity journal status and 11 tests. Separate Xvfb groups passed; next package/test exact-parent ZIP and verify Windows visual sizing and busy-disk behavior.

## 2026-10-12 — v0.2.16 iteration
- Recovered exact user-supplied v0.2.14 archive; manually compared the v0.2.15 app/logs UI delta and transplanted only native sash controls.
- Kept original v0.2.14 environment row buttons and single-row editor footer; installed 3 cached 20px images from bundled PNGs for missing actions.
- Passed targeted 7 and inherited Tk/native/project/session/log suites in bounded groups; documented bilingual scope and ADR-0034; package gates pending finalization.

## 2026-10-12 — v0.2.17
- Started from exact v0.2.16 Documentation Sync ZIP, not v0.2.15. Inspected classic Environment grid and Manual tab providers.
- Implemented only `sticky=ew` on the four Environment actions plus lazy own-project GUI Documentation tab, reusing existing document renderer. Updated matching current guides EN/PL, ADR-0035 and targeted tests. No other user-facing changes.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
2026-10-12 v0.2.18: checked exact parent and four source PNGs; measured 546×365 startup tiles; generated static PNGs; implemented fixed buttons and event-driven overflow; verified Tk geometry and click commands. No other runtime modules touched.

## v0.2.19 — Default window size (2026-10-12)
2026-10-12: measured user screenshot 1459×1165 PNG and window client region about 1429×1097; replaced only startup geometry caps; retained 90px screen margin and all UI behavior.

## v0.2.20 — Environment icons (2026-10-12)
2026-10-12: inspected user screenshot and packaged icon sizes. Enlarged precisely two Environment button images, preserved pre-existing theme and app behavior.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
2026-10-12: reconciled prior GUI Settings draft, implemented window-size preset persistence, and preserved single source of truth for repository paths; rebuilt Full and Commit Ready. No other GUI modifications.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: reprocessed 4 supplied colored images as optimized fixed Home tile assets only; preserved existing screen code and application modules.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: verified parent icon variants, introduced light-burgundy hex parameter with cached alpha-mask image generation, preserved original icons/ink and all other runtime. Release tests and archive checks are recorded in validation report.
- v0.2.24 scoped verification: 30 + 59 + 31 passing test executions with separate bounded Xvfb runs; checked frozen dashboard/brand/original icon bytes. Existing old test requiring 52 icon PNGs remains superseded by pre-existing 56 assets.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
v0.2.25: audited v0.2.24 active-vs-inactive tint regression; switched selected icons to packaged orange, darkened idle tint; maintained no-Pillow cached rendering and untouched orange theme.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: user declined title bar API, so modified no Windows title code or setting. Reused optional icon tint argument for Experiment idle icons, kept active orange, changed heading to static text, adjusted obsolete local-color assertion. Full + Commit Ready archives scheduled.


### v0.2.33 — English help wording review
- Audited existing English GUI Settings tooltip keys against visible controls and the local manual target markers; corrected ambiguous palette `window` deep-link marker.
- Replaced generic color role explanations with role-specific short and extended descriptions; clarified read-only settings, save/restart semantics and GUI-vs-experiment documentation.
- Checked 87 experiment parameter help records for English field coverage; no experiment runtime, YAML, launch or Polish translation changes.
- Added a deterministic English help consistency test.

## v0.2.34 — Polish localization (2026-10-13)

Scope: translate English v0.2.33 GUI Settings help and documentation, expose Polish option explanations in Experiment Manual. Stable keys/values preserved; runtime remains unchanged. Test gate: focused Tk/interpreter checks and regenerated PL/EN manuals, full ZIP manifest.

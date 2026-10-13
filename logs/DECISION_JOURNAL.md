# Technical decision and debugging journal (append-only)

## 2026-10-10 — J-0001: granica runtime GUI
**Obserwacje:** demonstracje wymagają Python 3.10/PsychoPy/ioHub; upstream to właściciel trial loop, adaptery demo już istnieją. **Warianty:** integracja in-process; subprocess native; web front-end. **Propozycja:** oddzielny GUI control plane + child process. **Motywacja:** footprint, niezależność GUI od awarii engine. **Dowód:** repo README, wrappery, historyczne audyty. **Niepewność:** OS process lifecycle. **Next:** parity test.

## 2026-10-10 — J-0002: lekki toolkit
**Obserwacje:** wymagane Windows/Linux i mały narzut. **Alternatywy:** Tkinter/ttk, Qt, Electron. **Propozycja:** Tkinter/ttk w pierwszym MVP, separate runtime interpreter. **Motywacja:** bez Chromium i dodatkowych usług. **Niepewność:** styling, High DPI, Linux Tcl/Tk. **Next:** prototyp na obu OS.

## 2026-10-10 — J-0003: CWD i komunikacja
**Obserwacje:** relative config dataset/output paths rozwiązywane względem cwd; Bash wrappers wymagają środowiska shell; demo-specific adapters istnieją. **Propozycja:** CWD obowiązkowy; `Popen(argv,shell=False)` + per-demo registry z referencyjnymi testami. **Ryzyko:** różnice w kolejności walidacji i przerwanych blokach. **Next:** mapowanie exact commands.

## 2026-10-10 — J-0004: tworzenie eksperymentów
**Obserwacje:** upstream wspiera image/text/time_series config, ale zaawansowane eksperymenty wymagają nowych adapterów. **Propozycja:** kreator 3 modalności i ustawień dokumentowanych, sidecar metadata projektu oraz generated YAML. **Motywacja:** brak fałszywych funkcji GUI. **Ryzyko:** schema drift i unknown fields. **Next:** upstream SHA + 3 integration runs.

## 2026-10-10 — J-0005: kryteria sukcesu
**Obserwacje:** upstream może złapać wyjątek i nie przerwać programu, output walidują osobne skrypty; gaze coverage niezależne od recorded answers. **Propozycja:** oddzielić process, collection i gaze quality statuses. **Motywacja:** nie ogłaszać sukcesu przy utracie danych. **Next:** test exit 0 + missing CSV.

## 2026-10-10 — J-0006: prowadzenie historii
**Obserwacje:** wcześniejszy projekt przechowuje osobne krótkie decision/debug i interruption-safe work journals. **Propozycja:** dzienniki append-only, exact next action, full ZIP/patch/manifest per iteracja. **Next:** aktualizować przy każdej implementacji i teście, nie tworzyć fikcyjnych raportów PASS.

## 2026-10-10 — J-0007: M1 bez tworzenia eksperymentów
**Wymaganie użytkownika:** na początku tylko aktualne dema, wybór jednego, config, ścieżki i mysz/no mouse. **Decyzja:** M1 kontrola istniejących funkcji, przyszły kreator dopiero po stabilnym M1. **Dlaczego:** wyeliminowanie równoległego developmentu eksperymentów i GUI. **Zależność:** dokument nadrzędny w docs/M1_SCOPE_AND_ACCEPTANCE.md. **Status:** accepted scope.

## 2026-10-10 — J-0008: trzy stany gaze
**Fakty:** upstream main CLI `--enable_eyetracker` i osobne mouse/tobii configs, no-gaze istnieje; MouseGaze pracuje przez przytrzymany przycisk. **Alternatywy:** boolean UseMouse vs NO_GAZE/MOUSEGAZE/TOBII. **Decyzja:** jawny enum 3-mode, no mouse to nie to samo co Tobii. **Motywacja:** użytkownik może chcieć przetestować zachowanie bez tracker i jednocześnie obsługiwać odpowiedzi myszą. **Testy:** prawdziwa macierz na Windows/Linux/Tobii; NOT_RUN.

## 2026-10-10 — J-0009: adaptery hardcoded
**Dowód:** 3 skrypty `run_experiment.py` z demo v1.17 mają literalnie `enable_eyetracker=True`, `enable_voice=False`, `raw_data=False`. **Ryzyko:** UI pokazuje toggle, ale aplikacja ignoruje go. **Alternatywy:** patch repo demo; child bridge UI; skopiować engine (zakazane). **Wybór:** cienki osobny child bridge importujący istniejące adaptery + oryginalny main, do walidacji. **Gate:** all variants modes and label integrity.

## 2026-10-10 — J-0010: profile immutable i ścieżki
**Dowód:** CustomConfig zachowuje względny dataset path, upstream output joins timestamp, demo run_native zmienia cwd na demo_root; zawiera dodatkowe `font_height`, `wrap_fraction`. **Wybór:** immutable base + lossless profile YAML + cwd=demo_root + atomic snapshot. **Dlaczego:** nie nadpisać upstream/demo i nie zgubić user-specific unknown YAML. **Ryzyko:** zachowanie komentarzy/parser; testy round-trip potrzebne.

## 2026-10-10 — J-0011: odpowiedź ≠ gaze success
**Dowód:** upstream loguje niektóre wyjątki bez failed exit; obecne kolektory sprawdzają nagrania gaze. **Wybór:** PROCESS/COLLECTION/GAZE oddzielne; w NO_GAZE własna walidacja behavioral-only; nie interpretować gaze missing jako błąd funkcji no-gaze. **Next:** fixture tests for no-gaze and stale output.

## 2026-10-10 — J-0012: UI implemented before launcher
**Trigger:** user requested working interface based on approved M1 with YAML and all seven variants. **Alternatives:** design mock only, reuse wrappers unchanged, real editor with no launch. **Choice:** source-grounded Tk editor with explicit offline-only run preview; implementation combines phase A UI and bounded part of B. **Why:** prevents hardcoded wrapper flags from appearing operational. **Evidence:** 8 native configs, unit/Tk tests. **Next:** exact Python 3.10/upstream binding and child process simulator, then real bridge.

## 2026-10-10 — J-0013: safe YAML and profile writes
**Observation:** PyYAML dump drops comments and unknown formatting; raw in-source edits are unacceptable. **Choice:** ruamel round-trip documents, immutable originals, app-private per-demo profile containing all blocks and hashes, atomic individual-file writes/backups. **Limitation:** scalar formatting/whitespace can normalize; multi-file profile update isn't a single fs transaction, integrity checks detect incomplete save. **Next:** runtime-owned immutable session staging and finer transaction commit protocol.

## 2026-10-10 — J-0014: first static validator boundaries
**Observation:** a syntactically valid YAML may point to missing dataset or wrong CSV columns. **Choice:** local read-only checks for modality, dimensions, paths, headers, output parent, and type checks; WARN for absent hardware verification. **Risk:** upstream schema/behavior unverified, image class counting and dataframe conditions incomplete. **Next:** compare validator against exact upstream CustomConfig, test all 7 variants with real assets.

## 2026-10-11 — J-0015: correct nested repository ownership and eliminate wrong-CWD assumptions
**Trigger:** Windows user observed contradictory clone/setup instructions: old GUI suggested sibling repo, but original demo README_TESTING and run_native.sh enforce `tobii-pytracker/tobii-pytracker-demo`. **Alternatives:** patch original scripts; keep three external siblings with manual paths; nest demo and GUI as two independent subtrees. **Choice:** independent nested trees, no upstream patches, no Git submodule requirement. **Motivation:** original scripts remain usable, clean Git independence and future cloneable GUI. **Implementation:** canonical path resolver using GUI source location, strict layout gate, UI autodetect/repair, tests. **Remaining limitation:** actual demo launch not integrated into GUI; exact Windows Git SHA and runtime not tested. **Next:** physical Git Bash setup and process bridge tests.

## 2026-10-11 — J-0016: validation before launch claims
**Observation:** v0.1.0 dry-run displayed `cwd=demo_root` but did not distinguish upstream commands; it had no default ioHub path. **Options:** auto-execute the unmodified demo wrapper immediately; expose a manual verified command only; implement adapter bridge in same release. **Decision:** show original runner explicitly as manual only, with warning that it ignores saved GUI profiles and dynamic gaze flags; source default ioHub paths from upstream and add a no-Tk `--check-layout` command. **Reason:** avoid false sense that GUI settings control actual collection. **Next:** fake-process Windows/Linux bridge then exact adapter parity.

## 2026-10-11 — J-0017: parameter manual as verified reference, not an implicit control surface
**Trigger:** user wants concise in-GUI explanations for each setting and full descriptions available as the basis of a future manual. **Observation:** upstream uses separate main YAML and ioHub configs; many original ioHub fields are not yet editable in v0.1.x. **Alternatives:** duplicate text in labels and README; add manual links now; maintain a single machine-readable catalog. **Decision:** JSON catalog + deterministic Markdown, explicit status `gui` / `yaml-only` / `iohub-only` / `reference` / `future`; `i` popovers show only the one-sentence text; no manual link. **Why:** avoids silent feature overclaim and future description drift. **Evidence:** upstream README plus RAW config files and supplied v1.17 demo configs, 23 targeted/inherited tests under Linux Xvfb. **Risk:** live upstream `main` could change; exact SHA still needed. **Next:** real Windows review of tooltip placement/readability and pin upstream/demo SHA.

## 2026-10-11 — J-0018: native Tk popup instead of heavy tooltip dependencies
**Trigger:** icons must be small, round, blue and clickable; app remains computationally lightweight. **Choice:** 19×19 Canvas vector glyph + single ephemeral Tk Toplevel with short description. **Rejected:** image/font assets, WebView/browser, hover-only tooltip, full manual panel, modal messagebox. **Implementation:** bind click/Enter/Space; toggle/X/Escape/outside-click; close on form rerender. **Validation:** live Tk/Xvfb smoke and image capture; manual link deliberately not implemented. **Limit:** Windows high-DPI, window manager focus and accessible screen reader behavior require real-device checks.

## 2026-10-11 — v0.1.3 language boundary
**Decision:** accept two UI languages (default PL, optional EN) and separate tooltip language (follows GUI by default, user override persists). Long manual remains exactly Polish.
**Motivation:** preserve familiar Polish GUI/manual, allow English usage without forks and permit English GUI with Polish explanations.
**Rejected:** translating YAML schema/profile keys, introducing a web translator, generating all English long manual files or a manual link at this stage.
**Risk:** bad YAML must not be discarded on UI switch; stop switch when invalid. Popup help overlay must provide 87/87 English short entries.

## 2026-10-11 — J-0019: two complete language references, one set of stable configuration keys
**Observation:** English popovers existed but long descriptions and current English user instructions were incomplete. **Decision:** maintain one shared key/status/source registry, long descriptions in both languages, two deterministically generated manuals and paired current guides; do not translate schema identifiers or past ADRs. **Reason:** eliminate missing English reference coverage while preserving compatibility and provenance. **Controls:** bilingual sync tests and explicit status glossary; no runtime bridge or manual hyperlinks. **Risk:** unpinned newer upstream commits and device-specific interpretation require revalidation. **Next:** Windows smoke + Git SHA provenance, then planned native child bridge.

## Decision checkpoint v0.1.5 — 2026-10-11
Observation: default demo wrappers hardcode gaze and cannot run saved GUI profiles. Decision: native child adapter bridge using `main.main` and existing `tools.demo_runtime_adapters`; no repository patching. Original time-series process boundary and serial order retained. Dynamic flags are now passed, but physical device success is not inferred. Distinguish process success from validated collected data and explicitly skip validators that assume unchanged full-length stimulus sets. See ADR-0016.

## Decision J-0020 — exact adapter file import versus generic `tools` (2026-10-11)
**Observation/evidence:** User Windows log: Test Demo collected and validated three trials but Text Search EN failed before PsychoPy with `ModuleNotFoundError: No module named 'tools.demo_runtime_adapters'`. The child invoked `-m pytracker_gui.launch_child` with correct paths and selected Python 3.10; the `tools` import remained ambiguous.
**Decision:** Load the named file from the manifest-authoritative demo checkout using an importlib file spec, and reject a missing adapter before spawning PsychoPy for UX/Text/Image. **Motivation:** avoid competing installed `tools` packages, reliance on package `__init__.py`, or modifying the demo Git checkout. **User requested:** add complete log copy button, retaining log text across reopening. **Non-goals:** hotkey/pause, tweaking Python requests dependencies, data collection redesign, PsychoPy/runtime changes. **Residual risks:** user's checkout may differ from v1.17.0; real Windows PsychoPy/hardware test needed. See ADR-0017.

## v0.1.7 — portable storage and deferred logs (2026-10-11)
**Problem:** `%LOCALAPPDATA%/pytracker-gui` profiles and per-run logs could not be shared by copying one project folder; opening an on-disk log for every console line added unnecessary I/O to the supervisor.
**Decision:** sibling `projects` outside replaceable GUI, one metadata-validated directory per named project and demo variant; profile plus `current-settings.json` and immutable per-run snapshots; no measurement artifacts moved. Copy legacy profiles once into default projects without deleting original data or previous runs. Standard ioHub YAML references are checkout-relative.
**Run ID:** five case-sensitive ASCII letters/digits from `secrets.choice`, exclusive directory creation, timestamp start in folder and save/completion in log names. **Logging:** in-memory queue+bounded spool while running, publish to project only after child completion; errors are reported but do not alter run status.
**Tradeoffs:** original run manifests retain historical absolute paths, external input data and Python installs are not bundled, OS temp may be used for unusually large logs, complete GUI log requires the GUI to process `[FINAL]`. See ADR-0018 and paired PL/EN guides. No new runtime features.

## 2026-10-11 — v0.1.8 modular navigation decision (ADR-0019)
**Observation:** The working v0.1.7 Tk experiment configuration page needs room for future separate log, diagnostic and statistic modules. Adding service-heavy tabs would couple their lifecycles and risk destabilizing the existing launcher.
**Considered:** expanding the current notebook, rebuilding the editor on every switch, multiple top-level windows, and a separate persistent `AppShell` hosting independent views.
**Decision:** retain the entire existing editor as a persistent `Experiment` screen and introduce a minimal host/navigation layer; create other views lazily and hold them in memory for reuse. Switching only packs/forgets frames. Do not commit partially edited YAML or touch `ExperimentRunner` on navigation.
**Why:** near-zero idle cost for unopened screens, minimal behavior changes, clear ownership boundaries, and safe recovery of unsaved work after returning to Experiment.
**Deferred:** actual log browser, diagnostics, statistical computation, new file formats, Docker and hardware changes. Screen-specific services will be designed only when their functionality is implemented.

## v0.1.9 — storage terminology boundary (ADR-0020, 2026-10-11)
**Observed ambiguity:** `projects/<name>/runs/` suggested that executions were a second kind of project; user explicitly wants reusable study data at project level and independent execution histories under `experiments/`. **Chosen:** rename only runtime allocation from `runs` to `experiments`, preserve the existing per-execution folder and deferred log architecture. **Rejected:** database/central archive/flat log files, moving data CSV, migrating old `runs/` paths, or changes to GUI/runtime adapters. **Safety:** do not delete historical folders automatically. **Tradeoff:** previous `runs/` directories will not be automatically discovered by the new version. See ADR-0020.

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- Selected native ttk/clam customization and small cached PNG icons instead of adding a GUI framework or animations. This keeps startup/runtime dependencies unchanged and minimizes changes to the established widget hierarchy.
- Kept Polish and English label sources and all screen navigation; orange marks priority actions, while a subdued blue remains for help `i` icons. Windows OS titlebar remains out of GUI theme scope.

## 2026-10-11 — v0.2.1 visual navigation decision
- Chose native ttk tiles rather than a new toolkit, secondary window or new navigation controller. Each tile delegates to the existing AppShell selection method.
- Dashboard is created only after brand click; current Experiment remains persistent. Brighter orange and 28px pre-rendered PNGs cost no background resources. Existing form font sizes and inactive tab padding remain untouched.


## 2026-10-11 — v0.2.2 brand logo placement
- User requested a minimal GUI change only: keep current functionality and add the new project logo beside the `pytracker-gui` title in the top-left brand area.
- Decision: retain the existing clickable ◈ symbol and brand button, insert one additional clickable logo label between them, and load the image from a packaged PNG cached once per Tk root.
- Rejected: changing screen logic, replacing the brand text, or touching any launcher/project-storage code.


## 2026-10-11 — v0.2.3 HiDPI sharpening
- User reported blurred icons in the current GUI and requested higher-resolution fonts and icons while preserving stability.
- Decision: keep native Tk/ttk, add best-effort Windows DPI awareness plus monitor-based `tk scaling`, and enlarge packaged PNG icons rather than introducing a new GUI framework or heavy rendering path.
- Tradeoff: slightly larger asset files and a small increase in startup memory, but no new dependencies, timers or background CPU load.

## 2026-10-11 — v0.2.4 read-only Manual decision (ADR-0023)
**Observation:** Extended PL/EN documentation already exists but cannot be opened directly from the current `i` tooltips. **Decision:** keep one cached catalog, add a fifth lazy screen and map each tooltip's stable key to the corresponding extended entry. Replace the legacy ◈ glyph with a small white-circle logo asset. **Why:** direct access without a new framework, duplicate content, timers or experiment work. **Testing:** Tk/Xvfb deep links, bilingual descriptions and unchanged unsaved YAML.

## 2026-10-11 — v0.2.5 English reference and starter-project naming
- Observation: 'demo' in top-level GUI labels mistakenly suggests the product only supports demos. Existing technical repo/manifest IDs are required for current projects, so those identities must remain untouched.
- Choice: display 'starter projects' for the fixed example inventory and 'project' for the user's project, with Polish/English locale-specific labels.
- Choice: add English-only structured option descriptions for documented discrete values and display them in the same lazy in-app Manual; no new form controls or run-time effects.
- Evidence: original upstream YAML and CLI flags, existing GUI choice fields, targeted and inherited tests. Polish translation is deferred to avoid unreviewed content changes.

## 2026-10-11 — v0.2.6 Manual tab boundary (ADR-0025)
- User requested clearly differentiated selectable option values and light upstream RST documentation browsing without changing Index or demo launch.
- Chosen: new green-only text tag for option values, lazy local-only Documentation tab, deferred file reads, and explicit path authority from GUI-selected upstream root. No change to help registry or demo repo.

## v0.2.8 — explicit run-specific output isolation (ADR-0027)
**Reason:** shared output roots and time-based validator discovery can misattribute another measurement CSV to a GUI run. **Decision:** per-run/per-block exclusive root, exact unique candidate, exact `--session` when available and persisted per-block association or unresolved reason. **Unchanged:** PsychoPy upstream, reusable profiles, seven variants, data CSV format, dual logs and GUI theme. **Deferred:** GUI log-preview memory cap as a separate controlled iteration.

## v0.2.9 — optional log viewer (ADR-0028)
**Observation:** closing the log popup alone would leave an unbounded `_run_display_lines` list and therefore would not limit memory growth. **Decision:** opt-out of auto-popup, keep manual Show Logs, bound display tail to 256 KiB / 2,000 lines, and spool the full GUI stream with post-run-only archival. **Why:** independent process remains untouched, short logs behave as before, long sessions can avoid Tk text rendering. **Tradeoff:** two spools (runner console and GUI augmented log) may spill to OS temp under high output; the complete GUI log still needs final status. **Deferred:** queue backpressure under extreme log rates and any removal of the existing console file.

## 2026-10-12 — v0.2.10 project-scoped demo documentation (ADR-0029)
- User explicitly deferred Diagnostics and requested project-grouped local Markdown instructions from the demo repo, not the upstream .rst repo.
- Chose native ttk.Treeview, lazy file discovery on first tab visit/path change and on-demand rendering to minimize memory and CPU. A per-file limit and read-only root boundary avoid untrusted external content and oversized UI work.
- Kept Index/deep-link semantics unchanged and deliberately avoided heavy Sphinx/Markdown dependencies or modification of original repositories.

## 2026-10-12 — v0.2.11 scoped ttk style fix
- User screenshot demonstrated a white project-tree background behind pale text. Root cause: theme configured `TTreeview` while the ttk base style is `Treeview`.
- Applied a separate `DemoDocs.Treeview` style to the affected widget instead of changing the entire GUI palette, minimizing visual and functional regression risk.

## 2026-10-12 — v0.2.12 logging policy (ADR-0030)
**Problem:** end-only writes lose the entire active run log on crash; writing every 2 s could contend with PsychoPy.
**Decision:** one append-only journal, background I/O, existing 256-KiB limit, newest-record-wins if disk unavailable, `.part` marker for interrupted or incomplete logs, no automatic recovery. A clean rename occurs only after successful final persistence.
**Why:** favor PsychoPy acquisition and bounded RAM over guaranteed preservation of every log byte during prolonged disk failure. A 15-s periodic wake and pressure trigger balance durability and load.

## 2026-10-12 — v0.2.13 / ADR-0031: Logs dashboard, stage 1
Decision: projects are discovered by actual `experiments` folders, run identities by timestamp+5-char ID; summary reads only selected run's immutable configs. Two adjacent selectors and six compact cards avoid copying Manual tree. Journal integrity and process exit remain distinct. Stage 2 log contents deferred. Motivation: compact, low-overhead historical view with no experimental data ownership.

## 2026-10-12 — v0.2.14 / ADR-0032: bounded Console Log viewer
Rejected whole-file Tk load and periodic disk watching because both can amplify contention. Chose user-triggered 64-KiB/2,000-line pages and explicit refresh for active `.part` plus strict filename/run-ID matching. Used screen-local light orange highlight and +1-step fonts; global palette and recorder stay frozen. Partial integrity is not an experiment-status judgment.

## 2026-10-12 — v0.2.16 visual revert with selective panel retention
- Direct version authority: v0.2.14. v0.2.15 uniform-size button layout is explicitly not accepted.
- Preserve three native paned separators only; button appearance unchanged except exactly three added 20px icons.
- Local, cached Tk images and no extra disk I/O/threads; reject broader refactors and persistence.

## v0.2.17 — Local width and documentation scope (2026-10-12)
- ADR-0035: equal width via Tk `grid(sticky='ew')` without modifying any intrinsic button styling. Rejected all-height/uniform-style redesign of v0.2.15 remains rejected.
- The fourth Manual tab uses an allowlist of current bundled GUI documentation only. Lazy and read-only; historical notes stay on disk and separate upstream/demo tabs remain authoritative for their respective repositories.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
ADR-0036: choose pre-optimized PNG + ttk image buttons; native Canvas overflow instead of scaling; keep all other screens frozen.

## v0.2.19 — Default window size (2026-10-12)
ADR-0037: resize only the AppShell startup geometry cap, preserving existing screen bounds and UI layout.

## v0.2.20 — Environment icons (2026-10-12)
ADR-0038: two Environment icon adjustments only; retain existing icon cache and button geometry/styles; all other buttons remain unchanged.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
ADR-0039: retain Experiment → Environment as the sole repository-path editor; GUI Settings writes only GUI startup size to the existing settings.json and reads other options. Logs tile uses the approved fixed-size image.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: keep image-only update scoped to existing four Home filenames; optimize RGB PNGs offline; no code changes beyond release identity.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: chose an actual `#RRGGBB` icon-only parameter instead of rewriting dozens of fixed-color PNGs or adding Pillow runtime; 19 compressed alpha masks and cached one-time tiny PNG construction. GUI Settings integration intentionally deferred.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
ADR-0042: retain one parameter for idle icon tint; selected icons use original orange PNGs, ink assets on filled orange buttons are unchanged. No new setting or dependency.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: rejected platform-specific Windows title bar styling. Local color override reuses existing icon mask/cache and honors explicitly saved `ICON_COLOR`; heading uses existing `Heading.TLabel`. No new settings keys.

## v0.2.34 — Polish localization (2026-10-13)

Scope: translate English v0.2.33 GUI Settings help and documentation, expose Polish option explanations in Experiment Manual. Stable keys/values preserved; runtime remains unchanged. Test gate: focused Tk/interpreter checks and regenerated PL/EN manuals, full ZIP manifest.

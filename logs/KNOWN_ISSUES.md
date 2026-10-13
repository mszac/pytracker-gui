# KNOWN ISSUES / RISKS (append-only)

| ID | Status | Problem | Działanie / warunek zamknięcia |
|---|---|---|---|
| R-001 | OPEN | Brak źródłowego exact upstream SHA w archiwach wejściowych | M0 source certification + preflight/CLI |
| R-002 | OPEN | Native Python 3.10/PsychoPy/ioHub konflikty i braki zależności | physical import and minimal run, nie modyfikować upstream |
| R-003 | OPEN | Windows DPI / screenshot / gaze alignment | monitor test, real MouseGaze |
| R-004 | OPEN | Bash launch scripts nie są samodzielnym cross-platform GUI backend | Python adapter parity incl EN/PL/timeseries blocks |
| R-005 | OPEN | YAML CWD; niekanoniczne ścieżki projektu | central path resolver + tests |
| R-006 | OPEN | Upstream może zgłaszać sukces procesu mimo niepełnych wyników | collection validators + logs/output matcher |
| R-007 | OPEN | Różnice native vs Docker i backend/mouse semantics | adapter & backend-specific profiles |
| R-008 | OPEN | Voice/real Tobii nieprzetestowane na maszynie | targeted hardware gate |
| R-009 | OPEN | Import obcych modelów/pluginów jako potencjalny arbitrary code | domyślnie disabled, osobne jawne flow |
| R-010 | OPEN | Wygenerowane YAML wobec przyszłego upstream schema drift | pin provenance + schema contract tests |

## Dopisane po audycie upstream — 2026-10-10
| ID | Status | Problem | Działanie / warunek zamknięcia |
|---|---|---|---|
| R-011 | OPEN CRITICAL | 3 demo wrappery hardcode `enable_eyetracker=True`, `enable_voice=False`, `raw_data=False`, a user wymaga modyfikowalnych parametrów | child bridge, dynamic flags, tests all variants, no silent ignore |
| R-012 | OPEN | README główne `main` jest ruchome i brak exact HEAD SHA w środowisku lokalnym | git clone/ref provenance, verify package path and CMD `--help` on OS |
| R-013 | OPEN | NO_GAZE jest response-only, a obecne demo validators sprawdzają gaze | osobny explicit behavioral validator, nie uważać gaze absence za błąd |
| R-014 | OPEN | utrata komentarzy/unknown YAML przy naive PyYAML rewrite | lossless parser/profiles copy; 9 YAML round-trip gate |
| R-015 | OPEN | main() reads eye YAML even when tracking off | pass valid ioHub config in all modes and preflight it |
| R-016 | OPEN | headless/voice/raw i różne zdarzenia mogą mieć inne output/lifecycle, `main()` logs exceptions | M1 interactive only; flag-specific integration tests and per-mode output validator |
| R-017 | OPEN | TimeSeries contains 2 serial blocks; cancellation/partial failure risk | transactional 2-block orchestration, independent status/result validation |
| R-018 | OPEN | timestamp-by-second path collision or stale output could create false PASS | per-run t0, output collision check, new output correlation |

## v0.1.0 unresolved
- KI-010-A (BLOCK for M1 launch): exact upstream SHA and demo Git SHA not pinned; target Python 3.10/PsychoPy/ioHub not validated on real Windows/Linux.
- KI-010-B (BLOCK for M1 launch): actual child bridge and session lifecycle absent. Native three wrapper entrypoints hardcode gaze/voice/raw; UI cannot invoke them as though toggles worked.
- KI-010-C (FEATURE GAP): ioHub YAML internal fields are not yet edited; GUI stores chosen path only, and does not bundle MouseGaze/Tobii file.
- KI-010-D (LIMIT): round-trip YAML preserves semantic fields/comments/order but may normalize whitespace, quoted scalar presentation, or list style; exact-byte preservation is not promised for saved profiles.
- KI-010-E (LIMIT): profile multi-file save is per-file atomic, not one transaction; SHA mismatch after interrupted writes blocks/reports load as corrupt.
- KI-010-F (NOT RUN): real Windows Tk GUI; physical Tobii, Python 3.10 with PsychoPy/ioHub, real datasets end-to-end, power/memory idle profiling and High DPI tests.
- KI-010-G (LIMIT): current static validator checks file existence/header and subset of expected YAML structures; not authoritative full upstream CustomConfig or gaze/voice validation.

## v0.1.1 outstanding and resolved
- KI-011-A (RESOLVED for path discovery): sibling layout from old documentation corrected to canonical nested checkouts; auto-detection ignores stale persisted paths when nested checkout exists.
- KI-011-B (OPEN, M1 BLOCK): GUI does not start/stop demos or apply saved profile YAML to processes; original `run-demo.sh` remains baseline only, with hardcoded MouseGaze in wrappers.
- KI-011-C (OPEN, physical gate): exact upstream/demo Git revisions on Windows and Python 3.10/ioHub/Tobii hardware validation not done in this host. Git HEAD can change after this release.
- KI-011-D (OPEN): auto detector assumes demo named `tobii-pytracker-demo` and inside upstream, as required by current native runners; altered future upstream path contracts would need an explicit migration.
- KI-011-E (OPEN): profiles can contain device config absolute paths from another machine; a stale custom file is not silently overwritten, requiring explicit correction.

## v0.1.2 additional findings
- KI-012-A (OPEN, provenance): upstream/demos were inspected through public README/RAW YAML and supplied v1.17.0 fixture sources, not from two freshly cloned immutable SHA-pinned commits in the container (no DNS); recheck parameter definitions after recording exact Windows Git HEADs.
- KI-012-B (OPEN, Windows): Tk info bubble position, DPI scaling, keyboard navigation and tooltip focus behavior passed Linux/Xvfb only; real Windows 10/11 Git Bash/Conda testing pending.
- KI-012-C (DEFERRED): long manual is a Markdown file in the source tree; no clickable link to the manual exists in the GUI by design. Internal ioHub YAML fields are described, but not editable through current forms.
- KI-012-D (UNCHANGED M1 BLOCKER): GUI does not launch experiments or apply changed profiles to original demo process; voice/raw/gaze adapter parity remains unimplemented.

## v0.1.3 — open limitations (2026-10-11)
- English full manual is intentionally not prepared; only English UI and short popover help are available. Polish full manual remains at docs/PARAMETER_MANUAL_PL.md.
- No in-GUI manual link/window (unchanged by design).
- Windows Git Bash/Conda Python 3.10 and physical Tobii testing still NOT RUN; UI screenshots/tests are Linux/Xvfb only.
- Native experiment launch and ioHub YAML internal editing remain deferred from earlier milestones.

## v0.1.4 documentation parity — closure/open items (2026-10-11)
- **RESOLVED relative to v0.1.3:** English long descriptions and full reference no longer missing. PL and EN both document the same 87 parameter keys; two installation and two user guides exist.
- **OPEN — authority drift:** Public upstream `main` and demo Git HEADs remain unpinned to user workstation commits; updated wording must be checked against the user's checkout if code changes.
- **OPEN — hardware/platform:** The real Windows/Conda Python 3.10/PsychoPy/ioHub/Tobii gates and Windows high-DPI tooltip behavior have not been run here.
- **DEFERRED:** Full manual link/window, internal ioHub YAML editing and starting demos with saved GUI profiles are not implemented; users must open the PL/EN Markdown files separately.

## v0.1.5 open runtime gates — 2026-10-11
- Blocker for certified M1: real Windows Git Bash/Conda Python 3.10 with exact upstream+demo HEAD, no physical runtime validation yet.
- MouseGaze: verify original right-button hold, left-answer events, CSV samples, focus and restart.
- Tobii: physical device/ioHub YAML detection, calibrations, acquisition, and stop; not proven by static preflight.
- Voice/raw: options forwarded, not verified with microphone/raw stream.
- Original validators require full sessions and source datasets; skipped session modes yield COLLECTION NOT VERIFIED; modified output path might affect validator expectations.
- No in-GUI editing of inner ioHub YAML and no Docker/headless path; deferred beyond native M1.

## v0.1.6 — Windows adapter field failure and residual gates (2026-10-11)
- **Fixed in code, awaiting Windows acceptance:** ambiguous `from tools.demo_runtime_adapters` path broke Text Search EN before PsychoPy. All adapter-backed launches now explicitly load `<demo_root>/tools/demo_runtime_adapters.py`; missing file becomes an actionable preflight error. On the user's workstation verify `[ADAPTER] Loaded from ...` then `[ADAPTER] Applied ...` and actual data collection.
- **Unrelated dependency warning:** `RequestsDependencyWarning` for missing `chardet`/`charset_normalizer` was present even in successful Test Demo; it was not the root cause of this crash and is intentionally not fixed in the GUI update.
- **Open:** actual Windows 3.10/Conda/Tk clipboard, all adapter-backed PsychoPy sessions, Tobii/voice/raw and collection validators must still be run by the user. A successful adapter load log is not a successful collected experiment.
- **Not changed:** earlier fullscreen/focus issue was attributed by user to an external problem and is excluded from v0.1.6 scope.

## v0.1.7 portable-project residual risks (2026-10-11)
- Files stored in `projects/` can contain experiment settings, paths and diagnostics; inspect their contents before sharing externally. CSV measurements and analysis outputs are intentionally not included.
- Copying a project does not copy external dataset paths, Python/Conda installations or exact upstream/demo checkouts. Historical run.json paths may remain absolute. Re-select locally unavailable paths.
- A hard GUI/process/OS crash before `[FINAL]` may leave only a partial or absent post-run GUI log; the raw child log is finalized by the supervisor if it survives. Disk errors after the session can prevent archiving but must not terminate the experiment.
- Windows NTFS case insensitivity: IDs differ by case but exclusive directory creation prevents case-only folder collisions within a second. No physical Windows/eye-tracker runtime benchmark for v0.1.7 yet.

## v0.1.8 modular navigation open gates (2026-10-11)
- The three additional screens are deliberately placeholders; they do not display real project logs, environment diagnostics or experiment statistics yet. The original Experiment log popup and diagnostics actions remain on the Experiment screen.
- The new top navigation consumes a small additional row of vertical space; Linux/Xvfb preview covers 1190×880. Physical Windows, small-screen, high-DPI, focus/keyboard and accessibility checks are still pending.
- Native PsychoPy/Tobii, adapter-backed demos and Windows child-process lifecycle are unchanged by this release; prior external hardware and runtime validation gates remain open.

## v0.1.9 — remaining limits after `experiments/` layout change (2026-10-11)
- Existing `projects/<name>/runs/` directories from v0.1.7/v0.1.8 are deliberately neither read nor migrated. They are left unchanged rather than deleted; users may archive them separately.
- Historical run manifests retain original absolute paths, external dataset files/Conda environments are not bundled, and a hard GUI crash before `[FINAL]` can still prevent full GUI log publication. None of these existing limits are changed by the path rename.
- Real Windows/PsychoPy/Tobii hardware and cross-checkout user tests for v0.1.9 remain external gates.

## v0.2.0 — dark/orange native visual refresh (2026-10-11)
- External visual acceptance: physical Windows 10/11 with pytracker-env, 100%/125%/150% DPI, smaller monitor, read-only combobox menus and log popup. Native Tk geometry is not an exact reproduction of rounded-corner mockup. No claim of Windows validation.
- Previously open runtime/demo hardware bugs and external gates remain open; no change in this visual-only version.

## v0.2.1 visual scope — 2026-10-11
- Physical Windows DPI scale 125%/150% and native font rasterization unverified. Larger PNGs improve icon fidelity only; system text antialiasing is outside this change.
- Other module screens remain intentionally unimplemented placeholders. Brand/home is only a navigation shortcut, not a new data processing workflow.

## v0.2.4 verification boundary (2026-10-11)
- Physical Windows/Tk HiDPI appearance and real PsychoPy/Tobii launch regression have not been reverified after the cosmetic/manual update. No known new engine changes.

## v0.2.5 notes (2026-10-11)
- English new option-value annotations are not translated into Polish in this release by request; the existing Polish Manual and tooltip descriptions remain available.
- ioHub-only and upstream-reference options are documentation, not new editable controls. Physical Tobii and dependent model support vary with hardware.

## v0.2.6 Documentation viewer scope
- The RST viewer preserves original source and highlights simple headings, but does not render Sphinx directives, embedded figures or resolve cross-document links. A missing upstream `docs/` tree or large document is reported, not silently replaced with demo documentation. No Windows/RST source-content physical test is certified yet.

## v0.2.8 session association boundaries
- Physical Windows/PsychoPy/Tobii verification of isolated native output paths is still required. Historical v0.2.6 and older runs are not retroactively bound. External moves/deletions of CSV after completion can invalidate stored absolute paths.

## v0.2.9 — logging limits / residual risks
- Auto-show logs OFF removes live Tk rendering, but not the subprocess's production of diagnostic messages or the background event queue; under pathological output rates queue growth remains possible. There is no change to the worker's log-level semantics.
- Preview shows the most recent 2,000 lines / 256 KiB; use Copy entire log or saved `.log` for full history. Explicit full clipboard copying allocates the requested content on demand.
- Complete GUI log capture after an abnormal GUI crash before `[FINAL]` remains best-effort; the separate worker console archive can still survive if the child supervisor finishes. Temp/disk-full errors are reported but cannot guarantee archives.

## v0.2.10 — Lightweight documentation renderer limitations
- Native Text styling is deliberately partial: complex tables, external media, RST directives, hyperlink navigation and HTML are not rendered as a full Sphinx/CommonMark site. Large files (>256 KiB) skip per-line formatting; Markdown is capped at 1 MiB and upstream RST retains its existing 2 MiB cap.
- Demo documentation is scoped to local `examples/<project>/**/*.md` and matching guides under `docs/basic_examples`; unrelated top-level demo-repo manuals are not a new navigation section in this release.

## v0.2.11 — Windows visual verification outstanding
- Direct dark tree style tested under Linux/Xvfb. Actual Windows/DPI contrast must be confirmed by the user; no other functional changes were made.

## v0.2.12 — single-journal limitations (2026-10-12)
- An unexpectedly killed process cannot necessarily append an `INTERRUPTED` line; remaining `.log.part` itself is the interrupted marker. Recovery/repair is deferred.
- Power loss or inaccessible volume can lose recently buffered bytes, and a 256-KiB pending queue may overwrite oldest not-yet-written bytes; such overflow is explicitly marked if the disk later recovers.
- Best-effort low-priority background writes do not provide deterministic disk-idle detection; no real Windows/PsychoPy/Tobii hardware check has yet been performed.

## v0.2.13 — open Logs-view gates
- Console Log viewing is intentionally postponed to stage 2; its disabled tab is a scope marker, not a broken feature.
- Window layout and font contrast require a physical Windows DPI/small-monitor test. Directory scanning occurs on entry/refresh; a project with exceptionally many runs may still need later paged enumeration. `result.json` reflects process status, not completeness of scientific data.

## v0.2.14 — Console Log viewer limits
- No automatic tail-follow; `.part` requires manual Refresh log. Only bytes flushed by the existing low-priority writer are visible.
- Very long unbroken lines may be split on the 64-KiB hard boundary, replacing a split multi-byte code point in preview (archive remains intact).
- Full archive copy/download, filtering/searching, repair of INTERRUPTED `.part`, and physical Windows/PsychoPy/Tobii smoke testing are deferred.
- Project/Run discovery and initial history indexing still execute on user navigation; very large directories should be checked on Windows hardware.

## v0.2.16 — Acceptance constraints
- Windows HiDPI physical check remains open for compact icon appearance and all three sash drag gestures.
- Original v0.2.14 single-row action footer can need more horizontal space when editor pane is manually narrowed; this visual limitation is preserved intentionally rather than reintroducing v0.2.15 changes.
- No new journal, YAML, PsychoPy or measurement changes.

## v0.2.17 — External UI validation (2026-10-12)
- Windows and HiDPI visual acceptance not available on this host: verify actual Environment width equalization and GUI Documentation Treeview selection colors after installation. No additional runtime correctness issues identified in this scoped change.
- Lightweight Markdown preview remains intentionally partial (not a complete HTML/CommonMark renderer). Current explicit documentation list excludes historical ADRs and logs by design.

## v0.2.18 — Fixed Home image tiles (2026-10-12)
v0.2.18: Windows HiDPI and physical display test pending. Supplied artwork captions are English in both locales by design; metadata remains localized.

## v0.2.19 — Default window size (2026-10-12)
v0.2.19: physical Windows/HiDPI visual verification of new initial geometry still pending; on smaller displays the existing screen-size cap applies.

## v0.2.20 — Environment icons (2026-10-12)
v0.2.20: real Windows/HiDPI visual confirmation of the adjusted two icons remains outstanding.


## v0.2.22 — GUI Settings and Logs home image (2026-10-12)
Physical Windows/HiDPI visual confirmation for the new GUI Settings screen and the approved Logs tile remains pending. Changes to the initial size take effect only after relaunch.

## v0.2.23 — Dashboard graphics refresh (2026-10-12)
v0.2.23: physical Windows/HiDPI verification of the four newly optimized Home images remains pending; no new known software regressions.

## v0.2.24 — Independent icon tint (2026-10-12)
v0.2.24: physical Windows/HiDPI icon-color contrast not yet tested; live GUI Settings control for ICON_COLOR intentionally deferred. Inherited v0.2.0 exact icon-count assertion assumes 52 files while v0.2.23 already contains 56; not an icon-tint regression.


## v0.2.25 — Darker idle burgundy / selected orange icons (2026-10-12)
Windows/HiDPI physical review of the new inactive/icon-selected contrast remains pending; GUI Settings does not yet expose ICON_COLOR. Older obsolete exact icon-count check is still not a release gate.


## v0.2.26 — Existing palette settings / blue idle icons (2026-10-12)
**Direct parent:** exact v0.2.25 Full. **Requested scope:** `ICON_COLOR` default changes from `#A9526B` to `#22289B` (34,40,155); active orange icon/label and all existing orange palette defaults are preserved. Added only a bottom editor in GUI Settings for existing `ICON_COLOR` and `COLORS` keys, strict #RRGGBB validation, atomic persistence through existing private `settings.json`, restart-only palette loading before `apply_theme`, and factory-default reset. No new color semantics/parameters, no live repaint/polling/Pillow. **Production change boundary:** `theme.py`, `screens.py`, `shell.py`, VERSION and `__init__.py` only. All other runtime, project and asset bytes frozen. **Checks:** focused palette and GUI regressions plus release manifest/fresh-unpack; physical Windows/HiDPI/PsychoPy not exercised here. **Exact next step:** on Windows check color editor, save/restart, default recovery, English/Polish labels and selected orange icons; do not change measurement runtime.


## v0.2.27 — Experiment presentation scope (2026-10-12)
v0.2.27: physical Windows/HiDPI validation remains outstanding. With a saved custom `ICON_COLOR`, that user preference takes precedence over the Experiment-only factory `#A46628`.

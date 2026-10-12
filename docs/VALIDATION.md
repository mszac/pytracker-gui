# Plan walidacji: Windows/Linux, input/output, platform boundary

## Bazowy matrix
| Test | Windows native (Git Bash tylko do diagnostyki) | Linux native | Docker optional |
|---|---|---|---|
| Tk UI bootstrap | PENDING | PENDING (X11/Wayland/Tcl-Tk) | poza zakresem |
| Python 3.10/runtime path | PENDING | PENDING | osobny backend |
| Upstream CLI+ioHub preflight | PENDING | PENDING | PENDING |
| MouseGaze test | PENDING | PENDING | inne input semantics |
| Real Tobii | PENDING | PENDING (wg wsparcia) | PENDING/niegwarantowane |
| Existing test+text demo | PENDING | PENDING | PENDING |
| Time-series two blocks | PENDING | PENDING | PENDING |
| New image/text/series | PENDING | PENDING | PENDING |
| Valid output + Jupyter post-hoc | PENDING | PENDING | PENDING |
| Interrupt/recovery and log quality | PENDING | PENDING | PENDING |

## Testy czysto hostowe (już w planie, brak implementacji)
- JSON project schema: invalid, missing, migration, round trip, unicode/path spaces, Windows/Linux separators.
- Config composer: dokładnie jedna sekcja dataset, whitelist pól, CWD resolve, brak nadpisania upstream/demo, atomowy zapis.
- Dataset fixtures: kolumny brakujące, pusty CSV, UTF-8 PL, obraz nienadający się do dekodowania, wiele klas, brak próbek, NaN/Inf.
- Process adapter: argv injection (shell=False), poprawny cwd, stdout/stderr osobne, nonzero exit, zero exit + brak data.csv, timeout, stop request, nested process.
- Path tests: Windows D:/..., spacje i polskie znaki; Linux symlinks/mounts; przypadkowe `../` na wejściu; duplicate output timestamps.
- Demo parity: istniejące `run_native.sh` vs nowe Python command spec; zachowanie preflight, czasu startu, walidatorów, `--unknown-label`, kolejności machine->pv.
- GUI test: responsive while process emits massive logs, bounded in-memory buffers, no accidental double launch.

## Fizyczne gate'y
- Wyświetlacz: rozdzielczość i DPI/scaling; screenshot/AOI alignment; kilka monitorów.
- MouseGaze: RIGHT-hold, zwolnienie RIGHT przed LEFT-answer, SPACJA i ESC; brak gaze ≠ brak odpowiedzi.
- Real Tobii: połączenie, calibration, zerwanie łączności, ponowne podłączenie, tryb z/bez głosu.
- Output: minimum jeden nowy `data.csv` z udanymi odpowiedziami, poprawne summary; Jupyter czyta świeże dane z tego samego uruchomienia.
- OS: Windows natywnie bez WSL i bez obowiązkowego Git Bash; Linux ze zwykłą graficzną sesją. Docker/VNC osobny gate.

## Dowody po każdym teście
OS i wersja, cmd argv, cwd, SHA commitów upstream/demo, Python i pakiety, profile danych/YAML, typ trackera, expected/observed output, elapsed/status, PASS/FAIL/NOT_RUN, działanie obejścia, next step. Brak urządzenia/`pio`/PsychoPy to BLOCKED, a nie PASS.

## Uwaga o zdrowiu danych
Upstream może maskować exceptions i zwracać 0. Należy testować validator + konkretny output i logi. W przypadku braku gaze przy poprawnej odpowiedzi wykazać osobno behavioral collection status i gaze coverage QC; nie mieszać dwóch rodzajów sukcesu.

## v0.1.0 implementation gate (2026-10-10)
See `docs/UI_PROTOTYPE_V010.md`, `logs/VALIDATION_LOG.md`, `tests/`. Editor implementation testable under Linux Xvfb; M1 hardware/Windows/native launch gates remain open. A/B original phase breakdown is partially overlapped by user request for YAML editor now; no C/D/E implemented.

## v0.1.4 documentation-only update (2026-10-11)
Both language editions now cover the same 87 source parameters, their availability/status and current M1 editor behavior. Refer to `docs/DOCUMENTATION_INDEX_PL.md` and `docs/DOCUMENTATION_INDEX_EN.md`. Demo launch/stop, physical hardware and ioHub internal editing remain pending; documentation parity does not complete M1 or replace platform validation.

## v0.1.5 native launch gate (2026-10-11)
Linux Python 3.13/Xvfb fake runtime: 43 unit tests, seven variant mapping, process isolation and dynamic flags, Time-Series order and cancellation, run snapshot integrity, PL/EN manual parity 87/87. Physical native Windows/Linux Python 3.10, connected Tobii/ioHub, PsychoPy and audio are **NOT TESTED**; accept only after user tests. See `docs/NATIVE_LAUNCH_V015_PL.md` and EN.

## v0.1.8 UI shell acceptance (2026-10-11)
Host tests: `PYTHONDONTWRITEBYTECODE=1 xvfb-run -a python -m unittest discover -s tests -v`. Verify 71 tests including five new `test_navigation_shell_v018.py` cases, PL/EN manual sync, and repeat on the fresh released ZIP. The new top-level screen switch must not rebuild the existing Experiment editor, commit YAML, touch process runner or create any background timer; future screens must be lazy. Physical Windows screen size/focus, actual run Stop/Restart, and PsychoPy/Tobii remain explicit external gates. See `docs/NAVIGATION_SHELL_V018_PL.md` / `EN.md`.

# pytracker-gui v0.1.0 — wykonany projekt interfejsu i profili YAML

**Status:** FUNCTIONAL EDITOR PROTOTYPE, not launchable engine. Milestone M1 is NOT complete.
**Baseline:** user supplied `tobii-pytracker-demo v1.17.0-release-readiness-REPO`, 8 native YAML configs behind 7 user-visible variants. Original upstream `sbobek/tobii-pytracker` is NOT bundled and exact commit SHA is NOT pinned.

## Ekrany i zachowanie

1. **Top: środowisko** — katalog dem (root, where examples/ and tools/ live), upstream path, Python 3.10 path; persist only on "Zapisz ścieżki". Probe chosen interpreter via an isolated, time-limited subprocess using `importlib.util.find_spec` (not actual PsychoPy/eye-tracker startup).
2. **Left: katalog 7 wariantów** — Test EN; UX A/B EN/PL; Time-Series Machine→PV (one demo with two independent config views); Text Search EN/PL; Image Semantic EN.
3. **Left: gaze** — no gaze, MouseGaze, Tobii; path to ioHub file, saved as profile metadata. The modes do NOT launch a device or alter current demo scripts at this stage.
4. **Right: tab Data** — dataset path; text CSV columns; the relevant bbox mode; text font_height/wrap_fraction where present; output.folder.
5. **Monitor** — resolution, physical width/distance, display index, monitor name.
6. **Wygląd** — button, text, fixation_dot, aoe settings.
7. **Instrukcje** — edit intro/outro lines in two text boxes.
8. **YAML** — complete source-derived working document, advanced editable; powered by ruamel.yaml preserving comments/unknown keys/order/tags on ordinary round-trip (but not necessarily original bytes or whitespace).
9. **Uruchomienie** — loop_count per time-series block, log_level, voice, raw, dry-run-only plan preview; no start/stop action. Hardcoded values in old UX/Text/Image adapter runners must not be ignored.
10. **Footer** — apply edits, save app-private profile, reset from demo YAML, export a copy to user-selected location, static validation report.

## Storage and data integrity

- Profiles: `%LOCALAPPDATA%/pytracker-gui/profiles/<demo_key>/` on Windows, `$XDG_CONFIG_HOME/pytracker-gui/profiles/<demo_key>/` or `~/.config/...` on Linux. Environment override `PYTRACKER_GUI_HOME` for tests.
- App settings and profile files are written with tempfile+fsync+os.replace; pre-existing individual files have `.bak` copies. A multi-file profile save is NOT one fully atomic transaction: a failed/incomplete save is detectable on next load by per-file SHA hash.
- Each profile keeps `source_sha256` of its exact base YAML to warn when original sources change; it does not automatically merge old profile into a changed upstream. GUI never deliberately overwrites source configs.
- `Exportuj YAML` prohibits overwrite of any of the eight known native YAML paths in the selected demo root; arbitrary external export destinations are allowed.
- Path values in configs are NOT implicitly changed to absolute values. Validation resolves them relative to demo root because that will be the child process CWD.
- The shipped eight YAML test fixtures are byte-identical to user-provided demo v1.17.0. These are fixtures, NOT a cloned runtime/dataset. The screenshot was made with those fixtures, not physical device execution.

## Static preflight scope

YAML structure; exactly one active dataset modality; dataset path/CSV header; image file existence; selected display numbers, positive dimensions, instructions type and output folder writability; warning for unknown runtime/hardware; config path for Tobii. **It does not validate** exact upstream CustomConfig/PsychoPy/ioHub, voice/raw, actual gaze collection, created files nor Windows hardware.

## Technology

Tkinter/ttk and Python 3.10+ standard library; only additional runtime package `ruamel.yaml`. GUI imports none of PsychoPy, tobii_research or NumPy. Child interpreter probe runs only when pressed. No Qt, Electron or browser.

## Test evidence and caveats

- Python 3.13 Linux dev host; `unittest` core+Tk smoke under Xvfb, 13 tests PASS.
- 7/7 registry, 8/8 source YAML fixtures, timeseries separation and profile isolation covered.
- Static YAML validation and `ruamel.yaml` preservation of unknown keys/comments covered.
- Physical Windows/Linux desktop and actual Python 3.10 PsychoPy/ioHub/Tobii runs: NOT RUN.
- Extended B scope remains: ioHub YAML form editing, complete upstream schema validation, exact profile session snapshots. C scope native launch/child bridge remains TODO.

## Screenshot

`docs/images/v010-linux-xvfb-preview.png` is an actual Tk screenshot on virtual Linux display with a development fixture path. It does not prove Windows/Tobii compatibility.

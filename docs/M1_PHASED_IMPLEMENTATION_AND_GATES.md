# M1 implementation checkpoints i gates (wersja nadrzędna do starych M2/M3)

Żadna faza poniżej nie jest jeszcze zaimplementowana. Milestone M1 = suma faz A..E. Każda faza ma checkpoint, testy, logi i osobny ZIP; nie prezentować PLAN jako PASS.

## Faza A — źródła, baseline i registry (`v0.1.0-env-and-catalog`)
- Spiąć upstream exact git ref/SHA, ocenić branch `main` vs demonstracyjny z release; odczytać `python --version`, `pip show`, `tobii_pytracker.__file__`, `where/which tobii-pytracker`, `sys.path`, `git status` bez dotykania upstream.
- Ustalić SHA demo i 7 wariantów, osobne cwd/argv/dane/outputs/walidatory; fake backend spec & tests.
- Tkinter/ttk shell ze stanem environment/capabilities, listą demo i wariantów; przy niezgodnym środowisku brak startu.
- Gate `A_PROVENANCE_AND_DEMO_REGISTRY_PASS`: 7/7 registry, origin/pip provenance, mock Windows/Linux paths, Tk GUI smoke na realnych OS.

## Faza B — kontrola YAML i profili (`v0.2.0-config-control`)
- Parser lossless YAML: odczyt bazowych configów, edycja wszystkich pola z `CONFIG_CONTROL_MATRIX.md`, walidacja strumienia/snapshotów, ochrona unknown keys, dual config time series, session staging.
- Standalone config preflight bez potrzeby Tobii; per demo copy profile/save/reset; file-dialog absolute paths i względne defaulty.
- Gate `B_CONFIG_ROUNDTRIP_PASS`: 9/9 native YAML (w tym smoke-only jako fixture), niezmienione źródła, 3 modalności, 2 time series configs, EN/PL, extra text fields, spacing/unicode path test.

## Faza C — native launch + wszystkie 7 wariantów (`v0.3.0-native-demo-launch`)
- Launcher cwd=demo_root, `python -m tobii_pytracker.main` lub CLI dla simple, child demo_bridge dla adaptowanych; adapter parity i runner-preserved label/response semantics.
- Proces/lifecycle/logi/stop i odseparowane stdout/stderr; two-block time series serial, nie równolegle.
- Gate `C_ALL_DEMOS_NATIVE_PASS`: Windows + Linux MouseGaze 7/7, wykonane próby i walidatory, odpowiedź-gated + outputs. Bez realnych testów platformy = NOT_RUN.

## Faza D — tryby gaze/CLI i QC (`v0.4.0-tracker-modes-and-parameters`)
- NO_GAZE, MOUSEGAZE, TOBII integracyjnie we wszystkich typach demo (Tobii wymaga sprzętu). Dynamiczne flags voice/raw/log_level/loop_count w bridged demos, a nie stare fixed wrapper.
- Wyraźnie oddzielić event-gaze mode, response-only mode i raw data; wyniki walidatora response vs gaze QC. Wykluczyć headless.
- Gate `D_MODE_PARITY_PASS`: 3-mode argv truth table, NO_GAZE results with gaze intentionally absent, MouseGaze real samples, live Tobii connect/setup/record (HARDWARE gate), voice/raw feature probes Windows/Linux.

## Faza E — release UX i hardening (`v0.5.0-m1-release`)
- Session metadata, status derived from validators, warnings on stale/collision output, error recovery, cancellation, preflight error UI, docs user operations Windows/Linux.
- Gate `E_M1_RELEASE_ACCEPTANCE`: full flow Windows/Linux with spaces/unicode, new folder per run, all 7 demos, no modifications to original repos; archive/patch reconstruction and SHA manifest, full append-only logs.

## Zależności i konflikty
- A before B/C; B before C to avoid CLI with unvalidated inputs; C before D to establish parity; D before E.
- `main.py` pyproject pin/reference + adapter monkeypatch are the main integration conflicts. Keep CLI bridge in child only and preserve demo authority.
- GUI tkinter runtime cannot import psychopy, tobii_research or Jupyter; resource baseline idle CPU/memory to measure, not assume.
- Validation scripted static on current system is independent of hardware gate; never substitute one for the other.

## Exact next implementable action
(1) na Windows/Linux pobrać i zapisać exact `git rev-parse HEAD` oryginalnego `sbobek/tobii-pytracker` i odpowiadającego demo; (2) wykonać provenance/N1R/Python 3.10 preflight i porównanie rzeczywistego `--help`; (3) przygotować 7-entry JSON/Python registry plus fake-process test; (4) dopiero wtedy uruchomić kod v0.1.0 GUI shell. Nie zmieniać upstream.

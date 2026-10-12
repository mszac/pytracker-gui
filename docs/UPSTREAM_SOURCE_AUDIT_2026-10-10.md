# Audyt oryginalnego upstream: sbobek/tobii-pytracker

**Odczyt:** 2026-10-10, URL źródła: https://github.com/sbobek/tobii-pytracker (gałąź `main`, zmienna). Odczytano bezpośrednio RAW: `pyproject.toml`, `src/tobii_pytracker/main.py`, `src/tobii_pytracker/configs/custom_config.py`, `src/tobii_pytracker/utils/eyetracker.py`, `src/tobii_pytracker/utils/gui.py`, `configs/config.yaml`, `configs/mouse_eyetracker_config.yaml`, `configs/eyetracker_config.yaml` oraz publiczne docs Configuration/CLI/Windows/Linux. Źródło internetowe NIE zostało sklonowane lokalnie, więc konkretny upstream SHA/checkout provenance pozostaje OPEN; wyniki są code-reading evidence, NIE runtime PASS.

## CLI, zgodnie z main.py cli()
| Flaga | Typ/default | Kontrakt GUI |
| --- | --- | --- |
| `--config_file` | path, `configs/config.yaml` | runtime YAML kopia aktywnego profilu |
| `--eyetracker_config_file` | path, `configs/eyetracker_config.yaml` | istniejący lub skopiowany ioHub YAML; wymagany nawet w NO_GAZE: `main()` czyta go także przy off |
| `--enable_eyetracker` | store_true / false | NO_GAZE pomija; MouseGaze/Tobii włącza |
| `--enable_voice` | store_true / false | voice on/off, fizyczne testy w późniejszym M1 gate |
| `--raw_data` | store_true / false | full vs filtered; actual gaze recording zależy od enable_eyetracker |
| `--disable_psychopy` | store_true / false | HEADLESS, wyłączone dla interaktywnego M1 launchera demonstracji |
| `--loop_count` | int / 10 | walidacja dodatniego int, max według demo; nie obiecywać więcej niż liczność danych |
| `--log_level` | str / info | info/debug/warning/error/critical |

`main()` ustawia `os.path.join(output.folder, timestamp)` i zapisuje `data.csv`; przy `disable_psychopy` i eye-tracker włącza także `raw_stream.csv`. Timestamp ma rozdzielczość sekundy — zapobiec kolizji przy identycznej sekundzie (preflight folderu i po-run provenance). `main()` łapie pewne wyjątki i tylko loguje; exit=0 nie stanowi dowodu kolekcji. `main()` odczytuje eyetracker YAML nawet jeśli enable_eyetracker=False: NIE pomijać jego walidacji w trybie NO_GAZE.

## `CustomConfig`
- exactly 1 of `dataset.image`, `dataset.text`, `dataset.time_series`; obowiązkowe ścieżki, specyficzne label/text columns.
- monitor ma `name`, `resolution[2]`, `width`, `distance`; `display_number` domyślnie 0.
- wymagane `display.gui.button` wraz z `text`, `output.folder`, `instructions.intro/outro` jako listy; dot/aoe używane przez renderer także jeżeli nie wszystkie są sprawdzane w `check_config`.
- `CustomConfig` rozwiązuje path samego config przez `.resolve()`, ale przechowuje `dataset_path` jako **nieprzebazowany string**; dataset i output są relatywne względem `cwd` child process. Python GUI nie może stosować `config.parent` jako podstawy dla danych.
- `bbox_model` top-level to własny model i inny klucz niż dataset.<type>.bbox_model; własne modele mogą uruchamiać zewnętrzny kod — tylko jawnie, nie przez automatyczny import w GUI.

## ioHub / gaze
- `configs/mouse_eyetracker_config.yaml` używa `eyetracker.hw.mouse.EyeTracker`, `controls.move=RIGHT_BUTTON`, `controls.blink=[LEFT_BUTTON, RIGHT_BUTTON]`, default sampling_rate=50, RIGHT_EYE.
- `configs/eyetracker_config.yaml` używa `eyetracker.hw.tobii.EyeTracker` oraz `model_name`, `serial_number`, `calibration.type`, `randomize`, `auto_pace`, `pacing_speed`, `runtime_settings.sampling_rate` (default 60), track_eyes=BINOCULAR, stream/save_events. Żadna wartość sampling nie jest gwarantowana dla każdego modelu hardware.
- `eyetracker.launch_hub_server` tworzy ioHub, uruchamia `tracker.runSetupProcedure()` i `setRecordingState(True)`; nie udawać sterowania kalibracją na poziomie GUI.
- `main()` przy MouseGaze rejestruje zdarzenia tylko, gdy wybrany `controls.move` przycisk jest wciśnięty; odpowiedź na przycisk PsychoPy nadal wymaga kliknięcia. Proponowane UI musi pokazywać realnie wybrany move control.
- PsychoPy `visual.Window(fullscr=True, screen=display_number)` zależy od prawdziwego display; ostrzegać przy niezgodności geometrii i trybu full screen, NIE zmieniać tego w engine.

## Pochodzenie/dependencies i platformy
- `pyproject.toml` zgłasza requires-python `>=3.10,<3.11`, package v0.1.2 w sprawdzanym main, skrypt `tobii-pytracker = tobii_pytracker.main:cli`; brak gwarancji zgodności z nieprzypiętym w przyszłości main.
- Windows/Linux: rekomendowany Python 3.10, osobne środowisko, PsychoPy i ioHub; Linux wymaga działającego X11/Wayland/Xwayland lub Xvfb dla okna graficznego; Tkinter także wymaga desktopowej sesji.
- Z plików upsteam potwierdzono kontrakt; NIE potwierdzono podpiętej wersji sprzętowej ani działania DLL/native SDK.

## Ryzyka do M1
A: live `main` zmienia się (trzeba pin SHA i zrekonstruować test z lokalnego repo); B: testy 3 adapterów na dynamiczne flagi; C: hardware Tobii calibration i Windows/Linux; D: GUI config persistence i lossless YAML; E: voice i raw_data nie są testowane w dotychczasowych adapterach; F: fizyczna zgodność monitor/DPI.

## Źródła do ponownej walidacji
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/src/tobii_pytracker/main.py
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/src/tobii_pytracker/configs/custom_config.py
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/src/tobii_pytracker/utils/eyetracker.py
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/config.yaml
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml
- https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml
- https://tobii-pytracker.readthedocs.io/en/latest/configuration.html
- https://tobii-pytracker.readthedocs.io/en/latest/commandline_usage.html

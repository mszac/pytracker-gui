# Formularz konfiguracyjny M1: pola, walidacja, zapis

**Reguła:** GUI edytuje kopię oryginalnego YAML, zachowuje nieznane klucze, komentarze i typy. Wersja źródłowa jest read-only. Na potrzeby późniejszej implementacji zalecany round-trip parser YAML `ruamel.yaml` (lekka zależność w procesie GUI) albo równoważnie testowane podejście; `yaml.safe_dump()` z PyYAML bez dodatkowych mechanizmów nie jest lossless.

| Sekcja UI | Pola YAML | Walidacja lokalna |
| --- | --- | --- |
| Dataset (istniejące dane) | dataset.image.path, .bbox_model (grid/superpixel/saliency) | folder istnieje, podfoldery klas, pliki obrazów; aktywna jedna modalność |
| Dataset text | dataset.text.path, label_column_name, text_column_name, bbox_model (word/line/sentence), color, background_color | CSV exists/header, wskazane kolumny; dla UX/Text Search `font_height`, `wrap_fraction` zachować i udostępnić w Advanced, bez utraty |
| Dataset time series | dataset.time_series.path, label_column_name, bbox_model (sample/window) | CSV exists/header, liczność próbek i nazwy kolumn |
| Monitor | display.monitor.name, resolution [w,h], width cm, distance cm, display_number | dodatnie liczby, indeks ekranu, dopasowanie do realnego monitora (WARN gdy nierówny, bez cichego nadpisywania) |
| PsychoPy GUI | display.gui.button.size [w,h], margin, color, text.color, text.size | wymiary dodatnie, kolory string / test PsychoPy przy uruchamianiu |
| Fixation/AOE | display.gui.fixation_dot.size,color, aoe [w,h] | dodatnie wymiary, AOE mieści się w display (WARN) |
| Output | output.folder | ścieżka względna demo root lub absolutna, writable/parent exists; guard against stale session; nie nadpisywać |
| Instrukcje | instructions.intro[] / outro[] | każdy wiersz string, puste wiersze legalne; edycja tekstu, NIE kreator prób |
| Opcjonalny model | bbox_model.folder,module,class | tylko advanced, import nie wykonywany w GUI; ostrzeżenie o kodzie użytkownika |
| MouseGaze ioHub | controls.move, blink, saccade_threshold; runtime_settings.sampling_rate (50/100), track_eyes RIGHT_EYE, calibration.* | zachować wszystkie inne klucze; ostrzegać, gdy move LEFT koliduje z odpowiedzią |
| Tobii ioHub | model_name, serial_number, calibration.type THREE/FIVE/NINE, randomize, auto_pace, pacing_speed, runtime_settings.sampling_rate, track_eyes BINOCULAR, save/stream_events, buffer size | części zależne od hardware; nie przedstawiać wyboru sampling rate jako gwarancji zgodności |

## Parametry CLI (nie w main YAML)
- `loop_count`: 1..n_trials zgodnie z wybranym wariantem (dla time series 2 niezależne wartości przy edycji zaawansowanej; 9+9 default).
- `log_level`: enum info/debug/warning/error/critical.
- `gaze_source`: NO_GAZE/MOUSEGAZE/TOBII; mapowanie na `--enable_eyetracker` i profile ioHub. No-gaze nadal dostaje czytelny/plausible ioHub YAML, bo oryginalny main go czyta.
- `enable_voice`: checkbox; zależność od wsparcia OS/audio/adapter bridge potwierdzać testem. `raw_data`: checkbox, disabled lub WARN gdy gaze_source=NO_GAZE (brak rejestracji do zmiany formatu). `disable_psychopy` OFF dla M1, bez UI toggle.
- `config_file`, `eyetracker_config_file`: zarządzane ze ścieżek profilu w GUI; read-only preview końcowych wartości po wyborze.

## Profil na dysku
- Profile identyfikowane przez `demo_id+variant`, `upstream_commit`, `demo_version`, `base_config_sha256`, `modified_fields`, `gaze_source`, `generated_yaml_path`. Nie kopiować całych źródeł danych do profilu; tylko referencje do ścieżek.
- Używać katalogu user data (`%LOCALAPPDATA%/pytracker-gui` Windows, `$XDG_CONFIG_HOME/pytracker-gui` Linux lub home fallback); user-selected path allowed.
- W momencie startu zamrożone YAML tworzyć w sesyjnym stagingu, wraz z manifestem; jeżeli oryginał zaktualizował się, komunikat "Base changed — Review", nie stosować bez pytania ślepego overwrite.
- Ścieżki: resolver względny do `demo_root`, niezależnie od miejsca YAML. W YAML zapisywać oryginalną wartość wybraną przez użytkownika bez niejawnej zmiany CWD; do walidacji rozwijać do ścieżki absolutnej, a nie modyfikować tekst w profilu.
- Zachować unknown fields w YAML, listy, kolejność, komentarze; bezpieczny atomic-write, poprzednia wersja profilu backup; możliwość resetu i dry-run command.

## Kontrakt walidacji
- PASS: YAML parse, upstream CustomConfig (wykonywany child Python 3.10), ścieżki/dataset/header OK, no conflicting modes, writable output, Python 3.10/imports, demo/adapter present.
- WARN: monitor size/resolution mismatch, Tobii unavailable/detection unknown, optional model unverified, voice device not validated.
- BLOCK: brak wymaganej sekcji, nieistniejący plik, brak kolumny CSV, multiple active dataset sections, brak obsługi wybranego trybu w backendzie lub failed local child imports.
- `config.py` sam nie waliduje wszystkiego (np. `fixation_dot`/`aoe` używane są później); własny preflight musi pokrywać realnie konsumowane pola.

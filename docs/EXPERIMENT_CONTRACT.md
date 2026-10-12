# Nowy eksperyment — model danych i przekład na upstream

## Zasada kompatybilności
Tworzenie eksperymentu nie oznacza automatycznej możliwości skonfigurowania dowolnego protokołu badawczego bez kodu. Pierwszy kreator wspiera **trzy klasy bodźców istniejące w upstream** oraz standardową odpowiedź klasyfikacyjną. Bardziej złożony experiment flow wymaga odrębnego, zweryfikowanego adaptera.

## Typy danych wejściowych
| Modalność | Dane w GUI | Kontrola przed sesją | Upstream mapping |
|---|---|---|---|
| `image` | folder `klasa/*.png|jpg|jpeg...` | pliki obrazów, co najmniej 1 klasa, niepuste klasy, identyfikatory, dostępność, ograniczenie liczby | `dataset.image.path`, `bbox_model` |
| `text` | CSV zawierający nazwane kolumny etykiety i tekstu | kodowanie CSV, unikatowe nagłówki, niepuste pola, liczenie klas/wierszy, opcjonalny podgląd | `dataset.text.path`, `label_column_name`, `text_column_name`, `bbox_model`, style text |
| `time_series` | CSV: indeks, kolumny próbek/kanałów, etykieta | nagłówki, liczba wierszy, typy numeryczne i braki, test shape na exact loader, profile wielokanałowe | `dataset.time_series.path`, `label_column_name`, `bbox_model` |

**Ważne**: szczegóły CSV `time_series` i możliwych grafów modelu są weryfikowane na konkretnym upstream SHA, a nie na podstawie samego nazewnictwa pól. W zbiorze demo time series jest 130 kolumn (id, `vibration_amplitude`/`power_output`, `s001`..`s127`, class).

## Struktura projektów (plan)
```
<user_projects>/
  my-study/
    project.json                # tylko pytracker-gui: schema_version, name, backend/profile
    stimuli/                    # kopia albo jawnie referencjonowany katalog danych
    configs/
      experiment.yaml           # wygenerowany main YAML dla upstream
      eyetracker.yaml           # opcjonalna kopia profilu, nie upstream source
    runs/
      <run-id>/
        run.json                # parametry, timestamp, platforma, upstream SHA, status
        config.snapshot.yaml    # copy at run start
        launch.log              # GUI orchestration process log
        collection_report.json  # exit/validator/output/protocol checks
```
Output kolekcji upstream może pozostawać w `output/<experiment>/<timestamp>/`, wskazywany z `run.json`. Nie udawać, że własny metadata JSON jest natywnym polem `data.csv`.

## Minimalny `project.json` (propozycja kontraktu)
```json
{
  "schema_version": 1,
  "project_id": "study_001",
  "name": "Nowy eksperyment",
  "backend": "native",
  "modality": "text",
  "dataset_path": "stimuli/items.csv",
  "experiment_config_path": "configs/experiment.yaml",
  "tracker_profile": "mouse-gaze",
  "runtime_profile": "python310-local",
  "metadata": {"description": "", "study_code": ""}
}
```
To metadane GUI, nie publiczny config upstream. Nazwa i identyfikatory nie są automatycznie wpisywane do plików wyjściowych runtime.

## Generator config
- Main YAML ma **dokładnie jeden** aktywny `dataset.image|text|time_series`.
- Formularz mapuje jawnie znane pola, pozostawia opcje nieobsługiwane zablokowane.
- `display.monitor` obejmuje name, `[px width,height]`, physical width cm, distance cm, display_number.
- `display.gui` zawiera rozmiary/kolory przycisków, fixation dot, AOI.
- `instructions.intro/outro` to listy linii, bez zewnętrznego templatingu ze skryptami.
- `output.folder` wskazuje kontrolowany katalog uruchomienia. Wygenerowane ścieżki powinny być poprawne względem zamierzonego CWD (dla przykładowych runnerów: demo_root); absolutne ścieżki systemowo poprawne mogą wymagać mapowania Docker i nie przechodzą bez konwersji.
- `bbox_model` top-level (custom Python model) jest **innym** mechanizmem niż modalny builtin `dataset.<modality>.bbox_model`.

## Parametry CLI / opcje sesji
`--config_file`, `--eyetracker_config_file`, `--enable_eyetracker`, `--enable_voice`, `--raw_data`, `--disable_psychopy`, `--loop_count`, `--log_level` — na podstawie dokumentacji upstream i audytu. Obsługa zależy od trybu oraz konkretnych adapterów. Domyślny eksperyment PsychoPy = interaktywny, headless = odrębna sesja ciągłej rejestracji z innymi plikami.

## Dodatkowe dane badania
- `participant_code`, `session_code` mogą być przechowywane jako **pseudonimowe metadane GUI/manifestu**, o ile operator je poda. Nie wolno zakładać, że upstream eksportuje takie kolumny; wiązanie musi być jednoznaczne i testowane.
- W przyszłości: randomizacja, bloki, warunki A/B, TAP (Think-Aloud Protocol), trigger i timing — tylko jako jawne rozszerzenia z osobnymi testami ich semantyki; nie udawać ich wsparcia przez sam YAML.
- Import plików powinien zachowywać kopię/hash materiału wejściowego lub jawną zewnętrzną referencję wraz ze statusem reprodukowalności.

## Warunek ukończenia sesji
Gdy proces zwróci 0, ale `data.csv` nie ma poprawnych triali, brakuje bloku PV lub log wskazuje save exception, wynik to `INCOMPLETE/FAILED`, nie SUCCESS. Akceptacja wymaga walidatora specyficznego dla modalności i zgodności liczby prób z RunSpec (z wyjątkiem jawnego early stop).

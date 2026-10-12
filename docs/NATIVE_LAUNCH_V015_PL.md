# pytracker-gui v0.1.5 — uruchamianie demonstracji (Windows / Linux)

## Zakres

Ta wersja dodaje przyciski **Uruchom demo** oraz **Zatrzymaj demo**. Działa na siedmiu istniejących wariantach demonstracji z ośmioma konfiguracjami YAML; wariant Time-Series Noise uruchamia kolejno dwa odrębne procesy **Machine → PV**. Aplikacja nie projektuje nowych eksperymentów, nie edytuje wnętrza ioHub YAML, nie uruchamia Dockera i nie modyfikuje kodu silnika `sbobek/tobii-pytracker` ani demonstracji `mszac/tobii-pytracker-demo`.

## Wymagany układ katalogów

```
tobii-pytracker/                  # git clone sbobek/tobii-pytracker
├── src/tobii_pytracker/
├── configs/
├── tobii-pytracker-demo/         # git clone mszac/tobii-pytracker-demo
│   ├── examples/
│   └── tools/demo_runtime_adapters.py
└── pytracker-gui/               # ten niezależny projekt, obecnie ZIP
    └── run_gui.py
```

GUI należy uruchomić w działającym środowisku `pytracker-env` (Python 3.10). GUI może wyświetlać okno z innego Pythona, ale wybrany interpreter **eksperymentu** musi być Pythonem 3.10 z pakietami `tobii_pytracker` i `psychopy`; w przeciwnym razie start jest blokowany. W `Upstream`, `Demo root`, `Python 3.10` oraz `ioHub YAML` należy podać prawidłowe ścieżki. `--check-layout` sprawdza strukturę źródeł, ale nie testuje urządzeń ani zależności PsychoPy.

## Uruchomienie

1. Otwórz GUI, wybierz jeden z siedmiu wariantów i poczekaj na wczytanie jego YAML/profilu.
2. W zakładkach Dane, Monitor, Wygląd, Instrukcje lub YAML zmień potrzebne ustawienia. **Zastosuj edycję** zapisuje zmiany w pamięci, **Zapisz profil** utrwala je w prywatnym katalogu, a **Eksportuj YAML** tworzy wskazaną kopię. Żadna z tych czynności nie uruchamia eksperymentu.
3. Wybierz NO_GAZE, MOUSEGAZE lub TOBII oraz właściwy plik ioHub. NO_GAZE nie blokuje odpowiedzi myszą. Fizyczny TOBII wymaga podłączonego urządzenia i zgodnej konfiguracji; nie jest weryfikowany przed startem.
4. W zakładce **Uruchomienie** ustaw liczbę prób *dla bieżącego bloku*, poziom logowania i ewentualnie Voice/Raw data. Raw data wymaga aktywnego gaze.
5. Kliknij **Uruchom demo**. Przed startem GUI zatwierdzi bieżący formularz, sprawdzi interpreter, repozytoria, YAML, wymagane pliki i przygotuje osobną kopię aktualnej konfiguracji dla każdego bloku.
6. Otworzy się okno dziennika. Przyciski **Zatrzymaj demo** przerywają bieżący proces i jego procesy potomne. Po przerwaniu sesji dane mogą być niepełne.

Nie należy uruchamiać równolegle oryginalnego `run-demo.sh` z GUI; może dojść do konfliktu o urządzenie, ekran lub katalog wyników. GUI blokuje drugą sesję uruchamianą z tego samego okna.

## Proces i dane

GUI nie importuje PsychoPy ani adapterów do procesu Tkinter. Uruchamia wybranym Pythonem 3.10 moduł `pytracker_gui.launch_child` w osobnym procesie, z katalogiem roboczym `tobii-pytracker-demo`. Adaptery `tools/demo_runtime_adapters.py` są używane dla UX A/B, Text Search i Image Semantic. Flagi gaze, voice, raw data, loop count, log level i ścieżki YAML są przekazywane dynamicznie do oryginalnego `main.main`.

Dla każdego uruchomienia tworzony jest prywatny katalog, np. Windows `%LOCALAPPDATA%/pytracker-gui/runs/<timestamp>_<id>` lub Linux `~/.config/pytracker-gui/runs/<timestamp>_<id>` (można użyć `PYTRACKER_GUI_HOME`). Zawiera `run.json`, `main.yaml` lub `machine.yaml` + `pv.yaml`, `console.log` i `result.json`. Oryginalne pliki dem oraz źródła upstream nie są nadpisywane. Wyniki eksperymentów pozostają w `output.folder` określonym w YAML (ścieżki względne są liczone od katalogu dem).

## Znaczenie rezultatów

- **PROCESS COMPLETE — COLLECTION VALIDATED:** wszystkie bloki zakończyły się kodem 0, a oryginalny walidator danych zakończył się poprawnie dla każdego bloku. To nie oznacza niezależnej certyfikacji urządzenia Tobii.
- **PROCESS COMPLETE — COLLECTION NOT VERIFIED:** proces zakończył się kodem 0, lecz walidator danych nie został uruchomiony; na przykład przy NO_GAZE, krótszej liczbie prób, zmienionych danych, innym układzie wyników lub braku skryptu walidacji.
- **FAILED:** proces, adapter lub walidator zwrócił błąd; przy Time-Series kolejny blok nie zostaje uruchomiony.
- **CANCELLED:** użytkownik przerwał działanie; nie należy interpretować niepełnych danych jako poprawnej sesji.

Walidatory demo są dostosowane do pełnych sesji i ich oryginalnych zbiorów bodźców. W trybach o zmienionych warunkach GUI nie zgłasza ich sukcesu. Żadna testowa sesja PsychoPy/Tobii nie została fizycznie wykonana podczas przygotowywania v0.1.5 — testy automatyczne korzystały z atrap oryginalnego runtime.

## Test Windows/Git Bash

```bash
cd /d/pytracker/tobii-pytracker
conda activate pytracker-env
python --version
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

W GUI rozpocznij od **Test Demo [EN]** przy MOUSEGAZE, trzech próbach i domyślnym źródłowym dataset. Nie używaj od razu trybu Tobii bez sprzętowego sprawdzenia. Zapisz wynik `result.json`, błędy `console.log` oraz `git rev-parse HEAD` z obu repozytoriów, jeśli test nie powiedzie się.

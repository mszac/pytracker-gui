# pytracker-gui v0.1.6 — adaptery demonstracji i kopiowanie logu (Windows / Linux)

## Przyczyna naprawionego błędu

W v0.1.5 `launch_child.py` wykorzystywał `from tools.demo_runtime_adapters import ...`. Oryginalny katalog `tobii-pytracker-demo/tools` nie musi zawierać `__init__.py`, a Python może rozwiązać nazwę `tools` do niezwiązanego pakietu znajdującego się w aktywnym środowisku. Objawem było `ModuleNotFoundError: No module named 'tools.demo_runtime_adapters'` jeszcze **przed** uruchomieniem PsychoPy w demonstracjach **UX A/B Text, Text Search i Image Semantic**. Test Demo i Time-Series nie wymagają tego adaptera, dlatego nie odtwarzały tego konkretnego błędu.

W v0.1.6 proces potomny pobiera adapter bezpośrednio z **wybranego repo demonstracji**: `<Demo root>/tools/demo_runtime_adapters.py`. Plik jest ładowany za pomocą `importlib.util.spec_from_file_location`, z pominięciem wyszukiwania pakietu o ogólnej nazwie `tools`. GUI sprawdza istnienie tego pliku **przed** startem demonstracji wymagającej adaptera. W logu pojawia się dokładna lokalizacja `[ADAPTER] Loaded from ...` i `[ADAPTER] Applied text/image adapter`. Nie kopiujemy adaptera do GUI i nie modyfikujemy kodu repozytoriów.

## Kopiowanie całego widocznego dziennika

W oknie **Dziennik eksperymentu** (EN: **Experiment log**) dodano przycisk **Kopiuj cały log** (EN: **Copy entire log**). Kopiuje on do schowka Windows/Linux całą aktualną treść okna — nie tylko zaznaczony fragment — łącznie z komunikatami `[RUN]`, `[STATUS]`, `[PROCESS]`, `[COLLECTION]` i `[FINAL]`, które dotarły do GUI przed kliknięciem. Można wkleić wynik w edytorze tekstu lub wiadomości za pomocą `Ctrl+V`. Zamknięcie i ponowne otwarcie okna zachowuje zgromadzony podgląd bieżącej sesji; kolejne uruchomienie rozpoczyna nowy podgląd. Oryginalny strumień stdout/stderr pozostaje na dysku w pliku `console.log` w katalogu sesji. Samo kopiowanie nie zatrzymuje eksperymentu ani nie edytuje jego danych.

## Aktualizacja na Windows / Git Bash

Zamknij GUI i nie uruchamiaj instalacji podczas aktywnego eksperymentu. Zapisane profile znajdują się poza katalogiem aplikacji. Rozpakuj pełny ZIP do oryginalnego `tobii-pytracker/` (archiwum zawiera już katalog `pytracker-gui/`). Zalecane jest przeniesienie dotychczasowego katalogu GUI do kopii zapasowej, zamiast scalania wersji.

```bash
cd /e/pytracker/tobii-pytracker   # dostosuj literę dysku
mv pytracker-gui "$HOME/pytracker-gui-v0.1.5-backup"
GUI_ZIP="$(cygpath -w "$HOME/Downloads/pytracker-gui-v0.1.6-demo-adapter-import-log-copy.zip")"
DEST="$(cygpath -w "$PWD")"
powershell.exe -NoProfile -Command "Expand-Archive -LiteralPath '$GUI_ZIP' -DestinationPath '$DEST' -Force"
conda activate pytracker-env
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Sprawdź, czy w repo dem jest wymagany plik:

```bash
ls tobii-pytracker-demo/tools/demo_runtime_adapters.py
```

W GUI wybierz **Text Search EN**, `MouseGaze`, odpowiednią konfigurację ioHub i kliknij **Uruchom demo**. Oczekiwane pierwsze linie związane z adapterem to `[ADAPTER] Loaded from ...` oraz `[ADAPTER] Applied text adapter`. Pojawienie się tych komunikatów potwierdza wczytanie adaptera, **nie** ukończenie zbierania danych. Następnie powtórz test dla UX A/B i Image Semantic. Test Demo powinno nadal działać; Time-Series pozostaje dwublokowe (Machine → PV).

Ostrzeżenie `RequestsDependencyWarning` o `chardet`/`charset_normalizer`, jeśli występuje, jest niezależne od naprawionego importu adaptera. Ta wersja nie modyfikuje instalacji PsychoPy ani pakietów Python. Jeżeli eksperyment nie uruchomi się po załadowaniu adaptera, skopiuj cały log i zachowaj pliki `run.json`, `console.log`, `result.json` z `%LOCALAPPDATA%/pytracker-gui/runs/`.

## Granica walidacji

Automatyczne testy obejmują procesy potomne z atrapą upstream, konflikt z innym pakietem `tools`, brak `tools/__init__.py`, wszystkie pięć wariantów wymagających adapterów, preflight brakującego pliku, schowek i obie wersje językowe GUI. Dodatkowy test w izolowanym środowisku załadował **oryginalny adapter z dostarczonego repo v1.17.0** z atrapami zależności. Rzeczywisty PsychoPy i fizyczny Windows/Tobii nie zostały uruchomione w środowisku przygotowawczym. Obserwowany przez użytkownika poprawny Test Demo stanowi wcześniejszy dowód uruchomienia jednej demonstracji na Windows, nie pełnej walidacji wszystkich dem.

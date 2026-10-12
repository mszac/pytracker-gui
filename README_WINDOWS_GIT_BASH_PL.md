# pytracker-gui v0.2.17 — instalacja i aktualizacja Windows / Git Bash

To **aktualna instrukcja po polsku**, opracowana na podstawie [README_WINDOWS_GIT_BASH_EN.md](README_WINDOWS_GIT_BASH_EN.md). Szczegóły funkcji: [polski przewodnik użytkownika](docs/USER_GUIDE_PL.md). Starsze dokumenty wersjonowane pozostają zapisem historycznym.

## 1. Wymagania i układ repozytoriów

Potrzebujesz Git for Windows, Git Bash, działającego środowiska Conda `pytracker-env` z **Pythonem 3.10 dla procesu eksperymentalnego** oraz dwóch niezależnych repozytoriów:

```text
tobii-pytracker/                       # sbobek/tobii-pytracker
├── src/tobii_pytracker/
├── configs/
├── tobii-pytracker-demo/             # mszac/tobii-pytracker-demo
│   ├── examples/
│   └── tools/
├── pytracker-gui/                   # GUI dostarczane w ZIP
└── projects/                        # projekty i historia GUI: zachowaj przy aktualizacji
```

Przykładowa lokalizacja: `E:\pytracker\tobii-pytracker`. Jeżeli repozytoria jeszcze nie istnieją, sklonuj je w Git Bash:

```bash
mkdir -p /e/pytracker
cd /e/pytracker
git clone https://github.com/sbobek/tobii-pytracker.git tobii-pytracker
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git tobii-pytracker-demo
```

**Nie klonuj ponownie do istniejących katalogów.** Wymagane jest repozytorium `tobii-pytracker-demo`; inne, podobnie nazwane repozytorium przykładów go nie zastępuje. Nie modyfikuj kodu oryginalnych repozytoriów.

## 2. Instalacja lub aktualizacja ZIP-a GUI

Pełny ZIP zawiera katalog najwyższego poziomu `pytracker-gui/`. Pobierz `pytracker-gui-v0.2.17-gui-documentation.zip` do folderu Windows **Downloads**. Przy aktualizacji **najpierw wykonaj kopię `pytracker-gui/`** i upewnij się, że nie jest uruchomiony eksperyment. **Nie usuwaj `projects/`**, który znajduje się poza kodem GUI.

```bash
cd /e/pytracker/tobii-pytracker
# Wykonaj kopię dotychczasowego GUI tylko, jeśli katalog istnieje:
if [ -d pytracker-gui ]; then
  cp -a pytracker-gui "$HOME/pytracker-gui-backup"
fi
GUI_ZIP_WIN="$(cygpath -w "$HOME/Downloads/pytracker-gui-v0.2.17-gui-documentation.zip")"
ROOT_WIN="$(cygpath -w "$PWD")"
powershell.exe -NoProfile -Command \
  "Expand-Archive -LiteralPath '$GUI_ZIP_WIN' -DestinationPath '$ROOT_WIN' -Force"
```

Jeśli korzystasz z innej lokalizacji, zmień `/e/pytracker`. Podana nazwa archiwum dotyczy **v0.2.17 z kartą GUI Documentation**; dla innego wydania użyj jego rzeczywistej nazwy. Aktualizacja GUI nie wymaga nadpisywania oryginalnych repozytoriów ani historii projektów.

## 3. Środowisko Python i kontrola wstępna

```bash
cd /e/pytracker/tobii-pytracker
conda activate pytracker-env
python --version
python -m pip install -r pytracker-gui/requirements-gui.txt
python -m tkinter
python pytracker-gui/run_gui.py --check-layout
```

Zamknij małe okno testowe Tk uruchomione przez `python -m tkinter`. Jeżeli Conda nie działa w Git Bash, skonfiguruj integrację Bash i uruchom terminal ponownie albo używaj `conda run --no-capture-output -n pytracker-env python` zamiast `python`. Niewielkie zależności GUI nie instalują ani nie konfigurują automatycznie PsychoPy, ioHub czy fizycznego trackera. **Interpreter eksperymentu** musi mieć zainstalowany oryginalny silnik i odpowiednie zależności badawcze.

`--check-layout` sprawdza ścieżki i pliki źródłowe demonstracji. Nie dowodzi gotowości eye-trackera, możliwości otwarcia okna PsychoPy ani poprawności pomiarów.

## 4. Uruchomienie GUI i eksperymentu

```bash
cd /e/pytracker/tobii-pytracker
conda activate pytracker-env
python pytracker-gui/run_gui.py
```

W **Experiment** sprawdź Demo root, Upstream, Python i ścieżkę YAML ioHub; dostępne są **Detect layout** i **Check Python**. Wybierz lub utwórz **Projekt**, wczytaj jeden z siedmiu wariantów dem, zmień YAML/formularz, kliknij **Apply changes** i opcjonalnie **Save profile**. Na karcie **Launch / Uruchomienie** wybierz tryb gaze i parametry sesji, a następnie użyj **Start demo / Stop demo**. GUI uruchamia osobny proces Python/PsychoPy; nie modyfikuje kodu oryginalnych repozytoriów.

**Auto-show logs** jest domyślnie włączone. Możesz je wyłączyć podczas długich eksperymentów, aby nie wyświetlać automatycznie konsoli; zapisywanie logów nadal działa. Każde uruchomienie ma jeden narastający dziennik `experiment_*.log.part`, który po poprawnym, kompletnym zamknięciu zmienia nazwę na `.log`. Plik `.part` może oznaczać historię przerwaną lub niepełną; automatyczna naprawa nie jest jeszcze dostępna. W **Logs** wybierzesz projekt/run, odczytasz zapisane ustawienia i przejrzysz dziennik strona po stronie. Zapisywanie wyników pozostaje zadaniem kodu oryginalnej demonstracji.

**Manual** zawiera Index, Documentation z plikami RST oryginalnego silnika oraz Demo Project Documentation z drzewem projektów i Markdown. **Statistics** pozostaje ekranem zastępczym. Granice paneli Experiment/Logs można przeciągać, ale po ponownym uruchomieniu programu proporcje nie są zachowywane. Szczegóły: [USER_GUIDE_PL.md](docs/USER_GUIDE_PL.md).

## 5. Historia uruchomień i porównanie z oryginalnym demo

Historia GUI znajduje się w `tobii-pytracker/projects/<nazwa>/experiments/<YYYYMMDD_HHMMSS>_<ID>/`, a nie w historycznym katalogu `runs/`. Są tam kopie konfiguracji i metadane (`run.json`, `result.json`); podczas uruchomienia pojedynczy dziennik konsoli ma rozszerzenie `.log.part`. To **kod danego projektu demonstracyjnego** tworzy pomiary i zapisuje je pod skonfigurowanym katalogiem wyjściowym, odizolowanym dla konkretnego uruchomienia. **Nie usuwaj ani nie zmieniaj nazwy aktywnego katalogu uruchomienia.**

Aby osobno przetestować *oryginalne demo* z jego własną konfiguracją, wykonaj:

```bash
cd /e/pytracker/tobii-pytracker
bash tobii-pytracker-demo/tools/run-demo.sh test_demo
```

To polecenie **nie korzysta z zapisanego profilu GUI**. Nie uruchamiaj równolegle oryginalnego demo i sesji GUI na tym samym urządzeniu lub w tym samym katalogu wynikowym.

## 6. Testy i rozwiązywanie problemów

W katalogu `pytracker-gui/` opcjonalne testy źródłowe obejmują `python -m unittest discover -s tests -v` oraz `python tools/render_parameter_manual.py --check`. Testy Tkintera mogą wymagać działającej sesji graficznej. Gdy start eksperymentu się nie powiedzie, najpierw sprawdź interpreter badawczy, kopie konfiguracji, `result.json` i plik `.log` lub `.log.part` konkretnego uruchomienia.

- **Conda nie działa:** skonfiguruj ją dla Git Bash albo użyj `conda run`.
- **Nie otwiera się Tk:** uruchom `python -m tkinter` w tym samym środowisku.
- **LAYOUT BLOCK:** sprawdź ścieżki oryginalnego repozytorium i zagnieżdżonego demo.
- **Brakuje `ruamel.yaml`:** zainstaluj ponownie `pytracker-gui/requirements-gui.txt` interpreterem, który uruchamia GUI.
- **Błąd startu PsychoPy/Tobii:** sprawdź *interpreter eksperymentu*, zależności oraz konfigurację ioHub; sama kontrola katalogów nie wystarcza.
- **Pozostał `.log.part`:** uruchomienie mogło zostać przerwane lub zapis logu był niepełny. Zachowaj plik; automatyczna naprawa nie jest dostępna.

**Ograniczenie walidacji:** automatyczne testy rozwojowe wykonywano na Linux/Xvfb. Rzeczywisty Windows HiDPI, PsychoPy i zbieranie danych Tobii wymagają sprawdzenia lokalnie.

**Manuale parametrów PL/EN:** [PARAMETER_MANUAL_PL.md](docs/PARAMETER_MANUAL_PL.md) oraz [PARAMETER_MANUAL_EN.md](docs/PARAMETER_MANUAL_EN.md). Historyczna instrukcja **v0.1.4** opisywała GUI bez uruchamiania; nie dotyczy to obecnego v0.2.17.

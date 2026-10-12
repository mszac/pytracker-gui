# pytracker-gui v0.2.17 — przewodnik użytkownika

**Aktualny przewodnik po polsku**, przygotowany na podstawie [USER_GUIDE_EN.md](USER_GUIDE_EN.md). Instalacja Windows/Git Bash: [README_WINDOWS_GIT_BASH_PL.md](../README_WINDOWS_GIT_BASH_PL.md). Starsze dokumenty poszczególnych wersji stanowią zapis historyczny; niniejszy przewodnik opisuje aplikację **v0.2.17**.

## 1. Cel i zakres odpowiedzialności

pytracker-gui to lekki, dwujęzyczny **edytor konfiguracji i program uruchamiający gotowe demonstracje** z `mszac/tobii-pytracker-demo`, korzystające z oryginalnego silnika PsychoPy/ioHub `sbobek/tobii-pytracker` w niezależnym procesie Pythona. Nie tworzy nowych protokołów eksperymentalnych, nie modyfikuje oryginalnych repozytoriów ani nie zastępuje kodu eksperymentu, który **generuje i zapisuje dane pomiarowe**. GUI przechowuje własne profile projektów, kopie konfiguracji konkretnych uruchomień, dzienniki konsoli i metadane wykonania. Ekran Logs nie analizuje plików pomiarowych CSV.

Główna nawigacja zawiera **Experiment**, **Logs**, **Statistics** i **Manual**. Kliknięcie logotypu otwiera panel główny z czterema kafelkami. **Statistics jest obecnie ekranem zastępczym**; Diagnostics usunięto z głównej nawigacji, ale sprawdzanie Pythona i konfiguracji nadal jest dostępne w Experiment. Pozostałe ekrany są tworzone dopiero po pierwszym otwarciu, a ich przełączanie nie zatwierdza ani nie odrzuca edycji YAML.

## 2. Wymagany układ katalogów i szybki start

```text
tobii-pytracker/                   # oryginalne repo sbobek/tobii-pytracker
├── tobii-pytracker-demo/         # osobne repo mszac/tobii-pytracker-demo
├── pytracker-gui/               # GUI z ZIP, wraz z run_gui.py
└── projects/                    # profile i historia uruchomień należące do GUI
```

Aktywuj działające środowisko Conda (`pytracker-env`; środowisko eksperymentu wymaga Pythona 3.10 z oryginalnym silnikiem i PsychoPy/ioHub). Z **katalogu głównego oryginalnego repozytorium** wykonaj:

```bash
conda activate pytracker-env
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

`--check-layout` kontroluje strukturę repozytoriów i konfiguracji; **nie potwierdza** działania PsychoPy, urządzenia ioHub ani fizycznego Tobii. Sam interfejs korzysta z niewielkiego zestawu zależności Tk/ruamel.yaml; środowisko badawcze trzeba osobno przygotować do uruchamiania eksperymentów.

## 3. Projekty, warianty i edycja konfiguracji

**Projekt** jest wielokrotnego użytku obszarem pracy GUI i musi zostać wybrany przed edycją lub uruchomieniem. Pliki projektu znajdują się w `projects/<projekt>/`; katalog jest **poza** `pytracker-gui/` i należy go zachować podczas aktualizacji. **Nowy projekt…** tworzy projekt dla jednego z istniejących wariantów demonstracji.

| Demonstracja | Dostępne warianty | Bloki uruchomienia |
| --- | --- | --- |
| Test Demo | EN | Test Demo |
| UX A/B Text | EN / PL | Jeden blok wybranego języka |
| Time-Series Noise | Machine Vibration → PV Power | Dwa kolejno wykonywane, osobno konfigurowane bloki |
| Text Search | EN / PL | Jeden blok wybranego języka |
| Image Semantic | EN | Jeden blok |

Dostępnych jest **siedem wariantów** opartych na **ośmiu źródłowych plikach YAML**. EN/PL w nazwach demonstracji oznacza język materiałów eksperymentalnych, a nie język GUI.

W **Experiment** wskaż katalog Demo root, oryginalny Upstream i interpreter Python; w razie potrzeby użyj **Detect layout**, **Check Python**, **Load repository** lub **Save paths**. Edytor udostępnia istniejące w źródłowym YAML pola danych, monitora, wyglądu, instrukcji oraz edycję surowego YAML. Wybór konfiguracji ioHub wskazuje ścieżkę pliku YAML, ale nie edytuje wewnętrznych ustawień urządzenia.

- **Apply changes / Zastosuj zmiany** zatwierdza edycję bieżącej karty w roboczej konfiguracji w pamięci.
- **Save profile / Zapisz profil** zapisuje profil projektu do ponownego użycia; nie nadpisuje YAML oryginalnych repozytoriów.
- **Restore original / Przywróć oryginał** przywraca w pamięci konfigurację źródłową, nie usuwając zapisanych profili.
- **Export YAML / Eksportuj YAML** zapisuje osobną kopię YAML, bez nadpisywania źródłowego pliku demonstracji.
- Istniejące zabezpieczenia ostrzegają przed utratą niezapisanych zmian.

W v0.2.16 zachowano **naturalne wymiary przycisków i jednorzędową stopkę z v0.2.14**. Małe ikony dodano **tylko do Check Python, Detect layout i Apply changes**; odrzuconego wyglądu przycisków o wyrównanych wymiarach i dwurzędowej stopce z v0.2.15 nie wykorzystano.

## 4. Start/Stop i automatyczne wyświetlanie logów

W **Experiment → Launch / Uruchomienie** wybierz tryb śledzenia wzroku (**NO_GAZE**, **MOUSEGAZE** lub **TOBII**), YAML ioHub, liczbę prób dla każdego bloku oraz dostępne opcje głosu, danych surowych i poziomu logowania. MouseGaze symuluje dane gaze przez ioHub; TOBII wymaga zgodnego urządzenia i sprawdzonej lokalnej konfiguracji. Kontrola przedstartowa nie potwierdza gotowości sprzętu.

**Start demo / Uruchom demo** tworzy wyłączny katalog uruchomienia, zapisuje niezmienne kopie konfiguracji z chwili startu, a następnie uruchamia osobny proces Python/PsychoPy. W Time-Series blok Machine jest wykonywany przed PV w osobnym procesie. **Stop demo / Zatrzymaj demo** żąda zakończenia bieżącego uruchomienia; dane eksperymentalne mogą pozostać niepełne. Za generowanie i zapisywanie pomiarów odpowiada **kod oryginalnej demonstracji**, a nie GUI.

**Auto-show logs / Automatycznie pokazuj logi** jest domyślnie **włączone** i otwiera osobne okno konsoli. Wyłącz je przy długich eksperymentach, jeśli nie chcesz automatycznie renderować tekstu w Tkinterze; **Show Logs / Pokaż logi** pozostaje dostępny ręcznie. Wybór zapisuje się w lokalnych ustawieniach aplikacji, nie w YAML eksperymentu. Podgląd konsoli ma limit **2 000 linii lub 256 KiB**, zależnie od tego, który osiągnie wcześniej; **Copy entire log / Kopiuj cały log** działa niezależnie od limitu podglądu.

Zapisujący dziennik wątek nie blokuje odczytu wyjścia procesu i korzysta z najlepiej dostępnych, niskopriorytetowych operacji I/O. Bufor niezapisanych danych ma **256 KiB**; kiedy zapis na nośnik nie nadąża, najstarsze *jeszcze niezapisane* wpisy mogą zostać zastąpione najnowszymi. Rozwiązanie chroni działający eksperyment, ale może pozostawić niepełny dziennik. Nie gwarantuje całkowitej bezczynności dysku ani przeżycia awarii zasilania.

## 5. Historia uruchomień i jeden dziennik konsoli

```text
projects/<projekt>/
├── project.json
├── current-settings.json
├── profiles/<wariant>/...
└── experiments/
    └── YYYYMMDD_HHMMSS_aB9z0/
        ├── run.json
        ├── gui-settings.json
        ├── main.yaml                 # lub machine.yaml / pv.yaml
        ├── eyetracker.yaml           # gdy dotyczy
        ├── result.json               # status/diagnostyka, nie dane pomiarowe
        └── experiment_YYYYMMDD_HHMMSS_aB9z0.log.part
```

Pięcioznakowy alfanumeryczny Run ID **rozróżnia wielkość liter**. Dla uruchomienia powstaje **jeden** trwały dziennik konsoli, a nie dwa pliki `console_*.log` i `experiment_*.log`. Podczas pracy komunikaty są dopisywane partiami do `.log.part`. Po prawidłowym zakończeniu i kompletnym utrwaleniu plik zmienia nazwę na `.log`; po zatrzymaniu, przerwaniu lub niekompletnym zapisie pozostaje `.log.part`, ewentualnie z oznaczeniem `INTERRUPTED` lub `BUFFER_OVERFLOW`. **Odzyskiwanie i naprawa plików `.part` nie są jeszcze zaimplementowane.** Kompletny `.log` **nie oznacza** sukcesu samego eksperymentu.

Runner rezerwuje osobny katalog zawierający Run ID i nazwę bloku pod wskazanym `output.folder`; **oryginalny kod eksperymentu** tworzy tam własny katalog sesji i zapisuje pomiary. Pliki `run.json` i `result.json` GUI rejestrują pochodzenie i status oraz mogą zawierać dokładne ścieżki sesji, ale GUI nie zapisuje ani nie analizuje pomiarów. Dawne katalogi `projects/<projekt>/runs/` nie są automatycznie migrowane do `experiments/`.

## 6. Logs — historia i raport ustawień tylko do odczytu

**Logs / Logi** wykrywa projekty zawierające rzeczywisty katalog `experiments/`. Wybierz projekt, a następnie uruchomienie (od najnowszego). Dashboard odczytuje **historyczne kopie konfiguracji**, nie bieżące wartości edytora YAML, i prezentuje sześć zwartych sekcji: identyfikacja, środowisko, wykonanie, dane wejściowe, monitor/wygląd oraz konfiguracja. Dodatkowe szczegóły YAML można rozwinąć. Oznaczenie dziennika rozróżnia **kompletny** `.log`, **niepełny** `.log.part` i **brak pliku**; nie jest to ocena sukcesu badania.

Po przełączeniu na **Console Log / Log konsoli** można przeglądać dziennik wybranego uruchomienia. **First / Previous / Next / Latest**, **Refresh log** oraz **Copy page** operują na stronie o rozmiarze najwyżej **64 KiB i 2 000 wierszy**. Rosnący `.log.part` jest odświeżany ręcznie. Brak automatycznego odpytywania, naprawy plików, odczytu CSV i zapisu zmian. Ekran Logs ma lokalnie powiększone czcionki i jasnopomarańczowe zaznaczenie dla lepszej czytelności.

## 7. Manual i języki

**Manual** ma cztery karty:

- **Index** (domyślna): 87 parametrów z wyszukiwaniem i rozszerzonymi opisami PL/EN; pomarańczowy link **man** w dymku otwiera odpowiadający wpis Index.
- **Documentation**: przeglądarka lokalnych plików `*.rst` z katalogu `tobii-pytracker/docs/` **oryginalnego repozytorium**.
- **Demo Project Documentation**: rozwijane drzewo **projekt → pliki Markdown** czytające lokalne instrukcje `.md` z `tobii-pytracker-demo`, razem z właściwymi przewodnikami przykładów.
- **GUI Documentation**: drzewo aktualnej dokumentacji tej instalacji pytracker-gui, pogrupowane według języka (EN/PL), z lekkim podglądem Markdown. Nie czyta dokumentacji upstream/dem ani wyników eksperymentów.

Nagłówki, listy i kod Markdown/reStructuredText są pokazywane z lekkim formatowaniem natywnego Tkintera. To **nie jest** pełny renderer CommonMark/Sphinx; złożone tabele, obrazy i dyrektywy mogą pozostać uproszczone. Dokumenty są czytane na żądanie, a duże pliki mogą korzystać z widoku zwykłego tekstu. Nie jest instalowany silnik przeglądarki internetowej.

Język interfejsu (domyślnie polski) i język opisów parametrów można wybierać niezależnie. Przełączenie języka nie zapisuje YAML. Niebieskie **i** w dymku udostępnia krótką pomoc; link **man** otwiera pełniejszy opis bez zatwierdzania niezapisanych zmian edytora.

## 8. Przesuwanie granic paneli

Przeciągaj natywne separatory, aby regulować proporcje **Experiment: lista projektów startowych ↔ edytor**, **Logs: panel wyboru ↔ raport/konsola** oraz **Logs: projekty ↕ uruchomienia**. Minimalne wymiary uniemożliwiają całkowite zwinięcie paneli. Ustawione proporcje pozostają podczas nawigacji w obrębie jednej sesji aplikacji, ale **nie są zapisywane między uruchomieniami**. Nie dodano timerów, dodatkowych wątków ani bibliotek układu.

### Oznaczenia dostępności parametrów

Manual 87 parametrów korzysta z oznaczeń: `gui` (pole edytowane w GUI), `yaml-only` (udokumentowane YAML bez osobnej kontrolki), `iohub-only` (wewnętrzne ustawienia ioHub), `reference` (informacja o upstream/CLI) i `future` (niezaimplementowane w GUI). Status `gui` nie gwarantuje automatycznie, że każda demonstracja korzysta z danego pola. Zobacz [polski manual parametrów](PARAMETER_MANUAL_PL.md) i [angielski manual parametrów](PARAMETER_MANUAL_EN.md).

## 9. Ograniczenia, walidacja i bezpieczeństwo

Kontrola konfiguracji i testy kolekcji nie potwierdzają naukowej poprawności pomiarów ani rzeczywistej precyzji eye-trackera. Za wyniki odpowiadają zewnętrzne procesy PsychoPy/demonstracji; nie uruchamiaj równolegle oryginalnego `tools/run-demo.sh` na tym samym urządzeniu i w tej samej lokalizacji danych. **Statistics** nie jest jeszcze zaimplementowane. Windows/HiDPI oraz rzeczywiste uruchomienia PsychoPy/Tobii wymagają sprawdzenia na komputerze użytkownika; automatyczne testy GUI Linux/Xvfb nie dowodzą poprawności działania sprzętu.

**Dodatkowe materiały:** [indeks dokumentacji](DOCUMENTATION_INDEX_PL.md), [natywne uruchamianie](NATIVE_LAUNCH_V015_PL.md), [jeden narastający dziennik](INCREMENTAL_SINGLE_LOG_V0212_PL.md), [historia Logs](LOGS_HISTORY_STAGE1_V0213_PL.md), [przeglądarka logów](LOGS_CONSOLE_VIEWER_V0214_PL.md), [drzewo instrukcji Manuala](MANUAL_DEMO_TREE_V0210_PL.md), [klasyczne przyciski i przesuwane panele](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_PL.md).

**Korekta historyczna:** opis v0.1.4 mówił, że GUI **„nie uruchamia”** eksperymentów. To już nieaktualne: v0.2.17 uruchamia istniejące obsługiwane demonstracje.

**v0.2.17:** Cztery przyciski Environment mają szerokość wyznaczaną przez Load repository; pozostałe elementy przycisków pozostają niezmienione. [Opis nowej zakładki](GUI_DOCUMENTATION_V0217_PL.md).

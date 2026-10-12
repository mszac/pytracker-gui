# Katalog funkcji i zakres

Priorytet: P0 wymagane do wiarygodnego uruchomienia; P1 potrzebne do pracy z nowym eksperymentem; P2 rozszerzenia. Etapy mapują się na `ROADMAP.md`.

| ID | Funkcja | Etap | Warstwa / ograniczenia |
|---|---|---|---|
| F01 | Autowykrywanie lub ręczny wybór interpretera Python 3.10 do runtime, repo upstream i demo | M1 | Preflight/paths, bez importu PsychoPy do GUI |
| F02 | Check instalacji: Python, importy, `tobii-pytracker --help`, ioHub, tracker YAML, uprawnienia i CWD | M1 | Wynik PASS/WARN/FAIL/NOT_TESTED, żadnej cichej naprawy pakietów |
| F03 | Katalog 5 demonstracji i wariantów EN/PL, w tym dwuetapowy time series | M1-M2 | Różne entrypoints; profile uruchomieniowe oparte na audytowanych komendach |
| F04 | Przejrzyj plan uruchomienia (komenda, cwd, pliki, hash config, wynik) | M1 | RunManifest, redakcja danych wrażliwych |
| F05 | Uruchom/monitoruj/zatrzymaj sesję, status, stdout/stderr | M1 | Osobny child process, asynchroniczny czytnik logów, UI responsive |
| F06 | Po zakończeniu sprawdź poprawność output i uruchom istniejące walidatory | M1-M2 | Exit 0 niewystarczający; liczba triali/błędy kompletności |
| F07 | Projekt eksperymentu: utwórz/otwórz/duplikuj, metadane, workspace | M2 | Projekt GUI odrębny od YAML upstream; wersjonowana metadana |
| F08 | Kreator: obraz / tekst / szereg czasowy; wybór folderu/CSV i walidacja | M2 | Tylko typy potwierdzone przez upstream; kontrakt danych poniżej |
| F09 | Formularz monitora i PsychoPy GUI: rozdzielczość, szerokość cm, odległość, ekran, przyciski, AOI, fixation dot | M2 | Mapowanie 1:1 do `display`; ostrzeżenia DPI / overflow |
| F10 | Edytor instrukcji intro/outro, etykiet i liczby prób | M2 | Opcje zależne od entrypoint; nie wszystkie etykiety są swobodnie ustawialne |
| F11 | Dataset bbox `image:{grid,superpixel,saliency}`, `text:{word,line,sentence}`, `time_series:{sample,window}` | M2 | Opcje zależne od runtime; walidacja na exact upstream |
| F12 | Generuj `config.yaml` i zamrożony snapshot konfiguracji/asset manifest do sesji | M2 | Nie modyfikuj upstream ani plików demo źródłowych |
| F13 | Profil eye-tracker: MouseGaze oraz upstream-compatible device config, test dostępności | M3 | Bez obietnicy automatycznego wykrycia modelu do czasu testów sprzętu |
| F14 | Flagi enable_eyetracker, enable_voice, raw_data, disable_psychopy, loop_count, log_level | M2-M3 | Osobne tryby eksperyment/headless; walidacja niedozwolonych kombinacji |
| F15 | Lista wykonanych sesji, szybkie otwieranie folderu, status walidacji, notebook Jupyter | M2-M3 | Otwarcie analiz poza procesem GUI; nie ukrywać braku danych |
| F16 | Import/eksport profili, archiwum projektów, walidacja ścieżek Windows/Linux | M3 | Schemat migracji + względne ścieżki względem projektu |
| F17 | Docker/VNC launch profiles i obsługa start/stop kontenera | M4 | Osobny adapter backendu; Docker optional, nie wymagać w instalacji native |
| F18 | Zaawansowane/custom bbox models, niestandardowe datasety i adaptery | M4+ | Niezaufany kod nie jest „zwykłą konfiguracją”, tylko rozszerzeniem z kontrolą |
| F19 | Playback/preview bodźca poza pełną sesją | M4+ | Co najwyżej lekki podgląd pliku; rendering dokładnie PsychoPy = osobny test process |
| F20 | Lokalizacja interfejsu PL/EN, dostępność, skalowanie UI, skróty klawiszowe | M1+ | Nie mylić języka GUI z wariantem językowym danych eksperymentu |

## Nie należy sugerować jako istniejącej funkcji upstream
- Swobodnego graficznego projektowania dowolnych ekranów, kolejności/scenariuszy/branchingu, timerów i odpowiedzi bez dodatkowej warstwy adaptera.
- Gwarantowanej obsługi wszystkich modeli Tobii, wszystkich formatów wideo/audio i natywnego kreatora kalibracji.
- Dokładnej wizualnej symulacji PsychoPy w lekkim Tkinterze.
- Automatycznej, ciężkiej analizy wzroku (heatmaps/saccades/ML) wewnątrz GUI.

## Kwalifikowanie parametrów
1. **DIRECT**: parametr upstream YAML/CLI już potwierdzony.
2. **DEMO_ADAPTER**: zachowanie dostarczonych `run_experiment.py`/`demo_runtime_adapters.py`; używaj konkretnej istniejącej implementacji.
3. **FUTURE_EXTENSION**: wymaga nowego adaptera lub testu upstream; UI disabled z wyjaśnieniem do czasu implementacji.

Przykłady: `loop_count`=DIRECT; tekstowe relabel `none` na `I DON'T KNOW`=DEMO_ADAPTER; dowolny custom branching=FUTURE_EXTENSION. Ten status musi być jawny w specyfikacji każdego pola.

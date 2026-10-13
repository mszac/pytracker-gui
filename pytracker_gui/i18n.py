"""English/Polish UI labels, independent of YAML keys and serialized profile data.

Polish originals remain the translation keys so previously released UI and
manual text remain the default. No Python/PsychoPy or network dependency.
"""

LANGUAGES = ('pl', 'en')

UI_EN = {
    'Podręcznik': 'Manual',
    'Ustawienia GUI': 'GUI Settings',
    'Kolor punktu fiksacji': 'Fixation dot color',
    'Model obszarów': 'Bounding box model',
    'Poziom rejestrowania': 'Log level',
    'Rozmiar punktu fiksacji': 'Fixation dot size',
    'Wysokość czcionki': 'Font height',
    'Nie można nadpisać oryginalnej konfiguracji projektu startowego.': 'Cannot overwrite the original starter-project configuration.',
    'Automatyczny układ: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Uruchamianie projektów dostępne w zakładce Uruchomienie.': 'Automatic layout: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Project launch is available on the Launch tab.',
    'Zapisano zmiany wyłącznie w pamięci. Zapisać profil przed zmianą projektu startowego?': 'Changes exist only in memory. Save the profile before switching starter projects?',
    'Uruchamianie projektów dostępne w zakładce Uruchomienie.': 'Project launch is available on the Launch tab.',
    'M1 · konfiguracja i uruchamianie projektów': 'M1 · configure and launch projects',
    'Projekty startowe (7)': 'Starter projects (7)',
    'Wybierz projekt startowy': 'Select a starter project',
    'Uruchom projekt': 'Launch project',
    'Zatrzymaj projekt': 'Stop project',
    'Wybierz prawidłowy katalog repozytorium projektów startowych i kliknij „Wczytaj repo”.': 'Select the starter-project repository directory, then click Load repository.',
    'Brak źródła YAML — wskaż katalog projektów startowych i kliknij Wczytaj repo': 'YAML source missing — set starter-project directory and click Load repository',
    'Wskaż katalog repozytorium projektów startowych, potem kliknij Wczytaj repo.': 'Select the starter-project repository directory, then click Load repository.',
    'Katalog projektów startowych': 'Starter-project repository',
    'Edytor konfiguracji i launcher 7 projektów startowych.': 'Configuration editor and launcher for seven starter projects.',
    'Wybierz ekran': 'Choose a screen',
    'Eksperyment': 'Experiment',
    'Logi': 'Logs',
    'Diagnostyka': 'Diagnostics',
    'Statystyki': 'Statistics',
    'Logi eksperymentów': 'Experiment logs',
    'Historia logów projektów będzie dostępna w przyszłej wersji.': 'Project log history will be available in a future release.',
    'Obecne okno Experiment log jest nadal dostępne na ekranie Eksperyment.': 'The existing Experiment log window remains available on the Experiment screen.',
    'Diagnostyka eksperymentu': 'Experiment diagnostics',
    'Oddzielne narzędzia diagnostyczne zostaną dodane w przyszłej wersji.': 'Separate diagnostic tools will be added in a future release.',
    'Dotychczasowe Sprawdź Python i Sprawdź konfigurację pozostają na ekranie Eksperyment.': 'The existing Check Python and Validate configuration actions remain on the Experiment screen.',
    'Statystyki projektu': 'Project statistics',
    'Statystyki i wykresy zostaną dodane w przyszłej wersji.': 'Statistics and charts will be added in a future release.',
    'Ten ekran nie odczytuje logów, wyników ani danych eksperymentu.': 'This screen does not read logs, results or experiment data.',
    'Proces nadal się zatrzymuje. Poczekaj na zakończenie.': 'The process is still stopping. Wait until it exits.',
    'Projekt:': 'Project:',
    'Nowy projekt…': 'New project…',
    'Nowy projekt': 'New project',
    'Nazwa projektu (litery, cyfry, _ lub -):': 'Project name (letters, digits, _ or -):',
    'Nie udało się zapisać logu projektu: ': 'Could not save project log: ',
    'Automatyczny układ: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Uruchamianie dem dostępne w zakładce Uruchomienie.':
        'Automatic layout: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Demo launch is available on the Launch tab.',
    'Backend: native Python subprocess · logi w osobnym oknie':
        'Backend: native Python subprocess · logs in a separate window',
    'Uruchom demo': 'Start demo',
    'Pokaż logi': 'Show logs',
    'Zatrzymaj demo': 'Stop demo',
    'Uruchomienie w osobnym procesie Python 3.10': 'Run in a separate Python 3.10 process',
    'Voice (mikrofon wymagany)': 'Voice (microphone required)',
    'Raw data (wymaga gaze)': 'Raw data (requires gaze)',
    'Uruchom demo: zapisuje kopię bieżącego YAML poza repozytoriami i uruchamia proces.\nWynik procesu i walidacja zebranych danych są raportowane osobno.':
        'Start demo: creates a copy of the current YAML outside the repositories and starts the process.\nProcess completion and collected-data validation are reported separately.',
    '\n\nEdytor konfiguracji i launcher 7 wariantów dem.\nPsychoPy działa w osobnym procesie Python 3.10.\nUstawienia są zapisywane w osobnym katalogu profili.':
        '\n\nConfiguration editor and launcher for 7 demo variants.\nPsychoPy runs in a separate Python 3.10 process.\nSettings are saved in a separate profiles directory.',
    'Nie można uruchomić': 'Cannot start',
    'Wybierz Python 3.10 z działającymi pakietami tobii_pytracker i psychopy.':
        'Select Python 3.10 with working tobii_pytracker and psychopy packages.',
    'Eksperyment uruchomiony; wyniki i logi pozostają w osobnych katalogach.':
        'Experiment started; results and run logs are stored separately.',
    'Dziennik eksperymentu': 'Experiment log',
    'Zamknij okno logów': 'Close log window',
    'Kopiuj cały log': 'Copy entire log',
    'Automatycznie pokazuj logi': 'Auto-show logs',
    'Skopiowano cały log eksperymentu do schowka.': 'Entire experiment log copied to clipboard.',
    'Błąd kopiowania logu': 'Cannot copy log',
    'Wynik eksperymentu: ': 'Experiment result: ',
    'Zatrzymać eksperyment?': 'Stop experiment?',
    'Przerwanie sesji może pozostawić niekompletne dane. Zatrzymać proces?':
        'Stopping a session may leave incomplete data. Stop the process?',
    'Zamknięcie GUI przerwie trwającą sesję. Kontynuować?':
        'Closing the GUI will interrupt the running session. Continue?',

    'Dane': 'Data',
    'Monitor': 'Monitor',
    'Wygląd': 'Appearance',
    'Instrukcje': 'Instructions',
    'YAML': 'YAML',
    'Uruchomienie': 'Launch',
    'Język interfejsu': 'Interface language',
    'Język podpowiedzi': 'Tooltip language',
    'Manuale PL/EN: docs/PARAMETER_MANUAL_PL.md i docs/PARAMETER_MANUAL_EN.md': 'Manuals PL/EN: docs/PARAMETER_MANUAL_PL.md and docs/PARAMETER_MANUAL_EN.md',
    'M1 · konfiguracja i start dem': 'M1 · existing demos · edit without modifying source files',
    'O projekcie': 'About',
    'Środowisko i repozytoria': 'Environment and repositories',
    'Wybierz…': 'Browse…',
    'Zapisz ścieżki': 'Save paths',
    'Sprawdź Python': 'Check Python',
    'Wczytaj repo': 'Load repository',
    'Wykryj układ': 'Detect layout',
    'Układ wymagany przez run_native.sh: tobii-pytracker / tobii-pytracker-demo + pytracker-gui':
        'Layout required by run_native.sh: tobii-pytracker / tobii-pytracker-demo + pytracker-gui',
    'Wariant demonstracji (7)': 'Demo variants (7)',
    'Wybierz dokładny wariant': 'Select an exact variant',
    'Źródło gaze': 'Gaze source',
    'Brak rejestrowania': 'No gaze recording',
    'MouseGaze (mysz)': 'MouseGaze (mouse)',
    'Tobii (urządzenie)': 'Tobii (device)',
    'ioHub YAML (wybór ścieżki)': 'ioHub YAML (choose file)',
    'Wybierz plik ioHub…': 'Choose ioHub file…',
    'Blok:': 'Block:',
    'Przywróć oryginał': 'Restore original',
    'Eksportuj YAML…': 'Export YAML…',
    'Sprawdź konfigurację': 'Validate configuration',
    'Zapisz profil': 'Save profile',
    'Zastosuj edycję': 'Apply changes',
    'Backend: start dem niedostępny (M1-C)': 'Backend: demo launch unavailable (M1-C)',
    'Wybierz prawidłowy katalog repozytorium dem i kliknij „Wczytaj repo”.':
        'Select a valid demo repository directory and click “Load repository”.',
    'Edycja pól istniejącego YAML · zastosuj zmiany przed zapisem':
        'Edit fields in existing YAML · apply changes before saving',
    'Instrukcje są listami tekstów: każda linia to osobny element YAML.':
        'Instructions are lists of text: each line is a separate YAML item.',
    'Instrukcje INTRO': 'INTRO instructions',
    'Instrukcje OUTRO': 'OUTRO instructions',
    'Zaawansowany edytor kopii YAML (z zachowaniem komentarzy i obcych kluczy)':
        'Advanced YAML copy editor (preserves comments and unknown keys)',
    'Przygotowanie uruchomienia (funkcja startu wejdzie w etapie M1-C)':
        'Launch preparation (start feature is planned for M1-C)',
    'Liczba prób': 'Trial count',
    'Log level': 'Log level',
    'Voice (wymaga walidacji adapterów)': 'Voice (adapter validation required)',
    'Raw data (wymaga gaze i walidacji)': 'Raw data (requires gaze and validation)',
    'Podgląd kontraktu uruchomienia': 'Preview launch contract',
    'Uruchomienie eksperymentów jest celowo niedostępne w tym prototypie.\n'
    'Adaptery dem wymagają osobnego child bridge; nie wykorzystujemy obecnych wrapperów z na stałe wpisanymi flagami.':
        'Experiment launching is intentionally unavailable in this prototype.\n'
        'Demo adapters require a separate child bridge; hardcoded wrappers are not used.',
    'Zamknij': 'Close',
    'O pytracker-gui': 'About pytracker-gui',
    'pytracker-gui v': 'pytracker-gui v',
    '\n\nLekki edytor konfiguracji 7 wariantów dem.\n'
    'Nie uruchamia PsychoPy/Tobii; etap C M1 będzie oddzielnym wydaniem.\n'
    'Ustawienia są zapisywane w osobnym katalogu profili.':
        '\n\nLightweight configuration editor for 7 demo variants.\n'
        'Does not launch PsychoPy/Tobii; M1-C is a separate release.\n'
        'Settings are saved in a separate profiles directory.',
    'Niekompletny układ repozytoriów': 'Incomplete repository layout',
    '\n\nRepozytoria trzeba sklonować we wskazanej strukturze.':
        '\n\nClone the repositories in the indicated layout.',
    'Błąd zapisu': 'Save error',
    'Diagnostyka środowiska (bez eksperymentu)': 'Environment diagnostics (no experiment)',
    'Niezapisane zmiany': 'Unsaved changes',
    'Zapisano zmiany wyłącznie w pamięci. Zapisać profil przed zmianą demonstracji?':
        'Changes exist only in memory. Save the profile before switching demos?',
    'Niepoprawne dane': 'Invalid input',
    'Niepoprawna liczba prób': 'Invalid trial count',
    'Przywróć': 'Restore',
    'Przywrócić oba bloki (lub pojedynczy YAML) do konfiguracji źródłowej w pamięci?\n'
    'Zapisany profil na dysku pozostanie do ponownego zapisu.':
        'Restore both blocks (or the single YAML) to the original configuration in memory?\n'
        'The saved profile on disk will remain until it is overwritten.',
    'Błąd': 'Error',
    'Eksport kopii YAML': 'Export YAML copy',
    'Wszystkie': 'All files',
    'Ochrona źródła': 'Source protection',
    'Nie można nadpisać oryginalnej konfiguracji demo.': 'Cannot overwrite the original demo configuration.',
    'Błąd eksportu': 'Export error',
    'Brak danych': 'Missing data',
    'Wskaż katalog repozytorium dem, potem kliknij Wczytaj repo.':
        'Select a demo repository directory, then click Load repository.',
    'Kontrola konfiguracji': 'Configuration validation',
    'Plan uruchomienia (nie wykonuje)': 'Launch plan (does not execute)',
    'Podgląd': 'Preview',
    'Katalog obrazów': 'Image directory',
    'Model bbox': 'Bounding box model',
    'Plik danych CSV': 'CSV data file',
    'Kolumna etykiet': 'Label column',
    'Kolumna tekstu': 'Text column',
    'Wysokość fontu': 'Font height',
    'Zawijanie tekstu (0–1)': 'Text wrapping (0–1)',
    'Kolumna klas': 'Class column',
    'Katalog wyników': 'Output directory',
    'Nazwa monitora': 'Monitor name',
    'Rozdzielczość (X, Y)': 'Resolution (X, Y)',
    'Szerokość fizyczna (cm)': 'Physical width (cm)',
    'Odległość od ekranu (cm)': 'Viewing distance (cm)',
    'Numer ekranu (od 0)': 'Display index (from 0)',
    'Rozmiar przycisku (X, Y)': 'Button size (X, Y)',
    'Margines przycisków': 'Button margin',
    'Kolor przycisków': 'Button color',
    'Kolor tekstu przycisków': 'Button text color',
    'Rozmiar tekstu': 'Text size',
    'Rozmiar fixation dot': 'Fixation dot size',
    'Kolor fixation dot': 'Fixation dot color',
    'Obszar AOE (X, Y)': 'AOE area (X, Y)',
    'Demo root': 'Demo root',
    'Upstream': 'Upstream',
    'Python 3.10': 'Python 3.10',
    'Bez gaze: odpowiedzi myszą pozostają dostępne. ioHub YAML nadal będzie wymagany przez upstream.':
        'No gaze: mouse responses remain available. Upstream still requires the ioHub YAML file.',
    'MouseGaze: trzymaj PRAWY przycisk, aby symulować gaze; puść przed LEWYM kliknięciem odpowiedzi.':
        'MouseGaze: hold the RIGHT button to simulate gaze; release before LEFT-clicking an answer.',
    'Tobii: wymagane urządzenie i jego własny plik ioHub. Połączenie nie jest jeszcze testowane.':
        'Tobii: a physical device and its ioHub file are required. The connection is not tested yet.',
    'Automatyczny układ: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Start dem: następny etap.':
        'Automatic layout: tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}. Demo launch: future stage.',
    'Wykryto ścieżki na podstawie położenia folderu pytracker-gui; sprawdź układ i zapisz.':
        'Detected paths from the pytracker-gui folder location; validate layout and save.',
    'Repozytoria: niekompletny układ. Ścieżek nie zapisano.':
        'Repositories: incomplete layout. Paths were not saved.',
    'Zapisano ścieżki aplikacji (bez modyfikacji repozytoriów).':
        'Application paths saved (repositories unchanged).',
    'Sprawdzanie interpretera…': 'Checking interpreter…',
    'Python: błąd diagnostyki': 'Python: diagnostics error',
    'Python: wykryta wersja inna niż 3.10': 'Python: detected version is not 3.10',
    'Python 3.10: wykryty. Test runtime wymaga środowiska badawczego.':
        'Python 3.10 detected. Runtime testing requires the research environment.',
    'Załadowano profil': 'Profile loaded',
    ' — ŹRÓDŁO ZMIENIONE: sprawdź ustawienia!': ' — SOURCE CHANGED: check settings!',
    'Wczytano konfigurację źródłową; modyfikacje zapisuj wyłącznie w profilu.':
        'Source configuration loaded; save modifications only in a profile.',
    'Brak źródła YAML — wskaż demo root i kliknij Wczytaj repo':
        'YAML source missing — set demo root and click Load repository',
    'Zastosowano zmiany w pamięci. Użyj „Zapisz profil”, aby utrwalić je na dysku.':
        'Changes applied in memory. Use “Save profile” to write them to disk.',
    'Zapisano profil: ': 'Profile saved: ',
    'Przywrócono ustawienia źródłowe W PAMIĘCI. Zapisz profil, aby je utrwalić.':
        'Source settings restored IN MEMORY. Save the profile to persist them.',
    'Wyeksportowano kopię: ': 'Exported copy: ',
    'Tobii: brak wskazanego pliku ioHub YAML': 'Tobii: ioHub YAML file is missing',
    'MouseGaze: plik ioHub YAML nie został wskazany/nie istnieje (wymagany do startu)':
        'MouseGaze: ioHub YAML file not set or missing (required to launch)',
    'NO_GAZE: upstream nadal odczytuje plik ioHub YAML; należy wskazać istniejący przed startem':
        'NO_GAZE: upstream still reads the ioHub YAML; select an existing file before launch',
    'Voice: obsługa tego trybu w adapterach nie została zweryfikowana':
        'Voice: support in demo adapters has not been validated',
    'Raw data: obsługa trybu w adapterach nie została zweryfikowana':
        'Raw data: adapter support has not been validated',
    'PRE-FLIGHT STATYCZNY · ': 'STATIC PREFLIGHT · ',
    'brak testów runtime/hardware': 'no runtime/hardware tests',
    'Walidacja statyczna: ': 'Static validation: ',
    '. Runtime: NOT RUN.': '. Runtime: NOT RUN.',
    'Dema': 'Demos',
    'Warianty': 'Variants',
    'POLSKI': 'POLISH',
    'modalność: ': 'modality: ',
    'backend: ': 'backend: ',
    '3 fotografie · klasyfikacja obrazów': '3 photos · image classification',
    '12 zadań · rozmieszczenie informacji': '12 tasks · information layout',
    '12 zadań · polska wersja': '12 tasks · Polish version',
    'Dwa bloki uruchamiane kolejno: machine (9), PV (9)':
        'Two sequential blocks: machine (9), PV (9)',
    '12 zadań · wyszukiwanie informacji': '12 tasks · information search',
    '12 obrazów · klasyfikacja semantyczna': '12 images · semantic classification',
}

# Translate existing validation findings without changing the validation model.
FINDING_EN = {
    'Brak mapy dataset': 'Missing dataset mapping',
    'Dataset musi zawierać dokładnie jedną aktywną modalność': 'Dataset must contain exactly one active modality',
    'CSV: nagłówek i wskazane kolumny są poprawne': 'CSV: header and selected columns are valid',
    'display.monitor.resolution: wymagane dwie dodatnie liczby całkowite': 'display.monitor.resolution: two positive integers are required',
    'display.monitor.display_number: liczba całkowita >= 0': 'display.monitor.display_number: integer >= 0 required',
    'display.gui.button.size: dwie dodatnie liczby': 'display.gui.button.size: two positive numbers required',
    'display.gui.aoe: dwie dodatnie liczby': 'display.gui.aoe: two positive numbers required',
    'instructions.intro/outro: wymagane listy tekstów': 'instructions.intro/outro: text lists required',
    'Brak output.folder': 'Missing output.folder',
    'Output: możliwe utworzenie katalogu (nie wykonywano zapisu)': 'Output: destination directory can be created (no files were written)',
    'Struktura YAML i kontrolowane pola: PASS (statycznie)': 'YAML structure and checked fields: PASS (static)',
    'Nie wykonano walidacji runtime PsychoPy/ioHub ani urządzenia Tobii.': 'PsychoPy/ioHub runtime and Tobii hardware were not tested.',
    'Katalog repozytorium dem nie istnieje': 'Demo repository directory does not exist',
    'display.monitor.width: liczba dodatnia': 'display.monitor.width: positive number required',
    'display.monitor.distance: liczba dodatnia': 'display.monitor.distance: positive number required',
    'Brak display.monitor': 'Missing display.monitor',
    'Brak display.gui.button': 'Missing display.gui.button',
}
FINDING_PREFIX_EN = {
    'Nie znaleziono oryginalnego tobii-pytracker ': 'Original tobii-pytracker not found ',
    'Repo demonstracji musi być w ': 'Demo repository must be located at ',
    'Nie znaleziono repo mszac/tobii-pytracker-demo ': 'mszac/tobii-pytracker-demo repository not found ',
    'Brak konfiguracji [': 'Missing configuration [',
    'Brak YAML ': 'Missing YAML ',
    'Demo wymaga modalności ': 'Demo requires modality ',
    'Niepoprawna sekcja dataset.': 'Invalid dataset section.',
    'Brak dataset.': 'Missing dataset.',
    'Brak katalogu obrazów: ': 'Missing image directory: ',
    'Katalog nie zawiera plików obrazów: ': 'Directory contains no image files: ',
    'Znaleziono obrazy: ': 'Images found: ',
    'Brak pliku danych: ': 'Missing data file: ',
    'Brak kolumny CSV: ': 'Missing CSV column: ',
    'Odczyt CSV: ': 'CSV read error: ',
    'Output wskazuje plik: ': 'Output points to a file: ',
    'Katalog wyników nie ma zapisywalnego katalogu nadrzędnego: ': 'No writable parent directory for output: ',
    'Nie znaleziono tools/run-demo.sh; sprawdź katalog repozytorium dem':
        'tools/run-demo.sh not found; check demo repository path',
}


def translate(text: str, language: str = 'pl') -> str:
    if language != 'en':
        return text
    if text in UI_EN:
        return UI_EN[text]
    if ': ' in text:
        field, detail = text.split(': ', 1)
        if detail in ('wymagana liczba całkowita', 'podaj dwie liczby oddzielone przecinkiem') or detail.startswith('dozwolone: '):
            suffix = {'wymagana liczba całkowita': 'integer required',
                      'podaj dwie liczby oddzielone przecinkiem': 'enter two comma-separated integers'}.get(detail, 'allowed: ' + detail[10:])
            return UI_EN.get(field, field) + ': ' + suffix
    if text in FINDING_EN:
        return FINDING_EN[text]
    for source, translation in FINDING_PREFIX_EN.items():
        if text.startswith(source):
            result = translation + text[len(source):]
            return result.replace(' (otrzymano: ', ' (received: ').replace('), znaleziono ', '), found ')
    return text

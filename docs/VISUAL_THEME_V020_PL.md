# pytracker-gui v0.2.0 — ciemny interfejs z pomarańczowymi akcentami

## Zakres
Wyłącznie wygląd istniejącego GUI v0.1.9, bez zmian w funkcjach.
Zachowano układ: nawigacja główna Eksperyment / Logi / Diagnostyka / Statystyki,
dotychczasowe zakładki konfiguracji, wszystkie pola, widoczne opcje, edycję YAML,
dymki, okno logu, przyciski Start/Stop i ścieżki projektów.

## Implementacja
- Nowy `pytracker_gui/theme.py` ustawia jeden statyczny motyw `ttk` na bazie dostępnego
  w Tk `clam`. Tło: ciemny grafit; powierzchnie: ciemne szarości; tekst: biały i jasnoszary;
  akcent aktywnych zakładek, zaznaczeń i głównych akcji: pomarańczowy.
- `tk.Listbox`, `ScrolledText` (YAML, instrukcje, raporty, okno Experiment log)
  oraz dymki `InfoPopover` używają spójnej ciemnej palety. Niebieskie ikony `i`
  pozostawiono jako mały, czytelny znacznik informacji.
- Ikony nawigacji, zakładek i najważniejszych przycisków są małymi obrazami PNG,
  wczytywanymi i pamiętanymi **raz na instancję głównego okna**. Nie dodano
  nowych zależności runtime; pakiety obrazów są dostarczone w `pytracker_gui/assets/`.
- Domyślna wielkość okna dostosowuje się jednorazowo do dostępnego ekranu, do
  maksimum 1300 × 960. Ustawienia minimalne i możliwość zmiany rozmiaru są zachowane.
- Trzy dodatkowe ekrany w dalszym ciągu tworzą się leniwie, tylko po wybraniu.
  Brak animacji, zewnętrznego silnika renderowania, procesów, wątków lub timerów.
- Pasek tytułowy systemu Windows jest zarządzany przez system, więc nie obiecujemy
  pełnego dopasowania dekoracji systemowych do makiety; komponenty aplikacji są ciemne.

## Niezmienione kontrakty
`PytrackerGUI` pozostaje właścicielem profili, YAML, procesu badawczego i okna logów.
`AppShell` odpowiada jedynie za nawigację. Bez zmian w `ExperimentRunner`, adapterach,
źródłach repozytoriów, `ProjectStore`, strukturze `projects/.../experiments`,
plikach konfiguracji, opcjach gaze/voice/raw ani wynikach w `output.folder`.
Język polski i angielski działa jak wcześniej; nie dodano wyboru motywu.

## Walidacja i ograniczenia
Lokalnie: Linux/Xvfb, Python 3.13, 92/92 testy PASS (87 odziedziczonych + 5 wizualnych).
Sprawdzono kolory, wielokrotne użycie ikon, przełączanie modułów, zachowanie niezapisanej
edycji YAML i tłumaczenia. Zrzut rzeczywistego GUI: `docs/images/v020-dark-orange-tk-preview.png`.
Windows 10/11, różne skale DPI i rzeczywisty runtime PsychoPy/Tobii nadal wymagają
weryfikacji użytkownika. Motyw `clam` zapewnia wygląd spójny, ale nie pikselową kopię
statycznej makiety (np. zaokrąglone rogi zależą od możliwości natywnego Tk).

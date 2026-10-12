# Schemat GUI — lekki interfejs desktopowy

## Nawigacja główna (docelowa)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ pytracker-gui    [Projekt: badanie_001 ▼]         [Środowisko: GOTOWE]     │
├─────────────────┬───────────────────────────────────────────────────────────┤
│ START           │ Projekt: nazwa / opis / aktywny profil                  │
│ EKSPERYMENTY    │ [NOWY] [OTWÓRZ] [DUPLIKUJ] [URUCHOM]                   │
│ MATERIAŁY       │ Ostatnia walidacja: PASS / WARN / FAIL                  │
│ KONFIGURACJA    │ Ostatnia sesja: stan / folder danych                    │
│ URZĄDZENIE      │                                                           │
│ SESJE / WYNIKI  │                 [Podgląd planu i konfiguracji]          │
│ DIAGNOSTYKA     │                                                           │
│ USTAWIENIA      │                                                           │
├─────────────────┴───────────────────────────────────────────────────────────┤
│ Status: GOTOWE   Python 3.10  | backend native  | brak aktywnej sesji     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Widoki i odpowiedzialność
- **Start:** preflight (Python/repo/urządzenie), ostatni projekt i prosty duży URUCHOM.
- **Eksperymenty:** lista demo i własnych projektów, szablony image/text/time_series, status `DIRECT`/`ADAPTER`.
- **Nowy eksperyment:** kreator 1) typ danych 2) import 3) klasy/kolumny 4) monitor/GUI 5) tracker 6) wynik 7) walidacja i zapis.
- **Materiały:** pliki CSV, foldery zdjęć, liczba bodźców, błędy importu/kolumn, bez domyślnego skanowania całego dysku.
- **Konfiguracja:** zakładki Podstawowe, Wyświetlanie, Instrukcje, Zbieranie danych, Zaawansowane (zależne od capabilities).
- **Urządzenie:** wybór znanego profilu YAML, weryfikacja dostępności, MouseGaze vs hardware, kalibracja przez upstream po potwierdzeniu.
- **Sesje/Wyniki:** status sesji, walidator, output/run manifest, link do folderu, uruchomienie notebooka jako akcja zewnętrzna.
- **Diagnostyka:** czytelny check-list i surowe logi, eksport zanonimizowanego raportu środowiska.
- **Ustawienia:** ścieżka interpretera runtime, preferencje GUI, katalog projektów, preferencje monitora.

## Model stanu
`NO_ENV -> ENV_CHECK -> READY -> CONFIG_VALIDATING -> READY_TO_RUN -> STARTING -> RUNNING -> VALIDATING_OUTPUT -> COMPLETE | INCOMPLETE | FAILED`

Zatrzymanie użytkownika: `RUNNING -> STOP_REQUESTED -> CANCELLED / INTERRUPTED` z jawnym ostrzeżeniem o możliwym niepełnym zapisie. Stan `COMPLETE` tylko po PASS wymaganych walidatorów.

## Przepływ badacza
1. Wybiera interpreter runtime Python 3.10 i repozytoria → uruchamia preflight.
2. Wybiera istniejącą demonstrację lub nowy eksperyment z 3 klas dataset.
3. Importuje dane; GUI waliduje pliki i zgodność z modalnością.
4. Ustawia monitor, instrukcje, metodę eye-trackingu i parametry sesji.
5. Zapisuje projekt → przegląda snapshot konfiguracji oraz wynik walidacji.
6. Naciska **Uruchom** → GUI uruchamia odizolowany proces; experiment window staje się osobnym oknem.
7. Po zakończeniu GUI koreluje nowy folder wyników i wykonuje walidatory → pokazuje status i otwarcie danych.

## UX oszczędny obliczeniowo
Jeden tkinter/ttk root, standardowe kontrolki, nie-renderujący podgląd plików; UI event loop nie importuje PsychoPy/ML/Jupyter. Prace I/O, subprocess i odczyt logów poza wątkiem GUI z przekazywaniem wyników przez kolejkę. Nie uruchamiać ukrytych polujących co sekundę usług detekcji trackera.

---
## SUPERSEDED FOR M1 (2026-10-10)
Powyższa makieta „NOWY eksperyment” to wyłącznie historia planowania v0.0.0. Aktualny ekran M1 nie ma tworzenia eksperymentów; obowiązuje `docs/M1_UI_SCREEN_SPEC.md` z Demo/variant, config, gaze source, runtime/path setup i session.

## IMPLEMENTED v0.1.8 navigation (supersedes historic map above)
Top bar: `Eksperyment | Logi | Diagnostyka | Statystyki` (English: `Experiment | Logs | Diagnostics | Statistics`). Experiment retains the current six sub-tabs, its project selector and full launch logic. Other modules are independently instantiated lazy placeholders until later implementation. There is no scan, timer or extra background process in navigation. See `NAVIGATION_SHELL_V018_PL.md` / `NAVIGATION_SHELL_V018_EN.md`.

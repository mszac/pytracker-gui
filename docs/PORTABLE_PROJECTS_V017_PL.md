# pytracker-gui v0.1.7 — przenośne projekty i logi

## Lokalizacja i wybór projektu

W standardowej instalacji `tobii-pytracker/` ma trzy sąsiadujące katalogi: `tobii-pytracker-demo/`, `pytracker-gui/` i nowy **`projects/`**. GUI tworzy `projects/` przy pierwszym użyciu. Projekty są oddzielone od kodu `pytracker-gui`, więc wymiana katalogu aplikacji nie usuwa projektów. Nie dodawaj projektów do repo upstream, jeśli nie zamierzasz ich tam wersjonować.

Dla każdego z siedmiu wariantów demo GUI udostępnia wybór **Projekt** i przycisk **Nowy projekt…**. Domyślny projekt nazywa się jak techniczny klucz wariantu (np. `search_en`). Możesz utworzyć wiele osobnych projektów dla tego samego wariantu; przełączenie projektu wczytuje przypisany profil lub oryginalną konfigurację, jeśli profil nie był jeszcze zapisany. Nazwa projektu: 1–64 znaki ASCII (`A–Z`, `a–z`, `0–9`, `_`, `-`), pierwszy znak musi być literą lub cyfrą. Projekty są związane z jednym wariantem demo i nie mogą przejąć profilu innego wariantu.

## Przykładowa struktura

```text
tobii-pytracker/
├── tobii-pytracker-demo/          # bez zmian
├── pytracker-gui/                # bez zmian w kodzie oryginalnym
└── projects/
    └── SearchStudy/
        ├── project.json          # identyfikator projektu, przypisany wariant demo
        ├── current-settings.json # ostatnia konfiguracja użyta do startu
        ├── profiles/
        │   └── search_en/
        │       ├── profile.json
        │       └── main.yaml
        └── runs/
            └── 20261011_192210_aB9z0/
                ├── run.json
                ├── gui-settings.json
                ├── main.yaml
                ├── eyetracker.yaml
                ├── result.json
                ├── console_20261011_192245_aB9z0.log
                └── experiment_20261011_192245_aB9z0.log
```

**ID** ma dokładnie pięć znaków alfanumerycznych `A–Z`, `a–z`, `0–9`. Wielkość liter jest istotna. Nazwa katalogu wykonania zawiera czas **utworzenia** sesji, a nazwy logów zawierają czas **zapisu po zakończeniu**, z rozdzielczością jednej sekundy. Logi z tej samej sesji mają wspólny ID, niezależnie od różnic sekund między zapisami. Dodatkowe zabezpieczenie przed kolizją: katalog jest tworzony atomowo i nie jest nadpisywany.

`experiment_*.log` to kompletna zawartość okna Experiment log, łącznie z `[RUN]`, `[STATUS]`, `[PROCESS]` i `[FINAL]`. `console_*.log` zawiera surowe wyjście przechwycone przez supervisor procesu. `result.json` przechowuje status, nie pomiary. Pliki bieżących YAML i ioHub są kopiowane **przed** startem do katalogu konkretnego wykonania. GUI aktualizuje też profil projektu, dzięki czemu ostatnie ustawienia eksperymentu są ponownie dostępne.

## Lekkość i bezpieczeństwo

Podczas działania PsychoPy GUI wyświetla komunikaty w pamięci, a supervisor używa `SpooledTemporaryFile` (do 256 KiB w RAM; nadmiar w tymczasowym pliku OS). **Nie otwiera ani nie dopisuje trwałych plików logu projektu przy każdej linii wyjścia.** Po zakończeniu procesu zapisuje surowy log, a po odebraniu `[FINAL]` jednorazowo zapisuje cały log GUI. Nie dodano nowych procesów, timerów, baz danych ani zależności. Błąd zapisu logu nie kończy i nie anuluje eksperymentu; może jednak oznaczać niekompletne lokalne archiwum logów, co należy sprawdzić po sesji.

Wyniki pomiarowe oraz pliki analiz **nie są przenoszone** do `projects/`; nadal trafiają do `output.folder` z oryginalnej konfiguracji i pozostają własnością demonstracji.

## Przenoszenie na inny checkout

1. Zamknij GUI i upewnij się, że eksperyment nie jest uruchomiony.
2. Skopiuj cały `tobii-pytracker/projects/SearchStudy/` do `projects/SearchStudy/` w nowej kopii repozytorium upstream, obok nowego `pytracker-gui/` i `tobii-pytracker-demo/`.
3. Uruchom GUI, wybierz ten sam wariant demonstracji i wybierz `SearchStudy` w polu Projekt. Zapisany profil i historia logów będą dostępne.
4. Zweryfikuj interpreter Python, obecność repozytorium dem i ścieżki do zewnętrznych plików danych; na nowej maszynie mogą one wymagać ponownego wskazania. Standardowa konfiguracja ioHub z `configs/` jest przechowywana jako ścieżka względem nowej kopii upstream.

`run.json` z wcześniejszych sesji zachowuje historyczne ścieżki absolutne w celach diagnostycznych; **nie** jest manifestem uruchomieniowym do odtworzenia na innym komputerze. Przenośnymi ustawieniami do kontynuacji pracy są profile, `current-settings.json` i kopie YAML/ioHub. Wersje oryginalnych repozytoriów i lokalne zewnętrzne datasety muszą być dostępne osobno.

Dla dotychczasowych instalacji: stare profile `%LOCALAPPDATA%/pytracker-gui/profiles/<demo_key>/` są **jednorazowo kopiowane** do domyślnego projektu przy pierwszym jego otwarciu, nigdy kasowane. Historyczne wykonania `%LOCALAPPDATA%/pytracker-gui/runs/` pozostają nienaruszone; nie wykonujemy automatycznej migracji lub nadpisania tych logów.

## Zakres

Ta iteracja dotyczy wyłącznie zarządzania lokalizacją projektów, przenośnych kopii konfiguracji i zapisu logów. Działanie PsychoPy, dobór adapterów, gaze, voice/raw, walidatorów, siedem wariantów dem, edytor YAML, języki GUI i dokumentacja parametrów pozostają bez zmian. Testy wykonano w Linux/Xvfb z atrapami procesu; fizyczny Windows i Tobii wymagają odrębnego testu.

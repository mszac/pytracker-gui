# v0.2.9 — automatyczne wyświetlanie logów (PL)

## Zakres

W zakładce **Eksperyment → Uruchomienie**, obok **Pokaż logi**, znajduje się przełącznik **Automatycznie pokazuj logi**, domyślnie **włączony**. Wybrana wartość zapisywana jest jedynie w lokalnym `settings.json`; nie jest częścią projektu, YAML ani parametrów PsychoPy.

- **Włączony (domyślnie):** po rozpoczęciu uruchomienia GUI otwiera okno Experiment log, tak jak wcześniej. Podgląd pokazuje ostatnie maksymalnie 2 000 linii/256 KiB.
- **Wyłączony:** uruchomienie nie otwiera okna logów i nie aktualizuje widgetu `Text`. Proces PsychoPy, komunikaty i archiwizacja pozostają aktywne. Kliknięcie **Pokaż logi** otwiera podgląd ręcznie — w takim przypadku aktualizuje się on, dopóki użytkownik go nie zamknie. Zmiana przełącznika na OFF zamyka otwarty podgląd.
- W trakcie eksperymentu pełny log GUI pozostaje w `SpooledTemporaryFile` (256 KiB RAM, później plik tymczasowy systemu). Pełny `experiment_<czas>_<ID>.log` jest zapisywany do katalogu projektu dopiero po zakończeniu i końcowym statusie, bez obcięcia do limitu podglądu. Odrębny `console_*.log` nadal jest finalizowany przez istniejący runner.
- **Kopiuj cały log** odczytuje pełne archiwum (lub bieżący spool) wyłącznie po kliknięciu. Ze względów wydajności sam podgląd na ekranie pozostaje ograniczony.

## Ograniczenia

Przy intensywnym logowaniu nadal mogą występować koszty procesu i kolejki zdarzeń; przełącznik usuwa koszt automatycznego renderowania oraz ogranicza pamięć historii widocznej w GUI, ale nie eliminuje kosztu generowania komunikatów PsychoPy. Pełny log ekranowy wymaga odebrania statusu końcowego przez GUI. Przy wyczerpaniu miejsca na dysku zapis archiwum może się nie udać, bez zatrzymywania eksperymentu.

**Poza zakresem:** zmiany w PsychoPy, projekcie, ID uruchomienia, walidatorach, plikach pomiarowych, kolorystyce v0.2.6 i ekranie Manual.

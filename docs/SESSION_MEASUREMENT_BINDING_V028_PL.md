# v0.2.8 — jednoznaczne powiązanie ID GUI z sesją pomiarową

## Kontrakt

Każdy nowy start GUI otrzymuje dotychczasowy, rozróżniający wielkość liter, pięcioznakowy `run_id` oraz katalog `projects/<projekt>/experiments/<YYYYMMDD_HHMMSS>_<ID>/` na konfiguracje i logi. Oryginalny kod `tobii-pytracker` nadal sam tworzy folder pomiaru z datą/czasem i zapisuje w nim `data.csv` oraz powiązane pomiary.

Od v0.2.8 kopia YAML danego uruchomienia posiada `output.folder` ustawione na unikalną, wcześniej zarezerwowaną ścieżkę:

```text
<oryginalnie_wskazany_output.folder>/
  pytracker_<YYYYMMDD_HHMMSS>_<ID>_<blok>/
    <czas_sesji_utworzony_przez_upstream>/
      data.csv
      ... istniejące pliki pomiarowe ...
```

Oryginalny `output.folder` profilu i pliki źródłowe pozostają nietknięte. Dla Machine/PV rezerwowane są osobne katalogi; nazwa bloku jest częścią ścieżki. Gwarancja dotyczy **nowych** uruchomień przez GUI v0.2.8, a nie migracji starszych sesji.

## Powiązanie i walidacja

- Unikalny katalog jest tworzony wyłącznie dla tego run ID jeszcze przed startem procesu. Nie jest współdzielony z innymi uruchomieniami, a jego wcześniejsze istnienie blokuje alokację.
- Po wykonaniu bloku sprawdzamy **tylko** ten katalog. Powiązanie `data.csv` jest przyjmowane jedynie przy dokładnie jednym podkatalogu z plikiem `data.csv` (symlinki są odrzucane). Zero/wiele kandydatów oznacza brak jednoznacznego powiązania.
- Walidatory UX/Text Search/Image Semantic/Time-Series otrzymują `--session <dokładny katalog>`. Walidator Test Demo nie wspiera `--session`, dlatego otrzymuje tylko unikalny `--output-root`, zawierający jeden sprawdzony katalog — **bez wyszukiwania według czasu**.
- `run.json` zawiera `schema=2`, `run_id`, źródłowy i zarezerwowany katalog wyników. `result.json` zachowuje status, a dodatkowo zapisuje mapę `measurement_sessions` zawierającą dla każdego bloku stan `linked/unresolved`, dokładny katalog i plik `data.csv`, rozmiar albo przyczynę braku powiązania.
- Status `COLLECTION VALIDATED` może zostać przyznany tylko wtedy, gdy zwalidowano blok **i** odnaleziono jego jednoznaczne `data.csv`.
- Nie zmieniono CSV ani sposobu gromadzenia danych w silniku. Nie gwarantuje to kompletności ani poprawności biologicznych/psychofizycznych pomiarów — to oddzielny warunek walidacji danych.

## Wydajność i ograniczenia

Sprawdzenie tylko jednego małego katalogu na blok następuje po jego zakończeniu. Nie ma dodatkowych wątków, timerów ani skanowania globalnego `output.folder`. Podczas aktywnego nagrywania nie wykonujemy nowych zapisów logu powiązania. Przeniesienie wyników lub zmiana `data.csv` przez zewnętrzny program po zakończeniu może unieważnić historyczną ścieżkę w `result.json`; nie modyfikujemy danych samych pomiarów.

Bufor logów **nie jest zmieniany w v0.2.8**. Zalecany przyszły limit podglądu GUI to 256 KiB tekstu i maksymalnie 2 000 linii (pierwszy osiągnięty), przy zachowaniu pełnego logu diagnostycznego; dotychczasowy bufor `SpooledTemporaryFile` przenosi dane do systemowego temp po przekroczeniu 256 KiB.

## Test wymagany na Windows

Uruchom `Test Demo` MouseGaze, następnie UX i Time-Series. Sprawdź unikalny folder `output.folder/pytracker_<start>_<ID>_<block>/`, dokładny `data.csv` w `result.json` i `run_id` identyczny jak ID obu logów. Powtórz dwa uruchomienia bez czyszczenia wcześniejszych wyników — nie mogą korzystać z tego samego folderu.

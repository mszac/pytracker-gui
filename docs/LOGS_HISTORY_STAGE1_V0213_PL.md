# v0.2.13 — Logs: wybór projektu, uruchomienia i raport konfiguracji (etap 1)

## Cel i zakres

Zastąpiono placeholder Logs ekranem tylko do odczytu, bez uruchamiania ani modyfikowania eksperymentu. Po lewej: projekty posiadające rzeczywisty `projects/<name>/experiments/`, z liczbą zapisanych uruchomień, oraz uporządkowana malejąco lista runów. Po prawej: zwarty dashboard sześciu grup ustawień danego uruchomienia, z rozwijanymi szczegółami. Wybrana kolorystyka obejmuje tylko Logs — globalna paleta v0.2.6 jest zamrożona.

## Kontrakt danych

* Lista projektów: jednorazowy płytki odczyt podkatalogów `projects`, bez `output.folder`, CSV, PsychoPy i analiz statystycznych.
* Lista runów: wyłącznie bezpośrednie katalogi `experiments/YYYYMMDD_HHMMSS_<5-char-ID>`; stan logu ustalany po istnieniu `experiment_*.log` (kompletny), `.log.part` (niepełny) albo braku obu. Priorytet ma niepełny `.part`, gdy oba są obecne. Nie oznacza to sukcesu/błędu eksperymentu.
* Po wybraniu run: pliki `run.json`, opcjonalnie `result.json`, `gui-settings.json` oraz istniejące kopie YAML `<block>.yaml`. `result.json` udostępnia jedynie status procesu — sekcja danych pomiarowych nie jest czytana.
* Zwięzłe kategorie: identyfikacja, środowisko, uruchomienie, dane wejściowe, monitor i wygląd, konfiguracja. Głębsze parametry można otworzyć przyciskiem **Pokaż szczegóły konfiguracji**. Ponowne zwijanie, rozwijanie i przełączanie języka nie wymaga ponownego odczytu danych.
* JSON maksymalnie 512 KiB, pojedyncza kopia YAML maksymalnie 256 KiB; brak dowiązań symbolicznych dla folderów projektu, runu lub plików konfiguracji; błędy składni plików są czytelnie zgłaszane zamiast powodować niekontrolowane otwieranie danych.
* Odświeżanie odbywa się podczas wejścia do Logs i po ręcznym **Odśwież**. Brak watcherów, timerów, bazy danych, nowych procesów i wątków.

## Celowo odroczone do etapu 2

Przycisk **Log konsoli — następny etap** jest widoczny, ale nieaktywny. Żaden kod nie otwiera pełnych logów w tym wydaniu; przeglądanie `.log` i `.log.part` z bezpiecznym porcjowaniem treści zostanie dodane osobno.

## Zamrożony zakres

Nie zmieniano PsychoPy, upstream, demo repo, run/stop, przełącznika Auto-show Logs, logowania przyrostowego, 256 KiB RAM, formatów `run.json`/YAML, magazynu projektów, analizy danych, formatowania Manuala ani globalnego motywu. Kod odczytu danych pomiarowych nie został dodany. W pierwszym wydaniu do zatwierdzenia pozostaje fizyczny Windows/DPI smoke, zwłaszcza liczne uruchomienia i długie nazwy.

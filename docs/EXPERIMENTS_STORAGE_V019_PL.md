# v0.1.9 — rozdzielenie projektu i uruchomień eksperymentu

## Bieżący kontrakt katalogów

```text
tobii-pytracker/
├── tobii-pytracker-demo/
├── pytracker-gui/
└── projects/
    └── <experiment_name>/
        ├── project.json                # tożsamość projektu i wariant demonstracji
        ├── current-settings.json       # najnowszy zestaw parametrów startu
        ├── profiles/
        │   └── <demo_key>/
        │       ├── profile.json         # trwały profil do kolejnych uruchomień
        │       └── main.yaml           # lub machine.yaml i pv.yaml
        └── experiments/                # tworzone leniwie przy uruchomieniu
            ├── 20261011_194500_aB9z0/
            │   ├── run.json            # manifest i ścieżki użyte w tym wykonaniu
            │   ├── gui-settings.json   # zapis ustawień GUI z chwili startu
            │   ├── main.yaml           # kopia YAML; dla Time-Series: machine/pv
            │   ├── eyetracker.yaml      # kopia ioHub
            │   ├── result.json         # status wykonania, bez pomiarów
            │   ├── console_20261011_194530_aB9z0.log
            │   └── experiment_20261011_194531_aB9z0.log
            └── 20261011_195000_Q7mX2/
                └── ...
```

`<experiment_name>` oznacza nazwę **projektu** nadaną przez użytkownika, a nie pojedynczej sesji. Projekt zawiera konfigurację wspólną dla kolejnych wykonań. Każde wywołanie Start tworzy osobny katalog wewnątrz `experiments/`, oznaczony lokalnym czasem utworzenia (sekundy) i losowym, pięcioznakowym ID `[A-Za-z0-9]`, z rozróżnianiem wielkości liter. Katalog jest zakładany atomowo bez nadpisywania innego wykonania. Time-Series Machine i PV należą do **jednego** wykonania GUI i zachowują odrębne kopie YAML, jak poprzednio.

Kopie konfiguracji powstają **przed** uruchomieniem procesu. `console_*.log` zostaje zapisany po zamknięciu procesu potomnego, `experiment_*.log` — po odebraniu przez GUI statusu `[FINAL]`, także z `[RUN]`, `[STATUS]` i `[PROCESS]`. Każdy log ma znacznik czasu zapisu do sekundy i ID wspólny z katalogiem wykonania. Przy działającym PsychoPy nie dopisujemy plików logów projektu po każdej linii; używany jest istniejący bufor 256 KiB RAM, z awaryjnym nadmiarem w pliku tymczasowym. Wyjątek zapisu logu nie zatrzymuje eksperymentu.

**Wyniki pomiarowe** (np. CSV i analizy) pozostają w istniejącym `output.folder` z konfiguracji demo; nie są kopiowane do `projects/` ani `experiments/`. Profil i `current-settings.json` pozostają bezpośrednio w katalogu projektu, a historia konkretnych wykonań tylko w `experiments/`.

## Zasady kompatybilności

To bezpośrednia zmiana ścieżki `projects/<name>/runs/` → `projects/<name>/experiments/`. **Nie implementowano migracji ani odczytu starego `runs/`.** GUI zapisuje nowe wykonania wyłącznie w `experiments/`. Pozostałości po starych instalacjach nie są automatycznie usuwane — można je zachować jako archiwum lub przenieść ręcznie po zamknięciu GUI. Historyczne dokumenty v0.1.7/v0.1.8 opisują wcześniejszą strukturę i nie są już obowiązującym kontraktem katalogów.

Nie zmieniono kodu adapterów, uruchamiania PsychoPy, trybów gaze, buforowania logów, nazewnictwa plików, UI ani struktury projektowych profili YAML. Nie dodano nowych zależności, procesów ani timerów. Testy runtime pozostają testami z atrapami; pełne uruchomienie na Windows/Tobii wymaga osobnej walidacji.

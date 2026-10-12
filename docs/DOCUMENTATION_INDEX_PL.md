# pytracker-gui v0.2.17 — indeks dokumentacji (polski)

**Najpierw korzystaj z poniższych aktualnych dokumentów.** Angielski odpowiednik: [DOCUMENTATION_INDEX_EN.md](DOCUMENTATION_INDEX_EN.md). Starsze opisy poszczególnych wersji są zachowanymi zapisami historycznymi; mogą omawiać funkcje jeszcze wtedy niedostępne albo wcześniejsze ścieżki, takie jak `runs/`.

| Temat | Aktualna dokumentacja PL | Odpowiednik EN |
| --- | --- | --- |
| Instalacja i aktualizacja Windows / Git Bash | [README_WINDOWS_GIT_BASH_PL.md](../README_WINDOWS_GIT_BASH_PL.md) | [README_WINDOWS_GIT_BASH_EN.md](../README_WINDOWS_GIT_BASH_EN.md) |
| Obsługa GUI, nawigacja, projekty, uruchomienia | [USER_GUIDE_PL.md](USER_GUIDE_PL.md) | [USER_GUIDE_EN.md](USER_GUIDE_EN.md) |
| Rozszerzone opisy 87 parametrów | [PARAMETER_MANUAL_PL.md](PARAMETER_MANUAL_PL.md) | [PARAMETER_MANUAL_EN.md](PARAMETER_MANUAL_EN.md) |

## Dokumentacja funkcjonalności (kolejność chronologiczna)

| Funkcja | Polski | English |
| --- | --- | --- |
| Natywne uruchamianie demonstracji | [v0.1.5](NATIVE_LAUNCH_V015_PL.md) | [EN](NATIVE_LAUNCH_V015_EN.md) |
| Obowiązująca struktura `projects/*/experiments/` | [v0.1.9](EXPERIMENTS_STORAGE_V019_PL.md) | [EN](EXPERIMENTS_STORAGE_V019_EN.md) |
| Manual Index i przeglądarka upstream `.rst` | [v0.2.6](MANUAL_UPSTREAM_RST_V026_PL.md) | [EN](MANUAL_UPSTREAM_RST_V026_EN.md) |
| Powiązanie Run ID z osobnym katalogiem pomiarów | [v0.2.8](SESSION_MEASUREMENT_BINDING_V028_PL.md) | [EN](SESSION_MEASUREMENT_BINDING_V028_EN.md) |
| Przełącznik Auto-show logs | [v0.2.9](AUTO_LOG_DISPLAY_V029_PL.md) | [EN](AUTO_LOG_DISPLAY_V029_EN.md) |
| Drzewo Markdown dem i lekki podgląd Manuala | [v0.2.10](MANUAL_DEMO_TREE_V0210_PL.md) | [EN](MANUAL_DEMO_TREE_V0210_EN.md) |
| Jeden narastający dziennik `.log.part` | [v0.2.12](INCREMENTAL_SINGLE_LOG_V0212_PL.md) | [EN](INCREMENTAL_SINGLE_LOG_V0212_EN.md) |
| Historia Logs i raport ustawień | [v0.2.13](LOGS_HISTORY_STAGE1_V0213_PL.md) | [EN](LOGS_HISTORY_STAGE1_V0213_EN.md) |
| Stronicowany podgląd konsoli w Logs | [v0.2.14](LOGS_CONSOLE_VIEWER_V0214_PL.md) | [EN](LOGS_CONSOLE_VIEWER_V0214_EN.md) |
| Klasyczne przyciski, trzy ikony i regulowane panele | [v0.2.16](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_PL.md) | [EN](CLASSIC_BUTTONS_RESIZABLE_PANELS_V0216_EN.md) |
| Karta GUI Documentation i szerokość przycisków Environment | [v0.2.17](GUI_DOCUMENTATION_V0217_PL.md) | [EN](GUI_DOCUMENTATION_V0217_EN.md) |

## Ważne rozróżnienia aktualnej wersji

- **Experiment** uruchamia i zatrzymuje istniejące demonstracje PsychoPy. **Statistics** pozostaje ekranem zastępczym. **Diagnostics** nie występuje w głównym menu, ale Experiment zachowuje kontrolę Pythona i konfiguracji.
- **Manual** ma cztery działające karty: **Index** (87 parametrów), upstream **Documentation** (`.rst`) oraz **Demo Project Documentation** (`.md` pogrupowane według projektów) i **GUI Documentation** (aktualne instrukcje tego GUI w EN/PL). Link `man` w dymku otwiera Index.
- **Logs** odczytuje zapisane metadane GUI, kopie YAML i ograniczony fragment pojedynczego `experiment_*.log` lub `.log.part`. **Nie odczytuje pomiarowych CSV**; za wyniki odpowiada kod oryginalnego eksperymentu.
- **Pojedynczy dziennik narastający** od v0.2.12 zastępuje historyczne opisy dwóch plików logów. `experiments/` zastępuje `runs/`. v0.2.16 korzysta z **klasycznych przycisków v0.2.14**, a nie odrzuconego jednolitego wyglądu v0.2.15.
- Rzeczywisty Windows/HiDPI, PsychoPy i Tobii wymagają testów na sprzęcie. Historyczne ADR oraz sześć dzienników rozwoju zachowują dotychczasowe decyzje i przebieg prac; nie służą jako aktualna instrukcja użytkownika.

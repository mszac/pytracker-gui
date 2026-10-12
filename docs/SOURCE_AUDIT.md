# Audyt źródeł — 2026-10-10

## To, co rzeczywiście sprawdzono
Rozpakowano obydwa archiwa. Repo v1.17.0 zawiera 104 pliki; porównany hash archiwum jest zgodny z raportem release. Repozytorium nie zawiera oryginalnego `src/tobii_pytracker` upstream. Historia release w osobnym archiwum podaje statyczną walidację release, ale **nie** fizyczną akceptację Windows/Docker.

| Obszar | Źródło | Wniosek dla GUI |
|---|---|---|
| Środowisko | `README_TESTING.md`, `tools/native_preflight.py` | Referencyjne natywne Python 3.10, oryginalny upstream i demo w udokumentowanym układzie, import PsychoPy/ioHub wymagający sprawdzenia |
| Dostępne szablony | `examples/*/config*.yaml`, `tools/run-demo.sh` | 5 typów demonstracji / 7 wariantów startu; 9 plików YAML (licząc smoke i dwa bloki czasowe) |
| Konfiguracja eksperymentu | `config.native*.yaml` | Rozdzielone sekcje `dataset`, `display`, `output`, `instructions`; dataset modalny: `image`, `text`, `time_series` |
| Entry points | `run.sh`, `run_native*.sh`, `run_experiment.py` | Nie każda demonstracja używa identycznego CLI: niezbędna tabela adapterów/profili |
| Sesje | `validate_collection.py` | PASS uruchomienia oznacza więcej niż exit code; trzeba sprawdzić wyniki i warianty |
| Docker | `docker/compose.yaml`, `docker/run-demo.sh` | To opcjonalna osobna ścieżka, korzystająca z upstream `psychopy`, Xvfb/VNC i DEMO/DEMO_LANG |
| Analiza | `examples/*/analysis/*.ipynb` | Jupyter jest procesem/narzędziem post-hoc, nie silnikiem wewnątrz GUI |
| Historia | `_project_logs/DEVELOPMENT_REASONING_LOG.md`, `WORK_SESSION_LOG.md`, `LOGGING_POLICY.md` | Dziennik decyzji + continuity log + testy, bez prywatnego chain-of-thought |

## Zweryfikowane zestawy demonstracyjne
- Test Demo: 3 obrazy w 3 katalogach klas; upstream CLI, loop_count=3.
- UX A/B Text: CSV 12 prób, wariant EN/PL, własny `run_experiment.py` i adapter tekstowy.
- Time-Series Noise: sekwencja dwóch bloków machine i PV (po 9), odrębne konfiguracje/walidacje.
- Text Search: CSV 12 prób, EN/PL, własny `run_experiment.py` i adapter tekstowy.
- Image Semantic: 12 obrazów, 3 klasy po 4, własny adapter interleaving bez odpowiedzi `none`.
- Smoke Text: dodatkowa pomocnicza konfiguracja (4 wiersze), **nie** jest pozycją publicznego launchera.
- 9 plików YAML: 1 smoke, 1 test, 2 UX, 2 text search, 2 time series, 1 image semantic.

## Potwierdzone właściwości/ryzyka integracyjne
1. **CWD jest częścią kontraktu**: upstream pobiera ścieżki danych i folderu wynikowego z YAML bez automatycznego rebasingu do katalogu config; `cwd=demo_root` jest wymagane dla obecnych przykładów.
2. `tools/run-demo.sh` jest dyspozytorem do istniejących shell runnerów; nie jest przenośnym API Pythona. GUI Windows powinno działać bez wymaganego Git Bash przy docelowym uruchamianiu.
3. Demonstracje response-gated, MouseGaze RIGHT-hold / LEFT-answer; Docker ma odmienną warstwę wejścia — nie mieszać instrukcji.
4. Błędy wewnątrz upstream mogą być logowane bez niezerowego exit code. Wynik `COMPLETE` wymaga kontroli plików/validatora, nie tylko procesu.
5. PsychoPy może wymagać pyzmq/ujson, a zainstalowany `setuptools` ma historię konfliktu metadanych. Preflight musi podawać konkretne wyniki zamiast instalować w ciemno.
6. W analizie z 2026-09 wskazano Windows DPI/monitor mismatch, różne możliwości hardware i voice oraz niepinned upstream branch.
7. Dla headless raw/voice inny output i lifecycle niż dla PsychoPy trial runs: osobne profile uruchomieniowe.

## Poziom pewności i granice
- POTWIERDZONE lokalnie: struktura ZIP, treść skryptów i YAML, ilości prób i ścieżki, hashe archiwum.
- POTWIERDZONE w dostarczonych historycznych audytach, lecz NIE powtórzone na źródle bieżącego upstream: szczegółowa implementacja CustomConfig i ioHub, legacy package metadata.
- PUBLICZNA DOKUMENTACJA (materiał pomocniczy):
  - https://tobii-pytracker.readthedocs.io/en/latest/configuration.html
  - https://tobii-pytracker.readthedocs.io/en/latest/commandline_usage.html
  - https://tobii-pytracker.readthedocs.io/en/latest/extending.html
- NIEZWERYFIKOWANE fizycznie: Windows/Linux realny GUI i gaze, Docker/VNC, realne nowe eksperymenty, urządzenia Tobii, zapis wyników w środowisku docelowym.
- Wymagany *snapshot certification* upstream: SHA, CLI `--help`, sample config schema, executable minimal no-hardware test, rozdzielenie backendów. Nie utożsamiać publicznego main/psychopy z raz zweryfikowanym commit SHA.

# M1 — kontrola istniejących dem (aktualny, nadrzędny zakres)

**Checkpoint:** v0.0.1-upstream-demo-control-plan · 2026-10-10 · TYLKO DOKUMENTACJA.
**Pierwszy duży cel przyjęty przez użytkownika:** wybór demonstracji z repo v1.17.0, konfiguracja istniejących parametrów i ścieżek, wybór sposobu gaze, uruchomienie i kontrola wyników na Windows/Linux.
**Wymaganie supersedujące v0.0.0:** projektowanie nowych eksperymentów / import nowych materiałów jako kreator nie jest częścią M1. Dawny plan M2 „kreator” oraz dawna kolejność M3 tracker są odroczone. Nie usuwać wcześniejszych zapisków.

## Zakres M1
1. **Setup:** wskazanie oryginalnego checkoutu sbobek/tobii-pytracker (tylko runtime), repo dem (assets i adaptery) oraz osobnego interpretera Python 3.10 z aktywnymi PsychoPy/ioHub; test wersji, importów, `--help`, `git origin/ref/SHA`, rozpoznanie Windows/Linux i kontrola uprawnień/ścieżek.
2. **Katalog:** 5 demonstracji / 7 wybieralnych wariantów: test, UX EN/PL, time series jako dwa kolejne bloki machine i PV, text search EN/PL, image semantic. Dla każdej widoczne: opis, typ danych, path, domyślny output, loop count, adapter i status zgodności. `smoke_text` pozostaje wyłącznie narzędziem deweloperskim.
3. **Konfiguracja:** edytor kopii YAML dla dataset (wybór istniejących plików/katalogów, NIE twórca nowego eksperymentu), monitor, UI PsychoPy, output, intro/outro, ewentualnie custom bbox, eyetracker/ioHub. Wybór aktywnego profilu + „Reset do oryginału”, „Zapisz profil”, „Pokaż wynikowy YAML” i „Otwórz oryginalny YAML (read-only)”.
4. **Tryb gaze:** NO_GAZE / MOUSEGAZE / TOBII. Każdy ma osobną reprezentację w RunSpec i reguły konfiguracji. Domyślnie MouseGaze, jeśli zgodne z istniejącym demo; UI nie może sprowadzać tego do „włącz mysz”.
5. **Parametry runtime:** loop_count, log_level, enable_voice, raw_data, config_file, eyetracker_config_file i enable_eyetracker; CLI headless/disable_psychopy **nie jest sesją istniejącego demo**, dlatego odłożony do osobnego przyszłego trybu narzędziowego. Wszystkie checkboxy na poziomie demo MUSZĄ odpowiadać realnie przekazanym wartościom; niemożliwe w danym backendzie opcje oznaczać wyraźnie jako unsupported/blocked (nigdy cichy no-op).
6. **Uruchamianie:** jeden jawny RunSpec (Python executable, argv, cwd, env whitelist, profile config snapshot, expected outputs, validator, backend/provenance), subprocess shell=False. UI pozostaje responsywny, logi są strumieniowane i zachowywane.
7. **Wyniki:** każdy blok ma session start timestamp, resolved config, exit status, log, nowy folder wyników, walidator i gaze-quality status osobno. Nie ogłaszać sukcesu na podstawie samego kodu wyjścia.
8. **Platformy:** Windows bez obowiązkowego Bash w runtime GUI; Linux bez osobnego serwera WWW. Native-first. Docker jest odłożony, bez usuwania historycznych ustaleń.

## Twarde granice
- NIE modyfikować ani `pip install .` z demo repo: runtime authority wyłącznie oryginalne sbobek/tobii-pytracker.
- NIE kopiować silnika, dataset rendererów lub ioHub do pytracker-gui. Istniejące `tools/demo_runtime_adapters.py` mają pozostać authority dla zachowań 3 adaptowanych dem.
- NIE zapisywać zmienionych YAML na oryginalne `examples/*/config.native*.yaml`; używać osobnych kopii profili, atomowego zapisu i snapshotów sesji.
- NIE przechowywać materiałów badawczych lub wyników w logach diagnostycznych bez jawnej zgody; nie przeszukiwać automatycznie dysku.
- NIE importować PsychoPy/Tobii w procesie GUI; ciężkie biblioteki importuje tylko wskazany child Python.

## M1 — definicja ukończenia
- [ ] wszystkie 7 wariantów można wybrać, wyedytować i uruchomić natywnie na Windows i Linux; dwublokowy time series zachowuje dokładnie kolejność i niezależne outputy; brak powłoki Bash.
- [ ] wybor NO_GAZE, MOUSEGAZE, TOBII jest rzeczywiście przekazany w backendzie; no-gaze potwierdzone testem; MouseGaze z próbami; fizyczny Tobii w dwóch systemach tylko gdy dostępny, w innym razie jawny HARDWARE_BLOCKED i niewydawanie pełnego gate.
- [ ] edytor obejmuje wszystkie dokumentowane główne sekcje YAML; wspiera demo-specyficzne nieudokumentowane klucze bez utraty; round-trip kopii nie zmienia oryginałów.
- [ ] kontrola log_level, loop_count i obsługiwanych kombinacji voice/raw ma parity z realnym wywołaniem; przypadki nieobsługiwane mają jawny status.
- [ ] resolve YAML ścieżek przy cwd=demo_root działa na Windows i Linux, w tym ścieżki ze spacjami, unicode i niestandardowym output root.
- [ ] preflight, snapshot config, log procesu, walidatory danych, stan odpowiedzi i jakość gaze rozróżnione; plik wyjściowy z poprzedniej sesji nie może dać fałszywego PASS.
- [ ] niespójne zależności (brak repo, Python !=3.10, brak ioHub, błędne CSV) blokują uruchomienie z konkretnym komunikatem.
- [ ] niezmienione authority upstream/demo + minimalny footprint; kompletne logi append-only, pełne ZIP/MANIFEST + patch i fresh-extract validation.

## Wyłączone z M1
Kreator i import zupełnie nowych eksperymentów; projektowanie bodźców, klasyfikatorów, GUI eksperymentu; pełne analizy Jupyter/ML; docker/VNC; headless continuous recording; reimplementacja sprzętowego discovery lub kalibracji; pakowanie całego PsychoPy do GUI.

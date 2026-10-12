# Roadmap rozwoju pytracker-gui

Statusy: **plan**, **implementacja**, **weryfikacja sprzętowa**. Żadna z funkcji poniżej nie jest jeszcze zaimplementowana w v0.0.0-plan.

## M0 — zamrożenie kontraktu i potwierdzenie środowiska (następny krok)
- Pozyskać *exact* checkout upstream `sbobek/tobii-pytracker` i zanotować SHA, branch, help/CLI, schema, tracker YAML.
- Sprawdzić w obu OS `tkinter`/ttk, ścieżkę Python 3.10, import PsychoPy/ioHub oraz minimalny native no-hardware test.
- Zdefiniować `DemoRegistry` dla: test_demo, ux_ab_demo en/pl, time series machine+pv, text_search_demo en/pl, image_semantic_demo; zapisać komendy/cwd/walidatory.
- Utworzyć fixture fake process bez urządzenia i fixture CSV dla walidacji; kryterium: dokładna specyfikacja RunSpec i błędów.
- Gate: `M0_COMPATIBILITY_BASELINE_PASS` + SHA/komendy/stany w logach; problemy fizyczne nie maskowane.

## M1 — v0.1.0: lekki natywny launcher (MVP)
- Minimalny UI (Start, Demo, Środowisko, Uruchomienie/Logi, Wyniki).
- Jawny interpreter Python 3.10, ścieżki repozytoriów, probe import/CLI, readonly profile.
- Obsługa `subprocess` bez powłoki, jawny CWD, monitor stanu, streaming logów i bezpieczny sposób zakończenia.
- Uruchamianie demonstracji przez adaptery natywne dokładnie odpowiadające istniejącym runnerom; najpierw test_demo i jeden text, potem pozostałe; osobna semantyka dwublokowego time series.
- Zachowanie wyników i stanu walidacji, brak przenoszenia PsychoPy do GUI.
- Gate: automat fake upstream, Windows 11 native + Linux native smoke, spójne kontrole output; verify main UI responsive while experiment runs.

## M2 — v0.2.0: kreator eksperymentów i edytor parametrów
- Workspace: Nowy / Otwórz / Duplikuj / Zapisz jako.
- Kreator image/text/time_series, import materiałów i walidacja; prosty podgląd metadanych/wybranych plików.
- Edycja `dataset`, monitor/GUI, intro/outro, wyjścia, `loop_count`, część flag CLI.
- Generowanie zgodnych YAML/profilu i snapshotów per run; eksport projektu.
- Gate: 3 rzeczywiste nowe eksperymenty (każda modalność), na dwóch OS bez ręcznej edycji YAML, wyniki walidowane; round-trip save/reopen bez utraty danych.

## M3 — v0.3.0: integracja sprzętowa i praca badawcza
- Profile MouseGaze / fizyczny Tobii; wskaźniki availability, rejestracja calibration/tracker diagnostics w zakresie publicznego API.
- Opcje voice/TAP, raw gaze, headless jako odrębne tryby, konsekwentne dane/metadane.
- UI sessions i linki do notebooków; automatyczny raport QC, ostrzeżenia o brakach gaze i błędach save.
- Gate: realny Tobii na Windows i Linux (jeśli wspierany), realny MouseGaze, gaze/voice quality evidence, interrupt/recovery test.

## M4 — v0.4.0: Docker i eksperckie funkcje (opcjonalne)
- DockerAdapter z jawnym VNC i specyfiką ścieżek; start/stop po Compose, bez tła kiedy nieużywany.
- Zaawansowane custom models i zweryfikowane adaptery rozbudowanych eksperymentów, eksport harmonogramu i provenance.
- Gate: Docker Desktop/Engine real test, host volume/output, port conflicts, parity with native output.

## M5 — v1.0.0: dystrybucja
- Stabilny schemat projektów/migracje, lokalizacja PL/EN, podpisane/zweryfikowane paczki, instrukcje Windows/Linux.
- Opcjonalny instalator/portable; **nie** pakować całego PsychoPy/Tobii runtime wewnątrz lekkiego GUI. Runtime jest skonfigurowaną zależnością.
- Gate: clean-machine install/start/migrate/uninstall, dokumentacja reprodukowalnego środowiska, zgodność archiwów.

## Zakres pierwszej iteracji — cięcie realizacyjne
**Zaimplementować najpierw F01-F06** w trybie native i bez nowego edytora YAML. To umożliwi sprawdzenie najtrudniejszych problemów: wersji upstream, interpreterów, ścieżek, lifecycle i wyników, zanim dodamy formularze.

## Polityka numeracji i wydania
- v0.0.0-plan: tylko dokumentacja.
- Każda implementacja to nowa wersja (np. v0.1.0); drobne poprawki podbijają patch.
- Jeden pełny ZIP, SHA-256/MANIFEST i test świeżego rozpakowania; osobny patch wersja-do-wersji i narastające logi w środku archiwum.
- Work sessions w `logs/WORK_SESSION_LOG.md` i `logs/PROJECT_CONTINUITY_LOG.md` mają jednoznaczny next action.
- `CHANGELOG` mówi *co*, `DECISION_JOURNAL` mówi *dlaczego i na podstawie czego*, `VALIDATION` mówi *jak sprawdzono*.

---
## SUPERSEDED BY SCOPE CHANGE 2026-10-10
Sekcje M2/M3 z początku tego dokumentu pozostają historyczne: user ustanowił nowy duży cel M1 — kontrola 5 istniejących dem (7 wariantów), ścieżek, YAML i źródła gaze. Aktualne fazy A..E opisuje `M1_PHASED_IMPLEMENTATION_AND_GATES.md`. Kreator nowych eksperymentów jest odłożony PO M1. Nie interpretować wcześniejszych terminów jako aktualnej kolejności.

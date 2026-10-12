# Minimalne GUI w pierwszym dużym celu

## Makieta logiczna (Tkinter/ttk, jeden proces bez PsychoPy)

```text
┌ pytracker-gui                                         [PYTHON 3.10 ●] ┐
│  START / DEMO        KONFIGURACJA        SESJA / LOGI       USTAWIENIA │
├───────────────────────────────────────────────────────────────────────┤
│  Demo: [ TEST DEMO                         v ]  Wariant [ EN        v ] │
│  [opis]   Dataset: image   3 bodźce   Adapter: ORIGINAL CLI           │
│  Runtime: [C:\...\python.exe                              Przeglądaj] │
│  Upstream: [D:\...\tobii-pytracker                        Przeglądaj] │
│  Demo root:[D:\...\tobii-pytracker-demo                   Przeglądaj] │
│                                                                        │
│  REJESTRACJA GAZE:   ( ) Brak    (●) MouseGaze    ( ) Tobii             │
│  [ ] Voice recording      [ ] Raw gaze     Trials [3]  Log [info v]    │
│                                                                        │
│  DANE I WYNIKI       Dataset: [examples/test_demo/data       ...]      │
│                     Output: [output/test_demo              ...]       │
│  KONFIGURACJA       [Dane][Monitor][Wygląd][Instrukcje][ioHub][YAML]   │
│                                                                        │
│  Status: YAML OK  | Python OK | ioHub OK | Dataset OK                   │
│                     [SPRAWDŹ] [ZAPISZ PROFIL] [URUCHOM DEMO]           │
├───────────────────────────────────────────────────────────────────────┤
│  LOG SESJI: [ stdout/stderr ] [Otwórz folder wyników] [STOP]           │
└───────────────────────────────────────────────────────────────────────┘
```

## Zachowania kluczowe
- `Demo` wybiera jedno z 5; UX i Text Search EN/PL, time series widoczny jako jeden wybór z etapami MACHINE -> PV; odrębne config tabs dla tych dwóch bloków.
- Trzy tryby gaze jako radio-group: `NO_GAZE`, `MOUSEGAZE`, `TOBII`; zmiana profilu ioHub nie zmienia przypadkiem runtime `enable_eyetracker` bez potwierdzenia. Pokazać instrukcję RIGHT-hold/LEFT answer dla MouseGaze.
- `Konfiguracja` otwiera przyjazny edytor formularzowy; `YAML` jest podglądem/kontrolą zachowania nieznanych pól; advanced fields wymagają jawnej decyzji.
- `Sprawdź` uruchamia statyczną i child dependency walidację, nigdy eksperyment.
- `Uruchom` pokazuje podsumowanie: demo/variant, argv, resolved paths, output, gaze, liczba prób, ostrzeżenia, baseline SHAs; potem uruchamia child.
- `Stop` współpracuje z grupą procesów, pokazuje „przerwane — wyniki mogą być niekompletne”; nie usuwa danych.
- `Sesja/Logi`: log append, oznaczenie timestampów, status procesu vs danych vs gaze; przy braku gaze nie ma fałszywego gaze PASS.
- Ekran początkowy nie ma przycisku „Nowy eksperyment”; kreator odsunięty, dotychczasowa dokumentacja ma znaczenie historyczne.

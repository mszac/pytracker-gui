# Architektura pytracker-gui

## Jednoznaczne granice
`pytracker-gui` to *control plane*, nie experiment engine. Wytwarza plan i pliki YAML, waliduje dane, uruchamia **zewnętrzny** proces upstream/dostępnego adaptera, obserwuje jego status i sprawdza wyniki. Upstream pozostaje jedynym właścicielem PsychoPy, ioHub, Tobii SDK, presentation loop, gaze/voice i zapisów trial data.

```
[ Tkinter/ttk GUI ]
      | (immutable input view model, events)
[ Services / orchestration ]---[ Project store / provenance / session index ]
      |                      \--[ validators: YAML, CSV, files, display ]
[ Backend interface ]
      +----[ NativeAdapter ]-----> subprocess(Python 3.10, cwd=demo_root)
      |                               |-- upstream CLI lub audytowany demo runner
      |                               |-- PsychoPy + ioHub (osobne okno)
      |                               `-- istniejący collection validator
      `----[ DockerAdapter, od M4 ]----> docker compose -> Xvfb/VNC
      |
[ Run manifest / stdout/stderr / output inspector ] --> user output dir
```

## Proponowane moduły kodu (jeszcze NIE utworzone)
```
pytracker_gui/
  app.py                  # lifecycle Tk, tylko UI
  views/                  # dashboard, wizard, configs, run monitor
  models/                 # schema project/profile/run, validation messages
  services/preflight.py   # sprawdzanie env/path/upstream commit
  services/configs.py     # safe YAML, value validation, generation
  services/datasets.py    # CSV/folder counts and shape; bounded I/O
  services/sessions.py    # session state machine, manifest, output matcher
  services/validation.py  # typed validators + historical demo validators
  adapters/native.py      # command spec / subprocess and streaming logs
  adapters/docker.py      # optional later
  adapters/demo_registry.py # known demo entrypoint/validation recipes
  storage/projects.py     # atomic save, schema version, migrations
  storage/logging.py      # runtime logs / diagnostic redaction
  tests/                  # unit, integration, fake upstream, OS smoke
```

## Rekomendowana technologia
- GUI: **Tkinter + ttk** (stdlib, minimalny narzut, brak Chromium/web server/Qt/PsychoPy w procesie GUI); Linux wymaga dostępnego Tcl/Tk (`python3-tk` zależnie od dystrybucji). Decyzja w ADR-0002 jest *proponowana* i wymaga krótkiego OS smoke.
- GUI-interpreter: może być niezależny od runtime. Runtime Python 3.10 wskazany jawną ścieżką, bez zależności od aktywnej powłoki lub `conda activate`.
- YAML: mała zależność `PyYAML` w wersjonowanej instalacji GUI lub wydzielonym workerze; bezpieczne parsowanie. Dla istniejących profili niebezpieczna utrata komentarzy/nieznanych kluczy: domyślnie zapis nowego wygenerowanego YAML, a nie nadpisywanie pliku źródłowego.
- Uruchomienie: `subprocess.Popen([...], cwd=..., env=...)` z **listą argumentów, shell=False**. Warianty EN/PL i dwublokowe są jawnie mapowane w demo registry.
- Metadane: JSON w projekcie GUI (stdlib), generowany YAML przekazywany do upstream; wersjonowanie schematu i migracji.
- IO: worker thread/process tylko do nieblokującej komunikacji; `queue.Queue` do wątku UI. Brak aktywnego importu ciężkich modeli do GUI.

## Założenia wykonawcze
1. Preflight identyfikuje `upstream_root`, `demo_root`, `runtime_python`, wersje i git SHA. Gdy brak repo albo niezgodna konfiguracja: FAIL, z czytelnym remedium; GUI nadal się otwiera.
2. W domyślnym trybie demo `cwd=demo_root`. Nie ufać katalogowi startu GUI ani `Path(config).parent`.
3. Cross-platform adapters nie uzależniają uruchomienia na Windows od `bash`; uruchamiają sprawdzone entrypoints Pythona i walidatory, zachowując semantykę oryginalnych wrapperów (w tym timestamp, bloki, unknown-label, return code).
4. `run-demo.sh`/`run.sh` pozostają wzorcem do testów równoważności oraz opcjonalnym trybem diagnostycznym, a nie nowym silnikiem.
5. Instancja sesji jest niemutowalna: z kopią wygenerowanego config, hashami datasetu/manifestu, wybranym profilem tracker, snapshotem komend i commita upstream. Edycja projektu po starcie nie zmienia uruchomienia.
6. Najpierw exit status + expected output + validator + log inspection; przypadek niejednoznacznego folderu output daje `INCOMPLETE/AMBIGUOUS`, nigdy automatyczne PASS.
7. GUI nie interpretuje skryptów z importowanego projektu i nie dodaje dowolnych flag ani ścieżek do `PYTHONPATH`. Custom adapters/plugins są zaawansowanym trybem z jawną zgodą.
8. Bez uprzedniego testu nie wymuszać zakończenia PsychoPy SIGTERM/KILL; operator najpierw zamyka sesję upstream, potem świadomie wymusza stop.

## Przyszła separacja backendów
`Backend.run(RunSpec) -> SessionHandle`; `Backend.preflight(Profile) -> CapabilityReport`; `OutputInspector.inspect(RunManifest) -> CollectionReport`. DockerAdapter ma tę samą warstwę kontroli, ale inny parser environment i tracker/control semantics. Te interfejsy są planem, nie implementacją.

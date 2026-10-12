# v0.1.4 — parytet dokumentacji PL/EN / bilingual documentation parity

## Polski

**Cel:** zapewnić równorzędną dokumentację bieżących funkcji bez zmiany GUI lub uruchamiania eksperymentów. Oba katalogi parametrów korzystają z identycznych, stabilnych kluczy (87/87). Polski `parameter_help.json` przechowuje klucz/status/źródło/grupę oraz opisy PL, a `parameter_help_en.json` przechowuje odpowiadające tytuły, krótkie i pełne opisy EN. Nie tłumaczymy nazw YAML, CLI ani wartości enum.

**Przyjęte definicje:** gaze to próbki pozycji spojrzenia, nie kliknięcia myszą; `NO_GAZE` nie wyłącza odpowiedzi myszą. `AOE` to obszar układu eksperymentu, a AOI oznacza regiony bodźca. „Zapis profilu” nie oznacza „uruchomienia demo”, „sprawdzenie konfiguracji” jest statyczne, a `gui` jako status oznacza dostępność w edytorze, nie skuteczne przesłanie ustawień do runtime. Opisy ustawień ioHub nie stanowią deklaracji ich edycji ani zgodności z fizycznym urządzeniem.

**Dokumenty bieżące:** dwie instalacje Git Bash, dwa przewodniki użytkownika, dwa manuale 87 parametrów i dwa indeksy dokumentacji. Generowanie `tools/render_parameter_manual.py` aktualizuje **oba** manuale; `--check` sprawdza synchronizację obu wersji. W GUI wyświetlane są tylko nazwy plików obu manuali; nie wdrażamy linka ani okna pełnego manuala. Historyczne ADR-y i logi nie są tłumaczone hurtowo i pozostają narastające.

## English

**Goal:** provide equivalent documentation for the current feature set without changing GUI behavior or enabling experiment launch. Both parameter catalogs share the same 87 stable keys. The Polish `parameter_help.json` is the authoritative registry of key, status, source, and group, with PL descriptions; `parameter_help_en.json` supplies corresponding English titles, short help, and extended help. YAML keys, CLI flags, and enum values are not translated.

**Terminology:** gaze samples represent eye position, not ordinary mouse button responses; `NO_GAZE` does not disable mouse responses. `AOE` refers to the experiment layout area, whereas an AOI is a stimulus-specific region. “Save profile” is not “launch demo”, “validate configuration” is static, and a `gui` availability tag does not imply that an option reaches a running experiment. Descriptions of ioHub internals are reference material, not evidence of in-app editing or physical device compatibility.

**Current paired artifacts:** two Git Bash installation guides, two user guides, two 87-entry parameter manuals, and two documentation indexes. Running `tools/render_parameter_manual.py` regenerates **both** manuals; `--check` validates both outputs. The GUI informational label names both manual files; no full-manual hyperlink or viewer has been added. Historical ADRs and development logs remain cumulative and are not retroactively translated.

## Automated parity gates

1. Both catalogs have exactly the same 87 unique keys; all English entries include title, short, and long descriptions.
2. Each short description is one meaningful sentence; each extended description has multiple sentences. Every record shares the same original status and source.
3. Both manuals are generated deterministically from the catalogs; unchanged YAML identifiers and all 5 status categories are present in each.
4. Both user guides identify seven variants, eight YAML files, three gaze modes, read-only original sources, static preflight, and no GUI demo execution.
5. Original application modules other than release identification, documentation lookups, and localized help data remain byte-identical to v0.1.3. Existing profile and YAML formats are not migrated.
6. Windows Python 3.10/PsychoPy/ioHub and physical Tobii remain separate acceptance gates: a documentation test cannot substitute for them.

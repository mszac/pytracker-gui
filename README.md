# pytracker-gui v0.2.17 — current documentation / aktualna dokumentacja

**Current functional release / Aktualna wersja funkcjonalna: v0.2.17.** Only the four Environment-button widths and the new read-only Manual → GUI Documentation tab differ from v0.2.16. / Zmiany wobec v0.2.16 dotyczą wyłącznie szerokości czterech przycisków Environment i nowej karty Manual → GUI Documentation.

**EN:** [User guide](docs/USER_GUIDE_EN.md) · [Windows / Git Bash setup](README_WINDOWS_GIT_BASH_EN.md) · [Documentation index](docs/DOCUMENTATION_INDEX_EN.md). **PL:** [Przewodnik](docs/USER_GUIDE_PL.md) · [Instalacja Windows / Git Bash](README_WINDOWS_GIT_BASH_PL.md) · [Indeks dokumentacji](docs/DOCUMENTATION_INDEX_PL.md).

The GUI launches existing demos, stores run configuration snapshots and **one incremental console journal** (`.log.part` / `.log`), and provides a read-only Logs history, four-tab Manual, and native resizable panel separators. **Original experiment code owns measurement data.** v0.2.16 retains the classic v0.2.14 button appearance; the v0.2.15 uniform-button design was rejected. / GUI uruchamia gotowe dema, zapisuje konfigurację uruchomień i **jeden narastający log konsoli**, udostępnia historię Logs, cztery karty Manuala i przesuwane granice paneli. **Za pomiary odpowiada kod oryginalnego eksperymentu.** Wygląd przycisków pochodzi z v0.2.14, bez odrzuconych zmian v0.2.15.

**Historical project/release notes follow below; earlier “not implemented” claims apply to their original versions only. / Poniżej zachowano historię rozwoju; dawne opisy brakujących funkcji dotyczą wyłącznie starszych wersji.**

---

# pytracker-gui v0.2.9 — Auto-show logs / Automatyczne logi

**PL:** Nowy przełącznik **Automatycznie pokazuj logi** w zakładce Uruchomienie domyślnie zachowuje poprzednie działanie. Wyłączenie zapobiega automatycznemu otwieraniu i aktualizowaniu okna logów; zapis końcowy pozostaje pełny. [Instrukcja](docs/AUTO_LOG_DISPLAY_V029_PL.md).

**EN:** Default-ON **Auto-show logs** switch next to Show Logs; OFF avoids automatic log-window rendering while full final run logs are still archived. [Guide](docs/AUTO_LOG_DISPLAY_V029_EN.md).

---

# pytracker-gui — current release / aktualna wersja: v0.1.8

**PL:** Dodano lekką górną nawigację między niezależnymi ekranami **Eksperyment / Logi / Diagnostyka / Statystyki**. Ekran Eksperyment i jego sześć zakładek zachowują istniejące działanie. Pozostałe ekrany powstają dopiero po pierwszym otwarciu i na razie wyświetlają komunikaty informacyjne, bez czytania logów, diagnostyki ani obliczeń. [Opis architektury](docs/NAVIGATION_SHELL_V018_PL.md).

**EN:** Added lightweight top-level navigation: **Experiment / Logs / Diagnostics / Statistics**. The existing Experiment view and its six tabs are preserved; other screens are lazy placeholders with no background I/O or computations. [Architecture and instructions](docs/NAVIGATION_SHELL_V018_EN.md).

**Start / Uruchomienie:** `python pytracker-gui/run_gui.py --check-layout` → `python pytracker-gui/run_gui.py` in the existing Python environment. No new dependencies. Project folders remain siblings of the GUI checkout. All earlier sections below are release history.

---

# pytracker-gui — current release / aktualna wersja: v0.1.7

**PL:** Projekty i kompletne logi uruchomień znajdują się teraz pod `tobii-pytracker/projects/<projekt>/`. Każde wykonanie ma pięcioznakowy ID i pliki logów zapisane po zakończeniu sesji; profile są przenośne między checkoutami. [Instrukcja](docs/PORTABLE_PROJECTS_V017_PL.md). Pozostałe funkcje v0.1.6 pozostają bez zmian.

**EN:** Self-contained project profiles and post-run logs now live in `tobii-pytracker/projects/<project>/`; each run has a five-character case-sensitive ID. [Guide](docs/PORTABLE_PROJECTS_V017_EN.md). v0.1.6 experiment behavior is preserved.

---

# Previous release / poprzednie wydanie: v0.1.6

**Naprawa UX A/B, Text Search i Image Semantic:** bezpośrednie ładowanie adaptera z repo dem; przycisk **Kopiuj cały log** w oknie dziennika (PL/EN). Instrukcje: [PL](docs/DEMO_ADAPTER_AND_LOG_COPY_V016_PL.md) · [EN](docs/DEMO_ADAPTER_AND_LOG_COPY_V016_EN.md). Pozostałe funkcje v0.1.5 zachowane. Starsze wpisy poniżej są historyczne.

---

# Previous release / Poprzednie wydanie: v0.1.5

**PL:** [indeks dokumentacji](docs/DOCUMENTATION_INDEX_PL.md) · [instalacja Windows](README_WINDOWS_GIT_BASH_PL.md) · [przewodnik](docs/USER_GUIDE_PL.md) · [pełny manual](docs/PARAMETER_MANUAL_PL.md).

**EN:** [documentation index](docs/DOCUMENTATION_INDEX_EN.md) · [Windows installation](README_WINDOWS_GIT_BASH_EN.md) · [user guide](docs/USER_GUIDE_EN.md) · [full parameter manual](docs/PARAMETER_MANUAL_EN.md).

GUI is now a **configuration editor and native demo launcher**. PL is the default interface; EN is optional; tooltips have their own language setting. Both manuals now describe all 87 settings. The full-manual link remains deferred. For launch behavior see [PL](docs/NATIVE_LAUNCH_V015_PL.md) and [EN](docs/NATIVE_LAUNCH_V015_EN.md). Earlier README notes below are historical checkpoints.

---

**Aktualna wersja: v0.1.1 — instalacja przez `docs/INSTALL_AND_USE_V011_GIT_BASH_WINDOWS.md`; wymagany układ `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}`. Uruchamianie eksperymentów z GUI jeszcze nie działa.**

# pytracker-gui — projekt koncepcyjny

**Status:** v0.0.0-plan, 2026-10-10. TYLKO plan/dokumentacja. Brak wykonywalnego GUI i brak zmian w `tobii-pytracker` lub `tobii-pytracker-demo`.

## Cel
Lekki desktopowy launcher i edytor konfiguracji dla eksperymentów `tobii-pytracker` na Windows i Linux. Docelowo pozwala stworzyć eksperyment z dostarczonych materiałów, zwalidować konfigurację, uruchomić silnik PsychoPy/ioHub w osobnym procesie oraz zebrać diagnostykę i wyniki. Nie zastępuje engine ani notebooków.

## Sprawdzone wejście
- `tobii-pytracker-demo v1.17.0-release-readiness-REPO.zip` — 104 pliki repozytorium.
- `...PROJECT-LOGS-AND-HELPERS.zip` — historia audytów, ryzyk i decyzji wcześniejszego projektu; nie należy jej kopiować jako historii zmian nowego GUI.
- Weryfikowany repo ZIP SHA-256: `f0c383851426437124c04aa629ab3ea617147740685307a3f662ab41bab48465`.
- Nie dostarczono pełnego, przypiętego do SHA source tree upstream (`sbobek/tobii-pytracker`). Kontrakt musi być zweryfikowany przeciw docelowemu commitowi przed generowaniem uruchamialnego GUI.

## Nawigacja
1. `docs/SOURCE_AUDIT.md` — konkretne fakty i granice analizy archiwów.
2. `docs/FEATURE_CATALOG.md` — wykaz funkcji, priorytety, powiązania z upstream.
3. `docs/UI_MAP.md` — mapa ekranów i przepływ użytkownika.
4. `docs/ARCHITECTURE.md` — izolacja procesów, adaptery, profile i ścieżki.
5. `docs/EXPERIMENT_CONTRACT.md` — modele eksperymentu, dane wejściowe/wyjściowe.
6. `docs/ROADMAP.md` — etapy, definicje gotowości i kolejność.
7. `docs/VALIDATION.md` — sprawdzalna macierz Windows/Linux.
8. `docs/SECURITY_AND_DATA.md` — bezpieczeństwo, prywatność, odtwarzalność.
9. `docs/OPEN_QUESTIONS.md` — decyzje do weryfikacji, bez blokowania prac projektowych.
10. `adr/` — proponowane decyzje architektoniczne.
11. `logs/` — append-only stan, dziennik, problemy i historia.

## Najbliższy krok
Rozpocząć implementację v0.1.0 (minimalny launcher native dla Windows/Linux) dopiero po wykonaniu gate P0 w `docs/ROADMAP.md`. Każda wersja ma wnosić ZIP zawierający pełny aktualny projekt, narastające logi, testy i odrębny patch do poprzedniej zaakceptowanej wersji.

## CURRENT SCOPE NOTICE — v0.0.1-upstream-demo-control-plan (2026-10-10)
Plan v0.0.0 powyżej pozostaje historią. Obecnie obowiązuje **M1 kontrola istniejących dem i config**, bez kreatora nowych eksperymentów; czytaj w pierwszej kolejności `docs/PROJECT_CURRENT_SCOPE.md`, `docs/M1_SCOPE_AND_ACCEPTANCE.md`, `docs/DEMO_LAUNCH_MATRIX.md`, `docs/CONFIG_CONTROL_MATRIX.md`, `docs/M1_PHASED_IMPLEMENTATION_AND_GATES.md`. Funkcjonalności projektowania nowych eksperymentów opisane w starszej roadmapie zostały odroczone, nie zaimplementowane.

## CURRENT IMPLEMENTATION — v0.1.0-ui-config-prototype (2026-10-10)

**First runnable GUI checkpoint.** Current v0.0.1 plan is preserved above; newer implementation/scope status is in `docs/UI_PROTOTYPE_V010.md` and `docs/INSTALL_AND_USE_V010.md`.

To start: extract the demo repository separately, install `ruamel.yaml` using `requirements-gui.txt`, then run `python run_gui.py`. Windows and Linux have the same Tk source. User-selected demo root is needed; no upstream/experiment contents are bundled.

What works: seven variants, two time-series blocks, main YAML form/raw editor, comment/unknown-field preserving write via `ruamel.yaml`, dataset/monitor/appearance/instructions, 3 gaze mode selectors, ioHub YAML path, Python interpreter probe, profile save/load, reset/export, static validation, dry-run plan preview.

**Not implemented:** actual experiment launch/stop, physical gaze recording, editor of ioHub YAML internals, voice/raw integration, native bridge. The original 3 adapters still hardcode key runtime flags, so start is deliberately unavailable. Windows and Tobii still need physical testing. Source README claim above about code absent is historical and only applies to v0.0.0/v0.0.1.

## CURRENT RELEASE — v0.1.1 nested-repository-layout (2026-10-11)

Use **`docs/INSTALL_AND_USE_V011_GIT_BASH_WINDOWS.md`** for the current installation, not the older v0.1.0 sibling setup. Canonical structure is `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}`; the demo Git URL is `https://github.com/mszac/tobii-pytracker-demo.git`. Install our ZIP directly to `tobii-pytracker/` (it already wraps the `pytracker-gui/` directory). Run `python pytracker-gui/run_gui.py --check-layout`, then `python pytracker-gui/run_gui.py`. Windows/Linux GUI code is cross-platform, but Windows and actual experiments are pending physical tests. No GUI start/stop exists yet; do not mistake the previewed manual original shell command for execution of a GUI profile. Earlier sections remain as historical record.

## CURRENT RELEASE — v0.1.2 parameter help and manual (2026-10-11)

For Windows/Git Bash setup use the new **`README_WINDOWS_GIT_BASH_EN.md`**. The previous v0.1.1 setup guide is preserved for historical reproducibility. All editable GUI parameters and additional original upstream/MouseGaze/Tobii settings now have short and extended Polish descriptions in `pytracker_gui/parameter_help.json`; the full reference is `docs/PARAMETER_MANUAL_PL.md`. Blue circular `i` controls show the short descriptions on click; **no manual hyperlink is present or planned for activation in this release**. Original experiments still cannot be started from the GUI; Windows/Tobii hardware validation remains outstanding.

## CURRENT RELEASE — v0.1.3 Polish/English GUI (2026-10-11)

Domyślny interfejs i pełny manual **pozostają polskie**. Dodano niezależne przełączniki języka GUI i dymków `Polski` / `English` (angielski obejmuje 87 krótkich podpowiedzi, nie pełny manual). Przełączenie zachowuje bieżące poprawne wartości edytora, a język zapamiętywany jest w prywatnym `settings.json` bez wpływu na profile YAML i oryginalne repozytoria. Angielski manual oraz otwieranie manuala z GUI pozostają odłożone. Szczegóły: `docs/UI_LANGUAGE_V013.md`. Uruchamianie Windows/Git Bash: istniejący `README_WINDOWS_GIT_BASH_EN.md`, niezmieniony schemat repozytoriów. GUI nadal nie uruchamia eksperymentów.

## CURRENT RELEASE — v0.1.4 bilingual documentation (2026-10-11)

Both languages now have complete parameter manuals (87 entries each), current user guides and Windows Git Bash installation instructions, with synchronized key/status coverage and clarified static-editor-versus-runtime boundaries. Source key names, experiment behavior, YAML profiles, original demo checkouts and GUI launch capability remain unchanged. The v0.1.3 notes above describe the historical state before the English extended reference was added. See `docs/DOCUMENTATION_PARITY_V014.md` for language and test gates.

## CURRENT RELEASE — v0.1.5 native demo launch (2026-10-11)

Seven demo variants can now be started and stopped in a separate research-Python process using immutable private YAML snapshots, dynamic gaze/voice/raw/loop/log settings, and existing demo runtime adapters. Time-Series Machine and PV execute sequentially with distinct child processes. Logs, status and validator results are retained under the private runs directory. This does **not** certify real Windows/PsychoPy/ioHub/Tobii behavior. Complete docs: `docs/NATIVE_LAUNCH_V015_PL.md` and `docs/NATIVE_LAUNCH_V015_EN.md`. Historic editor-only sections above describe earlier versions.

## CURRENT RELEASE — v0.1.9 experiments directory (2026-10-11)

**Current storage contract:** project-wide metadata and profiles stay in `tobii-pytracker/projects/<experiment_name>/`; individual runs now live exclusively in `projects/<experiment_name>/experiments/<YYYYMMDD_HHMMSS>_<5-char-ID>/`. See `docs/EXPERIMENTS_STORAGE_V019_PL.md` and `docs/EXPERIMENTS_STORAGE_V019_EN.md`. Earlier `runs/` examples in historical v0.1.7/v0.1.8 docs are superseded. No migration or legacy read fallback. Demo output CSV remains at configured `output.folder`. No launcher/UI changes beyond this storage path.

### Visual design (v0.2.0)

Native Tk/ttk now uses a lightweight charcoal/dark-gray appearance with orange
accents and small packaged icons. No graphics framework or optional runtime
package has been added. See [visual design notes PL](docs/VISUAL_THEME_V020_PL.md)
or [EN](docs/VISUAL_THEME_V020_EN.md). Functionality is unchanged from v0.1.9.

# Instalacja i użycie pytracker-gui v0.1.0

## Windows (development mode)

Prerequisite: installed Python 3.10+ with Tkinter and installed extracted `tobii-pytracker-demo v1.17.0` in a local directory. Use the actual Python 3.10 interpreter for future experiments, but v0.1.0 GUI can run under newer Python.

```powershell
cd <directory-containing-run_gui.py>
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-gui.txt
.\.venv\Scripts\python.exe run_gui.py
```

If `py -3.10` is unavailable, use the appropriate installed `python.exe`. Windows smoke test and hardware tests are pending.

## Linux

Install Python3 Tk system package if missing (often `python3-tk`; name depends on distribution). Do not run GUI with `sudo`.

```bash
cd <directory-containing-run_gui.py>
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-gui.txt
.venv/bin/python run_gui.py
```

## First use

1. Extract original **demo REPO ZIP** to an independent folder; don't point at the ZIP file or `examples/` subdirectory. The demo root contains `tools/` and `examples/`.
2. Browse for Demo root, Upstream root (original checkout; optional for static editing), Python 3.10 interpreter. Click **Zapisz ścieżki**, then **Wczytaj repo**.
3. Select from seven variants. Time-Series is one variant with editable Machine and PV YAML blocks.
4. Select a gaze mode: **none**, **MouseGaze**, or **Tobii**. Select correct device config YAML if available; at this stage the selection is only a profile/dry-run setting.
5. Configure data paths, monitor, UI or instructions. To modify advanced/unknown fields, select **YAML**. Use **Zastosuj edycję** to commit current fields to the in-memory working document.
6. Click **Sprawdź konfigurację** for static warnings. Click **Zapisz profil** to persist without modifying demo source. Click **Eksportuj YAML…** for an additional explicit copy.
7. **Uruchomienie** previews planned configuration metadata. It does NOT execute experiments. Run your original demos using their existing instructions until the child bridge phase of M1 is implemented and validated.

## Testing

`python -m unittest discover -s tests -v` for core tests. Linux Xvfb: `xvfb-run -a python -m unittest discover -s tests -v` for Tk integration tests. On a real Windows or Linux desktop, Tk integration tests can run with an available display.

Optional screenshot regeneration requires Pillow + X display: `PYTHONPATH=. python tools/make_preview.py` (development utility; do not count as core dependency).

## Superseded installation contract — 2026-10-11
The independent sibling demo checkout suggested in the historical v0.1.0 instructions is **incorrect for the real native runners**. See `INSTALL_AND_USE_V011_GIT_BASH_WINDOWS.md` for current nested layout, actual mszac/tobii-pytracker-demo Git URL and no-Tk preflight. Previous content above preserved for traceability.

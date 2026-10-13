# ADR-0002 — Tkinter/ttk jako pierwszy toolkit
Status: PROPOSED (2026-10-10).

**Warianty:** Tkinter stdlib; PySide6/Qt; Tauri/Electron/web. Tk minimalizuje nowe zależności i nie wymaga web servera; Qt zapewnia bardziej rozbudowane kontrolki kosztem biblioteki/packaging; web komplikuje local runtime.

**Propozycja:** Tkinter/ttk, Python GUI oddzielony od Python 3.10 upstream runtime. Przed akceptacją smoke Windows/Linux, DPI, file dialog i `python3-tk` availability.

**Fallback:** PySide6 tylko po udokumentowanym blockerze użyteczności/OS.

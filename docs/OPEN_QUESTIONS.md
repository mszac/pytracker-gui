# Otwarte kwestie do sprawdzenia na bramkach, bez fałszywych założeń

| Pytanie | Proponowana odpowiedź / wymagany test | Bramka |
|---|---|---|
| Dokładny upstream commit docelowy | Ustalić SHA po smoke, nie przypinać zgadywanego commita | M0 |
| Czy Tkinter/ttk działa dobrze na obu OS i wysokim DPI? | Mały prototyp OS; PySide6 rozważać dopiero jeśli Tk zawiedzie ergonomią/funkcjonalnością | M0/M1 |
| Czy wszystkie wrappery da się uruchomić przez bezpośredni Python bez Git Bash? | Zmapować Test, UX, TimeSeries, Text, Image do Popen list i porównać output | M1 |
| Jak bezpiecznie wybierać i konfigurować fizyczne Tobii? | Zweryfikować upstream ioHub tracker YAML i hardware, nie udawać auto-discovery | M3 |
| Jak dokładnie przypisać participant/session metadata do output? | Wariant sidecar + jednoznaczne połączenie run/output; nie dopisywać fikcyjnych kolumn | M2/M3 |
| Czy utrzymujemy zewnętrzne linki do plików danych czy kopiujemy? | Preferować snapshot dla reproducibility, opt-in reference dla dużych zbiorów, jawny status | M2 |
| Czy import dowolnego YAML zachowuje komentarze/unknown keys? | Nie nadpisywać źródłowego YAML; rozważyć ruamel tylko w trybie in-place advanced | M2 |
| Custom timing/randomization/TAP protocol | Osobny adapter, testy eksperymentalne i review schema | M4+ |
| Linux target | Zweryfikować minimum Ubuntu/Debian+X11/Wayland i support Tobii SDK; nie deklarować wszystkich distro | M0/M3 |
| Notebook launching, Python Jupyter | Zewnętrzny proces z jawnie wskazanym interpreteren/notebookiem | M2/M3 |

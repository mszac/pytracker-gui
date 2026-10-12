# v0.2.20 — Tylko rozmiary ikon w Environment

Zachowano układ, styl, pozycje przycisków, opisy i funkcjonalności v0.2.19. W **Experiment → Environment and repositories** zmieniono wyłącznie dwie ikony:

- **Save paths:** dotychczasowy rozmiar pliku graficznego 40×40 pozostaje, a sam znak zapisu jest powiększony *wewnątrz* tego obszaru i cache'owany w Tk root. Inne ikony zapisu w GUI są bez zmian.
- **Detect layout:** zastosowano pełnowymiarową ikonę katalogu 40×40, identyczną jak przy **Load repository**, zamiast pomniejszonej wersji 20×20.

Ikona **Check Python** pozostaje 20×20. Przyciski Environment zachowują style i równe szerokości kolumn. Pillow nie jest wymagane podczas działania GUI; nie wprowadzono timerów, nowych wątków ani zmian uruchamiania eksperymentów. Pozostałe moduły, YAML, logi, projekty, Manual i dashboard są bez zmian. Wizualny test fizyczny Windows/HiDPI pozostaje do wykonania.

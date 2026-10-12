# Osobny parametr koloru ikon — v0.2.24

Wersja zmienia wyłącznie kolor małych ikon nawigacji, zakładek Experiment i przycisków akcji na **jasny bordowy `#C77D8F`**. Pomarańczowe napisy aktywnych pozycji, podświetlenia, przyciski akcentowe i wszystkie pozostałe kolory globalnego motywu pozostają **bez zmian**. Nie zmieniono logo ani czterech grafik Home. Ciemne ikony `ink` na pomarańczowych przyciskach zachowano dla kontrastu.

Niezależny parametr `ICON_COLOR = '#C77D8F'` znajduje się w `pytracker_gui/theme.py`. Przyjmuje dowolny kolor w formacie `#RRGGBB`; zmiana wartości przed utworzeniem okna zmieni barwę wszystkich małych ikon. Jest to przygotowanie pod późniejsze GUI Settings, ale **obecnie nie dodaje opcji w panelu ustawień, zapisu preferencji ani automatycznej aktualizacji już widocznych ikon**.

Dla małego narzutu runtime lokalny `pytracker_gui/assets/icon-alpha-masks.json` (~16 KiB) przechowuje skompresowane maski przezroczystości obecnych antyaliasowanych ikon 40×40. Małe PNG RGBA są tworzone w pamięci tylko przy pierwszym użyciu danego koloru/ikony/stanu i dalej pobierane z cache dla konkretnego okna. Używany jest wyłącznie Python stdlib i Tkinter — bez Pillow w runtime, dodatkowych wątków, timerów lub przeskalowywania klatek. Oryginalne pliki PNG ikon i grafiki Home pozostają niezmienione.

Pozostała funkcjonalność, PsychoPy, YAML, projekty, dzienniki, Manual, GUI Settings, trasy nawigacji i geometria okna są nienaruszone. Fizyczny test Windows/HiDPI pozostaje osobnym etapem.

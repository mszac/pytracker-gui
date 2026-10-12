# v0.2.19 — Większe okno początkowe aplikacji

Zmiana dotyczy wyłącznie wymiarów startowego okna. Na podstawie zrzutu 1:1 użytkownika obszar aplikacji (bez paska tytułu i ramek systemu Windows) ma około **1429 × 1097 pikseli**. Na monitorach z dostateczną przestrzenią pytracker-gui otwiera się teraz w tym rozmiarze, zamiast poprzedniego limitu **1300 × 960**.

Pozostają dotychczasowe zabezpieczenia dla mniejszych monitorów: wymiary nie przekraczają rozmiaru ekranu minus 90 pikseli, z zachowaniem wcześniejszego minimum 940 × 650. Okno nadal można zmieniać ręcznie.

Bez zmian pozostają: nawigacja, proporcje paneli, obrazy, style, kontrolki, domyślny wybór, eksperymenty, logi, YAML i pozostałe działanie programu. Cztery kafelki Home nadal mają stałe rozmiary. Weryfikacja fizyczna na Windows/HiDPI pozostaje do wykonania.

# Odświeżenie grafik panelu głównego — v0.2.23

To wydanie zastępuje dokładnie cztery gotowe grafiki ekranu Home zatwierdzonymi wariantami o mocniejszym nasyceniu niebieskiego, cyjanu i pomarańczowego: Experiments, Logs, Statistics i Manual. Źródłem są cztery pliki użytkownika `*2.png`.

Każda grafika została centralnie wykadrowana do proporcji kafelka (bez deformacji), zmniejszona filtrem Lanczos do dokładnie **546 × 365 pikseli**, przekonwertowana do RGB i zapisana jako zoptymalizowany PNG. Każdy zasób ma mniej niż 350 KiB. GUI **nie wymaga Pillow podczas działania**, nie skaluje grafik w trakcie pracy i nie zyskuje dodatkowych widgetów, animacji ani operacji sieciowych. Nazwy plików i cztery dotychczasowe akcje pozostały bez zmian.

Jedynymi zmianami runtime względem v0.2.22 są bajty czterech obrazów i identyfikator wydania v0.2.23. `pytracker_gui/screens.py`, `shell.py`, GUI Settings, integracja PsychoPy, projekty, logi i pozostałe moduły runtime są niezmienione.

Walidacja: identyczny rozmiar obrazów, limit objętości, stare akcje kafelków, uruchomienie GUI, zamrożony kod, manifesty oraz czyste rozpakowanie obu ZIP-ów. Fizyczny test Windows/HiDPI pozostaje zewnętrzny.

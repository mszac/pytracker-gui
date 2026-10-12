# v0.2.25 — Ciemniejsze bordowe ikony nieaktywne; pomarańczowe ikony zaznaczone

Małe ikony **niezaznaczonych** elementów używają parametru `ICON_COLOR = '#A9526B'` w `pytracker_gui/theme.py` (wcześniej `#C77D8F`). Parametr pozostaje oddzielny i może zostać w przyszłości podłączony do GUI Settings; obecnie nie dodano tam kontrolki.

**Zaznaczony** element górnej nawigacji i aktywna zakładka edytora Experiment wykorzystują istniejący wariant `*-orange.png`, więc ikona i podpis są pomarańczowe. Przyciski z pomarańczowym wypełnieniem nadal mają ciemne ikony `*-ink.png`. Wszystkie warianty są buforowane dla okna Tkintera; niezaznaczone ikony otrzymują kolor przy pierwszym użyciu z wcześniej dostarczonych masek alfa.

Nie zmieniono pomarańczowych akcentów, geometrii, etykiet, czterech grafik Home, uruchamiania eksperymentów, mechanizmu logów ani formatów konfiguracji. Test wizualny Windows/HiDPI pozostaje do wykonania.

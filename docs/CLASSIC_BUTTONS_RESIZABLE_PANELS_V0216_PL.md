# v0.2.16 — oryginalne przyciski v0.2.14 i regulowane panele

## Decyzja i zakres

Źródłem zmian jest **dokładnie v0.2.14**. Wersja v0.2.15 nie jest bazą wydania: zaproponowane w niej wyrównane szerokości/wysokości przycisków, dwurzędowa stopka, zmniejszenie wszystkich ikon i lokalne style `ExperimentAction.*` zostały odrzucone. Wygląd przycisków, ich kolejność, układ oraz globalny motyw są takie jak w v0.2.14, poza trzema zamówionymi ikonami.

Do istniejących przycisków dodano **wyłącznie trzy** obrazy: **Sprawdź Python** (diagnostics), **Wykryj układ** (folder) i **Zastosuj edycję** (check). Każdy korzysta z istniejącego PNG, skalowanego w pamięci do 20×20 px przez natywne `PhotoImage.subsample(2, 2)`. Obrazy są cachowane przez czas życia korzenia Tk. Nie zmieniono istniejących ikon Save paths, Load repository, Restore, Export, Save profile ani Validate configuration.

Zachowano wyłącznie trzy natywne podziały `tk.PanedWindow` przeniesione z v0.2.15:

- Experiment: projekty startowe ↔ edytor, minima 220/650 px.
- Logs: selektor projektu/runu ↔ dashboard lub konsola, minima 228/390 px.
- Logs: projekty ↔ uruchomienia w pionie, minima 120/140 px.

Granice są przeciągane myszą, a proporcje zachowują się w ramach jednego uruchomienia podczas przełączania ekranów. Proporcje nie są zapisywane w pliku ustawień. Nie ma nowych timerów, wątków ani bibliotek.

## Frozen

Globalny `theme.py`, `shell.py`, `screens.py`, Manual, YAML, edytor, serializacja projektów, runner, PsychoPy, `incremental_log.py`, `log_history.py`, `log_viewer.py`, struktura folderów i plików pomiarowych pozostają identyczne bajtowo z v0.2.14. Zmieniono jedynie `app.py` i `logs_screen.py` w warstwie wizualnej, numer wersji, testy i dokumentację/logi wydania.

## Ograniczenia i kontrola Windows

Należy fizycznie potwierdzić na Windows/HiDPI, że trzy nowe ikony mają właściwy kontrast i przyciski zachowują naturalne wymiary z v0.2.14; także sprawdzić trzy uchwyty granic przy mniejszym oknie. Przy silnym zmniejszeniu edytora jego oryginalna jednorzędowa stopka może wymagać dodatkowej przestrzeni w poziomie — zgodnie z żądaniem nie modyfikowano jej wyglądu ani układu. Brak fizycznych testów PsychoPy/Tobii w tym środowisku.

## Testy

Linux/Python 3.13/Xvfb: 181 wykonanych testów PASS w niezależnych grupach (38 GUI/ikony/panele, 44 Logs/Manual, 25 core, 31 native/adapter/projects, 43 eksperymenty/session/journal). Nowe testy 7/7 PASS potwierdzają oryginalną stopkę, trzy ikony oraz regulowane granice. Formalne manifest/patch/fresh ZIP sprawdzane przy pakowaniu.

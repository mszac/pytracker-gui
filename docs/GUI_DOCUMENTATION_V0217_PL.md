# Karta GUI Documentation — v0.2.17

Zakładka **Manual → GUI Documentation** wyświetla dokumentację dotyczącą zainstalowanego projektu **pytracker-gui**. Nie przegląda oryginalnego silnika `tobii-pytracker` ani repozytorium `tobii-pytracker-demo`: do tego służą osobne karty **Documentation** i **Demo Project Documentation**.

Drzewo po lewej grupuje aktualne przewodniki i wybrane instrukcje funkcji w gałęziach **English** oraz **Polski**. Wybrany plik `.md` pojawia się w czytniku tylko do odczytu po prawej, z tym samym lekkim formatowaniem tekstu Tkinter, które zastosowano w pozostałych kartach dokumentacji. Lista jest jawnie ograniczona do dołączonych dokumentów; nie obejmuje historycznych ADR-ów, dzienników rozwoju, danych eksperymentów ani dowolnych plików użytkownika.

Indeks tworzony jest dopiero po otwarciu zakładki. Treść dokumentu odczytywana jest dopiero po wyborze pliku, z limitem 1 MiB i dotychczasowym prostym podglądem dla dużych plików. Nie dodano przeglądarki WWW, sieci, zależności, skanowania w tle, procesów, timerów ani zapisu. Linki `man` z podpowiedzi nadal prowadzą do karty **Index** (87 parametrów). Przełączanie zakładek nie zapisuje edytowanego YAML.

W sekcji **Experiment → Environment** wyrównano wyłącznie szerokości **Save paths**, **Check Python**, **Load repository** i **Detect layout**: przyciski wypełniają kolumnę o naturalnej szerokości najszerszego przycisku (w języku angielskim: Load repository). Zachowano wysokość, ikony, teksty, akcje, kolory, odstępy i style. Klasyczna jednorzędowa stopka oraz przesuwane granice paneli pozostają bez zmian.

Wydanie nie zmienia działania PsychoPy, danych pomiarowych, zapisu YAML, kopii konfiguracji, mechanizmu logowania, ekranu Logs ani globalnego motywu. Zaktualizowano przewodniki i indeksy dokumentacji EN/PL o czwartą kartę Manuala.

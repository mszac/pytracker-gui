# pytracker-gui v0.2.1 — dopracowanie wyglądu i ekran wyboru modułów

## Zakres
Zmiany wyłącznie w prezentacji i nawigacji. Ekran Eksperyment, jego formularze, uruchamianie
PsychoPy, edycja YAML, profile, projekty i historia logów pozostają bez zmian.

- W górnej części przywrócono znak `◈` i powiększono nazwę `pytracker-gui` do 17 pt (styl Tk).
  Kliknięcie ikony lub nazwy otwiera niezależny ekran wyboru modułu.
- Ekran wyboru zawiera cztery kafelki: Eksperyment, Logi, Diagnostyka, Statystyki.
  Każdy kafelek wywołuje **ten sam mechanizm nawigacji** co odpowiednia karta na pasku.
  Ekran jest budowany dopiero przy pierwszym otwarciu i później zachowywany w RAM.
- Rozjaśniono akcent pomarańczowy do `#ff9d45` i jego powiązane stany.
- Ikony PNG nawigacji i akcji są generowane w rozdzielczości 28×28 px zamiast 20×20,
  bez skalowania i zależności graficznych w trakcie działania aplikacji.
- Wcięcie poziome **zaznaczonej** zakładki konfiguracji zmniejszono o połowę:
  12 px → 6 px; niezaznaczone zakładki i wielkości czcionek formularzy zachowano.

## Wydajność i granice
Dashboard nie skanuje katalogów, nie odczytuje logów ani danych, nie wykonuje timerów,
wątków czy osobnych procesów. Obrazy PNG są buforowane na instancję okna, jak w v0.2.0.
Powrót do Eksperymentu nie niszczy jego widgetów, nie zatwierdza YAML i nie zatrzymuje sesji.
Pozostałe trzy ekrany są nadal placeholderami. Nie dodano funkcjonalności diagnostycznych,
statystycznych czy przeglądania historii logów.

## Weryfikacja
Testy automatyczne na Linux/Xvfb; ekran dashboardu i formularza sfotografowano z
rzeczywistego Tkintera (`docs/images/v021-dashboard-xvfb.png`,
`docs/images/v021-experiment-xvfb.png`). Test Windows i obsługi wysokiego DPI wymaga
sprawdzenia na stacji użytkownika. Większe ikony poprawiają ich wyrazistość, ale nie
zmieniają systemowego renderowania czcionek Windows.

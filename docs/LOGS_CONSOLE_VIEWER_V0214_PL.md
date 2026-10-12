# v0.2.14 — Logs, etap 2: konsola + większe czcionki

## Zakres

Na bazie dokładnego v0.2.13 uruchomiono kartę **Log konsoli** przy wybranym projekcie i Run ID, bez zmian mechanizmu zapisu sesji. Po lewej listy projektów i uruchomień oraz w sześciu kartach raportu używane są czcionki powiększone o jeden stopień. Lokalny kolor zaznaczenia listy to `#FFC187` z ciemnym tekstem `#131820`. Globalny motyw Tk i pozostałe ekrany są niezmienione.

## Zachowanie

- Wybranie uruchomienia nadal wyświetla Settings; log otwiera się dopiero na świadome kliknięcie **Log konsoli**. Żadne logi nie są wczytywane podczas zwykłego wyboru projektu, runu, rozwijania YAML ani przełączania języka w Settings.
- Rozpoznawana jest dokładna nazwa `experiment_<start_YYYYMMDD_HHMMSS>_<5-char-ID>.log[.part]` odpowiadająca zaznaczonemu runowi. Nigdy nie pokazujemy innego runu ani plików wyników pomiarowych. `.part` ma pierwszeństwo przy obu plikach, a nieobecność logu jest obsługiwana jako normalny stan.
- Nawigacja: **Początek**, **Poprzedni**, **Następny**, **Ostatnie**, **Odśwież log**, **Kopiuj fragment**; dostępne są też przewijanie pionowe i poziome. Przy `*.log.part` odświeżanie jest wyłącznie ręczne, nie ma pollingu.
- Odczyt jest ograniczony do **64 KiB i 2 000 wierszy na porcję**. Odczyty są sekwencyjne z `seek`, bez `read_text()` całego pliku, watcherów, background wątków, parserów wyników i bazy danych. Długie linie mogą wymagać poziomego przewijania; przecięcie bardzo długiej linii na granicy 64 KiB może zastąpić pojedynczy wielobajtowy znak UTF-8 znakiem zastępczym tylko w podglądzie.
- Kolory COMPLETE/INCOMPLETE dotyczą integralności dziennika, **nie** prawidłowości pomiaru. Pliki pozostają read-only; `.part` nie jest naprawiany, usuwany ani przemianowywany przez Logs.

## Wydajność i bezpieczeństwo

Ograniczona liczba wierszy i bajtów zapobiega alokowaniu całego logu w widżecie Tk. I/O występuje tylko w wyniku kliknięcia lub wejścia do Console Log; brak otwierania `data.csv`, odczytów `output.folder` czy dodatkowego obciążenia w trakcie pozyskiwania danych. Odrzucone są dowiązania symboliczne i pliki inne niż regularne, sprawdzana jest kanoniczna nazwa. Odczyt z aktywnego `.part` nie musi obejmować bajtów, które writer jeszcze trzyma w swoim buforze 256 KiB.

## Ograniczenia i test akceptacyjny Windows

Przy długim logu sprawdzić pierwszą, środkową i najnowszą stronę oraz długie linie; przy aktywnym eksperymencie i `Auto-show Logs = OFF` ręcznie odświeżyć rosnący `.part`. Dla przerwanej sesji wyświetlić oznaczenie INCOMPLETE. Potwierdzić czytelność jasnego pomarańczowego zaznaczenia obu list na HiDPI i brak regresji YAML/Manual. Fizyczne testy Windows/PsychoPy/Tobii nie były wykonywane na Linux/Xvfb.

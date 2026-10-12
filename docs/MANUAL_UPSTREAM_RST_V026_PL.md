# v0.2.6 — Manual: Index i Documentation

W ekranie **Manual** domyślnie otwiera się **Index**, zawierający dotychczasowy
wyszukiwalny katalog 87 parametrów i ich rozszerzone opisy. Odnośniki `man`
w dymkach nadal wybierają właściwy parametr właśnie na karcie **Index**.

W języku angielskim nazwy wartości pod nagłówkiem **Available options** są teraz
zielone. Kolor samego nagłówka pozostaje neutralny. Opisy i możliwe wartości
nie zostały zmienione.

Nowa karta **Documentation** udostępnia lokalne pliki `*.rst` z katalogu
`<tobii-pytracker>/docs/` oryginalnego repozytorium upstream. Nie korzysta
z dokumentacji `tobii-pytracker-demo`. Wyszukiwanie filtruje nazwy plików;
wybór otwiera zawartość wybranego dokumentu, z wyróżnieniem nagłówków.
Dokumenty pozostają w składni reStructuredText (nie jest to renderer Sphinx:
zaawansowane dyrektywy, linki i figury są pokazywane jako tekst źródłowy).

Lista plików jest odczytywana dopiero przy pierwszym otwarciu karty. Sam plik
czytany jest dopiero przy wybraniu. Po zmianie ścieżki do upstream karta
aktualizuje listę po ponownym wejściu. Czytnik jest tylko do odczytu, bez sieci,
procesów, dodatkowych pakietów, zapisu danych lub ingerencji w PsychoPy.

Jeżeli nie ma katalogu docs/ lub plików .rst, widać informację o braku dokumentacji.
Istniejące ustawienia, profile i uruchamianie projektów nie zmieniły się.

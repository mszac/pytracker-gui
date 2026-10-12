# v0.2.22 — kafelek Logs i sekcja GUI Settings

Zakres iteracji jest ograniczony do zatwierdzonej grafiki **Logs** na Home oraz nowej sekcji **GUI Settings** po prawej stronie Manual. Pozostałe cztery akcje dashboardu oraz stały rozmiar kafelków 546×365 px pozostają bez zmian.

## GUI Settings — pierwsza wersja

Ekran jest tworzony leniwie, bez wątków i okresowego skanowania dysku. Kompaktowy raport prezentuje katalog danych GUI, katalog historii projektów, aktualne ścieżki repozytoriów dem i upstream, interpreter Python, język interfejsu i podpowiedzi, stan Auto-show Logs oraz format pojedynczego narastającego logu konsoli. Ścieżki nadal są edytowane i zapisywane wyłącznie w **Experiment → Environment**.

W zakładce można ustawić domyślny rozmiar okna na **940×650**, **1100×800**, **1300×960**, **1429×1097** (domyślnie) lub **1600×1000**. Przycisk **Zapisz rozmiar** aktualizuje wyłącznie `window_size` w dotychczasowym lokalnym `settings.json` GUI, zachowując pozostałe ustawienia i spójność pamięci edytora Experiment. Nowa wielkość obowiązuje **po ponownym uruchomieniu**, nie podczas bieżącej sesji. Działa dotychczasowe ograniczenie do dostępnego rozmiaru ekranu. Nie zmieniono profili, YAML, danych pomiarowych, repozytoriów ani mechanizmu logowania.

Grafika Logs jest dopasowaną do 546×365 px wersją dokładnego dostarczonego pliku 1448×1086 px. Pozostałe obrazy i akcje dashboardu pozostają nietknięte.

## Walidacja

Testy Tk/Xvfb obejmują wielkość domyślną, zapis i ponowne uruchomienie, leniwą nawigację, ścieżki tylko do odczytu, języki i niezmienione cztery przyciski Home. Rzeczywisty Windows/HiDPI pozostaje do sprawdzenia.

# v0.2.10 — Manual: drzewo dokumentacji projektów startowych

Ta iteracja bazuje **bezpośrednio na v0.2.9**, bez zmiany kolorystyki v0.2.6, sposobu zapisu projektów ani uruchamiania eksperymentów.

## Nawigacja

- Usunięto **Diagnostyka / Diagnostics** z górnej nawigacji i dashboardu. Dotychczasowe narzędzia weryfikacyjne wewnątrz ekranu Eksperyment pozostają dostępne.
- Ekran Manual ma trzy zakładki: **Index** (domyślna), **Documentation** (lokalne `.rst` z oryginalnego `tobii-pytracker/docs`) i **Demo Project Documentation** (lokalne `.md` z `tobii-pytracker-demo`).
- Trzecia zakładka pokazuje rozwijane drzewo: nazwa projektu → pliki instrukcji `.md`. Dla projektów istniejących w źródłowym repo v1.17.0 dołączono również odpowiedni plik z `docs/basic_examples`, jeśli istnieje; dokument pozostaje przechowywany i odczytywany z oryginalnej lokalizacji.
- Kliknięcie `man` w dymku nadal otwiera odpowiedni parametr w **Index**, bez zapisywania konfiguracji.

## Koszt i bezpieczeństwo

Każdy ekran/zakładka jest tworzony leniwie, a lista plików jest odczytywana dopiero przy pierwszym wejściu do Demo Project Documentation lub po zmianie ścieżki do repozytorium. Treść konkretnego pliku jest odczytywana **dopiero po jego wskazaniu** w drzewie. Przeglądarka nie zapisuje danych, nie uruchamia programów, nie korzysta z sieci ani z zewnętrznych bibliotek renderujących. Odrzuca dowiązania symboliczne i dokumenty poza repozytorium; plik `.md` jest ograniczony do 1 MiB.

Użyto ograniczonego formatowania wewnątrz natywnego `tk.Text`: nagłówków, list, wyróżnień, cytatów i bloków kodu Markdown oraz nagłówków/list/kodu reStructuredText. **Nie jest to pełny renderer Markdown, Sphinx ani HTML**: linki, obrazy, zaawansowane dyrektywy i tabele mogą pozostać w formie uproszczonej. Dokumenty powyżej 256 KiB są wyświetlane bez dodatkowego formatowania linii, co zapobiega długiemu blokowaniu Tkintera.

Dokumentacja pomiarów, pliki CSV, dane wynikowe i logi nie są częścią tego widoku. Testy fizyczne Windows/PsychoPy/Tobii nadal pozostają zewnętrznym etapem walidacji.

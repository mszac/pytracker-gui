# v0.2.26 — edycja istniejącej palety GUI i nowy kolor ikon

**Baza:** dokładne wydanie v0.2.25. Zakres zmian funkcjonalnych dotyczy wyłącznie koloru ikon i istniejącego ekranu GUI Settings.

## Nowy domyślny kolor ikon nieaktywnych

`pytracker_gui/theme.py` nadal przechowuje jeden istniejący parametr `ICON_COLOR`. Jego wartość domyślna to `#22289B` (RGB 34, 40, 155). Zaznaczone pozycje nawigacji i zakładki pozostają pomarańczowe i korzystają z oryginalnych `*-orange.png`. Ciemne ikony na pomarańczowych przyciskach nie zostały zmienione. Maski przezroczystości, bufor ikon na okno Tk, zasoby PNG i obrazy Home pozostają bez zmian.

## Panel kolorów na dole GUI Settings

**GUI Settings → Kolory interfejsu** udostępnia istniejące `ICON_COLOR` oraz wszystkie istniejące pola słownika `COLORS`: `window`, `surface`, `surface_alt`, `field`, `hover`, `border`, `text`, `muted`, `accent`, `accent_hover`, `accent_text`, `selection`, `success`. Wszystkie przyjmują zapis `#RRGGBB`. **Nie dodano nowych parametrów kolorystycznych.** Próbka pokazuje zapisany kolor. **Zapisz kolory** zapisuje ustawienia atomowo do dotychczasowego prywatnego `settings.json` pod nazwami istniejących parametrów `ICON_COLOR` i `COLORS`. **Przywróć domyślne wartości** wypełnia pola wartościami domyślnymi; należy następnie kliknąć Zapisz kolory. Błędna wartość zatrzymuje cały zapis bez nadpisywania dotychczasowych ustawień.

**Zmiana zaczyna działać po ponownym uruchomieniu GUI.** Aplikacja raz odczytuje ustawienia i sprawdza dopuszczalne klucze i formaty, a następnie stosuje kolory przed utworzeniem widżetów. Nieprawidłowe/nieznane wartości nie zastępują domyślnych. Eliminuje to konieczność przebudowy kontrolek i ponownego kolorowania ikon podczas eksperymentu. GUI Settings ma natywne przewijanie, dzięki czemu dolny panel jest dostępny również w mniejszym oknie.

Użytkownik może świadomie zmienić pomarańczowe wartości słownika, ale ich domyślne odcienie pozostają identyczne z v0.2.25. Bez zależności Pillow podczas pracy, sieci, nowych wątków i odświeżania cyklicznego. Eksperymenty/YAML, logi, historia i identyfikacja sesji pomiarowych pozostają niezmienione.

## Granica walidacji

Testy obejmują nowy kolor ikon, pomarańczowe zaznaczenie, walidację wartości, zapis atomowy, odczyt po restarcie, przywrócenie domyślnych wartości, mniejsze okno i wcześniejszy wybór rozmiaru okna. Testy Linux Python 3.13/Xvfb nie zastępują rzeczywistego testu Windows/HiDPI.

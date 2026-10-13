# Ustawienia GUI — opis opcji

Ten przewodnik dotyczy wyłącznie **ustawień aplikacji pytracker-gui**. Nie zmienia konfiguracji eksperymentów ani plików oryginalnych repozytoriów. Niebieska ikona `i` obok opcji wyświetla krótkie wyjaśnienie, a link `man` otwiera właściwą sekcję tego przewodnika.

**Oznaczenia:** szare etykiety opisują opcje; niebieskie `i` otwiera podpowiedzi; pomarańczowe nagłówki wyróżniają tematy, a zielony tekst o stałej szerokości oznacza dosłowne wartości konfiguracji. Pola opisane jako „tylko do odczytu” nie są edytowane tutaj.

## Okno i wygląd

Zapisany rozmiar okna obowiązuje dopiero przy następnym uruchomieniu; kafelki Home pozostają w stałej rozdzielczości.

## Opcja: window_size

Wybierz jeden z gotowych rozmiarów okna startowego. Mniejszy ekran może ograniczyć ostateczne wymiary do dostępnego obszaru. Sam wybór na liście nie zapisuje wartości — użyj **Zapisz rozmiar**.

## Opcja: save

Zapisuje aktualnie wybrany rozmiar okna na następne uruchomienie aplikacji; nie zmienia rozmiaru bieżącego okna.

## Opcja: tile_size

Cztery obrazy kafelków Home zawsze mają wymiary **546 × 365 pikseli**. Podczas zmiany rozmiaru okna nie są rozciągane ani ponownie skalowane. W razie potrzeby pojawiają się paski przewijania.

## Opcja: paths

Wyświetlane ścieżki to wartości tylko do odczytu. Obsługiwane ścieżki repozytoriów i interpretera zmienia się w **Experiment → Environment**. Ta strona nie przenosi ani nie modyfikuje katalogów.

## Opcja: gui_home

Katalog konfiguracji i stanu należących do aplikacji GUI, oddzielony od pomiarów eksperymentalnych i oryginalnych repozytoriów.

## Opcja: projects_root

Katalog nadrzędny projektów użytkownika, zapisanych profili, katalogów uruchomień i historii. Nie usuwaj go podczas aktualizacji GUI.

## Opcja: demo_root

Katalog główny repozytorium przykładów/projektów startowych, z którego wybierane są konfiguracje demonstracji. To nie jest katalog historii projektów użytkownika.

## Opcja: upstream_root

Katalog główny oryginalnego repozytorium silnika wykorzystywanego przy uruchamianiu eksperymentów; nie jest to katalog GUI ani demonstracji.

## Opcja: python

Interpreter Python skonfigurowany do uruchamiania eksperymentów. Ten widok tylko wyświetla ścieżkę: nie testuje działania PsychoPy, ioHub ani fizycznego eye-trackera.

## Opcja: preferences

Podsumowanie aktualnych preferencji, wyświetlane tylko informacyjnie. Kontrolki zmieniające te wartości znajdują się w innych częściach aplikacji.

## Opcja: language

Aktualny język etykiet i menu GUI. Jest niezależny od języka bodźców w demonstracjach.

## Opcja: help_language

Język opisów parametrów i ich rozbudowanych wpisów w manualu. Może być inny niż język etykiet GUI.

## Opcja: auto_logs

Pokazuje, czy podgląd konsoli Logs otwiera się automatycznie podczas wykonywania eksperymentu. Wyłącza się go w Experiment; nie wyłącza to zapisu dziennika konsoli.

## Opcja: journal

Każde uruchomienie ma jeden narastający dziennik konsoli: aktywny lub niekompletny `.log.part` albo zakończony `.log`. Dziennik zawiera komunikaty konsoli, nie próbki pomiarowe wzroku.

## Opcja: colors

Edytor zmienia tylko istniejącą paletę GUI oraz obsługiwany kolor ikon. Wpisuj wartości sześciocyfrowe w formacie `#RRGGBB`. Podgląd próbek nie jest podglądem całej aplikacji na żywo.

## Opcja: save_colors

Przed zapisem sprawdzane są wszystkie wpisy palety. Jedna niepoprawna wartość odrzuca cały zapis; zapisane kolory zaczynają obowiązywać po ponownym uruchomieniu GUI.

## Opcja: reset_colors

Wczytuje fabryczne kolory do pól edytora, ale ich jeszcze nie zapisuje. Aby zachować przywróconą paletę, wybierz **Zapisz kolory** i uruchom ponownie GUI.

## Opcja: ICON_COLOR

Kolor obsługiwanych nieaktywnych ikon. Ikony aktywnych lub wybranych sekcji mogą korzystać z osobnych, pomarańczowych grafik i nie muszą podlegać temu ustawieniu.

## Kolory palety

Każdy kolor wpisz jako sześciocyfrową wartość RGB `#RRGGBB`. **Zapisz kolory** sprawdza całą paletę. Zmiany pojawiają się po ponownym uruchomieniu GUI. Niektóre grafiki i ikony aktywnych sekcji używają niezależnych zasobów.

## Opcja: window

**Tło głównego okna aplikacji.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: surface

**Tło głównych paneli treści.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: surface_alt

**Tło paneli pomocniczych i okienek podpowiedzi.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: field

**Tło pól wejściowych i zagłębionych obszarów treści.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: hover

**Tło po najechaniu kursorem w obsługiwanych kontrolkach.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: border

**Obramowania paneli i kontrolek.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: text

**Podstawowy kolor tekstu.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: muted

**Tekst drugoplanowy i mniej wyróżniony.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: accent

**Główny pomarańczowy akcent dla wyróżnień i zaznaczonych kontrolek.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: accent_hover

**Odcień akcentu po najechaniu kursorem.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: accent_text

**Tekst wyświetlany na tle w kolorze akcentu.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: selection

**Podświetlenie zaznaczenia w obsługiwanych kontrolkach.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.

## Opcja: success

**Wskaźniki pozytywnego statusu.** Wprowadź sześciocyfrową wartość RGB w formacie `#RRGGBB`. Zapisz całą paletę i uruchom ponownie GUI. Niektóre grafiki i ikony aktywnych sekcji mają niezależny wygląd.


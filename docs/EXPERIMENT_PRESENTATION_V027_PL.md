# v0.2.27 — Zmiany wyglądu wyłącznie w Experiment

**Dokładna baza:** v0.2.26 Full. W tej wersji nie zmieniono natywnego paska tytułowego Windows, nie dodano jego ustawienia ani wywołań Windows API.

## Nieaktywne ikony w Experiment

Nieaktywne małe ikony na ekranie **Experiment** (w tym Monitor, YAML i przyciski akcji) mają domyślnie kolor `#A46628`. Zaznaczone zakładki nadal używają oryginalnych pomarańczowych grafik, a ikony `active='ink'` na pomarańczowych przyciskach zachowują ciemny wariant. Nowy kolor jest lokalną wartością domyślną: globalny `ICON_COLOR` nadal ma wartość fabryczną `#22289B`, a `COLORS`, inne ekrany, GUI Settings i górna nawigacja pozostają bez zmian. Jeśli użytkownik jawnie zapisał własny `ICON_COLOR` w GUI Settings, ta preferencja nadal obowiązuje również w Experiment.

Kod ponownie wykorzystuje istniejące jednorazowe kolorowanie ikon i cache dla okna Tk. Nie dodano zależności, odpytywania, wątków, zapisów plików, skalowania ikon w czasie pracy ani nowego ustawienia koloru.

## Stały nagłówek panelu

Dynamiczny podpis wybranego demo (np. `Test Demo · EN`) w prawym panelu Experiment zastąpiono stałym napisem `Experiment setup` ze stylem `Heading.TLabel`, zbliżonym wizualnie do nagłówka Starter projects. Zmiana demo lub języka aplikacji nie nadpisuje już tego podpisu. Osobny istniejący opis demo, kontrolki Block i Project oraz cała logika wyboru i uruchamiania pozostają bez zmian.

## Zakres i testy

Jedynymi zmienionymi ścieżkami produkcyjnymi względem v0.2.26 są `pytracker_gui/theme.py`, `pytracker_gui/app.py`, `pytracker_gui/__init__.py` i `VERSION`. Oryginalne PNG oraz wszystkie pozostałe pliki runtime zachowano bajt po bajcie. Jedną wcześniejszą asercję testu stanu ikony dostosowano do lokalnego koloru; nowy test sprawdza pomarańczowe ikony aktywne, globalne wartości nawigacji, stałość nagłówka przy wyborze demo oraz własny `ICON_COLOR`.

Testy Linux/Xvfb nie zastępują sprawdzenia wyglądu na Windows/HiDPI. Ta iteracja nie obejmuje testów fizycznego Tobii ani eksperymentu PsychoPy.

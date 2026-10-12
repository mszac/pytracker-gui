# Nawigacja modułowa — pytracker-gui v0.1.8

## Zakres
Nowa, stała **górna nawigacja** prowadzi do czterech oddzielnych ekranów: **Eksperyment**, **Logi**, **Diagnostyka**, **Statystyki**. Jest to podział między *modułami aplikacji*, a nie zamiennik sześciu istniejących zakładek w ekranie Eksperyment (Dane, Monitor, Wygląd, Instrukcje, YAML, Uruchomienie). Polski pozostaje domyślny; nawigacja, komunikaty pustych ekranów i etykieta projektu mają odpowiedniki angielskie.

## Co działa
- **Eksperyment**: obecny ekran konfiguracji i sterowania uruchomieniem; zachowuje istniejące pola, profile, ikony informacyjne, okno `Experiment log`, procesy i walidację.
- **Logi**: niezależny, pusty ekran przeznaczony do przyszłego przeglądu zapisanych logów. Nie przegląda dysku i nie otwiera logów automatycznie.
- **Diagnostyka**: niezależny, pusty ekran dla przyszłych raportów. Dotychczasowe `Sprawdź Python` i `Sprawdź konfigurację` nadal są w Eksperymencie.
- **Statystyki**: niezależny, pusty ekran; nie liczy statystyk, nie czyta plików CSV i nie importuje pakietów analitycznych.
- **Kontekst projektu** w pasku nawigacji pokazuje nazwę aktualnie wybranego projektu. Nie jest edytorem ani drugim źródłem stanu.

## Kontrakt architektury
`pytracker_gui/shell.py` zawiera `AppShell`: przyciski nawigacji, kontekst projektu i jeden host ekranów. `pytracker_gui/app.py` nadal zawiera istniejącą klasę `PytrackerGUI`, obecnie osadzaną jako ekran `experiment` i utrzymującą wyłączną odpowiedzialność za wybór demo, edycję YAML, uruchamianie i zamykanie sesji. `pytracker_gui/screens.py` zawiera osobne widoki z minimalnym tekstem zastępczym. **Nie wprowadzono** wspólnej klasy dla procesów badawczych ani nowych połączeń między modułami.

Ekran Eksperyment jest tworzony raz przy starcie, ponieważ jest widokiem początkowym. Każdy dodatkowy widok powstaje **dopiero po pierwszym kliknięciu** i jest ponownie wykorzystywany przy kolejnych wizytach (`pack_forget`/`pack` zamiast `destroy`/odbudowy). Nawigacja **nie wywołuje** zapisu profilu, zastosowania edycji, walidacji YAML, zatrzymania/startu procesu, odczytów katalogów, wątków ani `after()`. Niezapisane zmiany w zakładce Eksperyment pozostają w tym samym obiekcie kontrolki podczas przełączania. Błędny YAML zostanie sprawdzony standardowo dopiero przy istniejącej operacji zastosowania, zmiany zakładki lub uruchomienia.

Zamknięcie głównego okna jest delegowane do istniejącego `PytrackerGUI.request_close()`, wraz z dotychczasowym potwierdzaniem zatrzymania aktywnej sesji oraz obsługą niezapisanych zmian. Widoczne okno logu jest nadal dotychczasowym `Toplevel` należącym do ekranu Eksperyment.

## Uruchomienie i test
W kanonicznym układzie `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui,projects}`:

```bash
conda activate pytracker-env
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Wybierz kolejno Logi, Diagnostyka, Statystyki i Eksperyment. Zmieniaj język PL/EN, sprawdź powrót do edycji YAML bez utraty wartości oraz dostępność zakładki Uruchomienie. Użytkownicy Windows powinni dodatkowo sprawdzić przyciski przy mniejszej rozdzielczości i działanie istniejących dem. Automatyczna walidacja Linux/Xvfb używa `python -m unittest discover -s tests -v`.

## Czego nie zmieniono
Brak zmian silnika upstream, adapterów dem, runnera, profili, YAML, `projects/`, kopii konfiguracji, identyfikatorów wykonania, formatu logów, walidatorów i istniejących sześciu zakładek. **Nie zaimplementowano** przeglądarki logów, nowych narzędzi diagnostycznych ani statystyk. Te funkcje będą osobnymi iteracjami, każda z własnymi testami.

Zrzut rzeczywistego okna Tkinter podczas testu Linux/Xvfb: [`docs/images/v018-navigation-xvfb.png`](images/v018-navigation-xvfb.png). Nie jest to test wyglądu na fizycznym Windows.

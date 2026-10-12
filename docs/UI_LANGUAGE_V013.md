> **Historia / historical checkpoint:** Ten dokument opisuje wyłącznie zakres swojego wydania. Aktualne przewodniki i manuale PL/EN w `docs/DOCUMENTATION_INDEX_PL.md` / `docs/DOCUMENTATION_INDEX_EN.md` zastępują nieaktualne twierdzenia o braku angielskiego manuala.

# pytracker-gui v0.1.3 — wybór języka interfejsu i podpowiedzi

## Zakres

Zmiana **wyłącznie prezentacyjna** w stosunku do v0.1.2. GUI Tkinter domyślnie otwiera się po **polsku**. W górnej części okna znajdują się dwa pola wyboru:

- **Język interfejsu / Interface language:** `Polski` albo `English` — zmienia etykiety, zakładki, komunikaty i okna dialogowe aplikacji.
- **Język podpowiedzi / Tooltip language:** `Polski` albo `English` — zmienia jednozdaniowe opisy w dymkach otwieranych ikonami `i`. Domyślnie podąża za językiem interfejsu; użytkownik może ustawić go niezależnie, np. angielskie GUI z polskimi podpowiedziami.

Oba wybory są przechowywane tylko w prywatnym `settings.json` GUI (`language`, `help_language`, `help_language_explicit`). Dotychczasowe profile, pliki YAML, identyfikatory dem, bloki Machine/PV, ścieżki i parametry runtime mają **identyczny** format i zachowanie. Przy zmianie języka aktywna karta formularza najpierw zapisuje bieżące poprawne wartości w modelu w pamięci; błędny YAML uniemożliwia przełączenie zamiast usunąć tekst. Profil użytkownika nadal wymaga jawnego zapisu.

## Stan manuala

Pełny manual **pozostaje wyłącznie po polsku**: `docs/PARAMETER_MANUAL_PL.md`. Jego istniejące 87 krótkich i 87 długich opisów są nietknięte. Angielskie krótkie opisy i tytuły ikon są w pliku `pytracker_gui/parameter_help_en.json` (87/87), bez angielskich długich opisów. Przy angielskim GUI można jawnie wybrać polskie podpowiedzi. Tekst interfejsu informuje o lokalizacji polskiego manuala, ale zgodnie z poprzednimi ustaleniami **nie ma linku ani okna manuala**. Angielski manual zostanie przygotowany w osobnej, przyszłej iteracji, jeśli będzie potrzebny.

## Testy i bramki

- Uruchomienie 30/30 testów, w tym 23 odziedziczonych testów funkcjonalnych i 7 nowych testów tłumaczeń, przełączania języków, trwałości ustawień, niezapisanych zmian i ochrony błędnego YAML.
- Oba warianty UI uruchomione w rzeczywistym Tk pod Linux/Xvfb. Obrazy: `docs/images/v013-polish-help.png`, `v013-english-help.png`.
- `tools/render_parameter_manual.py --check` — synchronizacja polskiego manuala.
- Oryginalne repozytoria `sbobek/tobii-pytracker` i `mszac/tobii-pytracker-demo` nie są modyfikowane. Nie ma start/stop dem ani rozszerzeń ioHub.
- Fizyczny Windows/Conda Python 3.10/Tobii **NOT RUN**; należy wykonać istniejący Windows smoke, w tym przełączenie PL/EN i osobny język dymków.

## Windows / Git Bash

Przy zachowanym zagnieżdżonym układzie `tobii-pytracker/{tobii-pytracker-demo,pytracker-gui}`, umieść pełny ZIP v0.1.3 tak, aby zastąpił poprzedni podkatalog `pytracker-gui` (najbezpieczniej rozpakować czysto do nowego katalogu; profile użytkownika są przechowywane poza nim). Następnie:

```bash
cd /d/pytracker/tobii-pytracker
conda activate pytracker-env
python -m pip install -r pytracker-gui/requirements-gui.txt
python pytracker-gui/run_gui.py --check-layout
python pytracker-gui/run_gui.py
```

Wybrany język UI i dymków powinien przetrwać zamknięcie i ponowne uruchomienie aplikacji. Nie zmieniaj oryginalnych repozytoriów ani plików YAML podczas instalacji GUI.

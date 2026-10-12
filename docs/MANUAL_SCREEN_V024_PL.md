# v0.2.4 — ekran Manual i logo

## Zakres

- W górnym lewym rogu pozostaje klikalne logo pytracker-gui, teraz na białym, okrągłym tle; historyczny pomarańczowy znak ◈ został usunięty. Kliknięcie logo lub nazwy nadal otwiera Dashboard.
- Górna nawigacja i Dashboard mają nową pozycję **Manual**. Jest to osobny ekran tworzony leniwie dopiero po pierwszym otwarciu, bez timerów, nowych procesów ani odczytów danych eksperymentalnych.
- Manual przedstawia **87 istniejących parametrów**. Pozycje są przeszukiwalne według nazwy, identyfikatora, opisu i grupy. Wybór tematu pokazuje krótki i rozszerzony opis oraz status dostępności.
- Dymki otwierane ikoną `i` mają pomarańczowy link **man**. Kliknięcie przenosi do odpowiedniej pozycji Manuala, bez zmiany formularzy i bez zatwierdzania edytowanego YAML.
- Teksty manuala są odczytywane z istniejących katalogów PL/EN (`parameter_help.json` i `parameter_help_en.json`). Język opisu podąża za językiem podpowiedzi, a język nawigacji za językiem GUI.

## Granice

Nie zmieniono siedmiu wariantów demonstracji, uruchamiania PsychoPy, wyboru gaze, zapisów projektów, konfiguracji, logów sesji, formatów profili i dotychczasowej ochrony niezapisanych pól. Dłuższe teksty nie są pobierane z sieci ani przeliczane w tle. Ekran Manual nie zmienia konfiguracji eksperymentu.

## Walidacja

Testy hostowe Linux/Xvfb obejmują leniwe tworzenie i ponowne użycie ekranu Manual, otwieranie dokładnego opisu przez `man`, polskie i angielskie dłuższe opisy, wyszukiwanie, nawigację kafelkami i zachowanie niezapisanego, niepoprawnego YAML. Windows/HiDPI i urządzenie Tobii wymagają zewnętrznego testu fizycznego.

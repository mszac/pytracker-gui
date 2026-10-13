# pytracker-gui — podręcznik parametrów (M1)

> Aktualizacja: 2026-10-11, v0.1.5. Opisy odnoszą się do znanych kontraktów
> repozytoriów `sbobek/tobii-pytracker` i `mszac/tobii-pytracker-demo`
> (zestaw dem v1.17.0) oraz do możliwości edytora pytracker-gui.
> Nie stanowią dowodu uruchomienia sprzętu ani gwarancji zachowania
> nowszych, nieprzypiętych do commita wersji upstream.

Każdy z **87 parametrów** zawiera krótki opis (jedno zdanie dla ikony `i`)
i opis rozszerzony. Identyfikatory YAML i CLI nie są tłumaczone. **Status `gui`
oznacza pole lub preferencję GUI; zastosowanie zależy od opisanej funkcji.
** Zapis profilu i eksport YAML nie uruchamiają PsychoPy — służy do tego
osobny przycisk Uruchom demo.
Parametry `yaml-only`, `iohub-only`, `reference` i `future`
nie muszą mieć własnych edytorów lub pełnej obsługi wykonawczej.

Link **man** w podpowiedzi otwiera odpowiedni wpis w karcie Manual → Index.
Dostępne wartości są opisane dla parametrów, które udostępniają wybór opcji.
Angielska wersja: [`PARAMETER_MANUAL_EN.md`](PARAMETER_MANUAL_EN.md).

**Źródła:** [upstream](https://github.com/sbobek/tobii-pytracker), [demo repository](https://github.com/mszac/tobii-pytracker-demo), [MouseGaze YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml), [Tobii YAML](https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml).

## Środowisko / GUI

### `gui.demo_root` — Demo root

**Krótko:** Katalog zagnieżdżonego repozytorium demonstracji zawierający examples/ i tools/.

**Opis:** Wskaż `tobii-pytracker/tobii-pytracker-demo`, pobrany z `mszac/tobii-pytracker-demo`. GUI wymaga osiem plików YAML dla siedmiu wariantów i przyjmuje katalog dem za bazę rozwiązywania ścieżek względnych. Wczytanie lub zapis profilu nie nadpisuje źródłowych plików repozytorium.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `gui.upstream_root` — Upstream

**Krótko:** Katalog główny oryginalnego repozytorium silnika `sbobek/tobii-pytracker`.

**Opis:** Wybierz katalog `tobii-pytracker` zawierający `pyproject.toml`, `src/tobii_pytracker` i `configs/`. Repozytorium dem oraz `pytracker-gui` powinny być dwoma odrębnymi podkatalogami tego katalogu. Diagnostyka sprawdza układ i ścieżki; nie zmienia plików silnika.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.python` — Python 3.10

**Krótko:** Ścieżka do interpretera Python 3.10 w środowisku `pytracker-env`.

**Opis:** Wskaż plik wykonywalny Pythona z istniejącego środowiska Conda `pytracker-env`, a nie dowolny interpreter systemowy. Oryginalny silnik deklaruje wymóg Pythona 3.10.x. Sprawdzenie interpretera w GUI jest diagnostyką wersji, nie testem działania PsychoPy, ioHub ani urządzenia.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.variant` — Wariant demonstracji

**Krótko:** Wybiera jeden z siedmiu wariantów istniejących demonstracji do edycji.

**Opis:** Lista zawiera Test Demo (EN), UX A/B Text (EN i PL), Time-Series Noise (Machine + PV), Text Search (EN i PL) oraz Image Semantic (EN). Wariant wybiera zestaw źródłowych konfiguracji do odczytu i statycznej kontroli. To nie jest kreator nowych badań ani przycisk wykonania eksperymentu.

**Dostępne wartości:**

- `test_en` — Test Demo [EN]: klasyfikacja obrazów w trzech próbach; standardowe uruchomienie upstream.
- `ux_en` — UX A/B Text [EN]: dwanaście angielskich zadań układu tekstu z dostarczonym adapterem.
- `ux_pl` — UX A/B Text [PL]: polski wariant z osobnym plikiem YAML.
- `ts_machine_pv` — Time-Series Noise [Machine → PV]: dwa kolejne bloki po dziewięć prób, z osobnymi plikami YAML i weryfikacją danych.
- `search_en` — Text Search [EN]: angielskie zadania wyszukiwania w tekście.
- `search_pl` — Text Search [PL]: polskie zadania wyszukiwania w tekście.
- `image_en` — Image Semantic [EN]: zadania analizy semantycznej obrazów z adapterem obrazów.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `gui.block` — Blok demonstracji

**Krótko:** Przełącza plik YAML wybranego bloku demonstracji.

**Opis:** Większość demonstracji posiada jeden blok i jeden natywny plik YAML. Time-Series Noise posiada dwa oddzielne bloki Machine Vibration i PV Power, z własnymi wartościami i limitami prób. Zmiana bloku nie przenosi wartości z jednego YAML do drugiego, a obecny GUI nie wykonuje obu bloków.

**Dostępne wartości:**

- `main` — Główny blok konfiguracji większości projektów startowych; edytowany i uruchamiany jako całość.
- `machine` — Pierwszy blok Time-Series Noise (Machine Vibration), z osobnym YAML; wykonywany przed PV.
- `pv` — Drugi blok Time-Series Noise (PV Power); wykonywany po pomyślnym zakończeniu Machine.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `gui.gaze` — Źródło gaze

**Krótko:** Wybiera sposób rejestrowania spojrzeń podczas uruchamiania demonstracji z GUI.

**Opis:** NO_GAZE wyłącza rejestrowanie gaze, ale nie blokuje myszy do udzielania odpowiedzi. MOUSEGAZE uruchamia symulację ioHub za pomocą myszy, a TOBII wybiera konfigurację fizycznego urządzenia. W v0.1.5 wybór jest przekazywany do odrębnego procesu z oryginalnym runtime; poprawność działania urządzenia wymaga rzeczywistego testu.

**Dostępne wartości:**

- `NO_GAZE` — Nie uruchamia pobierania danych wzrokowych; odpowiedzi z myszy w PsychoPy mogą nadal działać.
- `MOUSEGAZE` — Emulator śledzenia wzroku przez mysz w PsychoPy ioHub; konfiguracja musi być zgodna z projektem.
- `TOBII` — Fizyczny, obsługiwany tracker Tobii z odpowiednim plikiem ioHub; wymaga działającego urządzenia i sterownika.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.iohub_yaml` — Plik ioHub YAML

**Krótko:** Ścieżka do konfiguracji ioHub dla wybranego źródła gaze.

**Opis:** Dla emulacji MouseGaze zwykle jest to `configs/mouse_eyetracker_config.yaml`, a dla Tobii `configs/eyetracker_config.yaml` w katalogu upstream. Oryginalny punkt wejścia odczytuje plik także przy wyłączonej obsłudze trackera, dlatego dla NO_GAZE również potrzebna jest istniejąca ścieżka. GUI edytuje samą ścieżkę, nie zawartość konfiguracji urządzenia.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `gui.yaml_editor` — Edytor YAML

**Krótko:** Edytuje kopię YAML również poza polami formularzy, bez modyfikacji źródła.

**Opis:** Zakładka YAML pozwala zmienić pola niewystępujące w formularzach. Parser `ruamel.yaml` zachowuje istniejące komentarze i nierozpoznane klucze przy typowym zapisie dokumentu; nie gwarantuje identycznego formatowania bajt w bajt. Najpierw zastosuj zmiany do modelu w pamięci, a następnie jawnie zapisz profil lub wyeksportuj kopię.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `gui.profile` — Zapis profilu

**Krótko:** Zapisuje osobną kopię konfiguracji i preferencji bez nadpisywania dem.

**Opis:** Profil obejmuje robocze konfiguracje YAML, wybór źródła gaze, ścieżkę ioHub i przygotowane ustawienia uruchomienia. Metadane pozwalają zasygnalizować zmianę konfiguracji źródłowej od czasu utworzenia profilu. Zapis jest operacją w katalogu danych aplikacji, a nie w oryginalnym repozytorium silnika lub demonstracji.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `gui.instructions` — Instrukcje

**Krótko:** Treść ekranów początkowego i końcowego eksperymentu.

**Opis:** Pola instructions.intro oraz instructions.outro są listami tekstów wyświetlanych uczestnikowi. W edytorze formularzowym każda linia odpowiada jednemu elementowi listy YAML. Zmieniaj je z uwzględnieniem sposobu sterowania daną demonstracją oraz oczekiwanych odpowiedzi.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

## Dataset / output

### `dataset.image.path` — Katalog obrazów

**Krótko:** Ścieżka do katalogu obrazów, zwykle zawierającego podfoldery kategorii.

**Opis:** Silnik odczytuje obrazy z obsługiwanych formatów, takich jak JPG lub PNG. Nazwy podkatalogów mogą służyć jako etykiety klas w zbiorze obrazowym. Dla dem demonstracyjnych ścieżki względne rozwiązywane są względem root repozytorium dem.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.image.bbox_model` — Model bbox obrazów

**Krótko:** Wybiera metodę podziału bodźca obrazowego na obszary: grid, superpixel lub saliency.

**Opis:** Wartość wybiera strategię obszarów wykorzystywanych do powiązania danych spojrzenia z fragmentami obrazu. `grid` tworzy siatkę, `superpixel` stosuje segmentację, a `saliency` korzysta z mapy istotności. Nie oznacza uruchomienia modelu analitycznego w GUI; dostępność zależy od instalacji i kodu runtime.

**Dostępne wartości:**

- `grid` — Dzieli obraz na regularną siatkę prostokątnych obszarów.
- `superpixel` — Wyznacza regiony na podstawie lokalnie podobnych fragmentów obrazu (superpikseli).
- `saliency` — Wybiera regiony na podstawie mapy istotności wizualnej; wynik zależy od zastosowanego modelu.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.path` — Plik CSV z tekstami

**Krótko:** Ścieżka do pliku CSV z zadaniami tekstowymi i kolumnami danych.

**Opis:** Plik CSV musi mieć w pierwszym wierszu nagłówki kolumn. Powinien zawierać pola wskazane przez label_column_name i text_column_name. Dodatkowe kolumny mogą być wykorzystywane przez specyficzne adaptery danej demonstracji.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.label_column_name` — Kolumna etykiet

**Krótko:** Nazwa kolumny CSV określającej etykietę lub poprawną klasę.

**Opis:** Podaj dokładną nazwę kolumny istniejącej w nagłówku CSV, z zachowaniem wielkości liter. Silnik używa jej do określenia wartości etykiet dostępnych w zadaniu. Nie zmienia ona treści CSV i nie tworzy brakujących kolumn.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.text_column_name` — Kolumna tekstu

**Krótko:** Nazwa kolumny CSV zawierającej tekst prezentowany uczestnikowi.

**Opis:** Wartość musi wskazywać istniejące pole nagłówka CSV. W eksperymentach tekstowych dane z tej kolumny trafiają do wizualizacji bodźców. Nie należy zamieniać jej z kolumną etykiet, ponieważ pełnią odmienne role.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.bbox_model` — Model bbox tekstu

**Krótko:** Ustala poziom regionów tekstowych: word, line lub sentence.

**Opis:** Parametr określa sposób wyznaczania obszarów zainteresowania w tekście. Tryb word dzieli tekst na słowa, line na wiersze, a sentence na zdania. Zmiana wpływa na granulację późniejszej analizy spojrzeń, nie na zawartość CSV.

**Dostępne wartości:**

- `word` — Każde słowo jest osobnym obszarem analizy spojrzeń.
- `line` — Łączy tekst w regiony odpowiadające poszczególnym liniom widocznym na ekranie.
- `sentence` — Łączy tekst w regiony odpowiadające zdaniom, także gdy zdanie zajmuje kilka linii.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.color` — Kolor tekstu bodźca

**Krótko:** Kolor znaków w wizualizacji tekstowej PsychoPy.

**Opis:** Oryginalny config.yaml wymienia to pole w sekcji dataset.text jako opcjonalne ustawienie. Zestaw je z background_color tak, aby tekst był czytelny. Jeżeli pole nie występuje w danym demo, edytor formularzowy go nie dopisze automatycznie.

**Dostępność:** `yaml-only` — Tylko YAML; bez dedykowanego pola formularza

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.background_color` — Kolor tła tekstu

**Krótko:** Kolor tła bodźca tekstowego.

**Opis:** Ten parametr należy do ogólnej konfiguracji modalności tekstowej upstream. Dopasuj go do wartości color, aby zachować kontrast bodźców. W niektórych adapterach demonstracyjnych wygląd może być sterowany dodatkową logiką specyficzną dla danego demo.

**Dostępność:** `yaml-only` — Tylko YAML; bez dedykowanego pola formularza

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.text.font_height` — Wysokość fontu tekstu

**Krótko:** Wysokość czcionki bodźca tekstowego w adapterach dem.

**Opis:** To pole jest używane w dostarczonych konfiguracjach demonstracyjnych dla wybranych zadań tekstowych. Reguluje przestrzeń przeznaczoną na znaki bodźca, dlatego wpływa na zawijanie i pozycje obszarów zainteresowania. Nie jest częścią podstawowego przykładu ogólnego config.yaml upstream.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `dataset.text.wrap_fraction` — Udział szerokości dla tekstu

**Krótko:** Ułamek dostępnej szerokości ekranu używany do zawijania tekstu w demo.

**Opis:** W wybranych adapterach demonstracyjnych wartość dodatnia nie większa niż 1 określa, jaką część szerokości można wykorzystać do tekstu. Zmiana może wpływać na liczbę wierszy i współrzędne obszarów zainteresowania. Jest to rozszerzenie konfiguracji konkretnych dem, a nie gwarantowane pole uniwersalnego YAML upstream.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/mszac/tobii-pytracker-demo

### `dataset.time_series.path` — Plik CSV szeregów czasowych

**Krótko:** Ścieżka do CSV zawierającego próbki i klasy szeregów czasowych.

**Opis:** Oryginalny framework obsługuje dane time_series w formacie tabelarycznym. Pierwszy wiersz powinien zawierać nagłówki, w tym zdefiniowaną kolumnę etykiet. Demo Time-Series Noise zawiera dwa oddzielne bloki i osobne pliki konfiguracyjne.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.time_series.label_column_name` — Kolumna klas szeregu

**Krótko:** Nagłówek CSV wskazujący klasę danego szeregu.

**Opis:** Wskazana kolumna jest wykorzystywana jako etykieta dla danych time_series. Nazwa musi odpowiadać rzeczywistemu nagłówkowi dostarczonego pliku. Parametr sam nie przetwarza ani nie zmienia sygnału.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `dataset.time_series.bbox_model` — Model bbox szeregu

**Krótko:** Wybiera granice regionów szeregu: sample albo window.

**Opis:** Tryb sample umożliwia związanie regionu z pojedynczą próbką szeregu. Tryb window agreguje sąsiednie punkty w okno. Wybór ma znaczenie dla interpretacji późniejszych obszarów gaze na wykresie.

**Dostępne wartości:**

- `sample` — Poszczególne próbki wykresu są osobnymi obszarami analizy spojrzeń.
- `window` — Grupuje sąsiadujące próbki szeregu czasowego w większe okna analizy.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `output.folder` — Katalog wyników

**Krótko:** Folder docelowy dla plików wynikowych eksperymentu.

**Opis:** Ustawienie określa lokalizację wyników w oryginalnym silniku. Przy uruchamianiu z repozytorium dem ścieżka względna powinna być rozwiązywana zgodnie z jego katalogiem roboczym. Obecna wersja GUI tylko zapisuje i waliduje tę wartość, nie tworzy jeszcze sesji eksperymentalnej.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.folder` — Folder własnego modelu bbox

**Krótko:** Katalog zawierający opcjonalny zewnętrzny model wyznaczania regionów.

**Opis:** Upstream pozwala podać własny moduł modelu, gdy wbudowane strategie bbox są niewystarczające. Folder powinien zawierać importowalny kod zgodny z interfejsem CustomModel. Funkcja nie jest obecnie obsługiwana specjalnym formularzem GUI.

**Dostępność:** `yaml-only` — Tylko YAML; bez dedykowanego pola formularza

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.module` — Moduł własnego modelu bbox

**Krótko:** Nazwa modułu Pythona dostarczającego własny model obszarów.

**Opis:** Parametr jest wykorzystywany do wskazania klasy implementującej CustomModel. Odpowiedni kod musi być dostępny w runtime Pythona. Nie należy zmieniać nazwy bez sprawdzenia możliwości importu.

**Dostępność:** `yaml-only` — Tylko YAML; bez dedykowanego pola formularza

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `bbox_model.class` — Klasa własnego modelu bbox

**Krótko:** Nazwa klasy Python implementującej obsługę własnego bbox.

**Opis:** Klasa powinna realizować kontrakt CustomModel z metodami prepare_model, predict oraz process. Błędna nazwa powoduje brak możliwości wczytania niestandardowego modelu. Parametr pozostaje funkcją dla zaawansowanych użytkowników.

**Dostępność:** `yaml-only` — Tylko YAML; bez dedykowanego pola formularza

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

## Monitor

### `display.monitor.name` — Nazwa monitora

**Krótko:** Identyfikator profilu monitora używanego przez PsychoPy.

**Opis:** Podana nazwa identyfikuje ustawienia monitora w konfiguracji PsychoPy. Może wpływać na dopasowanie parametrów kalibracji i geometrii wyświetlania. Dobierz ją świadomie do stanowiska badawczego, aby nie pomylić profilu z innym ekranem.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.resolution` — Rozdzielczość ekranu

**Krótko:** Rozdzielczość wyświetlania bodźców w pikselach, jako para szerokość i wysokość.

**Opis:** Podaj szerokość i wysokość w pikselach w kolejności X, Y (np. `1920, 1080`). Parametr informuje PsychoPy i mechanizmy układu o geometrii, ale nie przełącza systemowej rozdzielczości Windows ani Linux. Zgodność z faktycznym monitorem trzeba sprawdzić na stanowisku.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.width` — Fizyczna szerokość ekranu

**Krótko:** Szerokość aktywnej części monitora w centymetrach.

**Opis:** Parametr jest używany razem z odległością obserwatora do określania geometrii widzenia. Podaj zmierzoną szerokość panelu, a nie jego przekątną w calach. Błędna wartość może zafałszować wielkości kątowe wyliczane przez PsychoPy.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.distance` — Odległość obserwatora

**Krótko:** Odległość oczu uczestnika od ekranu w centymetrach.

**Opis:** Wartość służy do konwersji współrzędnych przestrzennych na miary związane z kątem widzenia. Jest to przybliżenie standardowej pozycji uczestnika podczas eksperymentu. Dla badań z eye-trackerem ustawienie powinno odpowiadać rzeczywistemu stanowisku.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.monitor.display_number` — Numer ekranu

**Krótko:** Indeks ekranu, na którym PsychoPy ma wyświetlać eksperyment.

**Opis:** Numeracja rozpoczyna się od zera i zależy od kolejności ekranów widzianych przez system. Na stanowiskach wielomonitorowych przetestuj ustawienie przed sesją, by nie pokazać bodźców na ekranie operatora. W konfiguracji YAML zapisujemy wartość całkowitą.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

## Wygląd / layout

### `display.gui.button.size` — Rozmiar przycisków

**Krótko:** Szerokość i wysokość przycisków odpowiedzi w pikselach.

**Opis:** Wartość ma postać pary X i Y. Zmiana wielkości wpływa na obszary klikania oraz miejsce zajmowane przez odpowiedzi na ekranie. Należy przetestować ją łącznie z rozdzielczością i marginesami.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.margin` — Margines przycisków

**Krótko:** Odstęp używany przy rozmieszczaniu przycisków odpowiedzi.

**Opis:** Parametr określa przerwę między elementami sterowania w wizualizacji eksperymentu. Zbyt mały odstęp może utrudnić kliknięcie sąsiednich odpowiedzi. Jednostkę i wynik układu należy zweryfikować z renderowaniem konkretnego demo.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.color` — Kolor przycisków

**Krótko:** Kolor tła przycisków odpowiedzi.

**Opis:** Podawany jako kolor rozpoznawany przez PsychoPy w danej konfiguracji. Powinien kontrastować z kolorem tekstu przycisku. Zmiana wpływa tylko na prezentację, nie na znaczenie odpowiedzi.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.text.color` — Kolor tekstu przycisku

**Krótko:** Kolor podpisów przycisków odpowiedzi.

**Opis:** Wybierz barwę zapewniającą czytelność na wybranym tle button.color. Parametr dotyczy wizualizacji etykiet przycisków, a nie tekstu samego bodźca. Nie wpływa na rejestrowanie gaze ani na kody odpowiedzi.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.button.text.size` — Wielkość tekstu przycisku

**Krótko:** Rozmiar czcionki etykiet przycisków w ustawieniach GUI eksperymentu.

**Opis:** Wyższa liczba zwiększa podpisy odpowiedzi. Przy długich etykietach i małych przyciskach tekst może przestać się mieścić. Sprawdź podgląd w rzeczywistym PsychoPy, gdy uruchamianie demo zostanie włączone.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.fixation_dot.size` — Rozmiar punktu fiksacji

**Krótko:** Wielkość znacznika fiksacji na ekranie eksperymentu.

**Opis:** Znacznik może pomagać uczestnikowi skupić wzrok przed prezentacją bodźca. Parametr steruje rozmiarem tego elementu UI. Jego obecność i czas pokazywania zależą także od przebiegu konkretnego eksperymentu.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.fixation_dot.color` — Kolor punktu fiksacji

**Krótko:** Kolor znacznika używanego do fiksacji wzroku.

**Opis:** Ustaw go tak, aby punkt był widoczny na tle danej demonstracji. Jest to parametr wizualny, niezależny od surowego pomiaru eye-trackera. Nie należy mylić tego znacznika z elementami kalibracji ioHub.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `display.gui.aoe` — Obszar AOE

**Krótko:** Rozmiar obszaru układu eksperymentu (AOE), nie lista obszarów AOI bodźca.

**Opis:** W głównym YAML jest to para liczb definiująca rozmiar obszaru eksperymentu wykorzystywanego w układzie. AOE nie jest listą regionów zainteresowania (AOI) wyliczonych dla pojedynczego obrazu, tekstu czy szeregu. Jednostkę i działanie należy rozpatrywać wraz z konfiguracją PsychoPy i danego demo.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `instructions.intro` — Instrukcje przed startem

**Krótko:** Lista kolejnych linii instrukcji wyświetlanych przed eksperymentem.

**Opis:** Każda linia w edytorze GUI staje się oddzielnym elementem listy YAML. W instrukcji można opisać przebieg zadania, sterowanie i sposób rozpoczęcia. Treść powinna odpowiadać aktualnemu demo, szczególnie po zmianie sposobu rejestracji gaze.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

### `instructions.outro` — Instrukcje po zakończeniu

**Krótko:** Lista komunikatów pokazywanych po ukończeniu demonstracji.

**Opis:** Pole definiuje komunikat końcowy dla uczestnika. Może wyjaśniać, że sesja dobiegła końca i jak zamknąć PsychoPy. Sam komunikat nie jest dowodem poprawności zapisania wyników, dlatego nie należy obiecywać zapisu bez potwierdzenia runtime.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#configuration

## Parametry uruchomienia

### `runtime.config_file` — --config_file

**Krótko:** Wskazuje główny YAML eksperymentu przekazywany oryginalnemu runtime.

**Opis:** Oryginalne CLI udostępnia `--config_file`; GUI nie uruchamia już skryptu shell z domyślnymi plikami. W v0.1.5 tworzy poza repozytoriami nową kopię aktualnie edytowanego YAML i przekazuje jej ścieżkę do `CustomConfig` w osobnym procesie. Ścieżki dataset są rozwiązywane względem katalogu głównego repozytorium dem.

**Dostępność:** `reference` — Referencyjna opcja upstream/CLI; nie zawsze ma oddzielne pole edycji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.eyetracker_config_file` — --eyetracker_config_file

**Krótko:** Ścieżka do pliku YAML urządzenia obsługiwanego przez ioHub.

**Opis:** Parametr CLI wskazuje konfigurację używaną przez launchHubServer. Należy go powiązać z wyborem MouseGaze lub Tobii. W upstream plik jest wczytywany także przy wyłączonym rejestrowaniu gaze, więc ścieżka powinna istnieć.

**Dostępność:** `reference` — Referencyjna opcja upstream/CLI; nie zawsze ma oddzielne pole edycji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.enable_eyetracker` — --enable_eyetracker

**Krótko:** Włącza zbieranie gaze przez ioHub dla MouseGaze lub Tobii podczas startu.

**Opis:** Flaga `enable_eyetracker` ma wartość True dla MOUSEGAZE i TOBII oraz False dla NO_GAZE. Konkretny sterownik wybiera osobny plik YAML ioHub. Nawet przy NO_GAZE upstream wymaga istniejącej ścieżki do pliku konfiguracyjnego, a odpowiedzi myszą pozostają aktywne. Ta wersja przekazuje flagę do `main.main`, ale nie potwierdza sprzętowej gotowości urządzenia.

**Dostępne wartości:**

- `True` — Włącza ioHub i rejestrowanie zdarzeń wybranego trackera, zgodnie z konfiguracją YAML.
- `False` — Pomija inicjalizację trackera; odpowiedzi i inne włączone kanały mogą nadal działać.

**Dostępność:** `reference` — Referencyjna opcja upstream/CLI; nie zawsze ma oddzielne pole edycji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.enable_voice` — Voice / --enable_voice

**Krótko:** Wybiera nagrywanie głosu i przekazuje opcję do oryginalnego procesu eksperymentu.

**Opis:** Podczas uruchamiania GUI przekazuje `enable_voice` do `main.main`, również dla dem wykorzystujących adaptery. Tryb potrzebuje poprawnie skonfigurowanego mikrofonu i funkcjonującego toru audio w środowisku PsychoPy. Pomyślny start procesu nie stanowi dowodu, że nagranie dźwiękowe zostało utworzone; należy sprawdzić rezultat na docelowym Windows/Linux.

**Dostępne wartości:**

- `True` — Żąda nagrywania mikrofonem; wymaga urządzenia i działającej obsługi głosu.
- `False` — Nie uruchamia nagrywania mikrofonu dla sesji.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.raw_data` — Raw data / --raw_data

**Krótko:** Wybiera surowy zapis gaze i przekazuje ustawienie do runtime eye-trackera.

**Opis:** Opcja `raw_data` jest przekazywana do oryginalnego silnika, także w demonstracjach z adapterami. Wymaga trybu gaze MOUSEGAZE albo TOBII; GUI blokuje połączenie Raw data z NO_GAZE. Format i kompletność surowych danych zależą od wersji ioHub i urządzenia i wymagają weryfikacji na fizycznym stanowisku.

**Dostępne wartości:**

- `True` — Żąda pełnych, surowych zdarzeń trackera zamiast zwykłych przetworzonych próbek spojrzeń.
- `False` — Wybiera standardową ścieżkę ekstrakcji próbek spojrzeń zamiast surowych zdarzeń.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.disable_psychopy` — --disable_psychopy

**Krótko:** Uruchamia tryb headless bez okna PsychoPy.

**Opis:** Upstream udostępnia ten wariant do ciągłego zbierania gaze i voice aż do zatrzymania. Nie jest to zwykły tryb przeprowadzania obecnych siedmiu demonstracji. Dlatego GUI M1 nie oferuje jeszcze tego przełącznika.

**Dostępne wartości:**

- `True` — Żąda działania bez okien bodźców PsychoPy, jeśli obsługuje to uruchomiony tryb upstream.
- `False` — Uruchamia zwykłe, widoczne próby PsychoPy i ich elementy odpowiedzi.

**Dostępność:** `future` — Funkcja oryginalnego silnika, odroczona w GUI

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.loop_count` — Liczba prób / --loop_count

**Krótko:** Ustawia liczbę prób wykonywanych w bieżącym bloku demonstracji.

**Opis:** GUI przekazuje liczbę prób do `main.main` i ogranicza ją do zdefiniowanego zakresu danego bloku. W Time-Series Noise są dwa osobne procesy: Machine, następnie PV, z niezależną liczbą prób maksymalnie 9 w każdym. Przy wartości mniejszej od pełnej długości sesji oryginalne walidatory, które oczekują pełnego zestawu, są pomijane, a kolekcja zostaje oznaczona jako niezweryfikowana.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

### `runtime.log_level` — Log level / --log_level

**Krótko:** Ustawia poziom szczegółowości logów procesu eksperymentu.

**Opis:** Podczas uruchamiania GUI konfiguruje `CustomLogger` w odrębnym procesie wybranym poziomem debug, info, warning, error albo critical. Standardowe wyjście i błędy są zbierane do trwałego `console.log` w prywatnym katalogu sesji. Wyższa szczegółowość może pomóc w diagnozie problemów, lecz nie zastępuje walidacji zebranych wyników.

**Dostępne wartości:**

- `debug` — Szczegółowe komunikaty diagnostyczne pomagające odtwarzać przebieg i błędy.
- `info` — Typowe komunikaty cyklu życia i istotnych zdarzeń; zalecany poziom.
- `warning` — Ostrzeżenia i błędy, bez zwykłych komunikatów informacyjnych.
- `error` — Tylko błędy i sytuacje krytyczne; bez ostrzeżeń.
- `critical` — Wyłącznie błędy najwyższej wagi; obsługiwane przez CLI upstream.

**Dostępność:** `gui` — Pole lub preferencja GUI; przy uruchomieniu stosowana zgodnie z obsługą danej funkcji

**Źródło:** https://github.com/sbobek/tobii-pytracker#usage

## ioHub / eye-tracker (manual; nieedytowane obecnie)

### `iohub.mouse.name` — MouseGaze name

**Krótko:** Nazwa urządzenia emulowanego w instancji ioHub.

**Opis:** Oryginalny plik nazywa je tracker. Ta nazwa pozwala odwoływać się do urządzenia w kontekście ioHub. Zmiana bez modyfikacji kodu klienta może spowodować brak dostępu do urządzenia.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.mouse.auto_report_events` — MouseGaze auto_report_events

**Krótko:** Wskazuje, czy MouseGaze zaczyna zgłaszać zdarzenia automatycznie.

**Opis:** Gdy False, raportowanie wymaga jawnego włączenia przez odpowiednią metodę API. Domyślna konfiguracja upstream używa False. Zmiana wpływa na cykl rejestrowania i wymaga testu runtime.

**Dostępne wartości:**

- `True` — Automatycznie wysyła zdarzenia po inicjalizacji urządzenia lub eksperymentu.
- `False` — Zdarzenia nie są zgłaszane, dopóki raportowanie nie zostanie jawnie włączone.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.save_events` — save_events

**Krótko:** Określa, czy zdarzenia gaze są zapisywane przez ioHub.

**Opis:** Przełącznik wpływa na zachowanie magazynu zdarzeń ioHub. Nie zastępuje opcji eksportu danych samego eksperymentu. Wyłączenie może uniemożliwić późniejszą analizę części rejestracji.

**Dostępne wartości:**

- `True` — Zapisuje obsługiwane zdarzenia urządzenia w magazynie zdarzeń ioHub.
- `False` — Nie zapisuje zdarzeń w magazynie ioHub; nie jest to ustawienie zapisu wynikowego CSV eksperymentu.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.stream_events` — stream_events

**Krótko:** Określa, czy ioHub przesyła zdarzenia do procesu eksperymentu.

**Opis:** Wartość True pozwala aplikacji pobierać bieżące próbki. Przy False część obliczeń na żywo może nie otrzymywać danych. Ustawienie jest osobne od zapisywania zdarzeń.

**Dostępne wartości:**

- `True` — Przesyła zdarzenia trackera do procesu eksperymentu podczas rejestracji.
- `False` — Wyłącza strumieniowanie na żywo; zadania zależne od spojrzeń mogą nie działać.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.event_buffer_length` — event_buffer_length

**Krótko:** Limit liczby zdarzeń przechowywanych w buforze ioHub.

**Opis:** Po osiągnięciu limitu stare zdarzenia mogą być nadpisywane. Zbyt mała wartość podnosi ryzyko utraty danych podczas zatorów. Zbyt duża zwiększa zapotrzebowanie na pamięć.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.common.monitor_event_types` — monitor_event_types

**Krótko:** Lista typów zdarzeń, które ioHub ma odbierać lub udostępniać.

**Opis:** MouseGaze pozwala rejestrować między innymi próbki monokularne oraz zdarzenia fiksacji, sakad i mrugnięć. Tobii używa własnego typu próbek binokularnych. Nie należy kopiować listy bezpośrednio pomiędzy sterownikami różnych urządzeń.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.enable` — Calibration enable

**Krótko:** Włącza kalibrację urządzenia obsługiwanego przez ioHub.

**Opis:** Występuje w konfiguracji MouseGaze jako ustawienie calibration.enable. Ustawienie kalibracji może mieć inne znaczenie w zależności od sterownika. Przed użyciem na sprzęcie sprawdź zachowanie ioHub.

**Dostępne wartości:**

- `True` — Włącza kalibrację, jeśli jest obsługiwana przez wybrany sterownik.
- `False` — Pomija kalibrację, jeśli sterownik pozwala; dokładność może być niższa.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.type` — Calibration type

**Krótko:** Wybiera liczbę punktów kalibracji: THREE, FIVE albo NINE.

**Opis:** Więcej punktów może ułatwić dopasowanie kalibracji na większym obszarze ekranu. Obsługiwane tryby zależą od implementacji sterownika. Oryginalne przykłady używają THREE_POINTS.

**Dostępne wartości:**

- `THREE_POINTS` — Kalibracja w trzech punktach; najkrótszy dostępny wzór.
- `FIVE_POINTS` — Kalibracja w pięciu punktach, z większym pokryciem obszaru.
- `NINE_POINTS` — Kalibracja w dziewięciu punktach, gęstsza, ale dłuższa.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.randomize` — Calibration randomize

**Krótko:** Decyduje o losowej kolejności punktów kalibracji.

**Opis:** Przy True kolejność wyświetlania punktów może się zmieniać. Przy False punkty mogą następować w ustalonym porządku. Wybierz ustawienie zgodne z protokołem badania.

**Dostępne wartości:**

- `True` — Losuje kolejność odwiedzania punktów kalibracyjnych.
- `False` — Zachowuje kolejność punktów określoną w konfiguracji.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.auto_pace` — Calibration auto_pace

**Krótko:** Automatycznie przełącza punkty kalibracji bez dodatkowego klikania.

**Opis:** Gdy True, przejście między punktami odbywa się w oparciu o czas. Przy False operator lub uczestnik może musieć potwierdzić dalszy krok. Zależy to od implementacji ioHub.

**Dostępne wartości:**

- `True` — Automatycznie przechodzi do następnego punktu po czasie pacing_speed.
- `False` — Wymaga potwierdzenia przejścia; pacing_speed nie steruje wtedy tempem.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.pacing_speed` — Calibration pacing_speed

**Krótko:** Czas ekspozycji punktu kalibracji przy automatycznym przejściu.

**Opis:** Parametr wyrażany jest w sekundach dla auto_pace True. Przy auto_pace False jest ignorowany w oryginalnej konfiguracji. Zbyt krótka ekspozycja może utrudnić poprawną fiksację.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.screen_background_color` — Calibration background

**Krótko:** Kolor tła ekranu kalibracyjnego.

**Opis:** Jest to oddzielne ustawienie od tła bodźców eksperymentalnych. Dobre zestawienie z barwami celu kalibracyjnego zwiększa jego czytelność. Konfiguracja przykładowa ustawia tło na czarne.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_type` — Calibration target type

**Krótko:** Typ grafiki pokazywanej jako cel kalibracji.

**Opis:** Oryginalny sterownik Tobii obsługuje CIRCLE_TARGET. Dostępność innych typów zależy od implementacji. Zmieniaj tylko po weryfikacji wsparcia urządzenia.

**Dostępne wartości:**

- `CIRCLE_TARGET` — Rysuje udokumentowany cel kalibracyjny z dwoma okręgami, według zewnętrznej i wewnętrznej średnicy.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.color_type` — Calibration color type

**Krótko:** Sposób interpretacji wartości kolorów celów kalibracyjnych.

**Opis:** W udostępnionym pliku ioHub używane jest rgb. Nie jest to parametr barwy samego tekstu ani przycisków eksperymentu. Wartości muszą być zgodne z wymaganiami PsychoPy.

**Dostępne wartości:**

- `rgb` — Interpretuje kolory celu kalibracyjnego jako RGB; tryb pokazany w dostarczonym YAML.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.unit_type` — Calibration unit type

**Krótko:** Jednostka współrzędnych i rozmiarów elementów kalibracji.

**Opis:** Konfiguracja przykładowa używa pix. Zmiana jednostek wymaga konsekwentnego przeliczenia rozmiarów i ruchów celu. Nie należy jej wykonywać bez testu wyświetlania.

**Dostępne wartości:**

- `pix` — Interpretuje geometrię celu w pikselach zgodnie z dostarczonym YAML.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_diameter` — Outer diameter

**Krótko:** Średnica zewnętrznego koła celu kalibracji.

**Opis:** Pierścień zewnętrzny jest rysowany przed częścią wewnętrzną. W pliku upstream wielkość podawana jest w jednostkach kalibracji, domyślnie w pikselach. Należy zachować proporcje względem inner_diameter.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_stroke_width` — Outer stroke width

**Krótko:** Grubość konturu zewnętrznego okręgu kalibracji.

**Opis:** Wartość steruje widoczną krawędzią zewnętrznego pierścienia. Współdziała z jego kolorem oraz wypełnieniem. Zbyt cienki kontur może być słabo widoczny.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_fill_color` — Outer fill color

**Krótko:** Kolor wypełnienia zewnętrznego okręgu.

**Opis:** Okrąg zewnętrzny jest częścią wizualnego celu kalibracji. Ustawienie działa niezależnie od obramowania. Wybierz kolor zapewniający kontrast względem tła kalibracji.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.outer_line_color` — Outer line color

**Krótko:** Kolor obwódki zewnętrznego okręgu.

**Opis:** Barwa jest używana razem z outer_stroke_width. Należy dobrać ją do tła i wypełnienia. Zmiana nie wpływa na strumień próbek gaze.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_diameter` — Inner diameter

**Krótko:** Średnica środkowego, mniejszego punktu kalibracji.

**Opis:** Wewnętrzne koło jest nakładane na zewnętrzny cel. Zwykle powinno być mniejsze od outer_diameter. Pomaga uczestnikowi utrzymywać precyzyjną fiksację.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_stroke_width` — Inner stroke width

**Krótko:** Grubość konturu wewnętrznego punktu.

**Opis:** Parametr określa szerokość linii narysowanej wokół środka celu. Wpływa tylko na jego prezentację. Wartość powinna pasować do rozdzielczości i rozmiaru wewnętrznego koła.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_fill_color` — Inner fill color

**Krótko:** Kolor wypełnienia wewnętrznego punktu.

**Opis:** Kolor powinien odcinać się od wypełnienia zewnętrznego. W źródłowych ustawieniach stosowana jest szarość. Ułatwia rozróżnienie centrum celu kalibracyjnego.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.inner_line_color` — Inner line color

**Krótko:** Kolor konturu wewnętrznego koła.

**Opis:** Jest to barwa linii rysowanej na krawędzi wewnętrznego punktu. Stosowana jest wraz z inner_stroke_width. Nie zmienia parametrów rejestrowania ani modelu gaze.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.enable` — Animation enable

**Krótko:** Włącza animowany ruch celu kalibracyjnego.

**Opis:** Gdy False, cel może przechodzić skokowo między pozycjami. Gdy True, wykorzystywane są ustawienia prędkości i skalowania. Działanie jest zależne od implementacji ioHub.

**Dostępne wartości:**

- `True` — Animuje przejścia i zmianę wielkości celu zgodnie z ustawieniami ruchu i rozszerzania.
- `False` — Wyłącza animację; cel może pojawić się od razu w kolejnym położeniu.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.movement_velocity` — Movement velocity

**Krótko:** Prędkość przesuwania się celu kalibracji w pikselach na sekundę.

**Opis:** Wartość reguluje płynny ruch do kolejnej pozycji. Zbyt szybki ruch może być trudny do śledzenia wzrokiem. Ustawienie działa w połączeniu z włączeniem animacji.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.expansion_ratio` — Expansion ratio

**Krótko:** Maksymalne powiększenie zewnętrznego koła celu.

**Opis:** Wartość jest mnożnikiem outer_diameter. Dla 1.0 cel nie ulega powiększeniu. Większe wartości tworzą silniej widoczną animację celu.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.expansion_speed` — Expansion speed

**Krótko:** Tempo zmiany średnicy celu w pikselach na sekundę.

**Opis:** Parametr określa szybkość powiększania okręgu podczas animacji. Wpływa na wrażenie ruchu celu. Nie zmienia szybkości próbkowania Tobii ani MouseGaze.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.calibration.target_attributes.animate.contract_only` — Contract only

**Krótko:** Ogranicza animację rozmiaru do kurczenia celu.

**Opis:** Gdy True, cel może przechodzić tylko od stanu powiększonego do normalnego. Przy False może najpierw rosnąć i następnie maleć. Działanie wymaga włączonej animacji.

**Dostępne wartości:**

- `True` — Rozpoczyna od powiększonego celu i zmniejsza go do rozmiaru bazowego.
- `False` — Najpierw powiększa cel, a następnie ponownie go zmniejsza.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.runtime_settings.sampling_rate` — Sampling rate

**Krótko:** Żądana częstotliwość próbkowania eye-trackera w Hz, zależna od sterownika.

**Opis:** MouseGaze w konfiguracji upstream przewiduje 50 lub 100 Hz, natomiast przykładowy Tobii podaje 60 Hz. Wartość jest ustawieniem sterownika ioHub, a nie przełącznikiem częstotliwości monitora. Urządzenie fizyczne może nie obsługiwać danej częstotliwości; GUI jej nie negocjuje ani nie weryfikuje sprzętowo.

**Dostępne wartości:**

- `MouseGaze: 50 Hz` — Emulator próbuje generować 50 próbek na sekundę; domyślna wartość MouseGaze.
- `MouseGaze: 100 Hz` — Druga dokumentowana częstotliwość MouseGaze; zwiększa liczbę zdarzeń.
- `Tobii: device-supported rate` — Dostępne częstotliwości zależą od modelu Tobii; przykładowa konfiguracja wskazuje 60 Hz.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.runtime_settings.track_eyes` — Track eyes

**Krótko:** Określa, z którego oka pochodzą próbki gaze.

**Opis:** Oryginalny MouseGaze zgłasza próbki monokularne RIGHT_EYE. Sterownik Tobii w tym repozytorium opisuje tryb BINOCULAR. Nie należy zmieniać tych wartości na nieobsługiwane przez dany sterownik.

**Dostępne wartości:**

- `RIGHT_EYE` — Zdarzenia tylko prawego oka w emulatorze MouseGaze.
- `BINOCULAR` — Zdarzenia obuoczne sterownika Tobii; nie jest to tryb emulatora MouseGaze.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.move` — MouseGaze move

**Krótko:** Przycisk wyzwalający symulowane próbki gaze w źródłowym MouseGaze.

**Opis:** Źródłowy sterownik ioHub MouseGaze ma ustawienie `controls.move`, domyślnie `RIGHT_BUTTON`. Przycisk wykorzystywany do symulacji gaze należy odróżniać od lewego kliknięcia odpowiedzi. Ta dokumentacja opisuje upstream; niestandardowe adaptery mogą implementować inną politykę przycisku.

**Dostępne wartości:**

- `LEFT_BUTTON` — Lewy przycisk myszy generuje aktualizacje pozycji spojrzenia; może kolidować z obsługą odpowiedzi.
- `MIDDLE_BUTTON` — Środkowy przycisk myszy generuje aktualizacje pozycji spojrzenia.
- `RIGHT_BUTTON` — Prawy przycisk myszy generuje aktualizacje spojrzenia; domyślnie w dostarczonym YAML MouseGaze.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.blink` — MouseGaze blink

**Krótko:** Kombinacja przycisków emulująca mrugnięcie w MouseGaze.

**Opis:** Źródłowy MouseGaze korzysta z kombinacji lewego i prawego przycisku do symulacji zdarzenia mrugnięcia. Przytrzymywanie przycisku gaze podczas klikania odpowiedzi może więc prowadzić do konfliktów gestów. Ustawienie dotyczy emulacji ioHub, nie wykrywania fizycznego mrugania przez Tobii.

**Dostępne wartości:**

- `LEFT_BUTTON` — Lewy przycisk może symulować mrugnięcie, jeśli jest wymieniony w konfiguracji.
- `MIDDLE_BUTTON` — Środkowy przycisk może symulować mrugnięcie, jeśli jest wymieniony w konfiguracji.
- `RIGHT_BUTTON` — Prawy przycisk może symulować mrugnięcie, jeśli jest wymieniony w konfiguracji.
- `[LEFT_BUTTON, RIGHT_BUTTON]` — Oba wymienione przyciski mogą symulować mrugnięcia; tak skonfigurowano przykład.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.controls.saccade_threshold` — Saccade threshold

**Krótko:** Próg detekcji sakad w stopniach kąta widzenia.

**Opis:** Parametr należy do sterownika MouseGaze i steruje generowaniem syntetycznych zdarzeń sakad. Nie jest progiem rozpoznawania kliknięć ani filtrowaniem Tobii w trybie raw_data. Interpretacja zależy od geometrii ekranu.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/mouse_eyetracker_config.yaml

### `iohub.tobii.enable` — Tobii enable

**Krótko:** Decyduje, czy ioHub ładuje fizyczny sterownik Tobii.

**Opis:** W oryginalnym pliku ustawienie jest włączone. Oprogramowanie musi mieć dostęp do kompatybilnego urządzenia. Włączenie opcji nie zastępuje fizycznego podłączenia i sprawdzenia sterowników.

**Dostępne wartości:**

- `True` — Włącza sterownik Tobii w ioHub, gdy również konfiguracja główna zezwala na śledzenie wzroku.
- `False` — Wyłącza konfigurację urządzenia Tobii; fizyczny tracker nie będzie tu inicjalizowany.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.model_name` — Tobii model_name

**Krótko:** Opcjonalny filtr konkretnego modelu eye-trackera.

**Opis:** Jeżeli nazwa modelu jest podana, ioHub szuka urządzeń zgodnych z filtrem. Gdy podłączony jest jeden zgodny Tobii, pole można zostawić puste. Nieprawidłowy filtr może powodować pozorny brak urządzenia.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.serial_number` — Tobii serial_number

**Krótko:** Opcjonalny filtr numeru seryjnego fizycznego urządzenia Tobii.

**Opis:** Numer seryjny może być potrzebny, gdy dostępnych jest kilka kompatybilnych trackerów. Puste ustawienie nie wymusza konkretnego urządzenia, a błędne może uniemożliwić wybór. GUI nie skanuje urządzeń ani nie weryfikuje numerów seryjnych.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

### `iohub.tobii.manufacturer_name` — Tobii manufacturer_name

**Krótko:** Informacyjna nazwa producenta zapisywana w konfiguracji ioHub.

**Opis:** Oryginalny przykład podaje Tobii Technology. Pole pełni rolę metadanych i nie określa sposobu kalibracji. Nie zastępuje model_name ani serial_number.

**Dostępność:** `iohub-only` — Konfiguracja ioHub; GUI wybiera wyłącznie ścieżkę do pliku

**Źródło:** https://raw.githubusercontent.com/sbobek/tobii-pytracker/main/configs/eyetracker_config.yaml

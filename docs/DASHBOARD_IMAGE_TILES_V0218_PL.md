# Panel główny: kafelki graficzne o stałym rozmiarze (v0.2.18)

Zakres: wyłącznie ekran Home otwierany przez kliknięcie napisu `pytracker-gui` w lewym górnym rogu.

- Cztery dotychczasowe akcje prowadzą nadal do Experiment, Logs, Statistics i Manual. Przyciski wykorzystują cztery grafiki zaakceptowane przez użytkownika, a nie nowe ilustracje.
- Zasoby to zoptymalizowane, lokalne pliki PNG RGB o stałej rozdzielczości **546 × 365 pikseli**. Każdy zajmuje około 200–220 KiB wobec pierwotnych 1,8–2 MB. Napisy na dostarczonych grafikach pozostają angielskie niezależnie od języka interfejsu; metadane przycisków nadal są tłumaczone.
- Przyciski ttk nie zmieniają rozmiaru podczas powiększania i pomniejszania okna. Gdy małe okno nie mieści całego układu 2×2, natywny Canvas wyświetla paski przewijania tylko przy potrzebie. Przy starcie paski nie występują.
- Obrazki są wczytywane jednokrotnie, dopiero przy otwarciu Home. Nie ma timerów, nowych wątków, przeliczania grafiki podczas działania ani zależności od Pillow w runtime. Skalowanie i kadrowanie wykonano przy przygotowaniu wydania.
- Bez zmian pozostają ekrany, uruchamianie PsychoPy, YAML, projekty, Logs, Manual, Statistics, globalny motyw, ustawienia i persistence.

Weryfikacja: stała geometria czterech kafelków przed/po resize, paski przewijania, kliknięcia, zmiana języka, zawartość pakietów Full i Commit Ready oraz integralność sum SHA-256.

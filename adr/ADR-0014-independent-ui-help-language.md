# ADR-0014 — osobny język GUI i krótkiej pomocy (2026-10-11)

**Stan:** accepted for v0.1.3.

**Kontekst:** v0.1.2 ma polską warstwę GUI i pełny polski manual 87 parametrów. Użytkownik chce pozostawić je bez zmian, ale mieć alternatywny angielski interfejs i możliwość wyboru polskich podpowiedzi przy angielskim GUI; nie chce jeszcze pełnego angielskiego manuala.

**Decyzja:** osobno zapamiętywane kody `language` i `help_language`, `pl` jako domyślny, `en` jako alternatywa. Język dymków podąża za GUI, dopóki użytkownik nie dokona jawnego wyboru. Tłumaczenia krótkich podpowiedzi są wyłącznie overlay do oryginalnych 87 polskich rekordów. Istniejący polski manual i jego generator pozostają źródłem prawdy dla opisów pełnych. Tekst formularzy tłumaczony jest po stronie prezentacji, nigdy przez podmienianie wartości YAML, identyfikatorów pól lub profili. Przełączenie języka musi zachować poprawne niezapisane edycje i zatrzymać się na błędnym YAML.

**Alternatywy odrzucone:** dwa osobne kodowe warianty GUI (rozbieżności funkcji); przełączenie całego słownika i kluczy YAML (ryzyko uszkodzenia profili); wygenerowanie pełnego angielskiego manuala teraz (poza zakresem); automatyczne tłumaczenie online (niedeterministyczność, sieć).

**Ograniczenia:** brak linku do manuala w GUI; brak fizycznego testu Windows/Tobii; obsługa EN obejmuje interfejs i krótkie dymki, nie długie opisy dokumentacji.

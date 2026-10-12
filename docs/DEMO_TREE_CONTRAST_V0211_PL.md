# v0.2.11 — kontrast drzewa dokumentacji dem (PL)

Poprawka dotyczy wyłącznie lewej listy w **Manual → Demo Project Documentation**. Pod Windows widżet `ttk.Treeview` używał jasnego tła przy jasnym tekście, ponieważ globalnie skonfigurowano nieużywany styl `TTreeview` zamiast właściwego `Treeview`.

Nowy, lokalny styl `DemoDocs.Treeview` jawnie ustawia ciemne tło pól (`#161e26`), jasny tekst (`#f2f5f9`) oraz pomarańczowe zaznaczenie (`#ff8931`) z ciemnym tekstem. Nie zmieniono globalnego motywu, rozmiarów, renderera Markdown/RST ani innych funkcjonalności. Test obejmuje zwykły i zaznaczony wiersz.

Sprawdzenie fizyczne na Windows pozostaje otwarte: skontrolować kontrast nazw projektów, plików i aktywnego wiersza, także po ponownym otwarciu zakładki.

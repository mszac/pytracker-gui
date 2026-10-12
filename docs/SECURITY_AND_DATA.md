# Dane, bezpieczeństwo i odtwarzalność

1. GUI wykonuje tylko z góry zdefiniowane Python entrypoints i argumenty w listach (`shell=False`). Ścieżki użytkownika nie są poleceniami.
2. Podstawowy tryb nie ładuje obcego kodu z projektu; custom models są osobną jawnie autoryzowaną funkcją ekspercką.
3. Konfiguracji źródłowych upstream i demo nie edytuje się in-place. Trwałe projekty i runs przechowuje się w katalogu użytkownika, z atomic write i kopią manifestu.
4. Logi nie zbierają treści surowych gaze/voice, nie wyświetlają sekretów i unikają automatycznego indeksowania prywatnych plików. Raport diagnostyczny ma redakcję ścieżek osobowych na żądanie.
5. Badacz sam odpowiada za zgodę uczestnika, zasady przechowywania, retencję oraz RODO; GUI umożliwia pseudonimowe ID i wyjaśnia gdzie dane są zapisywane.
6. `raw_data`, `enable_voice` są jawne, default OFF. Nigdy nie zaczynać headless recording bez widocznej informacji w GUI i pozytywnego działania użytkownika.
7. Zatrzymanie procesów jest stopniowe: upstream-native exit -> informacja o ryzyku utraty danych -> emergency kill tylko po potwierdzeniu.
8. Snapshot SHA: upstream commit + demo commit/archive hash + config + referenced data manifest + run command + versions. Wskaźnik `REPRODUCIBLE/EXTERNAL_DATA_UNSNAPSHOTTED`.
9. Dla Docker obowiązuje oddzielne mapowanie ścieżek i jawny bind-mount; nie skanować/udostępniać dowolnych katalogów hosta automatycznie.

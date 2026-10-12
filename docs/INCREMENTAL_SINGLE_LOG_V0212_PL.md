# v0.2.12 — jeden narastający dziennik o niskim priorytecie

## Kontrakt

Każdy run w `projects/<project>/experiments/<timestamp>_<ID>/` tworzy tylko jeden trwały dziennik: `experiment_<start_timestamp>_<ID>.log.part`. Osobny `console_*.log` nie powstaje. Komunikaty `[RUN]`, `[STATUS]`, tekst stdout/stderr procesu, `[PROCESS]` oraz `[FINAL]` trafiają do tego samego strumienia w oryginalnej kolejności. Po pomyślnym zakończeniu i utrwaleniu bez utraty danych plik jest przemianowany atomowo na `.log`. Pliki `.part` pozostają po anulowaniu, wyjątkach, przepełnieniu, błędach I/O lub nagłej śmierci procesu. Na tym etapie **nie ma odzyskiwania ani naprawy**. Dla anulowania zapisujemy również `[LOG] INTERRUPTED` i `result.json` nadal wskazuje `CANCELLED`.

## Priorytet i wydajność

Wątek odczytujący stdout nie pisze na dysk: umieszcza komunikaty w ograniczonej kolejce RAM. **Limit 256 KiB nie został zmieniony**; przy przeciążeniu FIFO wypiera najstarsze *jeszcze niezapisane* komunikaty. Po odblokowaniu zapisu w dzienniku pojawia się licznik `[LOG] BUFFER_OVERFLOW: <bytes> ...`, a dziennik zostaje `.part`, aby nie udawać kompletnego. Wątek zapisujący jest niezależny (daemon), ma obniżony priorytet w Windows i pozostaje uśpiony przez większość czasu. Próba zapisu następuje co ok. 15 s lub po osiągnięciu 192 KiB bufora; przy nacisku nie częściej niż ok. co 5 s. Porcje wynoszą do 64 KiB. `fsync()` i zmiana nazwy następują dopiero po zakończeniu sesji i tylko w wątku zapisującym.

To **best effort**, nie gwarancja wykrywania wolnego dysku; zewnętrzne obciążenie nośnika nadal może spowodować opóźnienia zapisującego wątku. Niedostępny dysk może spowodować utratę starszych, niezapisanych wpisów. Zanik zasilania przed synchronizacją może utracić najnowszy fragment. Brak miejsca na dysku może uniemożliwić nawet utworzenie `.part`.

## Bez zmian

Istniejący 256-KiB `SpooledTemporaryFile` w GUI, limit widocznego podglądu (256 KiB/2000 linii), Auto-show Logs oraz Copy entire log pozostają. Bufor GUI nie tworzy drugiego **trwałego** logu. Format pomiarów, `run.json`, `result.json`, `projects/`, ID pomiarowe, adaptery, Python/PsychoPy, Manual i styl pozostają niezmienione. Testy są hostowe; Windows/PsychoPy/Tobii wymagają fizycznego gate.

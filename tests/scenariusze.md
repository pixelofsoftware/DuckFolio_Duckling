# Scenariusze sprawdzenia

Próby z 2026-11-21 na macOS 27.2 (Apple Silicon), `duckc 0.3-alpha (83882805a 2026-11-20)`, wariant natywny. Komendy z katalogu projektu po `python3 build.py --target all --output build`.

| Scenariusz | Dane lub czynności | Oczekiwany wynik | Komenda lub procedura | Otrzymany wynik |
| --- | --- | --- | --- | --- |
| Zwykłe działanie: stan 5 stycznia | dane przykładowe | gotówka 746.00, ALFA 6 (150.00), BETA 5 (160.00), wartość 1056.00, wynik 56.00 | `raport 2026-01-05` | zgodny; udziały 70.64% / 14.20% / 15.15% (suma 99.99%, zaznaczona) - OK |
| Wpłata i wypłata nie są zyskiem | 6 stycznia: wpłata 200.00, wypłata 50.00 | wartość 1206.00, wynik nadal 56.00 | `raport 2026-01-06` | wartość 1206.00, wynik 56.00 - OK |
| Historia wartości | dane przykładowe | 6 dni, wyniki 0.00, -2.00, 17.00, 56.00, 56.00, 6.00 | `historia 2026-01-07` | zgodny - OK |
| Dane kontrolne | `dane/oczekiwane-wyniki.csv` | wszystkie dni zgodne | `sprawdz dane/oczekiwane-wyniki.csv` | `Zgodne dni: 6/6` - OK |
| Niepoprawne dane: sprzedaż ponad stan | sprzedaż 7 ALFA przy 6 | odrzucenie z opisem, portfel bez zmian | `dodaj 2026-01-05,2,sprzedaz,ALFA,7,25.00,,1.00` | „sprzedaz 7 jednostek ALFA, a portfel ma 6”; raport 5 stycznia bez zmian - OK |
| Niepoprawne dane: ujemna gotówka | kupno ALFA za 1000.00 przy 746.00 | odrzucenie, portfel bez zmian | `dodaj 2026-01-05,2,kupno,ALFA,40,25.00,,0.00` | „kosztuje 1000.00 z prowizja, a gotowka to 746.00 - gotowka bylaby ujemna” - OK |
| Niepoprawne dane: data | 2026-02-30 w poleceniu i w pliku | odrzucenie; błędny plik nie zmienia danych | `dodaj 2026-02-30,1,wplata,,,,10.00,0.00`; test „data 2026-02-30: caly plik odrzucony” | odrzucone z numerem wiersza - OK |
| Niepoprawne dane: brak ceny | usunięta cena BETA z 5 stycznia | polityka ścisła: raport odrzucony | `usun-cene 2026-01-05 BETA`, `raport 2026-01-05` | „brak ceny BETA z dnia 2026-01-05” - OK |
| Przypadek graniczny: wcześniejsza cena | jak wyżej, `wycena wstecz` | cena BETA z 4 stycznia (30.00), oznaczona; nigdy cena późniejsza | `wycena wstecz`, `raport 2026-01-05`; test bez ceny z 4 stycznia | wartość 1046.00, „uzyto ceny z 2026-01-04”; bez ceny wcześniejszej raport odrzucony mimo ceny z 6 stycznia - OK |
| Przypadek graniczny: wartość 0 | raport przed pierwszą operacją | wartość 0.00, udziały „n/d” | `raport 2026-01-01` | zgodny - OK |
| Przypadek graniczny: duże liczby | kupno 10 000 000 × 10 mln zł; udział przy 1e18 groszy | obliczenia bez przepełnienia | `tests/testy.dk` | odrzucenie przez brak gotówki; udział 100.00% - OK |
| Testy modelu | 55 sprawdzeń | `Bledy: 0`, kod 0 | `python3 run.py --build build --target tests` | `Bledy: 0`, kod 0 - OK |
| Odtworzenie w nowym katalogu | świeży klon repozytorium | budowa, demonstracja i testy zgodne z README | `git clone`, `python3 build.py --target all --output build`, komendy z README | macOS: OK; Linux x86_64 (Ubuntu 24.04): nie sprawdzono |

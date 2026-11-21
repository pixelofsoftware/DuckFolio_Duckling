# DuckFolio - rozliczenie portfela inwestycyjnego w Ducklingu

![Napisane w Duckling](https://img.shields.io/badge/napisane%20w-Duckling-f2c94c)

Zespół: Pixel of Software (Marcin Kowalczyk). Temat: P01 DuckFolio. Skład: 1 osoba.

Program odtwarza stan fikcyjnego portfela inwestycyjnego na wybrany dzień z historii operacji i cen zapisanych w plikach CSV. Liczy gotówkę, liczbę jednostek, wartość i udział każdego składnika oraz wynik w złotych, który nie wlicza wpłat i wypłat. Całe minimum karty P01 działa i jest sprawdzone testami. Z rozszerzeń są:

* prowizje także przy wpłatach i wypłatach;
* polityka wyceny „wstecz” z oznaczoną datą ceny;
* dodawanie operacji i cen w trakcie pracy;
* automatyczne porównanie z plikiem oczekiwanych wyników.

## Uruchomienie

Wymagane są Python 3 i Duckling (`duckc` w `PATH`, instalacja według tutoriala). Z katalogu projektu:

```bash
python3 build.py --target all --output build          # aplikacja i testy, wariant natywny
python3 run.py --build build --workdir .               # interfejs tekstowy; wpisz 'pomoc'
python3 run.py --build build --workdir . < demo/demo.txt   # cała demonstracja z pliku
python3 run.py --build build --target tests            # testy modelu: PASS/FAIL, kod = liczba błędów
```

`--workdir .` sprawia, że ścieżki w poleceniach (np. `dane/operacje.csv`) liczą się od katalogu projektu. Program czyta polecenia ze standardowego wejścia, więc działa interaktywnie i z pliku. Kod zakończenia to 0, gdy wszystkie polecenia się powiodły, albo 1, gdy któreś zostało odrzucone. Skrypty `build.py` i `run.py` to niezmienione skrypty z szablonu konkursu.

## Funkcje i demonstracja

| Funkcja z minimum tematu | Sposób uruchomienia | Oczekiwany rezultat |
| --- | --- | --- |
| Portfel z gotówką i dwoma instrumentami | `wczytaj dane/operacje.csv dane/ceny.csv` | `Wczytano 6 operacji i 9 cen.` |
| Operacje z datą: wpłaty, wypłaty, kupno, sprzedaż z prowizją | `operacje` | lista 6 operacji w kolejności (data, kolejność) |
| Wczytywanie z plików CSV | jak wyżej; błędny plik | błędy z numerami wierszy, poprzedni stan bez zmian |
| Raport na wybrany dzień | `raport 2026-01-05` | gotówka 746.00, ALFA 6 × 25.00 = 150.00, BETA 5 × 32.00 = 160.00, razem 1056.00; udziały 70.64% / 14.20% / 15.15% |
| Historia wartości i wynik bez wpłat i wypłat | `historia 2026-01-07` | 6 wierszy; 5 i 6 stycznia wynik 56.00 przy wartości 1056.00 i 1206.00 |
| Zgodność z danymi kontrolnymi | `sprawdz dane/oczekiwane-wyniki.csv` | `Zgodne dni: 6/6` |
| Sprzedaż większej liczby jednostek niż posiadana | `dodaj 2026-01-05,2,sprzedaz,ALFA,7,25.00,,1.00` | odrzucona: „sprzedaz 7 jednostek ALFA, a portfel ma 6”; portfel bez zmian |
| Operacja prowadząca do ujemnej gotówki | `dodaj 2026-01-05,2,kupno,ALFA,40,25.00,,0.00` | odrzucona: kupno kosztuje 1000.00, a gotówka to 746.00 |
| Niepoprawna data | `dodaj 2026-02-30,1,wplata,,,,10.00,0.00` | odrzucona: niepoprawna data |
| Brak potrzebnej ceny | `usun-cene 2026-01-05 BETA`, `raport 2026-01-05` | raport odrzucony: brak ceny BETA z dnia 2026-01-05 |

**Demonstracja** (`demo/demo.txt`) idzie po kolei przez całą tabelę:
1. wczytuje dane przykładowe;
2. pokazuje portfel 5 i 6 stycznia: po wpłacie 200.00 i wypłacie 50.00 wartość rośnie z 1056.00 do 1206.00, a wynik zostaje 56.00;
3. porównuje wszystkie dni z plikiem kontrolnym;
4. próbuje trzech błędnych operacji i pokazuje, że stan 5 stycznia się nie zmienił;
5. usuwa cenę BETA: polityka ścisła odrzuca raport, a polityka „wstecz” wycenia BETA ceną z 4 stycznia i oznacza ją gwiazdką.

## Środowisko i zależności

| Element | Wartość |
| --- | --- |
| Kompilator | `duckc 0.3-alpha (83882805a 2026-11-20)`, `commit-hash: 83882805a` |
| Uruchomienie | natywnie (`--mode native`) |
| System operacyjny | macOS 27.2, Apple Silicon (arm64) |
| Zależności | Python 3 (do `build.py` i `run.py`) i Duckling; brak innych bibliotek |

Program korzysta z biblioteki C tylko przez `fopen`, `fread`, `ferror` i `fclose` ze standardowej biblioteki C. Te funkcje są takie same na Linuksie i macOS, więc kod nie używa linuksowych stałych `open()`. Budowę i testy sprawdziłem na macOS. Na Linuksie x86_64 (Ubuntu 24.04) projektu nie sprawdzałem. Wariantu DVM nie sprawdzałem, bo odczyt plików idzie przez funkcje C.

## Struktura i działanie

| Plik | Odpowiedzialność |
| --- | --- |
| `app/app.dk` | punkt wejścia: czyta polecenia wiersz po wierszu i wypisuje odpowiedzi |
| `app/sesja.dk` | interfejs tekstowy: polecenia, wczytanie danych w całości, `dodaj`, ceny, porównanie z oczekiwanymi wynikami |
| `app/dane.dk` | odczyt i walidacja CSV operacji i cen, sortowanie po (data, kolejność), granice danych |
| `app/portfel.dk` | reguły portfela: sprawdzenie i wykonanie operacji (w całości albo wcale), odtworzenie stanu na dzień |
| `app/wycena.dk` | raport na dzień, udziały, polityka brakującej ceny, historia wartości |
| `app/tekst.dk` | dzielenie CSV, odczyt dat, kwot i liczb, formatowanie tabel |
| `app/pliki.dk` | odczyt pliku przez `fopen`/`fread`/`fclose` ze sprawdzaniem błędów i limitem 16 MiB |
| `tests/testy.dk` | testy modelu bez interfejsu i bez plików |

**Format danych.** Pliki CSV są w UTF-8 (BOM na początku jest pomijany), z nagłówkiem i separatorem przecinka, a wiersze mogą kończyć się LF albo CRLF. Puste wiersze są pomijane. Cudzysłowy w polach nie są obsługiwane. Nagłówki muszą brzmieć dokładnie:
* `data,kolejnosc,typ,instrument,liczba,cena,kwota,prowizja`;
* `data,instrument,cena`.

Pola:
* daty: `RRRR-MM-DD`, z prawdziwą liczbą dni miesiąca i latami przestępnymi; lata 1900-2199;
* kwoty: kropka dziesiętna i najwyżej dwie cyfry po niej, bez znaku;
* nazwa instrumentu: 1-12 znaków `A-Z`, `0-9`, `_` lub `-`, zaczyna się literą;
* puste pole prowizji oznacza 0.

**Prowizje i zaokrąglenia.** Wszystkie kwoty są liczbami całkowitymi groszy, więc w obliczeniach nie ma zaokrągleń. Prowizja jest kwotą całej operacji:

| Operacja | Gotówka | Inne zmiany |
| --- | --- | --- |
| kupno | `− liczba × cena − prowizja` | jednostki `+ liczba` |
| sprzedaż | `+ liczba × cena − prowizja` | jednostki `− liczba` |
| wpłata | `+ kwota − prowizja` | wpłaty zewnętrzne `+ kwota` |
| wypłata | `− kwota − prowizja` | wypłaty zewnętrzne `+ kwota` |

Prowizja zmniejsza więc wynik, tak jak każdy koszt. Zaokrąglamy tylko udziały w raporcie: do 0.01%, połówki w górę, licząc dzieleniem pisemnym na liczbach całkowitych bez przepełnienia. Zaokrąglone udziały mogą sumować się do 99.99% albo 100.01%; raport wtedy to zaznacza. Przy wartości portfela 0 udziały są niedostępne („n/d”).

**Kolejność operacji.** Raport na dzień D obejmuje wszystkie operacje z datą nie późniejszą niż D, czyli stan na koniec dnia.
* Operacje przetwarzamy po parze (data, kolejność) rosnąco. Kolejność wierszy w pliku nie ma znaczenia.
* Para (data, kolejność) musi być jednoznaczna.
* Cena transakcji służy tylko rozliczeniu operacji. Wycena na dzień raportu pochodzi z `ceny.csv`.

**Walidacja i niepodzielność operacji.** Każdą operację najpierw w całości sprawdzamy, a dopiero potem zmieniamy portfel. Odrzucona operacja nie zmienia niczego.

Odrzucamy:
* sprzedaż większej liczby jednostek niż posiadana;
* każdą operację, po której gotówka byłaby ujemna (także wypłatę i sprzedaż z prowizją większą od przychodu);
* niepoprawną datę, liczbę, kwotę, typ, nazwę lub liczbę pól;
* przekroczenie granic modelu.

Wczytanie plików jest niepodzielne. Gdy którykolwiek wiersz jest błędny albo któraś operacja byłaby niewykonalna, program wypisuje wszystkie błędy z numerami wierszy, a poprzednie dane zostają. Program nigdy nie pokazuje częściowo zmienionego stanu jako poprawnego raportu.

Polecenie `dodaj` wstawia operację w jej miejsce w historii i sprawdza całą historię od nowa. Wypłata 3 stycznia, po której kupno z 4 stycznia byłoby niewykonalne, też jest więc odrzucona.

**Brak ceny.** Instrument z zerową liczbą jednostek ma wartość 0 i nie wymaga ceny. Dla posiadanego instrumentu bez ceny z dnia raportu są dwie polityki:
* **ścisła** (domyślna): raport jest odrzucony z listą brakujących cen;
* **`wycena wstecz`**: program bierze najnowszą cenę sprzed dnia raportu, oznacza ją gwiazdką i podaje jej datę.

Cena z dnia późniejszego nigdy nie zastępuje brakującej ceny. W historii dzień bez potrzebnej ceny jest oznaczony „brak wyceny”, a pozostałe dni są liczone.

**Wynik kwotowy** to wartość portfela pomniejszona o sumę wpłat zewnętrznych i powiększona o sumę wypłat zewnętrznych do dnia raportu. Kupno i sprzedaż do tych sum nie wchodzą. Wynik kwotowy nie jest stopą zwrotu.

**Granice modelu**, które chronią przed przepełnieniem liczb 64-bitowych:
* liczba jednostek: najwyżej 10 000 000;
* cena: najwyżej 10 mln zł;
* kwota operacji: najwyżej 10 mld zł;
* gotówka: najwyżej 1 bln zł;
* liczba instrumentów: najwyżej 100.

**Ograniczenia:** jedna waluta i jeden portfel. Nie ma krótkich pozycji, dywidend ani splitów. Dane są tylko w pamięci: polecenia `dodaj`, `cena` i `usun-cene` nie zapisują plików.

## Sprawdzenie projektu

```bash
python3 run.py --build build --target tests          # 55 sprawdzeń modelu
python3 run.py --build build --workdir . < demo/demo.txt
```

Testy (`tests/testy.dk`) sprawdzają między innymi:
* daty z 30 lutego i 29 lutego w latach zwykłych i przestępnych;
* kwoty graniczne i błędne;
* CSV z CRLF;
* zgodność wszystkich 6 dni z `oczekiwane-wyniki.csv`;
* udziały i zaokrąglenia, także przy 1e18 groszy;
* wszystkie próby błędnego wejścia z karty;
* politykę brakującej ceny, w tym zakaz użycia ceny z dnia późniejszego;
* niepodzielność wczytania i polecenia `dodaj`;
* prowizje przy wpłatach i sprzedaży.

Scenariusze z oczekiwanymi i otrzymanymi wynikami są w [tests/scenariusze.md](tests/scenariusze.md).

## Autorstwo i materiały

Kod i dokumentacja: Pixel of Software (Marcin Kowalczyk), z pomocą asystenta AI. Szczegóły, w tym pochodzenie danych przykładowych i skryptów szablonu, są w [ZRODLA.md](ZRODLA.md). Licencja: MIT (plik `LICENSE`, szablon Fundacji Duckling z dopisanym autorem).

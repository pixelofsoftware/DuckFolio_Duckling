# Autorstwo i źródła

## Wkład autorów

| Autor | Wykonane elementy | Lokalizacja w projekcie |
| --- | --- | --- |
| Marcin Kowalczyk (Pixel of Software) | założenia, przegląd i akceptacja kodu, publikacja | całość |
| Asystent AI Claude (Anthropic) | kod modułów, testy, dokumentacja | `app/`, `tests/`, `demo/`, `README.md` |

## Wykorzystane materiały

| Materiał | Autor i źródło | Wersja lub data | Licencja | Sposób wykorzystania |
| --- | --- | --- | --- | --- |
| `build.py`, `run.py`, `LICENSE` | Fundacja Duckling, szablon projektu z materiałów na start DuckQuest | 2026 | MIT (plik `LICENSE`) | skrypty skopiowane bez zmian; licencja z dopisanym autorem |
| `dane/operacje.csv`, `dane/ceny.csv`, `dane/oczekiwane-wyniki.csv` | Fundacja Duckling, dane przykładowe karty P01 z materiałów na start | 2026 | materiały konkursowe DuckQuest | dane wejściowe demonstracji i testów (fikcyjne instrumenty ALFA i BETA) |
| Duckling (kompilator i biblioteka standardowa) | ducktype-org/duckling | 0.3-alpha, commit 83882805a | licencja Ducklinga | zależność budowania |

Algorytm zamiany daty na numer dnia (`tekst.numerDnia`, `tekst.tekstDaty`) to znany, publicznie opisany algorytm kalendarza gregoriańskiego („days from civil”, Howard Hinnant); kod w Ducklingu napisano samodzielnie.

## Narzędzia AI

Kod w `app/` i `tests/`, plik `demo/demo.txt` i dokumentację (`README.md`, `ZRODLA.md`, `tests/scenariusze.md`) przygotowano z pomocą asystenta AI Claude (Anthropic). Autor ustalił zakres, przejrzał wyniki, sprawdził działanie (budowa, testy, demonstracja) i odpowiada za oddaną wersję.

## Licencja własnego projektu

MIT, treść w pliku `LICENSE` (szablon Fundacji Duckling z dopisaną linią `Copyright (c) 2026 Pixel of Software (Marcin Kowalczyk)`). Dane przykładowe pozostają materiałami konkursu DuckQuest.

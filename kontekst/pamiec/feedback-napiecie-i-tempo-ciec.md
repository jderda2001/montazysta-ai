---
name: feedback-napiecie-i-tempo-ciec
description: "Przed puentą lub wynikiem buduj napięcie (pauza, najazd na twarz); cięcia między zdaniami nie mogą być za ciasne"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1cd9d117-33dd-4f3b-b958-6ab5bf04fe4c
  modified: 2026-11-24T22:54:59.857Z
---

18.11.2026, po pierwszej wersji rolki PerfOS (IMG_0597), Jakub: „Mega spoko, z tym że jedna uwaga: gdy mówię «no i wynik», to powinno być bardziej zbudowane napięcie, czy troszkę przedłużone, i takie na przykład przybliżenie na moją twarz, coś w tym stylu. I mam wrażenie, w niektórych miejscach troszeczkę za szybko przyciąłeś, możesz to sprawdzić. Ale bardzo fajnie to wyszło, więc jak najbardziej akceptuję. Tylko ta jedna poprawka.”

**Why:** „No i wynik.” trwało 0,7 s i od razu szły liczby, więc zapowiedź nie miała wagi. Co do cięć nie wskazał miejsc; pomiar pokazał (moja interpretacja), że marginesy 0,10 / 0,15 s ścinały naturalne pauzy 0,4–0,7 s do 0,25 s.

**How to apply:**
- Zdanie, które zapowiada puentę albo liczby („No i wynik”, „I teraz najlepsze”), dostaje chwilę: szybki dojazd na twarz na kluczowym słowie, pauza ok. 1 s z dalszym powolnym najazdem, napis stoi do końca pauzy. Gdy po słowie nie ma dość nagrania z kontaktem wzrokowym, użyj zwolnienia 50% i zatrzymanej klatki. Wzór: `projekty/IMG_0597/skrypty/aroll.py` (kwestia `"HOLD"`) i `kompozycja.py` (`s_wynik`, `pauza`).
- Marginesy cięć: po zdaniu 0,22 s, przed zdaniem 0,14 s. Sąsiednie zdania z naturalną pauzą do ok. 0,5 s zostają jedną kwestią. Ciasno tylko przy cięciu w środku zdania.
- Koniec zdania przed ciszą wyznaczaj progiem ok. −52 dB, nie −45: ciche końcówki (ch, wygasające samogłoski) leżą między nimi. Przy cięciu w środku ciągłej mowy poziom nie wystarcza (wziąłem zapowiedź następnego słowa za końcówkę „dziś”); tam rozstrzyga widmo albo sonda whisperem.
- Otwarte: nie ocenił jeszcze wersji po poprawce. Dopisać, czy pauza i tempo są w sam raz, za długie czy za krótkie.

**Aktualizacja 24.11.2026 (C4527, C4528): styki mają być ciaśniejsze.** Jakub: „czasami wkradają się krótkie przerwy pomiędzy jednym a drugim elementem. Chciałbym, żeby one były minimalnie jeszcze krótsze, żeby było flow bardziej płynne… czasami jest taka cisza i ona jest taka niewypełniona… zapisz do przyszłych”.
- Pomiar: między ostatnim słowem kwestii a pierwszym następnej było średnio 0,53 s (0,39–0,71). Główną przyczyną był start wyspy z silencedetect, który wypada nawet 0,2 s przed pierwszą głoską.
- Teraz:
  - start kwestii = faktyczny początek głosu (−45 dB) minus 0,10 s;
  - koniec = faktyczne wygaśnięcie (−52 dB) plus 0,22 s po zdaniu (.?!) albo 0,12 s w środku zdania.
  - Funkcje `poczatek_mowy()` i `koniec_mowy()` są w `projekty/C4528/skrypty/aroll.py`.
- Cel: ok. 0,3–0,35 s ciszy między zdaniami, ok. 0,2–0,25 s w środku zdania. Celowa pauza przed puentą nadal przez `{"post": …}`.

**Druga aktualizacja 24.11.2026 (C4534–C4538): jeszcze ciaśniej.**
- Jakub: „dalej są przerwy pomiędzy ścinkami… pół sekundy albo sekunda… bardzo niepłynne. Weź to jeszcze bardziej zoptymalizuj, żeby to po prostu wycinać za każdym razem”.
- Pomiar przed poprawką: 0,3–0,4 s ciszy na każdym styku, raz 0,72 s, bo buczenie „mmm” przed słowem zaliczało się do mowy.
- Teraz:
  - start głosu wykrywany od −40 dB, więc oddech i „mmm” przed słowem odpadają;
  - margines przed głosem 0,05 s;
  - po zdaniu 0,10 s, w środku zdania 0,05 s.
  - Na styku zostaje ok. 0,15 s.
- Wartości są w `projekty/C4534/skrypty/aroll.py` i w szablonie skilla. Każdą rolkę sprawdzaj pomiarem przerw w gotowym audio.

Zob. [[feedback-false-starts]], [[feedback-reel-style-approved]], [[perfos-rolki-branding]].

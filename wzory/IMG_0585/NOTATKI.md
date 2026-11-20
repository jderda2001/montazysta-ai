# IMG_0585 – reklama adGen „Leady na służebność przesyłu” (hook A / B / C)

Źródło: `~/Downloads/IMG_0585.MOV` (iPhone 4K 60 kl./s, pion, 4:20, zakres kolorów tv, mikrofon DJI przez telefon, brak osobnego audio, więc offset 0).
Eksport: `~/Desktop/Montażysta AI/Eksporty/Reklamy adGen/2026-11-17 Leady na służebność przesyłu/` (HOOK A, B, C).
Paleta: `MARKA = "adgen"` (pomarańcz `#ff7018`, biały tekst na akcencie, zielony „zrobione”), bez logo.

## Wersje

| Wersja | Hook (to, co faktycznie mówi) | Długość |
|---|---|---|
| A | „Po wyroku Trybunału Konstytucyjnego właściciele działek znowu pytają o wynagrodzenie.” | 55,1 s |
| B | „Prowadzisz sprawy o służebność przesyłu? Możemy przełączyć właściciela działki zaraz po naszej rozmowie do Twojego handlowca. Na żywo.” | 58,0 s |
| C | „Dzwonisz do leada o służebność przesyłu, a on kompletnie nie pamięta, że zostawiał gdziekolwiek kontakt? U nas każdy najpierw rozmawia z naszym zespołem.” | 58,0 s |

Korpus po hooku jest we wszystkich wersjach identyczny (12 kwestii + 2,5 s planszy końcowej).

## Struktura projektu

Każda wersja ma swój folder `A/`, `B/`, `C/` (`aroll/`, `audio/`, `hf/`, `napisy.srt`). Skrypty są wspólne (`skrypty/`), wersję wybiera zmienna `HOOK`:

```bash
HOOK=A python3 -I skrypty/aroll.py              # cięcia, kadry, grading, dźwięk (A-roll + audio/aroll.wav)
HOOK=A python3 -I skrypty/aroll.py --audio-only # sam dźwięk, bez renderu obrazu (po zmianie obróbki dźwięku)
HOOK=A uv run --no-project --with numpy python3 -I skrypty/slowa.py
HOOK=A python3 -I skrypty/waliduj_napisy.py 0.15
HOOK=A python3 -I skrypty/kompozycja.py         # hf/index.html + napisy.srt
cd A/hf && hyperframes check && hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format png
```

Wspólne dla wersji: `audio/` (dźwięk źródła), `analiza/wyspy.json` (transkrypcja całego nagrania), `analiza/poziomy.json` (wyrównanie głośności kwestii).

## Wybrane duble (czasy w źródle)

| Fragment | Czas | Kadr | Tekst |
|---|---|---|---|
| Hook A | 21,47–25,84 | C | Po wyroku Trybunału Konstytucyjnego właściciele działek znowu pytają o wynagrodzenie. |
| Hook B cz. 1 | 31,92–33,74 | M | Prowadzisz sprawy o służebność przesyłu? |
| Hook B cz. 2 | 41,00–46,22 | C | Możemy przełączyć właściciela działki zaraz po naszej rozmowie do Twojego handlowca. Na żywo. |
| Hook C cz. 1 | 55,09–59,89 | M | Dzwonisz do leada o służebność przesyłu, a on kompletnie nie pamięta, że zostawiał gdziekolwiek kontakt? |
| Hook C cz. 2 | 69,59–71,79 | C | U nas każdy najpierw rozmawia z naszym zespołem. |
| Korpus 1 | 118,26–122,74 | W | Dostarczamy kancelariom właścicieli działek ze słupami i służebnościami na gruncie, |
| Korpus 2 | 127,77–130,18 | M | którzy chcą sprawdzić, czy należy im się wynagrodzenie. |
| Korpus 3 | 134,16–137,34 | C | Nasz zespół za każdym razem najpierw dzwoni do każdego z nich, |
| Korpus 4 | 146,08–153,69 | W (plansza) | aby zapytać o wysokość napięcia, rodzaj działki, dokładny adres i numer działki, a także o księgę wieczystą. |
| Korpus 5 | 164,73–168,95 | M | Dostajesz tylko tych, którzy odebrali i potwierdzili, że chcą rozmowy z prawnikiem. |
| Korpus 6 | 175,24–177,97 | W (plansza) | Każdy od razu ląduje w Twoim CRM z notatką z rozmowy. |
| Korpus 7 | 210,14–213,01 (ogon 0,09 s) | C | W tej niszy możemy też przełączyć rozmowę na żywo do Twojego handlowca. |
| Korpus 8 | 218,46–220,64 | M | Dostajesz wtedy nagranie z całej rozmowy. |
| Korpus 9 | 224,85–227,06 | W (plansza) | Pierwsze leady masz do 24 godzin od startu. |
| Korpus 10 | 231,77–236,25 | C | Płacisz tylko i wyłącznie za zapytania, nie za jakiś budżet reklamowy czy godziny zespołu. |
| Korpus 11 | 240,61–242,97 | W | Co ważne, każde zamówienie jest objęte gwarancją. |
| CTA | 247,69–253,97 | M → C (248,84) | Zostaw kontakt poniżej. Oddzwonię i powiem Ci, ile i do kiedy możemy dostarczyć Ci jaką ilość leadów na służebności. |

Zasada wyboru: ostatni pełny dubel. Przed prawie każdym dublem jest cicha próba (czytanie półgłosem, szczyt −20…−30 dB), „wykonania” mają −5…−12 dB, więc poziom odróżnia jedno od drugiego. Falstarty (kawałki bez promptu): 20,31 „Po wyroku…”, 64,80 i 66,02 „U nas…”, 173,45 „Każdy od razu ląduje”, 230,58 urwane „Płacisz…”, 213,18 przejęzyczenie „rozmowę z całej rozmowy”. Kwestie startują za nimi.

## Różnice względem skryptu (decyzje)

- **„do 24 godzin od startu”** zamiast „w 1 do 3 dni”. Jakub potwierdził 17.11.2026: zostaje 24 h.
- **Hook A** to w nagraniu tylko pierwsze zdanie, bez „ze słupami”. Zdań „Szukają kancelarii… Pytanie, czy trafią do Twojej” nie ma w nagraniu.
- **Hook B**: ostatni dubel ma inną kolejność niż skrypt („…zaraz po naszej rozmowie do Twojego handlowca. Na żywo.”). Wersja zgodna ze skryptem (36,19–40,44) to cicha próba.
- **Korpus 1**: w ostatnim dublu „ze słupami i służebnościami na gruncie”. Dubel z „liniami” (96,47–99,81) gaśnie na końcu.
- **Korpus 3–4**: dopowiedzenie spoza skryptu („za każdym razem… aby zapytać o wysokość napięcia…”, 7,6 s) jest w montażu jako plansza z listą. Wycięcie skraca film o ok. 8 s.
- **Korpus 5, 10, 11**: „chcą rozmowy z prawnikiem”, „tylko i wyłącznie za zapytania… czy godziny zespołu”, „Co ważne,” to jego słowa z nagrania.
- **CTA**: zdanie jest niezgrabne („ile i do kiedy… jaką ilość leadów”) i mówione ciągiem, więc „jaką ilość” nie da się czysto wyciąć. Przyimek: whisper na samym fragmencie słyszy „do kiedy” (6 z 6 prób), stąd taki napis.

## Grafiki (jedna na myśl, czasy ze słów)

| Kwestia | Grafika |
|---|---|
| Hook | kinetyczny, puenta w pomarańczu: A „WYNAGRODZENIE”, B „NA ŻYWO”, C „Z NASZYM ZESPOŁEM” |
| Korpus 1–2 | karta leada u góry: „Właściciel działki”, pigułki „Słupy na gruncie”, „Służebność”, „Chce sprawdzić wynagrodzenie” |
| Korpus 3 | chip „NASZ ZESPÓŁ ✓ DZWONI DO KAŻDEGO” |
| Korpus 4 | plansza „O CO PYTAMY W ROZMOWIE”: 5 wierszy, każdy na swoim słowie |
| Korpus 5 | dwa kafelki z ptaszkami: „Odebrał telefon”, „Chce rozmowy z prawnikiem” |
| Korpus 6 | plansza „TWÓJ CRM”: lead ląduje z odbiciem i pulsem obrysu, pigułka „NOTATKA Z ROZMOWY” |
| Korpus 7–8 | karta „Rozmowa z właścicielem → Twój handlowiec”, plakietka „NA ŻYWO”, pigułka „Nagranie całej rozmowy” |
| Korpus 9 | plansza „PIERWSZE LEADY / do 24h / OD STARTU”, fala wokół liczby |
| Korpus 10 | kafelki: „Płacisz za zapytania” ✓, „Budżet reklamowy” i „Godziny zespołu” szare, przekreślone |
| Korpus 11 | chip „KAŻDE ZAMÓWIENIE ✓ GWARANCJA” |
| CTA | przycisk „ZOSTAW KONTAKT ↓” pod napisami, potem plansza końcowa: „Leady dla Twojej kancelarii”, ten sam przycisk, „Oddzwonię i powiem, ile leadów i do kiedy” |

Poglądowe (nie padają wprost): nagłówek „O co pytamy w rozmowie”, „Nowe leady / Dziś” w karcie CRM, „Leady dla Twojej kancelarii” na planszy końcowej.

## Co jest inaczej niż w szablonie (IMG_0526)

- **Zakres kolorów:** szablon `aroll.py` zakładał źródło pc. To nagranie (i IMG_0576) ma zakres tv, więc pc → tv spłaszczało kontrast (czerń 49 → 58, biel 192 → 181). `aroll.py` bierze zakres z ffprobe (`src_range()`).
- **Głos naturalny, bez AI:** do filmu idzie `audio/aroll.wav` (highpass 70 Hz, kompresja 2,5:1, −14 LUFS), zgodnie z uwagą Jakuba z 17.11.2026 po IMG_0576 („za bardzo używasz voice enhancer AI”). Pierwsze podejście szło przez Sidon, bo zasada zmieniła się w trakcie pracy.
- **Wariant C w zapasie:** `skrypty/glos_c.sh A` (surowe cięcia → Sidon → łańcuch radiowy) zostawia `audio/aroll_studio_gleboki.wav` w każdej wersji. Łańcuch `DEEP` ma tu dwa dodatkowe dzwony (2,6 kHz +3 dB, 6 kHz +2,5 dB), po których różnica do głosu C z IMG_0526 mieści się w ±1,4 dB (`skrypty/widmo.py`). Żeby go użyć: `GLOS` w `kompozycja.py`.
- **Wyrównanie głośności kwestii:** hooki są nagrane 3–7 dB głośniej niż korpus. `poziomy.py` liczy poziom mowy każdej kwestii, `aroll.py` i `glos.py` dają wzmocnienie 80% różnicy do mediany (max ±4 dB). W naturalnym głosie rozrzut między kwestiami: 2,1 dB.
- **Cisza pod planszą końcową:** w nagraniu jest tam szmer (sięgnięcie po telefon), który po kompresji i normalizacji byłby słyszalnym stuknięciem. Ostatnia kwestia jest wyciszana 0,15 s po mowie (`hold` w EDL).
- **Czasy słów:** progi w `slowa.py` były strojone na głośniejsze nagranie, więc ciche początki słów wchodziły 0,2–0,3 s za późno. Obwiednia każdej kwestii jest teraz przesuwana do poziomu odniesienia z IMG_0526.
- **Biała koszulka pod napisami:** biały tekst na białym. Wygląd napisów zostaje, a czytelność daje miękkie przyciemnienie pasa wideo pod napisami (`#scrim`, 46%, przełącznik `SCRIM` w `kompozycja.py`). Koszulka w pasie napisów ma po tym ok. 110/255 zamiast 200/255 (kontrast białego tekstu ok. 4,4:1), broda i szyja zostają bez zmian.
- **Przycisk CTA:** gradient akcent → akcent przyciemniony o 16% (`--accent-lo`, liczony w `kolory()`), bo biały tekst na jasnym końcu gradientu miał kontrast 2,5:1.

## Kontrola (17.11.2026)

| Wersja | Długość | Głośność | Szczyt | Dźwięk względem `audio/aroll.wav` | Transkrypcja kawałkami |
|---|---|---|---|---|---|
| A | 55,10 s | −14,2 LUFS | −1,8 dBFS | 0,00 ms, różnica −39,8 dB | bez powtórzeń i falstartów |
| B | 58,00 s | −14,2 LUFS | −1,8 dBFS | 0,00 ms, różnica −39,0 dB | bez powtórzeń i falstartów |
| C | 58,00 s | −14,2 LUFS | −1,8 dBFS | 0,00 ms, różnica −39,5 dB | bez powtórzeń i falstartów |

- `hyperframes check`: 0 błędów w każdej wersji. Ostrzeżenia to `line_unread` przy napisach (tempo mowy) i struktura pliku.
- `waliduj_napisy.py`: A 13 flag z 145, B 1, C 0. Wszystkie to artefakty (słowa otwierające zdanie, „do/dla kiedy” gubiące dopasowanie), sprawdzone w liniach szczegółów.
- Przesunięcie dźwięku względem obrazu w A-rollu: 0,0–0,1 ms na każdej kwestii.
- Szczyt po renderze wychodził −1,3…−1,4 dBFS (kodowanie AAC), więc po loudnorm doszedł limiter przycinający szczyty do −1,9 dBFS, a ścieżka audio w gotowych plikach została podmieniona bez renderu obrazu (`-c:v copy`).
- Miejsce na dysku: klatki A-rollu w `$TMPDIR/hyperframes-extract-cache-501/` zajmują ok. 3,3 GB na wersję. Po każdym renderze usuwałem własny wpis; dysk zapełnił się w trakcie (rendery kilku sesji naraz) i B oraz C trzeba było puścić drugi raz.

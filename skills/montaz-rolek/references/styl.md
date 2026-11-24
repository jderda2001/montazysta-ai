# Styl: wygląd i animacje (wzorzec IMG_0526)

Wszystkie wartości pochodzą z `scripts/kompozycja.py` (szablon CSS i GSAP). Zmieniaj je tylko w ramach tego samego języka wizualnego. Układ i ruch pochodzą z IMG_0526, a kolory z palety personal brandu Jakuba (17.11.2026), która zastąpiła pomarańcz widoczny w tamtym filmie.

## Spis
1. Paleta marki i krój
2. Napisy (zamrożone)
3. Hook kinetyczny
4. Słownik grafik
5. Ruch i czasy animacji
6. Wideo: kadry, najazd, grading
7. Zasady czasowania
8. Strefa bezpieczna (safe zone)

## 1. Paleta marki i krój
Marka Jakuba to czerń, biel i ciemny szary. Kolor pojawia się tylko jako akcent na tym, o czym właśnie mówi.

| Rola | Kolor | Gdzie |
|---|---|---|
| Czarny | `#0f1012` | tło plansz, tekst i ikony na akcencie (`--on-accent`) |
| Ciemny szary | `#141518`, `#222327` (gradient radialny tła od góry), karty `#16171a`–`#1d1e22`, obrysy `#2b2d32` | plansze, karty, tory pasków |
| Biały | `#ffffff` | tekst główny, napisy |
| Szarości pomocnicze | `#c9ccd3`, `#898989` | podpisy, godziny, elementy „drugiej strony” porównania |
| **Akcent główny** | **`#00E5A0`** | wyróżnione słowa, puenta hooka, kafelki, paski, przyciski, ptaszki, nagłówki plansz |

- **Jeden akcent na film.** Domyślnie `#00E5A0`. Inny tylko wtedy, gdy wymaga tego temat filmu, i wtedy mówisz o tym Jakubowi przy oddaniu.
- **Paletę ustawiasz w jednym miejscu:** `PALETY` i `MARKA` w `kompozycja.py`. Funkcja `kolory()` wylicza z akcentu `--accent-rgb` (pod `rgba(var(--accent-rgb), .45)` w poświatach i przezroczystych wypełnieniach) oraz `--accent-hi` (akcent rozjaśniony o 35% bieli, dla `#00E5A0` wychodzi `#59eec1`). Gradienty: `--accent-hi → --accent` na kafelkach, przyciskach i w wyróżnionym tekście. Nie wpisuj kolorów akcentu na sztywno.
- **Na wypełnieniu akcentem tekst i ikony są ciemne** (`var(--on-accent)`, czyli `#0f1012`). Biały na `#00E5A0` ma kontrast 1,6:1. Na ciemnym tle akcent jako tekst jest czytelny (ok. 11:1).
- **„Zrobione” też w akcencie:** kropki z ptaszkiem i pigułka potwierdzenia (`.pill.ok`). Osobnego zielonego już nie ma.
- **Nic spoza palety.** Wyjątki: odtworzony cudzy interfejs i zdjęcia, które mają wyglądać jak oryginał.

**Reklamy adGen (`MARKA = "adgen"`)** zostają pomarańczowe, decyzja Jakuba z 17.11.2026. Baza ta sama (czerń, biel, ciemny szary), różnią się trzy wartości:

| Zmienna | Personal brand | Reklamy adGen |
|---|---|---|
| `--accent` | `#00E5A0` | `#ff7018` |
| `--on-accent` (tekst i ikony na akcencie) | `#0f1012` | `#ffffff` |
| `--ok` („zrobione”) | akcent | zielony `#3ddc84` |

Wszędzie niżej „kolor akcentu” oznacza akcent wybranej palety.
- Krój: Inter Tight (`fonts/InterTight.ttf`, wagi 100–900). Odtworzony interfejs (np. profil Kai) dostaje systemowy SF.
- Minimalny rozmiar tekstu: 28 px.

## 2. Napisy (zamrożone, nie zmieniać wyglądu)
- Pozycja: `top: 1120px` (`CAP_TOP`), wyśrodkowane, jedna linia (`white-space: nowrap`).
- Krój Inter Tight 650, `letter-spacing: -0.015em`, rozmiar `min(66, CAP_W / (liczba_znaków × 0,54))` px. `CAP_W` liczy się ze strefy bezpiecznej (punkt 8) i przy 1120 px wynosi 620 px, a nie dawne 950: szersza linia wchodziła pod przyciski Instagrama. Pełne 66 px mieści fraza do 17 znaków, najwyżej 22 (52 px, `CAP_MIN`). Dłuższe `kompozycja.py` wypisuje jako za długie i trzeba je podzielić.
- Biały tekst z cieniem `drop-shadow(0 4px 14px rgba(0,0,0,.55))` i poświatą `drop-shadow(0 0 22px rgba(255,255,255,.14))`.
- Wyróżnienie `*słowo*` w `PHRASES`: gradient `--accent-hi → --accent` wycięty w tekście. Wyróżniaj 1–2 słowa niosące sens frazy (liczby, kluczowe pojęcia).
- Frazy po 2–4 słowa, do ok. 20 znaków (limit daje szerokość strefy, nie liczba słów). Dziel na przecinkach i kropkach, a długie zdania na naturalnych pauzach.
- Każde słowo wchodzi osobno: `opacity 0 → 1, y 14 → 0, blur 7 → 0`, 0,16 s `power2.out`, start 0,03 s przed słowem.
- Fraza znika przy starcie następnej (−0,06 s) albo 0,6 s po ostatnim słowie.
- Napisy startują po hooku kinetycznym i kończą się przed planszą końcową.
- Pisownia: poprawiaj błędy whispera (`FIX` w `kompozycja.py`, np. „Seter” → „Setter”).

## 3. Hook kinetyczny (pierwsze 1–2 zdania)
- Zamiast napisów: małe słowa (50 px, 600) plus duże hasło (800, `min(132, KIN_W/(znaki × 0,63))` px; zmierzone 0,63 rozmiaru na znak) od `top: 900px` (`KIN_TOP`). Cały blok (do dwóch linii małych słów, hasło i linia dopowiedzenia, razem do 331 px) kończy się przed 1245 px; bez linii dopowiedzenia hook może zacząć się niżej (IMG_0597: 960 px), a `KIN_W` to 620 px. Pełne 132 px mieści hasło do 7 znaków („1000 ZŁ”, „175 ZŁ”), dłuższe maleje, więc na hasło wybieraj liczbę albo krótkie słowo.
- Puenta (np. „DWIE STÓWKI”) w kolorze akcentu, kontrast (np. „5–6 KOŁA”) na biało.
- Małe słowa: `y 18, blur 8`, 0,18 s. Duże: `scale 1,35, blur 14 → 1`, 0,26 s `power3.out`.
- Imię bohatera jako pigułka z awatarem (obramowanie w kolorze akcentu z poświatą). Szczegóły, które psują puentę (np. „Bot zespołu”), ukryj do momentu odkrycia.

## 4. Słownik grafik
Dobieraj do sensu zdania. Każda grafika wchodzi na słowie, które ją uzasadnia.

| Element | Kiedy | Wygląd |
|---|---|---|
| Plansza (`panel`) | wyliczenie, porównanie, proces | pełny ekran, tło radialne, nagłówek w kolorze akcentu 32 px 800 z rozstrzeleniem `.14em`. W personal brandzie bez dekoracji u dołu. Trzy obracające się kwadraty (2 pełne, 1 obrys) rysują się tylko w palecie adGen: w miętowej wersji Jakub je odrzucił („nie podoba mi się to”, IMG_0576) |
| Wykres (`chart`, SVG) | „to nie rośnie liniowo”, trend, porównanie tempa | osie i siatka rysują się na wejściu, punkty wyskakują z falą, linia rysuje się razem z jadącą kropką i odhacza podziałkę osi, odrzucony wariant trzęsie się i gaśnie pod znakiem „×”, właściwa krzywa w akcencie strzela z głowicą i wypełnieniem. Wzór: `projekty/IMG_0576/skrypty/kompozycja.py` (P1) |
| Lista z kafelkami | „robi X, Y, Z” | wiersze: kafelek 96 px z ciemną ikoną (zaokrąglenie 24, gradient akcentu, poświata) + etykieta 48 px 800 wersalikami |
| Powiadomienie | „dostaję od niej…” | karta jak z telefonu nad napisami (`top: 925px`, szer. 690; dawne 96 px było nad strefą, a 290 px zasłania włosy), zaokrąglenie 34, awatar, nadawca, godzina, pozycje wchodzące po kolei |
| Chip | krótki fakt („CRM ✓ uporządkowany”) | pigułka nad napisami (`top: 985px`, do 690 px szerokości, czyli ok. 25 znaków), `rgba(15,16,18,.86)`, obrys biały 14%, 30 px 800, kafelek 56 px, ptaszek wjeżdża na słowie-kluczu |
| Kalendarz | spotkania, terminy | siatka godzin, wydarzenie wpada z `bounce.out` na „ląduje”, pigułka potwierdzenia w akcencie (`.pill.ok`) |
| Kafelki z ptaszkami | wyliczenie zalet („nie choruje…”) | 3 karty 290×206 (ptaszek wystaje 12 px za róg, więc rząd ma 910 px, nie 940), ikona, podpis, kropka w akcencie z ciemnym ptaszkiem w rogu |
| Porównanie kosztów | liczby, „X razy więcej” | paski (szary vs akcent, `scaleX`), potem wielkie „30×” 230 px 900 i „WIĘCEJ” |
| Odkrycie | puenta („to agent AI”) | odtworzony interfejs ze zrzutu od użytkownika (ostra karta, nie zrzut), plakietka wyskakuje na słowie |
| Chip zadania | zwrot do widza | jak chip, ikona tarczy |
| Pole komentarza (CTA) | „napisz komentarz…” | pole „Dodaj komentarz…” nad napisami (`top: 990px`, szer. 680; dawne 1262 px leżało pod opisem rolki), słowo-klucz wpisuje się literami co 0,08 s, migający kursor, pulsujący przycisk wysyłania |
| Plansza końcowa | ostatnie 2,5 s | dymek w kolorze akcentu z ciemnym kluczem (170 px 900), „Napisz w komentarzu” 60 px 800, podpis 40 px `#c9ccd3`. **Bez logo.** |
| Plansza końcowa promo | rolki z long-formu, ostatnie 2,5 s | koło 320 px w kolorze akcentu z ciemnym trójkątem play (pulsuje), „Cały odcinek na YouTube” 60 px 800, tytuł odcinka 40 px `#c9ccd3`. **Bez logo.** |

Nowe elementy z IMG_0591 (wzór w `projekty/IMG_0591/skrypty/kompozycja.py`, funkcja `grafiki`):

| Element | Kiedy | Wygląd |
|---|---|---|
| Hasła nad głową (`beats`) | hook, nazwiska, liczby-hasła, gdy nad głową jest pusta przestrzeń | duże słowo 900 (do 150 px) na wysokości 300 px, wejście z rozmyciem, pod spodem opcjonalny podpis 40 px; każde hasło trwa do następnego |
| Macierz 2×2 (`macierz`) | dwie osie, cztery przypadki | siatka 2×2 z opisami osi; ćwiartka zapala się na akcent, gdy o niej mówi, potem gaśnie do obrysu; najgorsza ćwiartka na biało |
| Karta z licznikiem (`stat`) | jedna liczba-dowód | karta nad głową, liczba 150 px w akcencie liczona od zera (`textContent` ze `snap`), podpis pod spodem |
| Oś czasu (`tlv`, SVG) | od roku do roku | linia rysowana z jadącą kropką między dwoma punktami, etykiety lat, licznik na końcu |
| Pierścień z połówek (`rg`, SVG) | „to połowa, druga połowa to…” | dwa łuki po 50%, biały i w akcencie, licznik procentów w środku, pigułki z nazwami pod spodem |

Ikony: obrysowe 24×24 (styl Lucide), `stroke-width 2`. Zestaw jest w `ICON` w `kompozycja.py`.

## 5. Ruch i czasy animacji
- **Od 24.11.2026 obowiązuje zasada 10 z SKILL.md: mniej, ale płynniej.** Jakub pokazał referencję i napisał: „wszystko jest mega płynne… bardziej premium, bo teraz jest bardziej AI slopowe”. Konkretnie:
  - **Limit:** najwyżej 2 złożone animacje (sceny) na każde 30 s. Każdą scenę zgłaszasz `scena("nazwa", od, do)`, a `kompozycja.py` ostrzega, gdy w oknie 30 s są więcej niż dwie. Lepiej jedna scena, która trwa 5–8 s i rozwija się przez kilka zdań, niż cztery karty po 2 s.
  - **Wejście planszy (domyślne, `"fade"`):** przenikanie `opacity 0 → 1` z lekkim odjazdem `scale 1,04 → 1` i `blur 10 → 0`, 0,6 s `power2.out`; wyjście 0,45 s `power2.inOut` (`opacity 0, scale 0,98`). Pozostałe przejścia (`iris`, `wipe`, `zoom`, `diag`, `slide`, `blur`) tylko przez `wejscie=…`, najwyżej jedno w rolce. Light leak najwyżej raz.
  - **Elementy w scenie (`pop`):** `opacity 0, y 18, blur 8 → 0`, 0,6 s `power3.out`, bez skali i bez `back.out`. Kilka elementów wchodzi kaskadą co 0,08–0,15 s albo każdy na swoim słowie.
  - **Nakładki na wideo:** wejście 0,55 s `expo.out` (`y 24, blur 10 → 0`), wyjście 0,35 s `power2.inOut`. Nakładka to też scena i wlicza się do limitu.
  - **Plakietki i dymki:** `power3.out` z `scale 0,9 → 1`. Bez sprężyn i podskoków (`back.out`, `bounce`, wstrząsy).
  - **Kamera w scenie:** w złożonej animacji cała scena siedzi w kontenerze, który powoli jedzie i przybliża (`scale 1 → 1,1–1,25` plus przesunięcie x/y, 1,5–3 s, `sine.inOut`), zatrzymując się na elemencie, o którym akurat mówi. Tak jak przewijany i przybliżany ekran telefonu w referencji.
- Kwadraty dekoracyjne (tylko paleta adGen) obracają się liniowo przez cały czas planszy (kilka stopni), dla życia w tle.
- **Zapowiedź puenty albo liczb dostaje chwilę napięcia** (Jakub po IMG_0597: przy „No i wynik” „powinno być bardziej zbudowane napięcie, troszkę przedłużone, przybliżenie na moją twarz”). Na kluczowym słowie szybki dojazd do twarzy (`#vwrap` do 1,13 w 0,34 s, `power3.out`), potem ok. 1 s pauzy bez słów z dalszym powolnym najazdem (do ok. 1,22), ciemniejącymi brzegami kadru (`.focus`) i cichym narastającym „shh”; napis stoi do końca pauzy. Gdy po słowie nie ma dość nagrania z kontaktem wzrokowym, pauzę robi zwolnienie 50% i zatrzymana klatka (`"HOLD"` w `projekty/IMG_0597/skrypty/aroll.py`). Jedno takie miejsce na rolkę, najwyżej dwa.
- **Wykresy i schematy mają żyć** (Jakub po IMG_0576: „zanimuj bardziej wykres”). Statyczny rysunek, na którym tylko dorysowuje się linia, to za mało. Każdy element wchodzi własnym ruchem na swoim słowie: osie się rysują, punkty mają falę (pierścień rosnący i gasnący w 0,6 s), linie prowadzi jadąca kropka, etykiety wyskakują ze skalą, zmiana znaczenia ma mocny gest (wstrząs, wbicie znaku, zamiana nagłówka), a całość powoli najeżdża (`scale 1 → 1,05`).

## 6. Wideo: kadry, najazd, grading
- Kadry na źródle 1080×1920 (crop w, h, x, y): **W** (1080, 1920, 0, 0) pełny; **M** (940, 1672, 38, 102) zoom 1,15; **C** (832, 1478, 92, 180) zoom 1,30. Środek dopasuj do twarzy w nowym nagraniu (w IMG_0526 twarz była ok. 508, 653). Więcej niż 1,3 nie przybliżaj, bo źródło ma tylko 1080 px szerokości.
- **Tempo cięć** (Jakub po IMG_0597: „w niektórych miejscach troszeczkę za szybko przyciąłeś”): po zdaniu zostaje 0,22 s, przed zdaniem 0,14 s, razem ok. 0,36 s oddechu. Sąsiednie zdania, między którymi w nagraniu jest naturalna pauza do ok. 0,5 s, zostają jedną kwestią ze zmianą kadru w pauzie. Ciasno (0,10–0,15 s) tylko przy cięciu w środku zdania.
- Zmiana kadru W/M/C tylko w miejscach cięć dubli, czyli między kwestiami z różnych dubli. W ciągłej wypowiedzi kadru nie przeskakuj, tylko daj płynny zoom (od 24.11.2026, zasada 10).
- **Płynny zoom (`zoom(t, skala, dl)` w `kompozycja.py`):** najazd na `#vwrap` do 1,12–1,25 przez 1,5–3 s z `sine.inOut`, na zdaniu, które coś akcentuje, potem powolny powrót albo cięcie. Jeden zoom na 2–3 zdania, nie na każde.
- W każdym ujęciu bez zoomu delikatny najazd: `scale 1 → 1,035` liniowo, `transform-origin: 50% 36%`.
- Grading: `eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward`. **Najpierw zmierz jasność źródła** (`signalstats`, YAVG klatki po kadrowaniu): ten grading przyciemnia o ok. 15 punktów. Przy ciemnym nagraniu (YAVG poniżej ok. 55) rozjaśnij: `eq=contrast=1.04:saturation=1.08:gamma=1.34:brightness=0.015`, winieta `PI/8`, cel ok. 60–70 (Jakub o IMG_0688, YAVG 33: „dałeś za ciemny obraz”), skalowanie `in_range=pc:out_range=tv`.

## 7. Zasady czasowania
- Wszystkie czasy grafik bierz ze słów (`audio/slowa.json`) i cięć (`aroll/edl.json`), nigdy na sztywno. Wtedy zmiana dubla nie psuje grafik.
- Plansze trzymaj w granicach kwestii. Między dwiema planszami pod rząd przedłuż pierwszą pod drugą (`extend=0.3, fade_out=False`), żeby nie mignął A-roll.
- Po ostatnim słowie zostaw 2,5 s (`END_HOLD`) na planszę końcową. Plansza wchodzi 0,12 s po końcu mowy.
- Ostrzeżenia `line_unread` z `hyperframes check` przy napisach wynikają z tempa mowy. Nie wydłużaj napisów kosztem synchronizacji.

## 8. Strefa bezpieczna (safe zone)

Jakub, 18.11.2026: „napisy i animacje czasem są za wysoko bądź za szeroko”, do tego dwa szablony z sieci. Strefa to część wspólna obu, zmierzona na ich pikselach (kadr 1080×1920):

- `references/strefa_szablon_instagram_reels.png`: góra 14% (269 px), dół 35% (672 px), boki 6%, wcięcie na przyciski od 1147 px w dół (prawa krawędź 850 px).
- `references/strefa_szablon_loomer.png` (Reels i Stories w reklamach Meta): góra 13%, dół 20%, prawa kolumna przycisków już od 860 px w dół (prawa krawędź 887 px).

```
y = 0     ┌──────────────────────────────┐
          │  nagłówek aplikacji          │  nic do czytania
y = 270   │  ┌────────────────────────┐  │
          │  │  x od 70 do 1010       │  │  940 px szerokości
          │  │  (głowa, plansze)      │  │
y = 860   │  │                    ┌───┘  │
          │  │  x od 70 do 885    │ ♥    │  wyśrodkowane: do 690 px
y = 1145  │  │                 ┌──┘ 💬   │
          │  │  x od 70 do 850 │   ➤     │  wyśrodkowane: do 620 px (tu stoją napisy)
y = 1245  │  └─────────────────┘         │
          │  nazwa profilu, opis, muzyka │  nic do czytania
y = 1920  └──────────────────────────────┘
```

Zasady:

- **W strefie leży wszystko, co widz ma przeczytać albo zobaczyć:** napisy, hasło hooka, liczby, karty, ikony, logo, pole CTA, treść planszy końcowej. Poza strefę może wystawać tylko wideo, tło planszy, ciemne tło karty i dekoracje.
- **Stałe są w jednym miejscu:** `SAFE`, `CAP_TOP`, `KIN_TOP` w `kompozycja.py`. Szerokość elementu wyśrodkowanego w pasie `y0–y1` daje `safe_w(y0, y1)`; pas poza strefą kończy skrypt błędem. Nie wpisuj szerokości napisów ani haseł na sztywno.
- **Plansze pełnoekranowe:** treść w kolumnie 690 px (x 195–885) od 290 do ok. 1090 px, napisy pod nią na 1120 px. Szersze elementy (do 940 px) tylko powyżej 860 px. Dolne 35% planszy zostaje puste: tam Instagram kładzie opis.
- **Nakładki na wideo (chip, karta, powiadomienie, dymek):** dwa miejsca do wyboru, zależnie od kadru. Gdy nad głową jest wolne miejsce, pas 290–480 px (szer. do 940). Gdy głowa zajmuje górę kadru (IMG_0597: włosy od 8% wysokości), nakładka staje nad napisami, w pasie 950–1130 px (szer. do 690), i wjeżdża od dołu. Sprawdź na klatce, czy nie zasłania twarzy.
- **Chip nie powtarza napisu.** Stoi tuż nad nim, więc te same słowa dwa razy wyglądają jak błąd. Chip dopowiada („JEDNA ZASADA” nad napisem „nic nie ruszamy”) albo zastępuje napis (fraza z `~` w `PHRASES` idzie tylko do SRT; wzór: `projekty/IMG_0597/skrypty/kompozycja.py`).
- **Podgląd w aplikacji i w siatce profilu** przycina kadr z góry i z dołu (4:5 pokazuje pas ok. 285–1635 px), dlatego nakładka na 96 px była ucięta.

Kontrola (obowiązkowa przed renderem, obok `hyperframes check`):

```bash
uv run --no-project --with numpy python3 -I skrypty/strefa.py              # cały film, ok. 45 s na 2 minuty rolki
uv run --no-project --with numpy python3 -I skrypty/strefa.py --obrys KAT  # obrys strefy na klatkach ze snapshotu
```

`strefa.py` generuje kompozycję w trybie kontrolnym (same grafiki na czarnym tle), robi klatkę na końcu każdego napisu i co 0,75 s, a potem szuka jasnych pikseli poza strefą. Wypisuje czas, stronę („za wysoko”, „za szeroko z prawej”, „wchodzi pod przyciski”) i prostokąt, a klatki z obrysem zapisuje w `analiza/strefa/`. Klatki w trakcie wejścia i wyjścia plansz pomija, bo treść jest wtedy w ruchu. Wynik ma być „0 z treścią poza strefą”.

Long-form 16:9 ma własne strefy (SKILL.md, sekcja o YouTube); ten punkt dotyczy pionowych rolek i reklam.

# Styl: kompozycja miniatury

Wszystkie liczby są w pikselach kadru roboczego 1920×1080 (render wychodzi w 3840×2160). Pola i nazwy stylów odpowiadają sekcji DANE w `scripts/sklad.py`. Wzorce: `projekty/IMG_0529/miniatury/sklad.py` (pierwszy zestaw) i `projekty/IMG_0529/miniatury_test/sklad.py` (drugi).

## Spis
1. Zasada nadrzędna
2. Kadr i strefy
3. Twarz i postać
4. Tekst
5. Kolory i krój
6. Tła
7. Dodatki
8. Sprawdzone układy
9. Co mówi kontrola
10. Lista przed oddaniem

## 1. Zasada nadrzędna

Miniaturę ocenia się w 168 px szerokości, w ułamku sekundy, obok dwudziestu innych. Ma w niej zostać jedna twarz, jedna myśl i jeden mocny kolor. Każdy element, którego w tym rozmiarze nie widać, tylko zabiera miejsce temu, co widać. Dlatego po każdym renderze patrz najpierw na `podglad.jpg`, dopiero potem na pełny rozmiar.

## 2. Kadr i strefy

- **Marginesy:** tekst zaczyna się 80–96 px od krawędzi. YouTube zaokrągla rogi miniatury.
- **Prawy dolny róg (ok. 270×130 px)** zasłania znacznik długości filmu. Może tam być tułów albo tło, nigdy napis ani twarz.
- **Dolna krawędź (ok. 12 px)** to pasek postępu u widzów, którzy zaczęli oglądać.
- `python3 sklad.py A --strefy` zapisuje osobny plik `A_strefy.jpg` z naniesionymi strefami. Gotowej miniatury nie rusza.

## 3. Twarz i postać

- **Wielkość:** `twarz.wys` 0,34–0,42 wysokości kadru. To wysokość prostokąta twarzy z Vision (od brwi do brody), więc cała głowa z włosami zajmuje wtedy 60–70% wysokości. Poniżej 0,26 kontrola ostrzega: twarz ginie w małym rozmiarze.
- **Położenie:** środek twarzy na `x` 0,25–0,28 (postać po lewej) albo 0,70–0,74 (po prawej), `y` 0,40–0,45. Włosy mogą lekko wychodzić poza górną krawędź, czoło nie.
- **Kierunek:** twarz patrzy w obiektyw albo w stronę napisu. Postać zwrócona plecami do tekstu wyprowadza wzrok poza kadr.
- **Lustro** (`"lustro": True`) odwraca postać, ale też napisy na ubraniu (logo na bluzie wychodzi wspak) i stronę zegarka. Używaj tylko wtedy, gdy kadr ucina logo.
- **Powiększenie:** przy `wys` 0,40 klatka 4K jest pomniejszana do ok. 0,8, więc jest zapas. Gdy `sklad.py` ostrzega o powiększeniu ponad 1,25×, weź mniejszą twarz albo klatkę z bliższego ujęcia.
- **Dół postaci:** wycięcie kończy się na dolnej krawędzi nagrania. Jeśli `sklad.py` zgłasza, że postać kończy się nad krawędzią kadru, zwiększ `wys` albo `y`. Gdy na dole widać blat lub ucięte dłonie, pomaga `"zaslona_dol": True`.
- **Światło** (`swiatlo`): na ciemnym tle domyślnie poświata w kolorze akcentu (`"akcent"`), która odcina czarną bluzę od tła. Na tle `akcent` ciemny cień w odcieniu akcentu. Na zdjęciu (`kadr`, `obraz`) domyślnie nic: gdy postać zlewa się z ciemnym zdjęciem, daj `"akcent"`, a na jasnym lub pstrokatym `"biale"` albo `"obrys": "bialy"`.
- **Mikrofon** przed klatką piersiową zostaje w wycięciu. To część jego wizerunku z nagrań, a wycięcie go zostawiłoby dziurę w bluzie.

## 4. Tekst

- **Ile:** jedna albo dwie duże linie i najwyżej jedna pigułka. Razem 2–4 słowa w dużych liniach.
- **Rozmiar:** linia bez podanego rozmiaru rozciąga się do szerokości kolumny (`szer`), aż do `max` (domyślnie 300). Krótka linia wychodzi więc większa i sama staje się bohaterem. Główna linia powinna mieć co najmniej ok. 170 px, żeby dała się przeczytać w 168 px. Liczba-bohater może mieć `max` 420–470.
- **Kolumna:** `szer` 820–940, po stronie przeciwnej do twarzy. Tekst nie wchodzi na twarz (kontrola to wykrywa).
- **Kotwica:** `y` ustawia górę bloku, `dol` jego dół. Dół przydaje się, gdy tekst stoi nad dolną krawędzią.
- **Style linii:**
  - `bialy`: zwykła linia;
  - `akcent`: gradient w kolorze akcentu, dla bohatera na ciemnym tle;
  - `klocek`: plakietka w kolorze akcentu z ciemnym tekstem, lekko obrócona, bardzo czytelna na zdjęciach;
  - `klocek-ciemny` i `klocek-bialy`: plakietki na tło `akcent`;
  - `ciemny`: ciemny tekst na tle `akcent`;
  - `maly`: dopisek mniejszą wagą, podawaj z rozmiarem, np. `("i tyle", "maly", 70)`;
  - `zielony`: alias akcentu, zostawiony dla starych układów; w nowych pisz `akcent`;
  - `skreslony`: szary, przekreślony kreską w kolorze akcentu. Wygląda dobrze w pełnym rozmiarze, ale w 168 px kreska zamazuje słowo i kontrola go nie czyta. Stosuj najwyżej do jednej krótkiej liczby, a w układzie przed → po lepiej działa zwykła biała linia i strzałka.
- **Tekst za postacią** (`"za_postacia": True`) daje głębię, ale postać zasłania litery. Sprawdza się, gdy na dolną krawędź plakietki nachodzą tylko palce (patrz „Dłoń, która coś trzyma”). Zawsze sprawdź, czy kontrola czyta wszystkie słowa.
- **Wersaliki** są ustawione w szablonie. Pisz napisy normalnie albo wersalikami, wynik jest ten sam.

## 5. Kolory i krój

- **Paleta personal brandu (17.11.2026):** czarny `#0f1012`, biały, ciemne szarości (tło marki `#34363d → #1b1c20 → #0f1012`, szary tekst `#c9ccd3`) i jeden akcent, domyślnie `#00E5A0`.
- **Akcent ustawiasz w jednym miejscu:** `AKCENT` w `sklad.py`. Funkcja `paleta()` liczy z niego jasny koniec gradientu (`--akcent2`, dla `#00E5A0` to `#59eec1`), ciemny brzeg tła `akcent` (`--akcent-ciemny`), cień i składowe pod `rgba(var(--akcent-rgb), …)`. Nie wpisuj kolorów akcentu na sztywno.
- **Na akcencie zawsze ciemny tekst i ciemne znaki.** Biały na `#00E5A0` ma kontrast 1,6:1.
- Na jednej miniaturze: akcent, biel i ciemny. Trzeci kolor rozbija miniaturę na kawałki. Osobnego zielonego na „zrobione” już nie ma, jego rolę przejął akcent.
- Inny akcent tylko wtedy, gdy wymaga tego temat filmu, i wtedy ten sam w całym zestawie A/B/C, żeby test porównywał pomysły, a nie kolory.
- Krój Inter Tight 900, ten sam co w napisach i planszach filmów. Dzięki temu miniatura i film wyglądają jak jedna marka.
- Pomarańczowe okulary Jakuba to jego wizerunek, a nie kolor marki. Nie zmieniaj ich koloru korekcją. Na tle `akcent` są jedynym ciepłym punktem kadru i to działa na korzyść twarzy.

## 6. Tła

| Typ | Wygląd | Kiedy | Uwagi |
|---|---|---|---|
| `ciemne` | gradient marki z poświatą w kolorze akcentu za postacią | liczby, wynik, „zaprojektowany” wygląd | w ciemnym motywie YouTube zlewa się z tłem strony, dlatego bohater musi być jasny albo w kolorze akcentu |
| `kadr` | ta sama klatka co postać, rozmyta i przyciemniona, wyrównana piksel w piksel | autentyczność, „u mnie w biurze” | podaj `klatka`; od strony tekstu daj `"zaslony": ["prawa"]` albo `["lewa"]`; `jasnosc` domyślnie 0,62, `rozmycie` 13 |
| `akcent` | gradient w kolorze akcentu na całym kadrze | najmocniej odcina się na liście w obu motywach | tekst `ciemny` i plakietki; czarna bluza kontrastuje sama; najwyżej jeden wariant w zestawie, bo to wyjątek od „akcent tylko jako akcent” |
| `obraz` | dowolny plik: scena z kie.ai, zrzut ekranu | metafora (puste biuro) albo dowód (panel, wykres) | `plik`; `jasnosc` 0,5–0,9, `rozmycie` 0–6; zaznacz w `uwaga`, jeśli wygenerowane |

Opcje wspólne: `zaslony` (ciemny gradient od `lewa`, `prawa`, `dol`), `winieta` (domyślnie włączona poza `akcent`), `poswiata` (domyślnie tylko w `ciemne`), `kwadraty` (motyw marki: lista `(x, y, bok, obrót, "pelny" | "obrys")`; używaj oszczędnie, najwyżej dwa, z dala od twarzy).

W jednym zestawie daj trzy różne tła. Wtedy warianty różnią się już z daleka, a test sprawdza też, który klimat lepiej łapie oko.

## 7. Dodatki

Każdy dodatek ma nieść informację. Najwyżej dwa na miniaturę.

- **`pigulka`**: drugi fakt małym drukiem („zespół 3× mniejszy”). `rozmiar` 56–64. W 168 px jest nieczytelna, więc nie może nieść głównej myśli ani zastrzeżenia, od którego zależy prawdziwość napisu. Tekst dopisz do `tekst_dodatkowy`: kontrola sprawdzi go w pełnym rozmiarze i nie policzy do limitu słów.
- **`awatary`**: ludzie albo agenci jako kółka z obwódką w kolorze akcentu (`bok` 190–210, `zachodzenie` 0,12) lub kafle (`"ksztalt": "kafle"`). Dobre jako dowód w hipotezie „mechanizm”.
- **`obraz`**: zrzut ekranu jako karta (`"karta": True`) albo obiekt z przezroczystym tłem z kie.ai. Obiekt dostaje cień automatycznie.
- **`znak`**: okrągły znaczek `"x"` (nie) albo `"ptaszek"` (tak). Stawiaj go na rogu obiektu, którego dotyczy.
- **`strzalka`**: łuk od `(x, y)` do `(x2, y2)`; `wygiecie` ze znakiem zmienia stronę łuku. Prowadzi wzrok od tekstu do dowodu. Do układu przed → po prościej wpisać „→” w linii tekstu.
- **`html`**: własny fragment, gdy film wymaga czegoś spoza listy. Dostajesz element ustawiony w `(x, y)`; w środku działają klasy szablonu (`pigulka`, `kw pelny`, `kw obrys`) i zmienne `var(--akcent)`, `var(--akcent2)`, `var(--tlo)`. Przykład, licznik w kółku:
  ```python
  {"rodzaj": "html", "x": 1500, "y": 80, "html":
   "<div style='width:220px;height:220px;border-radius:50%;background:var(--akcent);color:#0f1012;"
   "font:900 120px/220px Inter Tight;text-align:center'>24</div>"}
  ```

`"za_postacia": True` chowa dodatek za postać. `obrot` obraca go w stopniach.

### Dłoń, która coś trzyma

Najmocniejszy chwyt z obu zestawów IMG_0529. Pusta uniesiona dłoń przy krawędzi wygląda jak obcy przedmiot, ale gdy coś na niej leży albo coś „trzyma”, wiąże element z postacią dużo mocniej niż grafika wisząca w rogu.

- **Obiekt na dłoni:** połóż dodatek `obraz` tak, żeby zakrywał górną część dłoni, a palce i nadgarstek wystawały spod spodu (pierwszy zestaw, wariant C: robot).
- **Dłoń trzyma plakietkę:** daj tekst z `"za_postacia": True` i ustaw blok tak, żeby palce nachodziły na dolną krawędź plakietki (drugi zestaw, wariant C: „APKA?”).
- **Położenie dłoni:** `sklad.py` wypisuje przy każdym wariancie wzór, np. `x = (X − 741) × 0.825 + 183`. X i Y dłoni odczytaj z linijek na `postac_podglad.jpg` i podstaw. Potem popraw na oko po renderze.

## 8. Sprawdzone układy

Punkty wyjścia z IMG_0529. Nie kopiuj tych samych trzech do każdego filmu: drugi zestaw zrobiony z układów pierwszego wygląda jak pierwszy z podmienionym napisem. Gdy w dzienniku widać, że któryś typ wygrywa, rozwijaj go; gdy przegrywa dwa razy z rzędu, zastąp go innym.

**Liczba na ciemnym tle** (postać po prawej):
```python
"twarz": {"x": 0.735, "y": 0.41, "wys": 0.38},
"tlo": {"typ": "ciemne"},
"tekst": {"x": 90, "y": 130, "szer": 880, "max": 470, "linie": [("PRZYCHÓD", "bialy"), ("×2,5", "akcent")]},
"dodatki": [{"rodzaj": "pigulka", "x": 96, "y": 840, "tekst": "zespół 3× mniejszy", "rozmiar": 60}],
```

**Prawdziwy pokój i dowód** (postać po lewej):
```python
"twarz": {"x": 0.25, "y": 0.41, "wys": 0.37},
"tlo": {"typ": "kadr", "klatka": "B/klatka.png", "zaslony": ["prawa"]},
"tekst": {"x": 900, "y": 120, "szer": 940, "linie": [("4 AGENTÓW AI", "bialy"), ("ZAMIAST DZIAŁU", "klocek")]},
"dodatki": [{"rodzaj": "awatary", "x": 910, "y": 640, "pliki": [...], "bok": 210, "zachodzenie": 0.12}],
```

**Teza na tle akcentu, obiekt na dłoni** (postać po prawej):
```python
"twarz": {"x": 0.72, "y": 0.45, "wys": 0.37},
"tlo": {"typ": "akcent"},
"tekst": {"x": 90, "y": 90, "szer": 800, "linie": [("TEGO AI", "ciemny"), ("NIE ZROBI", "klocek-ciemny")]},
"dodatki": [{"rodzaj": "obraz", "x": 235, "y": 585, "plik": "elementy/robot.png", "szer": 400, "obrot": -9},
            {"rodzaj": "znak", "x": 515, "y": 570, "symbol": "x", "bok": 170}],
```

**Przed → po na scenie-metaforze** (postać po prawej, tło z kie.ai):
```python
"twarz": {"x": 0.735, "y": 0.41, "wys": 0.38},
"swiatlo": "akcent",
"tlo": {"typ": "obraz", "plik": "elementy/biuro.png", "jasnosc": 0.9, "rozmycie": 2},
"tekst": {"x": 90, "y": 130, "szer": 880, "max": 470, "linie": [("15 OSÓB", "bialy"), ("→ 5", "akcent")]},
```

**Pytanie na plakietce trzymanej w dłoni** (postać po lewej, prawdziwy pokój):
```python
"twarz": {"x": 0.27, "y": 0.42, "wys": 0.37},
"tlo": {"typ": "kadr", "klatka": "C/klatka.png", "zaslony": ["prawa"]},
"tekst": {"x": 800, "y": 65, "szer": 1030, "za_postacia": True, "linie": [("JAKA TO", "bialy"), ("APKA?", "klocek")]},
```

## 9. Co mówi kontrola

`sklad.py` po renderze uruchamia `mini.py kontrola`. Dla każdego pliku wypisuje wymiary, wagę, udział twarzy i jasność.

| Komunikat | Znaczenie | Co zrobić |
|---|---|---|
| `BŁĄD: proporcje… to nie 16:9` / `szerokość…` | plik nie spełnia wymagań YouTube; poniżej 1280 px YouTube pomniejsza cały test do 480p | renderuj przez `sklad.py`, nie zmieniaj rozmiaru kadru |
| `twarz zajmuje X%` | twarz za mała | zwiększ `twarz.wys` |
| `Vision nie widzi twarzy` | twarz zasłonięta, ucięta albo bardzo mała | popraw kadr; przy miniaturze celowo bez twarzy to nie błąd |
| `OCR nie czyta w pełnym rozmiarze: …` | słowo zasłonięte postacią, przekreślone, ucięte albo o zbyt słabym kontraście | przesuń tekst, zmniejsz `szer`, zmień styl linii |
| `przy 320 px nieczytelne dla OCR: …` | w rozmiarze listy duża linia jest za mała (pigułki to nie dotyczy) | mniej słów, krótsza linia |
| `N słów w dużych liniach` | za dużo tekstu (liczone są słowa z literą lub cyfrą, bez pigułki) | skróć do 2–4 słów |
| `tytuły: jest N, a ma być 2 propozycje` | wariant nie ma dwóch tytułów | uzupełnij pole `tytuly` w `sklad.py` |
| `tytuł „…” ma N znaków` | powyżej 60 YouTube ucina go na liście, powyżej 100 to błąd | skróć, ważne słowa na początek |
| `tytuł „…” powtarza napis z miniatury`, `obie propozycje tytułu są takie same`, `ten sam tytuł jest przy kilku miniaturach` | tytuł nic nie dokłada albo warianty nie różnią się tytułami | napisz tytuł pod innym kątem (`koncepcje.md` §4) |
| `napis… wchodzi w prawy dolny róg` | zasłoni go czas filmu | przesuń blok albo użyj `dol` z mniejszą wartością |
| `napis… zasłania twarz` | tekst na twarzy | zwęź kolumnę albo przesuń twarz |
| `średnia jasność N/255` | miniatura bardzo ciemna, zginie w ciemnym motywie | jaśniejsze tło (`jasnosc`), większy jasny element |
| `plik ma N MB` | powyżej 2 MB nie wgra się z telefonu | zwykle nie występuje; w razie czego `--jpg-szer 2560` |

OCR jest czujnikiem dymu, nie sędzią. Bywa surowszy niż oko przy tekście obróconym i częściowo zasłoniętym. Każde ostrzeżenie sprawdź na `podglad.jpg`, a jeśli zostaje, zapisz w `NOTATKI.md`, dlaczego.

## 10. Lista przed oddaniem

- W 168 px da się przeczytać główny napis i rozpoznać minę na każdym wariancie.
- Trzy warianty różnią się tłem, napisem i twarzą.
- Na żadnym nie ma resztek fotela, dziury po mikrofonie, pustej uciętej dłoni ani odwróconego logo.
- Napis nie powtarza tytułu i zgadza się z tym, co pada w filmie, bez dopisków ukrytych w pigułce.
- Prawy dolny róg jest wolny od tekstu.
- Nie ma logo adGen.
- Do każdej miniatury są dwa tytuły, różne kątem, do 60 znaków, niepowtarzające napisu.
- Kontrola nie zgłasza błędów, a każda uwaga jest przyjęta świadomie.

# Dziennik miniatur

Czytaj na start każdej pracy nad miniaturami. Po każdym filmie dopisz wpis: data, projekt, warianty (typ hipotezy, napis, klatka), co Jakub pochwalił i co odrzucił (jego słowami, jeśli były mocne), co zmieniło się w skillu. Gdy przyjdzie wynik testu z YouTube Studio, dopisz go do tabeli na dole razem z wnioskiem.

## Decyzje Jakuba (z datą i jego słowami)

- **14.11.2026:** miniatury mają powstawać z najciekawszych fragmentów filmu i z klatek, na których dobrze wychodzi.
- **14.11.2026:** „Skill montażu działa genialnie, jego kompletnie nie ruszaj. Zrób osobny skill tylko i wyłącznie do tworzenia miniatur.”
- **14.11.2026:** „Zawsze 3 miniatury do testów a/b.”
- **14.11.2026:** do każdej miniatury skill ma dopisywać dwie propozycje tytułu: „puszczam to jako ABC, testy ABC na YouTubie… każda miniatura ma swój tytuł”. Test idzie jako para tytuł + miniatura.
- **14.11.2026:** „Tak, rób miniatury automatycznie przy każdym long-formie.” Odpowiedź na pytanie, czy mają powstawać razem z odcinkiem, tak jak 3 rolki promo.
- **14.11.2026:** klucz kie.ai dał do generowania elementów graficznych. Zgody na wysyłanie tam swoich zdjęć nie dawał.
- Z wcześniejszych ustaleń przy montażu: nigdy logo adGen (marka osobista), pobranie czegokolwiek nowego wymaga pytania.

## 2026-11-14, IMG_0529 „Zautomatyzowany dział growth”, zestaw 1 (A, B, C)

Folder `projekty/IMG_0529/miniatury/`, wyeksportowany do `Eksporty/YouTube/2026-11-13 Zautomatyzowany dział growth/Miniatury/`.

| Wariant | Typ | Napis | Klatka (nagranie) | Tło i dodatki |
|---|---|---|---|---|
| A | Wynik w liczbach | PRZYCHÓD / ×2,5 + pigułka „zespół 3× mniejszy” | 17:10,4, szeroki uśmiech | ciemne tło marki, pomarańczowa poświata |
| B | Mechanizm | 4 AGENTÓW AI / ZAMIAST DZIAŁU | 7:10,9, uśmiech | rozmyty pokój z tej samej klatki, 4 awatary agentów |
| C | Teza pod prąd | TEGO AI / NIE ZROBI | 16:39,9, poważna mina, zamknięte usta | pomarańczowe tło, robot z kie.ai ze znaczkiem „×”, położony na jego uniesionej dłoni |

Tytuły dopisane tego samego dnia, po jego prośbie (dwie propozycje do każdej miniatury):

| Wariant | Tytuł 1 | Tytuł 2 |
|---|---|---|
| A | Zautomatyzowałem cały dział growth w mojej firmie | Pół roku automatyzacji działu growth: co zadziałało |
| B | Agenci AI robią u nas marketing i sprzedaż. Pokazuję jak | Artur, Kaja, Weronika i Tymon: mój zespół agentów AI |
| C | Czego AI jeszcze nie zastąpi w sprzedaży B2B | AI nie zamknie za Ciebie sprzedaży: to zostaje człowiekowi |

- **Który tytuł poszedł z którą miniaturą:** nie wiem, wybiera Jakub. Dopisz, gdy poda.
- **Decyzja Jakuba (14.11.2026):** na pytanie, które miniatury idą do testu A/B, odpowiedział „Zestaw 1”. Poszczególnych miniatur nie komentował, więc nie wiadomo, co mu się w nich podoba. Dopisz tu jego ocenę, gdy ją poda.
- **Odrzucone w trakcie (moja decyzja, nie jego):** klatka z dłonią jak szpon (16:32), klatka 10:12 z lekko otwartymi ustami (zastąpiona pewniejszą miną z 16:39,9), napis „DZIAŁ BEZ LUDZI” (nieprawda, zostały dwa etaty).

## 2026-11-14, IMG_0529, zestaw 2 (test skilla)

Zrobił go świeży agent wyłącznie na podstawie instrukcji skilla, żeby sprawdzić powtarzalność. Folder `projekty/IMG_0529/miniatury_test/`, niewyeksportowany. Jakub poprosił, żeby mu go pokazać, i dostał podgląd oraz trzy pliki.

| Wariant | Typ | Napis | Klatka (nagranie) | Tło i dodatki |
|---|---|---|---|---|
| A | Przed → po | 15 OSÓB / → 5 | 10:18,4 (dubel), szeroki uśmiech | puste biuro z kie.ai jako metafora |
| B | Koszt / stawka | DZIAŁ AI / ZA 30 $ + pigułka „tyle wystarczy na start” | 7:02,0, spokojna mina | pomarańczowe tło |
| C | Luka ciekawości | JAKA TO / APKA? | 14:08,4, poważna mina, uniesiona dłoń | rozmyty pokój, palce „trzymają” plakietkę |

- **Decyzja Jakuba (14.11.2026):** do testu wybrał zestaw 1, ten zostaje w rezerwie. Nie skomentował go.
- **Moje zastrzeżenia:** w B zastrzeżenie „na start” siedzi w pigułce, której w małym rozmiarze nie widać, a ich własny koszt jest wyższy (kilka planów po 100 $). Bezpieczniej „START ZA 30 $”. B i C mają podobne, poważne miny.

## 2026-11-17, paleta personal brandu (zmiana w skillu, bez nowego zestawu)
- **Decyzja Jakuba:** „mój brand opiera się na czarnym, białym i ciemnym szarym, akcenty zależnie od tego, o czym mówię, głównie limonkowy `#00E5A0`”. Na pytanie, czy miniatury też: „Tak, miniatury też”. Reklamy adGen zostają pomarańczowe, ale to nie dotyczy miniatur.
- **Zmiana:** pomarańcz `#ff7018` i zielony `#3ddc84` wypadły z `sklad.py` i `mini.py`. Akcent ustawia się w `AKCENT`, odcienie liczy `paleta()`. Prompty do kie.ai przepisane na miętową zieleń.
- **Sprawdzone:** zestaw 1 z IMG_0529 złożony ponownie na kopii roboczej (oryginalne pliki nietknięte), kontrola OK dla A, B i C, podgląd 360 i 168 px obejrzany w obu motywach. Robot z kie.ai ma nadal pomarańczowe oczy, bo to stary plik.
- **Uwaga do testów A/B:** zestawy z IMG_0529 są pomarańczowe. Wyniki tamtego testu mówią o hipotezach, a nie o kolorze, i nie da się ich wprost porównać kolorystycznie z nowymi miniaturami.
- **Ocena Jakuba na nowym zestawie:** czeka.

## Czego nauczył pierwszy film

Z budowy zestawu 1:
- maska pierwszego planu zabierała kawałek fotela przy szyi, widoczny dopiero na pomarańczowym tle; stąd przycinanie do sylwetki z dokładnej segmentacji osób, podgląd wycięcia na dwóch tłach i gumka na resztki;
- czarna bluza zlewała się z ciemnym tłem, dopóki postać nie dostała pomarańczowej poświaty;
- klatki z kategorii „akcent” są w większości w pół słowa i rzadko nadają się na miniaturę; najlepsze okazały się „uśmiech” i „spokój”;
- pigułka z drugim faktem jest nieczytelna w 168 px, więc nie może nieść głównej myśli ani zastrzeżenia;
- pusta dłoń przy krawędzi kadru wygląda jak obcy przedmiot, ale ta sama dłoń trzymająca robota albo plakietkę to najmocniejszy efekt w obu zestawach.

Z testu na świeżym agencie (co poprawiłem w skillu tego samego dnia):
- czasy na arkuszach były o ok. 0,16 s za wczesne i `dopracuj` trafiało obok właściwej miny; teraz czas jest poprawiony, wzorzec miny pochodzi ze skanu, a `seria.jpg` pokazuje klatki po kolei;
- kontrola dawała fałszywy alarm, gdy OCR oddawał łacińskie litery cyrylicą („APKA”), i liczyła pigułkę do limitu słów;
- `--strefy` nadpisywało gotowe miniatury; teraz zapisuje osobne pliki;
- arkusz gestów kadrował za ciasno i nie było widać dłoni;
- gumka nie radziła sobie z cienką kreską, a współrzędnych nie dało się odczytać z linijek co 200 px; doszła lupa z siatką co 20 px;
- brakowało scenariusza „drugi zestaw” (litery D, E, F, `sklad_2.py`, ranking pomijający użyte klatki);
- przykład „30 000 ZŁ MIESIĘCZNIE” w koncepcjach łamał zasadę prawdy („miesięcznie” nie pada w filmie).

Czego nie naprawiłem: krawędź włosów jest gładka jak w naklejce (maska Vision nie oddaje pojedynczych kosmyków) i po gumce przy policzku może zostać jasny rąbek. Widać to tylko w pełnym rozmiarze.

## Wyniki testów A/B

Po każdym teście dopisz wiersz. Udziały to „udział czasu oglądania” z YouTube Studio.

**W toku:** IMG_0529, zestaw 1 (A wynik w liczbach, B mechanizm, C teza pod prąd), wybrany do testu 14.11.2026. Nie wiem, czy test już ruszył. Gdy Jakub wrzuci zrzut wyniku, dopisz wiersz poniżej i usuń tę notatkę.

| Data | Film | A (typ, tytuł, udział) | B (typ, tytuł, udział) | C (typ, tytuł, udział) | Wynik YouTube | Wniosek |
|---|---|---|---|---|---|---|

Jak czytać: jeden test to mało. Wniosek o typie hipotezy („liczby wygrywają z tezami”) wpisuj do `koncepcje.md` dopiero wtedy, gdy powtórzy się w dwóch lub trzech filmach. Wynik „Performed Same” lub „Inconclusive” też jest informacją: warianty były dla widzów równie dobre, więc następnym razem różnicuj je mocniej.

## Gust Jakuba: klatki i wygląd

Tu zbieraj uwagi o tym, jak chce wyglądać (miny, które lubi, których nie znosi, kadry, retusz). Na razie pusto.

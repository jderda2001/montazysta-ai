---
name: miniatury
description: Miniatury (okładki) do filmów Jakuba na YouTube, zawsze w 3 wariantach pod test A/B. Skill skanuje surowe nagranie, znajduje klatki, na których Jakub dobrze wygląda i które pasują do najciekawszych momentów filmu, wycina postać, składa miniatury w jego stylu, sprawdza czytelność w rozmiarach z YouTube i eksportuje pliki z opisem testu. Do każdej miniatury dopisuje dwie propozycje tytułu, bo Jakub puszcza test jako pary tytuł + miniatura. Używaj zawsze po zmontowaniu long-formu na YouTube, bez pytania o zgodę (stała zasada Jakuba), oraz gdy pada „miniatura”, „miniaturka”, „okładka”, „thumbnail”, „thumb”, „tytuł filmu” albo „test A/B”, gdy Jakub prosi o inną klatkę, inny napis, nowy wariant lub poprawkę miniatury, albo gdy wrzuca wynik testu z YouTube Studio. Także wtedy, gdy mówi tylko „zrób coś do kliknięcia” lub „grafikę do filmu”. Nie służy do montażu wideo, bo od tego jest osobny skill montaz-rolek, którego ten skill nie dotyka.
---

# Miniatury do YouTube w stylu Jakuba

Miniatura decyduje, czy film w ogóle zostanie kliknięty, więc traktuj ją jak osobny produkt, a nie dodatek do montażu. Ten skill prowadzi od surowego nagrania do trzech gotowych plików pod test A/B w YouTube Studio. Wzorcowy projekt: `~/Montażysta AI/projekty/IMG_0529/miniatury/` (odcinek „Zautomatyzowany dział growth”, 14.11.2026).

Na start przeczytaj `references/dziennik.md`: jest tam to, co Jakubowi się podobało, co odrzucił i które warianty wygrały testy. To najszybsza droga do miniatury, którą zaakceptuje za pierwszym razem.

## Paleta marki: czerń, biel, ciemny szary i jeden akcent

Kanał jest pod personal brand Jakuba, więc miniatury trzymają jego paletę. Decyzja z 17.11.2026 („mój brand opiera się na czarnym, białym i ciemnym szarym, a akcenty zależą od tego, o czym mówię; głównie limonkowy `#00E5A0`”), zastępuje wcześniejszy pomarańcz `#ff7018`.

- **Baza:** czarny `#0f1012`, biały i ciemne szarości. Z nich jest tło marki, tekst, plakietki i zasłony.
- **Akcent `#00E5A0`** dostaje bohater miniatury: liczba, kluczowe słowo, plakietka, obwódka awatarów, strzałka, poświata za postacią. Jeden akcent na miniaturę i na cały zestaw.
- **Inny akcent tylko wtedy, gdy wymaga tego temat filmu.** Zmieniasz wtedy `AKCENT` w `sklad.py` i piszesz o tym Jakubowi przy oddaniu. W razie wątpliwości zostaje `#00E5A0`.
- **Na akcencie tekst i znaki są ciemne** (`#0f1012`). Biały na `#00E5A0` ma kontrast 1,6:1 i w 168 px znika.
- **Tło `akcent`** (cała miniatura w kolorze akcentu) to świadomy wyjątek od „akcent tylko jako akcent”: najmocniej odcina się na liście YouTube. Najwyżej jeden wariant w zestawie.
- **Osobnego zielonego już nie ma.** Styl i kolor `zielony` działają dalej jako alias akcentu, żeby stare układy się nie wysypały.
- **Okulary Jakuba zostają pomarańczowe.** To jego wizerunek, a nie kolor marki, więc nie zmieniaj ich korekcją i nie dobieraj do nich akcentu.
- **Grafiki z kie.ai** zamawiaj w tej palecie (opis w `references/narzedzia.md`). Starsze elementy z pomarańczowymi detalami (robot z IMG_0529) nie pasują do nowych miniatur.

Reklamy adGen zostają pomarańczowe, ale to sprawa skilla montażu. Miniatury robisz tylko pod kanał Jakuba.

## Zasady, których nie ruszasz

Każda wynika z jego decyzji albo z tego, jak działa YouTube.

1. **Zawsze trzy miniatury, przy każdym long-formie.** Jego słowa: „Zawsze 3 miniatury do testów a/b” oraz „rób miniatury automatycznie przy każdym long-formie”. Gdy odcinek na YouTube jest zmontowany, robisz miniatury w tym samym przebiegu, bez pytania, i oddajesz je razem z filmem. Sygnał, że ich brakuje: w `Eksporty/YouTube/<film>/` jest plik odcinka, a nie ma folderu `Miniatury/`. YouTube przyjmuje w teście najwyżej trzy. Każdy wariant sprawdza inną hipotezę (inny pomysł na kliknięcie), bo trzy kolory tego samego pomysłu niczego go nie nauczą. Rolki i reklamy nie dostają miniatur, dopóki o nie nie poprosi.
2. **Do każdej miniatury dwie propozycje tytułu.** Jego słowa: „puszczam to jako ABC, testy ABC na YouTubie… każda miniatura ma swój tytuł”. Test idzie jako pary tytuł + miniatura, więc każdy wariant w `sklad.py` ma pole `tytuly` z dwiema propozycjami (razem sześć na film), a Jakub wybiera po jednej. Propozycje trafiają do `test_AB.txt`, na makietę listy i do wiadomości przy oddaniu. Jak je pisać: `references/koncepcje.md` §4.
3. **Prawdziwe klatki z nagrania.** Chce miniatur z najciekawszych fragmentów filmu i takich, na których dobrze wychodzi. Twarzy nie generujesz i nie podmieniasz.
4. **Twarz nie opuszcza Maca.** Klatki ocenia i wycina Apple Vision lokalnie. Do kie.ai idzie tylko tekst promptu. Wysłanie zdjęcia Jakuba do jakiejkolwiek usługi (retusz AI, powiększanie) wymaga jego zgody za każdym razem.
5. **Tylko prawda.** Napisy, tytuły i liczby bierzesz z tego, co pada w filmie. „Przychody razy 2,5” mówi wprost, więc „×2,5” wolno. „Dział bez ludzi” brzmi mocniej, ale w dziale zostały dwa etaty, więc nie wolno. Fałszywa obietnica psuje czas oglądania, a to on rozstrzyga test.
6. **Nigdy logo adGen.** Kanał jest pod jego marką osobistą.
7. **Skill montażu zostaje nietknięty.** Jego słowa: „skill montażu działa genialnie, jego kompletnie nie ruszaj”. Z projektu montażu tylko czytasz (lista cięć, transkrypcja, materiały). Piszesz wyłącznie w `miniatury/` i w `Eksporty/…/Miniatury/`.
8. **Nic nie pobierasz bez pytania.** Wszystko, czego potrzeba, już jest na Macu (ffmpeg, swiftc, Chrome z HyperFrames). Nowy model albo biblioteka wymaga pytania z nazwą, źródłem i rozmiarem.
9. **Wyjście:** JPG 16:9, 3840×2160, poniżej 2 MB (YouTube zaleca tę rozdzielczość, a 2 MB to limit przy wgrywaniu z telefonu).

## Foldery i nazwy

- **Nagranie:** surowy plik bez napisów i grafik, zwykle `~/Downloads/IMG_xxxx.MOV`. Ścieżkę znajdziesz w `NOTATKI.md` projektu. Gotowy film się nie nadaje, bo napisy zostają na wyciętej postaci. Gdy surowego pliku nie ma, zapytaj o niego.
- **Projekt montażu (tylko do czytania):** `~/Montażysta AI/projekty/<IMG_xxxx>/`. Przydają się `aroll/edl.json` (które fragmenty weszły do filmu), `analiza/montaz_tekst.txt` (tekst filmu z czasami), `rozdzialy.txt`, `opis_youtube.txt` i `branding/` (awatary, zrzuty).
- **Praca:** `projekty/<IMG_xxxx>/miniatury/`. Powstają tu:
  - ze skanu: `skan/` (klatki, `#2550` z arkusza to `skan/002550.jpg`), `skan.jsonl`, `kandydaci.json`, `arkusz_*.jpg`;
  - na wariant: `A/ B/ C/` z `klatka.png`, `seria.jpg`, `postac.png`, `postac.json`, `postac_podglad.jpg`;
  - ze składu: `sklad.py`, `A.html`, `A.png` (bezstratny wzorzec), `A.jpg` (plik do wgrania), `A.json` (napisy i tytuły dla kontroli), `podglad.jpg`, `podglad.json`, `test_AB.txt`;
  - `elementy/` (grafiki z kie.ai) i `NOTATKI.md` (klatki zapasowe, uwagi przyjęte świadomie, co odrzuciłeś).
- **Eksport:** `~/Desktop/Montażysta AI/Eksporty/YouTube/<RRRR-MM-DD Tytuł>/Miniatury/`, pliki `<Tytuł>_MINIATURA A_MM.RR.jpg` (B, C) oraz `<Tytuł>_MINIATURY_MM.RR - test AB.txt`. Folder filmu już istnieje po montażu. Nazwy nadaje `mini.py eksport`.

## Proces

Zanim zaczniesz, przeczytaj `references/koncepcje.md` i `references/styl.md` (oba krótkie): już przy wymyślaniu hipotez trzeba wiedzieć, jakie napisy, tła i dodatki są do dyspozycji. `references/narzedzia.md` otwórz, gdy narzędzie zachowa się inaczej, niż oczekujesz, przed pierwszym użyciem gumki i przed kie.ai.

Skrypty leżą w `~/.claude/skills/miniatury/scripts/`. Komendy uruchamiaj z folderu projektu (`projekty/<IMG_xxxx>/`). `MINI` w przykładach to skrót, który w zsh najprościej zdefiniować jako funkcję:

```bash
MINI() { python3 ~/.claude/skills/miniatury/scripts/mini.py "$@"; }
```

1. **Zrozum film i wymyśl trzy hipotezy.** Przeczytaj tytuł, opis i tekst filmu. Wybierz trzy różne pomysły na kliknięcie i do każdego napis (2–4 słowa), minę, która go niesie, oraz dwie propozycje tytułu (`references/koncepcje.md` §4). Zapisz kluczowe momenty do `miniatury/momenty.json`:
   ```json
   [{"nazwa": "Wynik: przychody ×2,5", "od": 62.0, "do": 90.1}]
   ```
   Czasy są na osi gotowego filmu (z `--edl`) albo surowego nagrania (`"os": "zrodlo"`).

2. **Przeskanuj nagranie.**
   ```bash
   MINI skanuj ~/Downloads/IMG_xxxx.MOV --wyj miniatury --edl aroll/edl.json --momenty miniatury/momenty.json
   ```
   Ocenia 3 klatki na sekundę (ok. 4 min na 20 min nagrania 4K) i zapisuje arkusze `arkusz_usmiech.jpg`, `arkusz_akcent.jpg`, `arkusz_spokoj.jpg`, `arkusz_gest.jpg` (szeroki kadr, widać dłonie), `arkusz_najlepsze.jpg` oraz `arkusz_momenty.jpg`. Momenty dopiszesz później bez ponownego skanu: `MINI ranking miniatury --edl … --momenty …`.

3. **Obejrzyj arkusze i wybierz klatki.** Ranking tylko zawęża wybór, decydujesz Ty, patrząc na twarz. Na każdy wariant wybierz inną klatkę o innej minie. Arkusze poza „gestem” kadrują ciasno wokół twarzy, więc gdy liczą się dłonie, otwórz całą klatkę ze `skan/`. Czasy klatek zapasowych zapisz w `miniatury/NOTATKI.md`. Co znaczy „dobrze wygląda” i które kategorie pasują do których hipotez: sekcja „Wybór klatki” niżej.

4. **Dopracuj klatkę.** Skan patrzy co 1/3 s na pomniejszonym obrazie, więc w pełnej jakości trzeba znaleźć najostrzejszą klatkę z tą samą miną:
   ```bash
   MINI dopracuj ~/Downloads/IMG_xxxx.MOV --t 17:10.4 --wyj miniatury/A
   ```
   Czas przepisujesz z arkusza (pierwszy czas pod klatką, czyli czas w surowym nagraniu, nie ten po słowie „film”). `A/seria.jpg` pokazuje klatki po kolei, z oznaczoną klatką wskazaną i wybraną. Obejrzyj ją zawsze: mina zmienia się w ćwierć sekundy i automat czasem wybiera sąsiedni moment. Inną klatkę wymusisz przez `--klatka K`.

5. **Wytnij postać.**
   ```bash
   MINI wytnij miniatury/A/klatka.png
   ```
   Obejrzyj `A/postac_podglad.jpg` (ciemne tło i tło w kolorze akcentu obok siebie). Szukaj resztek fotela przy szyi, dziury po mikrofonie i obcych przedmiotów przy dłoniach. Naprawa (inny tryb, sąsiednia klatka, gumka `--wymaz` z lupą `--lupa`) jest opisana w `references/narzedzia.md`.

6. **Dorób elementy, jeśli pomysł ich wymaga.** Najpierw sięgnij po prawdziwe materiały z odcinka (awatary, zrzuty ekranu), bo są wiarygodniejsze. Gdy potrzeba przedmiotu albo sceny, której nie ma, wygeneruj ją w kie.ai (`scripts/kie.py`, opis w `references/narzedzia.md`). Każdy taki element wpisz w polu `uwaga` wariantu.

7. **Złóż miniatury.** Skopiuj `scripts/sklad.py` do `miniatury/`, uzupełnij sekcję DANE (w tym `tytuly` każdego wariantu) i uruchom:
   ```bash
   python3 miniatury/sklad.py            # A, B, C + kontrola + podglad.jpg + test_AB.txt
   python3 miniatury/sklad.py B          # sam wariant B przy poprawkach
   python3 miniatury/sklad.py A --strefy # A_strefy.jpg z naniesioną strefą znacznika czasu
   ```
   Przy każdym wariancie skrypt wypisuje skalę postaci i wzór, którym punkt z klatki (linijki na `postac_podglad.jpg`) przeliczysz na położenie na miniaturze. Przydaje się, gdy dodatek ma stanąć przy dłoni.

8. **Obejrzyj i popraw.** Otwórz `A.jpg`, `B.jpg`, `C.jpg` i `podglad.jpg`. Podgląd pokazuje miniatury tak, jak widzi je widz: 360 px na stronie głównej i 168 px w pasku bocznym, w ciemnym i jasnym motywie, z pierwszym tytułem pod każdą miniaturą i drugim pod spodem. Jeśli w 168 px nie da się przeczytać głównego napisu ani rozpoznać miny, miniatura nie działa, choćby w pełnym rozmiarze wyglądała świetnie. Kontrola sprawdza też tytuły: po dwa na wariant, do 60 znaków, bez powtórzenia napisu z miniatury i bez tego samego tytułu przy dwóch miniaturach. Popraw każdy `BŁĄD` z kontroli. Każdą `uwagę` usuń albo przyjmij świadomie i zapisz w `NOTATKI.md`, dlaczego zostaje. Licz się z 2–4 rundami poprawek.

9. **Wyeksportuj.**
   ```bash
   MINI eksport miniatury/A.jpg miniatury/B.jpg miniatury/C.jpg --tytul "Tytuł filmu" \
     --folder "~/Desktop/Montażysta AI/Eksporty/YouTube/RRRR-MM-DD Tytuł filmu" --opis miniatury/test_AB.txt
   ```

10. **Oddaj.** Wyślij `podglad.jpg` i trzy pliki. Napisz w kilku zdaniach: jaką hipotezę sprawdza każdy wariant, co jest poglądowe albo wygenerowane i który wariant wgrać jako pierwszy (pierwsza para zostaje domyślna, gdy test nie wyłoni zwycięzcy). Pod spodem wypisz sześć tytułów, po dwa do każdej miniatury, dokładnie jak w `test_AB.txt`. Czas klatki w `test_AB.txt` to czas w surowym nagraniu, więc nie nazywaj go minutą filmu. Poproś o ocenę.

11. **Zapisz naukę.** Dopisz do `references/dziennik.md` jego ocenę, najlepiej jego słowami. Gdy po 1–2 tygodniach wrzuci wynik testu, dopisz go do tabeli wyników razem z wnioskiem. Z tego dziennika korzysta każda następna miniatura.

12. **Posprzątaj po akceptacji.** Usuń `miniatury/skan/` (ok. 200 MB) i `skan_lista.txt`. Zostaw `kandydaci.json`, arkusze, foldery wariantów i `sklad.py`: z arkuszy da się odczytać czas dowolnej klatki i zrobić nowy wariant przez `dopracuj`. Nowy ranking albo nowe momenty po usunięciu `skan/` wymagają ponownego skanu.

## Wybór klatki

Jakub chce klatek, na których „spoko wychodzi”. Liczby z rankingu (`wygląd`, miary miny) mówią, gdzie patrzeć, ale o tym, czy klatka jest dobra, decyduje to, co widać:

- **Oczy:** otwarte, patrzą w obiektyw albo w stronę napisu. Przymknięte powieki i wzrok w bok odpadają.
- **Usta:** uśmiech albo spokojnie zamknięte. Klatka w pół słowa prawie zawsze wygląda niezręcznie, nawet gdy ma wysoki wynik w kategorii „akcent”.
- **Głowa:** prosto albo lekko pochylona do przodu. Odchylona do tyłu skraca szyję i pokazuje podbródek.
- **Dłonie:** gest pomaga tylko wtedy, gdy czyta się od razu (otwarta dłoń, wskazanie). Pusta dłoń ucięta kadrem albo pięść przy krawędzi wygląda jak obcy przedmiot. Ta sama dłoń z położonym na niej obiektem albo trzymająca plakietkę z napisem wygląda za to świetnie (`references/styl.md`, „Dłoń, która coś trzyma”), więc klatka z uniesioną dłonią bywa warta więcej, niż widać na arkuszu.
- **Ostrość:** bez smużenia na twarzy i dłoniach. Od tego jest krok 4.
- **Trzy różne miny:** warianty mają się różnić także twarzą. Trzy miniatury z tym samym uśmiechem sprawdzają tylko napis.

Kategorie a hipotezy: wynik i dobra wiadomość idą z uśmiechem, teza pod prąd i ostrzeżenie z poważną miną (`spokoj`), tłumaczenie mechanizmu z gestem albo lekkim uśmiechem, zaskoczenie z `akcent`, ale tylko gdy klatka wygląda naturalnie. Klatka z momentu, o którym mówi napis, jest premią, a nie warunkiem: lepsza świetna mina z innej minuty niż przeciętna z właściwej.

## Kolejny zestaw do tego samego filmu

Gdy Jakub chce „drugi zestaw” albo „inne pomysły”, pierwszy zostaje nietknięty:

- **Te same dane skanu.** Nie skanuj ponownie. `MINI ranking miniatury …` sam pomija okolice klatek użytych już w wariantach (czyta `A/klatka.json`, `B/klatka.json`…), więc na czele arkuszy stają nowe twarze.
- **Nowe litery.** Warianty nazwij D, E, F (foldery `D/ E/ F/`), żeby nic nie nadpisać. Eksport da im nazwy `…_MINIATURA D…`.
- **Osobny skład.** Skopiuj szablon jako `miniatury/sklad_2.py`. Podgląd i opis testu zapiszą się wtedy jako `podglad_2.jpg` i `test_AB_2.txt`, a w Eksporty jako `… - test AB 2.txt`.
- **Inne hipotezy i inny wygląd.** Co najmniej dwa typy hipotez inne niż poprzednio (`references/koncepcje.md`) i inne układy niż w pierwszym zestawie (`references/styl.md`, sekcja 8). Nowy zestaw z tymi samymi układami wygląda jak stary z podmienionym napisem.
- **Nowe tytuły.** Każdy wariant dostaje własne dwie propozycje, inne niż w pierwszym zestawie. Makieta `podglad_2.jpg` pokaże je razem z miniaturami.
- **W dzienniku** dopisz go jako osobny zestaw tego samego filmu.

## Pliki skilla

- `references/koncepcje.md`: jak z filmu zrobić trzy hipotezy, napisy i tytuły.
- `references/styl.md`: kompozycja, rozmiary, tła, dodatki, sprawdzone układy i znaczenie komunikatów kontroli.
- `references/narzedzia.md`: jak działają skrypty, wycinanie i gumka, kie.ai (koszty, prompty), zasady YouTube.
- `references/dziennik.md`: oceny Jakuba i wyniki testów. Czytaj na start, dopisuj na koniec.
- `scripts/mini.py`: skan, ranking, dopracowanie, wycinanie, render, kontrola, eksport.
- `scripts/sklad.py`: szablon składu trzech wariantów (kopiujesz do projektu, zmieniasz sekcję DANE).
- `scripts/kie.py`: generowanie teł i elementów w kie.ai.
- `scripts/wizja.swift`: Apple Vision (ocena twarzy, wycinanie, odczyt tekstu). Kompiluje się sam przy pierwszym użyciu.
- `assets/InterTight.ttf`: krój marki.

Gdy w trakcie pracy odkryjesz coś, co poprawia proces (nowa pułapka, układ, który Jakub pochwalił, rodzaj napisu, który wygrał test), dopisz to do właściwej referencji. Tak ten skill robi się lepszy z każdym filmem.

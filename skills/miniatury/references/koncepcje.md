# Koncepcje: jak z filmu zrobić trzy hipotezy

Test A/B ma sens tylko wtedy, gdy warianty różnią się pomysłem. Jeśli wygra wariant z liczbą, Jakub dowiaduje się czegoś o swojej widowni („liczby działają lepiej niż tezy”) i następna miniatura startuje z lepszego miejsca. Jeśli trzy warianty różnią się kolorem tła, wygrana nie mówi nic.

## Spis
1. Skąd brać materiał
2. Sześć typów hipotez
3. Napis
4. Tytuły: dwa do każdej miniatury
5. Prawda i granice
6. Kolejność wariantów
7. Przykład: IMG_0529

## 1. Skąd brać materiał

Przeczytaj `opis_youtube.txt`, `rozdzialy.txt` i `analiza/montaz_tekst.txt` (każda linia zaczyna się czasem w gotowym filmie). W rolkach tekst kwestii siedzi w `aroll/edl.json` w polu `text`. Gdy projektu nie ma, zrób transkrypcję (komenda w `narzedzia.md`).

Wypisz sobie z tekstu:
- **liczby i wyniki** („przychody razy 2,5”, „zespół trzykrotnie mniejszy”, „24 agentów”);
- **kontrasty** (było → jest, drogo → tanio, ludzie → AI);
- **mechanizm** (co konkretnie zbudował, z czego to się składa, kto to robi);
- **tezy wbrew oczekiwaniom** („AI nie zamknie sprzedaży za nas”);
- **koszty i stawki** („w okolicach 30 tysięcy złotych na marketing”, „plan za 30 dolarów”);
- **rzeczy ujawnione dopiero w trakcie** (nazwa aplikacji pada w 12. minucie).

Przy każdym zanotuj czas i dokładne brzmienie. Te fragmenty wpisujesz do `momenty.json`, żeby skan pokazał najlepsze klatki właśnie z nich.

## 2. Sześć typów hipotez

Wybierz trzy różne. Typ wpisujesz w polu `hipoteza` wariantu, a potem w dzienniku, żeby wyniki testów dało się porównywać między filmami.

| Typ | Co obiecuje | Napis | Mina | Kiedy |
|---|---|---|---|---|
| **Wynik w liczbach** | twardy efekt | liczba jako bohater: „PRZYCHÓD ×2,5” | uśmiech, pewność | gdy w filmie pada konkretny wynik |
| **Mechanizm** | „pokażę, jak to jest zbudowane” | co jest w środku: „4 AGENTÓW AI ZAMIAST DZIAŁU” | lekki uśmiech albo gest | gdy film coś pokazuje lub rozkłada na części; dołóż dowód (awatary, zrzut) |
| **Teza pod prąd** | zdanie wbrew temu, co widz myśli | „TEGO AI NIE ZROBI” | poważna, spokojna | gdy w filmie jest uczciwe „ale” albo krytyka |
| **Przed → po** | zmiana | dwie wartości i strzałka: „15 OSÓB → 5” | uśmiech albo gest | gdy obie wartości padają wprost |
| **Luka ciekawości** | odpowiedź jest w filmie | pytanie: „JAKA TO APKA?” | poważna albo uniesione brwi | gdy film odpowiada konkretem (tu: nazwą aplikacji) |
| **Koszt / stawka** | pieniądze, ryzyko, strata | kwota: „START ZA 30 $” | spokojna | gdy kwota pada i robi wrażenie |

Trzy warianty z jednego typu (np. trzy różne liczby) to nadal jedna hipoteza. Dobierz typy tak, żeby jeden wariant stawiał na efekt, jeden na ciekawość i jeden na coś, czego widz się nie spodziewa.

## 3. Napis

Miniaturę ogląda się przez ułamek sekundy w rozmiarze znaczka pocztowego. Dlatego:

- **2–4 słowa**, najwyżej dwie duże linie plus ewentualnie mała pigułka. Kontrola liczy słowa tylko w dużych liniach i ostrzega powyżej pięciu.
- **Do ok. 12 znaków w linii.** Linia sama dopasowuje się do szerokości kolumny, więc długa wychodzi mała. „ZAMIAST DZIAŁU” (14 znaków) to już granica.
- **Jedno słowo albo liczba jest bohaterem** i dostaje kolor akcentu albo klocek. Reszta jest biała.
- **Konkret zamiast przymiotnika.** „×2,5” zamiast „OGROMNY WZROST”, „4 AGENTÓW AI” zamiast „NOWA ERA”.
- **Polski zapis:** przecinek dziesiętny („×2,5”), znak mnożenia „×” zamiast litery x, strzałka „→”, wersaliki z polskimi znakami (krój je ma).
- **Bez kropki na końcu.** Znak zapytania tylko przy prawdziwym pytaniu.
- **Jego język.** Mówi prosto i konkretnie („apka”, „dział”). Napis ma brzmieć jak coś, co sam by powiedział, a nie jak nagłówek portalu.
- **Zastrzeżenie nie może siedzieć w pigułce.** Pigułka znika w 168 px. Jeśli zdanie jest prawdziwe tylko z dopiskiem („na start”), dopisek musi być w dużej linii: „START ZA 30 $”, a nie „DZIAŁ AI ZA 30 $” z pigułką „tyle wystarczy na start”.

Sprawdzian: zasłoń tytuł i przeczytaj sam napis. Jeśli nie wiadomo, o czym jest film ani po co go oglądać, napis jest za słaby.

## 4. Tytuły: dwa do każdej miniatury

Jakub puszcza test w YouTube jako pary tytuł + miniatura (do trzech par), więc każda miniatura ma własny tytuł. Do każdej dajesz dwie propozycje, razem sześć na film, a on wybiera po jednej. Wpisujesz je w pole `tytuly` wariantu w `sklad.py`. Trafiają do `test_AB.txt`, na makietę listy (pierwszy stoi pod miniaturą, drugi pod spodem) i do wiadomości przy oddaniu.

Miniatura i tytuł to dwie połowy jednej obietnicy. Widz widzi je razem, więc:

- **Nie powtarzaj w tytule napisu z miniatury.** Jedno niesie temat, drugie powód do kliknięcia. Gdy miniatura mówi „co” (×2,5), tytuł mówi „jak” albo „po czym”. Kontrola ostrzega, gdy duża linia napisu wpada w tytuł. Przy miniaturze „TEGO AI NIE ZROBI” tytuł „…nie zrobi…” byłby powtórką, więc użyłem „nie zastąpi” i „nie zamknie”.
- **Dwie propozycje do jednej miniatury różnią się kątem**, a nie przestawionymi słowami: np. jedna w pierwszej osobie („Zautomatyzowałem…”), druga jako pytanie albo obietnica dla widza. Inaczej Jakub wybiera między tytułem a jego kopią.
- **Tytuły przy różnych miniaturach też są różne.** Każda para sprawdza inną hipotezę (§2), a kontrola ostrzega o tym samym tytule przy dwóch miniaturach.
- **Do ok. 60 znaków** (dalej YouTube ucina tytuł na liście), twardy limit to 100. Najważniejsze słowa na początek.
- **Prawda jak w napisie** (§5): bez liczb, nazw i obietnic, których film nie spełnia. Tytuł nie może być mocniejszy niż to, co pada w nagraniu.
- **Jego głos:** pierwsza osoba i konkret, z odrobiną prowokacji, a nie elegancji (skill `jakub-clone`, rejestr C: krótkie, mocne zdania, czasem zwrot do widza w drugiej osobie). Słowa z filmu i nazwy własne (Kaja, B2B, growth) są lepsze niż ogólniki.
- **Tytuł, który film już ma** (od Jakuba albo z `opis_youtube.txt`), może być jedną z dwóch propozycji. Wpisz go też do `TYTUL_YT` jako zapas dla makiety.

Przykład, zestaw 1 z IMG_0529:

| Miniatura | Napis | Tytuł 1 | Tytuł 2 |
|---|---|---|---|
| A, wynik w liczbach | PRZYCHÓD ×2,5 | Zautomatyzowałem cały dział growth w mojej firmie | Pół roku automatyzacji działu growth: co zadziałało |
| B, mechanizm | 4 AGENTÓW AI ZAMIAST DZIAŁU | Agenci AI robią u nas marketing i sprzedaż. Pokazuję jak | Artur, Kaja, Weronika i Tymon: mój zespół agentów AI |
| C, teza pod prąd | TEGO AI NIE ZROBI | Czego AI jeszcze nie zastąpi w sprzedaży B2B | AI nie zamknie za Ciebie sprzedaży: to zostaje człowiekowi |

Tytuł 1 w A to jego własne słowa z filmu („Zautomatyzowałem cały dział growth”), a tytuł 1 w B to jego własny opis odcinka („agentów AI, którzy robią u nas marketing i sprzedaż”). Kto z kim idzie w teście, wybiera Jakub.

Co z tego wynika dla testu: przy parach wynik mówi, która para wygrała, a nie czy zadziałała miniatura, czy tytuł. Jeśli kiedyś zechce to rozdzielić, kolejnym krokiem jest osobny test samych tytułów przy już wybranej miniaturze. Nie wracaj do tego przy każdym zestawie: pary to jego metoda.

## 5. Prawda i granice

- Liczba na miniaturze musi paść w filmie w tej samej postaci. Gdy mówi „paręnaście etatów”, nie robisz z tego „14”. Gdy mówi „14–15 osób”, wolno „15 OSÓB”.
- Nie dopowiadasz jednostek ani okresów. Mówi „wydawaliśmy w okolicach 30 tysięcy złotych na marketing”, więc „30 000 ZŁ NA MARKETING” wolno, a „30 000 ZŁ MIESIĘCZNIE” już nie, bo „miesięcznie” nie pada.
- Zdanie nie może obiecywać więcej niż film. „AI ZAMYKA SPRZEDAŻ” byłoby kłamstwem, skoro w filmie mówi, że agent sprzedaży nie zamknie.
- Pytanie jest uczciwe tylko wtedy, gdy film na nie odpowiada konkretem. „JAKA TO APKA?” tak (nazwa pada). „ILE TO KOSZTUJE?” słabo, jeśli odpowiedzią jest kilka luźnych kwot.
- Elementy poglądowe (wygenerowany robot, puste biuro jako metafora) są w porządku, ale wpisujesz je w polu `uwaga` i mówisz o nich przy oddaniu.
- Nazwiska i dane klientów nie trafiają na miniaturę. Zrzuty ekranu z danymi klienta rozmyj albo pomiń.
- Tytuły podlegają tym samym zasadom co napis. „Zautomatyzowałem cały dział growth” to jego słowa z filmu, a „agenci AI prowadzą dział bez ludzi” już nie, bo w dziale zostali ludzie.
- Bez logo adGen.

Powód jest praktyczny: test rozstrzyga czas oglądania. Miniatura, która obiecuje coś, czego w filmie nie ma, zbiera kliknięcia i szybkie wyjścia, a więc przegrywa.

## 6. Kolejność wariantów

A to wariant, na który stawiasz. Gdy test nie wyłoni zwycięzcy, YouTube zostawia pierwszy wgrany plik.

- **Są wyniki w `dziennik.md`:** typ, który już wygrywał u Jakuba, idzie na A, a nowy pomysł na C.
- **Nie ma jeszcze wyników:** na A idzie obietnica, którą film spełnia najwcześniej i najpełniej (widz, który dostał to, po co kliknął, ogląda dalej, a test rozstrzyga czas oglądania). Pytania i luki ciekawości idą na koniec, bo zawód po kliknięciu kosztuje je najwięcej.

## 7. Przykład: IMG_0529 „Zautomatyzowany dział growth”

Z jednego filmu wyszły dwa zestawy, razem sześć różnych hipotez. Klatki, tła i oceny są w `dziennik.md`.

| Typ | Napis | Podstawa w filmie |
|---|---|---|
| Wynik w liczbach | PRZYCHÓD / ×2,5 + pigułka „zespół 3× mniejszy” | „przychody razy 2,5”, „zespół trzykrotnie mniejszy” (1:16–1:28) |
| Mechanizm | 4 AGENTÓW AI / ZAMIAST DZIAŁU | czterech agentów: Artur, Kaja, Weronika, Tymon (3:23) |
| Teza pod prąd | TEGO AI / NIE ZROBI | rozdział „czego AI nie zrobi” (8:47) |
| Przed → po | 15 OSÓB / → 5 | „zespół liczył 14–15 osób”, „pięć w sumie” (0:57–1:10) |
| Koszt / stawka | DZIAŁ AI / ZA 30 $ + pigułka „tyle wystarczy na start” | „plan za 30 dolarów wystarczy na start” (13:11) |
| Luka ciekawości | JAKA TO / APKA? | nazwa aplikacji pada w 11:38 |

Co z tego wynika:
- „DZIAŁ AI ZA 30 $” jest na granicy: to cena startu dla widza, a nie koszt ich działu. Tak powstała zasada o zastrzeżeniu w dużej linii.
- Odrzucony napis „DZIAŁ BEZ LUDZI”: nieprawda, w dziale zostały dwa etaty.

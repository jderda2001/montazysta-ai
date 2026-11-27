# Dziennik ocen Jakuba

Czytaj na start każdego montażu. Po każdym filmie dopisz wpis: data, projekt, co pochwalił, co skrytykował (jego słowami, jeśli były mocne), co zmieniło się w skillu. Gdy dostaniesz statystyki z Instagrama, dopisz je w sekcji na dole razem z wnioskiem.

## 2026-11-07, IMG_0361 (pierwsza reklama adGen)
- **Krytyka:** syntetyczne whooshe z szumu („chujowe”, niepasujące). Napisy rozjeżdżały się z mową o 0,3–1,0 s (whisper na całym zmontowanym pliku).
- **Zmiana:** zero syntetycznych SFX. Czasy słów liczone osobno dla każdej kwestii.

## 2026-11-13, IMG_0526 „Kaja zamiast settera” (rolka organiczna, personal brand)
- **Pochwała:** „Świetny ten montaż, zapisz te preferencje i trzymajmy się tego stylu.” Później: „animacje, które zastosowałeś dzisiaj, są świetne i bardzo poprawne. Napisy zostawiłbym, nigdy bym ich nie zmieniał.”
- **Krytyka 1:** zostawione falstarty („I każdego ranka dosta…”, „CRM jest wz…”). Sam to wyłapał, a trzeci był w CTA. Zmiana: obowiązkowy `kawalki.py`.
- **Krytyka 2:** logo adGen na planszy końcowej. „Nigdy nie dodawaj logo adGen, bo to jest pod mój personal brand.”
- **Odkrycie przy okazji:** DTW whispera było wyłączone (brak `-nfa`), napisy wyskakiwały do 0,6 s za wcześnie. Naprawione w `slowa.py`.
- **Głos:** wersja „miękka” (sam EQ i de-esser) „dalej mi nie siedzi”, chce „studyjny, głęboki”. Po A/B/C wybrał **C**: Sidon + łańcuch radiowy. To teraz domyślne brzmienie.
- **Opis pod rolkę:** pierwsza wersja (długa, prawie transkrypcja) „chujowe xddd, krótka jako podsumowanie a nie 1:1”. Zmiana: 2–4 linijki, liczba lub kontrast na początku, CTA z kluczem.

## 2026-11-13, IMG_0529 „Zautomatyzowany dział growth” (pierwszy long-form YouTube)
- **Uwaga w trakcie:** „FILM MA BYĆ POZIOMO NA YOUTUBE”, więc long-form ma 16:9 (zrobione w 4K).
- **Materiał:** dwa pliki z Dyktafonu, bo nagranie się urwało. Koniec pierwszego był zapętlony, więc wątek „to ja byłem odpowiedzialny…” wypadł zamiast wklejki z telefonu.
- **Ocena:** „zajebiste!!!!”. Dopiero potem poprawki:
  - brak muzyki: chce cichego lo-fi na darmowej licencji;
  - logo aplikacji przy jej nazwie (dał zdjęcie);
  - „Subskrybuj” ma mieć białą czcionkę (pomarańczowy tekst na pomarańczowym przycisku był niewidoczny; sprawdzaj kontrast tekstu na akcentowym tle).
- **Nowa stała zasada:** przy każdym long-formie od razu 3 pionowe rolki promo po 10–15 s. Pierwsze: „Z kilkunastu etatów do dwóch”, „Czego AI nie zrobi”, „24 agentów, start za 30 $” (`scripts/rolki_promo.py`). Ocena rolek: czeka.
- **Muzyka:** po zgodzie pobrane 6 utworów lo-fi z Biblioteki audio YouTube (folder Muzyka), po jednym na część odcinka, 20 dB pod głosem z duckingiem. Poziom po podglądzie 60 s: „Pasuje” (20 dB pod głosem z duckingiem to dobry punkt startowy na kolejne odcinki).

## 2026-11-17, paleta personal brandu (zmiana w skillu, bez filmu)
- **Decyzja Jakuba:** marka opiera się na czerni, bieli i ciemnym szarym, a akcenty zależą od tego, o czym mówi. Główny akcent to „limonkowy” `#00E5A0`.
- **Zmiana:** w personal brandzie pomarańcz `#ff7018` i zielony „zrobione” `#3ddc84` wypadły. Paletę wybiera `MARKA` w `scripts/kompozycja.py` (`PALETY`), reszta liczy się w `kolory()`. Tekst i ikony na `#00E5A0` są ciemne.
- **Doprecyzowanie tego samego dnia:** „adGen zostaje pomarańczowy”. Reklamy adGen idą w `MARKA = "adgen"` (pomarańcz, biały tekst na akcencie, zielony „zrobione”).
- **Uwaga do wpisu z IMG_0529:** „biała czcionka na przycisku” dotyczyła pomarańczowego tła i w palecie adGen dalej obowiązuje. Na `#00E5A0` biały jest nieczytelny, więc tam zawsze `#0f1012`.
- **Sprawdzone:** IMG_0526 przegenerowany w obu paletach na kopii roboczej, `hyperframes check` 0 błędów, klatki obejrzane. Ocena Jakuba na prawdziwym filmie: czeka.
- **Long-form:** na jego „Tak, przenieś” paleta trafiła też do szablonów w `projekty/IMG_0529/skrypty/` (`paleta.py` plus `kompozycja.py`, `napisy.py`, `rolki.py`, `rolka_szablon.py`). Sprawdzone na kopii: 44 grafiki i napisy wygenerowane, 12 warstw obejrzanych. Sam odcinek i jego warstwy w `hf/` zostały pomarańczowe.
- **Otwarte:** czy ma własną listę akcentów pod konkretne tematy.

## 2026-11-17, IMG_0576 „10K vs 100K” (rolka organiczna, pierwsza w palecie `#00E5A0`, dwa hooki)
- **Uwagi po pierwszej wersji (hook A):**
  - zrzut miętowych kwadratów z dołu planszy: „nie podoba mi się to”. Zmiana: w personal brandzie plansze bez kwadratów (zostają tylko w palecie adGen);
  - „zanimuj bardziej wykres na początku”. Zmiana: wykres przebudowany tak, że każdy element wchodzi ruchem (osie, siatka, fale, jadąca kropka, wstrząs, zamiana nagłówka, krzywa z głowicą i wypełnieniem);
  - „za bardzo używasz voice enchancer ai (już kupiłem dobre mikrofony także bez tego, albo z dużo mniejszym filtrem też będzie super działać)”. Zmiana: domyślnie głos naturalny z mikrofonu po lekkim masteringu, Sidon tylko na prośbę.
- **Czego nie skomentował:** hook z dużym „100K vs 10K”, kafelki, paski, chipy, plansza końcowa bez CTA, długość 93 s. Brak uwagi to nie pochwała.
- **Moje błędy w tym montażu:** skróciłem koniec hooka B na podstawie halucynacji whispera i uciąłem słowo; skrypt przebiegu poszedł do renderu mimo błędu kompozycji (potok z `head` zgubił kod wyjścia); linie wykresu wskakiwały zamiast się rysować (skala 0–1). Wszystkie trzy opisane w `narzedzia.md`.
- **Ocena wersji po poprawkach (bez kwadratów, animowany wykres, głos naturalny):** „super podoba mi się”. Ta wersja jest punktem wyjścia dla kolejnych rolek w palecie `#00E5A0`: `projekty/IMG_0576/skrypty/kompozycja.py`.

## 2026-11-17, IMG_0585 „Leady na służebność przesyłu” (reklama adGen, hook A / B / C)
- **Ocena Jakuba:** czeka. Do uzupełnienia po jego odsłuchu.
- **Decyzja w trakcie:** w nagraniu padło „do 24 godzin od startu”, w skrypcie było „1 do 3 dni”. Zapytany, odpowiedział „Zostaje 24 h”. Liczby różne od skryptu potwierdzaj przed renderem.
- **Głos:** naturalny (`audio/aroll.wav`), zgodnie z uwagą po IMG_0576. Pierwsze rendery szły jeszcze z Sidonem, bo zasada zmieniła się w trakcie pracy (inna sesja). Przy długim montażu przeczytaj dziennik jeszcze raz przed renderem.
- **Jak nagrywa reklamy:** przed prawie każdym dublem czyta kwestię półgłosem (szczyt −20…−30 dB), a „wykonanie” ma −5…−12 dB. Poziom odróżnia próbę od dubla szybciej niż tekst. Dużo dopowiedzeń spoza skryptu, więc montuję to, co powiedział, a różnice wypisuję przy oddaniu.
- **Pułapki z nagrań iPhone 4K + mikrofon DJI (poza zakresem kolorów szablony w `scripts/` ich nie obsługują; poprawione kopie są w `projekty/IMG_0585/skrypty/`):**
  - źródło ma zakres kolorów tv, a `aroll.py` zakładał pc (`in_range=pc`), co spłaszczało kontrast (czerń 49 → 58, biel 192 → 181). Na „Tak, popraw szablon” Jakuba szablon `scripts/aroll.py` bierze już zakres z ffprobe (sprawdzone: źródło pc daje identyczny obraz jak przed zmianą, źródło tv zachowuje poziomy). IMG_0576 poszedł jeszcze ze starą linią;
  - nagranie jest ok. 5 dB cichsze niż IMG_0526, więc progi w `slowa.py` (−38 / −45 dB) spóźniały napisy o 0,2–0,3 s na cichych początkach słów. Obwiednię kwestii trzeba przesunąć do poziomu odniesienia;
  - hooki nagrane 3–7 dB głośniej niż korpus: wyrównanie per kwestia (`poziomy.py`), po nim rozrzut 2 dB;
  - szmer po ostatnim słowie (sięgnięcie po telefon) po normalizacji słychać pod planszą końcową. Ogon po mowie wyciszać (`hold` w EDL, `aroll.py --audio-only` przebudowuje sam dźwięk bez renderu obrazu).
- **Mój błąd:** zatrzymałem swój render przez `pkill -f "hyperframes render"` i przerwałem też rendery dwóch innych sesji (IMG_0576 hook B, IMG_0583 C). Na tym Macu pracuje kilka sesji naraz, a rendery HyperFrames stoją we wspólnej kolejce (blokada `~/.cache/hyperframes/locks/render.lock`). Zatrzymuj tylko własny proces po PID.
- **Dysk:** klatki A-rollu w `$TMPDIR/hyperframes-extract-cache-501/` to ok. 3,3 GB na 55 s rolki. Przy renderach kilku sesji naraz urosły do 37 GB, dysk się zapełnił i dwie wersje padły z „Low disk space”. Przed renderem `df -h`, po renderze usuń własny wpis.
- **Biała koszulka:** napisy wypadają na białym materiale. Wygląd napisów został, doszło miękkie przyciemnienie pasa wideo pod nimi (46%). Do oceny przez Jakuba.
- **Trzy hooki w jednym projekcie:** foldery `A/`, `B/`, `C/` i zmienna `HOOK` zamiast kopii całego projektu na hook.
- **Plansza końcowa reklamy:** bez logo, tekst plus przycisk „ZOSTAW KONTAKT”. Nie wiem, czy w reklamach adGen chce logo; zakaz padł przy rolce pod personal brand.

## 2026-11-17, IMG_0583 „Leady z OC” (reklama adGen, hook A / B / C)
- **Ocena Jakuba:** czeka.
- **Liczba inna niż w skrypcie:** powiedział „do 48 godzin od startu”, w skrypcie było „1 do 3 dni”. Zgłoszone przed renderem, odpowiedział „Tak, dokończ”, więc zostało 48 h.
- **Mój błąd, głos:** pierwsze trzy rendery poszły z Sidonem, bo zasada o naturalnym głosie weszła do skilla w trakcie mojej pracy (inna sesja). Zauważyłem to dopiero przy dopisywaniu dziennika i renderowałem wszystko drugi raz z `audio/aroll.wav`. `SKILL.md` i dziennik czytaj ponownie tuż przed pierwszym renderem, nie tylko na starcie.
- **Falstarty:** cztery w wybranych dublach, wszystkie wygładzone przez whispera. Przy „Poszkodowany właśnie teraz…” były trzy podejścia pod rząd. Rozstrzygają krótkie sondy whisperem (0,4–1 s) od kolejnych pauz, bez promptu.
- **Kadry:** siedział nisko i daleko (twarz na 44% wysokości, 19% wysokości kadru). Zamiast W = pełny kadr poszły zoomy 1,30 / 1,50 / 1,72 z twarzą na 33–34% wysokości i środkiem twarzy podanym osobno dla każdej kwestii. Do jego oceny, czy nie za ciasno.
- **Biała koszulka:** przyciemnienie pod napisami jak w IMG_0585, ale owalne (radialne, 44%), bo prosty pas było widać na ścianie przy ramionach.
- **Nowe grafiki w palecie adGen** (`projekty/IMG_0583/skrypty/kompozycja.py`): karta leada z ptaszkami, karta połączenia, karta liczby „do 48 h” nad głową, lista „za co płacisz” z przekreśleniami, pigułki wyboru „do Ciebie / do konkurencji”, plansza końcowa z ikoną telefonu i przyciskiem. Ocena: czeka.
- **Teksty pod reklamę:** oddałem 2 propozycje i zapytałem, czy zasada „2 opisy” ma dotyczyć też reklam. Odpowiedział: „Tak, zawsze”. Treści propozycji nie ocenił.

## 2026-11-17, uwaga po akceptacji IMG_0576: różnorodność i dźwięk
- **Jego słowa:** „bardzo generyczne są przejścia względem tych animacji… bardzo często są używane te same rzeczy”. Chce 20–30 szablonów „à la b-roll” do wyboru oraz subtelnych dźwięków: delikatny przy wyskakującym napisie i „shhh” przy animowanym wykresie. „A tak to już super.”
- **Zmiana:** biblioteka ok. 50 szablonów z katalogu HyperFrames w `biblioteka/` z opisem w `references/biblioteka.md`, `mount()` w szablonie kompozycji, sześć przejść plansz z rotacją w `panel()`, reguły różnorodności w SKILL.md.
- **Sprawdzone:** 43 szablony zmontowane w 9:16 w palecie marki (arkusze), przejścia przetestowane klatka po klatce na kopii IMG_0576, `hyperframes check` 0 błędów. Żaden film nie był jeszcze zmontowany z biblioteką.
- **Dźwięki:** na pytanie o pobranie odpowiedział „Tak, pobierz”. W `Muzyka/SFX/` są paczki Kenney (CC0) i 19 plików z Mixkit, razem ok. 12 MB. Powstał `scripts/sfx.py` i próbka A/B na pierwszych 28 s IMG_0576 (`projekty/IMG_0576/ab/sfx/`): bez dźwięków, z dźwiękami, same efekty podgłośnione. Dobór po pomiarach, bez odsłuchu. **Ocena próbki: „Jest dobrze”** (17.11.2026, odpowiedź na pytanie, jak brzmią dźwięki). Poziomy i warianty z `sfx.py` zostają jako domyślne.
- **Otwarte:** instalacja oficjalnych skilli HyperFrames i GSAP oraz aktualizacja HyperFrames 0.9.20 → 0.9.63 (ma wbudowany dobór SFX, ale zmienia sposób szukania ffmpeg). O żadne z nich nie prosił.

## 2026-11-18, IMG_0591 „Szczęście, plan czy pragnienie” (4 pliki: hook A i B, z efektami i tylko z napisami)
- **Zlecenie:** „dwie wersje po dwa hooki, chcę jedną pociętą tylko z napisami, a drugą normalnie z efektami”. Plan na ok. 65 s, nagranie na ok. 150 s, wyszło ok. 93 s.
- **Pierwszy film z biblioteką, rotacją przejść i dźwiękami.** Z biblioteki wszedł jeden szablon (`kinetic-type-swap`), reszta to nowe własne elementy (hasła nad głową, macierz 2×2, licznik, oś czasu, pierścień).
- **Decyzje, o których mu powiedziałem:** obraz odbity (lustrzane nagranie), napisy niżej niż zwykle (niski kadr), hook B inny niż w planie (nagrał pełne cytaty), co wypadło z nagrania.
- **Moje błędy:** trzy urwane słowa na końcach kwestii uznałem za halucynacje i poszły do pierwszego renderu; dwa rendery padły na braku miejsca na dysku, bo HyperFrames zostawia po każdym renderze ok. 6 GB klatek w katalogu tymczasowym. Oba opisane w `narzedzia.md`.
- **Ocena Jakuba, 18.11.2026:** „powtórzyłem i zaciąłem się w niektórych miejscach, przejrzyj i popraw”. Stylu, grafik i dźwięków nie skomentował.
- **Co było w oddanym filmie:** zdanie „gdzie autor pyta: sukces to szczęście czy umiejętności?” dwa razy pod rząd (2,5 s), „sukce- cesu” w pierwszym zdaniu hooka A i pauza w środku słowa „do… kładnie”. Powtórkę `kawalki.py` pokazywał, ale ją przeoczyłem; dwa zająknięcia wyszły dopiero przy podziale w pauzach od 0,09 s.
- **Poprawka:** kwestia 3 od drugiego podejścia, dwa wycięcia ze środka kwestii (nowe pole `wytnij` w `SEGS`): w „sukcesu” ze zbliżeniem w miejscu cięcia, w „dokładnie” sama pauza. Film krótszy o ok. 2,7 s.
- **Mój błąd przy poprawce:** pierwszy render poprawek miał „wiedziałem kładnie” (wyciąłem „do”, biorąc pauzę w słowie za powtórzoną sylabę) i „Napoleon” bez „Hill” (skrócony ogon). Złapała to kontrola eksportu, drugi render jest z dobrymi cięciami. Zostawione świadomie i zgłoszone: wolno wymówione „utożsamiam”, westchnienie „Europa, no… co ja mogę rzec?”, szybkie „A Ty co myślisz?” (innego dubla nie ma).
- **Zmiana w skillu:** `kawalki.py` sam oznacza powtórki i obce kawałki i ma tryb `--drobne`, doszły `fonemy.py` i `czesci.py`, `aroll.py` umie wycinać ze środka kwestii. Ocena poprawionej wersji: na pytanie, czy wyciąć jeszcze trzy zostawione miejsca („utożsamiam”, „Europa, no… co ja mogę rzec?”, szybkie „A Ty co myślisz?”), odpowiedział „zostaw jak jest” (18.11.2026). Samych sklejek nie skomentował.

## 2026-11-18, strefa bezpieczna (zmiana w skillu) i IMG_0597 „Dałem AI 1000 zł na reklamy książek” (pierwsza rolka PerfOS)
- **Zlecenie:** „Masz tu rolkę z perfosem (ściągnij sobie branding z perfos.pl). Zaktualizuj też w skillu safe zone (napisy i animacje czasem są za wysoko bądź za szeroko – masz tutaj templatki, które znalazłem w necie)”. Dwa szablony: Instagram Reels (góra 14%, dół 35%, boki 6%) i Jon Loomer (Reels i Stories). W trakcie dosłał zrzuty z panelu PerfOS (lejek, ROAS, przychód, średni koszyk) i z Shopify.
- **Zmiana w skillu:** strefa jako część wspólna obu szablonów (`SAFE` w `scripts/kompozycja.py`, zasada 9 w SKILL.md, `styl.md` punkt 8). Napisy 620 px zamiast 950 (frazy do ok. 20 znaków), hook od 960 px, nakładki z 96–150 px na 290–300 px albo nad napisy, pole CTA z 1262 na 990 px, przykładowe frazy szablonu podzielone. Nowy `scripts/strefa.py`: kontrola całego filmu (klatka na koniec każdego napisu i co 0,75 s, jasne piksele poza strefą) i obrys strefy na klatkach. `rolki_promo.py` bierze szerokości z szablonu.
- **Sprawdzone:** IMG_0597: 256 klatek, 0 poza strefą; kontrola złapała treść wyjeżdżającą górą w trakcie przejścia `slide`, więc klatki przejść są pomijane. Szablon sprawdzony na kopii IMG_0526 (95 klatek): kontrola złapała hook z linią dopowiedzenia wychodzący dołem (stąd `KIN_TOP` 900) i ptaszek kafelka za prawą krawędzią (kafelki 290 px), a klatki pokazały, że powiadomienie na 290 px zasłania włosy, więc w szablonie powiadomienie i chip stoją domyślnie nad napisami. Po poprawkach 0 poza strefą.
- **Rolka (116 s, scenariusz zakładał 45 s):** montaż poszedł za nagraniem, razem z lejkiem, ROAS-em i wątkiem piksela i Shopify. Liczby z nagrania i zrzutów (4220 zł, ROAS 3,38), w nagłówku scenariusza było 3700 zł.
- **Marka PerfOS:** tło `#0f0f0f` z siatką, mięta `#00E5A0`, krój Geist w grafikach, logo na dwóch planszach; napisy i hook bez zmian. Plansze to odtworzone karty z panelu (lejek, średni koszyk, ROAS z wykresem, Shopify) z toczącymi się cyframi i przełącznikami. Paleta `perfos` jest tylko w projekcie.
- **Moje decyzje do jego oceny:** hook sklejony z dwóch dubli (w ostatnim „AI” brzmiało jak „jej”), wycięty wtręt „gdzie na dziś dzień mamy 17 listopada”, pigułki i dymek zamiast napisu w dwóch miejscach, logo PerfOS w rolce, nakładki nad napisami zamiast u góry (głowa zajmuje górę kadru), z lejka pominięte żółte wyróżnienie i uwaga panelu.
- **Moje błędy:** dwa cięcia ustawione według heurystycznych czasów z `wyspy.py` (ogon „listopada”, ucięte „złotych”) wyszły dopiero po `slowa.py` i kosztowały dwa przerwane rendery A-rollu; render HyperFrames puszczony przez `&` anulował się po 7 s; przy sprzątaniu własnych plików tymczasowych usunąłem też osierocony `v.mp4` (43 MB) po wczorajszym przerwanym renderze innej sesji. Pułapki opisane w `narzedzia.md`.
- **Uwaga do IMG_0591:** tamta rolka wyszła tego samego ranka z napisami na 1420 px, czyli poza strefą; Jakub poprosił o przeróbkę, zrobiona (wpis niżej).
- **Ocena Jakuba (wersja 1):** „Mega spoko… bardzo fajnie to wyszło, więc jak najbardziej akceptuję. Tylko ta jedna poprawka”:
  - „gdy mówię «no i wynik», to powinno być bardziej zbudowane napięcie, czy troszkę przedłużone, i takie na przykład przybliżenie na moją twarz”;
  - „mam wrażenie, w niektórych miejscach troszeczkę za szybko przyciąłeś, możesz to sprawdzić”.
- **Czego nie skomentował:** logo PerfOS, węższe napisy, nakładki nad napisami, sklejony hook, długość 116 s, odtworzone karty, dźwięki. Brak uwagi przy ogólnej akceptacji, nie pochwała każdej z tych rzeczy.
- **Wersja 2:** przy „No i wynik” dojazd na twarz na słowie, 1,1 s pauzy (zwolnienie 50% i zatrzymana klatka, bo po słowie patrzy w kamerę tylko 0,15 s), ciemniejące brzegi, narastający szum, napis do końca pauzy. Cięcia: po zdaniu 0,22 s i przed 0,14 s (było 0,15 / 0,10), scalone kwestie z naturalną pauzą. Pomiar pokazał, że próg −45 dB kończył słowa za wcześnie (ciche końcówki do −55 dB). **Mój błąd w wersji 2:** uznałem 0,2 s po „dziś” za uciętą końcówkę i wydłużyłem kwestię, a była to dźwięczna zapowiedź wyciętego słowa „gdzie”; kontrola eksportu pokazała „dziś Gli-perfos”. Naprawione wyciszeniem dźwięku od 119.86 i podmianą samej ścieżki (bez renderu obrazu). Zmiana w skillu: `styl.md` punkty 5 i 6, `pipeline.md` punkt 5, domyślne marginesy w `scripts/aroll.py`.
- **Uwaga do wersji 2:** dwa zrzuty, „patrz jak nierówno to zrobiłeś… każde takie chujowe – wycentruj ładnie, uwzględniając safe zone”. Rząd kafelków był przesunięty o ok. 110 px w prawo względem etykiet i pigułki: w szablonie `kompozycja.py` jest stara klasa `.tiles` (kafelki „urlop/choroba”) z `right: 0` i `justify-content: center`, która nałożyła się na nową klasę o tej samej nazwie. Poprawka: własne nazwy klas (`.ltiers`, `.ltiles`) i sprawdzenie klatki z linią środka 540 px.
- **Wniosek:** nowym elementom dawaj nazwy klas, których nie ma w szablonie (`grep` w CSS przed użyciem), a każdy rząd, który ma być symetryczny, sprawdzaj na klatce z narysowaną osią 540 px i krawędziami strefy.
- **Ocena wersji 3:** czeka.

## 2026-11-18, IMG_0591 „Szczęście, plan czy pragnienie” przerobiona pod strefę bezpieczną (4 pliki, cięcia bez zmian)
- **Zlecenie:** „przerób też rolkę o Thielu pod nową strefę”. Rolka wyszła o 9:36 (i poprawiona o 11:12 przez inną sesję) z napisami na 1420 px i grafikami od 100 px, czyli poza strefą.
- **Co wyszło z pomiaru:** Jakub siedzi nisko, broda na 62–76% wysokości kadru (mediana 69%). Przy napisach na 1160 px broda musi kończyć się przed nimi, a to znaczy zoom 1,15–1,6, nie ten sam kadr co wcześniej. Pomiar twarzy robi teraz `scripts/twarze.py` (Vision z macOS, bez pobierania, `scripts/twarz.swift`), a `kadr()` w `aroll.py` dobiera zoom z zapasem na zarost. Pierwsza próba (broda do 1090 px, zoom do 1,9) dała twarz na pół ekranu i hasła na oczach; złagodzona do 1200 px i 1,6.
- **Pracowałem w kopii** (`IMG_0591_strefa`), bo druga sesja w tym samym czasie poprawiała cięcia w oryginale; potem skrypty wróciły do `IMG_0591` (stare w `_przed_strefa/`), a cztery pliki w Eksporty zastąpiłem moimi (te same nazwy).
- **Kontrola złapała dwa błędy, których nie widać na pojedynczej klatce:** pulsująca komórka „Europa” sięga 6 px za prawą krawędź (885 px) i descendery napisów 3 px za dolną (1245 px). Poprawione przesunięciem macierzy o 17 px i `CAP_TOP` 1160.
- **Podpis „Napoleon Hill” pod pierścieniem** wypadł, bo napis stoi teraz tuż nad nim i słowa były zdublowane.
- **Szablon kompozycji z IMG_0591 nie dostał jeszcze strefy w `scripts/`**, tylko wzór w `projekty/IMG_0591/skrypty/kompozycja.py` (`SAFE`, `rozbij()`, `STREFA`); w `scripts/kompozycja.py` strefa jest od rana.
- **Ocena Jakuba:** zapytany, czy zostawić bliższą twarz, czy szukać innego kadru, odpowiedział „Zostaw”. Bliższy kadr z pomiaru twarzy zostaje; o hasłach zachodzących na włosy nic nie dodał.

## 2026-11-18, cztery własne szablony b-roll
- **Skąd:** Jakub wkleił listę „5 libraries that kill AI slop” (HorizonX, Grainient, Arc UI, uberdesigner, Bencho) z pytaniem, czy to coś do montażu, czy tylko do aplikacji. Odpowiedź: prawie wszystko do aplikacji (React, animacje pod kursor), do montażu wprost tylko tła Grainient i mockupy HorizonX, oba płatne. Niczego nie kupował.
- **Jego decyzja:** na propozycję 3–4 szablonów wzorowanych na darmowych komponentach Arc UI i Bencho odpowiedział „Tak, zrób”.
- **Zrobione:** `pipeline-kanban`, `line-scrub-card`, `tick-slider`, `dot-heatmap` w `biblioteka/`, opis w `biblioteka.md`, podgląd na `biblioteka_arkusz_3.jpg`. Tablica kanban w Arc UI jest w płatnej części, wziąłem z niej tylko ogólny pomysł, bez kodu.
- **Przy okazji:** okazało się, że pudełko w `styl` nie skaluje szablonu, więc `mount()` dostał parametr `pole` (pomniejszające opakowanie na pole strefy).
- **Ocena Jakuba, 18.11.2026 (po podglądzie wideo):** „wszystkie super, można używać od dziś w rolkach”. Szablony nie były jeszcze w żadnym filmie.

## 2026-11-19, IMG_0640 „Graf firmy” (Mit przedsiębiorczości; rolka organiczna, 77 s)
- **Zlecenie:** scenariusz na 45–60 s z hookiem, kartką z grafem adGen z góry i puentą; napisy 1/2/3 i „TWOJA FIRMA TO KORPORACJA. NAWET JAK JESTEŚ SAM.” zamówione wprost. Wyszło 77 s, bo tyle treści jest w nagraniu.
- **Nagranie:** trzy ujęcia w jednym pliku (statyw, kartka z góry, z ręki przy oknie), dźwięk z krawatowego w pliku. Puenta „Kratka to odpowiedzialność” padła w trakcie podnoszenia telefonu, więc ten moment przykrywa plansza.
- **Nowe rzeczy:** ciemny miękki podkład pod napisami nad białą kartką (bez zmiany wyglądu napisów), cyfrowy graf działów z agentami wpadającymi na słowach, karty nad kartką zamiast nakładek nad napisami, render z klatkami JPG przy pełnym dysku. Szablonów z biblioteki nie użyłem (treść wymagała własnych).
- **Do jego oceny:** „kartek” w nagraniu podpisane jako „kratek”; „kampanie na Mecie” ze scenariusza nie padły, więc ich nie ma; rolka dłuższa niż plan.
- **Ocena Jakuba:** najpierw „na końcu powtórzyłem się 3 razy” (w gotowym pliku każde zdanie końcówki pada raz; trzy wcześniejsze duble „narysuj swój graf” były wycięte), po moim pytaniu, co dokładnie się powtarza: „nic nie rób, jest ok”. Rolka zostaje bez zmian; o grafikach nic nie powiedział.

## 2026-11-20, IMG_0688 „Agent AI w pół roku” (PerfOS, dzień 3 Build in Public, 49,7 s)
- **Zlecenie:** nagranie plus scenariusz na ok. 30 s z licznikami (349 000 zł, 37 746 leadów, 4 587 grafik), paskiem w mięcie i przekreślanymi rolami; uwagi z wklejki: ostrożnie z liczbą leadów.
- **Nagranie:** treści na ok. 50 s, ok. 20 dubli „dzień trzeci Build in Public”, hook B ze scenariusza nie nagrany. Montaż poszedł za nagraniem.
- **Nowe:** kadr ze środka twarzy z pomiaru (`twarze.py` + `twarz_ujecia()` w `aroll.py`) przy dalekim ujęciu; liczniki z toczącymi się cyframi w jednej planszy; karty ról przekreślane na „Teraz”. Pułapka: spacja tysięcy w `wheel()` zwijała się („349000”), teraz twarda spacja.
- **Ocena Jakuba:** „dałeś za ciemny obraz”. Źródło (ciemny pokój, zielone LED) miało średnio 48/255, a standardowy grading (gamma 0,96, mocna winieta) zbił je do 30–35. Poprawka: `eq=contrast=1.04:saturation=1.08:gamma=1.34:brightness=0.015`, winieta PI/8, średnio 63–66. Ocena wersji jaśniejszej: czeka.

## 2026-11-23, IMG_0718 „Mój stack AI” (rolka organiczna, 72,7 s)
- **Zlecenie:** „ma tam być na starcie wspomnienie, że oglądaj do końca po cały stack, albo żeby go odebrać… (i podgląd tego PDF-a, jak go przeglądasz)”. Do nagrania dołączył PDF „Mój stack AI w agencji” (14 stron).
- **Nagranie:** 6,5 min, bardzo dużo dubli (hook w 5 wersjach, „Po prostu etaty zastąpiliśmy…” i „A oto struktura…” po kilkanaście razy). Wybrane ostatnie pełne duble, sklejki w środku zdań przy „Grok Bot, | które…” (koniec „bot” z obwiedni) i „robotę zarządczą, | czyli…”. Falstarty z `kawalki.py --drobne`: „Reklamy na…”, „czyli zarządzają wszystkimi AI…”, „Także napisz pod tym filmem” (powtórzone).
- **Zapowiedź na starcie:** karta u góry kadru przez cały hook („ZOSTAŃ DO KOŃCA / Cały mój stack AI / PDF do odebrania na końcu”) z miniaturą PDF-a, która sama się przewija. Przy „rozpisałem cały ten mój stack AI… narzędzie po narzędziu” pełna plansza z przeglądanym PDF-em w perspektywie i plakietką „AUTOR: GROK” na jego żarcie. CTA: obserwuj → komentarz „AI” → karta pliku PDF; plansza końcowa z wachlarzem stron.
- **Nowe:** logotypy narzędzi wycięte prosto z PDF-a (spójne ikony), PDF → PNG przez PDFKit z macOS (`scripts/pdf_strony.swift`, bez instalowania poppler), plansza z 15 kafelkami, z których 10 obraca się w agentów AI.
- **Pułapka:** `constellation-hub` i `grid-card-assemble` z biblioteki po zmniejszeniu do pola strefy (`pole`) mają napisy 16–18 px (check: `text_below_floor`, a nagłówek planszy był pod szablonem: `text_occluded`). Zastąpione własnymi grafikami z tekstem 30+ px. Przed użyciem szablonu w polu sprawdź rozmiar czcionki w raporcie checka.
- **Grading:** ten sam pokój co IMG_0688, ale jaśniejsze źródło (YAVG 69), więc łagodny grading (gamma 1,06); A-roll 58–67.
- **Do jego oceny:** zostawione „To znaczy Grok, bo to zrobił”, „zarządzają wszystkimi etatami” (tak w ostatnim dublu), wiadomości w Slacku poglądowe, rolka 73 s.
- **Ocena Jakuba, 23.11.2026:** „super jest, puszczam to”. Bez poprawek; zostawione miejsca (żart o Groku, „etatami”, poglądowy Slack, 73 s) przyjęte bez uwag. To ogólna akceptacja, nie osobna pochwała każdego elementu.

## 2026-11-23, IMG_0720 + IMG_0721 „AI: masakra / spoko / genialne” (rolka organiczna, 36,3 s)
- **Zlecenie:** dwa nagrania i przykładowa rolka (snapgram) „żebyś wiedział, jak podkładać loga”: 4 kategorie po 3 narzędzia, „znajdź sobie te wszystkie loga i nad moją głową je zawieś”. Podał przypisanie narzędzi (maile: Gemini / Claude / Grok Bot; notatki: Google Note Taker / Fireflies / Fathom; kampanie FB: FastTony / Claude ze skillami / PerfOS; montaż: After Effects / Edits / Claude ze skillami).
- **Format z referencji:** rząd trzech kafelków nad głową z etykietami, pod nimi pigułka z kategorią; logo kolejnej kategorii najpierw rozmyte i przygaszone, ostre na „to jest…”, a na werdykcie kafelek pulsuje (GENIALNE z miętową poświatą). Etykiety MASAKRA / SPOKO / GENIALNE w palecie marki (szary, biały, akcent) zamiast czerwonego, pomarańczowego i zielonego z referencji. Dopiski „Note Taker” i „+ SKILLE” pod kafelkami. Kadry z twarzą niżej (środek na 47–48% wysokości), żeby głowa nie wchodziła pod rząd.
- **Dwa pliki jako jedno źródło:** `ffmpeg -f concat -c copy` sklejone bez rekompresji w `aroll/zrodlo.mov` (obrót zachowany), więc wszystkie skrypty działają na jednej osi czasu.
- **Pułapka:** przytrzymanie pod planszę końcową (`END_HOLD`) sięgało 1,8 s za koniec nagrania i A-roll miał 1035/1089 klatek; pierwszy render przeszedł z tym ostrzeżeniem niezauważony. Poprawka: `tpad=stop_mode=clone` w każdym ujęciu w `aroll.py` (projekt IMG_0720). Ostrzeżenie „NIEZGODNE” w logu A-rollu zawsze czytaj.
- **Logotypy:** Gemini, Google Meet (jako „Google Note Taker”), After Effects z Wikimedia Commons, Fireflies i FastTony ze stron producentów, Edits z App Store (w `~/Desktop/Montażysta AI/Grafiki/logo/`, źródła w `ZRODLA.txt`); Claude, Grok Bot, Fathom i PerfOS z PDF-a stacku (grokbot.com przekierowuje na x.ai bez własnego logo).
- **Do jego oceny:** etykiety w palecie zamiast kolorów z referencji, Google Meet jako znak „Google Note Taker”, brak tytułu u góry (w referencji był), pominięta rozmowa i próby z początku nagrania.
- **Uwagi Jakuba do wersji 1 (23.11.2026):** zrzut z rzędem logo i głową tuż pod pigułką kategorii: „źle wykadrowane…”; oraz „do «wyjebania» zacenzuruj i przykryj mi wtedy usta (jak na śmiesznych filmach albo na YouTubie, żeby nie zdejmowali monetyzacji)”.
- **Wersja 2:** rząd logo zwarty (kafelki 160 px, kończy się ok. 580 px), twarz niżej w kadrze (środek na 50%, bez zbliżenia 1,5), napisy na 1160 px. Przekleństwo: w głosie piknięcie 1 kHz na czas słowa (`audio/aroll_cenzura.wav`), w napisie „#@!%&”, na ustach czarny pasek z „#@!%&” (pozycja ust z `twarze.json` i kadru). Whisper w gotowym pliku słyszy „do ***”.
- **Wniosek na przyszłość:** gdy grafika ma wisieć nad głową, kadr ustawiaj pod nią od razu (głowa z włosami poniżej dolnej krawędzi rzędu, broda nad napisami). Cenzura przekleństw obowiązuje zawsze („Tak, zawsze”, 23.11.2026), zasada w `ZASADY.md`.
- **Uwaga do wersji 2:** dwa zrzuty, „patrz jak nierówno to zrobiłeś… każde takie chujowe – wycentruj ładnie, uwzględniając safe zone”. Rząd kafelków był przesunięty o ok. 110 px w prawo względem etykiet i pigułki: w szablonie `kompozycja.py` jest stara klasa `.tiles` (kafelki „urlop/choroba”) z `right: 0` i `justify-content: center`, która nałożyła się na nową klasę o tej samej nazwie. Poprawka: własne nazwy klas (`.ltiers`, `.ltiles`) i sprawdzenie klatki z linią środka 540 px.
- **Wniosek:** nowym elementom dawaj nazwy klas, których nie ma w szablonie (`grep` w CSS przed użyciem), a każdy rząd, który ma być symetryczny, sprawdzaj na klatce z narysowaną osią 540 px i krawędziami strefy.
- **Ocena wersji 3:** czeka.

## 2026-11-23, IMG_0717 „Zwolniłem montażystę” (rolka organiczna, 49,8 s)
- **Zlecenie:** samo nagranie, „dawaj tera to”. Treść: hook „Zwolniłem montażystę, którego nawet nigdy nie zatrudniałem”, 45 h i 3000 zł miesięcznie oszczędza jeden plik (skill), 30 rolek × 1,5 h, montażysta 3–4 tys. zł, agent w Claude, CTA „rolka”.
- **Nagranie:** 5 min, w pokoju rozmawiały inne osoby (wycięte). „Nie pierdolę.” po hooku półgłosem, wycięte zamiast cenzurowania.
- **Pułapki:**
  - źródło 1908×3304 (szersze niż 9:16): `crop()` w `aroll.py` wyliczał kadr wyższy niż nagranie i ffmpeg padał. Kadr liczę teraz od `min(SRC_W, SRC_H·9/16)`.
  - `twarze.py` miał na sztywno skalę 2160×3840, więc twarze wychodziły przesunięte i głowa była ucinana. Poprawione w skillu (`aroll.SRC_W/SRC_H`).
- **Grafiki:** prefiks klas `m7-` (lekcja z IMG_0720), kontrola osi 540 na klatkach, strefa 0 naruszeń. Kalendarz z trzema pustymi dniami jest poglądowy.
- **Uwaga Jakuba do v1:** „ten hook jest źle dobrany… «Zwolniłem montażystę, którego nawet nigdy nie zatrudniałem» – nielogiczne i bez sensu. Nawet moja mina wtedy jest zdziwiona, a trochę później powiedziałem ten poprawny hook”. Wziąłem zdanie spoza właściwego nagrania (próba w trakcie rozmowy z osobami w pokoju) tylko dlatego, że brzmiało jak hook.
- **v2:** hook „45 godzin i 3000 zł… jeden plik” jako kinetyczny na twarzy; nieudana próba i plansza liczników wypadły; 47,0 s; plik przemianowany na „45 godzin i 3000 zł”.
- **Wniosek:** hook to pierwsze zdanie właściwego nagrania (to, od którego zaczyna się ciąg dubli i treść), a nie efektowna linijka z rozgrzewki. Zdanie spoza ciągu biorę tylko wtedy, gdy ma sens w całości i nie widać po minie, że to próba; w razie wątpliwości pytam przed montażem.
- **Ocena v2:** czeka.

## 2026-11-24, PERFOS-film30 „PerfOS od środka” (film 16:9 z lektorem, glina z kie.ai + ekrany aplikacji)
- **Zlecenie:** film produktowy na YouTube, X i LinkedIn. Lektor EN to głos PerfOS z ElevenLabs V3, a postać jest z plasteliny (Kling 3.0). Montował Kreatywny (agent OpenBot) według tego skilla. Ekrany od IT będą 27.11, do tego czasu zastępuje je makieta panelu (`perfos.pl/nowy-panel`).
- **Uwagi Jakuba do v2:**
  - „nie czaję tego czarnego motywu z taką kratką… to jest tylko na etapie wyboru planu… po prostu brzydkie”. Tło `#0f0f0f` z kratką (z IMG_0597) wypada z filmów PerfOS, zasada jest w `ZASADY.md`.
  - „lektor się ucina w niektórych momentach i to nie jest takie płynne”. Przyczyna: ElevenLabs V3 kończył osobno generowane kwestie w środku ostatniego słowa. Ostatnie 40 ms plików miało od -19 do -37 dB zamiast ciszy („day”, „hire”, „headlines”, „ads”).
  - „przejścia pomiędzy ekranami czasami są zbyt szybkie”. Dwa ekrany trwały po ok. 1 s.
  - „ekrany muszą być ładnie zanimowane, np. przeglądanie strony albo nagrywanie”.
- **v3:**
  - Lektor: cała narracja w jednym zleceniu z kwestią-buforem na końcu („Okay, that's all for today.”, potem wycięta), cięcia w środku pauz, 0,25–0,5 s oddechu pod przejścia. Koszt 5,7 kr za podejście.
  - Obraz: okno aplikacji zostaje na ekranie i zmienia się tylko strona w środku. Do tego przewijanie, najazd kamery, obramowanie w mięcie na słowie i kursor z kliknięciem na „yes”. Plansze stoją na miętowym gradiencie z onboardingu. Wejścia trwają 0,8–0,85 s, wyjścia 0,6–0,65 s, zmiana strony 0,7 s. Długość 31,4 s.
- **Wniosek:** przy lektorze z TTS sprawdzaj obwiednią koniec każdej kwestii (ostatnie 40 ms mają być poniżej -50 dB), a narrację generuj jednym ciągiem. W filmach z aplikacją pokazuj ją tak, jak widzi ją klient, i animuj jak przeglądanie, a nie jako statyczne plansze.
- **Ocena v3:** czeka.

## 2026-11-24, zmiana stylu animacji: mniej, ale płynniej (zasada 10)
- **Zlecenie:** referencja (rolka o Instagramie ze snapgramu) i prośba: „wszystko jest mega płynne… nasze animacje są trochę mniej płynne… mniej tych przejść, ale więcej bardzo płynnych zoomów, jakaś bardzo ciekawa i złożona animacja… maksymalnie 2 animacje per 30 sekund… bardziej premium, bo teraz jest bardziej AI slopowe”.
- **Analiza referencji:** 27 s, jedno ujęcie bez twardych cięć, tylko 3 momenty graficzne:
  - jasna plansza z tekstem dopisywanym słowo po słowie;
  - jedna długa scena (ok. 8 s), w której kamera jedzie po ekranie telefonu i przybliża podświetlane elementy;
  - jedna karta komentarza na przyciemnionym obrazie.

  Przez resztę czasu jest sama twarz z miękkimi zoomami.
- **Zmiany w skillu:**
  - zasada 10 w SKILL.md;
  - `styl.md`, punkty 5 i 6;
  - szablon `kompozycja.py`:
    - domyślne przejście `"fade"`;
    - `pop` i `overlay` bez `back.out` (0,55–0,6 s, `power3.out` / `expo.out`, z rozmyciem);
    - `zoom()` na nowym kontenerze `#zwrap`;
    - `scena()` z ostrzeżeniem, gdy w oknie 30 s są więcej niż 2 sceny;
  - SFX 6–10 na minutę;
  - zasada w `ZASADY.md`.
- **Próbka:** IMG_0717 v3 („45 godzin i 3000 zł – PRÓBKA płynny styl”). Zamiast 12 grafik są 3 sceny:
  - scena A: 30 × 1,5 h → 45 h → paski i „ponad etat”, z kamerą odjeżdżającą od równania;
  - scena B: marki → agent w Claude → surowe nagranie → gotowa rolka, z kamerą zjeżdżającą w dół;
  - CTA z planszą końcową.

  Do tego 6 płynnych zoomów na twarz (`sine.inOut`, 1,4–3,5 s), 9 efektów dźwiękowych (11,5 na minutę). Wersja v2 została obok do porównania.
- **Ocena próbki 1:** „Mam uwagi… jakoś dalej mam wrażenie, że nie są takie płynne (np. w 60 fps), tak samo b-rolle (wstawki) nie są premium. W folderze Referencje i wytyczne znajdziesz 2 rolki, obejrzyj je”.
- **Druga referencja** (TikTok o Grok Bot, 54 s, 30 kl./s):
  - wstawki to jasne, kremowe plansze z małymi ikonami, cienkim ciemnym tekstem i białymi kartami z miękkim cieniem;
  - kilka razy ekran jest dzielony: wstawka u góry, A-roll na dole;
  - przejście to kurtyna: plansza zjeżdża z góry w ok. 0,35 s z miękkim startem i hamowaniem, treść tylko się przenika.

  Obie referencje mają 30 kl./s, więc płynność daje sam ruch, ale Jakub chce też 60 kl./s.
- **Zmiany:**
  - `FPS = 60` w `aroll.py`, `--fps 60` i `data-fps="60"`;
  - `panel(..., jasna=True)` (jasne tło, `.lcard`, kurtyna);
  - ciemne napisy z miętowym zakreślaczem na jasnych planszach;
  - opis w zasadzie 10.
- **Próbka 2:** IMG_0717 „PRÓBKA premium 60fps”, obie sceny jasne, kurtyna, render 60 kl./s (2820 klatek). A-roll został w 30 kl./s, bo `IMG_0717.mov` zniknęło z Pobranych.
- **Ocena próbki 2:** „Fajne białe tło, ale można by dodać też taką wersję blurred glass, tak jak na Apple… Daj różne wersje CTA (ale w podobnym stylu), takie bardziej różnorodne”.
- **Szkło:** `panel(..., szklo=True)`, matowa jasna tafla z `backdrop-filter`, A-roll prześwituje rozmyty. HyperFrames renderuje to poprawnie.
- **CTA:** moduł `scripts/cta.py` z 5 wariantami (`pole`, `arkusz`, `pigulka`, `profil`, `dm`) na jasnym szkle, bez sprężyn. Każda rolka ma dostać inny wariant niż poprzednia.
- **Demo:** `Eksporty/Rolki/2026-11-24 Szkło i CTA – demo/` (28 s, 60 kl./s, skrypt `scripts/demo_szklo_cta.py`).
- **Użyte CTA (prowadź od teraz):** IMG_0717 v2 – stare pole komentarza.
- **Ocena demo 1:** „zajebiste… daję Ci w referencjach moje zdjęcie profilowe, ten glass jest super, ale jeszcze trochę zrobiłbym bardziej jak Apple (liquid glass). Daj jeszcze 5 wersji planszy końcowej (aby była bardziej premium, może też być liquid glass)”.
- **Zrobione:**
  - CTA przestylowane na `.lglass` (Liquid Glass, biały tekst);
  - zdjęcie profilowe (od 24.11.2026 u użytkownika w `Referencje i wytyczne/Zdjęcie profilowe/`, nie w repo);
  - 5 plansz końcowych w `cta.plansza()` (`profil`, `slowo`, `telefon`, `jasna`, `stos`) na rozmytym A-rollu;
  - demo 2: „Liquid Glass, 5 CTA i 5 plansz końcowych” (48 s, 60 kl./s).
- **Użyte plansze końcowe (prowadź od teraz):** IMG_0717 v2 – stary dymek „ROLKA” na ciemnym tle.
- **Ocena demo 2 i decyzja (24.11.2026):** „zajebiste!!!! dobra, to daj eksport tego full, wrzucę na IG, zapisz całe referencje”. Wszystkie 5 plansz końcowych w rotacji.
- **Eksport finalny IMG_0717** „45 godzin i 3000 zł” (zastąpił v2):
  - 60 kl./s (A-roll w 30 kl./s, bo źródło zniknęło);
  - jasne sceny z kurtyną, płynne zoomy;
  - CTA `arkusz` (niższy arkusz z jednym starym komentarzem, `c-wys`, żeby nie wchodził na napisy);
  - plansza `profil` (karta 660 px, z zapasem na dryf 1,035 w strefie).
- **Użyte (rotacja):** IMG_0717 v3 – CTA `arkusz`, plansza `profil`.
- **Referencje (poprawka Jakuba):** „zdjęcia i grafiki referencyjne niech będą w README/installation… żeby wgrać w dane miejsce rolki, które się tej osobie podobają, np. swoje albo od ulubionych twórców, a także swoje zdjęcie profilowe”.
  - Pliki wyszły z repo.
  - Każdy trzyma je u siebie: `Referencje i wytyczne/Rolki wzorcowe/` i `…/Zdjęcie profilowe/`.
  - Instalator na końcu przypomina o wgraniu i otwiera folder.
  - `cta.przygotuj_avatar()` bierze zdjęcie stamtąd.
  - `references/wzorce/README.md` opisuje, czego szukać we wzorcach.
  - U Jakuba skopiowane: 2 rolki wzorcowe, zatwierdzone demo, `avatar.jpg`.
- **Ocena demo (24.11.2026):** szkło bez uwag; które CTA w rotacji: „Wszystkie 5”. Rotacja: pole → arkusz → pigulka → profil → dm, każda rolka inny wariant niż poprzednia.

## 2026-11-24, kontrola powtórzeń na całej rolce (`powtorzenia.py`)
- **Zlecenie:** „są jeszcze czasem miejsca, w których się powtarzam albo poprawiam bardzo szybko… wiem, że to ciężkie do wyłapania, ale może da się dodać do skilla jeszcze jedno sprawdzenie, czy na pewno nie ma powtórzenia na całej rolce”.
- **Odkrycie przy testach:** whisper nie zapisuje drugi raz frazy powtórzonej bez pauzy („Pewnie widzisz, że Pewnie widzisz, że…” wyszło raz), nawet na kawałkach dzielonych od 0,09 s. Dlatego doszło porównanie akustyczne (MFCC, podobieństwo fragmentu do fragmentu 0,2–3 s wcześniej).
- **Kalibracja:**
  - czyste rolki IMG_0717, IMG_0718 i IMG_0720: 0 alarmów;
  - prawdziwe falstarty Jakuba z surowego IMG_0717 („Dobrze użyte AI nigdy…”, „Pewnie widzisz, że…”, „tak jak to… tak jak ta”): 3 na 3;
  - wklejone wpadki (falstart, „Jedna jedna”, zdanie powtórzone na styku kwestii): 3 na 3;
  - IMG_0640: 2 miejsca do odsłuchu, m.in. końcówka „Daj znać w komentarzu, ile…”, czyli tam, gdzie Jakub zgłaszał powtórzenie.
- **Fałszywe alarmy usunięte:**
  - zdania o tej samej budowie („To jest masakrą. / To jest spoko”): reguła krótkich falstartów tylko dla kawałków urwanych;
  - sformułowania, które są dwa razy w tekście („który jest wspomagany przez”): akustyka je pomija, chyba że podobieństwo ≥ 0,85.

## 2026-11-24, scenariusze i CTA „zaobserwuj”
- Pierwsza rolka pod nowe zasady powstała ze scenariusza (skill `scenariusze-rolek`, paczka „3 scenariusze – freelancerzy i małe firmy”).
- Jakub: „CTA ma być coś w stylu «zaobserwuj», bo nie chcę mieć automatyzacji na każdej rolce”. Od tego dnia `cta.py` domyślnie w trybie „obserwuj” (5 CTA i 5 plansz), słowo-klucz tylko na prośbę.

## 2026-11-24, C4527 „20 ofert w godzinę” (pierwsze nagranie z kamery Sony, hook A i B, ok. 34 s)
- Nowe źródło: kamera Sony (XAVC 4K, obrót w metadanych, 29,97 kl./s, mikrofon w pliku). Hook A powiedziany dwa razy („Wysyłam 20 ofert w godzinie”), wzięte drugie podejście; falstart „Dałem jednym…”.
- Grafiki: jasna scena Grok Bot → Useme/Oferteo → zlecenia → oferta w Canvie; szklana 12 ofert / 8 odpowiedzi / 4 spotkania; plansza `telefon`.
- Problemy rozwiązane: napisy na białej koszulce (miękkie przyciemnienie obrazu pod pasem napisów), miętowe litery hasła gasły na zielonej ścianie (akcent jako zakreślenie), hasło na klatce 0 zasłaniało oczy (mniejsze 74 px).
- Do sprawdzenia przez Jakuba (zgłoszone): hook A mówi „20 ofert w godzinę”, a wynik „12 ofert po tygodniu”.
- **Uwaga Jakuba po oddaniu:** „czasami wkradają się krótkie przerwy pomiędzy jednym a drugim elementem… chciałbym, żeby były minimalnie krótsze”. Pomiar: 0,39–0,71 s między ostatnim słowem a pierwszym następnej kwestii. Poprawka: marginesy od faktycznego głosu (pipeline, punkt 5).

## 2026-11-24, C4528 „AI przypomina o fakturach” i C4529 „AI nie zabierze Ci klientów” (scenariusze 2 i 3, hook A i B)
- C4528: prawdziwa historia (administracja zapominała o fakturach, AI przypomina coraz mniej miło i przekazuje do windykacji). Falstarty „Najpierw… Najpierw”, „Potem SMS a c…”, hook B „Klient nie płacicie nad…”. Whisper na ostatniej kwestii z długim ogonem zwrócił tylko „Dobra, lecimy trójkę”: od tej pory `slowa.py` na przyciętej ostatniej kwestii. Plansza `jasna`.
- C4529: cztery falstarty; „Kogo wybiera klient? … Oczywiste” jako jedna kwestia z pauzą 0,8 s i najazdem 1,0 → 1,2 → 1,27 (napięcie). W wersji B mrugnięcie na klatce 0 (klatki 0–2 zastąpione klatką 3). Plansza `stos` (karty rozsunięte, bo zasłaniały uchwyt).
- Ocena: brak osobnej; uwaga o przerwach (wyżej) dotyczyła też tych rolek.

## 2026-11-24/25, paczka „5 scenariuszy – AI i biznes”: C4534 (IPO Anthropic), C4535 (OpenWorks), C4536 (Klarna), C4537 (oferta po callu), C4538 (skill)
- Montaż jedna po drugiej, każda w wersjach A i B, z logo nazw własnych (Anthropic, Claude, OpenAI, ChatGPT, Klarna, Grok Bot, Canva) z Wikimedia Commons / ikon stron.
- Poprawka faktów: w C4536 ostatni dubel miał „Klarna **rok temu** wpuściła AI” (to był luty 2024), wycięte ze środka zdania (`a_out`/`a_in`, zmiana kadru, sklejka sprawdzona whisperem w 3 kontekstach).
- **Uwaga Jakuba 1 (25.11):** „Dalej są takie przerwy pomiędzy ścinkami… pół sekundy albo sekunda… bardzo niepłynne. Weź to jeszcze bardziej zoptymalizuj… składaj całą rolkę wedle logiki całej tej wypowiedzi i scenariuszy… w rolce o OpenAI też się to zbugowało”. Znalezione i poprawione:
  - styki 0,3–0,4 s (raz 0,72 s przez „mmm” przed słowem) → ok. 0,15 s (`przerwy.py` do pomiaru);
  - OpenAI: kurtyna sceny A w górę i dopiero potem scena B, więc ok. 0,5 s mignięcia twarzy ze starym napisem → przenikanie; licznik „0000 $” przed zakręceniem → wchodzi z liczeniem;
  - logika: „…ale myślę, że to kwestia czasu” gryzło się z „U nas tego jeszcze nie ma” → dubel zgodny ze scenariuszem.
- **Ocena Jakuba po poprawce:** „Super, super, dużo lepiej”.
- **Uwaga Jakuba 2 (25.11), C4538 w 13–14 s:** „zacząłem pewien wyraz i pomyliłem się, i powtórzyłem go dosłownie pół sekundy później. Takie rzeczy też musimy wyłapywać”. Było to „Jed… jeden folder” (pauza 0,16 s, płytki dołek): kawalki.py i powtorzenia.py go nie widziały. Dodany przebieg mikro i reguła „restart słowa” w `powtorzenia.py` (na starej wersji wykrywa to miejsce; fałszywe alarmy najwyżej 1 na rolkę).
- Wnioski na stałe: zasady w `ZASADY.md` (logika i przejścia, restart słowa, styki), proces w `pipeline.md` punkt 12, wzór `wzory/C4538`.

## Statystyki z Instagrama

### 2026-11-24, zrzuty od Jakuba (6 rolek, IG + FB)
Przypisanie po klatce i długości; dwóch rolek z 1:33 i 1:51 nie da się pewnie przypisać do konkretnych podsumowań, więc ich liczby podaję razem.

| Rolka | Wyśw. | Pominięcia | Polub. | Kom. | Udost. | Zapis. | Krzywa |
|---|---|---|---|---|---|---|---|
| IMG_0688 „Agent AI w pół roku” (0:49) | 837 | 65,4% | 2,2% | 0,5% | 0,2% | 0,0% | spadek do ok. 25% w 3–5 s, potem płasko |
| IMG_0717 „45 godzin” v2, stary styl (0:47) | 556 | 74,8% | 2,5% | 2,5% | 0,0% | 0,4% | to samo |
| „Zakładając firmę… KORPO” (1:05, nie nasz montaż, duży napis od 1. klatki) | 624 | 63,3% | 5,9% | 0,0% | 1,0% | 0,0% | najłagodniejszy spadek |
| IMG_0718 „Mój stack AI” (1:12) | 1013 | 74,8% | 2,7% | 2,2% | 1,6% | 0,6% | spadek do ok. 20%, potem płasko |
| IMG_0576 „10K vs 100K” (1:33) i IMG_0597 PerfOS (1:51) | 1130 / 1382 | 68,1% / 68,6% | 3,2% / 2,9% | 0,2% / 0,9% | 0,5% / 0,4% | 0,0% / 0,4% | spadek do ok. 20–25%, potem płasko |

- **Wniosek:** widzów tracimy w pierwszych 2–3 sekundach (pominięcia 63–75%). Kto zostanie, ogląda prawie do końca, bo krzywe są płaskie. Środek montażu trzyma, a problemem jest wejście:
  - pierwsza klatka bez czytelnego hasła (napisy i hook kinetyczny pojawiają się słowo po słowie);
  - hook zaczyna się od kontekstu („W listopadzie 2025…”, „Dzisiaj, czyli dokładnie rok później…”), a nie od puenty;
  - hook mówi o Jakubie („moja firma”, „mój agent”), a nie o korzyści widza;
  - pierwsza klatka jest ciemna i ma niski kontrast (ciemny pokój, zielony LED).
- **Najlepszy wynik:** najmniej pominięć i najwięcej polubień i udostępnień miała rolka „KORPO” z dużym, gotowym napisem od 1. klatki i uniwersalnym tematem. Najwięcej udostępnień: „Mój stack AI” (konkretna wartość do zabrania). CTA ze słowem-kluczem działa (komentarze 2,2–2,5%).
- **Źródła:** Aktualności, Karta Rolki i Relacje; Eksploruj tylko 1,5–3,9%, czyli zasięg głównie u obserwujących.

### 2026-11-25, pomiar 24 h od Social Media Managera PB: „45 godzin i 3000 zł” (D0 IG + FB, publikacja 24.11, jedna wersja)
Źródło: `/Users/jd/OpenBot/Shared/PersonalBrand/analityka/2026-11-25.md` (statystyki rolki IG, odczyt 25.11 17:50). Której wersji montażu IMG_0717 dotyczy post, nie potwierdzono.

| Kanał | Wyśw. | Widzowie | Polub. | Kom. | Udost. | Zapis. | Nowi obserwujący | Wejścia na profil |
|---|---|---|---|---|---|---|---|---|
| Instagram | 718 | 278 | 7 | 10 | 0 | 2 | 0 | 0 |
| Facebook (crosspost) | 275 | brak | 1 reakcja | 0 | brak | brak | brak | brak |

- 51,4% wyświetleń od nieobserwujących, a mimo to 0 obserwacji i 0 wejść na profil. Średniego czasu i % obejrzeń IG nie pokazał.
- Komentarze to głównie słowo-klucz „rolka” z przypiętego komentarza (mechanizm Social Media Managera, poza montażem).
- **Wniosek dla montażu:** końcówka musi dać jasny powód, żeby wysłać rolkę dalej albo wejść na profil (np. „to część serii”, „w kolejnej rolce pokażę…”). Na planszy końcowej z „zaobserwuj” dopisek z tym powodem, ale tylko z tego, co Jakub mówi w nagraniu lub scenariuszu: serię wpisuję, gdy rolka naprawdę do niej należy. CTA nie trafia do opisu. Porównania hook A/B i pór będą od 26.11.

Brak danych. Format wpisu: data publikacji, projekt, średni czas oglądania, % obejrzeń do końca, gdzie spada wykres utrzymania (sekunda i co wtedy było na ekranie), wniosek dla montażu.

## 2026-11-25, C4537_v2 „Kończę call, oferta już czeka” (montaż testowy agenta-montażysty OpenBot, hook A i B, ok. 28 s)
- Zlecenie: Jakub wrzucił C4537 do `Surówki/nie zmontowane` jako test nowego obiegu (Surówki → w montażu → Eksporty/Rolki/Nieopublikowane). Montaż od zera według skilla; C4537 z 24.11 zostaje obok.
- Hook B pełniejszy niż w C4537: „Przestań pisać oferty po callu.” (15.59) + „Niech napisze ją rozmowa.” wycięte z pierwszego, szybkiego podejścia (9.91, w ciągłej mowie) + `post` 0,31 po „callu” (bez tego 0,02 s ciszy). Pułapka: 9.88 przechodziło 3 konteksty na surowym dźwięku, a kontrola eksportu (gotowy głos, kawałek 15 s) dała „W ogóle niech” (30 ms przejścia z „callu”). Sklejkę w ciągłej mowie sprawdzaj na `audio/aroll.wav` po `aroll.py --audio-only` w oknach 0–4 i 0–8 s, nie na sklejonym surowym nagraniu (jest ciszej, whisper potrafi pominąć całą kwestię).
- Ciche „mmm” przed „Na każdym moim callu” (29.28–29.62, −37…−42 dB) robiło 0,49 s przerwy → `a_in` 29.60; styki śr. 0,19 s.
- Scena A jako jedna bogata scena z kamerą: zakreślacze na słowach → przejazd kamery w prawo → fragmenty płyną do notatki → Grok Bot → oferta w Canvie z sekcjami. Pułapka: biała `.lcard` później w DOM przykryła przelatujące chipy (z-index 3). Ruch chipów tylko `x/y` (check odrzuca `left/top`). Przejazd kamery dopisany do `_okna_ruchu`, żeby strefa.py nie liczyła treści w ruchu.
- Scenariusz chciał CTA „pole” + planszę `profil`: CTA pole pominięte (3. złożona animacja w 30 s, zasada 10), plansza `profil` od „Zaobserwuj” z dopiskiem „Chcesz zobaczyć cały setup? / Daj znać w komentarzu”.
- Fakty spoza nagrania pominięte: nazwa notetakera (brak), „wysłano w 5 min” (brak czasu w nagraniu).
- Naprawione narzędzia: `oczy.sh` (`$Z:e` w zsh), `sprawdz_sync.py` (ścieżka nagrania na sztywno → `VIDEO` z `aroll.py`).
- **Użyte (rotacja):** C4537_v2 – CTA brak (plansza pełni CTA), plansza `profil`.
- Ocena Jakuba (25.11.2026, przekazana przez Social Media Managera i Personal Brand Managera): HOOK A („Przestań pisać oferty po callu”, opublikowany 18:00 na IG, FB, YT Shorts, TikTok) zdjęty ze wszystkich platform: w pierwszych 3 s „coś się powtarza i wygląda źle”. Ok. 19:45–19:51 w jego miejsce wyszedł HOOK B („Kończę calla…”). HOOK A nigdy nie wraca.
- Przyczyna: sklejka dwóch podejść tego samego zdania na 1,67 s (podejście 3 „…po callu.” + podejście 1 „Niech napisze ją rozmowa.” od 9,91 s, 40 ms po starcie głosu, w ciągłej mowie). Od cięcia whisper słyszy „O nich napiszę” (ułamek „u” z „callu”), obraz przeskakuje na inny plan i pozycję głowy. `powtorzenia.py` dał 0 (powtórzony ułamek głoski, nie słowo), a sklejkę testowałem tylko w oknach od 0 s. Wniosek i nowa kontrola: `poczatek.py`, notatka `kontekst/pamiec/feedback-pierwsze-5-sekund-sklejka.md`.
- Drobne w HOOK B: naprawa mrugnięcia (klatki 0–2 = klatka 8) daje na 0,10 s mały przeskok obrazu wstecz (klatka z 0,27 s, potem powrót). Przy kolejnych naprawach oczu bierz klatkę najbliższą startu (jak C4529 B: klatka 3), nie późniejszą.

## 2026-11-25, PERFOS-film30 wersja pionowa 9:16 (robocza, z poziomego filmu 16:9 z gliną i ekranami aplikacji)
- Zlecenie (CMO PerfOS, prośba Jakuba): pion 1080×1920 na Reels i Shorts z tych samych ujęć, bez nowych generacji. Projekt `projekty/PERFOS-film30/pion/` (osobny `skrypty/`, `hf/`, `analiza/`, więc `strefa.py` działa bez zmian). Dźwięk 1:1 z wersji poziomej (te same czasy słów i efektów).
- Przekadrowanie ujęć 16:9 (1928×1072): skala do 1920 px wysokości (×1,79) i wycinek 1080 px w miejscu bohatera, lekki `unsharp`. Postać centralna (P na biurku, P w maszynowni) wychodzi dobrze i dużo większa niż w poziomie. Gorzej: duże zbliżenie (soczewka wypełnia cały kadr) i scena szeroka, gdzie akcja jest w dwóch miejscach. Na to panorama: ujęcie w pełnej szerokości (3414 px) jako `<video>` i GSAP `x` od bohatera do detalu na słowie i z powrotem przed przejściem.
- Punkty przejść z poziomej kompozycji przeliczane funkcją (`v16()`: offset kadru 16:9 → skala → odjęcie wycinka), żeby koło z obiektywu i wyjście okna z oka trafiały w oko także w pionie.
- Ekrany aplikacji (zrzuty 1260 px szer.) w pionie: okno 690×700 w strefie (pod 860 px prawa krawędź 885), a w środku kamera po stronie: najazdy 1,2–1,7 i przejazdy między obramowaniami. Przy skali poniżej ok. 1,2 tekst panelu ma ok. 12 px i na telefonie jest nieczytelny; pierwsza próba z 0,95 odpadła na podglądzie. Strona nie może być niższa niż widok przy danej skali (biały pas pod spodem), a przy krawędziach zrzutów onboardingu widać ich miętowy margines: punkt kamery trzymaj w obrębie karty.
- Napis w akcencie na miętowej glinie ginie: pod napisami scrim (radialny, 0,5), a w ujęciu, gdzie na 1120 px stoi dół litery P, napisy niżej (1170 px, nadal w strefie).
- Hasło od klatki 0 (zasada 11) w dwóch wierszach małych słów, żeby nie zostało jedno słowo w drugiej linii.
- Kontrole: check 0 błędów, strefa 0, YAVG klatki 0 = 138.
- Ocena Jakuba: (czeka).

## 2026-11-26, kontrola każdego cięcia w 17 zaplanowanych wersjach (zlecenie Personal Brand Managera po HOOK A C4537_v2)
- Nowy skrypt `ciecia.py` (obwiednia nagrania ±0,5 s przy `a_in`/`a_out`, whisper w oknach od i do cięcia, urwane słowo, sklejka podejść, słowo dwa razy na styku). 154 cięcia w 17 plikach. Kalibracja: wycofany HOOK A C4537_v2 daje 2 alarmy na 1,67 s.
- Błędy: C4538 („Przestań tłumaczyć AI…”) A 9,20 s i B 10,53 s „pracu(ję)”, IMG_0720 („AI masakra…”) 19,23 s „zajebist(e)”. Oba to koniec kwestii postawiony przed ostatnią sylabą (zob. `kontekst/pamiec/feedback-kazde-ciecie.md`). Poprawki w `projekty/C4538_poprawka` i `projekty/IMG_0720_poprawka`, pliki „ - poprawka” obok zaplanowanych; zaplanowanych plików nie ruszałem.
- Reszta czysta. Znane: Klarna 5,23 s (A) / 4,53 s (B) celowe cięcie „rok temu” (opisane 25.11), 81 mld B „te narzędzie” na 2,96 s (napis „to narzędzie”).
- `aroll.py`: ostrzeżenie, gdy `koniec_mowy()` nie znajduje ciszy w 0,45 s.
- Ocena Jakuba: (czeka).

## 2026-11-27, PERFOS-film30 finał v5 (16:9, LinkedIn PL+EN, 1:1, 9:16) na prawdziwych ekranach aplikacji od IT
- Zlecenie (CMO PerfOS): podmiana makiet na zrzuty z konta pokazowego (E1–E7, 3840×2160), dwie poprawki faktu w lektorze, 4 wersje z jednego zestawu kompozycji. Projekt `projekty/PERFOS-film30/`.
- Zrzuty IT mają w PNG systemowy kursor (a pierwszy zestaw jeszcze znaczek trybu deweloperskiego Next.js „N”). Kursor usuwany łatką: z bliźniaczego zrzutu o identycznym układzie (różnica obrazów = sam kursor) albo kolorem tła. Kursor do kliknięcia dokładamy sami, więc stary w zrzucie dawałby dwa kursory.
- Treści zakazane w kadrze (koszt na zapytanie, progi kwotowe, polski format daty, kraj): kadrowanie zamiast zamazywania. Strona wjeżdża już w zbliżeniu, a kamera ma obszar dozwolony (`BOUNDS` z prawą krawędzią przed kolumną kosztu), bo przy najeździe od skali 1 zakazana liczba jest czytelna w klatkach pośrednich (OCR złapał „$17.32” w połowie najazdu). Gdy kadr nie wystarcza: zakrycie wyglądające jak interfejs (puste pole „Click to add” skopiowane z sąsiedniej karty, ucięcie „, 30.11” do „On Monday”), nie rozmycie.
- Kontrola treści po renderze: OCR (Apple Vision) klatki co 0,5 s ze wzorcami zakazów zleceniodawcy (waluta, słowo, data, kraj) i pomijaniem tekstu napisów z .srt. Fałszywe alarmy biorą się z przejść (blednąca strona pod spodem: „19 inquiries” → „1.9”) i polskich napisów czytanych bez ogonków; każdy alarm sprawdzić na klatce.
- Ten sam zestaw reklam na trzech ekranach (generowanie, akceptacja, „poniedziałek”) zastąpiony przy „Every Monday” kafelkiem „To do … Mon 7:12”, żeby nie powtarzać tych samych grafik.
- Kontrole: −14,0 LUFS, szczyt −1,7 dBFS, strefa 9:16 = 0, transkrypcja bez zakazanych zwrotów, OCR 0 prawdziwych alarmów.
- Ocena Jakuba: (czeka).

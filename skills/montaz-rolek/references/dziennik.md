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
- **Ocena wersji 2:** czeka.

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
- **Wniosek na przyszłość:** gdy grafika ma wisieć nad głową, kadr ustawiaj pod nią od razu (głowa z włosami poniżej dolnej krawędzi rzędu, broda nad napisami). Czy cenzurować przekleństwa zawsze, nie powiedział; to było przy tej rolce.
- **Ocena wersji 2:** czeka.

## Statystyki z Instagrama
Brak danych. Format wpisu: data publikacji, projekt, średni czas oglądania, % obejrzeń do końca, gdzie spada wykres utrzymania (sekunda i co wtedy było na ekranie), wniosek dla montażu.

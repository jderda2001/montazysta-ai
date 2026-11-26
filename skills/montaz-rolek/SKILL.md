---
name: montaz-rolek
description: Montaż pionowych rolek (Reels/TikTok/Shorts) i reklam wideo Jakuba w jego zatwierdzonym stylu i w palecie jego personal brandu (czerń, biel, ciemny szary plus akcent `#00E5A0`; reklamy adGen zostają pomarańczowe). Obejmuje synchronizację osobnego audio z mikrofonu z wideo z iPhone'a, wycinanie dubli i falstartów, napisy słowo po słowie, animowane plansze w HyperFrames, głos „studio AI” (Sidon + łańcuch radiowy), mastering, kontrolę i eksport do Eksporty. Używaj zawsze, gdy użytkownik wrzuca film lub nagranie do zmontowania („zmontuj”, „podmień audio”, „dodaj napisy”, „zrób rolkę”, „nowe video”, ścieżki .mov/.m4a), prosi o poprawki gotowej rolki, o wersję z innym hookiem lub o opis pod rolkę, albo pyta o styl montażu. Dotyczy to też sytuacji, gdy nie pada słowo „montaż”.
---

# Montaż rolek w stylu Jakuba

Ten skill zbiera to, co Jakub zatwierdził przy kolejnych filmach. Pierwszy wzorcowy projekt to `~/Montażysta AI/projekty/IMG_0526/` (rolka „Kaja zamiast settera”, 13.11.2026), o którym powiedział: „świetny montaż, trzymajmy się tego stylu”. **Najnowszy wzór rolki to `wzory/C4538/`** (repo; instalator kopiuje go do `projekty/C4538/`, 25.11.2026): kamera Sony, styl premium (zasada 10), hasło od klatki 0 (zasada 11), hook A i B, CTA „zaobserwuj”, cięcia od głosu, przenikanie scen. Przy nowej rolce kopiuj skrypty stamtąd (aroll.py, kompozycja.py, cta.py, powtorzenia.py), a nie z IMG_0526, i zmieniaj tylko dane nagrania oraz blok grafik w `build()`. Pełny kontekst o Jakubie i całą pamięć poprzedniego montażysty masz w `kontekst/` w repo.

Na start przeczytaj `references/dziennik.md`: co mu się podobało, a co odrzucił. To najszybszy sposób, żeby nie powtórzyć starego błędu.

## Paleta marki: czerń, biel, ciemny szary i jeden akcent

To jest montażysta personal brandu Jakuba, więc paleta obowiązuje w każdej klatce, którą sam rysujesz: napisy, plansze, nakładki, plansza końcowa, klipy A/B. Decyzja Jakuba z 17.11.2026, zastępuje wcześniejszy pomarańcz `#ff7018` we wszystkim poza reklamami adGen (wyjątek opisany niżej).

- **Baza to trzy kolory:** czarny (`#0f1012`), biały (`#ffffff`) i ciemny szary (`#141518`–`#222327` na tła i karty). Z nich jest zbudowane wszystko, co nie jest akcentem. Odcienie szarości na tekst pomocniczy i obrysy są w porządku, bo zostają w tej samej rodzinie.
- **Akcent pojawia się tam, gdzie jest sens wypowiedzi:** kluczowe słowo w napisie, puenta hooka, liczba, kafelek z ikoną, pasek, przycisk, ptaszek „zrobione”. Akcent pokazuje widzowi, co w tym zdaniu jest ważne, więc nie rozlewaj go na tła ani na całe akapity.
- **Główny akcent: `#00E5A0`.** Jakub nazywa go limonkowym. Używaj go domyślnie w każdym filmie.
- **Inny akcent tylko wtedy, gdy wymaga tego temat** (Jakub: akcenty mają zależeć od tego, o czym mówi). Jeden akcent na film, baza zostaje czarno-biało-szara. Jeśli wybierasz coś innego niż `#00E5A0`, powiedz mu o tym przy oddaniu i napisz dlaczego. Dopóki nie poda własnej listy kolorów pod tematy, w razie wątpliwości zostaje `#00E5A0`.
- **Na akcencie `#00E5A0` zawsze ciemny tekst i ciemne ikony (`#0f1012`).** Biały ma tam kontrast 1,6:1 i znika, czarny ma ponad 11:1.
- **Żadnych kolorów spoza palety w grafikach.** Dawny zielony „zrobione” `#3ddc84` też wypadł, jego rolę przejął akcent. Wyjątek to odtworzony cudzy interfejs i zdjęcia (awatar, zrzut ekranu), bo one mają wyglądać jak oryginał.

### Wyjątek: reklamy adGen zostają pomarańczowe

Jakub, 17.11.2026: „adGen zostaje pomarańczowy”. Reklamy adGen (te, które lądują w `Eksporty/Reklamy adGen/`) robisz w dotychczasowej palecie: akcent `#ff7018`, biały tekst na akcencie, zielony „zrobione” `#3ddc84`. Układ, ruch i napisy są te same co w rolkach, różni się tylko kolor.

O palecie decyduje to, czyja to marka, a nie format. Rolka organiczna, long-form i rolki promo to personal brand, czyli `#00E5A0`. Reklama adGen to pomarańcz. Jeśli z nagrania nie wynika, czy to reklama adGen, czy treść pod jego markę, zapytaj przed kompozycją, bo pomyłka oznacza cały film w złym kolorze. Zasada „nigdy logo adGen” dotyczy personal brandu i się nie zmienia.

### Jak to ustawić

W `scripts/kompozycja.py` jest słownik `PALETY` i przełącznik `MARKA`: `"personal"` (domyślnie) albo `"adgen"`. Inny akcent pod temat filmu to zmiana `accent` w palecie `personal`. Jaśniejszy koniec gradientu, poświaty i przezroczystości liczą się z akcentu same (`kolory()`), więc nie wpisuj kolorów na sztywno w CSS, tylko używaj zmiennych `--accent`, `--accent-hi`, `--accent-rgb`, `--on-accent` i `--ok`. Szczegóły są w `references/styl.md`, punkt 1.

## Zasady, których nie ruszasz

Każda z tych zasad wynika z jego wyraźnej decyzji. Złamanie którejś cofa zaufanie do całego montażu.

1. **Napisy są zamrożone.** Słowo po słowie, frazy po 2–4 słowa (do ok. 20 znaków, tyle mieści strefa bezpieczna), wyróżnienia kluczowych słów w kolorze akcentu, krój Inter Tight, pozycja i animacja jak w `references/styl.md`. Powiedział: „napisy zostawiłbym, nigdy bym ich nie zmieniał”. Nie eksperymentuj z ich wyglądem. Wolno poprawiać tylko trafność czasów. Kolor wyróżnień idzie za paletą marki (17.11.2026: akcent zamiast pomarańczu), reszta wyglądu bez zmian.
2. **Animacje z IMG_0526 to wzorzec.** Jego słowa: „świetne i bardzo poprawne”. Nowe grafiki projektuj w tym samym języku wizualnym (ciemne plansze, akcenty w kolorze marki, wejście z rozmyciem i light leakiem). Rozwijaj go, ale nie podmieniaj stylistyki bez pytania. Dwie poprawki z IMG_0576 (17.11.2026): w personal brandzie plansze nie mają kwadratów dekoracyjnych u dołu („nie podoba mi się to”), a wykresy i schematy mają być mocno animowane („zanimuj bardziej wykres”), czyli każdy element wchodzi ruchem na swoim słowie, a nie pojawia się gotowy. Jak, opisuje `references/styl.md`, punkt 4.
3. **Nigdy logo adGen.** Filmy są pod jego personal brand. Plansza końcowa to wezwanie do obserwowania ze zdjęciem profilowym, bez logo.
4. **Głos naturalny, bez AI.** Od 17.11.2026 domyślnie idzie dźwięk z mikrofonu po lekkim masteringu z `aroll.py` (highpass, łagodna kompresja, −14 LUFS). Jego słowa po IMG_0576: „za bardzo używasz voice enhancer AI, już kupiłem dobre mikrofony, także bez tego, albo z dużo mniejszym filtrem”. Wariant „C” (Sidon plus łańcuch radiowy), który wybrał 13.11.2026 przy mikrofonie stojącym pół metra od ust, robisz tylko na jego prośbę albo gdy nagranie jest wyraźnie złe (pogłos pokoju, daleki mikrofon), i wtedy mówisz mu o tym przy oddaniu.
5. **Efekty dźwiękowe tylko z prawdziwych próbek i tylko subtelnie.** Whooshe generowane z szumu określił jako „chujowe” (IMG_0361). 17.11.2026 sam poprosił o delikatne dźwięki pod animacje: „wyskakuje jakiś napis, to jest taki bardzo delikatny, subtelny dźwięk”, a przy animowanym wykresie „takie shhh”. Biblioteka leży w `~/Desktop/Montażysta AI/Muzyka/SFX/` (Kenney, CC0, i wybrane pliki z Mixkit, pobrane za jego zgodą), a miksuje ją `scripts/sfx.py`. Poziomy są celowo niskie (pyknięcia ok. −20 dBFS w szczycie, swooshe −21, „shh” −24, przy głosie −14 LUFS) i po odsłuchu próbki 17.11.2026 ocenił je: „Jest dobrze”. Nie podgłaśniaj ich bez jego prośby. Nowe paczki pobierasz dopiero po pytaniu z nazwą, źródłem i rozmiarem. Muzyka nadal tylko z `~/Desktop/Montażysta AI/Muzyka/`.
6. **Liczby i treści w grafikach tylko z tego, co mówi.** Jeśli coś jest poglądowe (np. „3 follow-upy” w powiadomieniu), powiedz mu o tym przy oddaniu.
7. **Pobranie czegokolwiek nowego** (model, biblioteka) wymaga pytania z nazwą, źródłem i rozmiarem. Wyjątek: zdjęcia, logo i okładki do filmu z zasady 10 pobierasz bez pytania (zgoda Jakuba z 20.11.2026).
8. **Parametry wyjścia:** 1080×1920, 30 kl./s, −14 LUFS, szczyt −1,5 dBFS.
9. **Strefa bezpieczna (safe zone).** Wszystko, co widz ma przeczytać albo zobaczyć, leży między 270 a 1245 px w pionie i między 70 a 1010 px w poziomie, a od 860 px w dół omija prawą kolumnę przycisków (prawa krawędź 885 px, od 1145 px 850 px). Jakub, 18.11.2026: „napisy i animacje czasem są za wysoko bądź za szeroko”, plus dwa szablony z sieci. Napisy mają przez to 620 px szerokości zamiast 950 (krótsze frazy, ten sam wygląd), nakładki nie stoją już na 96 px u góry, a pole CTA zeszło spod opisu rolki. Stałe są w `SAFE` w `kompozycja.py`, opis i rysunek w `references/styl.md`, punkt 8, a przed każdym renderem `scripts/strefa.py` ma pokazać zero klatek z treścią poza strefą.
10. **Mniej, ale płynniej (premium zamiast „AI slopu”).** Jakub, 24.11.2026, z referencją (rolka o Instagramie ze snapgramu): „wszystko jest mega płynne… mniej tych przejść, a więcej bardzo płynnych zoomów, jakaś bardzo ciekawa i złożona animacja… maksymalnie 2 animacje per 30 sekund… bardziej premium, bo teraz jest bardziej AI slopowe”. W referencji przez 27 s są tylko trzy momenty graficzne:
    - czysta jasna plansza, na której tekst dopisuje się słowo po słowie;
    - jedna długa, złożona animacja (ok. 8 s): ekran telefonu, po którym „kamera” płynnie jedzie i przybliża kolejne podświetlane elementy;
    - jedna karta komentarza na przyciemnionym A-rollu.

    Przez resztę czasu jest sama twarz z powolnymi, miękkimi zoomami, bez nakładek. Zasady:
    - **Najwyżej 2 złożone animacje na każde 30 s filmu.** Złożona to plansza, przepływ, wykres albo karta z kilkoma elementami. Logo przy nazwie własnej i CTA się wliczają, napisy nie. Zamiast pięciu małych kart daj jedną bogatą scenę, która rozwija się przez kilka zdań. `kompozycja.py` liczy sceny (`scena()`) i ostrzega przy przekroczeniu.
    - **Płynne zoomy zamiast przeskoków kadru i przejść plansz.** Najazd albo odjazd o 12–25% przez 1,5–3 s z `sine.inOut` / `power2.inOut`, na zdaniu, które coś akcentuje (`zoom()` w `kompozycja.py`). Twarde przeskoki W/M/C zostają tylko w miejscach cięć dubli.
    - **Ruch bez sprężyn.** Żadnego `back.out`, `bounce` ani podskoków. Wejścia trwają 0,5–0,8 s z `power3.out` / `expo.out`, z małym przesunięciem (12–24 px) i lekkim rozmyciem schodzącym do zera. Elementy jednej sceny wchodzą kaskadą, nie wszystkie naraz.
    - **Kamera wewnątrz grafiki.** W złożonej animacji przesuwaj i przybliżaj cały kontener sceny (scale + x/y), tak jakby kamera jechała po ekranie i zatrzymywała się na tym, o czym mówisz.
    - **Dwie sceny pod rząd** (mniej niż ok. 1 s twarzy między nimi): pierwsza `panel(..., fade_out=False, extend=0.75)`, druga `wejscie="fade"` (najlepiej jasna), czyli przenikanie nad pierwszą. Kurtyna w górę i od razu następna plansza daje ok. 0,5 s mignięcia twarzy ze starym napisem (C4535, Jakub: „zbugowało się”). Licznik (`wheel`/`roll`) wchodzi razem z liczeniem, bez widocznych zer.
    - **Przejścia plansz.** Domyślnie miękkie przenikanie z lekkim zoomem (`"fade"`). Iris, wipe, diag i slide najwyżej raz w rolce, light leak najwyżej raz.
    - **Czysto.** Jedna myśl na ekranie, dużo powietrza, mniej obramowań, poświat i chipów. Jasne tło planszy (biel albo jasny szary, czarny tekst, akcent) jest dozwolone w palecie i dobrze odcina się od ciemnego A-rollu.
    - Przy oddaniu wypisz sceny i ich czasy, żeby było widać, że w każdym oknie 30 s są najwyżej dwie.
    - **60 kl./s.** Jakub po pierwszej próbce: „dalej mam wrażenie, że nie są takie płynne (np. w 60 fps)”. iPhone nagrywa w 60 kl./s, więc A-roll (`FPS = 60` w `aroll.py`) i render (`--fps 60`, `data-fps="60"`) idą w 60. Gdy źródło jest w 30 kl./s, A-roll zostaje w 30, a grafiki i zoomy i tak renderuj w 60.
    - **Wstawki premium są jasne** (referencje w `Referencje i wytyczne/`, 24.11.2026: „b-rolle nie są premium”). Wstawka to pełnoekranowa jasna plansza: złamana biel `#f5f5f2` z delikatnym miętowym gradientem w rogu, ciemny tekst `#0f1012`, białe karty (`.lcard`) z cienką ramką `#e7e7e3` i miękkim cieniem, małe ikony, dużo powietrza. Bez poświat i grubych obramowań. Akcent tylko na jednej rzeczy (pasek, przycisk, liczba), na jasnym tle jako ciemniejsza mięta albo wypełnienie z ciemnym tekstem. Robi to `panel(..., jasna=True)`.
    - **Kurtyna:** jasna plansza zjeżdża z góry w 0,55 s z `power3.inOut` i tak samo odjeżdża, a treść tylko łagodnie się pojawia. To domyślne wejście jasnej planszy.
    - **Wariant szkło** (Jakub, 24.11.2026: „fajne białe tło, ale można by dodać też taką wersję blurred glass, tak jak na Apple”). `panel(..., szklo=True)` daje matową, jasną taflę (`backdrop-filter: blur(54px) saturate(165%)`), spod której prześwituje rozmyty A-roll, z półprzezroczystymi kartami `.lcard`. Przeplataj białą i szklaną wstawkę, np. jedną białą i jedną szklaną w rolce.
    - **CTA domyślnie „zaobserwuj”, bez słów-kluczy i automatyzacji DM** (Jakub, 24.11.2026: „CTA ma być coś w stylu «zaobserwuj», bo nie chcę mieć automatyzacji na każdej rolce”). `cta.cta()` i `cta.plansza()` mają `tryb="obserwuj"` jako domyślny. Kwestia CTA daje powód do obserwowania (następna rolka, seria, „po kolei pokażę Ci…”), może poprosić o zwykły komentarz („Którym jesteś?”), ale bez słowa-klucza. `tryb="slowo"` („Napisz SŁOWO w komentarzu”, link w DM) tylko na wyraźną prośbę Jakuba. W trybie obserwuj `slowo` to zwykły tekst: treść komentarza (`pole`, `arkusz`), wiadomość widza (`dm`), dopisek (`profil`), krótkie hasło lub liczba na planszy (`slowo`, `jasna`, `stos`, np. „40 H”, „8000 $”, „SKILL”) albo `""`. W praktyce (C4527–C4538) plansza końcowa wchodzi na słowie „zaobserwuj”/„koniecznie” i sama pełni rolę CTA, a osobne CTA na wideo pomijam, żeby nie przekroczyć 2 scen na 30 s.
    - **CTA za każdym razem w innym wariancie**, w tym samym jasnym, szklanym stylu (Jakub: „daj różne wersje CTA… bardziej różnorodne”). Warianty są w `scripts/cta.py`: `pole` (pole komentarza), `arkusz` (arkusz komentarzy z Instagrama), `pigulka` („Zaobserwuj @jakub.derda”, palec stuka), `profil` (Obserwuj → Obserwujesz) i `dm` (pytanie widza i odpowiedź „pokażę w następnej rolce”). Przed wyborem sprawdź w dzienniku, który wariant był w poprzedniej rolce, weź inny i zapisz, którego użyłeś. Podgląd wszystkich: `Eksporty/Rolki/2026-11-24 Szkło i CTA – demo/`.
    - **Liquid Glass na wideo** (Jakub: „glass jest super, ale jeszcze trochę bardziej jak Apple (liquid glass)”). CTA i plansze końcowe leżące na A-rollu są w klasie `.lglass` z `cta.py`: przezroczysta tafla z mocnym rozmyciem i nasyceniem tła, jasna krawędź z odblaskiem u góry po lewej, wewnętrzna poświata, biały tekst i miętowe akcenty z ciemnym tekstem.
    - **Plansza końcowa też w rotacji, 5 wariantów** w `cta.plansza()`:
      - `profil`: szklana karta ze zdjęciem w miętowym pierścieniu, hasło, podpis, przycisk Obserwuj → Obserwujesz;
      - `slowo`: wielka szklana pigułka z hasłem lub liczbą i odblaskiem, pod nią „Zaobserwuj @jakub.derda”;
      - `telefon`: szklany telefon z ekranem profilu i przyciskiem Obserwuj → Obserwujesz;
      - `jasna`: jasna plansza ze zdjęciem, zakreślonym hasłem i „Zaobserwuj @jakub.derda”;
      - `stos`: trzy szklane karty w wachlarzu (profil, hasło z podpisem, Zaobserwuj).

      Rotacja w praktyce: C4527 telefon, C4528 jasna, C4529 stos, C4534 profil, C4535 slowo, C4536 telefon, C4537 stos, C4538 jasna.

      Pod planszą zostaje rozmyty A-roll, więc ostatnie kwestie nie mogą być przykryte inną planszą. Każda rolka dostaje inną planszę niż poprzednia; zapis w dzienniku.
    - **Zdjęcie profilowe i rolki wzorcowe są u użytkownika, nie w repo:** `~/Desktop/Montażysta AI/Referencje i wytyczne/Zdjęcie profilowe/` (`foto = cta.przygotuj_avatar(P / "hf")` przycina do 512 px i kopiuje do `hf/`) oraz `…/Rolki wzorcowe/`. Przed montażem obejrzyj rolki wzorcowe. Gdy folder jest pusty, poproś o wgranie. Opis w `references/wzorce/README.md`.
    - Podgląd wszystkich CTA i plansz: `scripts/demo_szklo_cta.py` (film demo na tle dowolnego A-rollu).
    - **Napisy na jasnej planszy są ciemne**, a wyróżnienie to miętowy zakreślacz pod słowem. Krój, rozmiar, pozycja i ruch zostają; klasę `dk` nadaje `kompozycja.py` sam. To jedyny wyjątek od zasady 1 i wynika z czytelności.

11. **Pierwsze 2 sekundy decydują (od 24.11.2026, na podstawie statystyk).** Sześć rolek miało 63–75% pominięć: widzowie odpadają w 2–3 s, a kto zostanie, ogląda prawie do końca (krzywe płaskie). Najmniej pominięć miała rolka z dużym, gotowym napisem od pierwszej klatki („KORPO”). Szczegóły są w dzienniku, w sekcji „Statystyki z Instagrama”. Zasady:
    - **Klatka 0 ma pełny hook na ekranie.** `hook0()` w `kompozycja.py` stawia hasło (1–2 linie, 70–96 px, jedno słowo w akcencie) w górnej części kadru od pierwszej klatki, bez wjazdu i bez pisania słowo po słowie. Większość ludzi przewija bez dźwięku, więc w pierwszej sekundzie muszą przeczytać, o co chodzi. Hook kinetyczny z napisami słowo po słowie może iść pod spodem.
    - **Ruch od pierwszej klatki:** szybki odjazd kadru 1,12 → 1,0 w 0,6 s (`power3.out`). Robi to `hook0()`.
    - **Jasny start:** pierwsza klatka nie może być ciemna. `hook0()` rozjaśnia obraz przez pierwsze 1,2 s (brightness 1,15 → 1). Zmierz YAVG pierwszej klatki; cel to co najmniej ok. 70.
    - **Puenta w pierwszych 1,5 s.** Zaczynaj od najmocniejszego zdania (liczba, kontrast, teza), a kontekst daj potem. Zdania typu „W listopadzie 2025…” czy „Dzisiaj, czyli dokładnie rok później…” nie mogą otwierać rolki. Gdy w nagraniu puenta pada później, przestaw kolejność kwestii albo daj ją jako hasło `hook0()`.
    - **Hook pod widza, nie o sobie.** Hasło z klatki 0 mówi o korzyści albo problemie widza („Ten plik zastąpi Ci montażystę”), a nie o „mojej firmie”. Gdy nagranie mówi o Jakubie, hasło i tak może być pod widza.
    - **Zawsze 2 wersje hooka** do testu przez „Próbne rolki” na Instagramie: wersja A (puenta o Jakubie, jak w nagraniu) i B (hasło pod widza albo inna kolejność). Pliki `<Tytuł>_HOOK A_MM.RR.mp4` i `_HOOK B_` w tym samym folderze Eksporty, a wzór dwóch wersji jest w `projekty/IMG_0576` (`hookB/`). Przy oddaniu napisz, czym się różnią, i poproś o wynik testu do dziennika.
    - Wpisuj statystyki każdej rolki do dziennika (pominięcia, polubienia, komentarze, udostępnienia, kształt krzywej). Gdy hook B wygrywa kilka razy z rzędu, zmień domyślny styl hooka.

## Foldery i nazwy

- **Wejście:**
  - od 24.11.2026 zwykle kamera Sony: `C45xx.MP4` (XAVC, 3840×2160 z obrotem 90° w metadanych, czyli po obrocie 2160×3840, 29,97 kl./s), dźwięk z mikrofonu DJI w pliku (bez synchronizacji, `analiza/sync.json` z `offset: 0`). Pliki przychodzą z pulpitu albo z `~/Desktop/Montażysta AI/Surówki/nie zmontowane/`; po montażu, za zgodą Jakuba, przenieś je do `Surówki/zmontowane/` i popraw `VIDEO` w projektach. Wzór: `wzory/C4538/`;
  - starsze: wideo w `~/Downloads/IMG_xxxx.mov` (iPhone), audio z mikrofonu w `~/Desktop/Montażysta AI/Nagrania /` (uwaga: spacja na końcu nazwy folderu).
- **Projekt:** `~/Montażysta AI/projekty/<IMG_xxxx>/` z podfolderami `skrypty/`, `audio/`, `analiza/`, `aroll/`, `hf/` (HyperFrames), opcjonalnie `ab/` (porównania), plus `NOTATKI.md` i `napisy.srt`.
- **Eksport (zawsze porządek, struktura zatwierdzona 13.11.2026):** jeden folder na film, nazwany `<RRRR-MM-DD Tytuł>` (dzień eksportu), w folderze typu:
  - `Eksporty/Rolki/…/<Tytuł>_MM.RR.mp4`: rolki organiczne;
  - `Eksporty/Reklamy adGen/…/<Tytuł>_HOOK A_MM.RR.mp4`: reklamy, wersja na każdy hook;
  - `Eksporty/YouTube/…/`: long-form z `.srt`, opisem i rozdziałami, a 3 rolki promo w podfolderze `Rolki promo/`.
  Nazwy plików zostają pełne, żeby plik wysłany osobno nadal mówił, czym jest. Nic nie zostaje luzem w głównym `Eksporty`. Surowe nagrania nie trafiają do Eksporty, tylko do `Nagrania `.
- **Referencje od niego:** `~/Desktop/Montażysta AI/Referencje i wytyczne/`.

## Proces

Kolejność ma znaczenie, bo każdy krok korzysta z wyniku poprzedniego. Dokładne komendy i progi kontroli są w `references/pipeline.md`. Pułapki narzędzi (whisper, ffmpeg, HyperFrames, zsh) są w `references/narzedzia.md`. Przejrzyj je przed pierwszą komendą, bo oszczędzają godziny.

1. **Projekt.** Załóż folder `projekty/<nazwa nagrania>/`, skopiuj skrypty z najnowszego wzoru (`projekty/C4538/skrypty/` albo `wzory/C4538/skrypty/`), a do `hf/` konfigurację HyperFrames (`package.json`, `hyperframes.json`, `meta.json`, `fonts/`). Ustaw w `aroll.py` ścieżkę `VIDEO` (i `AUDIO`, gdy dźwięk jest osobno).
   - **Hook A i B:** w `aroll.py` słownik `HOOKI` (każdy hook to lista kwestii, np. dwa podejścia sklejone) i `N_HOOK = len(HOOKI[HOOK])`. Wersja B to podfolder `hookB/` z kopią `skrypty/`, linkiem do `audio/nowe_16k.wav`, `analiza/sync.json` i `twarze.json`, `hf/` oraz pustym plikiem `HOOK_B` (to on przełącza wersję w `aroll.py` i `kompozycja.py`). Zmiany w skryptach rób w głównym folderze i kopiuj do `hookB/skrypty/`.
   - Cały łańcuch dla jednej wersji: `zsh skrypty/przebieg.sh <folder>` (A-roll, powtórzenia, czasy słów, kompozycja, strefa, check).
2. **Synchronizacja** (`sync.py`): korelacja dźwięku telefonu z mikrofonem daje offset i dryf. Nigdy nie synchronizuj na oko.
3. **Transkrypcja i wybór dubli** (`wyspy.py`). Zasada: ostatni pełny dubel każdej kwestii, chyba że psuje logikę całości. Przed cięciem przeczytaj wybrane kwestie po kolei i porównaj ze scenariuszem: nic się nie powtarza, nie wyklucza i nie ma błędu faktycznego (C4535: „…to kwestia czasu” kontra „U nas tego jeszcze nie ma”; C4536: „rok temu”). Wtedy weź wcześniejszy pełny dubel albo wytnij wtrącenie. Wszystkie niewykorzystane warianty (inne hooki, CTA) wypisz w `NOTATKI.md` jako materiał na wersję B.
4. **Falstarty** (`kawalki.py`), obowiązkowo. Whisper na całym dublu wygładza zająknięcia, więc „I każdego ranka dosta… I każdego ranka dostaję…” wygląda jak czyste zdanie. Jakub sam wyłapał to w IMG_0526. Kawałek, który powtarza początek następnego, oznacza start kwestii od powtórzenia. Puszczaj oba tryby, zwykły i `--drobne`: skrypt sam oznacza `POWTORKA?` (w kawałkach słychać więcej sylab, niż ma tekst kwestii) i `?` (kawałek, w którym żadne słowo nie pasuje do tekstu), a na końcu wypisuje listę miejsc do sprawdzenia. Każde z nich rozstrzygnij osobnym whisperem na samym kawałku i drobną obwiednią (`fonemy.py`), nie czytaniem na oko. Zdanie powiedziane dwa razy pod rząd bierz od drugiego podejścia. Zająknięcie w środku kwestii (powtórzona sylaba „sukce- cesu”, pauza w środku słowa „do… kładnie”) wytnij polem `wytnij` w `SEGS`, a skok obrazu większy niż 3 klatki schowaj zmianą kadru dokładnie w miejscu cięcia. Zanim wytniesz, policz sylaby w `fonemy.py`, bo od tego zależy, co ma wypaść, a sklejkę sprawdź whisperem w trzech kontekstach (`pipeline.md`, krok 4). W IMG_0591 powtórzone zdanie i dwa zająknięcia poszły do oddanego filmu i Jakub sam musiał je zgłosić („powtórzyłem i zaciąłem się w niektórych miejscach”).
5. **A-roll** (`aroll.py`): lista `SEGS` (start, koniec, kadry, tekst), kadry W/M/C zmieniane między kwestiami i w pauzach, grading, cięcia z mikrofonu. Kontrola: `sprawdz_sync.py` (przesunięcie dźwięku względem obrazu poniżej klatki, typowo 4–5 ms).
6. **Głos:** domyślnie nic więcej nie robisz, bo `aroll.py` zapisuje `audio/aroll.wav` (naturalny głos po lekkim masteringu) i to on idzie do kompozycji. Tylko gdy Jakub poprosi o wariant C albo nagranie jest złe: `sidon_infer.py` na surowych cięciach (eksport przez `glos.raw_concat`), potem `studio.py`, z kontrolą przesunięcia (Sidon daje ok. 8 ms, skrypt wyrównuje), tonu (F0 bez zmian) i treści.
7. **Czasy słów** (`slowa.py`, whisper z DTW i `-nfa`), potem `waliduj_napisy.py`. Bez `-nfa` napisy wyskakują do 0,6 s przed mową.
8. **Kompozycja** (`kompozycja.py`): `PHRASES` (podział napisów i `*wyróżnienia*`) oraz grafiki liczone z czasów słów i cięć, nigdy wpisane na sztywno. Głos (`GLOS`, domyślnie `audio/aroll.wav`) wchodzi jako `<audio>`, a wideo jest wyciszone. Momenty efektów dźwiękowych dopisujesz w `build()` do listy `dzw` (wejścia plansz dodają swoosh same, resztę stawiasz Ty: `pop` na wyskakujący napis lub kafelek, `tik` na drobny ruch, `shh` na rysowanie wykresu, `powiad` na powiadomienie) i `kompozycja.py` sam miksuje je pod głos. Celuj w 6–10 efektów na minutę (mniej animacji, więc mniej efektów; zasada 10), tylko na ruchach, które coś znaczą. Potem `hyperframes check` (0 błędów), `hyperframes snapshot` w kluczowych momentach i `strefa.py` (0 klatek z treścią poza strefą bezpieczną). Obejrzyj klatki, zanim pójdziesz dalej.
8a. **Powtórzenia na całej rolce** (`powtorzenia.py`), obowiązkowo po `aroll.py` i jeszcze raz po każdej zmianie cięć. Jakub, 24.11.2026: „są jeszcze czasem miejsca, w których się powtarzam albo poprawiam bardzo szybko… dodaj sprawdzenie, czy na pewno nie ma powtórzenia na całej rolce”. `kawalki.py` widzi kwestie osobno, a whisper wygładza powtórzenie powiedziane bez pauzy, więc skrypt sprawdza całość czterema sposobami:
    - powtórzone frazy;
    - falstarty i urwane słowa;
    - słowa spoza tekstu kwestii;
    - akustykę: fragment, który brzmi jak fragment 0,2–3 s wcześniej, łapie powtórkę, której whisper nie zapisuje.
    - restart słowa w przebiegu mikro (dołki do −30 dB od 0,05 s, na głosie po masteringu): krótki kawałek, po którym następny zaczyna się od słowa o tym samym początku. Jakub, 25.11.2026 (C4538, 13 s): „zacząłem pewien wyraz, pomyliłem się i powtórzyłem go pół sekundy później… takie rzeczy też musimy wyłapywać”. Było to „Jed… jeden folder” z pauzą 0,16 s, której zwykły i drobny podział nie rozcinał, a whisper na całości pisał jedno „Jeden”. Mikro daje też fałszywe alarmy na urwanych spółgłoskach („Nikt” jako „Nie”), więc każdy rozstrzygnij uchem.

    Każde miejsce dostaje klip w `analiza/powtorzenia/`. Rozstrzygnij je uchem i `fonemy.py`, prawdziwe wytnij i puść kontrolę jeszcze raz. Oddajesz dopiero przy 0 miejscach albo z wymienionymi miejscami, które świadomie zostały (powód przy oddaniu). Kalibracja: czysta rolka daje 0, prawdziwe falstarty Jakuba 3 na 3, wklejone wpadki 3 na 3.
9. **Render i kontrola:** `hyperframes render`, potem `kontrola_eksportu.py` (głośność, właściwa ścieżka głosu, transkrypcja kawałkami bez powtórzeń). Dopiero wtedy kopiuj do Eksporty.
9a. **Pierwsze 5 s słowo po słowie** (`poczatek.py`), obowiązkowo na każdym gotowym pliku, HOOK A i HOOK B: `uv run --no-project --with numpy python3 -I skrypty/poczatek.py <plik.mp4> <napisy.srt> --projekt <folder wersji>`. 25.11.2026 HOOK A C4537_v2 wyszedł na wszystkie platformy i Jakub go zdjął: w pierwszych 3 s „coś się powtarza i wygląda źle”. Hook był sklejony z dwóch podejść tego samego zdania, cięcie w ciągłej mowie (ułamek „u” po „callu”, inny plan i pozycja głowy), a `powtorzenia.py` dał 0, bo powtórzony był ułamek głoski, nie słowo. Skrypt:
    - transkrybuje 0–5 s ze znacznikami słów (DTW) i porównuje z `.srt` (słowa spoza napisów, brakujące, powtórzone);
    - na każdym cięciu transkrybuje okna zaczynające się i kończące dokładnie na nim (tu whisper słyszy ułamki głosek, których w dłuższym oknie nie pokazuje);
    - w nagraniu sprawdza głos tuż przed `a_in` i po `a_out` oraz sklejkę podejść: czy tuż przed `a_in` pada to samo, co kończy poprzednią kwestię;
    - szuka zamrożeń, powrotu do tej samej klatki i napisu dwa razy pod rząd, zapisuje stykówkę klatek co 0,5 s i klipy z cięć w `analiza/poczatek/`.

    Hook bierz z jednego podejścia. Drugą połowę zdania z innego podejścia doklejaj tylko przy wyraźnej pauzie w nagraniu przed `a_in`; inaczej krótszy hook z jednego podejścia. Oddajesz przy 0 alarmach albo z każdym alarmem rozstrzygniętym uchem (i opisanym przy oddaniu). Stykówkę zawsze obejrzyj.
9b. **Każde cięcie w całym filmie** (`ciecia.py`, od 26.11.2026), obowiązkowo na każdym gotowym pliku, HOOK A i HOOK B: `uv run --no-project --with numpy python3 -I skrypty/ciecia.py <plik.mp4> <napisy.srt> --projekt <folder wersji>`. `poczatek.py` patrzy tylko na 0–5 s, a ten sam błąd (cięcie w trakcie głoski, ułamek głosu z sąsiedniego dubla, urwana końcówka) może wypaść na każdym styku. Dla każdego cięcia (t_in kwestii i≥1, plus wycięcia ze środka kwestii):
    - obwiednia nagrania (`audio/nowe_16k.wav`) ±0,5 s przy `a_in` i `a_out` poprzedniej: głos w 60 ms przed `a_in` / po `a_out` powyżej mowy−6 dB = ALARM, powyżej mowy−14 dB = uwaga; długość ciszy na styku;
    - whisper bez promptu w oknach zaczynających się (1,0 i 1,5 s) i kończących (1,2 i 1,6 s) dokładnie na cięciu: pierwsze/ostatnie słowo vs `audio/slowa.json` i `.srt`;
    - urwane słowo (słowo z `slowa.json` przecina cięcie), sklejka dwóch podejść (pomijana, gdy kwestia zaczyna się w nagraniu do 1,6 s po poprzedniej, czyli to ten sam dubel), to samo słowo dwa razy na styku.

    Wynik: lista `ALARM`/`uwaga`, `<out>/<plik>_ciecia.json` (obwiednie i transkrypcje każdego cięcia) i klipy ±1 s z oznaczonych cięć. Każdy alarm rozstrzygnij `fonemy.py` (samogłoska = głośno i mało przejść przez zero, „s/c/sz” = dużo przejść, zwarcie = dołek) i dłuższymi oknami whispera. Whisper w krótkim oknie wypełnia ucięte słowo całym („pracuję”, „zajebiste”), więc o urwanej końcówce rozstrzyga obwiednia, nie transkrypcja. Fałszywe uwagi: „AI” jako „Ej, ej”, „Mała” jako „No a”, pisownia whispera („w klucze” = „w Claude'zie”).
10. **Oddanie:** krótko, co zrobione i co warto sprawdzić. Uzupełnij `NOTATKI.md` i `napisy.srt`. Plik powyżej 30 MiB nie dojdzie na telefon. Lżejszą kopię zrób tylko na prośbę, a gdy pyta, gdzie jest plik, pokaż mu go w Finderze (`open -R`).
11. **Pętla nauki:** zapytaj o ocenę. Po publikacji poproś o zrzuty z Insights (wykres utrzymania widzów). Dopisz wpis do `references/dziennik.md` i ważne decyzje do pamięci.

## Nazwy własne: zdjęcie, logo, okładka

Jakub, 20.11.2026: „Zawsze jak wspominam o jakiejś firmie, nazwie własnej, imieniu i nazwisku, to staraj się wyszukiwać zdjęcie osoby, o której wspominam… i wrzucić je jako taką miniaturkę w film. Tak samo jak wspominam o Meta, znajdź logo Mety. Jak o Facebooku, logo Facebooka, jak o Instagramie, logo Instagrama. Jak o książce, wyszukaj okładkę.”

- **Po transkrypcji wypisz nazwy własne** z wybranych kwestii: osoby, firmy i produkty, książki. Każda dostaje grafikę, która wchodzi na słowie, w którym pada nazwa:
  - osoba: zdjęcie twarzy w kółku z obrysem w kolorze akcentu i podpisem imienia (pigułka jak `mention` w hooku albo mała karta nad napisami);
  - firma lub produkt: oficjalne logo, najlepiej SVG albo PNG z przezroczystym tłem, na małym ciemnym kafelku (logo w swoich kolorach, to obcy znak);
  - książka: okładka z lekkim cieniem i obrotem, ewentualnie z autorem.
- **Skąd brać:** logo z oficjalnej strony z materiałami prasowymi albo z Wikimedia Commons, zdjęcia osób z Wikimedia Commons albo oficjalnej strony, okładki od wydawcy albo z księgarni. Bierz najlepszą jakość, jaką znajdziesz, i obejrzyj plik, zanim go użyjesz: czy to ta osoba, czy aktualne logo, czy polskie wydanie książki, jeśli o takim mówi.
- **Pobieranie bez pytania** (zgoda z 20.11.2026, wyjątek od zasady 7): tylko obrazy pod konkretny film, nic do instalowania. Zapisuj je do wspólnego folderu `~/Desktop/Montażysta AI/Grafiki/` (`osoby/`, `logo/`, `ksiazki/`, nazwa pliku = nazwa własna), żeby kolejne filmy brały je z dysku, a do projektu kopiuj do `branding/`.
- **Rytm i strefa:** grafika trwa, dopóki o tym mówi (zwykle 1,5–3 s), stoi w strefie bezpiecznej i nie zasłania twarzy. Gdy w jednym zdaniu pada kilka nazw (np. Facebook i Instagram), daj je razem w jednym rzędzie, a nie po kolei w tym samym miejscu. Liczy się do limitu szablonów (najwyżej dwa razy ten sam układ pod rząd), więc zmieniaj formę: pigułka przy napisie, karta nad napisami, logo na planszy.
- **Wyjątki:** nigdy logo adGen w personal brandzie (zasada 3); marka, o której film jest (np. PerfOS), ma swój branding z projektu. Jeśli nie da się znaleźć pewnego zdjęcia albo logo, pomiń grafikę i powiedz o tym przy oddaniu, zamiast wstawiać coś podobnego.
- Przy oddaniu wypisz, które zdjęcia, logo i okładki weszły i skąd są.

## Jak dobierać grafiki

**Najpierw biblioteka.** Jakub po IMG_0576: przejścia i grafiki są „bardzo generyczne”, „bardzo często są używane te same rzeczy”. Przed projektowaniem grafik przeczytaj `references/biblioteka.md` i obejrzyj oba arkusze podglądów: jest tam ok. 50 gotowych szablonów (liczniki, wykresy, siatki kart, czaty AI, powiadomienia, adnotacje markerem, kinetyczna typografia) i sześć przejść plansz. Trzy twarde reguły: kolejne plansze nie wchodzą tym samym przejściem (pilnuje tego `panel()`), ten sam szablon grafiki pada najwyżej dwa razy w rolce i nigdy pod rząd, a przy oddaniu wypisujesz, których szablonów i przejść użyłeś, żeby w następnym filmie sięgnąć po inne.

Jedna grafika na jedną myśl, w momencie, gdy ją wypowiada. Słownik elementów (hook kinetyczny, plansza, powiadomienie, chip, kafelki, porównanie kosztów, odkrycie, pole komentarza, plansza końcowa) i ich parametry są w `references/styl.md`. Przeczytaj go przed edycją `kompozycja.py`. Przy nowym temacie wybierz z tego słownika to, co ilustruje sens zdania, a nie tylko jego słowa. Przykład: przy „CRM jest zawsze uporządkowany” pasuje chip z ptaszkiem, przy „30 razy więcej” paski kosztów i duże „30×”.

## Opis pod rolkę

Krótki, jako podsumowanie, nie transkrypcja 1:1. Pierwszą długą wersję odrzucił („chujowe, krótka jako podsumowanie”). **Zawsze 2 propozycje** różniące się kątem (np. liczba/kontrast vs teza/pytanie), w pliku `<Tytuł>_MM.RR - opisy.txt` obok filmów i w wiadomości. Struktura: 2–4 linijki, liczba lub kontrast w pierwszej linii, na końcu CTA „zaobserwuj” (słowo-klucz tylko w rolkach z automatyzacją). Jego głos (krótko, konkretnie, prowokacyjnie) opisuje skill `jakub-clone`, rejestr C.

## Porównania A/B

Gdy zmieniasz coś, co ocenia uchem lub okiem (głos, wariant hooka), zrób klip porównawczy w `ab/` (kompozycja HyperFrames z planszami „A / B” i podpisami). Warunki: ta sama głośność, synchronizacja sprawdzona co do próbki, plik poniżej 30 MiB (`--video-bitrate 4M`), żeby dotarł na telefon. Wzór: `projekty/IMG_0526/ab/index.html`.

## Long-form na YouTube (16:9)

Pierwszy taki odcinek: `projekty/IMG_0529` (13.11.2026, „Zautomatyzowany dział growth”). Jakub od razu poprawił: „FILM MA BYĆ POZIOMO NA YOUTUBE”. Long-form zawsze 16:9, rolki zostają pionowe. Szablony skryptów są w `projekty/IMG_0529/skrypty/` (opis w `NOTATKI.md` projektu). Od 17.11.2026 są w palecie personal brandu: grafiki i napisy odcinka biorą kolory z `paleta.py` (`PALETY`, `MARKA`, `kolory()`), a rolki promo z `rolka_szablon.py`. Uwaga na dwie rzeczy: gotowe warstwy w `projekty/IMG_0529/hf/` i wyeksportowany odcinek są nadal pomarańczowe (tak wyszedł 13.11.2026), a oryginalne skrypty sprzed zmiany leżą w `skrypty/_przed_paleta_2026-11-17/`. Do nowego odcinka kopiuj skrypty z głównego folderu, nie z tej kopii.

- **Głos i kwadraty w long-formie:** szablony z IMG_0529 nadal robią głos C (Sidon); kwadraty na planszach rysują już tylko przy `MARKA = "adgen"`. Uwaga o głosie z 17.11.2026 dotyczy też long-formu: przy następnym odcinku użyj naturalnego głosu z mikrofonu, a Sidon tylko na prośbę.
- **Montaż:** `kawalki.py` (mapa całego nagrania), potem `slowa_kawalki.py` (DTW dla każdego kawałka), potem `montaz.py` (`SEGS` i `CUTS`). Pauzy powyżej 0,6 s są skracane do 0,3 s, a długie ujęcia dzielone zmianą kadru w pauzach. Kadry z 4K: W/M/C = 1,0/1,2/1,4. Kontrola: `kontrola.py` na zmontowanym dźwięku.
- **Obraz:** `aroll.py` renderuje każde ujęcie osobno (HEVC VT, cache po parametrach). Grafiki i napisy są osobnymi warstwami HyperFrames (ProRes 4444 z alfą, `--resolution landscape-4k`): `render_warstwy.py`. Składanie w oknach po 60 s: `finalny.py`.
- **Napisy:** ten sam wygląd co w rolkach, ale w dolnym pasie (`top: 905px`, 58 px). Tekst poprawiany ręcznie w `tekst.py`, z którego powstaje też `napisy.srt` na YouTube. Chowane, gdy ten sam tekst pokazuje grafika.
- **Grafiki:** karty z boku kadru, szerokie tylko po lewej (twarz jest na ok. 56% szerokości, a w kadrze C prawa karta wchodzi na głowę). Plansze pełnoekranowe na liczby i schematy, rozdziały jako plansze „01/02…”, plansza końcowa 8 s pod ekran końcowy YouTube.
- **Zawsze 3 rolki promocyjne:** przy każdym long-formie (powyżej 10 min) w tym samym przebiegu robię 3 pionowe rolki po 10–15 s z najmocniejszych momentów, w stylu rolek, z CTA do pełnego odcinka. Eksport do `Eksporty/YouTube/<RRRR-MM-DD Tytuł>/Rolki promo/`: `<Tytuł>_ROLKA 1_MM.RR.mp4`… plus `<Tytuł>_ROLKI_MM.RR - opisy.txt`. To stała zasada Jakuba z 13.11.2026. Jak (wzór: IMG_0529, `scripts/rolki_promo.py`):
  - **Wybór:** trzy różne kąty: liczby i kontrast (efekt), kontrowersyjna teza (komentarze), coś praktycznego (koszt, jak zacząć). Każda rolka musi być zrozumiała bez odcinka i nie może przekręcać sensu (np. „plan za 30 $” tylko razem z „Tobie na start”).
  - **Cięcia:** fragmenty osi odcinka (`segs`), granice w minimach obwiedni głosu C, każdy fragment sprawdzony whisperem bez promptu (wypadają „Eee…” i ucięte słowa). Mowa ok. 10–12,5 s plus 2,5 s planszy końcowej.
  - **Obraz:** prosto ze źródła 4K przez `edl.json` (kadr 9:16, środek x osobno dla ujęcia, bo twarz chodzi). Start kawałka liczony od czasu jego pierwszej klatki, więc nie ma błędu zaokrąglenia.
  - **Grafika:** hook kinetyczny na 1–2 pierwsze zdania, potem napisy i jedna plansza albo chip na myśl. Plansza końcowa: przycisk play w kolorze akcentu (ciemny trójkąt), „Cały odcinek na YouTube”, tytuł odcinka. Gdy rolka kończy się planszą, plansza końcowa wchodzi na tę samą planszę (bez dwóch pełnoekranowych naraz). Plansza wchodzi na słowie z treścią, nigdy pusta.
  - **Kontrola:** `hyperframes check`, snapshoty, `kontrola_eksportu.py` i synchronizacja ust (dźwięk z telefonu w miejscu kawałka, mierzony z pełnego dekodu albo `-ss` > 0).
  - **Strefa bezpieczna:** rolki promo biorą szablon z `skrypty/rolka_szablon.py`, a kopia w `projekty/IMG_0529/skrypty/` jest sprzed 18.11.2026 (napisy 950 px, nakładki na 96 px). Przy nowym odcinku skopiuj aktualny `scripts/kompozycja.py` jako `rolka_szablon.py`, wtedy `rolki_promo.py` weźmie z niego `CAP_W`, `KIN_W` i pozycje ze strefy (zasada 9). Frazy napisów w rolkach promo też do ok. 20 znaków.
- **Muzyka (long-form):** Jakub chce cichego lo-fi na darmowej licencji. Źródło: Biblioteka audio YouTube (licencja bez atrybucji; pobieranie tylko za jego zgodą, z nazwą, źródłem i rozmiarem). `scripts/muzyka_podklad.py` (z IMG_0529):
  - **rozkład:** osobny utwór na część odcinka, przenikanie 3 s na planszach rozdziałów;
  - **poziom:** każdy utwór do −14 LUFS, EQ pod głos, podkład na −29 LUFS, ducking −5 dB od głosu C (pod mową −20 dB względem głosu);
  - **koniec:** +4 dB na planszy końcowej, potem wyciszenie;
  - **montaż do filmu:** miks do −14 LUFS i limiter, potem tylko podmiana dźwięku (`-c:v copy`), bez renderu obrazu.
- **Do opisu:** `rozdzialy.txt` (z czasów plansz) i `opis_youtube.txt`.

## Pliki skilla

- `references/styl.md`: wygląd i animacje, z parametrami. Czytaj przed kompozycją.
- `references/biblioteka.md` i `references/biblioteka_arkusz_1.jpg`, `_2.jpg`: biblioteka szablonów grafik i przejść z zasadami różnorodności. Czytaj przed wyborem grafik.
- `biblioteka/`: pliki szablonów z katalogu HyperFrames (montuje je `mount()` z `scripts/kompozycja.py`).
- `references/pipeline.md`: komendy krok po kroku i progi kontroli.
- `references/narzedzia.md`: pułapki narzędzi i gdzie co jest zainstalowane.
- `references/dziennik.md`: oceny Jakuba film po filmie. Czytaj na start, dopisuj na koniec.
- `scripts/sfx.py`: miks subtelnych efektów dźwiękowych pod głos (typy, warianty i poziomy są na górze pliku).
- `scripts/przebieg.sh`: łańcuch od A-rollu do sprawdzonej kompozycji dla jednej wersji (A albo `hookB/`).
- `scripts/przerwy.py`: pomiar ciszy na stykach i dziur ≥ 0,25 s w zmontowanym głosie (cel ok. 0,15 s).
- `scripts/oczy.sh`: podgląd pierwszych klatek (oczy na klatce 0) i podmiana klatek z mrugnięciem przed startem mowy.
- `scripts/cta.py`: CTA i plansze końcowe Liquid Glass, domyślnie w trybie „obserwuj”.
- `scripts/strefa.py`: kontrola strefy bezpiecznej na całym filmie i obrys strefy na klatkach; szablony od Jakuba leżą w `references/strefa_szablon_*.png`.
- `scripts/twarze.py` i `scripts/twarz.swift`: pomiar twarzy w ujęciach (Vision z macOS) pod automatyczny dobór kadru, gdy broda wypada nisko i napisy nie mieszczą się w strefie (`references/pipeline.md`, punkt 5).
- `scripts/`: szablony skryptów (z IMG_0526) plus `waliduj_napisy.py`, `kontrola_eksportu.py` `rolki_promo.py` (3 rolki promo z long-formu, IMG_0529) i `muzyka_podklad.py` (podkład lo-fi z duckingiem pod long-form).

Gdy w trakcie pracy odkryjesz coś, co poprawia proces (nowa pułapka, lepszy parametr, nowa grafika, którą pochwalił), dopisz to tutaj albo do odpowiedniej referencji. Tak ten skill robi się z każdym filmem lepszy.

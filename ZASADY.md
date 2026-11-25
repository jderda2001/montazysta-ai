# Montażysta AI: zasady zespołu (Jakub, Maciej)

Ten plik jest instrukcją dla Claude Code. Instalator podpina go jako `~/Montażysta AI/CLAUDE.md`, więc wczytuje się w każdej sesji uruchomionej w folderze `~/Montażysta AI`. Szczegóły procesu są w skillach `montaz-rolek` i `miniatury` (folder `skills/` w tym repo). Tu zebrane są zasady, które Jakub ustalał w rozmowach i które dotąd żyły tylko w jego pamięci Claude'a.

## Kto jest kim

- **Jakub Derda** jest autorem stylu i zwykle występuje w kadrze. Skille piszą o nim „Jakub”: jego oceny i zatwierdzenia obowiązują wszystkich, którzy montują.
- **Maciej** jest wspólnikiem Jakuba w adGen i montuje głównie **reklamy adGen** i **rolki PerfOS**.
- Operator to osoba, która uruchamia sesję. Pytania o decyzje kieruj do niej, a nie do „Jakuba” z tekstu skilla. W dzienniku zapisuj, kto dał ocenę (np. „Ocena Macieja: …”).
- Odpowiadaj po polsku.

## Wspólne repo: synchronizacja

Skille w `~/.claude/skills/montaz-rolek` i `~/.claude/skills/miniatury` to linki do tego repo, więc każda zmiana w skillu jest zmianą w repo.

1. **Przed montażem** pobierz zmiany z repo: `git -C "$HOME/Montażysta AI/montazysta-ai" pull --rebase --autostash`.
2. **Po montażu** zrób to, co każe skill: ocena do `references/dziennik.md`, nowe pułapki do referencji. Potem commit z krótkim opisem i `git push`. Nie zostawiaj zmian w skillu bez commita, bo druga osoba ich nie dostanie.
3. `dziennik.md` scala się automatycznie (`merge=union` w `.gitattributes`), więc dopisuj wpisy na końcu i nie przestawiaj starych.
4. Gdy operator podaje nową ogólną zasadę stylu, dopisz ją tutaj albo do właściwej referencji skilla, a nie tylko do prywatnej pamięci.
5. Do repo nie trafiają surowe nagrania, eksporty, rendery, klatki ani klucze API. Repo jest prywatne, a `.gitignore` odcina media.

## Marki

O palecie decyduje marka, a nie format filmu. Jeśli z nagrania nie wynika, czyja to rolka, zapytaj przed kompozycją.

**Reklamy adGen** (Meta Ads, leady dla kancelarii odszkodowawczych). W skillu `MARKA = "adgen"`.
- Ciemne plansze `#0f1012`, akcent pomarańczowy `#ff7018` z białym tekstem na akcencie, zielony „zrobione” `#3ddc84`, krój Inter Tight.
- Nagranie zwykle ma kilka hooków („hook A… hook B…”), więc każdy hook dostaje osobną wersję do testu A/B. Pliki nazywaj `<Tytuł>_HOOK A_MM.RR.mp4` i zapisuj w `Eksporty/Reklamy adGen/<RRRR-MM-DD Tytuł>/`.
- CTA „zostaw kontakt” i plansza końcowa. **Bez logo adGen** (zasada Jakuba z 13.11.2026), chyba że zlecający wprost o nie poprosi.
- Do każdej reklamy oddaj **2 propozycje tekstu** do reklamy, różniące się kątem: plik `<Tytuł>_MM.RR - teksty reklamy.txt` obok filmów i w wiadomości. Jeden zestaw na film, wspólny dla hooków.
- Montuj to, co padło w nagraniu. Liczby inne niż w scenariuszu zgłoś przed renderem.
- Wzór: `projekty/IMG_0583` („Leady z OC”, hooki A/B/C, wersję wybiera nazwa folderu). Podobny jest IMG_0585.

**PerfOS** (system AI Jakuba do reklam na Meta; perfos.pl).
- Ciemny motyw: tło `#0f0f0f`, karty `#131313`–`#161616`, obrys `#262626`, tekst `#f5f5f5`, tekst pomocniczy `#a1a1aa`, akcent `#00E5A0`, tekst na akcencie `#04261c`. Krój Geist. Logo PerfOS (litera P z przełącznikiem) może być na planszach.
- **Bez czarnego tła z kratką** (Jakub, 24.11.2026: „nie czaję tego czarnego motywu z taką kratką… to jest tylko w ostatnim etapie, gdy wybiera się plan… po prostu brzydkie”). Panel aplikacji ma tylko jasny motyw: tło `#ffffff`, powierzchnie `#fafafa`, tekst `#171717`, linie `#ededed`, akcent `#00e5a0`, tekst na akcencie `#04261c`. Ekrany aplikacji pokazuj w tym jasnym motywie, w jasnym oknie, na miętowym gradiencie z onboardingu (`#b9f5dd` → `#4fd9a8` → `#0f8f66` → `#063d2d`); ciemny `#0f0f0f` tylko na drobne elementy (pigułki, karty nad napisami).
- **Ekrany mają żyć jak przeglądanie** (Jakub, 24.11.2026): okno zostaje, a strona w środku się zmienia (wjazd z prawej, 0,7 s), do tego przewijanie, najazd kamery na ważny element, obramowanie w mięcie na słowie i kursor z kliknięciem. Przejścia nie krótsze niż ok. 0,6 s, ekran nie krócej niż ok. 1,5 s. Wzór: `projekty/PERFOS-film30/skrypty/kompozycja.py` (wersja 3).
- Pliki marki: `projekty/IMG_0597/branding/`. Większy zestaw jest w repo `PerfOS` w `public/brand/`.
- Wzór: `projekty/IMG_0597/skrypty/kompozycja.py` (`MARKA = "perfos"`, odtworzone karty panelu PerfOS, toczące się cyfry, przełączniki). Liczby bierz tylko z nagrania i ze zrzutów panelu.
- Eksport: `Eksporty/Rolki/<RRRR-MM-DD Tytuł>/`.

**Personal brand Jakuba** (rolki organiczne, long-form, rolki promo). W skillu `MARKA = "personal"`.
- Czerń `#0f1012`, biel i ciemne szarości. Jeden akcent na film, domyślnie `#00E5A0`, zawsze z ciemnym tekstem na akcencie. Kolor stawiaj tylko na sensie: kluczowe słowo, liczba, przycisk.
- Bez logo adGen i bez dekoracyjnych kwadratów na planszach.
- CTA to „zaobserwuj” (z powodem: następna rolka, seria), bez słów-kluczy i automatyzacji DM; plansza końcowa też z wezwaniem do obserwowania (`cta.py`, `tryb="obserwuj"`). „Napisz SŁOWO w komentarzu” tylko na wyraźną prośbę Jakuba (24.11.2026).

- **Logika i przejścia** (24.11.2026):
  - Kwestie układaj według sensu wypowiedzi i scenariusza. Ostatni dubel nie wchodzi, gdy przeczy reszcie albo ma błąd faktyczny: wtedy wcześniejszy dubel albo wycięte wtrącenie.
  - Dwie plansze pod rząd tylko przenikaniem: pierwsza zostaje pod drugą, bez mignięcia twarzy.
  - Licznik wchodzi razem z liczeniem, bez widocznych zer.

- **Restart słowa** („Jed… jeden”, poprawka w pół sekundy): `powtorzenia.py` ma przebieg mikro, który to łapie. Każdy alarm sprawdź uchem (25.11.2026).

## Styl (zatwierdzony, nie eksperymentuj)

- **Napisy są zamrożone:** słowo po słowie, frazy po 2–5 słów, wyróżnienia akcentem, Inter Tight, pozycja 1120 px i szerokość 620 px. Nie zmieniaj ich wyglądu.
- **Hook kinetyczny:** małe słowa i duże hasło (liczba albo puenta) w kolorze akcentu.
- **Plansze i nakładki** ilustrują to, co pada w nagraniu. Wykresy i schematy mają być mocno animowane: rysujące się osie, jadąca kropka, wstrząs. Statyczny rysunek odpada.
- **Mniej, ale płynniej (od 24.11.2026, zasada 10 skilla):**
  - najwyżej 2 złożone animacje na każde 30 s filmu: jedna bogata scena zamiast kilku małych kart;
  - płynne zoomy (`zoom()`, 1,5–3 s, `sine.inOut`) zamiast przeskoków kadru;
  - ruch bez sprężyn i podskoków, wejścia 0,5–0,8 s;
  - przejście plansz domyślnie miękkie przenikanie, efektowne najwyżej raz w rolce;
  - czysto, dużo powietrza;
  - wstawki jasne, „premium”: złamana biel, ciemny tekst, białe karty, wejście kurtyną, ciemne napisy na jasnym tle;
  - render i A-roll w 60 kl./s.
- **Różnorodność:** jeden szablon pojawia się najwyżej dwa razy w rolce i nigdy dwa razy pod rząd. Przed wyborem grafik przeczytaj `references/biblioteka.md` i obejrzyj arkusze podglądów.
- **Kadry:** W/M/C (zoom 1,0/1,15/1,30). Twardy przeskok kadru tylko przy cięciu dubli, a akcenty robi płynny zoom. W każdym ujęciu jest delikatny najazd. Przy niskim kadrze najpierw zmierz twarz (`twarze.py`), dopiero potem ustawiaj napisy.
- **Strefa bezpieczna rolek:** y 270–1245, x 70–1010. Od 860 px w dół prawa krawędź jest na 885 px, od 1145 px na 850 px. Przed każdym renderem uruchom `strefa.py` i dopiero przy zerze naruszeń renderuj.
- **Napięcie przed puentą:** zdanie zapowiadające wynik („No i wynik”) dostaje najazd na twarz i ok. 1 s pauzy. Styki kwestii mają być płynne, bez pustej ciszy (24.11.2026): marginesy liczone od faktycznego głosu, ok. 0,15 s ciszy na styku (po zdaniu 0,10 s, w środku 0,05 s, start głosu od −40 dB) (`poczatek_mowy()` / `koniec_mowy()` w `aroll.py`). Końcówek słów nie ścinaj.

## Pierwsze 2 sekundy (od 24.11.2026, zasada 11 skilla)

Statystyki 6 rolek: 63–75% widzów odpada w 2–3 s, a kto zostanie, ogląda do końca. Dlatego:
- pełny hook na ekranie od klatki 0 (`hook0()`), z ruchem i jasnym startem;
- puenta w pierwszych 1,5 s;
- hasło pod widza, nie o sobie;
- zawsze 2 wersje hooka (A i B) do testu przez „Próbne rolki”;
- statystyki każdej rolki trafiają do dziennika.

## Dźwięk

- Głos naturalny z mikrofonu, lekki mastering, −14 LUFS. Sidon albo „studio” tylko na prośbę albo przy wyraźnie złym nagraniu, i wtedy powiedz o tym przy oddaniu.
- Efekty dźwiękowe tylko z biblioteki `zasoby/Muzyka/SFX` przez `sfx.py`, subtelnie, na poziomach zatwierdzonych w skrypcie. Nigdy nie generuj whooshy z szumu.
- Rolki są bez muzyki, chyba że ktoś poprosi. W long-formie cichy lo-fi z `zasoby/Muzyka`, ok. 20 dB pod głosem, z duckingiem (`muzyka_podklad.py`).
- Czasy słów do napisów licz osobno dla każdej kwestii, whisperem z DTW i flagą `-nfa`. Bez `-nfa` DTW po cichu się wyłącza.

## Przekleństwa: zawsze cenzura

Jakub, 23.11.2026: „zacenzuruj i przykryj mi wtedy usta… żeby nie zdejmowali monetyzacji”, a zapytany, czy tak ma być zawsze, odpowiedział: „Tak, zawsze”. Każde przekleństwo cenzuruj bez pytania, w trzech miejscach:
- **Dźwięk:** piknięcie 1 kHz na czas słowa w miejsce głosu.
- **Napis:** „#@!%&” w miejscu słowa.
- **Obraz:** czarny pasek z „#@!%&” na ustach.

Wzór: projekt IMG_0720. Na koniec sprawdź whisperem na gotowym pliku, że przekleństwa nie słychać.

## Falstarty i powtórki

Whisper wygładza zająknięcia, powtórzone zdania i falstarty. Przed oddaniem każdego filmu:
- uruchom `kawalki.py` dwa razy: zwykle i z `--drobne`;
- każdy alarm (`POWTORKA?`, `?`) rozstrzygnij whisperem bez promptu na samym kawałku i obwiednią z `fonemy.py`;
- zająknięcie w środku kwestii wytnij polem `wytnij` w `SEGS`, a sklejkę sprawdź whisperem w trzech kontekstach;
- po renderze przeczytaj kontrolę eksportu zdanie po zdaniu.
- po `aroll.py` uruchom `powtorzenia.py` (cała rolka: frazy, falstarty, akustyka) i rozstrzygnij każde miejsce z klipu w `analiza/powtorzenia/`.
- **Pierwsze 5 s słowo po słowie (od 25.11.2026, po zdjęciu HOOK A C4537_v2 ze wszystkich platform):** hook bierz z jednego podejścia; drugą połowę zdania z innego podejścia doklejaj tylko przy wyraźnej pauzie w nagraniu przed `a_in`. Na każdym gotowym pliku (HOOK A i HOOK B) uruchom `poczatek.py` (transkrypcja 0–5 s ze znacznikami słów vs `.srt`, okna od i do każdego cięcia, głos przed `a_in`, sklejka podejść, klatki co 0,5 s, podwójny napis) i obejrzyj stykówkę. Oddajesz przy 0 alarmach albo z każdym rozstrzygniętym uchem. Szczegóły: `kontekst/pamiec/feedback-pierwsze-5-sekund-sklejka.md`.

## Formaty i komplet przy oddaniu

- **Rolka:** 1080×1920, 60 kl./s, zawsze dwie wersje: `<Tytuł>_HOOK A_MM.RR.mp4` i `_HOOK B_` (do testu przez „Próbne rolki” na IG), do każdej `.srt` (reklama: jedna wersja na hook). Do każdej rolki **2 propozycje opisu** różniące się kątem, w pliku `<Tytuł>_MM.RR - opisy.txt` obok filmu i w wiadomości.
- **Long-form na YouTube** zawsze poziomo, 16:9, 4K. Przy każdym wideo dłuższym niż 10 min, bez pytania:
  - **3 rolki promo** po 10–15 s;
  - **3 miniatury A/B/C** skillem `miniatury`, z 2 tytułami do każdej.
- **Eksporty** (`~/Desktop/Montażysta AI/Eksporty/`) układaj w folderach:
  - `YouTube/<RRRR-MM-DD Tytuł>/` (w środku `Rolki promo/`, `Miniatury/`);
  - `Rolki/<RRRR-MM-DD Tytuł>/`;
  - `Reklamy adGen/<RRRR-MM-DD Tytuł>/`.

  Nic nie zostaje luzem w katalogu głównym. Surowe nagrania leżą tylko w `Nagrania ` (ze spacją na końcu nazwy).

## Wzorcowe projekty

Skille odsyłają do projektów typu `projekty/IMG_0526/`. Ich skrypty, notatki, branding i szkielet HyperFrames są w repo w `wzory/`, a instalator kopiuje je do `~/Montażysta AI/projekty/`, więc ścieżki ze skilla działają. Nie ma tam nagrań ani renderów.

| Projekt | Co to jest |
|---|---|
| IMG_0526 | Wzór układu i ruchu (rolka „Kaja zamiast settera”); szkielet `hf/` do kopiowania przy nowym projekcie. |
| IMG_0576 | Wzór personal brandu w palecie `#00E5A0`. |
| IMG_0583, IMG_0585 | Reklamy adGen z hookami A/B/C. |
| IMG_0597 | Pierwsza rolka PerfOS. |
| IMG_0529 | Long-form na YouTube z rolkami promo i miniaturami. |
| IMG_0591, IMG_0640, IMG_0688 | Najnowsze rolki: strefa bezpieczna, cięcia w środku kwestii, scrim pod napisami. |
| **C4538** | **Najnowszy wzór rolki (25.11.2026), od niego zaczynaj.** Kamera Sony, styl premium, hasło od klatki 0, hook A/B (`hookB/` + plik `HOOK_B`), CTA „zaobserwuj”, styki ok. 0,15 s, dwie sceny pod rząd z przenikaniem. |
| C4527–C4529 | Scenariusze 1–3 dla freelancerów (20 ofert, faktury i windykacja, AI nie zabierze klientów); C4527 ma scrim pod napisami na białej koszulce i akcent hasła jako zakreślenie na zielonej ścianie. |
| C4534–C4537 | Scenariusze „AI i biznes”: IPO Anthropic (wykres kursu), OpenWorks (licznik, przenikanie scen), Klarna (wycięte wtrącenie „rok temu” ze środka zdania przez `a_in`/`a_out`), oferta po callu (oczy na klatce 0). |
| IMG_0361 | Stara wersja, sprzed zakazu logo i zasad o falstartach. Tylko poglądowo. |

## Kontekst i scenariusze

- `kontekst/README.md`: kim jest Jakub, foldery, od czego zacząć; `kontekst/pamiec/`: wszystkie notatki poprzedniego montażysty (cytaty, daty, decyzje). Przy sprzeczności wygrywa nowsza data, a ponad notatkami ten plik i `SKILL.md`.
- Scenariusze rolek pisze skill `scenariusze-rolek` (proces, format, przykłady z 24.11.2026).

## Praca techniczna

- **Agenci:** model i effort dobieraj do zadania. Wyszukiwanie, streszczanie i mechaniczne przeróbki idą na Sonnet albo Haiku. Ocena falstartów, decyzje montażowe i trudny debug zostają na najmocniejszym modelu albo robisz je sam.
- **Dysk i HyperFrames:** render na całe konto idzie jeden naraz (wspólna blokada). Klatki A-rollu lądują w `$TMPDIR/hyperframes-extract-cache-*` i potrafią zająć dziesiątki GB.
  - Przed renderem sprawdź `df -h`.
  - Przy małym dysku renderuj z `--video-frame-format jpg`.
  - Po udanym renderze usuń tylko własny wpis cache.
  - Nigdy nie rób `pkill` po nazwie procesu; zatrzymuj własny proces po PID.
- **Klucz kie.ai** (generowanie elementów w miniaturach) trzymaj w `~/.config/kie/api_key` z prawami 600 albo w zmiennej `KIE_API_KEY`, nigdy w repo. Zdjęć osób nie wysyłaj do kie.ai bez pytania.
- Bez pytania nie pobieraj nowych plików (muzyki, SFX, szablonów) i nie usuwaj cudzych danych.

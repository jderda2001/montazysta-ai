# Narzędzia i pułapki

## Gdzie co jest
- **Instalacja bez Homebrew:** wszystko w `~/.local` (w PATH). Nie proponuj `brew install` ani globalnego `npm i -g`.
- **FFmpeg n9.0.2** z libx264, bez libass, freetype i drawtext. Tekst na wideo rób zawsze w HyperFrames, nie filtrem ffmpeg.
- **whisper.cpp v1.9.5:** `whisper-cli`, model `~/.local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin` (Metal działa).
- **HyperFrames 0.9.20:** wrapper `~/.local/bin/hyperframes` na node 22 (`npx hyperframes` na domyślnym node 20 nie zadziała).
- **Python:** systemowy 3.9 bez numpy, więc `uv run --no-project --with numpy python3 -I`. Dla PyTorch: `--python 3.12` (zainstalowany przez uv).
- **Sidon:** wagi `sarulab-speech/sidon-v0.1` (wersje CPU, ok. 1 GB) w `~/.cache/huggingface`. 47 s głosu przetwarza w ok. 12 s na CPU.

## whisper
- **DTW działa tylko z `-nfa`.** Flash attention jest domyślnie włączone i po cichu wyłącza DTW (`t_dtw = -1`). Zostają wtedy czasy heurystyczne, nawet 0,6 s za wcześnie.
- **`t_dtw` tokenu to jego koniec.** Sprawdzone sondami: whisper na `[początek, t]` pokazuje słowo dopiero, gdy t minie tę wartość.
- **Interpunkcja ma `t_dtw` w pauzie po słowie.** Nie licz jej do końca słowa, ale użyj jako startu następnego.
- **Whisper wygładza falstarty i powtórzenia**, a `--prompt` z oczekiwanym tekstem jeszcze to wzmacnia. Do wykrywania używaj kawałków między pauzami bez promptu.
- **Powtórzone zdanie przechodzi przez DTW bez żadnego sygnału.** W IMG_0591 kwestia „gdzie autor pyta: sukces to szczęście czy umiejętności?” padła dwa razy pod rząd, a `slowa.py` (prompt + DTW) oddał jedno czyste zdanie, rozciągając słowo „szczęście” na 1,5 s. `kawalki.py` pokazywał oba podejścia, ale przy czytaniu 20 kwestii na oko to umknęło. Stąd alarm `POWTORKA?` (sylaby) i `?` w `kawalki.py` oraz tryb `--drobne`. Drugi sygnał to słowo w `slowa.json` trwające ponad sekundę.
- **Zająknięcie w środku słowa zwykły podział przepuszcza.** „sukce- cesu” (przerwa 0,1 s) i „do… kładnie” (pauza 0,15 s w środku słowa) mieszczą się w jednym kawałku przy pauzach od 0,15 s, a whisper na całym kawałku pisze poprawne słowo. Wychodzą dopiero w `kawalki.py --drobne`, często jako dziwne słowo („Czasu.”, „dokuje.”). Dziwne słowo w drobnym kawałku to nie przesłyszenie, dopóki `fonemy.py` nie pokaże, że sylab jest tyle, ile trzeba.
- **Margines `PRE`/`POST` przy cięciu w środku słowa zabiera to, co miało wypaść.** Dlatego zająknięć nie wycinaj dzieleniem kwestii na dwie, tylko polem `wytnij` (cięcie co do klatki, zanik 6 ms). Dzielenie przesuwa też numery kwestii, na których stoją grafiki.
- **Test sklejki na jednym wycinku kłamie.** Whisper uzupełnia brakującą sylabę z kontekstu, więc „czyste zdanie” na całej kwestii niczego nie dowodzi. W IMG_0591 dwie z trzech poprawek po pierwszym renderze były złe („wiedziałem kładnie”, „Napoleon” bez „Hill”) i wyszły dopiero w `kontrola_eksportu.py`, którą trzeba czytać zdanie po zdaniu także po poprawkach. Sprawdzaj w trzech kontekstach i licz sylaby w `fonemy.py`.
- **Typowe pisownie whispera:** „Seter/Syter” (Setter), „z czym, że” (mówi tak naprawdę, w napisach dajemy „z tym, że”), „pilnuję/piszę” zamiast 3. osoby, „200” zamiast „dwie stówki”.
- **Na ciszy halucynuje „Dziękuję.”**. To nie jest błąd montażu.
- **Dodatkowe słowo na końcu kawałka w `kawalki.py` traktuj jako prawdziwe, dopóki nie udowodnisz, że nie jest.** W IMG_0591 pokazał „to jedna połowa. Drugą”, „gdzie jestem. Także” i „w 61, a…”, a ja uznałem to za halucynacje, bo obwiednia na samym końcu kwestii była cicha. Wszystkie trzy były urwanymi słowami i wróciły w transkrypcji gotowego pliku. Sprawdzian: wytnij samą końcówkę (0,6–0,8 s) i przepisz ją osobno bez promptu. Jeśli whisper słyszy w niej słowo, skróć kwestię do ciszy przed nim.
- **Halucynacja tuż po ostatnim słowie kwestii** („Dziękuję.” w osobnym kawałku 0,1–0,2 s) może być szmerem w marginesie `POST`, ale równie dobrze cichą końcówką ostatniego słowa. Zanim skrócisz kwestię, obejrzyj obwiednię (`obwiednia.py OD DO --wykres`): koniec mowy jest tam, gdzie poziom spada poniżej ok. −60 dB. W IMG_0576 „Dziękuję.” po hooku B było ściszoną końcówką słowa „tysięcy”, a nie szmerem. `slowa.py` zapisał je przy tym jako „tysi.” (niezależnie od cięcia), co wywróciło kompozycję: takie słowo popraw w `FIX`, nie cięciem.
- **Głos naturalny i szczyt po AAC:** `aroll.wav` ma szczyt −1,5 dBFS, ale po kodowaniu AAC w renderze wychodzi −1,3. W `kompozycja.py` głos przechodzi więc przez `alimiter=limit=0.81` (−1,8 dBFS), co nie zmienia głośności.
- **`waliduj_napisy.py` i liczebniki:** na krótkich wycinkach whisper pisze „10 tysięcy” raz jako „10 000”, raz jako „dziesięć tysięcy”, a „AI” jako „AA”. Walidator gubi wtedy dopasowanie i flaguje resztę zdania. Zanim uznasz to za błąd czasów, przeczytaj linie szczegółów: jeśli słowo jest w tym, co „słychać”, czas jest dobry (IMG_0576: 48 flag, zero realnych).
- **Transkrypcja gotowego pliku łapie więcej niż surowego.** Na głosie po Sidonie whisper usłyszał falstart „t-” i poprawną wersję zdania („uwierz, wiem, co mówię”), których nie pokazał na dźwięku z telefonu. Czytaj wynik `kontrola_eksportu.py` zdanie po zdaniu, zanim zrobisz drugi wariant hooka.

## ffmpeg / dźwięk
- **Zakres kolorów źródła:** iPhone 1080p (`yuvj420p`) nagrywa w zakresie pc, iPhone 4K HEVC w tv. `aroll.py` bierze zakres z ffprobe (`src_range()`, od 17.11.2026). Wcześniej miał `in_range=pc` na sztywno, co na nagraniach 4K spłaszczało kontrast (czerń 49 → 58, biel 192 → 181 w skali 0–255). Projekty skopiowane z szablonu przed tą datą (IMG_0576) mają jeszcze starą linię. Kontrola: `signalstats` na klatce źródła i A-rollu bez gradingu, `YLOW` i `YHIGH` mają się zgadzać.
- **loudnorm zawsze dwuprzebiegowo** (`linear=true`) do −14 LUFS, TP −1,5, LRA 9.
- **`adynamicequalizer` (de-esser):**
  - Próg jest liniowy (0–100, w dB: `20·log10`). Detektor uśrednia |pasmo|, więc kalibruj na średniej z |x| w ramkach 10 ms, nie na szczytach (te są ok. 10 dB wyżej).
  - Wygładzanie wzmocnienia ma stałą 4× dłuższą niż detekcja.
  - W trybie `cutabove` wchodzenie cięcia idzie gałęzią `release`, a wychodzenie gałęzią `attack`. Dlatego de-esser ma `attack=4:release=2`. Z typowym `release=60` cięcie nie zdąży na sybilant.
- **Detekcja de-essera wąska** (6,5 kHz, Q 1,5), bo szeroka łapie samogłoski z mocnym pasmem 3 kHz.
- **Gęsta kompresja wyciąga spółgłoski**, więc przy mocnym kompresorze de-esser stawiaj za nim.
- **Uczciwe A/B:** zawsze przy tej samej głośności (głośniejsze brzmi „lepiej”).

## HyperFrames
- **Element czasowy:** `data-start`, `data-duration`, `class="clip"`. Jeden zatrzymany timeline w `window.__timelines["main"]`.
- **Głos jako osobna ścieżka:** `<video … muted>` + `<audio src="glos.wav" data-start="0" data-duration="…">`.
- **Kolejne `<video>` z tym samym plikiem** odtwarzają od 0 w swoim `data-start` (sprawdzone).
- **Snapshot:** `hyperframes snapshot --at 3.0,10.5 --no-end -o KATALOG`, który robi też `contact-sheet.jpg`.
- **Render:** `--quality delivery --video-frame-format png` (finał) albo `--video-bitrate 4M` (podglądy poniżej 30 MiB). Dźwięk wychodzi w AAC ok. 192 kb/s.
- **Ozdobne elementy wychodzące poza kadr** dostają `data-layout-allow-overflow`, inaczej check zgłasza overflow.
- **Nie animuj właściwości układu** (`width`, `maxWidth`, `margin`, `padding`): `hyperframes check` zgłasza to jako błąd StaticGuard, bo takie wartości skaczą po całych pikselach i zacinają się w renderze klatka po klatce. Element, który ma „dojść” do pigułki, trzymaj w `display:none`, włącz przez `tl.set(…, {display:"flex"})` i animuj tylko `x`, `y`, `scale`, `opacity` (IMG_0576, druga część chipa).
- **Rysowanie linii w SVG:** `pathLength="1000"` na ścieżce, w CSS `stroke-dasharray: 1000`, a w GSAP `fromTo({strokeDashoffset:1000},{strokeDashoffset:0})`. Nie używaj skali 0–1: render zaokrągla wartość do całości i linia wskakuje cała w połowie ruchu, czego nie widać na pojedynczej klatce końcowej. Skalowanie elementów SVG wymaga `svgOrigin:"x y"` (IMG_0576, wykres).
- **Kropka jadąca po krzywej:** policz punkty krzywej w Pythonie i daj serię krótkich `tl.to(…, {attr:{cx,cy}, ease:"none"})`. Ułamek długości musi iść tym samym tempem co rysowanie linii. W GSAP `power1` to kwadrat, `power2` sześcian, `power3` czwarta potęga.
- **Element ukryty do swojego momentu:** `fromTo` ze stanem początkowym widocznym (np. fala z `opacity:0.75`) rysuje ten stan od załadowania strony. Daj `immediateRender:false` i ukryj element przez `gsap.set`.
- **Animację oglądaj na gęstych klatkach:** snapshot co 0,2–0,3 s w trakcie ruchu, wycięty i powiększony (`ffmpeg crop` + `tile`). Pojedyncza klatka po zakończeniu ruchu nie pokaże, że linia wskoczyła zamiast się narysować.
- **Pusta plansza albo karta:** jeśli treść karty wchodzi na późniejszym słowie, przesuń wejście całej planszy na to słowo. W IMG_0576 karta „Kiedyś” stała pusta 2 s, dopóki plansza wchodziła na początku kwestii.

## Powłoka i system
- **Miejsce na dysku przed renderem:** `hyperframes render` wypakowuje klatki wideo na dysk i przy braku miejsca pada z `ENOSPC` (IMG_0591, przy ok. 3,8 GB wolnego i równoległych montażach). Sprawdź `df -h` przed serią renderów. Każdy render zostawia w katalogu tymczasowym (`$TMPDIR/hyperframes-extract-cache-501/hfcache-v8-*`) ok. 6 GB wypakowanych klatek PNG na 95 s rolki i sam ich nie sprząta: po czterech renderach było tam 31 GB i piąty padł. Po serii renderów usuń te foldery (tylko własne, po dacie, i tylko gdy żaden render nie działa). A-roll z ciemnego 4K potrafi mieć 430 MB na 95 s.
- **Potok gubi kod wyjścia:** `python3 kompozycja.py | head -1` w skrypcie z `set -e` nie zatrzyma się na błędzie Pythona, bo liczy się kod `head`. W IMG_0576 render poszedł przez to ze starą kompozycją. Wynik kroku zapisuj do pliku (`> log 2>&1 || exit 1`), a skracaj go osobną komendą.
- **Kilka sesji na jednym Macu:** nie zabijaj procesów po nazwie (`pkill -f hyperframes`), bo trafisz też w rendery innych sesji. Sprawdź katalog roboczy procesu (`lsof -a -p PID -d cwd`) i zabijaj tylko swoje.
- **zsh nie dzieli zmiennych na słowa:** `set -- ${=r}` zamiast `set -- $r`, a `${G1}` zamiast `$G1[b1]`.
- **awk na macOS nie ma `strtonum`.** Pomiary pikseli rób w Pythonie.
- **`python3 -I` nie dodaje katalogu skryptu do `sys.path`.** Moduły z `skrypty/` ładuj przez `importlib.util.spec_from_file_location`.
- **Pokazanie pliku w Finderze** spoza folderów sesji: `open -R "ścieżka"`.
- **`SendUserFile`:** pliki powyżej 30 MiB widać tylko w aplikacji na Macu, nie na telefonie. Powiedz o tym przy wysyłce.
- **Folder `Nagrania `** ma spację na końcu nazwy.

## Warstwy HyperFrames i składanie (long-form)
- **Overlay po `-ss`:** pierwsza klatka warstwy ma znacznik minimalnie późniejszy niż podkład, więc overlay wypuszcza pierwszą klatkę bez grafiki. Zawsze daj `setpts=PTS-STARTPTS(+offset/TB)` na obu wejściach.
- **Kolizje nazw klas CSS:** klasa `.on` (węzeł schematu, `position:absolute`) rozwaliła aktywną zakładkę profilu (`pf-tab on`). Klasy stanów nazywaj jednoznacznie (`act`, `sel`).
- **`hyperframes check` z wieloma plikami `o_*.html` w katalogu** zgłasza „Multiple root-level HTML files”. Przy warstwach to normalne (render przez `-c plik.html`). Liczą się runtime, layout i contrast.
- **Rozmiary ProRes 4444 4K:** plansza pełnoekranowa ok. 80–95 MB/s, karta z boku ok. 25 MB/s, napisy ok. 7 MB/s. Render: grafika 2,5–6 s na sekundę, napisy ok. 1,8 s na sekundę.
- **Wspólny CSS w każdej warstwie:** każda kompozycja ma pełny blok stylów, więc zmiana dowolnej reguły (nawet czcionki jednej karty) zmienia hash wszystkich warstw i wymusza pełny re-render (ok. 20 min w 4K). Poprawki CSS zbieraj w jedną turę albo hashuj tylko reguły użyte w danej warstwie.
- **Składanie w oknach: wycinaj ujęcia po numerach klatek** (`trim=start_frame=…:end_frame=…`), nie `-ss` + `trim=duration`. Przy tamtej metodzie 2 z 16 okien miały 1799 zamiast 1800 klatek, przez co obraz uciekał dźwiękowi o 33–66 ms. Po złożeniu policz klatki każdego okna (`ffprobe -count_packets`).
- **Dyktafon** potrafi zapętlić bufor 0,5 s na końcu urwanego nagrania. Sprawdzaj autokorelacją (`x[t]` wobec `x[t+0,5 s]`).

## Rolki promo z long-formu (IMG_0529)
- **`ffmpeg -ss 0` na MP4 z AAC przesuwa dźwięk o −21 ms** (podwójnie zdjęty priming). Synchronizację mierz z pełnego dekodu albo z `-ss` > 0, inaczej pierwszy kawałek każdej rolki wygląda na przesunięty o klatkę.
- **Plansza końcowa wjeżdżająca na pełnoekranową planszę** daje w `hyperframes check` błąd `text_occluded`. Rozwiązanie: treść planszy końcowej na tej samej planszy (stara treść znika, nowa wchodzi).
- **HyperFrames zaokrągla długość w górę:** `data-duration="12.267"` dało 369 klatek zamiast 368. Nieszkodliwe (ostatnia klatka to plansza), ale licz długość jako wielokrotność 1/30 s.
- **zsh:** `echo =====` kończy się błędem „not found” (rozwijanie `=`). Separatory pisz jako `-----`.

## A-roll z iPhone'a 4K 60 kl./s i kontrola (IMG_0583)
- **Mux A-rollu z `-shortest` gubi do 3 ostatnich klatek** (klatki B na końcu strumienia): 1423 zamiast 1426. To sam ogon pod planszą końcową, nie rozjazd z dźwiękiem. Zanim uznasz to za dryf, porównaj momenty cięć z EDL: `ffmpeg -i aroll.mp4 -vf "select='gt(scene,0.12)',showinfo" -f null -` (w IMG_0583 zgadzały się co do klatki). Poprawiony `aroll.py` muxuje bez `-shortest` i tnie ujęcia przez `trim=end_frame=n`.
- **Długi kawałek w `kontrola_eksportu.py`:** gdy przerwy między kwestiami nie schodzą poniżej −45 dB, kilkanaście kwestii zlewa się w jeden kawałek 30 s i whisper gubi w nim całe zdania („…czas zespołu. gwarancją.”). To nie jest dziura w dźwięku. Odsłuchaj wtedy plik kwestia po kwestii według EDL: `projekty/IMG_0583/skrypty/odsluch_kwestii.py FILM.mp4`.
- **Kadry przed renderem:** `projekty/IMG_0583/skrypty/podglad_kadrow.py WYNIK.jpg` wyciąga po jednej klatce z każdego ujęcia po kadrowaniu (kilka sekund zamiast 3 min renderu). Twarz przesuwa się między dublami, więc środek twarzy podawaj per kwestia.
- **Kontrola F0 po Sidonie:** `studio.py` potrafi pokazać r ≈ 0,82 i mediany różne o 9 Hz, choć ton się nie zmienił. To skoki prostego trackera i dodatkowe ramki dźwięczne po odszumieniu. Policz stosunek F0 na wspólnych ramkach (mediana 1,000, 90% ramek w ±5%) zamiast samej korelacji.
- **Naturalny głos i szczyt po AAC:** bez Sidona i gęstej kompresji głos ma wyższe szczyty. `loudnorm` zostawia szczyt na −1,5, a kodowanie AAC podbija go o ok. 0,1 dB (kontrola: −1,4 dBFS). W `projekty/IMG_0583/skrypty/aroll.py` po `loudnorm` stoi `alimiter=limit=0.794` i `volume=0.15dB`: wychodzi −14,0 LUFS i szczyt −1,8. Samą ścieżkę w gotowym pliku można podmienić bez renderu obrazu (`-c:v copy`).

## Rolka PerfOS, IMG_0597 (18.11.2026)
- **`hyperframes render` puszczony przez `( … ) &` kończy się po kilku sekundach** z „render_cancelled_parent_exited”: HyperFrames przerywa render, gdy zniknie proces nadrzędny. Długi render uruchamiaj jako zadanie w tle narzędzia (run_in_background), nie przez `&` w powłoce. `ffmpeg` i `python3` w tle przez `&` działają normalnie.
- **Zatrzymany `aroll.py` zostawia osieroconego `ffmpeg`** (i plik `v.mp4` w `$TMPDIR/tmp…`). Po `kill` skryptu zabij też jego `ffmpeg` po PID i usuń katalog tymczasowy.
- **„No space left on device” w połowie A-rollu:** inna sesja renderowała w tym samym czasie (pamięć klatek HyperFrames 6 GB plus jej pliki), a `df` chwilę wcześniej pokazywał 19 GB. Przy pracy kilku sesji sprawdzaj dysk tuż przed każdym długim krokiem i po błędzie po prostu ponów.
- **`wyspy.py` nie ma `-nfa`, więc czasy słów w `wyspy.json` są heurystyczne (do 0,5 s za wcześnie).** Wystarczają do wyboru dubli, ale nie do cięcia w środku zdania. W IMG_0597 cięcie „…do dziś | PerfOS zrobił” ustawione według nich zostawiło ogon „listopada”. Granicę cięcia w ciągłej mowie ustalaj sondami whispera na krótkich wycinkach (0,4–1 s) i obwiednią, a po `slowa.py` przeczytaj pierwsze i ostatnie słowa każdej kwestii: obce słowo na początku albo ucięta końcówka („4220 zł” zamiast „złotych”) to źle postawione cięcie.
- **Połknięte słowo w hooku:** w ostatnim dublu „Dałem AI” trwało 0,14 s i whisper bez podpowiedzi słyszał „Dałem jej” (z podpowiedzią „AI”). Prompt z oczekiwanym tekstem maskuje takie rzeczy. Pierwsze słowa hooka sprawdzaj bez promptu; gdy są niewyraźne, weź początek z wcześniejszego dubla i sklej w pauzie albo zwarciu, ze zmianą kadru na cięciu.
- **Liczniki w grafikach rób transformem, nie w JS.** Kolumna cyfr 0–9 przesuwana przez `yPercent` (`wheel` / `roll` w `projekty/IMG_0597/skrypty/kompozycja.py`) daje ten sam obraz przy renderze i przy skoku na dowolny czas. Liczbę ukryj do momentu, w którym pada, inaczej na karcie stoi „000”.
- **Walidator napisów na długiej kwestii (powyżej ok. 10 s) sypie fałszywymi flagami**, bo whisper inaczej zapisuje długi wycinek. Porównaj wtedy czasy kilku słów z granicami kawałków z obwiedni (sondy): zgodność do 0,05 s znaczy, że czasy są dobre.


- **PDF na obrazy bez instalowania czegokolwiek** (IMG_0718): `scripts/pdf_strony.swift` (PDFKit z macOS). `swiftc -O -o analiza/pdf_strony scripts/pdf_strony.swift`, potem `analiza/pdf_strony PLIK.pdf KATALOG 1100` daje `strona_01.png`… Narzędzie Read nie pokaże PDF-a, bo nie ma `pdftoppm`.
- **Szablony biblioteki w polu strefy (`mount(..., pole=…)`) mają po zmniejszeniu drobny tekst:** `constellation-hub` 16 px, `grid-card-assemble` 18 px (IMG_0718). `hyperframes check` zgłasza to jako `text_below_floor`; wtedy zrób grafikę własną albo montuj bez pola.
- **Kolizje klas CSS w `kompozycja.py`** (IMG_0720): szablon ma już m.in. `.tiles`, `.list`, `.row`, `.tile`, `.chip2`, `.panel`, `.cap`, `.kin`. Nowa klasa o tej samej nazwie dziedziczy stare reguły (`right: 0`, `justify-content: center`) i przesuwa elementy. Przed nazwaniem klasy zrób `grep -n "\.nazwa " skrypty/kompozycja.py`. Symetrię sprawdzaj na klatce z osią 540 px (`drawbox`).

## Film 16:9 z lektorem i gliną, PERFOS-film30 (24.11.2026)
- **Głos mono mierzony jako mono kłamie o 3 dB.** Render HyperFrames robi z mono `glos.wav` stereo (dual mono), a `ebur128` w `kontrola_eksportu.py` mierzy stereo: głos z -15,8 LUFS w pliku wyszedł -12,8 LUFS w filmie. Ścieżkę głosu złóż od razu w stereo (`pan=stereo|c0=c0|c1=c0`) i mierz ją w stereo. Przy lektorze z TTS `loudnorm` z `linear=true` zatrzymał się na -15,7 przez limit szczytu, więc pewniej działa wzmocnienie do -14 i `alimiter=limit=0.79` (wzór: `projekty/PERFOS-film30/skrypty/kompozycja.py`, `build_voice()`).
- **`kontrola_eksportu.py` transkrybuje po polsku (`-l pl` na sztywno).** Przy filmie po angielsku skopiuj go do `skrypty/` projektu z `-l en`, inaczej whisper tłumaczy albo gubi zdania.

## Pułapki z rolek z kamery Sony (24–25.11.2026)
- **whisper na kawałku dłuższym niż 30 s** (przy ciasnych stykach kontrola eksportu daje takie kawałki) gubi albo przekręca końcówkę („Cześć i koniecznie zaobserwuj”). Przepisz podejrzany fragment osobno.
- **whisper z promptem na kwestii z długim ogonem** (END_HOLD pod planszą końcową) potrafi zwrócić tylko słowa z ogona i pominąć całą kwestię: `slowa.py` puszczaj na ostatniej kwestii przyciętej do końca mowy.
- **Czasy słów z `wyspy.py`** dla wyspy z kilkoma podejściami są śmieciowe (wszystkie słowa drugiego podejścia na jednym czasie). Podejścia rozdzielaj `kawalki.py` i whisperem `-ml 1 -sow` na wycinku.
- **Krótki falstart bez wyraźnej pauzy** („Jed… jeden folder”, dołek 0,06 s do −48 dB surowego dźwięku): `kawalki.py` w obu trybach go nie rozcina, whisper pisze jedno słowo. Łapie go przebieg mikro w `powtorzenia.py` (dołki do −30 dB na głosie po masteringu).
- **zsh i zmienne w filtrach ffmpeg:** `$g[x]` zsh czyta jako indeks tablicy. Pisz `${g}`. W pętlach `for r in "a b"` zsh nie dzieli słów: użyj `${=r}` albo par `a:b` z `${p%%:*}`.
- **GSAP i kolory z CSS:** `backgroundColor:"var(--accent)"` się nie animuje. Wpisz `{{ACCENT}}` (podmienia `kolory()`), w f-stringu `{{{{ACCENT}}}}`.

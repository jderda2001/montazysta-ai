# Proces: komendy i kontrole

Komendy zakładają, że jesteś w `projekty/<IMG_xxxx>/`. Python z numpy uruchamiaj przez `uv run --no-project --with numpy python3 -I …`, bo systemowy python 3.9 nie ma numpy. Skrypty z `scripts/` skopiuj do `skrypty/` i dostosuj stałe opisane niżej.

## Spis
1. Założenie projektu
2. Synchronizacja audio
3. Transkrypcja i wybór dubli
4. Falstarty
5. A-roll
6. Głos (naturalny; wariant C z Sidonem tylko na prośbę)
7. Czasy słów
8. Kompozycja HyperFrames
9. Render, kontrola, eksport
10. Porównania A/B
11. Zmiana dubla albo cięcia w gotowym projekcie

## 1. Założenie projektu
```bash
mkdir -p skrypty audio analiza aroll hf/fonts hf/renders
cp ~/.claude/skills/montaz-rolek/scripts/*.py skrypty/
cp ../IMG_0526/hf/{package.json,hyperframes.json,meta.json} hf/ && cp ../IMG_0526/hf/fonts/InterTight.ttf hf/fonts/
```
- W `hf/meta.json` i `hf/package.json` zmień nazwę projektu.
- Dźwięk do analizy: `audio/wideo_16k.wav` (z wideo) i `audio/nowe_16k.wav` (z mikrofonu), mono 16 kHz, przez `ffmpeg -ac 1 -ar 16000`.
- Grafiki od użytkownika (zrzuty, awatary) trzymaj w `branding/`. Wycinki skaluj z lanczosem.

## 2. Synchronizacja audio
- `sync.py`: korelacja krzyżowa dla całości plus okna co 15 s (dryf). Wynik w `analiza/sync.json` (`offset`: czas_audio = czas_wideo + offset).
- Dobrze: jakość korelacji wysoka, dryf rzędu ppm (IMG_0526: offset 7,37 s, dryf −15 ppm). Duży dryf oznacza przeliczanie offsetu per kwestia.
- **Brak osobnego audio** (mikrofon krawatowy podpięty do iPhone'a, IMG_0576): pomiń `sync.py`. `audio/nowe_16k.wav` wyciągnij z wideo, w `analiza/sync.json` wpisz `{"offset": 0.0}`, a w `aroll.py` ustaw `AUDIO = VIDEO`. `sprawdz_sync.py` ma wtedy pokazać 0 ms.

## 3. Transkrypcja i wybór dubli
- `wyspy.py`: wyspy mowy (silencedetect) i whisper na każdej, zapis do `analiza/wyspy.json`. `obwiednia.py OD DO --wykres` pokazuje obwiednię RMS i doliny (pauzy).
- Zasada: ostatni pełny dubel każdej kwestii. Wątpliwe miejsca sprawdzaj na obwiedni, nie na samym tekście.
- Hook kinetyczny potrzebuje 1–2 krótkich zdań z liczbą albo kontrastem.
- **Hook bierz z właściwego nagrania**, czyli od zdania, od którego zaczyna się ciąg dubli i treść. Linijka z rozgrzewki albo z rozmowy w pokoju to próba, nawet jeśli brzmi efektownie (IMG_0717: „Zwolniłem montażystę, którego nigdy nie zatrudniałem” Jakub uznał za nielogiczne, a jego mina była zdziwiona). W razie wątpliwości obejrzyj minę na klatce i zapytaj.

## 4. Falstarty (obowiązkowo)
```bash
uv run --no-project --with numpy python3 -I skrypty/kawalki.py        # wszystkie kwestie
uv run --no-project --with numpy python3 -I skrypty/kawalki.py 3 4 9  # wybrane
```
- Kawałek, który powtarza początek następnego, to falstart. W `SEGS` ustaw start na początek powtórzenia (onset z obwiedni).
- Podejrzane jest też tempo: wyraźnie więcej sylab na sekundę mowy, niż wymaga tekst.
- Drugi przebieg z drobniejszym podziałem (pauzy od 0,09 s), obowiązkowo przed oddaniem: `uv run --no-project --with numpy python3 -I skrypty/kawalki.py --drobne`. Łapie zająknięcia w środku zdania, których zwykły podział nie rozdziela.
- Skrypt sam podnosi alarm: `POWTORKA?` przy kwestii, w której kawałki mają o co najmniej 3 sylaby (i 15%) więcej niż tekst, oraz `?` przy kawałku, w którym żadne słowo nie pasuje do tekstu. Lista „Do sprawdzenia” na końcu to rzeczy do rozstrzygnięcia, a nie do przeczytania i pominięcia. Część z nich to przesłyszenia whispera („Czasu.” zamiast „-cesu”, „Zobaczmy.” zamiast „chcę”), dlatego każdą sprawdź tak:
  1. osobny whisper bez promptu na samym kawałku i na oknie o 0,3 s szerszym,
  2. `fonemy.py audio/nowe_16k.wav OD DO`: głośność i liczba przejść przez zero co 20 ms. Samogłoska jest głośna i ma mało przejść, „s/c/sz” ma ich dużo, zwarcie i pauza to dołek. Po tym widać, ile sylab naprawdę padło.
- **Zdanie powiedziane dwa razy pod rząd** (w IMG_0591 „gdzie autor pyta: sukces to szczęście czy umiejętn… gdzie autor pyta: sukces to szczęście czy umiejętności?”): start kwestii przesuń na drugie podejście.
- **Zająknięcie w środku kwestii:** piąty element kwestii w `SEGS`, `wytnij = [(od, do)]`, usuwa kawałek ze środka bez marginesów. Najpierw policz sylaby (głośne grudki w `fonemy.py`) przed i po przerwie, bo są dwa różne przypadki:
  - *powtórzona sylaba* („sukce- cesu”: 4 grudki na 3 sylaby): wytnij od końca głoski w pierwszym podejściu do tej samej głoski w drugim. W IMG_0591 od końca pierwszego „c” do początku drugiego „c” (14,2567–14,40);
  - *pauza w środku słowa* („do… kładnie”: grudek tyle, ile sylab): wytnij samą pauzę i zostaw ok. 70 ms na zwarcie (343,3333–343,42). W IMG_0591 wziąłem to najpierw za powtórzone „do” i wyciąłem pierwsze, przez co zostało „wiedziałem kładnie”.
  „od” wyrównuje się do klatki licząc od początku kawałka, więc dobierz je tak, żeby wypadło w dołku; `aroll.py --edl-only` wypisuje faktyczne miejsce. Skok obrazu większy niż 3 klatki chowa zmiana kadru ustawiona dokładnie na „do”: `[(None, "W"), (14.40, "C")]`; przy 2–3 klatkach kadr zostaje.
- **Sklejkę sprawdź przed renderem w trzech kontekstach**, bez promptu: cała kwestia, okno 2–3 s wokół sklejki i kwestia razem z sąsiednimi. Jeden kontekst nie wystarcza: whisper dopowiada słowo z sensu zdania („wiedziałem kładnie” przeszło jako „dokładnie” na całej kwestii, a w dłuższym fragmencie wyszło „ładnie”). Gdy żaden wariant nie przechodzi wszędzie, przesuwaj cięcie po 10–30 ms i porównuj (dla „sukcesu” przeszedł jeden z siedmiu). Dźwięk kwestii po wycięciu daje `czesci.wytnij(e, SRC, plik)`.
- **Nie skracaj końca kwestii na podstawie samej obwiedni.** Cichy fragment po ostatnim słowie bywa jego końcówką: po skróceniu ogona o 0,37 s z „Napoleon Hill” zostało „Napoleon”. Sprawdzian jak wyżej, whisper z ogonem i bez.
- Nie tnij tego, co jest stylem, a nie potknięciem (westchnienie „Europa, no… co ja mogę rzec?”, pauza przed puentą). Wątpliwe miejsca, których nie ruszyłeś, wymień Jakubowi przy oddaniu.

- **Kontrola całej rolki (od 24.11.2026, obowiązkowo):** po `aroll.py` uruchom `uv run --no-project --with numpy python3 -I skrypty/powtorzenia.py`. Szuka powtórzeń także na stykach kwestii i takich bez pauzy (porównanie akustyczne MFCC: okno 0,4 s przy odstępie 0,4–3 s z progiem 0,68 oraz okno 0,25 s przy odstępie 0,2–0,4 s z progiem 0,78). Celowo powtórzone sformułowania, które są dwa razy w tekście kwestii, pomija. Wynik: lista miejsc z klipami w `analiza/powtorzenia/` i kod wyjścia 1, gdy coś znalazł.

## 5. A-roll
- W `aroll.py` ustaw `VIDEO`, `AUDIO`, `FRAMES` (pod twarz), `SEGS` = [(start_mowy, koniec_mowy, [(od, kadr), …], tekst), …] w czasie nagrania z mikrofonu.
- **Styki kwestii liczone od faktycznego głosu** (od 24.11.2026, Jakub: „czasami wkradają się krótkie przerwy… chciałbym, żeby były minimalnie krótsze, żeby flow było płynniejsze”).
  - `poczatek_mowy()`: start głosu przy −40 dB (oddech i „mmm” przed słowem odpadają), minus `PRE` 0,05 s.
  - `koniec_mowy()`: wygaśnięcie przy −52 dB, plus `POST_ZDANIE` 0,10 s po kropce, pytajniku lub wykrzykniku albo `POST_SRODEK` 0,05 s w środku zdania.
  - Historia:
    - Wcześniej marginesy liczyły się od granic wysp z silencedetect. Wyspa startuje nawet 0,2 s przed głoską, więc na styku było średnio 0,53 s ciszy (C4527, C4528).
    - Po pierwszej poprawce wyszło 0,3–0,4 s i Jakub nadal uznał to za „bardzo niepłynne” (C4534–C4538, 24.11.2026).
    - Teraz cel to ok. 0,15 s ciszy na każdym styku.
  - Pomiar: przerwy powyżej 0,25 s w `audio/aroll.wav` (próg −38 dBFS) mają być tylko tam, gdzie pauza jest celowa.
  - Sprawdzian po `aroll.py`: przerwa między ostatnim słowem kwestii a pierwszym następnej (z `audio/slowa.json`).
  - Celowa pauza przed puentą: opcja kwestii `{"post": …}`.
  - `END_HOLD` 2,5. Wersja `aroll.py` z marginesami per kwestia (`{"pre": …, "post": …}`), twarzą per ujęcie, wyrównaniem głośności kwestii i pauzą `"HOLD"` (zwolnienie i zatrzymana klatka) jest w `projekty/IMG_0597/skrypty/`; bierz ją, gdy nagranie to iPhone 4K z mikrofonem podpiętym do telefonu.
- **Koniec słowa mierz progiem ok. −52 dB, nie −45.** Kawałki z `kawalki.py` i sond kończą się na −45 dB, a ciche końcówki (ś, ch, wygasająca samogłoska) trwają jeszcze 0,05–0,25 s na poziomie −45…−55 dB. To dotyczy końców zdań, po których jest cisza. Przy cięciu w ciągłej mowie sam poziom nie wystarcza: w IMG_0597 po „dziś” szło 0,2 s na −35 dB, które wziąłem za końcówkę „ś”, a była to dźwięczna zapowiedź następnego, wyciętego słowa („gdzie”) i whisper w gotowym pliku słyszał ją jako „Gli-”. Rozstrzyga widmo (sybilant ma energię powyżej 3 kHz, dźwięczna zapowiedź poniżej 500 Hz) albo sonda whisperem na wycinku kończącym się w miejscu cięcia. Gdy obraz ma trwać dłużej niż dźwięk, wycisz dźwięk wcześniej (`"cisza_od"` w `projekty/IMG_0597/skrypty/aroll.py`), zamiast przesuwać cięcie: samą ścieżkę da się potem podmienić bez renderu obrazu.
- **Nie ścinaj naturalnych pauz.** Jeśli dwie wybrane kwestie sąsiadują w nagraniu i dzieli je do ok. 0,5 s, zrób z nich jedną kwestię (zmiana kadru w pauzie) zamiast dwóch z marginesami. Dźwięk w A-rollu przechodzi przez highpass 70 Hz, kompresję i loudnorm −14 (dwuprzebiegowy).
- **Przednia kamera:** obejrzyj klatkę z napisem (książka, ekran, logo na bluzie). Jeśli tekst czyta się wspak, nagranie jest lustrzane i każde ujęcie dostaje `hflip` przed kadrowaniem (IMG_0591).
- **Niski kadr** (twarz w dolnej połowie, nad głową pusta ściana albo sufit): dosuń kadry do dolnej krawędzi, podnieś twarz kadrowaniem tak, żeby napisy zmieściły się pod brodą w strefie bezpiecznej: `CAP_TOP` najwyżej 1170 px (`styl.md`, punkt 8). **Kadr dobiera pomiar twarzy:** `skrypty/twarze.py --flip` (systemowe wykrywanie twarzy z macOS, Vision, bez pobierania czegokolwiek; narzędzie `~/.local/bin/twarz` kompiluje się z `scripts/twarz.swift`) mierzy twarz co 0,4 s w każdym ujęciu, a `kadr()` w `aroll.py` (wzór: `projekty/IMG_0591_strefa/skrypty/aroll.py`) dobiera zoom tak, żeby broda kończyła się najniżej na 1090 px. Przy twarzy w dolnej połowie kadru (broda na 62–76% wysokości) wychodzi zoom 1,4–1,9, bo z 4K da się to zrobić bez utraty ostrości. W IMG_0591 napisy stały na 1420 px (`.cap { top: 1420px }`), czyli pod opisem rolki na Instagramie; to było przed wprowadzeniem strefy 18.11.2026 i nie jest już wzorem pozycji napisów (wzór układu nad głową: `projekty/IMG_0591`). Nakładki z górnego pasa (hasła, karty) przy takim kadrze zachodzą na włosy; to świadoma cena strefy. Wartości sprawdzone na IMG_0591: broda do 1200 px, zoom 1,15–1,6 (przy 1090 px i 1,9 twarz wypełniała pół ekranu, a hasła wypadały na oczach). Kontrola `strefa.py` złapała też elementy, które pulsują albo drżą poza strefę o kilka pikseli (zapal komórki ×1,06, drżenie macierzy) i descendery napisów o 3 px: zapas 15 px od krawędzi.
- **Dwie wersje z jednego cięcia („z efektami” i „tylko napisy”):** `kompozycja.py efekty|napisy` w IMG_0591 pisze do `hf/` albo `hfn/`, a `render.sh` robi obie. Wersja z samymi napisami nie ma grafik, dźwięków ani planszy końcowej.
- Źródło 4K (2160×3840 po obrocie): kadry W/M/C = 1,0/1,2/1,4 (gdy twarz jest już duża, jak w selfie z IMG_0591, zejdź do 1,0/1,12/1,25), np. `"M": (1800, 3200, x, y)`, `"C": (1544, 2744, x, y)`. A-roll z 4K 60 kl./s renderuje się ok. 3 min na 90 s rolki.
- **Dwa hooki (wersje A i B):** wzór w `projekty/IMG_0576`. W `aroll.py` słownik `HOOKS` i stała `HOOK`, wersja B w podfolderze `hookB/` z kopią skryptów, a `przebieg.sh <folder>` puszcza cały łańcuch od A-rollu do kontroli eksportu. Najpierw doprowadź A do końca razem z kontrolą eksportu, dopiero potem rób B, bo każda poprawka cięć oznacza pełny przebieg obu (ok. 12 min na wariant).
```bash
python3 -I skrypty/aroll.py && ln -f aroll/aroll.mp4 hf/aroll.mp4
uv run --no-project --with numpy python3 -I skrypty/sprawdz_sync.py   # dobrze: 4-5 ms na każdej kwestii
```

## 6. Głos
**Domyślnie nic tu nie robisz.** Od 17.11.2026 do kompozycji idzie `audio/aroll.wav`, czyli głos z mikrofonu po lekkim masteringu z `aroll.py` (Jakub: „za bardzo używasz voice enhancer AI… bez tego, albo z dużo mniejszym filtrem”). `kontrola_eksportu.py` porównuj wtedy z `audio/aroll.wav`. Poniższe kroki to wariant C, tylko na jego prośbę albo przy złym nagraniu.

```bash
# surowe cięcia (te same co A-roll, bez obróbki), 16 bit
uv run --no-project --with numpy python3 -I -c "import importlib.util,json,subprocess; from pathlib import Path; s=importlib.util.spec_from_file_location('g','skrypty/glos.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g); Path('audio/studio').mkdir(exist_ok=True); g.raw_concat(json.loads(Path('aroll/edl.json').read_text()), Path('audio/studio/surowe32.wav').resolve()); subprocess.run(['ffmpeg','-v','error','-y','-i','audio/studio/surowe32.wav','-c:a','pcm_s16le','audio/studio/surowe.wav'],check=True)"
uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub --with numpy python -I skrypty/sidon_infer.py audio/studio/surowe.wav audio/studio/sidon.wav
uv run --no-project --with numpy python3 -I skrypty/studio.py
```
- `studio.py` wypisuje przesunięcie (wyrównuje je), F0 oryginału i Sidona (ma się zgadzać, r > 0,9) oraz progi de-essera. Daje `audio/aroll_studio_gleboki.wav` (C) i `audio/aroll_studio.wav` (B).
- Po Sidonie dół jest chudszy o 4–6 dB, a pogłos krótszy. Łańcuch C odbudowuje dół (+7,5 dB przy 170 Hz), tnie muł (−2 dB przy 400 Hz) i ma de-esser za kompresorem 4:1.
- Treść sprawdź whisperem na kwestiach A i C: te same słowa, tylko różnice pisowni whispera.
- Inne nagranie (inny mikrofon lub pokój) zmierz najpierw widmem (LTAS z ramek mowy) i dopiero wtedy koryguj łańcuch.
- Mikrofon krawatowy przez iPhone'a (IMG_0576): po Sidonie środek i góra były 2–5 dB niżej niż w głosie C z IMG_0526. Pomogło `lowshelf` 170 Hz +5,5 dB (zamiast +7,5) i dodatkowe `highshelf=f=5000:g=2.5`. Po korekcie pasma mieszczą się w ±1,7 dB względem wzorca. Sidon liczy 93 s w ok. 3 min, gdy równolegle idzie render.

## 7. Czasy słów
```bash
uv run --no-project --with numpy python3 -I skrypty/slowa.py
python3 -I skrypty/waliduj_napisy.py 0.15
```
- `slowa.py` używa whispera z `-dtw large.v3.turbo -nfa`. t_dtw tokenu to jego koniec, a start słowa wyznacza koniec poprzedniego, interpunkcja, pauza albo powrót głośności.
- Walidacja: pojedyncze wpisy dla słów 1–2 literowych i otwierających zdanie to artefakty. Seria błędów w jednej kwestii oznacza problem z czasami.

## 8. Kompozycja HyperFrames
- W `kompozycja.py`: `PHRASES` (podział i `*wyróżnienia*`, tekst musi odpowiadać słowom po normalizacji; fraza do ok. 20 znaków), `FIX` (pisownia), grafiki w `build()` (czasy przez `W("słowo", po_czasie)` i `seg(i)`), `GLOS` (ścieżka głosu C).
```bash
python3 -I skrypty/kompozycja.py
cd hf && hyperframes check            # 0 błędów; line_unread przy napisach jest normalne
hyperframes snapshot --at 5.0,12.7,23.6,45.9 --no-end -o <scratchpad>/snap   # obejrzyj contact-sheet.jpg
cd .. && uv run --no-project --with numpy python3 -I skrypty/strefa.py       # 0 klatek z treścią poza strefą bezpieczną
```
- `kompozycja.py` wypisuje frazy, które nie mieszczą się w strefie przy czcionce 52 px („UWAGA: … fraz”). Podziel je w `PHRASES` i wygeneruj jeszcze raz, zanim pójdziesz dalej.
- `strefa.py` sam przełącza kompozycję w tryb kontrolny i z powrotem. Gdyby przerwał w połowie, uruchom `kompozycja.py` jeszcze raz przed renderem (w trybie kontrolnym nie ma wideo ani teł plansz). Opis strefy: `styl.md`, punkt 8.
- Zawsze obejrzyj klatki w momentach, które zmieniałeś. Zdany check nie mówi, jak to wygląda.

## 9. Render, kontrola, eksport
```bash
cd hf && hyperframes render -o renders/final.mp4 --quality delivery --fps 60 --video-frame-format png   # w tle tylko przez run_in_background, nie przez `( … ) &`
uv run --no-project --with numpy python3 -I ../skrypty/kontrola_eksportu.py renders/final.mp4 ../audio/aroll_studio_gleboki.wav
D="$HOME/Desktop/Montażysta AI/Eksporty/Rolki/<RRRR-MM-DD Tytuł>"   # reklamy: Eksporty/Reklamy adGen/…, long-form: Eksporty/YouTube/…
mkdir -p "$D" && cp -f renders/final.mp4 "$D/<Tytuł>_MM.RR.mp4"
```
- Dobrze: −14,0 LUFS, szczyt −1,5, przesunięcie 0,00 ms, różnica ok. −30 dB (szum AAC), w transkrypcji kawałkami brak powtórzeń.
- **Przy ciasnych stykach kawałki z `kontrola_eksportu.py` robią się długie (ponad 30 s) i whisper gubi albo przekręca końcówki** (C4535, 25.11.2026: „Cześć i koniecznie zaobserwuj”, a w nagraniu było pełne CTA). Zanim uznasz to za błąd montażu, przepisz podejrzany fragment osobno, w oknie 10–12 s.
- Render z HyperFrames: 47 s rolki to ok. 70 s pracy, ok. 50 MB.

## 10. Porównania A/B
- Folder `ab/` z kompozycją: plansza „A/B/C” 1,5 s, potem ten sam fragment rolki (`<video muted>` + `<audio src=…>`) z podpisem w pigułce u dołu.
- Wspólne źródło wideo: twarde linki do `hf/renders/final.mp4` pod różnymi nazwami (`va.mp4`, `vb.mp4`).
- Render: `hyperframes render -o renders/ab_X.mp4 --video-bitrate 4M` (poniżej 30 MiB, dojdzie na telefon).
- Kontrola: głośność części ±0,5 LU, przesunięcie dźwięku 0 ms, obraz najlepiej pasuje przy przesunięciu 0 klatek (sprawdzaj w połowie klatki).

## 11. Zmiana dubla albo cięcia w gotowym projekcie
Kolejność: `aroll.py` → `ln -f` → (`kawalki.py` dla zmienionych kwestii) → `slowa.py` → surowe cięcia + `sidon_infer.py` + `studio.py` → `kompozycja.py` → check i snapshot → render → `kontrola_eksportu.py` → eksport. Grafiki dopasują się same, bo liczą się ze słów.

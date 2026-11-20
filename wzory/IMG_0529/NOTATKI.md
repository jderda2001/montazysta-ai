# IMG_0529: long-form YouTube „Zautomatyzowany dział growth” (16:9)

Pierwszy odcinek serii o zautomatyzowanej firmie: 4 agentów AI działu growth (Artur, Kaja, Weronika, Tymon), czego AI jeszcze nie zrobi, aplikacja i koszty.

## Źródła

- Obraz: `~/Downloads/IMG_0529.MOV` (iPhone, 3840×2160, HEVC 60p, SDR bt709, 20:33).
- Dźwięk (mikrofon, Dyktafon, dwa pliki, bo nagranie się urwało):
  - `~/Desktop/Salon kosmetyczny Dreams 7.m4a` (m7, 4:11): wstęp.
  - `~/Desktop/Salon kosmetyczny Dreams 8.m4a` (m8, 14:02): reszta.
- Materiały: `materialy/` (zrzuty profili agentów, lista „Growth”, newsletter). Awatar Kai jest w jakości 396 px z IMG_0526, pozostałe awatary to wycinki ze zrzutów (69 px, powiększone).

## Synchronizacja (`skrypty/sync.py m7|m8`)

- m7: czas audio = czas wideo − 101,40 s, rozrzut 2 ms. Pozorne skoki o ok. 5 ms to okres tonu krtaniowego, a nie ubytki.
- m8: czas audio = czas wideo − 364,06 s, dryf −6,5 ppm (5 ms na całość), rozrzut 0,1 ms.
- **m7 jest uszkodzony od 249,44 s** (pętla 0,5 s bufora, „byłem, byłem, byłem…”). Końcówka zdania „…to ja byłem odpowiedzialny za przynoszenie tego przychodu” istnieje tylko na dźwięku z telefonu.
  Decyzja: wycinam ten wątek i dubel z początku m8 („Dlatego też czuję…”). Po „…dlaczego go tak bardzo czuję.” od razu pada „I dlaczego to jest pierwszy odcinek z tej serii?”. Dzięki temu w filmie nie ma dźwięku z telefonu.
  Alternatywa: wkleić te ok. 3 s z telefonu po dopasowaniu barwy. Będzie słychać inny pogłos.

## Montaż (`skrypty/montaz.py`)

- Mapa nagrania: `kawalki.py` (350 kawałków między pauzami, każdy transkrybowany osobno) i `slowa_kawalki.py` (czasy słów z DTW, `-nfa`).
- Lista cięć: `SEGS` + `CUTS`. Wycięte zostały:
  - duble hooka (trzecie podejście zostaje) i 1. „półrocznej”;
  - „eee” i „uhhh” (wstęp oraz „ku końcowi… jeśli spodobało się… ten”);
  - „zszedłem z tronu, znaczy jakby”, „żeby ich praca była na tyle…”, „podeszłem/podszedłem”;
  - falstarty „Tymon jest osobą, która jest odpow…”, „Czego… / To… / Stare… / te takie…”, „dwadzieścia… 24 boty”;
  - powtórzenia „które/na które”, „od/od”, „która/która”, „alternatywą/alternatywa”, „to/to działamy”, „te wszy-/wszystkie”;
  - przeciągnięte „Także…” i podwójne podsumowanie struktury.
- Pauzy powyżej 0,6 s są skracane do ok. 0,3 s. Długie ujęcia dzielę w pauzach zmianą kadru, bez wycinania czasu: 142 ujęcia po 4–10 s.
- Kadry (źródło 4K, twarz ok. 2170, 740): W = 1,0, M = 1,2, C = 1,4. Co drugie ujęcie W. Hook ma kadr C.
- Kontrola cięć: `kontrola.py` (zmontowany dźwięk kawałkami między pauzami).
- Wynik: mowa 15:02 plus plansza końcowa 8 s, razem 15:10.

## Dźwięk

- `audio.py`: m7 dopasowany do m8. Korekcja barwy (match EQ z widm mowy, 75% różnicy): 800–1000 Hz −4,5 dB, góra powyżej 5 kHz −6 dB. Do tego +4,5 dB głośności. Cięcia mają przejścia 8 ms.
- Głos C (zatwierdzony 13.11): `sidon_infer.py` offline (modele z cache, bez pobierania), potem `studio.py` w wariancie głębokim. Wynik: `audio/aroll_studio_gleboki.wav`, −14 LUFS.
- Wersja A (bez AI): `audio/montaz.wav` (highpass, kompresja, −14 LUFS).

## Grafiki (`skrypty/kompozycja.py`) i napisy (`skrypty/napisy.py`)

- 44 grafiki, każda jako osobna warstwa HyperFrames (`hf/o_*.html`), renderowana w 4K do ProRes 4444 z alfą.
- Treści grafik pochodzą tylko z tego, co pada w nagraniu, i ze zrzutów (zajawki na liście „Growth” są ucięte jak na zrzucie).
  Nazwisko klienta z podglądu Kai („Klimkowskiego”) jest rozmyte (dane klienta).
- Newsletter jest pokazany bez nagłówka z logo adGen.
- Napisy: słowo po słowie w stylu z IMG_0526, frazy po 2–5 słów, jedno wyróżnienie na frazę. Są chowane tam, gdzie ten sam tekst pokazuje grafika.
- Tekst napisów i SRT jest poprawiony ręcznie: `skrypty/tekst.py`. Na górze pliku są niepewne miejsca.
- `napisy.srt`: pełny tekst do wgrania na YouTube. `rozdzialy.txt`: rozdziały do opisu.

## Render

- `aroll.py`: ujęcia 4K HEVC VT 100 Mb/s (`aroll/ujecia`, cache).
- `render_warstwy.py`: warstwy grafik i napisów.
- `finalny.py`: składanie w oknach po 60 s, HEVC 45 Mb/s, AAC 320 kb/s. Opcja `--bez-napisow` daje wersję bez napisów.
- Podgląd dowolnej chwili: `podglad.py T1 T2 …`.

## Do potwierdzenia przez Jakuba

- Nazwa aplikacji: whisper słyszy „grogbot”. W grafice rozdziału 04 jest „Grok”, w napisach „Grok Bot”.
- „Półrocznej, bardzo mocnej pracy”: whisper raz słyszy jedno „bardzo”, raz trzy. W napisach jest jedno.
- „No to będzie z Polski” (alternatywa dla Groka): whisper słyszy „będę”.

## Wynik (13.11, 18:50)

- **Eksport:** `~/Desktop/Montażysta AI/Eksporty/YouTube/2026-11-13 Zautomatyzowany dział growth/Zautomatyzowany dział growth_11.26.mp4`, 3840×2160, 30 kl./s, HEVC (hvc1) ok. 41 Mb/s, AAC 320 kb/s, 15:10, 4,73 GB. Obok leżą:
  - `…_11.26.srt`: napisy do wgrania na YouTube;
  - `… - opis i rozdziały.txt`: opis i rozdziały.
- **Kontrole:**
  - głośność −14,0 LUFS, szczyt −1,5 dBFS (limiter −2,5 dB przed AAC w `audio/glos_finalny.wav`);
  - dźwięk względem głosu C przesunięty o 0,00 ms (początek, środek i koniec), różnica ok. −40 dB;
  - 27 300 klatek, każde okno ma dokładną liczbę klatek;
  - synchronizacja ust: −4 do +3 ms na 140 ujęciach;
  - transkrypcja gotowego pliku kawałkami bez dubli i ucięć (`analiza/kontrola.txt`).
- **Pliki robocze:**
  - ujęcia A-rollu: `aroll/ujecia`, ok. 11 GB;
  - warstwy ProRes: `hf/renders`, ok. 20 GB;
  - okna: `render/okna`, ok. 4,7 GB.
  Po akceptacji można je usunąć. Są potrzebne tylko do szybkich poprawek, bo wtedy renderuje się wyłącznie to, co się zmieniło.
- **Wersja bez napisów:** `python3 -I skrypty/finalny.py --bez-napisow --wyjscie render/odcinek_bez_napisow.mp4` (ok. 10 min).
- **Świadome odstępstwa od stylu rolek:**
  - napisy w dolnym pasie 16:9;
  - bez ciągłego najazdu w każdym ujęciu (w 15-minutowym odcinku zmiany kadru W/M/C idą na cięciach);
  - plansza końcowa trwa 8 s pod ekran końcowy YouTube.

## Poprawki po ocenie (13.11, wieczór)

- **Ocena Jakuba:** „zajebiste!!!!”.
- **Logo aplikacji** (`hf/assets/app_logo.svg`, odtworzone wektorowo z jego zdjęcia) stoi obok „Grok Bot” na planszy rozdziału 04 (ok. 11:40).
- **„Subskrybuj”** w CTA ma biały tekst.
- **Eksport podmieniony** na wersję v2 (27 300 klatek, okna po 1800 klatek). Rendery v1 i v2 usunięte 13.11 za zgodą Jakuba (ok. 9,5 GB). Obraz v2 jest w `render/odcinek_v3.mp4`, a w razie potrzeby da się go złożyć z `render/okna` przez `finalny.py`.
- **Muzyka lo-fi jest w eksporcie** (`render/odcinek_v3.mp4`, ten sam obraz co v2, nowa ścieżka dźwięku). Szczegóły niżej w sekcji „Muzyka”.

## Rolki promo (`skrypty/rolki.py`, folder `rolki/`)

Zasada Jakuba: przy każdym long-formie 3 pionowe rolki po 10–15 s, robione razem z odcinkiem.

| Rolka | Czas | Fragmenty odcinka | Grafika |
|---|---|---|---|
| 1 „Z kilkunastu etatów do dwóch” | 12,3 s | 0:00 „Zautomatyzowałem cały dział growth” · 0:41 „Zeszliśmy z parunastu etatów do dosłownie dwóch” · 1:22 „Przychody razy 2,5… a zespół trzykrotnie mniejszy” | hook kinetyczny w 3 częściach → plansza ×2,5 / 3× → plansza końcowa |
| 2 „Czego AI nie zrobi” | 14,8 s | 8:50 „Czego AI nie zrobi?” · 9:08 „Ten bot, ten agent nie zamknie sprzedaży za nas” · 10:19 „AI nam jeszcze nie zadzwoni… będzie fala krytyki” | hook → lista z trzema „nie” → twarz + chip „FALA KRYTYKI” → plansza końcowa |
| 3 „24 agentów, start za 30 $” | 14,1 s | 12:55 „24 agentów, którzy każdy zastępuje… osobę fizyczną” · 13:09 „Z tym, że Tobie na start… plan za 30 dolarów wystarczy” | hook (24 AGENTÓW / OSOBĘ FIZYCZNĄ) → chip „NA START” → plansza 30 $ → plansza końcowa |

- **Obraz** idzie prosto z 4K: kadr 9:16 pod twarz, ze środkiem x ustawianym osobno dla każdego ujęcia (twarz chodzi w zakresie 1940–2320 px).
- **Głos** to C z odcinka, a **napisy** powstają ze słów odcinka.
- **Cięcia** leżą w minimach obwiedni. Każde sprawdziłem transkrypcją kawałka; w rolce 3 przed „Z tym, że” wypadło „Eee…”.
- **Kontrole:**
  - −14,0 LUFS, szczyt −2,5 dBFS;
  - dźwięk to głos C (0,00 ms);
  - synchronizacja ust −1…−10 ms, jak w odcinku;
  - transkrypcja bez powtórzeń;
  - `hyperframes check` bez błędów.
- **Eksport:** `Eksporty/YouTube/2026-11-13 Zautomatyzowany dział growth/Rolki promo/` (`…_ROLKA 1|2|3_11.26.mp4`, 12–21 MB, oraz `…_ROLKI_11.26 - opisy.txt`).
- **Rezerwa na kolejne rolki:**
  - „AI montuje nam 80–90% materiałów, wcześniej dwóch montażystów” (8:03–8:33);
  - „nie zastąpimy feelingu closingu w B2B” (9:30–9:37).

## Muzyka (`skrypty/muzyka.py`, 13.11 wieczór)

- **Źródło:** 6 utworów z Biblioteki audio YouTube, pobranych za zgodą Jakuba do `~/Desktop/Montażysta AI/Muzyka/`. Licencja Biblioteki audio YouTube: wolno używać w swoich filmach, także zarabiających, bez podawania autora. Wszystkie są instrumentalne (whisper zwraca na nich tylko halucynacje).
- **Rozkład** (przenikanie 3 s na planszach rozdziałów):

| Część | Od | Utwór |
|---|---|---|
| Intro | 0:00 | On The Flip (The Grey Room / Density & Time) |
| 01 Dlaczego growth, struktura | 2:52 | Twinkle (The Grey Room / Density & Time), od 0,9 s (wcześniej cisza) |
| Tymon, Artur, voice call, co dalej | 5:55 | Misdirection (The Grey Room / Density & Time) |
| 03 Czego AI nie zrobi | 8:50 | High Noon (The Grey Room / Density & Time) |
| 04 Aplikacja i koszty | 11:38 | No Rush (Dyalla) |
| Podsumowanie i plansza końcowa | 13:31 | Kicking It (Dyalla) |

- **Poziom:**
  - każdy utwór do −14 LUFS;
  - EQ robi miejsce na głos: −3 dB przy 170 Hz, −3,5 dB przy 2,7 kHz;
  - podkład na −29 LUFS, a gdy mówisz, dodatkowo −5 dB (ducking od głosu C: atak 80 ms, powrót 600 ms);
  - wynik: pod mową muzyka jest 20 dB ciszej niż głos;
  - na planszy końcowej +4 dB, potem wyciszenie przez ostatnie 4 s.
- **Kontrole:**
  - film −14,0 LUFS, szczyt −1,5 dBFS po AAC;
  - dźwięk filmu zgodny z `audio/glos_z_muzyka.wav` (0,00 ms w 5 miejscach na pełnym dekodzie);
  - 27 300 klatek (obraz skopiowany z v2).
- **Głośniej albo ciszej:** zmień `BASE_LUFS` w `muzyka.py` (np. −26 to 3 dB głośniej), potem `muzyka.py` i podmiana dźwięku (`ffmpeg -i render/odcinek_v3.mp4 -i audio/glos_z_muzyka.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k …`). Całość trwa ok. 1 min.
- **Podgląd na telefon:** `render/podglad_muzyka.mp4` (60 s: początek i pierwsze przejście).
- **Pułapka pomiaru:** `-ss` na MP4 z AAC przesuwa dźwięk o 5–21 ms, czyli o ramkę AAC. Przesunięcie mierz na pełnym dekodzie.
- **Ocena:** poziom muzyki „Pasuje” (13.11, po podglądzie 60 s).

## Paleta (zmiana 17.11.2026, po publikacji)

Odcinek, jego warstwy w `hf/` i rolki promo zostały wyrenderowane 13.11.2026 z pomarańczowym akcentem `#ff7018`. 17.11.2026 Jakub przeszedł w personal brandzie na czerń, biel, ciemny szary i akcent `#00E5A0`, a te skrypty są szablonem dla kolejnych odcinków, więc dostały nową paletę:

- `skrypty/paleta.py`: `PALETY`, `MARKA` i `kolory()` dla `kompozycja.py` (grafiki) i `napisy.py`;
- `skrypty/rolka_szablon.py` i `skrypty/rolki.py`: wersje ze skilla `montaz-rolek` (własny przełącznik `MARKA`);
- oryginały sprzed zmiany: `skrypty/_przed_paleta_2026-11-17/`.

Ponowne uruchomienie `kompozycja.py` albo `napisy.py` w tym projekcie nadpisze warstwy w `hf/` wersją w nowej palecie. Żeby odtworzyć odcinek tak, jak wyszedł, ustaw `MARKA = "adgen"` w `paleta.py` (pomarańcz, biały tekst na akcencie, zielone ptaszki; light leak wychodzi wtedy trochę bielszy niż w oryginale) albo użyj skryptów z kopii.

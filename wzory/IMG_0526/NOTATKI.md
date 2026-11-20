# IMG_0526 – rolka „Kaja zamiast settera”

Źródła:
- Obraz: `~/Downloads/IMG_0526.mov` (iPhone, 1080×1920 po obrocie, 3:36, HEVC, z dźwiękiem z telefonu).
- Dźwięk: `~/Desktop/Montażysta AI/Nagrania /Audio do rolki o Kaji.m4a` (mikrofon, 3:33, to samo wykonanie).
- Profil Kaji: `branding/kaja_profil.png` (zrzut od użytkownika), wycięty awatar `branding/kaja_avatar.png`.

## Podmiana dźwięku

- Przesunięcie: czas w nowym audio = czas w wideo + 7,372 s (korelacja krzyżowa, `skrypty/sync.py`).
  Dryf zegara ok. 3 ms na 200 s, czyli pomijalny.
- Kontrola gotowego A-rollu: `skrypty/sprawdz_sync.py`. Na każdej kwestii przesunięcie wynosi 4–5 ms (klatka trwa 33 ms).
- Dźwięk w A-rollu pochodzi wyłącznie z mikrofonu: highpass 70 Hz, łagodna kompresja, loudnorm dwuprzebiegowy −14 LUFS, TP −1,5.

## Wybrane duble (czas w nowym audio)

| # | Kwestia | Czas | Kadr |
|---|---|---|---|
| 0 | Setter kosztuje Cię w okolicach 5–6 koła miesięcznie. | 10,28–13,38 | W |
| 1 | Moja Kaja kosztuje mnie niecałe dwie stówki. | 13,76–15,72 | C |
| 2 | Pilnuje pipeline'u, pisze do leadów, przygotowuje oferty. | 29,80–32,93 | M (plansza) |
| 3 | I każdego ranka dostaję od niej to, co jest konkretnie na ten dzień do zrobienia. | 56,97–60,49 (3. dubel, po falstarcie) | W |
| 4 | CRM jest zawsze uporządkowany. | 71,73–73,28 (po falstarcie) | M |
| 5 | Każde spotkanie ląduje w kalendarzu i wysyła się zaproszenie do klienta. | 88,25–91,60 (ostatni z 5) | C (plansza) |
| 6 | Nie bierze urlopu, nie choruje i nigdy nie zapomina o follow-upach. | 102,77–105,73 | W |
| 7 | Czy się myli? Czasem tak. Z tym, że setter też się myli, a kosztuje 30 razy więcej. | 113,43–118,62 (ostatni) | C → plansza |
| 8 | Kaja to agent AI, to oczywiste. … Czy na pewno agent AI po prostu nie wystarczy? | 132,15–144,20 | M/W/C/M |
| 9 | Jeśli interesuje Cię, skąd taką Kaję wytrzasnąć, napisz komentarz o treści Kaja, a nagram o tym osobną rolkę. | 203,97–209,80 (ostatni CTA, po falstarcie) | C |

Kadry: W to pełny kadr, M to zoom 1,15, a C to zoom 1,30 (źródło ma tylko 1080 px szerokości, więc więcej nie przybliżam).

Falstarty (poprawka z 13.11, zgłoszona przez użytkownika). Trzy duble zaczynały się od urwanego początku, po którym padało pełne zdanie:
- „I każdego ranka dosta…” (55,61);
- „CRM jest wz…” (70,57);
- „Jeśli interesuje Cię, jak sobie tak…” (202,40).

Whisper na całym dublu zwracał tylko czyste zdanie, więc teraz te kwestie startują od powtórzenia. Po tej zmianie rolka ma 47,6 s zamiast 51,7 s. Wykrywanie: `skrypty/kawalki.py` (każdy kawałek między pauzami transkrybowany osobno).
Zmiany kadru w kwestii 8 wypadają w pauzach po „oczywiste.”, po „pierwszego,” i przed „Czy na pewno”.

### Niewykorzystane warianty (do ewentualnej wersji B)

- Możliwy hook B: „Zanim zatrudnisz kolejną osobę do klepania CRM-u, sprawdź, czy nie zrobi tego agent.” (124,86–127,90)
- CTA 1: „Zostaw komentarz Kaja i będzie to dla mnie wyznacznik, czy nagrać osobny odcinek…” (157,29–167,24)
- CTA 2: „Jeśli interesuje Cię, skąd taką Kaję sobie wytrzasnąć, zostaw komentarz o treści Kaja, a nagram o tym kompletnie osobny odcinek.” (176,56–184,89)
- Szybszy dubel: „Czy się myli? Czasem tak, tylko że setter też się myli…” (108,48–111,58)
- „I każdego ranka dostaję na tacy od niej to, co jest do zrobienia.” (43,51–47,39)

## Grafiki (styl adGen)

- Hook kinetyczny: „5–6 KOŁA” na biało, „DWIE STÓWKI” na pomarańczowo, Kaja jako pigułka z awatarem
  (bez napisu „Bot zespołu”, żeby nie zdradzać puenty).
- Plansza „Co robi Kaja”: pipeline, leady, oferty.
- Powiadomienie „Plan na dziś” (3 follow-upy, 2 spotkania, 1 oferta) nad głową, w pełnym kadrze.
- Chip „CRM ✓ uporządkowany”.
- Plansza kalendarza: spotkanie wpada w slot, „zaproszenie wysłane”.
- Kafelki: urlop, choroba, follow-upy.
- Plansza kosztów: setter 5–6 tys. zł kontra Kaja < 200 zł, „30× więcej”.
- Odkrycie: odtworzony profil Kaji (jak na zrzucie) z plakietką AGENT AI przy „Kaja to agent AI”.
- Chip „Zadanie dla Ciebie”.
- CTA: pole komentarza, w którym wpisuje się „Kaja”.
- Plansza końcowa: dymek „KAJA” i „Napisz w komentarzu”, bez logo adGen (rolki są pod personal brand użytkownika, logo nigdy).

Liczby na powiadomieniu i godzina spotkania w kalendarzu są ilustracyjne (zmienisz je w `kompozycja.py`).

## Jak zmienić

- Kontrola falstartów w wybranych dublach: `uv run --no-project --with numpy python3 -I skrypty/kawalki.py [nr kwestii]`.
- Duble lub kadry: `SEGS` w `skrypty/aroll.py`, potem:
  `python3 -I skrypty/aroll.py && uv run --no-project --with numpy python3 -I skrypty/slowa.py && python3 -I skrypty/kompozycja.py`
  i `ln -f aroll/aroll.mp4 hf/aroll.mp4`.
- Napisy (podział na frazy, wyróżnienia `*słowo*`): `PHRASES` w `skrypty/kompozycja.py`.
- Plansze i teksty grafik: `skrypty/kompozycja.py`.
- Render: w `hf/` uruchom `hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format png`.
- Napisy do Premiere i uploadu: `napisy.srt`.

## Dźwięk B: „miękki głos” (próbka A/B z 13.11, czeka na decyzję)

Analiza barwy (widmo średnie z ramek mowy, porównane z typowym widmem mowy):
- góra 2,5–8 kHz o ok. 8–12 dB mocniejsza (ostrość, sybilanty);
- „pudło” w 300–450 Hz ok. +5 dB;
- dolina ok. 800 Hz, prawdopodobnie odbicie od blatu (mikrofon stoi ok. pół metra od ust);
- dół już mocny, a pogłos krótki (RT60 ok. 0,25 s).

Łańcuch B (`skrypty/glos.py`): highpass 70 Hz → EQ → de-esser → ta sama kompresja co A → −14 LUFS.
- EQ: 360 Hz −3, 820 Hz +2, 3 kHz −4, półka od 5 kHz −4.
- De-esser: `adynamicequalizer` przy 6,5 kHz, próg z rozkładu poziomów sybilantów i samogłosek.

Wynik przy tej samej głośności:
- ostrość 2,5–4 kHz −2,4 do −3,3 dB, góra 5–8 kHz −4 do −5 dB, dół i środek +1 do +2 dB;
- najgłośniejsze sybilanty −7 dB, przy czym ciche „s” i samogłoski zostają;
- przesunięcie względem A: 0 ms.

Pliki:
- `audio/aroll_miekki.wav`: B na całą rolkę, oś czasu jak `aroll.wav`.
- Klip porównawczy: `ab/renders/ab_glos.mp4`, czyli pierwsze 12,7 s rolki najpierw z A, potem z B (kompozycja w `ab/index.html`).

Jeśli B zostaje, wystarczy podmienić ścieżkę dźwięku w `hf/renders/final.mp4` na `aroll_miekki.wav`, bo ma tę samą oś czasu.

## Dźwięk „studio AI” (Sidon), druga próba z 13.11

Wersja „miękki głos” (sam EQ) użytkownikowi nie wystarczyła. Chce brzmienia studyjnego, głębokiego.

**Sidon** (github.com/sarulab-speech/Sidon, ICASSP 2026, MIT) odtwarza mowę „jakości studyjnej” z nagrań z pokoju.
- Wagi: `sarulab-speech/sidon-v0.1`, wersje CPU ok. 1 GB w cache Hugging Face.
- Inferencja: `skrypty/sidon_infer.py`, w środowisku uv z PyTorch.
- 47,6 s głosu przetwarza się w ok. 12 s na CPU Maca.

Co zmienia Sidon:
- pogłos z ok. 0,25 s do 0,12 s;
- dolina przy 800 Hz (odbicie od blatu) znika;
- ostrość i sybilanty o 5–8 dB łagodniejsze;
- dół o 4–6 dB chudszy.

Kontrole wyniku:
- Synchronizacja: Sidon opóźnia o 8 ms, `studio.py` to wyrównuje.
- Ton głosu: 137,9 → 136,8 Hz, zgodność intonacji r = 0,92.
- Treść: słowa bez zmian (whisper na A i na wersji AI daje te same wyniki).

Warianty (`skrypty/studio.py`, wszystkie −14 LUFS, oś czasu jak A):
- `audio/aroll_studio.wav`: Sidon + de-esser + kompresja jak w A (czysto, sucho, neutralnie).
- `audio/aroll_studio_gleboki.wav`: Sidon + półka w dole +7,5 dB (170 Hz), −2 dB przy 400 Hz, odrobina powietrza, kompresja 4:1, de-esser za kompresorem. Wynik względem A: dół 100–160 Hz +2 do +4 dB, „pudło” −2 dB, góra −3 do −4 dB, najostrzejsze sybilanty −8,6 dB.

Klip porównawczy: `ab/renders/ab_studio.mp4`, kolejno A / B (studio AI) / C (studio AI + głęboki). Poprzednie A/B (sam EQ) leży w `ab/renders/ab_glos.mp4`.

**Decyzja 13.11: w rolce jest głos C** (`audio/aroll_studio_gleboki.wav`). `kompozycja.py` wycisza wideo A-rollu i dodaje ścieżkę `<audio src="glos.wav">`, czyli twardy link do pliku ze stałej `GLOS`. Każdy kolejny render ma więc już głos C.
- Powrót do A: ustaw `GLOS = P / "audio/aroll.wav"`.
- Po zmianie cięć w kolejności: `aroll.py` → `slowa.py` → `glos.py`/`studio.py` (Sidon na nowych surowych cięciach) → `kompozycja.py` → render.
- Kontrola eksportu: −14,0 LUFS, szczyt −1,5 dBFS, dźwięk = głos C (przesunięcie 0 ms), obraz identyczny z zatwierdzoną wersją.

## Czasy słów (`slowa.py`)

Każda kwestia jest transkrybowana osobno, whisperem z `-dtw large.v3.turbo -nfa`.
Bez `-nfa` flash attention po cichu wyłącza DTW (t_dtw = −1) i zostają czasy heurystyczne. W pierwszej wersji tej rolki były przez to miejscami 0,35–0,6 s za wcześnie, np. „agent AI po prostu” i „i nigdy nie zapomina”.

- Koniec słowa: t_dtw jego ostatniego tokenu z literą lub cyfrą. Sondy potwierdzają, że to koniec tokenu: whisper na odcinku [początek, t] pokazuje słowo dopiero, gdy t minie tę wartość.
- Start słowa: koniec poprzedniego słowa. Jeśli po poprzednim słowie była interpunkcja, przesuwa go jej t_dtw. Potem jeszcze koniec pauzy z obwiedni RMS albo powrót głośności po krótkim spadku (zwarcie, oddech), o ile spadek zaczyna się od razu po poprzednim słowie.
- Pierwsze słowo kwestii zaczyna się od faktycznego początku mowy.

Kontrola: whisper na odcinku [początek kwestii, koniec słowa + 0,15 s] musi już zawierać to słowo.

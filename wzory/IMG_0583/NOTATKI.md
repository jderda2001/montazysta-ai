# IMG_0583 – reklamy adGen „Leady z OC” (hook A / B / C)

Źródło: `~/Downloads/IMG_0583.MOV` (iPhone 4K 60 kl./s, pion, 4:12, zakres kolorów tv). Dźwięk z tego samego pliku (mikrofon krawatowy DJI), offset 0.
Eksport (17.11.2026): `~/Desktop/Montażysta AI/Eksporty/Reklamy adGen/2026-11-17 Leady z OC/`
- `Leady z OC_HOOK A_11.26.mp4` (47,5 s), `…_HOOK B_…` (44,8 s), `…_HOOK C_…` (44,2 s)
- `Leady z OC_11.26 - teksty reklamy.txt` (2 propozycje tekstu pod reklamę)

Paleta: adGen (`MARKA = "adgen"`, pomarańcz `#ff7018`), bez logo. Głos: naturalny z mikrofonu po lekkim masteringu (`audio/aroll.wav`), bez Sidona (zasada z 17.11.2026).

## Układ projektu

- `skrypty/` w głównym folderze to źródło prawdy. Wersje robocze: `A/`, `B/`, `C/` (każda ma `skrypty/`, `aroll/`, `audio/`, `hf/`). Wersję wybiera nazwa folderu (`HOOK = P.name`).
- Po każdej zmianie skryptu: `for h in A B C; do rsync -a skrypty/ $h/skrypty/; done`.
- Kolejność dla wersji (z jej folderu): `aroll.py` (albo `--audio-only`, gdy zmienia się tylko dźwięk) → `ln -f aroll/aroll.mp4 hf/aroll.mp4` → `kawalki.py` → `slowa.py` → `waliduj_napisy.py 0.15` → `kompozycja.py` → `hyperframes check` i `snapshot` → `hyperframes render` → `kontrola_eksportu.py hf/renders/final.mp4 audio/aroll.wav` → `odsluch_kwestii.py hf/renders/final.mp4`.
- `skrypty/poziomy.py` (z głównego folderu, po `aroll.py --edl-only` w A, B, C) zapisuje `analiza/poziomy.json`: wyrównanie głośności kwestii.
- Pierwsze rendery z głosem C (Sidon) zostały jako `X/hf/renders/final_sidon.mp4`, a głos C w `X/audio/aroll_studio_gleboki.wav`, gdyby Jakub chciał porównać.

## Wybrane duble (czasy w źródle)

| Fragment | Czas | Tekst (tak jak powiedział) |
|---|---|---|
| Hook A | 12,56–14,66 + 18,17–25,80 | Prowadzisz kancelarię zajmującą się szkodami OC? Płać tylko i wyłącznie za leady, które są zweryfikowane telefonicznie, a nie za takie, które za każdym razem mówią: „Ej, ja nie pamiętam, żebym cokolwiek wypełniał”. |
| Hook B | 37,27–38,79 + 39,47–40,13 + 40,99–45,57 | Dzwonisz do leada ze szkody OC. A tam cisza. Gwarantuję Ci, nasze leady odebrały telefon, zanim dotarły do Twojego CRM-a. |
| Hook C | 63,63–65,45 + 79,29–81,48 + 84,71–86,85 | Ubezpieczyciel zaniżył odszkodowanie OC. Poszkodowany właśnie teraz szuka kancelarii, która to sprawdzi. I teraz pytanie: trafi do Ciebie, czy do konkurencji? |
| Korpus 1 | 134,25–137,93 | Dostarczamy kancelariom osoby, którym ubezpieczyciel wypłacił za mało z OC sprawcy |
| Korpus 2 | 141,89–144,33 | i które chcą sprawdzić, czy da się odzyskać więcej. |
| Korpus 3 | 149,41–153,59 | Nasz zespół za każdym razem najpierw dzwoni do każdej z tych osób. |
| Korpus 4 | 160,34–165,52 | Dostajesz tylko i wyłącznie te, które odebrały i chcą rozmawiać z prawnikiem. |
| Korpus 5 | 186,94–189,96 | Każda od razu ląduje w Twoim CRM z notatką z rozmowy. |
| Korpus 6 | 194,19–196,82 | Pierwsze leady masz do 48 godzin od startu. |
| Korpus 7 | 199,90–202,72 | Płacisz za leady, a nie za budżet reklamowy czy czas zespołu. |
| Korpus 8 | 215,04–217,76 | I co warto dodać, każde zamówienie jest objęte gwarancją. |
| CTA | 227,04–228,14 + 228,75–233,33 | Zostaw kontakt poniżej. Oddzwonię i powiem Ci, ile i na kiedy mógłbym Ci dostarczyć pierwsze leady OC. |

## Falstarty (wycięte, kwestia startuje od powtórzenia)

- Hook B: 36,81 „Dzwoni—” → start 37,27.
- Hook C: 77,74 „Poszko—”, 78,18 „Poszkodowany właśnie” → start 79,29 (trzecie podejście, pełne zdanie, szybkie tempo).
- Korpus 4: 159,45 „Dostajesz tylko—” → start 160,34.
- CTA: 226,17 „Zostaw kontakt,” → start 227,04.

## Różnice względem skryptu

- Hooki A, B, C powiedziane inaczej niż w skrypcie (tabela wyżej).
- „Pierwsze leady masz **do 48 godzin** od startu” zamiast „w 1 do 3 dni”. Zgłoszone Jakubowi przed renderem, odpowiedział „Tak, dokończ”.
- Doszło „czy czas zespołu” i „I co warto dodać”.
- W hooku C whisper słyszy „Poszkodowana właśnie”; w napisach jest „Poszkodowany” jak w skrypcie.
- „za mało z OC sprawcy”: „z” zlewa się z „mało” (whisper: „za małe OC”), w napisach pełna forma.

## Niewykorzystane duble (materiał na inne wersje)

- Hook B, dubel 1 (bliższy skryptowi): 28,45–30,49 + 31,06–33,08 „Dzwonisz do leada ze szkody OC, a po drugiej stronie cisza. Nasze leady odebrały telefon, zanim trafiły do Ciebie.”
- Hook C, 1. zdanie wolniej: 58,39–62,89 „Ubezpieczyciel zaniżył odszkodowanie z tytułu OC.”
- Hook C, 2. zdanie wolniej i bez „to”: 71,23–74,51 „Poszkodowany właśnie teraz szuka kancelarii, która sprawdzi,” (urwane).

## Kadry

Jakub siedzi nisko w kadrze (twarz na ok. 44% wysokości, 19% wysokości kadru), więc „pełny kadr” nie pasuje do wzorca. Kadry: W = zoom 1,30, M = 1,50, C = 1,72, twarz na ok. 33–34% wysokości. Środek twarzy podany osobno dla każdej kwestii w `SEGS` (przesuwa się między dublami o ok. 180 px źródła). Podgląd przed renderem: `podglad_kadrow.py`.

## Grafiki

- Hook kinetyczny: A „SZKODAMI OC?” / „ZA LEADY,” / „ZWERYFIKOWANE” + chip „LEAD BEZ WERYFIKACJI” przy cytacie; B „A TAM CISZA.” / „ODEBRAŁY TELEFON,”; C „ZANIŻYŁ” / „SZUKA KANCELARII,” + pigułki „DO CIEBIE” i „DO KONKURENCJI”.
- Korpus 1–2: plansza „KOGO DOSTARCZAMY” z kartą leada (trzy ptaszki).
- Korpus 3: karta połączenia „Nasz zespół · Dzwonimy do każdej osoby”. Korpus 4: dwa kafelki z ptaszkami.
- Korpus 5: plansza „TWÓJ CRM” (lead ląduje, pigułka „NOTATKA Z ROZMOWY”).
- Korpus 6: karta „PIERWSZE LEADY · do 48 h”. Korpus 7: plansza „ZA CO PŁACISZ”. Korpus 8: chip „KAŻDE ZAMÓWIENIE ✓ GWARANCJA”.
- CTA: przycisk „ZOSTAW KONTAKT ↓” na mówcy + chip „ODDZWONIĘ · ILE I NA KIEDY”. Plansza końcowa: ikona telefonu, tekst, przycisk, bez logo.
- Poglądowe (nie padają dosłownie): nagłówki plansz, podpis „lead z OC”, „LEAD BEZ WERYFIKACJI”, „Rozmowa/telefon · teraz”, forma „Odebrała telefon”.
- Biała koszulka pod napisami: miękkie, owalne przyciemnienie wideo pod strefą napisów (`SCRIM = 0.44` w `kompozycja.py`). Wygląd samych napisów bez zmian.

## Kontrola (wersje z naturalnym głosem)

Wyniki w sekcji „Kontrola eksportu” na końcu pliku.

## Kontrola eksportu (17.11.2026, wersje z naturalnym głosem)

| Wersja | Długość | Głośność | Szczyt | Dźwięk względem `audio/aroll.wav` | Treść (odsłuch kwestia po kwestii) |
|---|---|---|---|---|---|
| HOOK A | 47,53 s | −14,0 LUFS | −1,8 dBFS | 0,00 ms, różnica −47,5 dB | 12 kwestii, bez powtórzeń |
| HOOK B | 44,83 s | −14,0 LUFS | −1,8 dBFS | 0,00 ms, różnica −48,7 dB | 13 kwestii, bez powtórzeń |
| HOOK C | 44,23 s | −14,0 LUFS | −1,8 dBFS | 0,00 ms, różnica −47,3 dB | 13 kwestii, bez powtórzeń |

- `hyperframes check`: 0 błędów w każdej wersji. Jedno ostrzeżenie o kontraście: biały napis na pomarańczowym przycisku (2,5:1), zostawione celowo, bo to paleta adGen.
- Napisy (`waliduj_napisy.py 0.15`): A 10 z 131, B hook 0, C hook 3 flagi. Wszystkie pojedyncze (słowa otwierające zdanie, „czy”, „nie”, błędy rozpoznania krótkiego wycinka), żadnej serii.
- Cięcia A-rollu zgadzają się z EDL co do klatki (detekcja scen w wersji A).
- Głośność kwestii po wyrównaniu: rozrzut 1,6 dB (A), 2,5 dB (B), 2,1 dB (C). Pod planszą końcową cisza (−62 dB).
- Dźwięk w plikach finalnych został podmieniony bez renderu obrazu (`-c:v copy`, AAC 256 kb/s) po dodaniu limitera szczytów w `aroll.py`: pierwszy render z naturalnym głosem miał szczyt −1,4 dBFS, o 0,1 dB ponad limit.
- Napisy do Premiere lub uploadu: `napisy_A.srt`, `napisy_B.srt`, `napisy_C.srt`. Klatki finalnych wersji: `klatki/final_A_sheet.jpg` itd.

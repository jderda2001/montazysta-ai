---
name: feedback-false-starts
description: "Whisper ukrywa falstarty, powtórzone zdania i zająknięcia w dublu; każdy dubel sprawdzaj kawalki.py w obu trybach i rozstrzygaj każdy alarm (Jakub dwa razy sam wyłapał to, co przeoczyłem)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-25T10:31:36.909Z
---

Jakub dwa razy musiał sam zgłaszać potknięcia, które zostawiłem w oddanym filmie:

- IMG_0526 (13.11.2026): falstarty na początku dubli („I każdego ranka dosta…”, „CRM jest wz…”), a dopiero potem pełne zdanie.
- IMG_0591 (18.11.2026): „powtórzyłem i zaciąłem się w niektórych miejscach, przejrzyj i popraw”. W filmie było zdanie powiedziane dwa razy pod rząd („gdzie autor pyta: sukces to szczęście czy umiejętn… gdzie autor pyta…”) oraz zająknięcia w środku zdania (powtórzona sylaba „sukce- cesu”, pauza w środku słowa „do… kładnie”).

**Why:** whisper wygładza zająknięcia i powtórki, a prompt z oczekiwanym tekstem i DTW jeszcze to wzmacniają (powtórzone zdanie wyszło jako jedno, ze słowem rozciągniętym na 1,5 s). W IMG_0591 `kawalki.py` pokazywał powtórkę, ale przeoczyłem ją, czytając 20 kwestii na oko, a zająknięcia z przerwą ok. 0,1 s mieściły się w jednym kawałku.

**How to apply:**
- Przed oddaniem każdego filmu puść `kawalki.py` w obu trybach: zwykłym i `--drobne` (pauzy od 0,09 s). Skrypt w skillu `montaz-rolek` sam oznacza `POWTORKA?` (więcej sylab niż w tekście) i `?` (kawałek spoza tekstu) i wypisuje listę do sprawdzenia.
- Każdy alarm rozstrzygnij osobnym whisperem bez promptu na samym kawałku i drobną obwiednią (`fonemy.py`). Dziwne słowo w kawałku traktuj jako prawdziwe potknięcie, dopóki pomiar nie pokaże inaczej.
- Falstart: kwestia startuje od powtórzenia. Powtórzone zdanie: drugie podejście. Zająknięcie w środku: pole `wytnij` w `SEGS` (`aroll.py`) i zmiana kadru w miejscu cięcia.
- Sklejkę w środku słowa sprawdzam whisperem w trzech kontekstach (kwestia, krótkie okno, z sąsiednimi kwestiami) i po renderze czytam kontrolę eksportu zdanie po zdaniu: pierwsza poprawka IMG_0591 miała „wiedziałem kładnie” i „Napoleon” bez „Hill”, bo zaufałem jednemu testowi.
- Miejsca wątpliwe, których nie ruszam (styl, nie potknięcie), wymieniam mu przy oddaniu. To mój wniosek, on o to nie prosił.

- **Od 24.11.2026 dodatkowo `powtorzenia.py` na całej rolce** (Jakub: „czasem się powtarzam albo poprawiam bardzo szybko… sprawdzenie, czy na pewno nie ma powtórzenia na całej rolce”). Skrypt łapie też powtórzenia na stykach kwestii i powiedziane bez pauzy (porównanie akustyczne; whisper zapisuje takie powtórzenie tylko raz). Każde wskazane miejsce rozstrzygnij z klipu w `analiza/powtorzenia/`.

- **Od 25.11.2026 przebieg mikro w `powtorzenia.py` (restart słowa)**. Jakub po C4538, 13. sekunda: „zacząłem pewien wyraz… pomyliłem się i powtórzyłem go dosłownie pół sekundy później. Takie rzeczy też musimy wyłapywać… zapamiętaj”.
  - Było to „Jed… jeden folder”: 0,16 s przerwy, dołek tylko do −48 dB (po masteringu −27…−36). Kawalki i dwa stare przebiegi tego nie rozcięły, a whisper na całości pisał jedno „Jeden”.
  - Teraz przebieg mikro (dołki poniżej −30 dB od 0,05 s, na głosie po masteringu) i reguła: krótki kawałek (do 0,6 s, 1–2 słowa), a następny zaczyna się od słowa o tym samym początku (min. 3 litery).
  - Kalibracja na C4534–C4538: prawdziwy przypadek wykryty. Fałszywe alarmy to najwyżej 1 na rolkę („Nikt” urwane jako „Nie”, „A jeśli” jako „jeszcze”); każdy rozstrzygam uchem.
  - Jeśli on znajdzie coś jeszcze, dopisz tu i dostrój próg.

Zob. [[skill-montaz-rolek]], [[separate-mic-audio-reels]].

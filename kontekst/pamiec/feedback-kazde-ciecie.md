---
name: feedback-kazde-ciecie
description: "Przed oddaniem każdej wersji kontrola KAŻDEGO cięcia w całym filmie (ciecia.py); pierwsza kontrola 17 zaplanowanych plików 26.11.2026 złapała dwie urwane końcówki słów"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-26T11:30:00.000Z
---

25.11.2026, po zdjęciu HOOK A C4537_v2 (sklejka dwóch podejść na 1,67 s), Personal Brand Manager zlecił kontrolę każdego cięcia w całym filmie, nie tylko w pierwszych 5 s, dla 17 wersji rolek zaplanowanych na 26.11–24.12. Zrobione 26.11.2026 skryptem `scripts/ciecia.py`.

Wynik pierwszej kontroli (154 cięcia w 17 plikach):
- C4538 „Przestań tłumaczyć AI, kim jesteś”, HOOK A 9,20 s i HOOK B 10,53 s (ta sama kwestia): koniec kwestii „…w jakiej firmie pracuję,” ucięty w środku słowa. W nagraniu „pra” 62,86, „c” 62,96–63,04, „uję” 63,06–63,30; `a_out` = 63,14, czyli „-ję” (ok. 0,16 s głosu) za cięciem. Przyczyna: koniec kwestii w `SEGS` = 62,96 (początek „c”), a `koniec_mowy()` nie znalazł ciszy w 0,45 s i wziął zapas `koniec + 0,12 s`.
- IMG_0720 „AI masakra spoko genialne” 19,23 s: „a to jest zajebiste.” bez końcowego „-e”. Fonemy: „s” 72,80–72,86 (dużo przejść przez zero), zwarcie „t” 72,88–72,94 (dołek), samogłoska „e” 72,96–73,06 (głośno, mało przejść). W notatkach projektu to było „westchnienie po zajebiste”, ale ten sam wzór ma „zajebiste” na 91,73/91,81/91,87, więc to koniec słowa. Cięcie było na 72,95.
- Whisper w obu przypadkach pisał całe słowo („pracuję”, „zajebiste”) w każdym oknie: model językowy dopowiada uciętą końcówkę. Złapała to obwiednia nagrania (głos −22 / −29 dB tuż po `a_out` przy mowie −25 / −24 dB).
- Poprawki obok zaplanowanych plików („ - poprawka.mp4”), projekty `C4538_poprawka` i `IMG_0720_poprawka` (koniec kwestii na końcu ostatniej samogłoski + `post`).

**How to apply:**
- Na każdym gotowym pliku (HOOK A i HOOK B): `ciecia.py PLIK.mp4 PLIK.srt --projekt <folder wersji>` obok `poczatek.py`. Oddajesz przy 0 alarmach albo z każdym rozstrzygniętym i opisanym.
- Alarm „głos po `a_out`” rozstrzygaj `fonemy.py` na końcu kwestii, nie whisperem. Słowo po polsku nie kończy się na zwarciu: po „t”/„c” szukaj samogłoski.
- Koniec kwestii w `SEGS` ustawiaj na faktycznym końcu ostatniej samogłoski. Gdy `aroll.py` wypisze „UWAGA koniec_mowy”, sprawdź ten koniec.
- Fałszywe uwagi: „AI” w krótkim oknie jako „Ej, ej”, „Mała/Małe” jako „No a/Nowe”, pisownia („w klucze” = „w Claude'zie”), ciche „mmm” przed słowem (C4537_v2 29,28–29,62), celowe cięcie Klarna („rok temu”, opisane 25.11).

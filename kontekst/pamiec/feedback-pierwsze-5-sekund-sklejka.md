---
name: feedback-pierwsze-5-sekund-sklejka
description: "Hook nie może być sklejony z dwóch podejść tego samego zdania w ciągłej mowie; przed oddaniem pierwsze 5 s każdej wersji słowo po słowie (poczatek.py) — C4537_v2 HOOK A zdjęty ze wszystkich platform 25.11.2026"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-25T21:00:00.000Z
---

25.11.2026 rolka C4537_v2 „Kończę call, oferta już czeka”, plik HOOK A („Przestań pisać oferty po callu. Niech napisze ją rozmowa.”) wyszedł o 18:00 na IG, FB, YT Shorts i TikTok. Jakub zdjął go ze wszystkich platform i podmienił na HOOK B. Jego uwaga (przekazana przez Social Media Managera i Personal Brand Managera): w pierwszych 3 sekundach „coś się powtarza i wygląda źle”. Ten plik nigdy nie wraca.

Co było w pliku (analiza po fakcie, bez odsłuchu przez człowieka):
- 0,00–1,67 s „Przestań pisać oferty po callu.” z trzeciego podejścia (nagranie 15,59 s, plan szeroki).
- 1,67 s cięcie na „Niech napisze ją rozmowa.” z PIERWSZEGO, szybkiego podejścia (nagranie 9,91 s, plan bliższy). W tym podejściu Jakub powiedział całe zdanie jednym ciągiem, bez pauzy po „callu”, a cięcie wypadło 40 ms po starcie głosu, w środku mowy.
- Efekt: po „po callu.” słychać ułamek głoski z drugiego podejścia, whisper od miejsca cięcia pisze „O nich napiszę”, czyli „callu… u niech”. Do tego obraz przeskakuje na inne podejście z inną pozycją głowy, a pod koniec (2,5 s) Jakub patrzy w dół jak po skończonym dublu. Zdanie brzmi i wygląda na sklejone z dwóch prób.

Dlaczego kontrole tego nie złapały:
- `powtorzenia.py` szuka powtórzonych SŁÓW i fraz na całej rolce. Tu powtórzony był ułamek głoski (poniżej 0,1 s), a whisper w każdym dłuższym oknie pisze czyste „Niech”.
- Sklejkę sprawdziłem whisperem w oknach zaczynających się od 0 s (0–4, 0–8, 0–15,6 s). Okno zaczynające się DOKŁADNIE na cięciu daje „O nich” — tego nikt nie sprawdził.
- Ostrzeżenia były w notatkach: w punktach 9,88 i 9,94 whisper słyszał „W ogóle niech” i „bo niech”. Wybrałem punkt pomiędzy, zamiast zrezygnować z tej sklejki.

**How to apply:**
- Hook (i każde zdanie w pierwszych 5 s) bierz z jednego podejścia. Drugą połowę zdania z innego podejścia doklejaj tylko wtedy, gdy w nagraniu przed `a_in` jest wyraźna pauza (dołek poniżej ok. −45 dB przez co najmniej 0,1 s). Gdy zdanie nie wyszło w całości w żadnym podejściu, zrób krótszy hook z jednego podejścia (jak C4537 z 24.11: samo „Przestań pisać oferty po callu.”).
- Przed oddaniem każdej wersji (HOOK A i HOOK B, gotowy MP4): `scripts/poczatek.py PLIK.mp4 PLIK.srt --projekt <folder wersji>`. Skrypt robi transkrypcję 0–5 s ze znacznikami słów i porównuje ją z .srt, transkrybuje okna zaczynające się i kończące dokładnie na każdym cięciu, sprawdza w nagraniu, czy przed `a_in` jest głos i czy tuż przed nim pada to samo, co kończy poprzednią kwestię (sklejka podejść), szuka zamrożeń, powrotu do tej samej klatki i podwójnych napisów oraz zapisuje stykówkę klatek co 0,5 s. Oddajesz przy 0 alarmach albo z każdym alarmem rozstrzygniętym uchem i opisanym przy oddaniu. Stykówkę zawsze obejrzyj.
- Kalibracja 25.11.2026 na 17 plikach (rolki 26.11–3.12 + „45 godzin” + C4537_v2 B): wadliwy HOOK A C4537_v2 daje 3 alarmy (cięcie w mowie, sklejka podejść, „O nich”). Fałszywe alarmy to cięcia celowe w środku zdania (Klarna: wycięte „rok temu”, styk na początku „w”) i pisownia whispera („grogbotów”, „8000$”); rozstrzygasz je uchem.

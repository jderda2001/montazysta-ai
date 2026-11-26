---
name: feedback-okladka-plik
description: "Folder rolki w Eksporty musi mieć okładkę każdej wersji jako plik jpg; 26.11.2026 przy publikacji „AI nie zabierze Ci klientów” jej brakowało"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-26T12:00:00.000Z
---

26.11.2026 Social Media Manager Personal Brand opublikował „AI nie zabierze Ci klientów” (HOOK A) na IG, FB, YT i TikToku i zgłosił: „W folderze nie było pliku okładki („… - okładka.jpg”), więc przy kolejnych rolkach dołączaj okładkę.” Okładki jako pliku nie było też w pozostałych folderach zaplanowanych 23–24.11. Jedyny wzór to „Kończę call” (C4537_v2).

**How to apply:**
- Do każdej wersji plik `<Tytuł>_HOOK A_MM.RR - okładka.jpg` i `<Tytuł>_HOOK B_MM.RR - okładka.jpg` w tym samym folderze co mp4, `.srt` i opisy. Bez nich folder nie jest gotowy do oddania.
- Okładka 1080×1920: klatka z zamkniętymi ustami albo lekkim uśmiechem (kilku kandydatów, nie otwarte usta w pół słowa), hasło tej wersji pod brodą albo nad głową, nigdy na czole i włosach, w strefie bezpiecznej; na jasnym tle ciemna karta pod tekstem.
- Wzór: `wzory/okladka-C4537_v2/` (HyperFrames, `A.html`/`B.html`, tło = klatka z A-rollu z gradingiem). Opis w `projekty/C4537_v2/NOTATKI.md`: napis pod brodą na ciemnej karcie, top 880 px, maks. 680 px szerokości.

**26.11.2026, pierwsza partia (Personal Brand Manager):** okładka „Przestań tłumaczyć AI, kim jesteś” HOOK A zatwierdzona („usta zamknięte, napis pod brodą, czytelny. Ten sam układ trzymaj w kolejnych”). Dorobione okładki do wszystkich wersji w Zaplanowane i do „AI nie zabierze Ci klientów” A/B (16 plików).
- Klatki: `scripts/kandydaci.py <aroll.mp4> <folder> 6` (co 0,1 s, `usta.swift` mierzy otwarcie warg, oczy i yaw; stykówka twarzy do wyboru okiem). Metryka czasem przepuszcza lekko otwarte usta, więc wybór zawsze na stykówce.
- Render: `scripts/okladka.py <klatka.jpg> <broda_y> "<linia 1>" "<linia 2 w mięcie>" <wyjście.jpg>` (karta 34 px pod brodą, font 84 px zmniejszany do 820 px szerokości; wypisuje pozycję karty).
- Hasła z hasła klatki 0 danej wersji, przycięte do 3–5 słów (np. „Przestań tłumaczyć” / „AI, kim jesteś”, „OpenAI płaci” / „do 8000 $” z „do” jak w nagraniu).

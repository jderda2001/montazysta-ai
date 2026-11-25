---
name: feedback-sfx-and-caption-sync
description: User rejected synthesized whoosh SFX and noticed captions drifting from speech; how to handle SFX and caption timing in edits
metadata:
  node_type: memory
  type: feedback
  originSessionId: 86deeb8d-c257-42cc-9214-7efdf8a192fb
  modified: 2026-11-13T13:10:01.879Z
---

Użytkownik ocenił moje syntetyczne whooshe (szum z ffmpeg) jako „chujowe” i niepasujące. Zauważył też, że napisy nie trzymały się mowy.

**Why:** syntetyczne efekty brzmią tanio. Transkrypcja whispera z DTW dla całego zmontowanego pliku rozjeżdżała się o 0,3–1,0 s, bo słowa przechodziły przez cięcia.

**How to apply:**
- Nie generuj efektów dźwiękowych z szumu. Używaj tylko efektów od użytkownika (folder `~/Desktop/Montażysta AI/Muzyka/`) albo zostaw film bez nich.
- Czasy słów do napisów licz osobno dla każdej kwestii, whisperem z `-dtw large.v3.turbo -nfa`. Bez `-nfa` DTW jest po cichu wyłączone i zostają czasy heurystyczne, nawet 0,6 s za wcześnie; tak było w pierwszej wersji IMG_0526.
  - Koniec słowa to t_dtw jego ostatniego tokenu.
  - Start słowa to koniec poprzedniego słowa, przesunięty do t_dtw interpunkcji, końca pauzy albo powrotu głośności.
  - Gotowy skrypt: `projekty/IMG_0526/skrypty/slowa.py`.
  - Kontrola: whisper na odcinku [początek kwestii, koniec słowa + 0,15 s] musi już zawierać to słowo.
- Czasy plansz bierz ze słów i cięć, nie wpisuj ich na sztywno.
- Montuje w Premiere Pro. Gdy będzie chciał sam poprawiać, daj warstwy: ProRes 4444 z alfą + SRT.

Zob. [[adgen-video-style]].

---
name: feedback-cenzura-przeklenstw
description: "Przekleństwa w każdym filmie cenzuruję zawsze: piknięcie w dźwięku, grawlix w napisie, czarny pasek na ustach (monetyzacja YouTube); wzór IMG_0720"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-23T19:11:06.769Z
---

23.11.2026, przy IMG_0720: „do «wyjebania» zacenzuruj i przykryj mi wtedy usta (jak na śmiesznych filmach albo na YouTubie, żeby nie zdejmowali monetyzacji twórcom)”. Zapytany, czy tak ma być w każdym filmie, odpowiedział: „Tak, zawsze”.

**Why:** platformy obcinają zasięgi i monetyzację za przekleństwa; ma to też wyglądać jak zabawny efekt, a nie jak wpadka.

**How to apply:**
- Po transkrypcji wypisz przekleństwa z wybranych kwestii i cenzuruj każde, bez pytania.
- Dźwięk: na czas słowa wycisz głos i daj piknięcie 1 kHz (ok. −18 dBFS, krótkie wejście i wyjście). Wzór: `projekty/IMG_0720/audio/aroll_cenzura.wav`, jako `GLOS` w `kompozycja.py`.
- Napis: grawlix „#@!%&” zamiast słowa, z zachowaniem wyróżnienia.
- Obraz: czarny pasek z „#@!%&” na ustach na czas słowa; pozycja ust z `analiza/twarze.json` i kadru (`crop()` w `aroll.py`).
- Sprawdzenie: whisper na gotowym pliku nie może słyszeć przekleństwa (w IMG_0720 słyszy „do ***”).
- Dotyczy rolek, reklam i long-formów.

Zob. [[skill-montaz-rolek]], [[repo-montazysta-ai]].

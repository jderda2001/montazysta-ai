---
name: longform-youtube-img0529
description: "Pierwszy long-form na YouTube (IMG_0529, 13.11.2026, seria o zautomatyzowanej firmie): jak był zrobiony, pułapki i co czeka na potwierdzenie"
metadata:
  node_type: memory
  type: project
  originSessionId: 901d293e-32a2-4c5b-8f18-cad6c655b493
  modified: 2026-11-13T15:18:55.725Z
---

Odcinek „Zautomatyzowany dział growth” jest pierwszym z serii o zautomatyzowanej firmie (adGen). Kolejny odcinek ma dotyczyć innego działu. Projekt: `/Users/jd/Montażysta AI/projekty/IMG_0529/`, opis w `NOTATKI.md`.

**Materiał**
- Wideo z iPhone'a: 4K 60p poziomo, ok. 20 min.
- Dźwięk z mikrofonu: Dyktafon na Macu, dwa pliki („Salon kosmetyczny Dreams 7/8.m4a”, nazwy nadane automatycznie od lokalizacji). Ten sam plik leży też w `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/` pod datą i godziną.
- Pierwsze ok. 2 min wideo to przygotowanie: odtworzenie rolki o Kaji i próba mikrofonu.

**Pułapki**
- Nagranie z Dyktafonu może się urwać i zapętlić bufor 0,5 s na końcu („byłem, byłem, byłem…”). Sprawdzaj końcówkę każdego pliku autokorelacją.
- Dwa pliki z tej samej sesji różnią się barwą (o kilka dB). Sidon wyrównuje to prawie całkowicie.

**Pipeline long-form**
- Ujęcia 4K renderowane osobno do HEVC.
- Grafiki i napisy jako osobne warstwy HyperFrames: ProRes 4444 z alfą, 4K przez DPR 2.
- Składanie w oknach po 60 s.
- Overlay po `-ss` wymaga `setpts=PTS-STARTPTS`, inaczej pierwsza klatka wychodzi bez grafiki.

**Why:** to wzór na kolejne odcinki serii.
**How to apply:**
- Zacznij od skryptów z IMG_0529/skrypty (`montaz.py`, `audio.py`, `napisy.py`, `kompozycja.py`, `render_warstwy.py`, `finalny.py`).
- Przy oddaniu dopytaj o rzeczy oznaczone w NOTATKI.md jako „do potwierdzenia”, m.in. nazwę aplikacji (Grok?).

**Stan na 13.11.2026, wieczór**
- Ocena odcinka: „zajebiste!!!!”.
- Logo aplikacji przy „Grok Bot” i biały tekst „Subskrybuj” są w eksporcie.
- Wszystko do publikacji w `Eksporty/YouTube/2026-11-13 Zautomatyzowany dział growth/`, a 3 rolki promo w jego podfolderze `Rolki promo/`.
- Muzyka lo-fi jest w eksporcie (`render/odcinek_v3.mp4`, `skrypty/muzyka.py`). Poziom muzyki zatwierdzony („Pasuje”). Stare rendery v1 i v2 usunięte za jego zgodą. Eksport to twardy link do `render/odcinek_v3.mp4`.

Zob. [[feedback-youtube-poziomo]], [[separate-mic-audio-reels]], [[feedback-longform-3-rolki]].

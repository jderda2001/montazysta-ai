---
name: separate-mic-audio-reels
description: "User films reels on iPhone but records voice separately on a mic and asks to \"podmień audio\"; how to sync and what organic reels look like"
metadata:
  node_type: memory
  type: project
  originSessionId: a055733e-41e0-4da2-ad7a-117372a42b88
  modified: 2026-11-13T14:18:20.342Z
---

Od 2026-11-13 użytkownik nagrywa też organiczne rolki (np. o swoim agencie AI „Kaja”, bot sprzedażowy). Obraz kręci iPhone'em (1080×1920 po obrocie). Dźwięk nagrywa osobno mikrofonem stojącym na biurku i dostarcza jako .m4a w `~/Desktop/Montażysta AI/Nagrania /` (folder ze spacją na końcu nazwy). Prośba „podmień audio” oznacza: to samo wykonanie, wymień dźwięk telefonu na nagranie z mikrofonu.

- Synchronizacja: korelacja krzyżowa dźwięku telefonu z nagraniem z mikrofonu (`projekty/IMG_0526/skrypty/sync.py`), potem kontrola każdej kwestii w gotowym A-rollu (`sprawdz_sync.py`). W IMG_0526 offset wynosił 7,37 s, a dryf był pomijalny.
- Rolka organiczna różni się od reklamy: jedna wersja, CTA „zaobserwuj” zamiast „zostaw kontakt” (od 24.11.2026, zob. [[feedback-cta-obserwuj]]), plansza końcowa z wezwaniem do obserwowania, bez logo adGen. Wszystkie duble z nagrania (warianty hooków i CTA) wypisuję w NOTATKI.md jako materiał na wersję B.
- Wzorcowe skrypty do kolejnych filmów są w `projekty/IMG_0526/skrypty/` i są nowsze niż te w IMG_0361:
  - `aroll.py`: obraz i dźwięk z dwóch plików;
  - `kawalki.py`: wykrywanie falstartów;
  - `slowa.py`: czasy słów z DTW;
  - `sidon_infer.py` i `studio.py`: głos studyjny i głęboki, domyślny od 13.11, zob. [[feedback-voice-sound]];
  - `kompozycja.py`.

**Why:** pierwszy taki film (IMG_0526, 2026-11-13) przyszedł jako dwa osobne pliki.
**How to apply:** gdy dostaniesz osobno wideo i audio, zsynchronizuj je korelacją, a nie na oko. Skrypty skopiuj z IMG_0526. Zob. [[adgen-video-style]], [[feedback-sfx-and-caption-sync]].

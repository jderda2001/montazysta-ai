---
name: feedback-safe-zone
description: Rolki i reklamy pionowe mają trzymać strefę bezpieczną (safe zone) z dwóch szablonów od Jakuba; napisy i animacje bywały za wysoko i za szeroko
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1cd9d117-33dd-4f3b-b958-6ab5bf04fe4c
  modified: 2026-11-18T09:05:47.732Z
---

18.11.2026, przy zleceniu rolki PerfOS (IMG_0597), Jakub napisał: „Zaktualizuj też w skillu safe zone (napisy i animacje czasem są za wysoko bądź za szeroko – masz tutaj templatki, które znalazłem w necie)” i dołączył dwa szablony: Instagram Reels safe zone (góra 14% / 269 px, dół 35% / 672 px, boki 6%) oraz szablon Jona Loomera pod Reels i Stories.

**Why:** treść wchodziła pod interfejs Instagrama. Moja interpretacja, nie jego słowa: „za wysoko” to nakładki na 96–150 px (ucięte też w podglądzie 4:5), „za szeroko” to napisy do 950 px szerokości, które sięgały pod przyciski po prawej.

**How to apply:**
- Strefa to część wspólna obu szablonów, kadr 1080×1920: y 270–1245, x 70–1010, od 860 px w dół prawa krawędź 885 px, od 1145 px 850 px. Stałe `SAFE` w `scripts/kompozycja.py` skilla montaz-rolek, opis w `references/styl.md`, punkt 8.
- Napisy zostają na 1120 px, ale mają 620 px szerokości (frazy do ok. 20 znaków). Wygląd bez zmian.
- Przed każdym renderem rolki uruchom `skrypty/strefa.py`: ma wyjść zero klatek z treścią poza strefą.
- Dotyczy rolek, reklam adGen i rolek promo z long-formu. Long-form 16:9 ma osobne zasady.
- Pierwszą rolkę zrobioną w strefie (IMG_0597: napisy 620 px, nakładki nad napisami) ocenił 18.11.2026: „Mega spoko… jak najbardziej akceptuję”. O szerokości napisów ani pozycji nakładek nie powiedział nic osobno.

- 18.11.2026 Jakub poprosił, żeby „też rolkę o Thielu” przerobić pod strefę (IMG_0591, 4 pliki, zrobione). Przy niskim kadrze (broda na 62–76% wysokości) napisy w strefie wymagają zbliżenia dobranego z pomiaru twarzy: `scripts/twarze.py` plus `kadr()` w `aroll.py`; zapytany, czy zostawić bliższą twarz, odpowiedział „Zostaw” (18.11.2026). Zasada na przyszłość: przy każdej nowej rolce z niskim kadrem zmierz twarz, zanim ustawisz napisy.

Zob. [[skill-montaz-rolek]], [[feedback-reel-style-approved]], [[perfos-rolki-branding]].

---
name: feedback-paleta-marki
description: "Paleta personal brandu Jakuba w filmach i miniaturach — czerń, biel, ciemny szary plus akcent, głównie #00E5A0; reklamy adGen zostają pomarańczowe #ff7018"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-17T15:06:56.818Z
---

17.11.2026 Jakub: jego personal brand opiera się na czerni, bieli i ciemnym szarym, a akcenty mają zależeć od tego, o czym mówi. Główny akcent to „limonkowy” `#00E5A0` (jego nazwa; w praktyce to miętowa zieleń, liczy się hex). Kazał wpisać to mocno do skilla `montaz-rolek`, bo to montażysta stricte pod personal brand.

Tego samego dnia doprecyzował: „adGen zostaje pomarańczowy”. Reklamy adGen (`Eksporty/Reklamy adGen`) dalej mają akcent `#ff7018`, biały tekst na akcencie i zielony „zrobione” `#3ddc84`.

**Why:** spójność marki osobistej. Pomarańcz to kolor agencji adGen, a nie jego personal brandu, więc zostaje tylko w reklamach adGen (to drugie zdanie to mój wniosek, on powiedział tylko, że adGen zostaje pomarańczowy).

**How to apply:**
- O palecie decyduje marka, nie format: rolki organiczne, long-form i rolki promo to personal brand (`#00E5A0`); reklama adGen to pomarańcz. Gdy z nagrania nie wynika, czyje to, zapytaj przed kompozycją.
- Personal brand: grafiki, napisy i plansze z czerni `#0f1012`, bieli i ciemnych szarości. Kolor tylko jako akcent na sensie wypowiedzi (kluczowe słowo, liczba, kafelek, przycisk).
- Domyślnie `#00E5A0`, jeden akcent na film. Inny akcent tylko, gdy wymaga tego temat, i wtedy mów o tym przy oddaniu. To moja interpretacja „akcenty zależnie od tematu”; Jakub nie podał listy kolorów pod tematy.
- Na `#00E5A0` zawsze ciemny tekst i ikony (`#0f1012`), bo biały ma kontrast 1,6:1. Na pomarańczu adGen tekst zostaje biały.
- W skillu paletę wybiera `MARKA` (`"personal"` / `"adgen"`) i słownik `PALETY` w `scripts/kompozycja.py`. Szablony long-formu w `projekty/IMG_0529/skrypty/` też są już w tej palecie (`paleta.py`); wyrenderowany odcinek IMG_0529 został pomarańczowy, a oryginalne skrypty są w `skrypty/_przed_paleta_2026-11-17/`.
- Miniatury YouTube też w tej palecie („Tak, miniatury też”, 17.11.2026): w skillu `miniatury` akcent ustawia `AKCENT` w `scripts/sklad.py`. Okulary Jakuba zostają pomarańczowe, to jego wizerunek. Zob. [[skill-miniatury]].
- Nierozstrzygnięte 17.11.2026: czy ma własną listę akcentów pod konkretne tematy.

Zob. [[feedback-reel-style-approved]], [[adgen-video-style]], [[skill-montaz-rolek]].

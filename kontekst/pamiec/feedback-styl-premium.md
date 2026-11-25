---
name: feedback-styl-premium
description: "Od 24.11.2026 obowiązuje styl „premium”: 60 kl./s, max 2 sceny na 30 s, płynne zoomy, jasne/szklane wstawki z kurtyną, Liquid Glass CTA i plansze końcowe w rotacji; wzorce w skillu references/wzorce"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-24T16:02:45.620Z
---

24.11.2026 Jakub uznał dotychczasowe animacje za „AI slopowe” i pokazał dwie rolki referencyjne. Po trzech próbkach nowy styl zatwierdził słowami „zajebiste!!!!… daj eksport tego full, wrzucę na IG… zapisz całe referencje”.

**Why:** chce efektu premium: mniej grafik, płynniej, czysto, jak u najlepszych twórców i w interfejsach Apple.

**How to apply:**
- Zasada 10 w SKILL.md skilla montaz-rolek. Rolki wzorcowe i zdjęcie profilowe leżą u użytkownika: `~/Desktop/Montażysta AI/Referencje i wytyczne/Rolki wzorcowe/` i `…/Zdjęcie profilowe/avatar.jpg`, a nie w repo (decyzja Jakuba z 24.11.2026). Przed montażem obejrzyj rolki wzorcowe.
- Ruch:
  - 60 kl./s (A-roll i `--fps 60`);
  - najwyżej 2 złożone sceny na 30 s;
  - akcenty robią płynne zoomy `zoom()`;
  - bez sprężyn; przejście domyślnie przenikanie lub kurtyna.
- Wstawki:
  - `panel(..., jasna=True)` (złamana biel, ciemny tekst, białe karty) albo `szklo=True` (matowe szkło nad rozmytym A-rollem);
  - napisy na nich ciemne z miętowym zakreślaczem.
- CTA i plansze końcowe z `scripts/cta.py` w Liquid Glass:
  - 5 CTA i 5 plansz, wszystkie w rotacji („Wszystkie 5”);
  - każda rolka bierze inny wariant niż poprzednia; użyte zapisuj w dzienniku.
  - CTA „zaobserwuj” z lokalnej kopii poza repo, zob. [[feedback-cta-obserwuj]].
- Zdjęcie profilowe: `foto = cta.przygotuj_avatar(P / "hf")`.

Zob. [[skill-montaz-rolek]], [[feedback-reel-style-approved]], [[feedback-roznorodnosc-grafik]], [[repo-montazysta-ai]].

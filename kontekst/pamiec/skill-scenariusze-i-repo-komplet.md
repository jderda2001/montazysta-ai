---
name: skill-scenariusze-i-repo-komplet
description: "25.11.2026: skill scenariusze-rolek (format, zasady, przykłady) i decyzja, że w repo montazysta-ai ma być dosłownie wszystko, bo montaż przejmuje osobny agent"
metadata:
  type: project
---

25.11.2026 Jakub: „Czy całe GitHub repo jest zaktualizowane dosłownie wszystko wraz ze strukturą na przykład tworzenia scenariuszy? Bardzo proszę, żeby dokładnie wszystko, cały ten kontekst i cały ten skill był napełniony, bo przenoszę po prostu cię do osobnego agenta, który będzie montował wszystkie moje materiały”.

**Why:** nowy agent nie ma tej pamięci ani historii rozmów; wszystko, czego się nauczyłem, musi być w repo.

**How to apply:**
- Scenariusze: skill `skills/scenariusze-rolek/` (SKILL.md z zasadami z uwag Jakuba, przykłady paczek z 24.11.2026), link w `~/.claude/skills/scenariusze-rolek`, instalator go podpina.
- Kontekst: `kontekst/README.md` (kim jest Jakub, foldery, od czego zacząć) i `kontekst/pamiec/` (kopia całej tej pamięci). Po każdej nowej notatce w pamięci skopiuj ją też do `kontekst/pamiec/` i dopisz do `INDEKS.md`.
- Wzory: `wzory/C4527–C4529`, `wzory/C4534–C4538` (najnowszy: C4538), narzędzia `przebieg.sh`, `przerwy.py`, `oczy.sh` w skillu.
- Wcześniejsze zastrzeżenia „nie wpisuj do skilla/repo” (CTA, opisy, miniatury long-form, scenariusze) są nieaktualne.

Zob. [[repo-montazysta-ai]], [[feedback-cta-obserwuj]], [[skill-montaz-rolek]].

---
name: skill-montaz-rolek
description: Skill montaz-rolek w ~/.claude/skills to główne źródło wiedzy o montażu dla Jakuba; po każdym filmie dopisuj ocenę do jego dziennika
metadata:
  node_type: memory
  type: reference
  originSessionId: a055733e-41e0-4da2-ad7a-117372a42b88
  modified: 2026-11-13T14:49:36.885Z
---

13.11.2026 użytkownik poprosił o skill, żeby montaż z czasem był coraz lepszy. Skill leży w `~/.claude/skills/montaz-rolek/`:
- `SKILL.md`: zasady i proces;
- `references/styl.md`, `pipeline.md`, `narzedzia.md`, `dziennik.md`;
- `scripts/`: szablony z IMG_0526 plus `waliduj_napisy.py` i `kontrola_eksportu.py`.

Kopię do zainstalowania w profilu dostał jako plik `montaz-rolek.skill`.

**How to apply:**
- Przy każdym montażu korzystaj ze skilla.
- Po filmie dopisz do `references/dziennik.md` jego ocenę (pochwały, krytykę, statystyki z Instagrama), a nowe pułapki i parametry do odpowiedniej referencji. To jest mechanizm „uczenia się”, o który prosił.
- Notatki w pamięci ([[feedback-reel-style-approved]], [[feedback-voice-sound]], [[feedback-false-starts]]) zostają jako skrót, ale szczegóły trzymaj w skillu.

---
name: repo-montazysta-ai
description: Skille montaz-rolek i miniatury żyją od 20.11.2026 w prywatnym repo jderda2001/montazysta-ai (wspólne z Maciejem); po każdej zmianie w skillu commit + push
metadata:
  node_type: memory
  type: project
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-20T16:36:58.086Z
---

20.11.2026 Jakub poprosił o repo na GitHubie z całym systemem montażu, „bo chcę go dać Maciejowi, wspólnikowi… żeby montował w ten sam sposób” dla adGen i PerfOS. Wybrał wspólne repo, a nie jednorazową kopię. Kazał też wrzucić muzykę i SFX do repo, a zaproszenie Macieja wysyła sam.

- Repo: `jderda2001/montazysta-ai` (prywatne), lokalnie `~/Montażysta AI/montazysta-ai/`.
- `~/.claude/skills/montaz-rolek` i `~/.claude/skills/miniatury` to linki symboliczne do `skills/` w repo. Oryginały sprzed zmiany leżą w `~/.claude/skills-kopia-2026-11-20/`.
- W repo są też:
  - `ZASADY.md`: reguły z tej pamięci, przepisane dla obu osób; u Macieja podpięte jako `~/Montażysta AI/CLAUDE.md`;
  - `wzory/`: skrypty, notatki, branding i szkielet hf projektów;
  - `zasoby/Muzyka/`: muzyka i SFX, z których korzystają `sfx.py` i `muzyka_podklad.py`, z fallbackiem na pulpit;
  - `instalacja/zainstaluj.sh`.

**Why:** Maciej ma montować tak samo, a lekcje z obu stron mają do siebie trafiać.

**How to apply:**
- Przed montażem zrób `git pull --rebase --autostash` w repo.
- Po każdej zmianie w skillu (dziennik, referencje, skrypty) zrób commit i `git push`.
- Nową ogólną zasadę od Jakuba dopisz także do `ZASADY.md`, nie tylko do pamięci.
- Gdy powstanie nowy wzorcowy projekt, skopiuj jego `skrypty/` i `NOTATKI.md` do `wzory/`.
- Zob. [[skill-montaz-rolek]], [[skill-miniatury]].

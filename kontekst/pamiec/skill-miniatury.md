---
name: skill-miniatury
description: "Skill miniatury w ~/.claude/skills to osobny proces do miniatur YouTube (skan klatek, wycinanie, skład, kontrola); klucz kie.ai leży w ~/.config/kie/api_key"
metadata:
  node_type: memory
  type: reference
  originSessionId: 87183a9e-13b3-488a-8ba7-63e994ca44d9
  modified: 2026-11-14T11:34:56.004Z
---

14.11.2026 Jakub poprosił o powtarzalny skill do miniatur z najciekawszych fragmentów filmu i z klatek, na których dobrze wychodzi. Skill leży w `~/.claude/skills/miniatury/`:
- `SKILL.md`: zasady i proces (12 kroków);
- `references/koncepcje.md`, `styl.md`, `narzedzia.md`, `dziennik.md`;
- `scripts/mini.py` (skan, ranking, dopracowanie klatki, wycinanie, render, kontrola, eksport), `sklad.py` (szablon składu 3 wariantów), `kie.py`, `wizja.swift` (Apple Vision, kompiluje się sam do `~/.cache/miniatury`).

Wzorcowy projekt: `/Users/jd/Montażysta AI/projekty/IMG_0529/miniatury/`. Eksport: `Eksporty/YouTube/<RRRR-MM-DD Tytuł>/Miniatury/`.

Klucz kie.ai dał 14.11.2026 „do generowania elementów graficznych”. Leży w `~/.config/kie/api_key` (prawa 600), a nie w skillu. Do kie.ai wysyłam tylko tekst promptu. Zdjęć Jakuba tam nie wysyłam bez pytania: to moja ostrożność, a nie jego wyraźny zakaz.

**How to apply:**
- Miniatury rób zawsze przez ten skill.
- Jego ocenę i wynik testu A/B z YouTube Studio dopisuj do `references/dziennik.md`. To mechanizm uczenia się, taki sam jak w [[skill-montaz-rolek]].

Zob. [[feedback-miniatury-ab]], [[feedback-eksporty-porzadek]], [[video-tools-setup]].

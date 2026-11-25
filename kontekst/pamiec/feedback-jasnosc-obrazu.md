---
name: feedback-jasnosc-obrazu
description: Jakub uznał A-roll za za ciemny (IMG_0688); przed gradingiem mierz jasność, ciemne nagrania rozjaśniaj zamiast przyciemniać
metadata:
  type: feedback
---

20.11.2026, po rolce IMG_0688 („Agent AI w pół roku”), Jakub: „dałeś za ciemny obraz”.

**Why:** nagranie w ciemnym pokoju z zielonym LED miało średnią jasność 48/255, a standardowy grading ze skilla (gamma 0,96, kontrast 1,08, winieta PI/5) zbił ją do 30–35. Moja interpretacja: grading był dobrany pod jasne nagrania z IMG_0526 i stosowałem go bez pomiaru.

**How to apply:** przed renderem A-rollu zmierz YAVG kilku klatek po kadrowaniu (`signalstats`). Przy ciemnym źródle (poniżej ok. 55) daj `eq=contrast=1.04:saturation=1.08:gamma=1.34:brightness=0.015` i winietę `PI/8`, cel ok. 60–70. Opis w skillu montaz-rolek, `references/styl.md`, punkt 6. Ocena jaśniejszej wersji czeka.

Zob. [[skill-montaz-rolek]], [[perfos-rolki-branding]].

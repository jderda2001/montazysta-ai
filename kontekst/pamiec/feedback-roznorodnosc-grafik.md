---
name: feedback-roznorodnosc-grafik
description: Jakub chce różnorodnych przejść i grafik (biblioteka 20–30 szablonów „à la b-roll”) oraz subtelnych efektów dźwiękowych pod animacje
metadata:
  type: feedback
---

17.11.2026, po zaakceptowanej rolce IMG_0576 („a tak to już super”) Jakub dodał jedną uwagę: przejścia względem animacji są „bardzo generyczne” i „bardzo często są używane te same rzeczy”. Poprosił, żebym poszukał szablonów i skilli tak, żeby mieć 20–30 grafik „à la b-roll” do wyboru. Chce też subtelnych efektów dźwiękowych: delikatny dźwięk, gdy wyskakuje napis, i „shhh” (miękki swoosh), gdy ładuje się albo animuje wykres.

**Why:** powtarzalne wejścia plansz i te same chipy sprawiają, że rolki wyglądają jak z szablonu. Dźwięk ma podbijać ruch, ale delikatnie.

**How to apply:**
- Przed wyborem grafik czytaj `~/.claude/skills/montaz-rolek/references/biblioteka.md` i oglądaj arkusze podglądów. Biblioteka (ok. 50 szablonów z katalogu HyperFrames, w palecie marki) leży w `~/.claude/skills/montaz-rolek/biblioteka/`, a `mount()` w szablonie kompozycji je wstawia.
- Kolejne plansze nie wchodzą tym samym przejściem (`panel()` rotuje: iris, wipe, zoom, diag, slide, blur), ten sam szablon grafiki najwyżej dwa razy w rolce i nigdy pod rząd.
- Efekty dźwiękowe: prawdziwe próbki z darmowych bibliotek, nigdy generowane z szumu (zob. [[feedback-sfx-and-caption-sync]]). 17.11.2026 zgodził się na pobranie („Tak, pobierz”): w `~/Desktop/Montażysta AI/Muzyka/SFX/` są paczki Kenney (CC0) i 19 plików z Mixkit, a `scripts/sfx.py` w skillu miksuje je pod głos. Próbkę A/B (`projekty/IMG_0576/ab/sfx/`) ocenił 17.11.2026: „Jest dobrze”, więc poziomy z `sfx.py` (pyknięcia ok. −20 dBFS, swooshe −21, „shh” −24) są zatwierdzonym punktem wyjścia.
- Poziomy z rozpoznania (do weryfikacji uchem Jakuba): tiki i pyknięcia 14–20 dB pod głosem, swooshe 18–24 dB, szczyt swoosha na trafieniu obrazu, najwyżej 8–12 dźwięków na minutę, po 3–4 warianty każdego rodzaju.
- 18.11.2026 zatwierdził cztery własne szablony b-roll w bibliotece skilla (`pipeline-kanban`, `line-scrub-card`, `tick-slider`, `dot-heatmap`): „wszystkie super, można używać od dziś w rolkach”. Używać na równi z resztą biblioteki; w polu strefy bezpiecznej montować przez `mount(..., pole=POLE_STREFY)`.

Zob. [[feedback-reel-style-approved]], [[skill-montaz-rolek]].

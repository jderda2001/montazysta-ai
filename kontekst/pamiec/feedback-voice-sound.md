---
name: feedback-voice-sound
description: "Brzmienie głosu w filmach — od 17.11.2026 naturalny głos z mikrofonu, bez AI (Sidon) albo z dużo mniejszym filtrem; wariant C tylko na prośbę"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a055733e-41e0-4da2-ad7a-117372a42b88
  modified: 2026-11-17T16:34:18.848Z
---

17.11.2026, po pierwszej wersji rolki IMG_0576 (głos przez Sidon + łańcuch radiowy) Jakub napisał: „za bardzo używasz voice enchancer ai (już kupiłem dobre mikrofony także bez tego, albo z dużo mniejszym filtrem też będzie super działać)”.

**Why:** ma teraz dobre mikrofony (w IMG_0576 krawatowy podpięty do iPhone'a), więc AI odbudowujące mowę przestało być potrzebne i było dla niego słyszalnie za mocne. Wcześniejszy wybór wariantu C z 13.11.2026 dotyczył nagrań mikrofonem stojącym pół metra od ust, z pokojem i „pudłem” w 300–450 Hz.

**How to apply:**
- Domyślnie głos naturalny: dźwięk z mikrofonu po lekkim masteringu (highpass 70 Hz, kompresja 2,5:1, −14 LUFS), czyli `audio/aroll.wav` z `aroll.py`. W skillu `montaz-rolek` to już domyślne `GLOS`.
- Sidon i łańcuch radiowy (wariant C, `studio.py`) tylko gdy sam o to poprosi albo nagranie jest wyraźnie złe, i wtedy mów mu o tym przy oddaniu. Dotyczy też long-formu (szablony IMG_0529 nadal mają tam Sidon).
- Jeśli kiedyś zechce „trochę” obróbki, zaczynaj od delikatnego EQ, a nie od AI. To mój wniosek z „dużo mniejszym filtrem”, on nie doprecyzował.
- Zmiany brzmienia nadal porównuj A/B przy tej samej głośności.

Zob. [[skill-montaz-rolek]], [[separate-mic-audio-reels]], [[video-tools-setup]].

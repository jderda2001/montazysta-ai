---
name: feedback-agenci-model-i-effort
description: "Przy zlecaniu pracy agentom dobieraj model i effort do złożoności zadania (nie Fable tam, gdzie wystarczy Sonnet), bez straty jakości"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-18T08:49:46.036Z
---

18.11.2026 Jakub: „Pamiętaj, że gdy zlecasz jakąś pracę agentom, dostosowuj ich model językowy oraz effort do złożoności zadania (tak aby nie palić bez sensu tokenów na Fable przy taskach, które może zrobić Sonnet), oczywiście nie może to wpłynąć na jakość pracy.”

**Why:** dwa rozpoznania w sieci (szablony, biblioteki SFX) puściłem 17.11.2026 na domyślnym, najdroższym modelu, choć to było wyszukiwanie i streszczanie. Tokeny są jego kosztem i limitem (tego samego dnia skończył mu się limit użycia w trakcie montażu).

**How to apply:**
- Przy każdym `Agent` (i w workflow) ustaw `model` świadomie: wyszukiwanie w sieci, czytanie dokumentacji, zbieranie list, proste przeglądy plików i mechaniczne przeróbki idą na `sonnet` (albo `haiku`, gdy to czysta ekstrakcja); najmocniejszy model zostaje do zadań wymagających oceny, projektowania albo trudnego debugowania.
- `effort` też dopasuj do zadania, zamiast zostawiać domyślny, jeśli zadanie jest proste.
- Jakość ma pierwszeństwo: gdy tańszy model mógłby coś przeoczyć (np. ocena falstartów, decyzje montażowe), zostaje mocniejszy albo robię to sam.
- Zanim w ogóle zlecę: kilka wywołań narzędzi robię sam, bez agenta.

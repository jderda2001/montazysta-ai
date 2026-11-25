---
name: feedback-logika-i-przejscia
description: Rolkę składam według logiki wypowiedzi i scenariusza (nie tylko ostatni dubel); dwie sceny pod rząd tylko przenikaniem; liczniki bez widocznego 0000 (24.11.2026)
metadata:
  node_type: memory
  type: feedback
  originSessionId: 19183056-dbe1-450c-9478-38de5a3a8498
  modified: 2026-11-24T22:55:07.451Z
---

24.11.2026, po paczce 5 rolek (C4534–C4538), Jakub: „składaj całą rolkę wedle logiki całej tej wypowiedzi i scenariuszy… czasami zauważyłem, że to się wywala i jeśli chodzi o rolkę o OpenAI, tam też się to zbugowało”.

**Why:** w rolce o OpenAI były trzy błędy:
- Wziąłem ostatni dubel „Na razie tylko w USA, ale myślę, że to kwestia czasu”, który gryzł się z końcówką „U nas tego jeszcze nie ma”.
- Między dwiema planszami pod rząd jasna zjeżdżała w górę, a druga dopiero wchodziła. Przez ok. 0,5 s mignęła twarz ze starym napisem.
- Licznik pokazywał „0000 $”, zanim się zakręcił.

**How to apply:**
- Przed cięciem przeczytaj wybrane kwestie jako całość i porównaj ze scenariuszem: czy nic się nie powtarza, nie wyklucza i nie pada w złej kolejności. Gdy ostatni dubel psuje sens (albo zawiera błąd faktyczny, np. „rok temu” w Klarnie), weź wcześniejszy pełny dubel albo wytnij wtrącenie.
- Dwie sceny pod rząd (mniej niż ok. 1 s twarzy między nimi): pierwsza `fade_out=False, extend=0.75`, druga `wejscie="fade"` i jasna, żeby przenikała się nad pierwszą. Nigdy kurtyna w górę i od razu następna plansza.
- Licznik (`wheel`/`roll`) wchodzi razem z liczeniem (karta na 0,35 s przed liczbą), nigdy nie stoi na zerach.

Zob. [[feedback-napiecie-i-tempo-ciec]], [[feedback-styl-premium]], [[feedback-false-starts]].

# C4538 „Przestań tłumaczyć AI, kim jesteś” (skrypt 5 z „5 scenariuszy – AI i biznes”)

Montaż 24.11.2026. Wersje: hook A (34,3 s), hook B (`hookB/`, 35,7 s).

## Cięcia
- Hook A: 11.34 „Przestań za każdym razem tłumaczyć AI, kim jesteś i jak pracujesz.”
- Hook B: 30.93 „Jeden plik sprawił, że AI pisze maile i oferty dokładnie tak samo, jak ja bym to robił.” (trzy wcześniejsze podejścia od 27.4 wycięte).
- Falstarty: 55.2 „Większość ludzi przy każdej wycenia wpłat” → 57.47; 104.96 „AI sam po niego sięgnie, kiedy po…” → 107.37.
- Pominięte: duble „Większość ludzi…” 38–54 s, wpadka 73.9, „Jeden folder” 90.0, „Ja mam tak…” 129–135.
- Kontrole: kawalki.py (oba tryby), powtorzenia.py: 0.

## Grafiki
- Hasło: A „Przestań tłumaczyć AI, kim jesteś.”, B „Jeden plik. AI pisze jak ja.”
- Scena A (szkło) 3,7–10,5 s: „Nowy czat · ten sam prompt, znowu”, linie „Kim jestem / Co robię / W jakiej firmie pracuję / Jakie są ceny”, „Wklejasz przy każdej wycenie…”.
- Scena B (jasna) 10,6–20,1 s: logo Claude „albo” Grok Bot, „skill: wycena · jeden folder”, Twoje stawki / Twój styl / Szablon wyceny, „AI sięga po niego samo”.
- Najazdy: „Piszesz jedno zdanie”, „a nawet montaż tej rolki”.
- Plansza `jasna` w trybie obserwuj od „koniecznie zaobserwuj”: „SKILL”, „Pokazuję, jak robić to w firmie”.

## Poprawka 25.11.2026 (Jakub: „w 13/14 sekundzie… zacząłem wyraz, pomyliłem się i powtórzyłem pół sekundy później”)
- „Jeden folder” zaczynał się od falstartu „Jed…” (94.00–94.30, pauza 0,16 s). Kwestia startuje teraz od 94.45 („jeden folder”), sprawdzone whisperem.
- Kawalki.py i powtorzenia.py tego nie łapały (za krótki i za płytki dołek, whisper pisał jedno „Jeden”). Dodany przebieg mikro i reguła „restart słowa” w powtorzenia.py: na starej wersji wykrywa to miejsce (13,08 s).

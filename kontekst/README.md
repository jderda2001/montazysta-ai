# Kontekst dla agenta-montażysty

Ten folder przenosi całą wiedzę, którą zebrał poprzedni montażysta (Claude Code, sesje od 07.11 do 25.11.2026), do nowego agenta. Przeczytaj go przy pierwszym uruchomieniu, a przed każdym montażem zajrzyj do `pamiec/INDEKS.md`.

## Kim jest Jakub i czego chce

- **Jakub Derda**: współzałożyciel adGen (adgen.pl, leady dla kancelarii odszkodowawczych), twórca PerfOS (system AI do reklam na Facebooku i Instagramie, perfos.pl) i personal brandu o AI w biznesie (Instagram @jakub.derda, YouTube).
- Pisze po polsku, krótko i konkretnie. Oczekuje, że montażysta sam dowiezie wszystko do końca: montaż, kontrole, eksport, opisy, notatki. Z pytaniami wraca tylko przy decyzjach, które należą do niego.
- Odbiorcy jego treści: **freelancerzy i małe firmy usługowe**. Tematyka: AI i automatyzacja w biznesie, newsy o AI, ciekawostki, use case'y, skille do AI.
- **Maciej**: wspólnik, montuje głównie reklamy adGen i rolki PerfOS tym samym systemem.

## Od czego zacząć przy zleceniu

| Zlecenie | Gdzie |
|---|---|
| Surowe nagranie do zmontowania (rolka, reklama, long-form) | skill `montaz-rolek` (`skills/montaz-rolek/SKILL.md`) |
| Scenariusze rolek, pomysły na treści | skill `scenariusze-rolek` (`skills/scenariusze-rolek/SKILL.md`) |
| Miniatury na YouTube | skill `miniatury` (`skills/miniatury/SKILL.md`) |
| Zasady wspólne dla obu montażystów | `ZASADY.md` (u Macieja i Jakuba podpięty jako `~/Montażysta AI/CLAUDE.md`) |
| Najnowszy wzorcowy projekt rolki | `wzory/C4538/` (kamera Sony, styl premium, hook A/B, CTA „zaobserwuj”) |

## Pamięć: `pamiec/`

Każdy plik to jedna lekcja albo jeden fakt: kiedy i jak Jakub coś powiedział (cytaty), dlaczego i jak to stosować. `pamiec/INDEKS.md` to spis z jednozdaniowym streszczeniem każdej notatki.

- Notatki mają daty. **Przy sprzeczności wygrywa nowsza**, a ponad notatkami stoją `ZASADY.md` i `SKILL.md`, bo są aktualizowane przy każdej zmianie. Przykład: starsze notatki mówią o jednej wersji rolki i CTA „napisz w komentarzu”, a od 24.11.2026 obowiązują hook A i B oraz CTA „zaobserwuj”.
- Ścieżki w notatkach dotyczą Maca Jakuba: `~/Montażysta AI/` (projekty, repo) i `~/Desktop/Montażysta AI/` (Eksporty, Nagrania, Surówki, Referencje, Grafiki, Muzyka).
- Notatki o tym, czego „nie wpisywać do skilla”, są nieaktualne: 25.11.2026 Jakub poprosił, żeby w repo było dosłownie wszystko.

## Jak się uczysz (obowiązkowo)

1. Po każdym filmie dopisz do `skills/montaz-rolek/references/dziennik.md` ocenę Jakuba: pochwały, krytykę, cytaty, statystyki z Instagrama.
2. Nową ogólną zasadę od Jakuba zapisz w trzech miejscach: w `ZASADY.md`, w odpowiednim `SKILL.md` lub referencji oraz jako notatkę w `kontekst/pamiec/` (z datą i cytatem) z linijką w `INDEKS.md`.
3. Nowy wzorcowy projekt skopiuj do `wzory/` (skrypty i `NOTATKI.md`, bez nagrań).
4. Po zmianie: commit w repo. Push robi Jakub sam (`git -C ~/"Montażysta AI/montazysta-ai" push`), chyba że powie inaczej.

## Foldery na Macu Jakuba

- `~/Desktop/Montażysta AI/Surówki/nie zmontowane/` → po montażu przenieś do `Surówki/zmontowane/` (za jego zgodą; poprawiaj ścieżki `VIDEO` w projektach).
- `~/Desktop/Montażysta AI/Nagrania /` (ze spacją na końcu): starsze nagrania z iPhone'a i mikrofonu.
- `~/Desktop/Montażysta AI/Eksporty/{Rolki, YouTube, Reklamy adGen}/<RRRR-MM-DD Tytuł>/`: gotowe pliki.
- `~/Desktop/Montażysta AI/Referencje i wytyczne/`: `Rolki wzorcowe/`, `Zdjęcie profilowe/` (nie w repo, każdy wgrywa swoje).
- `~/Desktop/Montażysta AI/Grafiki/{logo, osoby, ksiazki}/` + `ZRODLA.txt`: pobrane logo i zdjęcia nazw własnych.
- `~/Montażysta AI/projekty/<nazwa nagrania>/`: projekty montażu (skrypty, analiza, hf, renders).
- `~/Montażysta AI/scenariusze/`: scenariusze rolek (kopia w repo: `skills/scenariusze-rolek/przyklady/`).

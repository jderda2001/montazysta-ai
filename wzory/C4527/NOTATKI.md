# C4527 „20 ofert w godzinę” (rolka organiczna, personal brand)

Montaż 24.11.2026, scenariusz 1 z `scenariusze/2026-11-24 3 scenariusze – freelancerzy i małe firmy.md`.
Dwie wersje: hook A (ten folder, 35,2 s) i hook B (`hookB/`, 34,1 s).

## Źródło
- `~/Desktop/C4527.MP4`: kamera Sony (XAVC), 4K 29,97 kl./s, nagrana pionowo (obrót w metadanych, po obrocie 2160×3840), dźwięk z mikrofonu w pliku (offset 0, synchronizacja 2 ms).
- Jasne nagranie (YAVG ok. 126), zielone światło na ścianie; lekki grading bez rozjaśniania.

## Cięcia (ostatni pełny dubel)
- Hook A: 10.18 „Wysłałem 20 ofert w godzinę, nie dotykając komputera” (8.60 „Wysyłam 20 ofert w godzinie” to pierwsze podejście, wycięte).
- Hook B: 17.14 „Ten bot szuka Ci zleceń, kiedy śpisz.”
- Falstart 25.96 „Dałem jednym…” → start od 26.98.
- „Kiedy coś pasuje, czyta brief” (59.40) + „i tworzy ofertę w Canvie…” (68.64); pominięte 47.3 i 52.3 (niepełne) i falstart 65.0 „I pi…”.
- „Po tygodniu…” z 103.05 (wcześniejsze cztery podejścia pominięte).
- CTA 132.51 (122.9 przerwane „a… czekaj”).
- Kontrole: kawalki.py (oba tryby) 0 alarmów po poprawkach, powtorzenia.py 0 miejsc (A i B).

## Grafiki (zasada 10: 2 sceny + plansza końcowa)
- Hasło od klatki 0: A „20 ofert w godzinę. Zero klikania.”, B „Bot szuka Ci zleceń, kiedy śpisz.”; akcent jako miętowe zakreślenie (zielona ściana gasiła miętowe litery).
- Scena A (jasna, kurtyna) 3,2–15,7 s: Grok Bot z zadaniem → Useme, Oferteo, „+ inne” → trzy zlecenia, jedno „Pasuje ✓” → „Czyta brief…” → oferta z logo Canvy pisze się linijka po linijce, chip „pod tego klienta”.
- Twarz z płynnym najazdem: „Nie szablon. Pełnoprawną ofertę.”, „nawet nie dotknąłem komputera”.
- Scena B (szkło) 18,5–23,7 s: PO TYGODNIU 12 ofert wysłanych / 8 odpowiedzi / 4 umówione spotkania (liczniki).
- Plansza końcowa `telefon` w trybie obserwuj (ekran profilu, Obserwuj → Obserwujesz), od „koniecznie zaobserwuj”. CTA z lokalnej kopii `skrypty/cta.py` = `scenariusze/narzędzia/cta_obserwuj.py` (nie z repo).
- Napisy na białej koszulce: pod pasem napisów miękkie przyciemnienie obrazu (`.c7-scrim`), wygląd napisów bez zmian.
- Logo: Useme, Canva (ikony stron przez favicony Google, useme.com blokuje pobieranie), Oferteo (apple-touch-icon), Grok Bot (z IMG_0720). Zapisane w `Desktop/Montażysta AI/Grafiki/logo/` + ZRODLA.txt.
- 6 efektów dźwiękowych (ok. 10 na minutę).

## Do sprawdzenia przez Jakuba
- Hook A mówi „20 ofert w godzinę”, a wynik to „po tygodniu wysłał 12 ofert”. Liczby się gryzą; hook B tego problemu nie ma.
- „Zero klikania” w haśle A to skrót od „nie dotykając komputera”.

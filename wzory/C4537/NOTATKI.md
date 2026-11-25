# C4537 „Kończę call, oferta już czeka” (skrypt 4 z „5 scenariuszy – AI i biznes”)

Montaż 24.11.2026. Wersje: hook A (30,2 s), hook B (`hookB/`, 28,9 s).

## Cięcia
- Hook A: 3.96 „Kończę calla sprzedażowego z klientem, a oferta już na mnie czeka.” (3.0 „Kronecza…” = falstart). Whisper słyszy „nam nie czeka”, w napisach „na mnie czeka”. Klatki 0–4 (mrugnięcie) zastąpione klatką 8, synchronizacja bez zmian (2 ms).
- Hook B: 15.66 „Przestań pisać oferty po callu.” (druga połowa „Niech napisze ją rozmowa” nie wyszła w nagraniu).
- „Na każdym moim callu siedzi notetaker.” z trzeciego podejścia (29.30). Falstarty: 67.7 „Zakcy…” → 68.58; 98.0 „Jeszcze raz” → 98.85.
- Kontrole: kawalki.py (oba tryby), powtorzenia.py: 0.

## Grafiki
- Hasło: A „Koniec rozmowy = gotowa oferta.”, B „Przestań pisać oferty po callu.”
- Scena A (jasna) 3,0–8,9 s: ROZMOWA Z KLIENTEM, „Call sprzedażowy” + „notetaker” + fala głosu, notatka: czego klient chce / na kiedy / ile może wydać.
- Scena B (szkło) 9,0–19,4 s: Notatka › Grok Bot › Oferta (logo Canvy), „Oferta dla klienta · Twój szablon”: Zakres, Cena, Termin, Następny krok, przycisk Wyślij → „Wysłano ✓”.
- Najazd na „zanim zdąży o mnie zapomnieć”.
- Plansza `stos` w trybie obserwuj od „Zaobserwuj”: „Cały setup? Daj znać w komentarzu”.
- Notetaker bez nazwy (w nagraniu bez marki); logo Grok Bota i Canvy z Grafiki/logo.

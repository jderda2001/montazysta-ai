# IMG_0361 – „Przedstawiciele bez spotkań”

Źródło: `~/Desktop/Montażysta AI/Nagrania /IMG_0361.mov` (iPhone 4K, pion, 3:18, surowe nagranie z dublami; do 13.11.2026 leżało w Eksporty).
Eksport: `~/Desktop/Montażysta AI/Eksporty/Reklamy adGen/2026-11-09 Przedstawiciele bez spotkań/` (HOOK A i HOOK B).

## Wersje

| Wersja | Hook | Długość |
|---|---|---|
| A | „Zatrudniłeś przedstawicieli, którzy mieli Ci dostarczać sprawy na służebność przesyłu? A oni jedyne co robią…” | 45,7 s |
| B | „Przedstawiciel bez leadów to koszt, który rośnie każdego miesiąca.” | 39,1 s |

Treść po hooku jest w obu wersjach identyczna.

## Wybrane duble (czasy w pliku źródłowym)

| Fragment | Czas w źródle | Kadr |
|---|---|---|
| Hook A, cz. 1 | 25,5–29,1 | średni |
| Hook A, cz. 2 („od drzwi do drzwi…”) | 33,1–38,7 | bliski |
| Hook B | 59,1–62,1 (dubel 2, bez zapowiedzi „hook B”) | bliski |
| „Kancelarie rekrutują…” + „szybciej, niż…” | 96,7–100,0 + 105,1–107,3 (ostatnia wersja ze słowami „na to klientów”) | szeroki → bliski |
| „Po ostatnich wyrokach TK…” | 113,3–118,3 | średni |
| „Tyle, że… pensja, paliwo” | 124,3–128,0 | szeroki |
| „I co najważniejsze… frustracja” | 130,2–132,8 | bliski |
| „Dostarczamy…” / „pod liniami…” | 143,0–144,8 / 147,6–149,5 | średni |
| „Sprawdzonych telefonicznie…” | 161,4–163,2 + 166,8–167,5 | szeroki |
| „Wolumen dobieramy…” | 172,3–174,3 | bliski |
| „A każdy lead…” | 176,9–179,2 | średni |
| CTA „Zostaw kontakt…” | 188,4–191,4 (wersja z „idealnym wolumenem”) | bliski |

Zasada wyboru: ostatni pełny dubel każdej kwestii, bez potknięć w transkrypcji.

## Branding (z adgen.pl)

- Font: Inter Tight
- Kolory: czerń `#0f1012`, pomarańcz `#ff7018`, biel, szarości `#898989` / `#50545a`
- Logo: `branding/adGen_Logo.svg`

## Jak zmienić

- Duble lub kadry: `skrypty/aroll.py`, potem `python3 -I skrypty/aroll.py A B`.
- Napisy, plansze, CTA: `skrypty/kompozycja.py`, potem `python3 -I skrypty/kompozycja.py`.
- Render: w `hf_A` lub `hf_B` uruchom `hyperframes render -o renders/final.mp4`.

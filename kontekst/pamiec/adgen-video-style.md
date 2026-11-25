---
name: adgen-video-style
description: "How the user's adGen ad videos are edited (references, branding, folder layout, output naming) — derived from their reference films"
metadata:
  node_type: memory
  type: project
  originSessionId: 86deeb8d-c257-42cc-9214-7efdf8a192fb
  modified: 2026-11-13T13:09:52.603Z
---

Użytkownik prowadzi adGen (adgen.pl, leady dla kancelarii odszkodowawczych) i montuje pionowe reklamy wideo (Meta Ads).

- Foldery: `~/Desktop/Montażysta AI/` → `Eksporty/` (gotowe pliki w podfolderach, zob. [[feedback-eksporty-porzadek]]; surowe nagrania od 13.11.2026 w `Nagrania `, tam leży też IMG_0361.mov), `Referencje i wytyczne/` (wzorcowe filmy), `Nagrania/`.
- Surowe nagrania zawierają dużo dubli i warianty hooków („to jest hook A… teraz hook B”), więc robię osobną wersję dla każdego hooka (testy A/B).
- Styl z referencji: 1080×1920, napisy słowo po słowie (biały gradient, cień i poświata), hook z dużym kinetycznym słowem, ciemne plansze `#0f1012` z pomarańczowymi kwadratami `#ff7018`, ikony w pomarańczowych kafelkach, zielone „ptaszki” przy pozytywach, przejścia blur + light leak, CTA pod koniec.
- Branding: font Inter Tight. Logo `adGen_Logo.svg` jest w referencjach, ale od 13.11.2026 obowiązuje zakaz: nigdy nie dodawaj logo adGen, bo filmy są pod personal brand użytkownika (zob. [[feedback-reel-style-approved]]).
- Nazwy plików wynikowych w stylu referencji: `<Tytuł>_HOOK A_MM.RR.mp4`.
- Projekt pierwszego filmu (narzędzia i notatki): `/Users/jd/Montażysta AI/projekty/IMG_0361/` (skrypty `aroll.py` i `kompozycja.py` można skopiować do kolejnych filmów).

- Kolory: 17.11.2026 Jakub potwierdził, że reklamy adGen zostają pomarańczowe (`MARKA = "adgen"` w skillu `montaz-rolek`), mimo że jego personal brand przeszedł na `#00E5A0` (zob. [[feedback-paleta-marki]]).

**Why:** pierwszy montaż (2026-11-07) zbudowałem na tej analizie, a kolejne filmy mają mieć ten sam wygląd.
- Najnowszy wzór reklamy z kilkoma hookami (17.11.2026): `/Users/jd/Montażysta AI/projekty/IMG_0583/` „Leady z OC”, hook A / B / C. Jedne `skrypty/` w głównym folderze, wersje w `A/`, `B/`, `C/` (wersję wybiera nazwa folderu), grafiki reklamowe w palecie adGen (karta leada, karta połączenia, karta liczby, lista „za co płacisz”, przycisk „ZOSTAW KONTAKT”, plansza końcowa bez logo) w `skrypty/kompozycja.py`, przebieg i pułapki w `NOTATKI.md`. Podobny układ ma równoległy projekt IMG_0585 (służebność przesyłu). Ocena Jakuba obu reklam: jeszcze nie znam.
- Jakub nagrywa reklamy z dopowiedzeniami spoza skryptu (inne brzmienie hooków, inne liczby, np. „do 48 godzin” zamiast „1 do 3 dni”). Montuję to, co powiedział, a liczby różne od skryptu zgłaszam mu przed renderem.

**How to apply:** przy następnej reklamie zacznij od skryptów z IMG_0583 (IMG_0361 to stara wersja sprzed zakazu logo i sprzed zasad o falstartach i głosie) zamiast analizować referencje od nowa. Głos naturalny, zob. [[feedback-voice-sound]]. Zob. [[video-tools-setup]], [[feedback-false-starts]].

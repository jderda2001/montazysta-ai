---
name: feedback-eksporty-porzadek
description: Folder Eksporty ma być zawsze uporządkowany: podfoldery wg typu (YouTube / Rolki / Reklamy adGen), folder na każdy film, bez surowych nagrań
metadata:
  type: feedback
---

13.11.2026 Jakub pokazał płaską listę plików w `~/Desktop/Montażysta AI/Eksporty/` i napisał: „zawsze utrzymuj porządek tutaj, zaproponuj strukturę podfolderów”.

**Why:** w jednym folderze mieszały się long-form, rolki, reklamy, napisy, opisy i surowe nagranie z iPhone'a, przez co trudno znaleźć pliki do publikacji.

**How to apply** (struktura zatwierdzona 13.11.2026 słowami „Tak, przenieś”; pliki zostały wtedy przeniesione):
- `Eksporty/YouTube/<RRRR-MM-DD Tytuł>/`: odcinek, `.srt`, opis z rozdziałami i podfolder `Rolki promo/` (3 rolki i ich opisy).
- `Eksporty/Rolki/<RRRR-MM-DD Tytuł>/`: rolka organiczna (plus opis, jeśli jest).
- `Eksporty/Reklamy adGen/<RRRR-MM-DD Tytuł>/`: wersje z hookami (`_HOOK A_`, `_HOOK B_`).
- Data w nazwie folderu to dzień eksportu. Nazwy plików zostają jak dotąd (`<Tytuł>_MM.RR.mp4` itd.), żeby miały sens wysłane osobno.
- Surowe nagrania nie trafiają do Eksporty. Ich miejsce to `~/Desktop/Montażysta AI/Nagrania /` (ze spacją na końcu nazwy).
- Przy każdym eksporcie od razu kładź plik we właściwym folderze. Nic nie zostaje luzem w katalogu głównym Eksporty.

Zob. [[adgen-video-style]], [[feedback-longform-3-rolki]].

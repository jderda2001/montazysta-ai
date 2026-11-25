# Skrypty (szablony z IMG_0526)

Skopiuj do `projekty/<IMG_xxxx>/skrypty/`. Każdy skrypt liczy ścieżki względem folderu projektu (`P = folder nadrzędny skrypty/`).

| Skrypt | Do czego | Co zmienić w nowym projekcie |
|---|---|---|
| `sync.py` | offset i dryf audio z mikrofonu względem wideo | nic (czyta `audio/wideo_16k.wav`, `audio/nowe_16k.wav`) |
| `wyspy.py` | wyspy mowy i transkrypcja, wybór dubli | nic |
| `obwiednia.py` | obwiednia RMS i pauzy w zakresie czasu | nic |
| `kawalki.py` | falstarty, powtórzenia i zająknięcia w wybranych dublach; sam oznacza `POWTORKA?` i `?`, tryb `--drobne` | nic |
| `fonemy.py` | drobna obwiednia (dB i przejścia przez zero co 20 ms) do cięcia w środku słowa | nic |
| `czesci.py` | dźwięk kwestii po wycięciach ze środka (`wytnij` w `SEGS`); używają go `slowa.py`, `kawalki.py`, `waliduj_napisy.py` | nic |
| `aroll.py` | A-roll: cięcia, kadry, grading, dźwięk | `VIDEO`, `AUDIO`, `FRAMES` (pod twarz), `SEGS` |
| `sprawdz_sync.py` | przesunięcie dźwięku względem obrazu na kwestię | nic |
| `slowa.py` | czasy słów (whisper DTW `-nfa`) | nic |
| `waliduj_napisy.py` | czy żadne słowo napisów nie wyprzedza mowy | nic |
| `glos.py` | surowe cięcia (`raw_concat`), wersja „miękki głos” (EQ) | nic (EQ tylko po pomiarze) |
| `sidon_infer.py` | Sidon: mowa „studyjna” z AI. Tylko na prośbę Jakuba albo przy złym nagraniu (od 17.11.2026 domyślnie głos naturalny) | nic |
| `studio.py` | wyrównanie Sidona, kontrola F0, warianty B i C | łańcuch `DEEP` tylko po pomiarze widma |
| `kompozycja.py` | HyperFrames: hook, napisy, grafiki, CTA, plansza końcowa, SRT | `PHRASES`, `FIX`, grafiki w `build()`, `AV` (awatar), `GLOS` (domyślnie `audio/aroll.wav`), `MARKA`. **Styl napisów i CSS zostaw.** |
| `sfx.py` | miks subtelnych efektów dźwiękowych pod głos (wywołuje go `kompozycja.py`) | poziomy i warianty tylko po odsłuchu Jakuba |
| `twarze.py` (+ `twarz.swift`) | pomiar twarzy w ujęciach (macOS Vision) do automatycznego kadru pod strefę bezpieczną; `aroll.py` z `kadr()` bierze z niego zoom | `--flip` przy nagraniu lustrzanym; narzędzie: `swiftc -O -o ~/.local/bin/twarz scripts/twarz.swift` |
| `strefa.py` | kontrola strefy bezpiecznej (safe zone) na całym filmie, obrys strefy na klatkach | nic (strefę zmienia się w `SAFE` w `kompozycja.py`) |
| `kontrola_eksportu.py` | kontrola gotowego pliku przed oddaniem | nic |
| `poczatek.py` | pierwsze 5 s gotowego pliku słowo po słowie: transkrypcja vs `.srt`, okna od i do każdego cięcia, głos przed `a_in`, sklejka dwóch podejść, zamrożenia i powtórzone klatki, podwójny napis, stykówka co 0,5 s (od 25.11.2026, obowiązkowo na HOOK A i B) | nic |

Grafiki w `build()` opowiadają historię Kai (lista zadań, powiadomienie, CRM, kalendarz, koszty, profil, komentarz). W nowym temacie zostaw funkcje pomocnicze (`panel`, `overlay`, `pop`, `leak`, `W`, `seg`) i CSS, a zestaw grafik ułóż od nowa pod treść, korzystając ze słownika w `references/styl.md`.

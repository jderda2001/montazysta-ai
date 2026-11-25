# Montażysta AI

Zestaw, z którym Claude Code montuje rolki, reklamy i long-formy w stylu zatwierdzonym przez Jakuba. Ten sam zestaw działa na Macu Jakuba i na Macu Macieja: skille czytają pliki prosto z tego repo, więc każda poprawka i każda lekcja z montażu trafia do obu osób przez `git pull`.

## Co jest w środku

| Folder | Zawartość |
|---|---|
| `skills/montaz-rolek/` | Skill montażu: proces, styl, skrypty (cięcia, falstarty, napisy, kadry, plansze, SFX, kontrola), biblioteka ok. 50 szablonów grafik HyperFrames i dziennik ocen. |
| `skills/miniatury/` | Skill miniatur YouTube: 3 warianty do testu A/B, po 2 tytuły do każdego. |
| `skills/scenariusze-rolek/` | Skill scenariuszy rolek 20–30 s (dwa hooki, hasło od klatki 0, rozpiska z montażem, CTA „zaobserwuj”, źródła) i wzorcowe paczki scenariuszy. |
| `kontekst/` | Cała wiedza poprzedniego montażysty: kim jest Jakub, foldery, od czego zacząć (`README.md`) i wszystkie notatki z uwagami Jakuba (`pamiec/`, spis w `INDEKS.md`). **Nowy agent czyta to na start.** |
| `ZASADY.md` | Zasady zespołu: marki (adGen, PerfOS, personal brand), styl, dźwięk, eksporty, synchronizacja. Instalator podpina ten plik jako `~/Montażysta AI/CLAUDE.md`. |
| `wzory/` | Wzorcowe projekty bez nagrań: skrypty, notatki, branding, szkielet HyperFrames. Instalator kopiuje je do `~/Montażysta AI/projekty/`. Najnowszy wzór rolki: `wzory/C4538/` (kamera Sony, hook A/B, CTA „zaobserwuj”). |
| `zasoby/Muzyka/` | Muzyka lo-fi do long-formów (Biblioteka audio YouTube) i SFX (Kenney CC0, Mixkit). Szczegóły licencji są w plikach w `SFX/`. |
| `instalacja/zainstaluj.sh` | Instalacja wszystkich narzędzi i podpięcie skilli. |

## Instalacja (Maciej, jednorazowo, ok. 15 minut)

Potrzebne są macOS, Claude Code i dostęp do tego repo (zaproszenie od Jakuba na GitHubie, przyjmij je z maila).

1. Zainstaluj Homebrew, jeśli go nie masz (poprosi o hasło do Maca):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Zaloguj się do GitHuba i sklonuj repo do folderu roboczego:
   ```bash
   brew install gh && gh auth login
   ```
   ```bash
   mkdir -p ~/"Montażysta AI" && gh repo clone jderda2001/montazysta-ai ~/"Montażysta AI/montazysta-ai"
   ```
3. Uruchom instalator. Zainstaluje ffmpeg, whisper.cpp z modelem (ok. 550 MB), HyperFrames na Node 22 i uv. Podepnie też skille i zasady oraz założy foldery:
   ```bash
   zsh ~/"Montażysta AI/montazysta-ai/instalacja/zainstaluj.sh"
   ```
4. Do miniatur potrzebny jest klucz kie.ai: dostaniesz go od Jakuba albo założysz własne konto. Zapisz go tak:
   ```bash
   mkdir -p ~/.config/kie && pbpaste > ~/.config/kie/api_key && chmod 600 ~/.config/kie/api_key
   ```
   Przed tym poleceniem skopiuj klucz do schowka.
5. Otwórz Claude Code w folderze `~/Montażysta AI`. W aplikacji desktopowej wybierz ten folder, w terminalu wpisz `cd ~/"Montażysta AI" && claude`.

## Twoje referencje (wgraj po instalacji)

Repo nie zawiera cudzych rolek ani zdjęć. Każdy wgrywa swoje, a instalator przypomni o tym na końcu i otworzy folder:

- **`~/Desktop/Montażysta AI/Referencje i wytyczne/Rolki wzorcowe/`**: 1–3 rolki, które Ci się podobają, Twoje albo ulubionych twórców (pobrane np. przez snapgram albo ssstik). Montażysta ogląda je przed montażem i bierze z nich tempo, ruch, styl wstawek, CTA i plansz końcowych.
- **`~/Desktop/Montażysta AI/Referencje i wytyczne/Zdjęcie profilowe/`**: Twoje zdjęcie profilowe, najlepiej kwadratowe, z twarzą na środku. Trafia do CTA (profil, wiadomość) i na plansze końcowe.

Opis tego, czego szukać we wzorcach, jest w `skills/montaz-rolek/references/wzorce/README.md`.

## Jak pracować

- Nagranie (kamera Sony `C45xx.MP4` albo iPhone) wrzuć do `~/Desktop/Montażysta AI/Surówki/nie zmontowane/` (albo na pulpit, do `~/Downloads`, do `Nagrania `). Napisz Claude'owi, co to jest: reklama adGen z hookami A/B/C, rolka PerfOS albo rolka organiczna. Jeśli nagranie jest ze scenariusza, scenariusz leży w `~/Montażysta AI/scenariusze/` i Claude go odnajdzie.
- Scenariusze: poproś o nie („daj 5 skryptów o AI w biznesie”); skill `scenariusze-rolek` sprawdzi newsy w sieci i zapisze paczkę w `~/Montażysta AI/scenariusze/`.
- Claude sam pobierze najnowszą wersję skilli (`git pull`), zmontuje film w wersjach z hookiem A i B, sprawdzi falstarty, powtórzenia, przerwy, strefę bezpieczną i oczy na pierwszej klatce, wyrenderuje i odłoży pliki do `~/Desktop/Montażysta AI/Eksporty/…` razem z 2 propozycjami opisu albo tekstu reklamy.
- Uwagi do montażu pisz normalnie („za szybko ucięte”, „mocniej animuj wykres”). Po oddaniu Claude zapisze ocenę w dzienniku skilla i wypchnie zmianę do repo, więc druga osoba dostanie tę lekcję.

## Synchronizacja

- Zmiany ze skilli i zasad Claude commituje po montażu; `git push` robi Jakub (albo Claude, jeśli go o to poprosisz). Ręcznie: `git -C ~/"Montażysta AI/montazysta-ai" pull` / `push`.
- `dziennik.md` scala się automatycznie (`merge=union`), więc równoległe wpisy obu osób się nie gryzą.
- Do repo nie trafiają nagrania, eksporty, rendery ani klucze (`.gitignore`). Repo jest prywatne.

## Wymagania

macOS 14 lub nowszy (Apple Vision w pomiarze twarzy i miniaturach) i ok. 60 GB wolnego miejsca na dysku. Rendery HyperFrames trzymają klatki w pamięci podręcznej, więc 4K-owe nagrania szybko zajmują dysk.

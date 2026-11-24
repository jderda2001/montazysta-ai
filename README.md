# Montażysta AI

Zestaw, z którym Claude Code montuje rolki, reklamy i long-formy w stylu zatwierdzonym przez Jakuba. Ten sam zestaw działa na Macu Jakuba i na Macu Macieja: skille czytają pliki prosto z tego repo, więc każda poprawka i każda lekcja z montażu trafia do obu osób przez `git pull`.

## Co jest w środku

| Folder | Zawartość |
|---|---|
| `skills/montaz-rolek/` | Skill montażu: proces, styl, skrypty (cięcia, falstarty, napisy, kadry, plansze, SFX, kontrola), biblioteka ok. 50 szablonów grafik HyperFrames i dziennik ocen. |
| `skills/miniatury/` | Skill miniatur YouTube: 3 warianty do testu A/B, po 2 tytuły do każdego. |
| `ZASADY.md` | Zasady zespołu: marki (adGen, PerfOS, personal brand), styl, dźwięk, eksporty, synchronizacja. Instalator podpina ten plik jako `~/Montażysta AI/CLAUDE.md`. |
| `wzory/` | Wzorcowe projekty bez nagrań: skrypty, notatki, branding, szkielet HyperFrames. Instalator kopiuje je do `~/Montażysta AI/projekty/`. |
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

- Nagranie z iPhone'a wrzuć do `~/Downloads` albo do `~/Desktop/Montażysta AI/Nagrania `. Napisz Claude'owi, co to jest: reklama adGen z hookami A/B/C, rolka PerfOS albo rolka organiczna. Dołącz scenariusz, jeśli go masz.
- Claude sam pobierze najnowszą wersję skilli (`git pull`), zmontuje film, sprawdzi falstarty i strefę bezpieczną, wyrenderuje i odłoży plik do `~/Desktop/Montażysta AI/Eksporty/…` razem z 2 propozycjami opisu albo tekstu reklamy.
- Uwagi do montażu pisz normalnie („za szybko ucięte”, „mocniej animuj wykres”). Po oddaniu Claude zapisze ocenę w dzienniku skilla i wypchnie zmianę do repo, więc druga osoba dostanie tę lekcję.

## Synchronizacja

- Zmiany ze skilli i zasad wypycha Claude po montażu (commit i `git push`). Ręcznie: `git -C ~/"Montażysta AI/montazysta-ai" pull`.
- `dziennik.md` scala się automatycznie (`merge=union`), więc równoległe wpisy obu osób się nie gryzą.
- Do repo nie trafiają nagrania, eksporty, rendery ani klucze (`.gitignore`). Repo jest prywatne.

## Wymagania

macOS 14 lub nowszy (Apple Vision w pomiarze twarzy i miniaturach) i ok. 60 GB wolnego miejsca na dysku. Rendery HyperFrames trzymają klatki w pamięci podręcznej, więc 4K-owe nagrania szybko zajmują dysk.

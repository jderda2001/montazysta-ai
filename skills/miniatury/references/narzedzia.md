# Narzędzia i pułapki

Otwórz ten plik, gdy narzędzie zachowa się inaczej, niż oczekujesz, przed pierwszym użyciem gumki i przed kie.ai.

## Spis
1. Co jest potrzebne i gdzie leży
2. `mini.py` komenda po komendzie
3. Ranking i jego granice
4. Wycinanie postaci i gumka
5. Render i pliki wynikowe
6. kie.ai: tła i elementy
7. Zasady YouTube (stan na 14.11.2026)
8. Transkrypcja, gdy nie ma projektu montażu
9. Pułapki powłoki

## 1. Co jest potrzebne i gdzie leży

Nic nie trzeba instalować. Skrypty używają tylko biblioteki standardowej Pythona (systemowy `python3` 3.9 wystarcza; nie ma numpy ani PIL i nie są potrzebne).

- **ffmpeg / ffprobe** n9.0.2 w `~/.local/bin`. Bez `drawtext` i bez `zscale`.
- **swiftc** z Command Line Tools (`/usr/bin/swiftc`). `mini.py` sam kompiluje `scripts/wizja.swift` do `~/.cache/miniatury/wizja` (ok. 3 s) i robi to ponownie, gdy źródło jest nowsze od binarki.
- **Chrome bez okna** z HyperFrames: `~/.cache/hyperframes/chrome/chrome-headless-shell/…`. Gdy go nie ma, `mini.py` bierze Google Chrome z `/Applications`.
- **Krój** `assets/InterTight.ttf` (wagi 100–900, polskie znaki).
- **Klucz kie.ai** w `~/.config/kie/api_key` (prawa 600) albo w zmiennej `KIE_API_KEY`. Klucza nie ma w skillu, żeby nie wyciekł przy jego udostępnianiu. Nie wypisuj go w rozmowie.
- **Skill w innym miejscu niż `~/.claude/skills/miniatury`:** ustaw `MINIATURY_SKILL=/ścieżka/do/skilla` przed uruchomieniem `sklad.py`.

## 2. `mini.py` komenda po komendzie

| Komenda | Co robi | Czas | Wynik |
|---|---|---|---|
| `skanuj WIDEO --wyj KAT [--edl] [--momenty] [--fps 3] [--od --do]` | klatki co 1/3 s w 1280 px, ocena twarzy, ranking | ok. 3,5 min na 18 min 4K 60p | `skan/`, `skan.jsonl`, `kandydaci.json`, `arkusz_*.jpg` |
| `ranking KAT [--edl] [--momenty] [--ile 18] [--odstep 1.5] [--z-zajetymi]` | przelicza ranking bez skanowania | 3 s | jak wyżej |
| `dopracuj WIDEO --t 17:10.4 --wyj KAT/A [--okno 0.4] [--klatka K] [--mina 0.7]` | wszystkie klatki z ±0,4 s w pełnej jakości, wybór najostrzejszej z tą samą miną | 3 s | `klatka.png`, `klatka.json`, `seria.jpg` |
| `wytnij KAT/A/klatka.png [--tryb plan\|plan-pelny\|osoba] [--skurcz 2] [--wymaz X,Y,R] [--lupa X,Y]` | postać z przezroczystym tłem | 2 s | `postac.png`, `postac.json`, `postac_podglad.jpg`, `postac_lupa.jpg` |
| `render PLIK.html` | zrzut 1920×1080 w skali 2 | 2 s | `PLIK.png` i `PLIK.jpg` 3840×2160 |
| `kontrola A.jpg B.jpg C.jpg --tytul … --czas …` | wymiary, twarz, czytelność tekstu, strefy, jasność, tytuły, makieta listy z tytułami | 5 s | raport, `podglad.jpg`, `podglad.json` |
| `eksport A.jpg B.jpg C.jpg --tytul … --folder … [--opis test_AB.txt]` | kopie z właściwymi nazwami w `…/Miniatury/` | – | pliki w Eksporty |

- **Czasy** (`--t`, `--od`, `--do`) podajesz w sekundach (`1030.4`) albo tak jak na arkuszach (`17:10.4`).
- **Z `--edl`** skan obejmuje tylko zakres nagrania, który wszedł do filmu (z sekundą zapasu), i oznacza klatki czasem w filmie. Klatki z odrzuconych dubli też są oceniane, bo dobra mina z dubla nadal jest dobrą miną. Bez `--edl` skanowany jest cały plik; rozgrzewkę i próbę mikrofonu utnij przez `--od`.
- **Skan pamięta parametry** w `skan_meta.json`. Ponowne `skanuj` z tymi samymi parametrami nie wyciąga klatek drugi raz (`--od-nowa` wymusza).
- **`#2550` na arkuszu to plik `skan/002550.jpg`** (cała klatka w 1280 px).
- **`ranking` pomija okolice klatek już użytych** (±3 s wokół czasów z `A/klatka.json`, `B/klatka.json`…), żeby przy kolejnym zestawie na czele stały nowe twarze. `--z-zajetymi` to wyłącza.
- **`dopracuj` szuka wzorca miny w skanie.** Gdy folder nad `--wyj` zawiera `skan.jsonl` (albo podasz `--skan KAT`), bierze stamtąd klatkę o wskazanym czasie i znajduje w serii tę o tej samej minie. Wybiera potem najostrzejszą spośród klatek, których mina nie odbiega od wzorca o więcej niż `--mina` (domyślnie 0,7). `seria.jpg` pokazuje klatki po kolei, z oznaczeniem „(wskazana)” i „← wybrana” oraz odległością miny Δ. Gdy automat stanął obok właściwego momentu, wskaż klatkę przez `--klatka K`.
- **`skan/` zajmuje ok. 65 kB na klatkę** (200 MB przy 18 min). Usuń go po akceptacji miniatur.

## 3. Ranking i jego granice

`wygląd` łączy jakość ujęcia twarzy według Vision, ostrość i ustawienie głowy. Miny (`usmiech`, `akcent`, `spokoj`, `gest`) są liczone jako odchylenie od tego, jak ta osoba wygląda zwykle w tym nagraniu, więc działają też przy okularach i u innych osób. Kandydaci w kategorii są od siebie oddaleni o co najmniej 1,5 s.

Czego ranking nie widzi:
- czy mina jest sympatyczna, czy dłoń wygląda naturalnie, czy włosy leżą dobrze;
- że kategoria `akcent` łapie głównie klatki w pół słowa;
- mrugnięć za barwionymi szkłami (miara jest mniej pewna, sprawdź oczy na `seria.jpg`).

Dlatego arkusze trzeba obejrzeć, a liczby traktować jako wskazówkę, gdzie patrzeć.

Czasy na arkuszach: filtr `fps` oddaje ostatnią klatkę z każdej 1/3 sekundy, więc `skanuj` dolicza do czasu klatki ok. 0,16 s. Skany zrobione przed tą poprawką `ranking` przelicza sam przy pierwszym uruchomieniu i wtedy arkusze pokażą czasy późniejsze o 0,16 s.

## 4. Wycinanie postaci i gumka

Vision daje trzy maski i każda ma inną wadę, dlatego `wytnij` je łączy:

- **pierwszy plan** (wycinanie obiektów): najlepsze krawędzie i mikrofon przed klatką piersiową w komplecie, ale zabiera też kawałek fotela przy szyi;
- **dokładna segmentacja osób** (model od rozmów wideo): dobrze odróżnia człowieka od fotela, ale pomija mikrofon, więc w bluzie zostaje dziura;
- **maska instancji osoby**: zapas, gdy segmentacja nic nie zwróci.

Tryby:
- **`plan` (domyślny):** krawędzie z pierwszego planu, przycięte do obrysu sylwetki z segmentacji osób. Mikrofon zostaje, zagłówek obok szyi odpada.
- **`plan-pelny`:** cały pierwszy plan stykający się z osobą. Użyj, gdy Jakub trzyma coś obok ciała (kubek, telefon w wyciągniętej ręce) i `plan` to ucina.
- **`osoba`:** sama sylwetka z segmentacji. Użyj, gdy mikrofon ma zniknąć, a kadr i tak ucina tułów nad nim.

Krawędź jest wygładzana, cofana o `--skurcz` pikseli (domyślnie 2) i odbarwiana: półprzezroczyste piksele dostają kolor z wnętrza postaci, więc jasna ściana nie zostaje jako obwódka wokół włosów. Gdy obwódka nadal jest, daj `--skurcz 3` lub `4`.

**Zawsze obejrzyj `postac_podglad.jpg`.** Pokazuje wycięcie na ciemnym tle i na tle w kolorze akcentu (`#00E5A0`), z linijkami co 200 px w pikselach klatki. Resztki ciemnego fotela są niewidoczne na ciemnym tle, a na jasnym akcencie widać je od razu. Sprawdzaj szyję i okolice uszu, przestrzeń między palcami i miejsca, gdzie dłoń nachodzi na przedmioty z tła.

Gdy coś zostało, próbuj w tej kolejności:
1. **Sąsiednia klatka.** `dopracuj --klatka K` z tej samej serii często daje czystą maskę, bo głowa zasłania fotel inaczej.
2. **Tło, które to wybacza.** Na tle `kadr` resztka fotela pokrywa się z rozmytym fotelem z tyłu i wygląda naturalnie. Na `akcent` i `obraz` razi.
3. **Gumka.** Opis niżej.

Drobne kropki po siatce fotela tuż przy brodzie (kilka pikseli) nie są widoczne w żadnym rozmiarze, w którym YouTube pokazuje miniaturę. Nie trać na nie czasu.

### Gumka krok po kroku

1. **Znajdź resztkę z grubsza** na `postac_podglad.jpg` (linijki co 200 px).
2. **Zrób lupę:** `MINI wytnij A/klatka.png --lupa 2010,950` zapisuje `postac_lupa.jpg`, czyli wycinek 240×240 px klatki wokół tego punktu z siatką co 20 px. Trzecia liczba zmienia promień (`--lupa 2010,950,60` to większe powiększenie).
3. **Wymaż:** `MINI wytnij A/klatka.png --wymaz X,Y,R`. W kole o promieniu R wokół punktu X,Y znikają piksele o kolorze podobnym do koloru w środku koła, więc koło może zachodzić na skórę bez szkody.
4. **Obejrzyj podgląd ponownie.** Lista `--wymaz` nie jest zapamiętywana między uruchomieniami: przy każdej poprawce podaj wszystkie koła od nowa (zapisane są w `postac.json` w polu `wymazane`).

Na co uważać:
- **To samo ubranie co resztka.** Przy czarnym fotelu i czarnej bluzie test koloru nie odróżni jednego od drugiego: trzymaj koła nad linią ramion.
- **Cienka kreska (kilka pikseli)** przy policzku: środek koła musi leżeć dokładnie na niej, a to trudne. Pewniejsze jest koło z tolerancją 0 (`--wymaz X,Y,R,0` usuwa wszystko w kole), ustawione na zewnątrz postaci tak, żeby tylko zahaczało o kreskę.
- **Czwarta liczba** to tolerancja koloru: domyślnie 45, większa łapie więcej odcieni.

`postac.json` podaje prostokąt wycięcia w klatce (`kadr`), twarz we współrzędnych wycięcia (`twarz`) i użyte gumki (`wymazane`). Na tym `sklad.py` opiera ustawienie postaci i wyrównanie tła typu `kadr`.

## 5. Render i pliki wynikowe

- Kadr roboczy to 1920×1080 CSS px, render w skali 2 daje PNG 3840×2160. JPG ma tę samą wielkość i jakość dobieraną tak, żeby zmieścić się w 1,9 MB (zwykle 0,7–0,9 MB przy jakości 0,95).
- Chrome potrzebuje `--allow-file-access-from-files`, inaczej nie wczyta kroju z pliku. `mini.py render` to ustawia.
- Rozmiar linii tekstu dobiera skrypt w stronie po załadowaniu kroju. Gdy tekst wyjdzie nagle mały albo innym krojem, sprawdź, czy `assets/InterTight.ttf` istnieje.
- Pliki `A.html`, `B.html`, `C.html` można otworzyć w przeglądarce, żeby podejrzeć układ w narzędziach deweloperskich.
- `A.json` obok miniatury (id, hipoteza, napisy, tytuły) czyta kontrola i eksport. Tworzy go `sklad.py`.
- **HDR:** gdy nagranie jest w HLG albo PQ, `skanuj` ostrzega. Ten ffmpeg nie ma `zscale`, więc klatki mogą wyjść sprane. Dotąd nagrania Jakuba były w SDR (bt709).

## 6. kie.ai: tła i elementy

Jakub dał klucz po to, żeby dorabiać elementy graficzne. Skrypt `kie.py` wysyła wyłącznie tekst promptu.

```bash
python3 ~/.claude/skills/miniatury/scripts/kie.py kredyty
python3 ~/.claude/skills/miniatury/scripts/kie.py generuj --rodzaj element --proporcje 1:1 \
  --wyj miniatury/elementy/robot.png --prompt "…"
```

| `--rodzaj` | Wynik | Koszt | Czas | Do czego |
|---|---|---|---|---|
| `tlo` (domyślny, `--proporcje 16:9`) | PNG 1280×720 | 0,8 kredytu | 10–25 s | sceny i tła, które i tak będą przyciemnione lub rozmyte |
| `element` (`--proporcje 1:1`) | PNG ok. 1254×1254 z przezroczystym tłem | 5 kredytów | ok. 60 s | przedmioty, ikony 3D, naklejki |
| `premium` (opcjonalnie `--rozdzielczosc 4K`) | PNG 2K | ok. 5 kredytów według dokumentacji, niesprawdzone w praktyce | – | tło, które ma być ostre i w pełnym kadrze |

Stan konta 14.11.2026: ok. 8850 kredytów. Obok każdego pliku powstaje `*.prompt.json` z promptem, modelem i kosztem.

**Prompty** (po angielsku):
- opisz obiekt, materiał, światło i kadr; dodaj kolory marki słowami: „matte black and dark graphite”, „white details”, „bright mint green accents (#00E5A0)”, „cool mint green rim light”. Bez pomarańczu i innych ciepłych akcentów, bo od 17.11.2026 marka to czerń, biel, ciemny szary i akcent `#00E5A0`;
- zawsze dopisz „no text, no logos”, a przy scenach „no people”: napisy z generatora wychodzą z błędami, a jedyną osobą na miniaturze ma być Jakub;
- dla elementu: „single object, centered, isolated on a transparent background”;
- dla tła pod tekst: napisz, po której stronie ma być ciemniej i spokojniej („darker and calmer on the left side”);
- bez nazwisk, nazw klientów i innych danych w prompcie.

Sprawdzone prompty (IMG_0529, przepisane na paletę z 17.11.2026; w oryginale miały „orange” w miejscu „mint green” i tylko w tamtej wersji były renderowane):
- element: „A single friendly minimalist 3D robot head, matte dark graphite body, two glowing mint green eyes (#00E5A0), small mint green accent details, soft studio lighting with a subtle cool mint green rim light, front view, centered, isolated object on a transparent background, no text, no logos”
- tło: „Empty modern open-space office in the evening, rows of desks with empty office chairs and dark monitors, abandoned workstations, cool mint green accent light (#00E5A0) glowing from the right side, dark charcoal walls and floor, darker and calmer on the left side, cinematic wide shot, shallow depth of field, moody, high contrast, no people, no text, no logos”

**Zasady:**
- Obejrzyj każdy wygenerowany plik, zanim trafi na miniaturę.
- Wygenerowany element wpisz w polu `uwaga` wariantu i powiedz o nim przy oddaniu.
- Zdjęć Jakuba nie wysyłasz do kie.ai. `kie.py` celowo nie ma takiej opcji. Jeśli sam poprosi o retusz AI, zapytaj o zgodę na wysłanie konkretnego pliku.
- Prawdziwy materiał z odcinka (awatary agentów, zrzut panelu) jest lepszym dowodem niż wygenerowany obrazek. Generuj to, czego nie ma.

Gdyby skrypt wymagał poprawki: zadanie tworzy `POST https://api.kie.ai/api/v1/jobs/createTask`, stan zwraca `GET /api/v1/jobs/recordInfo?taskId=…`, kredyty `GET /api/v1/chat/credit`. Błędy przychodzą z HTTP 200 i kodem w polu `code`. Dokumentacja: `https://docs.kie.ai/llms.txt`.

## 7. Zasady YouTube (stan na 14.11.2026)

Źródło: pomoc YouTube, strony o miniaturach (answer/72431) i testach A/B (answer/13861714). Skrót tych zasad trafia do `test_AB.txt` dla Jakuba; tu jest to, co wpływa na pracę.

- **Miniatura:** JPG albo PNG, 16:9, zalecane 3840×2160, minimalna szerokość 640 px. Limit wagi: 2 MB z telefonu, 50 MB z komputera.
- **Test A/B:** do 3 miniatur, tylko w YouTube Studio na komputerze. Wygrywa wariant z największym czasem oglądania, a nie z najwyższym CTR. Trwa do 2 tygodni. Gdy nie ma zwycięzcy, zostaje pierwszy wgrany wariant.
- **Rozdzielczość w teście:** gdy którakolwiek miniatura ma mniej niż 1280×720, wszystkie są pomniejszane do 854×480.
- **Wyniki:** „Winner”, „Performed Same” (podobnie, można wybrać samemu), „Inconclusive” (brak rozstrzygnięcia).
- **Nie działa** dla Shorts, filmów prywatnych, dla dzieci i z ograniczeniem wieku. Zmiana tytułu albo miniatury w trakcie zatrzymuje test.

## 8. Transkrypcja, gdy nie ma projektu montażu

```bash
ffmpeg -i NAGRANIE.MOV -vn -ac 1 -ar 16000 miniatury/dzwiek.wav
whisper-cli -m ~/.local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin -l pl -osrt -of miniatury/tekst -f miniatury/dzwiek.wav
```
Czasy w `tekst.srt` są wtedy na osi surowego nagrania, więc w `momenty.json` daj `"os": "zrodlo"`.

## 9. Pułapki powłoki

- **`MINI` jako funkcja, nie zmienna.** zsh nie dzieli zmiennych na słowa, więc `MINI="python3 …"; $MINI skanuj` nie zadziała. Zdefiniuj `MINI() { python3 ~/.claude/skills/miniatury/scripts/mini.py "$@"; }`.
- **zsh i brak dopasowania:** `rm -f katalog/*.jpg` w pustym katalogu kończy się błędem „no matches found” i przerywa łańcuch `&&`. Używaj `find katalog -name '*.jpg' -delete`.
- **Folder `Nagrania `** na Pulpicie ma spację na końcu nazwy.
- **Pokazanie pliku Jakubowi:** `open -R "ścieżka"` zaznacza go w Finderze.

# Biblioteka grafik i przejść

Jakub po IMG_0576 (17.11.2026): „bardzo generyczne są przejścia względem animacji… bardzo często są używane te same rzeczy”, chce 20–30 szablonów „à la b-roll” do wyboru. Ta biblioteka jest odpowiedzią. Zanim zaprojektujesz grafiki do filmu, obejrzyj oba arkusze i wybierz z listy, zamiast sięgać trzeci raz po chip i planszę z kafelkami.

- Arkusze podglądów (w palecie marki, 9:16): `references/biblioteka_arkusz_1.jpg`, `references/biblioteka_arkusz_2.jpg`. Kolejność na arkuszach jest alfabetyczna, najpierw komponenty, potem bloki. Własne szablony z 18.11.2026 są na `references/biblioteka_arkusz_3.jpg` (od lewej: `dot-heatmap`, `line-scrub-card`, `pipeline-kanban`, `tick-slider`, potem kanban i wykres w polu strefy).
- Pliki: `~/.claude/skills/montaz-rolek/biblioteka/` (59 szablonów, 1,5 MB: 55 z katalogu i 4 własne). Źródło katalogowych: oficjalny katalog HyperFrames, `github.com/heygen-com/hyperframes` (Apache-2.0), pobrane 17.11.2026 komendą `hyperframes add`.
- Cały katalog ma ok. 450 pozycji. Gdy brakuje czegoś pod temat filmu: `hyperframes catalog --query "…"` albo `--tag transition|data|typography|mock-ui|annotation`, potem `hyperframes add <nazwa>` w folderze tymczasowym, test w 9:16 i dopiero wtedy kopia do biblioteki z wpisem tutaj.

## Zasady różnorodności

1. **Przejścia plansz się nie powtarzają pod rząd.** `panel()` bierze kolejne z listy `PRZEJSCIA` (iris, wipe, zoom, diag, slide, blur). W jednej rolce używaj 3–5 rodzajów, nie wszystkich naraz i nie jednego w kółko.
2. **Ten sam szablon grafiki najwyżej dwa razy w rolce**, i nigdy dwa razy pod rząd. Chip u góry kadru też się liczy.
3. **Wybór idzie od sensu zdania:** liczba → licznik albo pierścień; porównanie → karty przed/po albo wykres; „robi X, Y, Z” → siatka kart albo konstelacja; rozmowa z AI → czat; podkreślenie słowa → marker albo adnotacja; zmiana zdania → przekreślenie i zamiana.
4. **Wejścia elementów też różnicuj.** Samo `pop` (skok ze sprężyną) na wszystkim wygląda jak szablon. Z dokumentacji HyperFrames: wejścia `expo.out` albo `power4.out`, wyjścia `power3.in` i o 40–50% krótsze, słowa co 60–120 ms, pozycje listy co 40–80 ms, żadnych pulsujących pętli.
5. **Obce interfejsy zostają w swoich kolorach** (niebieski dymek iMessage, okno Claude), reszta bierze paletę marki z tokenów.

## Jak użyć

**Montowalne (M):** w `build()` wywołaj `mount(el, "g1", "count-up", t_in, 3.0, {"end": 24, "suffix": "+"})`. Funkcja kopiuje plik do `hf/` i dopisuje element na pełnym kadrze. Kolory przychodzą z tokenów `--brand`, `--bg`, `--fg`, `--surface` w `:root` szablonu. Czas wejścia podajesz ze słów, jak przy każdej grafice. Wiele szablonów ma zmienną `cues` (sekundy od startu elementu, po przecinku), którą ustawiasz momenty kolejnych pozycji na słowa.

**Wycinki (S):** plik zawiera `<style>`, znacznik i `<script>` do wklejenia w kompozycję (np. `<span class="hf-number-wheel" data-value="24">`). Otwórz plik, instrukcja jest w komentarzu na górze.

**Ograniczenia:** szablony mają własne nieprzezroczyste tło, więc nadają się na plansze, a nie na nakładki na twarz (wyjątki: powiadomienia i czaty z przezroczystym tłem, sprawdź na klatce). Teksty domyślne są po angielsku, zawsze podawaj własne. Szablon zawsze rysuje się na pełnym kadrze 1080×1920 i nie zna strefy bezpiecznej (`styl.md`, punkt 8): jego treść może wejść pod przyciski Instagrama, pod opis rolki albo na napisy z 1120 px. Rozmiar pudełka w `styl` go nie skaluje (sprawdzone 18.11.2026: treść zostaje w skali pełnego kadru i wychodzi poza pudełko). Żeby zmieścić szablon w kolumnie strefy, użyj `mount(..., pole=POLE_STREFY)`: cały kadr szablonu trafia do pomniejszającego opakowania (skala 0,64) wyśrodkowanego w polu 690×800 px. Tekst maleje wtedy o jedną trzecią, więc najmniejszy napis w szablonie musi mieć na pełnym kadrze co najmniej 44 px (własne szablony to spełniają, katalogowe sprawdzaj na klatce). Po każdym montowaniu obejrzyj klatki i uruchom `strefa.py`: arkusze 1 i 2 powstały przed strefą, więc pokazują układ na pełnym kadrze.

## Liczby i dane

| Szablon | Typ | Kiedy | Najważniejsze zmienne |
|---|---|---|---|
| `count-up` | M, 3 s | jedna duża liczba („24+ agentów”) | `start`, `end`, `prefix`, `suffix`, `glow` |
| `number-wheel` | S | kwota albo licznik z toczącymi się cyframi | `data-value`, `spin`, `tone` |
| `slot-machine-roll` | S | wartość, która „wypada” jak na automacie | `result`, `direction` |
| `conic-progress-ring` | M, 4 s | procent, udział | `progress`, `label`, `thickness` |
| `chart-story` | M, 5 s | słupki z jednym wyróżnionym | `data`, `labels`, `emphasize`, `unit` |
| `animated-bar-chart` | S | mała karta ze słupkami | w pliku |
| `decline-chart` | M, 4 s | spadek (linia w dół i licznik) | `label`, `start_value`, `end_value` |
| `pull-back-reveal` | M, 4,5 s | detal liczby, potem odjazd na cały panel | `detail_text`, `headline` |
| `outline-draw` | M, 4 s | obrys, który „zamyka” dowód | `progress`, `thickness`, `radius` |
| `svg-stroke-trace` | M, 3,5 s | własna linia albo kształt rysowany kreską | `path`, `stroke_width` |

Własny wykres z IMG_0576 (prosta kontra krzywa) zostaje wzorem dla wykresów opowiadających historię.

## Listy, procesy, porównania

| Szablon | Typ | Kiedy | Najważniejsze zmienne |
|---|---|---|---|
| `grid-card-assemble` | M, 4,5 s | „robi X, Y, Z”, 3–6 kart z ikonami | `items`, `layout`, `columns`, `cues` |
| `constellation-hub` | M, 4,5 s | centrum i połączone węzły (agenci, narzędzia) | `hub_label`, `nodes`, `cues` |
| `radial-surround` | M, 5 s | etykiety wokół środka („Twój zespół”) | `center_label`, `chips`, `cues` |
| `state-chip-rail` | M, 5 s | etapy procesu, aktywny się przesuwa | `states`, `times`, `badges` |
| `split-tilt-cards` | M, 4,5 s | przed i po, A kontra B | `label_a`, `label_b`, `badge_a`, `badge_b` |
| `spring-stack-shuffle` | M, 4 s | stos kart, które się przetasowują | `cards`, `cues` |
| `modal-morph` | M, 4 s | mała karta rozrasta się w panel | `expand_at`, `register` |
| `morph-swap` | M, 3,5 s | jedno zamienia się w drugie | `swap_at`, `register` |
| `strikethrough-replace` | S | stara wartość przekreślona, nowa obok | `origin`, `tint`, `tone` |

## Tekst i podkreślenia

| Szablon | Typ | Kiedy | Najważniejsze zmienne |
|---|---|---|---|
| `headline-slam` | M, 3,5 s | mocne hasło z jednym słowem w akcencie | `text`, `accent_word_index` |
| `kinetic-type-swap` | M, 4 s | „nie X, tylko Y”: jedno słowo się wymienia | `prefix`, `options`, `suffix`, `cues` |
| `ticker-takeover` | M, 4,5 s | przewijane opcje, zatrzymanie na jednej | `options`, `final_word` |
| `kinetic-center-build` | M, 2 s | zdanie budowane słowo po słowie | `text`, `font_size`, `color` |
| `text-shimmer` | M, 3 s | jedno słowo z przejazdem światła | `text`, `sweep_at` |
| `type-match-cut` | M, 4 s | hasło rozstępuje się wokół wchodzącego panelu | `text` |
| `marker-highlight` | M, 3,5 s | zdanie z zakreślonym słowem | `text`, `emphasis_word`, `style`, `draw_at` |
| `vox-annotate` | M, 4 s | słowo zakreślone i dopisek strzałką | `text`, `keyword`, `note` |
| `inline-highlight` | S | zakreślacz pod słowem w dowolnym tekście | `tint`, `thickness` |
| `hw-underline`, `hw-callout-circle`, `hw-arrow` | S | odręczne podkreślenie, kółko, strzałka | w plikach |
| `typed-prompt` | M, 4 s | polecenie wpisywane do AI | `text`, `prompt_glyph`, `cadence` |
| `typewriter` | S | tekst litera po literze | `text`, `caret` |
| `tracking-in`, `focus-blur-resolve` | S | spokojne wejście nagłówka | w plikach |
| `testimonial-proof-card` | M, 4,5 s | cytat klienta | `quote`, `name`, `role`, `emphasis` |

## Interfejsy i AI (temat Jakuba)

| Szablon | Typ | Kiedy | Najważniejsze zmienne |
|---|---|---|---|
| `claude-exchange` | blok M, 8 s | rozmowa z asystentem AI: pytanie, myślenie, odpowiedź | `prompt`, `thinking`, `lead`, `answer1`… |
| `ai-chat-reveal` | blok M, 8 s | pytanie wpisane na klawiaturze i odpowiedź AI | `userMessage`, `answer1`…, `bullet1`… |
| `chat-thread` | M, 8 s | rozmowa w komunikatorze | `contact`, `messages` (`recv:`/`sent:`) |
| `chat-message` | M, 3 s | jeden dymek | `type`, `text` |
| `message-thread-reveal` | blok M, 8 s | rozmowa na telefonie z kartą linku | `contactName`, `questionMessage`… |
| `native-notification-pop` | M, 3 s | jedno powiadomienie systemowe | `title`, `body`, `app_label`, `os` |
| `notification-stack` | M, 4 s | 1–5 powiadomień jedno po drugim | `titles`, `bodies`, `cues` |
| `notification-cascade` | blok M, 8 s | lawina powiadomień na ekranie blokady | `notifTitle`, `message1`… |

Treści w tych makietach podlegają tej samej zasadzie co reszta: tylko to, co Jakub mówi, a jeśli coś jest poglądowe, powiedz mu o tym przy oddaniu.

## Własne szablony à la b-roll (18.11.2026)

Jakub przysłał listę bibliotek UI (Arc UI, Bencho i inne) z pytaniem, czy coś z nich nadaje się do montażu, i na propozycję zrobienia wzorowanych na nich szablonów odpowiedział „Tak, zrób”. Tamte komponenty są w React i reagują na kursor, więc nie da się ich zamontować. Te cztery są napisane od zera na osi czasu GSAP, w palecie marki, z polskimi domyślnymi tekstami. Wzorem był tylko pomysł (tablica kanban, karta z wykresem, suwak z kresek, mapa aktywności z kropek), nie kod.

| Szablon | Typ | Kiedy | Najważniejsze zmienne |
|---|---|---|---|
| `pipeline-kanban` | M, 5 s | lead albo zadanie przechodzi przez etapy („od zapytania do klienta”) | `stages`, `fill`, `card`, `done`, `cues`, `title` |
| `line-scrub-card` | M, 5 s | wynik w czasie: wzrost, spadek, dowolny kształt; liczba czyta wartość pod punktem | `data`, `title`, `prefix`, `suffix`, `delta`, `labels`, `draw_at`, `draw` |
| `tick-slider` | M, 4 s | jedna wartość przesuwa się z A do B (budżet, czas, cena), także w dół | `from`, `to`, `min`, `max`, `label`, `suffix`, `ends`, `move_at`, `move` |
| `dot-heatmap` | M, 4,5 s | regularność i skala: „codziennie przez 30 dni”, „24/7”, seria z dziurami | `cols`, `rows`, `active`, `pattern`, `label`, `suffix`, `total`, `order`, `fill_at`, `fill` |

- Wszystkie mają zmienną `backdrop`: `solid` (własne tło, na pełny kadr) albo `none` (przezroczyste, na planszę z `panel()` albo do pola strefy).
- Najmniejszy tekst ma 4,2% szerokości kadru (45 px), więc po zmniejszeniu do pola strefy zostaje 29 px.
- `pipeline-kanban`: do 4 etapów mieści się w polu strefy; przy 5 tablica jest wyższa niż pole i trzeba ją zamontować na pełnym kadrze albo dać mniej etapów. Szare karty to atrapy bez treści. `cues` ustaw na słowa, w których mówi o kolejnym etapie, w odstępach co najmniej 0,9 s.
- `line-scrub-card`: linia przechodzi dokładnie przez podane punkty, a plakietka `delta` to tekst, który podajesz sam. Dane tylko z tego, co Jakub mówi; wykres poglądowy zgłoś przy oddaniu.
- Miejsca na dźwięk są opisane w komentarzu na górze każdego pliku (`shh` pod rysowanie i ruch, `pop` na lądowaniu karty i na plakietce).
- **Zatwierdzone przez Jakuba 18.11.2026:** „wszystkie super, można używać od dziś w rolkach”. Sięgaj po nie na równi z resztą biblioteki (z zasadami różnorodności).
- Sprawdzone: `hyperframes check` bez błędów, klatki na pełnym kadrze i w polu strefy. Nie były jeszcze użyte w żadnym filmie.

## Przejścia

Wbudowane w `panel()` (parametr `wejscie`, domyślnie rotacja z `PRZEJSCIA`):

| Nazwa | Wejście | Wyjście |
|---|---|---|
| `iris` | koło otwiera się z okolic twarzy | koło się zamyka |
| `wipe` | plansza wjeżdża maską od dołu | zwija się do góry |
| `zoom` | wyskakuje z głębi (skala 0,35 → 1, rozmycie) | przelatuje przez kamerę |
| `diag` | ukośna krawędź przejeżdża z lewej na prawą | ucieka w prawo |
| `slide` | cała plansza wjeżdża z dołu | wyjeżdża górą |
| `blur` | dawne wejście z IMG_0526: rozmycie i light leak | rozmycie i light leak |

W bibliotece są też gotowe komponenty przejść między dwiema scenami (`iris-reveal`, `whip-pan-cut`, `match-cut`, `halftone-dissolve`, `fade-through`, `parallax-zoom`, `grid-pixelate-wipe`) oraz cztery bloki z przepisami (`transitions-push`, `-cover`, `-radial`, `-scale`). Wymagają dwóch warstw (przed i po) w jednym komponencie, więc traktuj je jako źródło przepisów do nowych pozycji w `RUCH`, a nie jako gotowce. Wartości w przejściach podawaj w pikselach, nie w procentach.

## Sygnały dźwiękowe

Biblioteka dźwięków leży w `~/Desktop/Montażysta AI/Muzyka/SFX/` (pobrana 17.11.2026 za zgodą Jakuba): Kenney Interface Sounds (100 plików OGG, CC0), Kenney UI SFX Set (51 WAV, CC0) i 19 wybranych swooshy i pyknięć z Mixkit (Mixkit Sound Effects Free License, bez podpisu). Pomiary każdego pliku (długość, jasność, moment szczytu) są w `pomiary.json` w tym folderze: wybierałem po nich, bo nie mogę dźwięków odsłuchać, więc ostateczny dobór zatwierdza Jakub uchem.

`scripts/sfx.py` ma pięć typów, każdy z 2–4 wariantami branymi po kolei:

| Typ | Do czego | Wyrównanie | Szczyt |
|---|---|---|---|
| `pop` | wyskakujący napis, kafelek, liczba | start próbki klatkę po obrazie | −20 dBFS |
| `tik` | ptaszek, podziałka, kropka, mała zmiana | jak wyżej | −25 dBFS |
| `swoosh` | wejście planszy, przejście | szczyt próbki na trafieniu obrazu | −21 dBFS |
| `shh` | rysowanie wykresu lub linii (pole `dl` = czas ruchu) | start razem z ruchem, nie dłużej niż ruch | −24 dBFS |
| `powiad` | powiadomienie | start klatkę po obrazie | −20 dBFS |

Zasady z rozpoznania: dźwięk nigdy przed obrazem, swoosh nie może przeżyć swojego ruchu, ten sam plik nie pada dwa razy pod rząd, najwyżej 8–12 efektów na minutę. Część szablonów z katalogu wysyła zdarzenie `hf:sfx` z nazwą dźwięku w chwili trafienia (`iris-land-soft`, `notification-pop`, `badge-pop-soft`, `whip-cut`): to podpowiedź, gdzie w szablonie jest moment na dźwięk.

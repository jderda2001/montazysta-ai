# IMG_0591 „Szczęście, plan czy pragnienie” (rolka organiczna, personal brand)

Montaż 17–18.11.2026. Cztery pliki: hook A i hook B, każdy w wersji z efektami i w wersji „tylko napisy” (prośba Jakuba: „jedną pociętą tylko z napisami, a drugą normalnie z efektami”). Pierwsza rolka zmontowana z nową biblioteką grafik, rotacją przejść i efektami dźwiękowymi.

## Źródło

- `~/Downloads/IMG_0591.MOV`: przednia kamera iPhone'a, 4K 60 kl./s, 6 min 17 s, dźwięk z mikrofonu krawatowego w tym samym pliku (offset 0).
- **Obraz jest lustrzany** (tytuł „Zero to One” czyta się wspak), więc `aroll.py` odbija każde ujęcie (`hflip`).
- **Kadr jest niski:** twarz zajmuje 40–72% wysokości, nad głową jest pusty sufit. Dlatego kadry są dosunięte do dołu (W 1,0 / M 1,12 / C 1,25), napisy stoją na 1420 px zamiast 1120, a nakładki idą nad głowę.

## Struktura

Plan Jakuba zakładał ok. 65 s, nagranie ma treści na ok. 150 s. Zostały wszystkie punkty planu, wypadły powtórzenia i dygresje. Wynik po poprawce z 18.11: 92,6 s (A) i 91,5 s (B); wersje „tylko napisy” 90,5 i 89,4 s.

- **Hook A:** „Według Petera Thiela Europa siedzi w najgorszej ćwiartce sukcesu, no i Ty w sumie razem z nią.”, potem cytaty Buffetta i Bezosa.
- **Hook B:** nagrany inaczej niż w planie. Zamiast „Buffett mówi, że wygrał loterię genetyczną…” Jakub przeczytał pełne cytaty, więc wersja B zaczyna się od cytatów Buffetta i Bezosa i ma dodatkowo Gatesa. Zdania o Europie w niej nie ma.
- **Wspólne body (kwestie 2–20):** Zero to One i pytanie Thiela, „nie jesteś losem na loterii”, dwie osie, USA lat 50. i 60. (drogi, Księżyc), USA od lat 80., Chiny, Europa, „liczy się plan”, dwie połowy (plan i palące pragnienie, Napoleon Hill), dowód osobisty, pytanie do widza.

Wycięte: Empire State Building i Golden Gate (177 s), Projekt Manhattan (187 s), druga połowa zdania o Chinach („dlatego robią wszystko, żeby zminimalizować ryzyko”), „gdy mamy plan i gorące pragnienie, wszystko jest do zdobycia…” (302–316 s), „te słowa Hilla i Thiela mają pokrycie w mojej osobie” (355 s), podsumowanie cytatów „najwięksi mówią, że to szczęście” (106 s), Gates w wersji A.

Jakub mówi „palące pragnienie”, nie „płonące” ani „głód” jak w planie, i „klub szczęśliwej spermy” zamiast „loteria genetyczna”. Napisy i grafiki idą za nagraniem. Dowód osobisty to wersja o 16–17 roku życia, wolności i biznesie online (historia o Norwegii z planu nie pada).

## Falstarty i urwane słowa

- 336,48 „Chcę wolność? Nie. Ja od zawsze, czyli ja”: kwestia startuje od „od praktycznie” (339,80).
- 206,60 „a w 70…” po „w 61,”: kwestia kończy się na 206,40.
- 292,41 „Drugą” po „to jedna połowa.”: kwestia kończy się na 292,22.
- 354,37 „Także” po „gdzie jestem.”: kwestia kończy się na 354,18.
- 172,83 oddech po „optymizm.”: kwestia kończy się na 172,72.

Trzy środkowe przepuściłem przy pierwszym przebiegu: `kawalki.py` je pokazał, ale uznałem je za halucynacje, bo obwiednia na samym końcu kwestii była cicha. Wyszły ponownie w transkrypcji gotowego pliku i dopiero osobny whisper na samej końcówce je potwierdził.

## Poprawka 18.11.2026: powtórka i zacięcia

Jakub po obejrzeniu: „powtórzyłem i zaciąłem się w niektórych miejscach, przejrzyj i popraw”. Znalezione drobniejszym podziałem (`kawalki.py --drobne`) i pomiarem głosek (`fonemy.py`):

- **Kwestia 3, zdanie dwa razy pod rząd:** 82,57–84,69 „gdzie autor pyta: sukces to szczęście czy umiejętn…”, potem całe od 85,06. Zostaje drugie podejście (85,06–87,44). Prompt i DTW w `slowa.py` ukryły powtórkę, rozciągając „szczęście” na 1,5 s.
- **Hook A, „sukce- cesu”:** powtórzona sylaba w środku słowa. Wycięte 14,2567–14,40 (od końca pierwszego „c” do początku drugiego), w miejscu cięcia zbliżenie W → C. Z siedmiu wariantów cięcia tylko ten whisper słyszy jako „sukcesu” w każdym kontekście.
- **Kwestia 16, „do… kładnie”:** pauza 0,15 s w środku słowa. Wycięta sama pauza (343,3333–343,42), bez zmiany kadru (skok 2–3 klatek).

Pierwszy render poprawek był zły w dwóch miejscach i wyszło to w kontroli eksportu: w kwestii 16 wyciąłem „do”, biorąc pauzę za powtórzoną sylabę (zostało „wiedziałem kładnie”), a skrócony ogon kwestii 15 zjadł „Hill”. Obie rzeczy cofnięte, drugi render jest czysty.

Zostawione świadomie (styl albo brak innego dubla): wolno wymówione „utożsamiam” (297,9–298,6), westchnienie „Europa, no… co ja mogę rzec?”, szybkie, niewyraźne „A Ty co myślisz?” (368,03–368,44), „No i…” z pauzą przed „można powiedzieć”.

Cięcia ze środka kwestii to nowe pole `wytnij` w `SEGS` (`aroll.py`); `czesci.py` daje pozostałym skryptom dźwięk kwestii po wycięciu. Grafika pytania Thiela trwa teraz do 0,9 s po wejściu kwestii 4, bo sama kwestia 3 skróciła się do 2,6 s. Kopie skryptów sprzed poprawki: `_przed_poprawka_zaciec/`.

## Wersja z efektami

Grafiki (czasy ze słów): hasła nad głową w hooku (EUROPA, NAJGORSZA ĆWIARTKA, nazwiska z cytatami), chip książki, szablon z biblioteki `kinetic-type-swap` („Sukces to szczęście? / umiejętności?”), cytat „Nie jesteś losem na loterii”, macierz 2×2 „Plan × wiara” w dwóch wejściach (ćwiartki zapalają się, gdy o nich mówi; Europa na biało), licznik „32 tys. km”, oś czasu lotu na Księżyc 1961 → 1972 z licznikiem 12 osób, pigułki „optymista / pesymista / liczy się plan”, pierścień „Dwie połowy”, hasło „16–17 lat”, trzy kafelki, trzy odpowiedzi i plansza końcowa „Daj znać w komentarzu”.

Przejścia plansz: iris, wipe, zoom, diag (każde raz). Dźwięki: ok. 33 na film, ok. 21 na minutę (`analiza/sfx_efekty.json`).

Poglądowe elementy: etykiety ćwiartek („plan + optymizm” itd.) to streszczenie tego, co mówi, a nie cytaty. Podpisy pod nazwiskami są skrótami cytatów.

## Wersja „tylko napisy”

Te same cięcia, napisy słowo po słowie przez cały film (hook też), bez grafik, bez dźwięków i bez planszy końcowej. Film kończy się pół sekundy po ostatnim słowie.

## Uruchamianie

- `./caly.sh .` albo `./caly.sh hookB`: A-roll, falstarty, czasy słów, potem obie wersje.
- `./render.sh <folder>`: sama kompozycja, check, render i kontrola obu wersji (`hf/` = efekty, `hfn/` = napisy). Ze zmienną `HF_ZNACZNIK` (ścieżka pliku-znacznika) sprząta po każdym renderze klatki z katalogu tymczasowego.
- `uv run --no-project --with numpy python3 -I skrypty/kawalki.py [--drobne]`: falstarty, powtórki i zająknięcia; wynik drobnego sita w `analiza/kawalki_drobne.log`.
- `python3 -I skrypty/kompozycja.py efekty|napisy`: tylko kompozycja.

## Wersja w strefie bezpiecznej (18.11.2026, po prośbie Jakuba „przerób też rolkę o Thielu pod nową strefę”)
Pierwsze eksporty (9:36 i poprawka z 11:12, cięcia bez zmian) miały napisy na 1420 px i grafiki od 100 px, czyli poza strefą Instagrama (`SKILL.md` montaz-rolek, zasada 9). Przeróbka powstała w kopii `IMG_0591_strefa/`, bo druga sesja poprawiała wtedy cięcia (cięcia w obu wersjach są te same, sprawdzone `diff` na `HOOKS`); skrypty wróciły tutaj, stare leżą w `_przed_strefa/`. Gotowe pliki i rendery: `IMG_0591_strefa/{hf,hfn,hookB/hf,hookB/hfn}/renders/final.mp4`.
- **Kadr z pomiaru twarzy:** broda siedzi nisko (62–76% wysokości, mediana 69%), więc napisy pod brodą w strefie wymagają zbliżenia. `skrypty/twarze.py --flip` mierzy twarz co 0,4 s (Vision z macOS), `kadr()` w `aroll.py` dobiera zoom tak, żeby broda kończyła się najniżej na 1200 px (zoom 1,15–1,6). Przy pochyleniu do kamery napisy zachodzą na sam dół brody (jest przyciemnienie pod nimi).
- **Napisy:** 1160 px, szerokość 620 px, frazy dzielone automatycznie do ok. 21 znaków (`rozbij()`), przyciemnienie pod napisami 0,44 (biała koszulka).
- **Grafiki:** nakładki z górnego pasa od 285 px (było 96–230), macierz 2×2 w kolumnie 690 px (skala 0,734 w `.mxw`), pierścień „Dwie połowy” mniejszy, kafelki 290 px, plansza końcowa wyżej. Podpis „Napoleon Hill” pod pierścieniem usunięty, bo napis stoi teraz tuż nad nim.
- **Kontrole:** `strefa.py` 210 klatek (A) i 217 (B), 0 poza strefą po dwóch poprawkach (pulsująca komórka „Europa” sięgała 6 px za 885 px, descendery napisów 3 px za 1245 px). `hyperframes check` 0 błędów, głośność −14,1 LUFS, brak powtórzeń w transkrypcji.
- **Do oceny przez Jakuba:** twarz jest bliżej niż w pierwszych eksportach, a hasła nad głową (BUFFETT, BEZOS, cytat) przy zbliżeniach zachodzą na włosy.


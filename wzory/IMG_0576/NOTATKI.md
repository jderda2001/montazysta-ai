# IMG_0576 „10K vs 100K” (rolka organiczna, personal brand)

Montaż 17.11.2026. Pierwsza rolka w palecie personal brandu: czerń, biel, ciemny szary i akcent `#00E5A0` (`MARKA = "personal"` w `skrypty/kompozycja.py`).

## Źródło

- Wideo i dźwięk: `~/Downloads/IMG_0576.MOV` (iPhone, 4K 60 kl./s, po obrocie 2160×3840, SDR bt709, 6 min 38 s).
- Osobnego nagrania z mikrofonu nie ma. Jakub ma mikrofon krawatowy podpięty do telefonu, więc dźwięk idzie z pliku wideo: `AUDIO = VIDEO`, `analiza/sync.json` ma offset 0, a `sprawdz_sync.py` pokazuje 0 ms.
- Kadry ze źródła 4K: W 1,0 / M 1,2 / C 1,4 (twarz ok. 1060, 1450).

## Dwie wersje

- **Hook A** (folder główny): „Pierwsze 100 tysięcy jest 10 razy łatwiejsze niż pierwsze 10 tysięcy złotych w miesiąc.” (33,20–37,55 s, jedyny pełny dubel).
- **Hook B** (`hookB/`, ten sam zestaw skryptów z `HOOK = "B"`): „Pierwsze 10 tysięcy w miesiąc jest 10 razy trudniejsze niż pierwsze 100 tysięcy.” (46,49–49,96 s, ostatni dubel; wcześniejszy kończył się na „100 koła”). Końcówka „tysięcy” jest w nagraniu ściszona (po 49,80 s poziom spada do ok. −45 dB i trwa do 49,97), więc `kawalki.py` pokazuje po niej osobny kawałek „Dziękuję.” (halucynacja), a `slowa.py` zapisuje słowo jako „tysi.” niezależnie od miejsca cięcia. Napis poprawia `FIX`, a cięcie zostaje na 49,96, żeby końcówka była cała.
- Cały przebieg dla jednego wariantu: `./przebieg.sh .` albo `./przebieg.sh hookB` (A-roll, falstarty, głos C, czasy słów, kompozycja, check, render, kontrola).

## Wybór dubli i falstarty

Zasada: ostatni pełny dubel każdej kwestii. Falstarty złapane przez `kawalki.py` i kontrolę eksportu:

- 66,27 „Większość myśli tak. Jeśli…” i powtórka od 68,21: kwestia startuje od powtórki.
- 178,38 „Wie, skąd biorą” i powtórka od 179,84.
- 202,47 samotne „I” z pauzą: kwestia startuje od „Tu właśnie” (203,00).
- 305,98–306,43 króciutkie „t-” przed „ta sama maszyna”: kwestia rozcięta w tej pauzie na dwie. Whisper na surowym dźwięku tego nie pokazał, wyszło dopiero w transkrypcji gotowego pliku.
- 149,03 szmer po „żart”: kwestia kończy się na 148,88.

Niewykorzystane warianty:

- „Na starcie nie masz nic…”: pięć nieudanych podejść (95–116 s), użyte ostatnie (117,19).
- „I co najważniejsze, ma proces, który umożliwia mu powtarzanie tego” (184,88): dłuższa wersja, użyta krótsza (188,40).
- „Więc jeśli jesteś na etapie 500 zł w kieszeni” (330,01): urwane, użyta wersja „pierwszych paru tysięcy” (349,42).
- „U mnie setki reklam tygodniowo” (231,20): urwane. W użytej wersji nie pada „100 tygodniowo” ze skryptu, tylko „setki nowych reklam, dla mnie i dla każdego z moich klientów”.

Co Jakub powiedział inaczej niż w skrypcie (napisy idą za nagraniem): „ponad dwudziestu czterech” agentów „w samym adGenie”, „pięć stów wlatuje na Twoje konto”, „uwierz, wiem, co mówię”, zakończenie z „skup się na tym, żeby pozyskiwać klientów”.

## Głos

Ostatecznie głos naturalny (`audio/aroll.wav` po limiterze −1,8 dBFS), bo po pierwszej wersji Jakub napisał, że AI na głosie jest za dużo. Pierwsza wersja miała wariant C (Sidon + łańcuch radiowy); pliki zostały w `audio/`. Po pomiarze widma względem głosu C z IMG_0526 środek i góra były 2–5 dB niżej, więc w `skrypty/studio.py` łańcuch `DEEP` ma dół +5,5 dB zamiast +7,5 i dodatkową półkę +2,5 dB od 5 kHz. Po korekcie różnica w pasmach mieści się w ±1,7 dB.

`waliduj_napisy.py` zgłasza tu kilkadziesiąt słów, ale to fałszywe alarmy: whisper na krótkich wycinkach zapisuje „10 tysięcy” jako „10 000” albo „dziesięć tysięcy” i walidator gubi dopasowanie reszty zdania. W każdym zgłoszeniu słowo było już słyszalne w swoim czasie.

## Grafiki (wszystkie czasy liczone ze słów)

1. Hook kinetyczny: małe słowa fraza po frazie i stałe duże „100K vs 10K” (w hooku B „10K vs 100K”), 100K w akcencie.
2. Wykres „Jak to liczą”: prosta 10K / 1 rok → 100K / 10 lat, przekreślona na „odpuszczają”, potem krzywa w akcencie na „to nie rośnie liniowo”.
3. Kafelki z białym „×”: produkt, proces, dowód, że działa.
4. Powiadomienie „Pierwsza sprzedaż, + 500 zł” (poglądowe, kwota z nagrania).
5. Paski „Z perspektywy 500 zł”: 500 zł, 10 000 zł (kosmos), 100 000 zł (żart), w proporcji.
6. Chip „Mój start: 500 zł”.
7. Kafelki z ptaszkami: za co ludzie płacą, skąd klienci, proces.
8. Plansza „10× więcej przychodu”: kiedyś 10× ludzi, dziś powtarzanie robi AI.
9. Chipy „Setki reklam: robi AI” i „Zamiast etatu: kolejny agent”.
10. Plansza „24+ agentów AI” z awatarami czterech agentów (z `IMG_0529/branding`).
11. Chip „Pierwsze 10K: budowa maszyny” i plansza „Ta sama maszyna” (10× więcej ludzi przekreślone, AI).
12. Chipy kroków „1 Zbuduj proces”, „2 Daj go AI”.
13. Plansza końcowa „10K → 100K”, „Zbuduj proces. Daj go AI.”, podpis. Bez logo i bez CTA, bo w nagraniu nie pada wezwanie do komentarza.

Czego nie ma: zrzutu agenta albo kreacji z PerfOS, o który prosił skrypt. Nie dostałem takiego pliku, więc w tym miejscu jest chip i plansza z awatarami.

## Do sprawdzenia przez Jakuba

- „uwierz, wiem, co mówię” w napisach (trzy transkrypcje dały trzy wersje, ta jest z oczyszczonego dźwięku).
- Plansza końcowa bez CTA.
- Długość ok. 93 s.

## Ocena

17.11.2026, wersja po poprawkach (bez kwadratów, wykres z rozbudowaną animacją, głos naturalny): „super podoba mi się”.

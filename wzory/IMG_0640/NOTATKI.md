# IMG_0640 „Mit przedsiębiorczości, graf adGen” (rolka organiczna, personal brand)

Montaż 19.11.2026. Jedna wersja, 77 s (scenariusz zakładał 45–60 s; treści w nagraniu jest na tyle, nic merytorycznego nie wypadło).

## Źródło

- `~/Downloads/IMG_0640.MOV`: tylna kamera iPhone'a, 4K 60 kl./s (zakres tv), 5 min 37 s, dźwięk z mikrofonu krawatowego w tym samym pliku (offset 0). Obraz nie jest lustrzany (napisy na kartce czytają się normalnie).
- Trzy ujęcia w jednym pliku: hook ze statywu (46–67 s), kartka z grafem z góry (113–284 s), puenta i CTA z ręki przy oknie (284–335 s).

## Cięcia (ostatni pełny dubel)

- Hook: 52.15 („Zakładasz swoją pierwszą firmę?…”); wcześniej 46.15 falstart z „to jedna rada”. „Dobra, to lecimy” ze scenariusza nie padło.
- „Po pierwsze…”: 124.00 falstart, użyte 134.35 (trzy punkty jako jedna kwestia, zmiany kadru w pauzach).
- Growth: 158–176 kilka falstartów. „Na przykład w Growth… mamy” (162.35) porzucone, zdanie od nowa o 164.24, koniec przed „W Sales” (166.23).
- Delivery i HR to jedna ciągła wypowiedź (219.44–231.54).
- Administracja: 235.03 falstart, użyte 239.08. „Inicjał przy kratce”: 256.96 i 262.11 falstarty, użyte 268.19.
- Puenta „Narysuj swój graf”: duble 295.70, 299.26, 307.81, użyty ostatni 312.78.
- „Kratka to odpowiedzialność, nie etat” mówi, podnosząc telefon znad kartki (do 285.0 kartka i szarpnięcie obrazu): ten moment przykrywa plansza.
- Kontrola falstartów: `kawalki.py` w obu trybach, jedyny alarm (POWTÓRKA przy Growth) rozstrzygnięty sondami i obwiednią.

## Kadry

- Hook: W pełny, M 1,15, C 1,30 wokół twarzy (pomiar `twarze.py`: broda do 1910 px źródła, czyli ok. 955 px wyjścia; hook kinetyczny od 975 px).
- Kartka: G pełny, GM 1,15. Pod napisami miękki ciemny podkład (`.scrim`), bo biały napis znikał na białym papierze. Wygląd napisów bez zmian.
- Z ręki: broda na 63–74% wysokości źródła, więc zbliżenia 1,3 dosunięte do dołu (S2, S3). S1 (1,5) w kwestii 11 jest pod planszą.

## Grafiki (czasy ze słów)

- Nagłówek ze scenariusza na ciemnych pigułkach nad głową: „TWOJA FIRMA TO KORPORACJA.” (słowo zapala się na „korporacji”) i „NAWET JAK JESTEŚ SAM.” (tekst ze scenariusza, nie pada w nagraniu).
- Hook kinetyczny: „Zakładasz swoją / PIERWSZĄ FIRMĘ?”, „Musisz myśleć o niej od razu jak o / KORPORACJI”.
- Chip książki „MIT PRZEDSIĘBIORCZOŚCI”, błysk światła na cięciu do kartki.
- Karty nad kartką: „LUDZI < KRATEK” + „KAŻDA POZYCJA ROZPISANA” → „PO CO?”; lista 1. WIZJA / 2. ODPOWIEDZIALNOŚĆ / 3. REKRUTACJA; kratka z przekreślonym człowiekiem → „AGENT AI”; „INICJAŁ = CZŁOWIEK / AI ROBI / CZŁOWIEK ODPOWIADA”; rysujący się graf „NARYSUJ GRAF → ZATRUDNIJ”.
- Plansza „graf działów” (kwestie 5–8): Growth (Sales: Grok, Marketing: PerfOS), Delivery (KAM: Grok, Project Manager: Claude Cowork, PerfOS), HR (Grok), Administracja (Grok, Claude). Dział podświetla się, gdy go nazywa, agent wpada na swoim słowie. Wszystko z nagrania; „kampanie na Mecie” ze scenariusza w nagraniu nie padły.
- Plansza „KRATKA TO ODPOWIEDZIALNOŚĆ / NIE ~~ETAT~~”, pole komentarza („Moje kratki:”), plansza końcowa „ILE KRATEK? / Daj znać w komentarzu”.
- Przejścia plansz: iris, wipe, zoom. Szablony z biblioteki: żaden (wszystko własne, pod treść).

## Napisy

- „część tych kartek”: Jakub powiedział „kartek” (przejęzyczenie), w napisie „kratek” (`FIX`).
- Whisper: „Kia Kanta” → „KAM-a”, „Perfosa” → „PerfOSa”, „krajce” → „kratce”, „EA” → „AI”.

## Render

- Klatki A-rollu wypakowywane jako JPG (`--video-frame-format jpg`), bo na dysku było 4–8 GB wolnego, a PNG potrzebowałyby ok. 4,6 GB.

## Uruchamianie

```bash
python3 -I skrypty/aroll.py && ln -f aroll/aroll.mp4 hf/aroll.mp4
uv run --no-project --with numpy python3 -I skrypty/slowa.py
python3 -I skrypty/kompozycja.py
uv run --no-project --with numpy python3 -I skrypty/strefa.py
cd hf && ~/.local/bin/hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format jpg
```

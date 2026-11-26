# Indeks pamięci montażysty

Jedna linijka na notatkę. Przy sprzeczności wygrywa nowsza data, a ponad notatkami stoją `ZASADY.md` i `SKILL.md` (zob. `../README.md`).

- [Skill montaz-rolek](skill-montaz-rolek.md) — ~/.claude/skills/montaz-rolek = cały proces i styl; po każdym filmie dopisz ocenę do references/dziennik.md
- [Video tools setup](video-tools-setup.md) — gdzie leżą ffmpeg/yt-dlp/whisper/HyperFrames/Remotion i jak je zainstalowano (bez brew); wspólna kolejka renderów HyperFrames i pamięć klatek zapychająca dysk
- [adGen video style](adgen-video-style.md) — jak montuję reklamy adGen: foldery, styl z referencji, branding (bez logo), nazwy plików; najnowszy wzór z hookami A/B/C to projekty/IMG_0583
- [Zatwierdzony styl rolek](feedback-reel-style-approved.md) — montaż IMG_0526 to wzór na kolejne filmy; NIGDY logo adGen (personal brand); bez kwadratów na planszach, wykresy mocno animowane
- [Paleta marki](feedback-paleta-marki.md) — personal brand: czerń, biel, ciemny szary + akcent #00E5A0, ciemny tekst na akcencie; dotyczy też miniatur; reklamy adGen zostają pomarańczowe
- [Różnorodność grafik i SFX](feedback-roznorodnosc-grafik.md) — przejścia nie mogą się powtarzać, biblioteka ok. 50 szablonów w skillu; subtelne dźwięki pod animacje z Muzyka/SFX przez sfx.py, poziomy zatwierdzone 17.11.2026
- [Falstarty w dublach](feedback-false-starts.md) — whisper wygładza falstarty i powtórki; kawalki.py w obu trybach + powtorzenia.py na całej rolce (tekst + akustyka), każdy alarm rozstrzygnij
- [Brzmienie głosu](feedback-voice-sound.md) — od 17.11.2026 głos naturalny z mikrofonu, bez Sidona (ma dobre mikrofony); wariant C tylko na prośbę
- [SFX i synchronizacja napisów](feedback-sfx-and-caption-sync.md) — bez syntetycznych whooshy; czasy słów z DTW (-nfa!) per kwestia; montuje w Premiere
- [Osobne audio z mikrofonu, rolki](separate-mic-audio-reels.md) — wideo z iPhone'a + audio z mikrofonu: synchronizacja korelacją; rolki organiczne z CTA komentarz; najnowsze skrypty w IMG_0526
- [YouTube poziomo](feedback-youtube-poziomo.md) — long-form na YouTube zawsze 16:9 (4K), rolki zostają pionowe
- [Long-form IMG_0529](longform-youtube-img0529.md) — pierwszy odcinek YouTube (seria o zautomatyzowanej firmie): pipeline warstw, pułapki Dyktafonu, rzeczy do potwierdzenia
- [Long-form = +3 rolki](feedback-longform-3-rolki.md) — przy każdym wideo >10 min od razu 3 pionowe rolki promo po 10–15 s, w stylu rolek
- [Muzyka lo-fi w long-formie](feedback-muzyka-lofi.md) — cichy lo-fi z Biblioteki audio YouTube (folder Muzyka), ok. 20 dB pod głosem z duckingiem
- [Porządek w Eksporty](feedback-eksporty-porzadek.md) — podfoldery YouTube / Rolki / Reklamy adGen, folder na film, surowe nagrania tylko w Nagrania
- [Skill miniatury](skill-miniatury.md) — ~/.claude/skills/miniatury = cały proces miniatur YouTube; klucz kie.ai w ~/.config/kie/api_key; oceny i wyniki testów do references/dziennik.md
- [Miniatury: 3 warianty A/B + tytuły](feedback-miniatury-ab.md) — zawsze 3 miniatury pod test A/B, do każdej 2 propozycje tytułu; osobny skill, skilla montażu nie ruszać
- [Opisy rolek i teksty reklam: 2 propozycje](feedback-opisy-rolek.md) — przy każdym montażu rolek 2 propozycje opisu, przy każdej reklamie adGen 2 propozycje tekstu („Tak, zawsze”, 17.11.2026); reguła tylko w pamięci, skilla montażu nie edytować
- [Long-form = +3 miniatury](feedback-longform-miniatury.md) — przy każdym long-formie od razu 3 miniatury A/B skillem miniatury, bez pytania; skilla montażu nie edytować
- [Agenci: model i effort](feedback-agenci-model-i-effort.md) — przy zlecaniu agentom dobieraj model i effort do zadania (Sonnet zamiast Fable, gdzie wystarczy), bez straty jakości
- [Safe zone w rolkach](feedback-safe-zone.md) — treść w strefie y 270–1245, x 70–1010 z wcięciem na przyciski; napisy 620 px; przed renderem strefa.py (18.11.2026)
- [Rolki PerfOS](perfos-rolki-branding.md) — branding z perfos.pl (Geist, #0f0f0f, #00E5A0, logo), pliki i wzór w projekty/IMG_0597; logo i paleta w skillu do potwierdzenia
- [Napięcie i tempo cięć](feedback-napiecie-i-tempo-ciec.md) — przed puentą pauza i najazd; styki ciasne: ok. 0,15 s ciszy (start głosu −40 dB, +0,10 po zdaniu), od 24.11.2026
- [Jasność obrazu](feedback-jasnosc-obrazu.md) — przed gradingiem zmierz YAVG; ciemne nagrania rozjaśniaj (gamma 1,34), nie przyciemniaj (IMG_0688, 20.11.2026)
- [Nazwy własne = grafika](feedback-nazwy-wlasne-grafiki.md) — osoba → zdjęcie, firma/produkt → logo, książka → okładka; pobieram bez pytania do Grafiki/ (20.11.2026)
- [Repo montazysta-ai](repo-montazysta-ai.md) — skille są linkami do prywatnego repo wspólnego z Maciejem; przed montażem pull, po zmianie w skillu commit + push, nowe zasady też do ZASADY.md
- [Cenzura przekleństw](feedback-cenzura-przeklenstw.md) — zawsze: piknięcie 1 kHz, „#@!%&” w napisie, czarny pasek na ustach (23.11.2026, wzór IMG_0720)
- [Styl premium](feedback-styl-premium.md) — od 24.11.2026: 60 kl./s, max 2 sceny/30 s, płynne zoomy, jasne/szklane wstawki z kurtyną, Liquid Glass CTA i plansze końcowe (wszystkie w rotacji); wzorce i zdjęcie profilowe w Referencje i wytyczne/ (Rolki wzorcowe, Zdjęcie profilowe)
- [Pierwsze 2 sekundy](feedback-pierwsze-2-sekundy.md) — zasada 11: hook w całości od klatki 0 (hook0), puenta w 1,5 s, hasło pod widza, zawsze hook A i B do Próbnych rolek; statystyki do dziennika (24.11.2026)
- [CTA „zaobserwuj”](feedback-cta-obserwuj.md) — od 24.11.2026 domyślne CTA rolek to obserwowanie, bez słów-kluczy i automatyzacji; tryb „obserwuj” w cta.py skilla (od 25.11.2026 w repo)
- [Logika rolki i przejścia](feedback-logika-i-przejscia.md) — kwestie układaj według sensu i scenariusza, nie tylko ostatni dubel; dwie sceny pod rząd przenikaniem; liczniki bez zer (24.11.2026)
- [Skill scenariusze-rolek + całe repo](skill-scenariusze-i-repo-komplet.md) — 25.11.2026: scenariusze robi skill scenariusze-rolek; w repo ma być dosłownie wszystko (kontekst/, pamięć, wzory C45xx), bo montaż przejmuje osobny agent
- [Pierwsze 5 s i sklejka podejść](feedback-pierwsze-5-sekund-sklejka.md) — 25.11.2026 HOOK A C4537_v2 zdjęty ze wszystkich platform (sklejka dwóch podejść w ciągłej mowie); hook z jednego podejścia, `poczatek.py` na każdej wersji przed oddaniem
- [Każde cięcie w całym filmie](feedback-kazde-ciecie.md) — od 26.11.2026 `ciecia.py` na każdej wersji; pierwsza kontrola 17 plików: urwane „pracu(ję)” (C4538) i „zajebist(e)” (IMG_0720), poprawki obok; o urwanej końcówce rozstrzyga obwiednia, nie whisper
- [Okładka jako plik w folderze rolki](feedback-okladka-plik.md) — 26.11.2026 przy publikacji „AI nie zabierze Ci klientów” zabrakło okładki; do każdej wersji `<Tytuł>_HOOK X_MM.RR - okładka.jpg` obok mp4, wzór `wzory/okladka-C4537_v2/`

#!/usr/bin/env python3
"""Generuje ../hf/index.html (HyperFrames) dla rolki C4534 "81 mld $ na Twoja konkurencje" (skrypt 1, AI i biznes):
haslo od klatki 0, napisy, scena A (jasna: Claude/Anthropic na gieldzie, rekordowe IPO, kurs +34%), najazdy na twarz,
scena B (szklo: inwestorzy 81 mld $ vs Ty 80 zl / mies.), plansza "profil" w trybie obserwuj.
Dodatkowo ../napisy.srt (frazy napisow, do Premiere / uploadu).

Uzycie: python3 -I kompozycja.py
"""
import html
import json
import os
import re
import subprocess
import shutil
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Glos w rolce: naturalny dzwiek z mikrofonu po lekkim masteringu z aroll.py (highpass 70 Hz, kompresja 2,5:1, -14 LUFS).
# Jakub 17.11.2026: "za bardzo uzywasz voice enhancer AI, kupilem dobre mikrofony, bez tego albo z duzo mniejszym filtrem".
# Wariant C (Sidon + lancuch radiowy, studio.py) tylko na zyczenie albo przy zlym nagraniu: plik audio/aroll_studio_gleboki.wav.
# Wideo A-rollu idzie bez dzwieku, glos jako osobna sciezka <audio> (ta sama os czasu co aroll.wav).
GLOS = P / "audio/aroll.wav"
# Dwie palety, ten sam uklad i ruch. MARKA wybiera, w ktorej jest caly film:
#   "personal" - personal brand Jakuba (rolki, long-form, rolki promo): czern, biel, ciemny szary + akcent #00E5A0
#   "adgen"    - reklamy adGen (Eksporty/Reklamy adGen): akcent pomaranczowy #ff7018, jak w IMG_0361 / IMG_0526
# accent    - kolor akcentu; inny akcent pod temat filmu (tylko "personal") = zmiana tej jednej wartosci
# on_accent - tekst i ikony NA akcencie (bialy na #00E5A0 ma kontrast 1,6:1, wiec tam ciemny; na pomaranczu bialy)
# ok        - kolor "zrobione" (ptaszki, pigulka potwierdzenia); None = akcent
PALETY = {
    "personal": {"accent": "#00E5A0", "on_accent": "#0f1012", "ok": None},
    "adgen": {"accent": "#ff7018", "on_accent": "#ffffff", "ok": "#3ddc84"},
}
MARKA = "personal"
HOOK = "B" if (P / "HOOK_B").exists() else "A"
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import cta  # noqa: E402  (skrypty/cta.py = scenariusze/narzędzia/cta_obserwuj.py)

# ---------------------------------------------------------------- strefa bezpieczna (safe zone), kadr 1080x1920
# Czesc wspolna dwoch szablonow, ktore Jakub przyslal 18.11.2026 ("napisy i animacje czasem sa za wysoko badz za szeroko"):
#   Instagram Reels: gora 14% (269 px), dol 35% (672 px), boki 6%, wciecie na przyciski od 1147 px w dol (x <= 850)
#   Jon Loomer (Reels i Stories, reklamy Meta): gora 13%, dol 20%, prawa kolumna przyciskow od 860 px w dol (x <= 887)
# W strefie lezy wszystko, co widz ma przeczytac albo zobaczyc: napisy, hasla, liczby, karty, logo, pole CTA.
# Poza strefa moze byc tylko wideo, tlo plansz i dekoracje. Opis i rysunek: references/styl.md, punkt 8.
# Kontrola gotowej kompozycji: scripts/strefa.py (obrys na klatkach i automatyczne wykrywanie wyjsc poza strefe).
SAFE = {"top": 270, "bottom": 1245, "left": 70, "right": 1010,
        "wciecia": [(860, 885), (1145, 850)]}  # (od tej wysokosci w dol, prawa krawedz): serce / komentarz / udostepnij
CAP_TOP = 1120  # gorna krawedz linii napisow; przesuwaj tylko w granicach strefy (np. gdy na napisy wchodzi broda)
CAP_MIN = 52    # fraza, ktora wymaga mniejszej czcionki, jest za dluga: podziel ja w PHRASES
KIN_TOP = 900   # gora bloku hooka: do 2 linii malych slow (126 px) + haslo (139 px) + linia dopowiedzenia (66 px) = 331 px
STREFA = os.environ.get("STREFA") == "1"  # tryb kontrolny dla strefa.py: same grafiki na czarnym tle, bez wideo i poswiat


def safe_right(y0, y1):
    """Prawa krawedz strefy (px) dla pasa y0..y1."""
    return min([SAFE["right"]] + [x for y, x in SAFE["wciecia"] if y1 > y])


def safe_w(y0, y1, srodek=540):
    """Najwieksza szerokosc elementu wysrodkowanego na `srodek`, ktory zajmuje pas y0..y1. Pas poza strefa = blad."""
    if y0 < SAFE["top"] or y1 > SAFE["bottom"]:
        raise SystemExit(f"Poza strefa bezpieczna: pas {y0}-{y1} px, dozwolone {SAFE['top']}-{SAFE['bottom']}")
    return int(2 * min(srodek - SAFE["left"], safe_right(y0, y1) - srodek))


CAP_W = safe_w(CAP_TOP, CAP_TOP + 73)   # linia napisow 66 px x 1,1; przy 1120 px wychodzi 620 px
KIN_W = safe_w(KIN_TOP, KIN_TOP + 340)  # caly blok hooka (konczy sie przed 1245 px); wychodzi 620 px

ICON = {
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22 11 13 2 9z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "palm": '<path d="M13 8c0-2.76-2.46-5-5.5-5S2 5.24 2 8h2l1-1 1 1h4"/><path d="M13 7.14A5.82 5.82 0 0 1 16.5 6c3.04 0 5.5 2.24 5.5 5h-3l-1-1-1 1h-3"/><path d="M5.89 9.71c-2.15 2.15-2.3 5.47-.35 7.43l4.24-4.25.7-.7.71-.71 2.12-2.12c-1.95-1.96-5.27-1.8-7.42.35"/><path d="M11 15.5c.5 2.5-.17 4.5-1 6.5h4c2-5.5-.5-12-1-14"/>',
    "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
    "up": '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "alert": '<path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
}


def icon(name, size, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def kolory(page, marka=None):
    """Wstawia palete do szablonu: akcent, {{ACCENT_RGB}} (pod rgba), {{ACCENT_HI}} (jasny koniec gradientu),
    kolor tekstu na akcencie i kolor "zrobione". Reszta CSS korzysta tylko ze zmiennych, bez kolorow na sztywno."""
    p = PALETY[marka or MARKA]

    def rgb(h):
        h = h.lstrip("#")
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

    acc, ok = rgb(p["accent"]), rgb(p["ok"] or p["accent"])
    hi = "#%02x%02x%02x" % tuple(round(c + (255 - c) * 0.35) for c in acc)
    for key, val in (("ACCENT_RGB", ",".join(map(str, acc))), ("ACCENT_HI", hi), ("ACCENT", p["accent"]),
                     ("ON_ACCENT", p["on_accent"]), ("OK_RGB", ",".join(map(str, ok))), ("OK", p["ok"] or p["accent"])):
        page = page.replace("{{" + key + "}}", val)
    return page

# ---------------------------------------------------------------- przejscia plansz i biblioteka grafik
# Przejscia plansz: kolejne plansze biora kolejne pozycje z PRZEJSCIA, wiec dwie pod rzad nigdy nie wchodza tak samo
# (Jakub po IMG_0576: "bardzo generyczne sa przejscia"). Wymuszenie konkretnego: panel(..., wejscie="iris").
# Wartosci w px, nie w %: render zaokragla liczby do calosci, a 1% kadru to 19 px skoku.
# Krotka: (stan poczatkowy, stan otwarty, czas wejscia, ease, stan wyjscia, czas wyjscia, ease, czy z light leakiem).
# Od 24.11.2026 (zasada 10, Jakub: "wszystko mega plynne... mniej tych przejsc... bardziej premium"): domyslnie kazda
# plansza wchodzi miekkim przenikaniem "fade". Efektowne przejscia tylko przez wejscie="...", najwyzej jedno w rolce.
PRZEJSCIA = ["fade"]
RUCH = {
    # kurtyna: jasna plansza zjezdza z gory w 0,55 s (referencje Jakuba z 24.11.2026); do plansz panel(..., jasna=True)
    "kurtyna": ('{y:-1920}', '{y:0', 0.55, "power3.inOut", '{y:-1920', 0.5, "power3.inOut", False),
    "fade": ('{opacity:0,scale:1.04,filter:"blur(10px)"}', '{opacity:1,scale:1,filter:"blur(0px)"', 0.6, "power2.out",
             '{opacity:0,scale:0.98,filter:"blur(8px)"', 0.45, "power2.inOut", False),
    "blur": ('{opacity:0,scale:1.06,filter:"blur(18px)"}', '{opacity:1,scale:1,filter:"blur(0px)"', 0.32, "power3.out",
             '{opacity:0,scale:1.04,filter:"blur(14px)"', 0.18, "power2.in", True),
    "iris": ('{clipPath:"circle(0px at 540px 760px)"}', '{clipPath:"circle(2300px at 540px 760px)"', 0.55, "power3.out",
             '{clipPath:"circle(0px at 540px 760px)"', 0.26, "power3.in", False),
    "wipe": ('{clipPath:"inset(1920px 0px 0px 0px)"}', '{clipPath:"inset(0px 0px 0px 0px)"', 0.45, "expo.out",
             '{clipPath:"inset(0px 0px 1920px 0px)"', 0.24, "power3.in", False),
    "zoom": ('{opacity:0,scale:0.35,filter:"blur(14px)",transformOrigin:"50% 40%"}', '{opacity:1,scale:1,filter:"blur(0px)"', 0.42, "expo.out",
             '{opacity:0,scale:1.9,filter:"blur(12px)"', 0.22, "power3.in", False),
    "diag": ('{clipPath:"polygon(0px 0px, 0px 0px, -400px 1920px, -400px 1920px)"}',
             '{clipPath:"polygon(0px 0px, 1480px 0px, 1080px 1920px, -400px 1920px)"', 0.5, "expo.out",
             '{clipPath:"polygon(1480px 0px, 1480px 0px, 1080px 1920px, 1080px 1920px)"', 0.26, "power3.in", False),
    "slide": ('{y:1920}', '{y:0', 0.5, "expo.out", '{y:-1920', 0.26, "power3.in", False),
}
_uzyte_przejscia = []
_okna_ruchu = []  # (od, do) wejsc i wyjsc plansz: w tych chwilach tresc jest w ruchu, kontrola strefy je pomija

# Subtelne efekty dzwiekowe pod animacje (Jakub, 17.11.2026). False = film bez efektow.
SFX = True

# Biblioteka gotowych grafik z katalogu HyperFrames (opis i arkusze: references/biblioteka.md).
BIBLIOTEKA = Path.home() / ".claude/skills/montaz-rolek/biblioteka"


POLE_STREFY = (195, 290, 690, 800)  # kolumna strefy bezpiecznej nad napisami: x, y, szerokosc, wysokosc


def mount(el, mid, nazwa, t_in, dur, zmienne=None, track=6, styl="left:0;top:0;width:1080px;height:1920px", pole=None):
    """Montuje szablon z biblioteki jako pod-kompozycje: kopiuje jego plik (i zasoby blokow) do hf/ i dopisuje element
    z wartosciami zmiennych. Kolory bierze z tokenow --brand/--bg/--fg/--surface w :root szablonu, czyli z palety marki.
    Dziala dla pozycji oznaczonych w biblioteka.md jako "montowalne"; "wycinki" wkleja sie recznie.

    pole=(x, y, w, h), np. POLE_STREFY: szablon zmniejszony do szerokosci w i wysrodkowany w tym polu. Szablon zawsze
    rysuje sie na pelnym kadrze 1080x1920 (rozmiar pudelka w `styl` go NIE skaluje - sprawdzone 18.11.2026), wiec caly
    kadr szablonu idzie do pomniejszajacego opakowania. Tlo szablonu tez sie pomniejsza: w polu uzywaj wariantu bez
    tla (np. "backdrop": "none") na planszy z panel(). Tresc wyzsza niz h * 1080 / w wyjdzie poza pole: obejrzyj klatke."""
    src = next(BIBLIOTEKA.glob(f"compositions/**/{nazwa}.html"))
    rel = src.relative_to(BIBLIOTEKA)
    dst = P / "hf" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if "components" not in rel.parts:  # bloki maja wlasne zasoby (zdjecia, czcionki)
        shutil.copytree(BIBLIOTEKA / "assets", P / "hf/assets", dirs_exist_ok=True)
    vals = json.dumps(zmienne or {}, ensure_ascii=False).replace("&", "&amp;").replace("'", "&#39;")
    if pole:
        styl = "left:0;top:0;width:1080px;height:1920px"
    host = (f'<div id="{mid}" class="clip" style="position:absolute;{styl}" data-composition-id="{mid}" data-composition-src="{rel}" '
            f"data-start=\"{t_in:.3f}\" data-duration=\"{dur:.3f}\" data-track-index=\"{track}\" data-variable-values='{vals}'></div>")
    if pole:
        x, y, w, h = pole
        k = w / 1080
        host = (f'<div style="position:absolute;left:{x}px;top:{y + h / 2 - 1920 * k / 2:.1f}px;width:1080px;height:1920px;'
                f'transform:scale({k:.4f});transform-origin:0 0">{host}</div>')
    el.append(host)



def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


# poprawki transkrypcji (whisper -> tekst napisow)
FIX = {}

# Frazy napisow po hooku. *slowa* = wyroznienie akcentem. Tekst brany stad, czasy z transkrypcji.
# Fraza ma sie zmiescic w CAP_W (620 px w strefie bezpiecznej): do ok. 17 znakow w pelnym rozmiarze, najwyzej 22.
PHRASES = [
    "W zeszłym tygodniu", "na *giełdę* weszła", "firma od *Claude'a,*", "czyli *Anthropic.*", "*Największe IPO*", "w historii.",
    "Akcje w pierwszej", "minucie wystrzeliły", "o *1/3* do góry.", "Nikt nie daje", "takich pieniędzy", "na *chatbota.*",
    "Płacą, bo wierzą,", "że za chwilę", "*każda firma*", "będzie na tym", "pracować.", "I tu jest", "*lekki haczyk.*",
    "Ty masz dokładnie", "*to samo* narzędzie,", "ale za *80 zł*", "miesięcznie.", "Pytanie tylko,", "czy zaczniesz",
    "tego używać", "*przed* konkurencją,", "czy *po niej?*",
]


def load_words():
    ws = json.loads((P / "audio/slowa.json").read_text())
    out = []
    for a, b, t in ws:  # whisper pisze "tak że" osobno; w napisach "także"
        if out and norm(out[-1][2]) == "tak" and norm(t) == "że" and a - out[-1][1] < 0.15:
            out[-1] = [out[-1][0], b, "także"]
            continue
        out.append([a, b, FIX.get(t, t)])
    return out


def manual_group(ws):
    phrases, k = [], 0
    for ph in PHRASES:
        cur, inhl = [], False
        for tok in ph.split():
            start = tok.startswith("*")
            end = "*" in tok[1:]
            text = tok.replace("*", "")
            hl = inhl or start
            inhl = (inhl or start) and not end
            if k >= len(ws):
                raise SystemExit(f"Brak slow dla frazy: {ph}")
            if norm(ws[k][2]) != norm(text):
                raise SystemExit(f"Niezgodnosc: '{ws[k][2]}' vs '{text}' we frazie '{ph}' (t={ws[k][0]:.2f})")
            cur.append([ws[k][0], ws[k][1], text, hl])
            k += 1
        phrases.append(cur)
    if k != len(ws):
        raise SystemExit(f"Nieprzypisane slowa: {[w[2] for w in ws[k:]]}")
    return phrases


def span(w, cls="w", text=None):
    hl = " hl" if len(w) > 3 and w[3] else ""
    return f'<span class="{cls}{hl}">{html.escape(text if text is not None else w[2])}</span>'


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def build():
    edl = json.loads((P / "aroll/edl.json").read_text())
    total = edl[-1]["t_out"]
    words = load_words()

    def W(text, after=0.0):
        for a, b, t in words:
            if a >= after - 1e-6 and norm(t) == norm(text):
                return a, b
        raise SystemExit(f"Nie znaleziono slowa: {text} po {after}")

    seg = lambda i: edl[i]
    el, js, srt = [], [], []
    dzw = []  # efekty dzwiekowe: dzw.append({"t": czas_trafienia, "typ": "pop" | "tik" | "swoosh" | "shh" | "powiad"}); opis w sfx.py

    # --- zasada 10 (24.11.2026): plynne zoomy i limit scen
    sceny = []  # (nazwa, od, do): kazda zlozona animacja (plansza, karta, przeplyw, logo, CTA); najwyzej 2 na 30 s

    def scena(nazwa, od, do):
        sceny.append((nazwa, od, do))

    def zoom(t, skala=1.18, dl=2.0, do=None, wroc=None):
        """Plynny najazd calego kadru (#zwrap, niezalezny od najazdu ujec w #vwrap): do `skala` w `dl` s, sine.inOut.
        do=czas ciecia -> skala wraca do 1 skokiem (cięcie to ukrywa); wroc=czas -> wraca plynnie w 1,2 s."""
        js.append(f'tl.to("#zwrap",{{scale:{skala},duration:{dl},ease:"sine.inOut"}},{t:.3f});')
        if wroc is not None:
            js.append(f'tl.to("#zwrap",{{scale:1,duration:1.2,ease:"sine.inOut"}},{wroc:.3f});')
        elif do is not None:
            js.append(f'tl.set("#zwrap",{{scale:1}},{do:.3f});')

    def hook0(linie, akcent=None, do=None, top=300, rozmiar=92):
        """Zasada 11 (24.11.2026, statystyki: 63-75% pominiec w 2-3 s): pelny hook widoczny OD KLATKI 0, bez wjazdu.
        linie: 1-2 linie hasla (do ok. 16 znakow na linie przy 92 px); akcent: slowo (albo jego fragment) w kolorze
        akcentu; do: kiedy haslo znika (domyslnie koniec hooka). Do tego ruch od pierwszej klatki (odjazd 1,12 -> 1,0
        w 0,6 s) i rozjasnienie startu (brightness 1,15 -> 1 przez 1,2 s)."""
        do = do if do is not None else seg(1)["t_in"]
        def lin(t):
            if akcent and akcent in t:
                a_, b_ = t.split(akcent, 1)
                return f'{html.escape(a_)}<span class="hk0-ac">{html.escape(akcent)}</span>{html.escape(b_)}'
            return html.escape(t)
        el.append(f'<div id="hk0" class="hk0 clip" data-start="0" data-duration="{do:.3f}" data-track-index="5" style="top:{top}px">'
                  + "".join(f'<div class="hk0-l" style="font-size:{rozmiar}px">{lin(t)}</div>' for t in linie) + "</div>")
        js.append(f'tl.fromTo("#hk0",{{scale:1.04}},{{scale:1,duration:0.8,ease:"power3.out"}},0);')
        js.append(f'tl.to("#hk0",{{opacity:0,y:-16,filter:"blur(8px)",duration:0.35,ease:"power2.inOut"}},{do - 0.35:.3f});')
        js.append('tl.fromTo("#zwrap",{scale:1.12},{scale:1,duration:0.6,ease:"power3.out"},0);')
        js.append('tl.fromTo("#vwrap",{filter:"brightness(1.15)"},{filter:"brightness(1)",duration:1.2,ease:"power1.out"},0);')

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1}); gsap.set("#zwrap",{scale:1});')
    for e in edl:
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')

    # --- C4527: biala koszulka pod napisami (1120 px) - miekkie przyciemnienie samego obrazu pod pasem napisow
    # (wyglad napisow bez zmian, zasada 1); lezy nad wideo, pod planszami (z-index 5 < 10)
    el.append(f'<div id="c7scrim" class="c7-scrim clip" data-start="0" data-duration="{total:.3f}" data-track-index="1"></div>')
    # --- haslo od klatki 0 (zasada 11), bez hooka kinetycznego; napisy od kwestii 1
    kin_end = next(e["t_in"] for e in edl if not e["hook"])
    if HOOK == "A":
        hook0(["81 mld $", "na Twoją konkurencję."], akcent="81 mld $", top=280, rozmiar=72, do=kin_end)
        srt.append((0.0, kin_end, "Inwestorzy właśnie postawili 81 miliardów na to, że Twoja konkurencja zacznie używać AI."))
    else:
        hook0(["Oni: 81 mld $.", "Ty: 80 zł."], akcent="Ty: 80 zł.", top=276, rozmiar=68, do=kin_end)
        srt.append((0.0, kin_end, "Za tę firmę zapłacili 81 miliardów dolarów. Ty masz to narzędzie za 80 zł miesięcznie."))
    end_card_in = round(W("zaobserwuj", edl[-1]["t_in"])[0] - 0.12, 3)  # plansza koncowa wchodzi na "koniecznie zaobserwuj"

    # --- napisy slowo po slowie (od kwestii 1 do wejscia planszy koncowej)
    phrases = manual_group([w for w in words if kin_end - 0.02 <= w[0] < end_card_in])
    za_dlugie = []
    for i, ph in enumerate(phrases):
        start = max(ph[0][0] - 0.06, kin_end if i == 0 else 0)
        nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
        end = min(nxt, ph[-1][1] + 0.6, end_card_in)
        cid = f"c{i}"
        txt = " ".join(w[2] for w in ph)
        fs = min(66, int(CAP_W / (len(txt) * 0.54)))  # Inter Tight 650: ok. 0,54 rozmiaru na znak
        if fs < CAP_MIN:
            za_dlugie.append((ph[0][0], fs, txt))
        el.append(f'<div id="{cid}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                  f'data-track-index="4" style="font-size:{fs}px">' + " ".join(span(w) for w in ph) + "</div>")
        for j, w in enumerate(ph):
            js.append(f'tl.fromTo("#{cid} .w:nth-child({j + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{max(start, w[0] - 0.03):.3f});')
        srt.append((start, end, txt))

    leak_n = [0]

    def leak(t):
        lid = f"lk{leak_n[0]}"
        leak_n[0] += 1
        el.append(f'<div id="{lid}" class="leak clip" data-layout-ignore data-start="{t - 0.22:.3f}" data-duration="0.55" data-track-index="8"></div>')
        js.append(f'tl.fromTo("#{lid}",{{opacity:0,xPercent:-18}},{{opacity:1,xPercent:0,duration:0.2,ease:"power2.out"}},{t - 0.22:.3f});')
        js.append(f'tl.to("#{lid}",{{opacity:0,xPercent:16,duration:0.3,ease:"power2.in"}},{t - 0.02:.3f});')

    jasne = []  # okna jasnych plansz: napisy w nich dostaja klase dk (ciemny tekst, mietowy zakreslacz)

    def panel(pid, t_in, t_out, inner, track=2, leak_in=True, leak_out=True, cls="", fade_out=True, extend=0.0, wejscie=None, jasna=False, szklo=False):
        """jasna=True: wstawka "premium" jak w referencjach Jakuba (24.11.2026) - jasne tlo, ciemny tekst, biale karty
        (.lcard), wejscie kurtyna z gory. Napisy na niej robia sie ciemne same."""
        if szklo:  # matowe szklo jak w Apple: A-roll przeswieca rozmyty spod jasnej tafli (Jakub, 24.11.2026)
            jasna, cls = True, (cls + " glass-p").strip()
        if jasna:
            cls = (cls + " light").strip()
            wejscie = wejscie or "kurtyna"
            jasne.append((t_in + 0.25, t_out - 0.3))
        """extend/fade_out=False: plansza trwa dluzej pod nastepna plansza (przenikanie bez przeswitu wideo)."""
        # Kwadraty dekoracyjne u dolu planszy zostaja tylko w palecie adGen. W personal brandzie plansza jest czysta:
        # Jakub o mietowych kwadratach (IMG_0576, 17.11.2026): "nie podoba mi sie to".
        sq = ('<div class="sq sq1" data-layout-allow-overflow></div><div class="sq sq2" data-layout-allow-overflow></div>'
              '<div class="sq sq3" data-layout-allow-overflow></div>') if MARKA == "adgen" else ""
        rodzaj = wejscie or PRZEJSCIA[len(_uzyte_przejscia) % len(PRZEJSCIA)]
        _uzyte_przejscia.append(rodzaj)
        scena(f"plansza {pid}", t_in, t_out)
        dzw.append({"t": t_in, "typ": "swoosh"})  # kazde wejscie planszy ma miekki swoosh
        r_od, r_do, r_czas, r_ease, w_do, w_czas, w_ease, r_leak = RUCH[rodzaj]
        el.append(f'<div id="{pid}" class="panel clip {cls}" data-layout-allow-overflow data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12 + extend:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div>{sq}{inner}</div>')
        js.append(f'tl.fromTo("#{pid}",{r_od},{r_do},duration:{r_czas},ease:"{r_ease}"}},{t_in - 0.12:.3f});')
        _okna_ruchu.append((t_in - 0.12, t_in - 0.12 + r_czas))
        d = t_out - t_in
        if sq:
            js.append(f'tl.fromTo("#{pid} .sq1",{{rotation:-14,y:60}},{{rotation:-6,y:0,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            js.append(f'tl.fromTo("#{pid} .sq2",{{rotation:18,y:40}},{{rotation:9,y:-20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            js.append(f'tl.fromTo("#{pid} .sq3",{{rotation:8}},{{rotation:20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        if leak_in and r_leak:
            leak(t_in)
        if t_out < total - 0.1 and fade_out:
            js.append(f'tl.to("#{pid}",{w_do},duration:{w_czas},ease:"{w_ease}"}},{t_out - w_czas:.3f});')
            _okna_ruchu.append((t_out - w_czas, t_out))
            if leak_out and r_leak:
                leak(t_out)

    def pop(sel, t, extra=""):
        # zasada 10: bez sprezyn (back.out) - plynne wejscie z rozmyciem, 0,6 s power3.out
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:18,filter:"blur(8px)"{extra}}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.6,ease:"power3.out"}},{t:.3f});')

    def overlay(oid, t_in, t_out, inner, cls, track=5, y_from=30):
        """Nakladka na wideo. Domyslnie stoi nad napisami (pas 925-1110 px, do 690 px szerokosci) i wjezdza od dolu, bo
        w typowym kadrze gorny pas strefy (270-480 px) zajmuje glowa. Gdy nad glowa jest wolne miejsce (niski kadr),
        przenies klase na 290 px (do 940 px szerokosci) i daj y_from ujemne. Zawsze sprawdz na klatce."""
        scena(f"nakladka {oid}", t_in, t_out)
        el.append(f'<div id="{oid}" class="{cls} clip" data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from * 0.8:.0f},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.55,ease:"expo.out"}},{t_in:.3f});')
        js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.4:.0f},filter:"blur(8px)",duration:0.35,ease:"power2.inOut"}},{t_out - 0.35:.3f});')

    # ================================================================ C4534 "81 mld $ na Twoja konkurencje" (klasy CSS z prefiksem d1-)
    def wejdz(sel, t, y=20, dur=0.6):  # zasada 10: wejscie z rozmyciem, bez sprezyn
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{dur},ease:"power3.out"}},{t:.3f});')

    nH = len([e for e in edl if e["hook"]])  # ile kwestii hooka (A: 1, B: 2)
    S = lambda k: seg(nH + k)  # kwestie tresci od 0

    # --- SCENA A (jasna, kurtyna): wejscie na gielde, rekordowe IPO, kurs +34% (tresc 0-2)
    tA_in = S(0)["t_in"] + 0.05
    tA_out = S(3)["t_in"]
    inner = ('<div class="d1-cam" id="d1cam">'
             '<div class="p-head" style="top:300px" id="d1ah">WEJŚCIE NA GIEŁDĘ</div>'
             '<div class="lcard d1-co" id="d1co"><img class="d1-cl" src="logo/claude.png" alt="" id="d1cl">'
             '<div class="d1-cn"><b id="d1cb">Claude</b><img class="d1-an" src="logo/anthropic-wordmark.png" alt="" id="d1an"></div>'
             '<span class="d1-tk" id="d1tk">Nasdaq: ANT</span></div>'
             '<div class="d1-rek" id="d1rek">Największe IPO w historii · ok. 81 mld $</div>'
             '<div class="lcard d1-ch" id="d1ch"><div class="d1-chh"><span>Kurs na otwarciu</span><span class="d1-pct" id="d1pct">+34%</span></div>'
             '<svg class="d1-svg" width="572" height="220" viewBox="0 0 572 220" fill="none">'
             '<path d="M10 200 H562" stroke="#e4e4df" stroke-width="2"/>'
             '<path id="d1line" d="M14 176 C80 172 120 168 170 150 S260 120 300 98 S400 60 450 46 S530 26 558 20" stroke="#0f1012" stroke-width="6" stroke-linecap="round"/>'
             '<circle id="d1dot" cx="558" cy="20" r="11" fill="var(--accent)" stroke="#0f1012" stroke-width="4"/></svg>'
             '<div class="d1-lab"><span>83 $</span><b id="d1end">111,50 $</b></div></div>'
             '</div>')
    panel("pA", tA_in, tA_out, inner, jasna=True)
    wejdz("#d1ah", tA_in + 0.3, 10, 0.5)
    wejdz("#d1co", W("giełdę", S(0)["t_in"])[0] - 0.15, 18, 0.6)
    js.append(f'gsap.set(["#d1an","#d1tk"],{{opacity:0}});')
    wejdz("#d1tk", W("weszła", S(0)["t_in"])[0] - 0.05, 8, 0.5)
    js.append(f'tl.fromTo("#d1cl",{{scale:0.85}},{{scale:1,duration:0.6,ease:"power3.out"}},{W("claudea", S(0)["t_in"])[0] - 0.1:.3f});')
    wejdz("#d1an", W("anthropic", S(0)["t_in"])[0] - 0.1, 8, 0.55)
    t_naj = W("największe", S(1)["t_in"])[0]
    wejdz("#d1rek", t_naj - 0.12, 12, 0.55)
    dzw.append({"t": t_naj - 0.12, "typ": "pop"})
    t_ak = W("akcje", S(2)["t_in"])[0]
    wejdz("#d1ch", t_ak - 0.2, 22, 0.6)
    t_wy = W("wystrzeliły", S(2)["t_in"])[0]
    js.append(f'tl.fromTo("#d1line",{{strokeDasharray:720,strokeDashoffset:720}},{{strokeDashoffset:0,duration:{t_wy + 0.6 - t_ak:.2f},ease:"power2.inOut"}},{t_ak + 0.2:.3f});')
    js.append(f'tl.fromTo("#d1dot",{{opacity:0,scale:0.4,transformOrigin:"558px 20px"}},{{opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{t_wy + 0.7:.3f});')
    wejdz("#d1pct", W("13", S(2)["t_in"])[0] - 0.1, 8, 0.5)
    wejdz("#d1end", t_wy + 0.7, 8, 0.5)
    dzw.append({"t": t_ak, "typ": "shh"})
    js.append('gsap.set("#d1cam",{scale:1});')
    js.append(f'tl.to("#d1cam",{{scale:1.04,duration:{tA_out - tA_in:.2f},ease:"sine.inOut"}},{tA_in:.3f});')

    # --- twarz: "Nikt nie daje takich pieniedzy na chatbota." / "Placa, bo wierza..." - najazdy
    zoom(W("nikt", S(3)["t_in"])[0] - 0.1, 1.16, 1.4, do=S(4)["t_in"])
    zoom(W("każda", S(4)["t_in"])[0] - 0.3, 1.1, 1.4, do=S(5)["t_in"])

    # --- SCENA B (szklo): inwestorzy 81 mld $ vs Ty 80 zl / mies., to samo narzedzie (tresc 5)
    tB_in = S(5)["t_in"] + 0.05
    tB_out = S(6)["t_in"]
    inner = ('<div class="lcard d1-k" id="d1inv" style="top:380px"><span class="d1-kl">Inwestorzy</span><b>81 mld $</b></div>'
             '<div class="d1-same" id="d1same"><img src="logo/claude.png" alt="">to samo narzędzie</div>'
             '<div class="lcard d1-k d1-acc" id="d1ty" style="top:660px"><span class="d1-kl">Ty</span><b id="d1tyb">80 zł / mies.</b></div>')
    panel("pB", tB_in, tB_out, inner, szklo=True)
    wejdz("#d1inv", tB_in + 0.25, 22, 0.6)
    wejdz("#d1ty", W("ty", S(5)["t_in"])[0] - 0.12, 22, 0.6)
    js.append('gsap.set("#d1tyb",{opacity:0});')
    t80 = W("80", S(5)["t_in"])[0]
    js.append(f'tl.fromTo("#d1tyb",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.45,ease:"power3.out"}},{t80 - 0.12:.3f});')
    dzw.append({"t": t80 - 0.12, "typ": "pop"})
    wejdz("#d1same", W("dokładnie", S(5)["t_in"])[0] - 0.05, 10, 0.5)

    # --- twarz: "Pytanie tylko, czy zaczniesz tego uzywac przed konkurencja, czy po niej?"
    zoom(W("przed", S(6)["t_in"])[0] - 0.3, 1.18, 1.6, do=S(7)["t_in"])

    # --- plansza koncowa "profil" w trybie obserwuj (rotacja: C4527 telefon, C4528 jasna, C4529 stos), od "Zaobserwuj"
    foto = cta.przygotuj_avatar(P / "hf")
    h, j, d = cta.plansza("profil", "pend", end_card_in, total, "Przed czy po?", "Pokazuję, od czego zacząć", foto=foto)
    el.append(h)
    js.extend(j)
    dzw.extend(d)
    # plansza koncowa = zakonczenie z CTA "zaobserwuj"; nie liczona jako scena (przy oddaniu wymieniona osobno)

    for i in range(len(el)):
        if 'class="cap clip"' in el[i]:
            m = re.search(r'data-start="([0-9.]+)" data-duration="([0-9.]+)"', el[i])
            if any(a <= float(m.group(1)) + float(m.group(2)) / 2 <= b for a, b in jasne):
                el[i] = el[i].replace('class="cap clip"', 'class="cap dk clip"')
    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el)) \
        .replace("{{JS}}", "\n      ".join(js)).replace("{{KIN_TOP}}", str(KIN_TOP)).replace("{{CAP_TOP}}", str(CAP_TOP)) \
        .replace("{{KIN_PAD}}", str((1080 - KIN_W) // 2))
    page = page.replace("</style>", cta.CTA_CSS + "</style>", 1)
    page = kolory(page)
    # Czasy do kontroli strefy: koniec kazdego napisu i hooka (fraza jest wtedy cala) oraz siatka co 0,75 s na grafiki.
    czasy = sorted({round(float(m) + float(d) - 0.05, 2) for m, d in re.findall(
        r'class="(?:cap|kin) clip" data-start="([0-9.]+)" data-duration="([0-9.]+)"', page)}
        | {round(0.4 + 0.75 * k, 2) for k in range(int((total - 0.5) / 0.75))})
    czasy = [t for t in czasy if not any(a - 0.03 <= t <= b + 0.03 for a, b in _okna_ruchu)]  # bez klatek w trakcie przejscia
    (P / "analiza").mkdir(exist_ok=True)
    (P / "analiza/strefa_czasy.json").write_text(json.dumps({"safe": SAFE, "czasy": czasy}))
    if STREFA:
        page = page.replace("</style>", STREFA_CSS + "</style>", 1)
    out = P / "hf/index.html"
    out.write_text(page)
    glos = P / "hf/glos.wav"
    glos.unlink(missing_ok=True)
    # Efekty dzwiekowe: momenty zebrane w `dzw` ida do analiza/sfx.json, a sfx.py miksuje probki pod glos (z limiterem).
    # Bez efektow glos przechodzi tylko przez limiter -1,8 dBFS, bo kodowanie AAC w renderze dodaje ok. 0,2 dB szczytu.
    (P / "analiza").mkdir(exist_ok=True)
    (P / "analiza/sfx.json").write_text(json.dumps(sorted(dzw, key=lambda e: e["t"]), indent=1))
    if SFX and dzw:
        subprocess.run(["uv", "run", "--no-project", "--with", "numpy", "python3", "-I", str(BIBLIOTEKA.parent / "scripts/sfx.py"),
                        str(GLOS), str(P / "analiza/sfx.json"), str(glos)], check=True)
    else:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(GLOS), "-af",
                        "alimiter=limit=0.81:attack=1:release=40:level=false", "-c:a", "pcm_s16le", str(glos)], check=True)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | {len(phrases)} fraz, {len(el)} elementow, {total:.2f}s, plansza koncowa od {end_card_in:.2f}")
    for ph in phrases:
        print(f"   {ph[0][0]:6.2f} " + " ".join(("*" + w[2] + "*") if w[3] else w[2] for w in ph))
    # zasada 10: najwyzej 2 zlozone animacje (sceny) w kazdym oknie 30 s
    sceny.sort(key=lambda x: x[1])
    print(f"sceny ({len(sceny)}): " + ", ".join(f"{n} {a:.1f}-{b:.1f}" for n, a, b in sceny))
    for n, a, b in sceny:
        w_oknie = [x for x in sceny if a <= x[1] < a + 30]
        if len(w_oknie) > 2:
            print(f"UWAGA (zasada 10): {len(w_oknie)} scen w oknie {a:.1f}-{a + 30:.1f} s (dozwolone 2): "
                  + ", ".join(x[0] for x in w_oknie) + ". Polacz je w jedna scene albo zostaw sama twarz z plynnym zoomem.")
            break
    if za_dlugie:
        print(f"UWAGA: {len(za_dlugie)} fraz nie miesci sie w strefie bezpiecznej ({CAP_W} px) przy czcionce >= {CAP_MIN} px. "
              f"Podziel je w PHRASES (do ok. {int(CAP_W / (CAP_MIN * 0.54))} znakow):")
        for t, fs, txt in za_dlugie:
            print(f"   {t:6.2f}  {fs} px  {txt}")
    if STREFA:
        print("TRYB KONTROLNY STREFY: index.html bez wideo i teł. Nie renderuj; uruchom kompozycja.py jeszcze raz bez STREFA=1.")


# Tryb kontrolny (STREFA=1): znika wideo, tla plansz, poswiaty i cienie, zostaje sama tresc grafik na czarnym tle.
# strefa.py robi z tego klatki i szuka jasnych pikseli poza strefa.
STREFA_CSS = """
      #vwrap, .pbg, .leak, .sq, .e-tlo { display: none !important; }
      html, body, #root { background: #000 !important; }
      * { box-shadow: none !important; text-shadow: none !important; filter: none !important; }
"""

TEMPLATE = r"""<!doctype html>
<html lang="pl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      :root { --ground: #0f1012; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --on-accent: {{ON_ACCENT}};
        /* tokeny, z ktorych biora kolory szablony z biblioteki (katalog HyperFrames) */
        --brand: {{ACCENT}}; --accent-2: {{ACCENT_HI}}; --bg: #0f1012; --fg: #ffffff; --surface: #16171a; --border: #2b2d32; --radius: 28px;
        --font-body: "Inter Tight", sans-serif; --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #898989; --font-display: "Inter Tight", sans-serif;
        --font-ui: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); color: var(--ink); }
      #zwrap, #vwrap { position: absolute; inset: 0; transform-origin: 50% 36%; }
      #aroll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }

      .kin { position: absolute; left: 0; right: 0; top: {{KIN_TOP}}px; text-align: center; z-index: 30; }
      .kin-s { font-size: 50px; font-weight: 600; letter-spacing: -0.01em; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 6px 16px; padding: 0 {{KIN_PAD}}px; }
      .kin-t { margin-top: 6px; }
      .kin-b { font-weight: 800; letter-spacing: -0.04em; line-height: 1.02; margin-top: 4px; display: flex; justify-content: center; gap: 0 0.22em; white-space: nowrap; }
      .kin .w, .kin .b, .cap .w { display: inline-block; }
      .kin-s .w, .cap .w, .kin-b .b {
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,255,255,.14));
      }
      .kin-b.accent .b, .cap .w.hl { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .kin-s .w.mention { display: inline-flex; align-items: center; gap: 12px; padding: 5px 24px 5px 5px; border-radius: 100px;
        background: rgba(var(--accent-rgb),.22); -webkit-background-clip: border-box; background-clip: border-box; color: #fff;
        border: 2px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 30px rgba(var(--accent-rgb),.35); filter: drop-shadow(0 4px 14px rgba(0,0,0,.45)); }
      .kin-s .w.mention img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; display: block; }

      .cap { position: absolute; left: 0; right: 0; top: {{CAP_TOP}}px; text-align: center; font-size: 66px; font-weight: 650; letter-spacing: -0.015em; line-height: 1.1; z-index: 30; white-space: nowrap; }

      .panel { position: absolute; inset: 0; z-index: 10; overflow: hidden; }
      .panel.top { z-index: 35; }
      .pbg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 18%, #222327 0%, #141518 45%, var(--ground) 100%); }
      .sq { position: absolute; border-radius: 34px; }
      .sq1 { width: 300px; height: 300px; left: 640px; top: 1560px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 80px rgba(var(--accent-rgb),.35); }
      .sq2 { width: 190px; height: 190px; left: -50px; top: 1480px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 60px rgba(var(--accent-rgb),.3); }
      .sq3 { width: 330px; height: 330px; left: 250px; top: 1640px; border: 5px solid rgba(var(--accent-rgb),.85); }

      .p-head { position: absolute; left: 0; right: 0; text-align: center; color: var(--accent); font-size: 32px; font-weight: 800; letter-spacing: .14em; }
      .p1av { position: absolute; left: 50%; margin-left: -75px; top: 285px; width: 150px; height: 150px; border-radius: 50%; padding: 6px;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 50px rgba(var(--accent-rgb),.45); }
      .p1av img { width: 138px; height: 138px; border-radius: 50%; object-fit: cover; display: block; border: 4px solid #141518; }
      .list { position: absolute; left: 160px; width: 725px; display: flex; flex-direction: column; gap: 30px; }
      .row { display: flex; align-items: center; gap: 30px; }
      .tile { width: 96px; height: 96px; border-radius: 24px; display: grid; place-items: center; color: var(--on-accent); flex: none;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 40px rgba(var(--accent-rgb),.45), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.sm { width: 56px; height: 56px; border-radius: 16px; box-shadow: 0 0 24px rgba(var(--accent-rgb),.4), inset 0 1px 0 rgba(255,255,255,.35); }
      .lbl { font-size: 48px; font-weight: 800; letter-spacing: .01em; white-space: nowrap; }

      .notif { position: absolute; left: 195px; width: 690px; top: 925px; padding: 20px 22px; border-radius: 34px; display: flex; gap: 20px; align-items: flex-start; z-index: 25;
        background: rgba(24,25,28,.9); border: 1.5px solid rgba(255,255,255,.10); box-shadow: 0 24px 70px rgba(0,0,0,.35); }
      .nt-av { width: 72px; height: 72px; border-radius: 20px; object-fit: cover; flex: none; }
      .nt-body { flex: 1; }
      .nt-top { display: flex; align-items: baseline; gap: 10px; font-size: 30px; color: #a0a3aa; font-weight: 500; }
      .nt-top b { color: #fff; font-weight: 700; }
      .nt-time { margin-left: auto; font-size: 28px; }
      .nt-title { font-size: 40px; font-weight: 750; margin-top: 2px; display: flex; align-items: center; gap: 12px; }
      .nt-title .ic { color: var(--accent); }
      .nt-items { display: flex; gap: 10px; margin-top: 12px; }
      .nti { font-size: 28px; font-weight: 700; padding: 8px 16px; border-radius: 100px; background: rgba(var(--accent-rgb),.16); border: 1.5px solid rgba(var(--accent-rgb),.6); white-space: nowrap; }

      .chipwrap { position: absolute; left: 0; right: 0; top: 985px; display: flex; justify-content: center; z-index: 25; }
      .chip2 { display: flex; align-items: center; gap: 18px; padding: 14px 32px 14px 14px; border-radius: 100px; background: rgba(15,16,18,.86);
        border: 1.5px solid rgba(255,255,255,.14); font-size: 30px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .okpart { display: flex; align-items: center; gap: 12px; color: var(--ok); padding-left: 18px; border-left: 1.5px solid rgba(255,255,255,.16); }
      .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: #0f1012; background: var(--ok); box-shadow: 0 0 24px rgba(var(--ok-rgb),.45); flex: none; }
      .dot.sm { width: 40px; height: 40px; }

      .cal { position: absolute; left: 140px; width: 800px; top: 360px; border-radius: 34px; padding: 26px 30px 30px;
        background: linear-gradient(180deg, #1d1e22, #16171a); border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .cal-top { display: flex; align-items: center; gap: 14px; font-size: 38px; font-weight: 750; padding-bottom: 18px; border-bottom: 1.5px solid #2b2d32; }
      .cal-top .ic { color: var(--accent); }
      .cal-d { margin-left: auto; color: var(--muted); font-size: 28px; font-weight: 600; }
      .cal-grid { position: relative; height: 360px; margin-top: 10px; }
      .cal-row { position: absolute; left: 0; right: 0; height: 120px; border-top: 1.5px dashed #2f3136; }
      .cal-row span { position: absolute; left: 0; top: 12px; font-size: 28px; color: #6b6f77; font-weight: 600; }
      .evt { position: absolute; left: 118px; right: 0; top: 128px; height: 106px; border-radius: 22px; padding: 14px 24px;
        background: linear-gradient(140deg, rgba(var(--accent-rgb),.30), rgba(var(--accent-rgb),.16)); border: 2px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 40px rgba(var(--accent-rgb),.25); }
      .evt-t { font-size: 36px; font-weight: 800; }
      .evt-s { font-size: 28px; color: var(--accent-hi); margin-top: 6px; font-weight: 600; display: flex; gap: 10px; align-items: center; }
      .inv { position: absolute; top: 905px; left: 0; right: 0; display: flex; justify-content: center; }
      .pill { display: inline-flex; align-items: center; gap: 12px; white-space: nowrap; font-size: 31px; font-weight: 800; letter-spacing: .08em; padding: 14px 30px; border-radius: 100px; }
      .pill.ok { color: var(--ok); background: rgba(var(--ok-rgb),.14); border: 1.5px solid rgba(var(--ok-rgb),.55); box-shadow: 0 0 30px rgba(var(--ok-rgb),.25); }

      /* kafelki zostaja w gornym pasie strefy (3 x 290 px nie mieszcza sie nad napisami): uzywaj ich tylko wtedy,
         gdy nad glowa jest wolne miejsce, inaczej zaslonia wlosy i czolo */
      .tiles { position: absolute; left: 0; right: 0; top: 290px; display: flex; justify-content: center; gap: 20px; z-index: 25; }
      .tcard { position: relative; width: 290px; height: 206px; border-radius: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
        background: rgba(15,16,18,.86); border: 1.5px solid rgba(255,255,255,.12); box-shadow: 0 18px 50px rgba(0,0,0,.3); }
      .tcard .tile { width: 76px; height: 76px; border-radius: 20px; }
      .tlbl { font-size: 29px; font-weight: 750; text-align: center; line-height: 1.12; }
      .tok { position: absolute; top: -12px; right: -12px; width: 46px; height: 46px; border-radius: 50%; background: var(--ok); color: #0f1012;
        display: grid; place-items: center; box-shadow: 0 0 20px rgba(var(--ok-rgb),.45); }

      .bars { position: absolute; left: 140px; width: 800px; top: 420px; display: flex; flex-direction: column; gap: 46px; }
      .bhead { display: flex; align-items: center; justify-content: space-between; font-size: 40px; font-weight: 800; margin-bottom: 14px; }
      .bl { display: flex; align-items: center; gap: 14px; letter-spacing: .04em; }
      .bl img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; border: 2px solid var(--accent); }
      .bv { font-weight: 700; color: #d6d8dd; }
      .bv.o { color: var(--accent-hi); }
      .btrack { height: 40px; border-radius: 100px; background: #24262b; overflow: hidden; }
      .bfill { height: 100%; border-radius: 100px; transform-origin: left center; }
      .bfill.gray { width: 100%; background: linear-gradient(90deg, #6b6f77, #b3b7bf); }
      .bfill.accent { width: 4%; min-width: 30px; background: linear-gradient(90deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 24px rgba(var(--accent-rgb),.6); }
      .big30 { position: absolute; left: 0; right: 0; top: 690px; text-align: center; font-size: 230px; font-weight: 900; letter-spacing: -0.05em; line-height: 1;
        background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .big30s { position: absolute; left: 0; right: 0; top: 935px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: .2em; }

      .pcard { position: absolute; left: 90px; top: 285px; width: 900px; height: 754px; border-radius: 40px; overflow: hidden; background: #121212;
        box-shadow: 0 40px 120px rgba(0,0,0,.6), 0 0 0 1.5px rgba(255,255,255,.08); font-family: var(--font-ui); }
      .pc-banner { position: absolute; left: 0; right: 0; top: 0; height: 203px; background: linear-gradient(100deg, #c3c3c3, #cdcdcd 60%, #cacaca); }
      .pc-ring { position: absolute; left: 78px; top: 77px; width: 248px; height: 248px; border-radius: 50%; background: #141414; }
      .pc-av { position: absolute; left: 90px; top: 89px; width: 224px; height: 224px; border-radius: 50%; object-fit: cover; }
      .pc-name { position: absolute; left: 92px; top: 336px; font-size: 78px; font-weight: 500; color: #f5f5f5; letter-spacing: -0.01em; white-space: nowrap; }
      .pc-bot { position: absolute; left: 89px; top: 470px; display: flex; align-items: center; gap: 16px; font-size: 47px; color: #9b9b9b; }
      .pc-tabs { position: absolute; left: 58px; top: 590px; display: flex; align-items: center; gap: 8px; font-size: 46px; color: #a8a8a8; }
      .pc-tab { padding: 17px 30px; border-radius: 100px; }
      .pc-tab.on { background: #1f1f1f; color: #f5f5f5; }
      .pc-badge { position: absolute; right: 56px; top: 462px; display: flex; align-items: center; gap: 12px; font-family: var(--font-display); font-size: 36px; font-weight: 800;
        letter-spacing: .06em; color: var(--on-accent); padding: 14px 28px; border-radius: 100px; background: linear-gradient(180deg, var(--accent-hi), var(--accent));
        box-shadow: 0 0 40px rgba(var(--accent-rgb),.55), inset 0 1px 0 rgba(255,255,255,.35); }

      .ctawrap { position: absolute; left: 0; right: 0; top: 990px; display: flex; justify-content: center; z-index: 26; }
      .cbox { width: 680px; display: flex; align-items: center; gap: 20px; padding: 14px 14px 14px 16px; border-radius: 100px; background: rgba(15,16,18,.88);
        border: 1.5px solid rgba(255,255,255,.16); box-shadow: 0 18px 50px rgba(0,0,0,.4); }
      .cav { width: 74px; height: 74px; border-radius: 50%; background: #2a2c31; color: #b9bcc3; display: grid; place-items: center; flex: none; }
      .cin { flex: 1; position: relative; height: 74px; display: flex; align-items: center; font-size: 40px; white-space: nowrap; }
      .cph { position: absolute; left: 0; color: #7c8089; font-weight: 500; }
      .ctyped { display: flex; font-weight: 750; color: #fff; }
      .cl { display: none; }
      .caret { width: 4px; height: 48px; background: var(--accent); margin-left: 4px; border-radius: 2px; }
      .csend { width: 74px; height: 74px; border-radius: 50%; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); color: var(--on-accent); display: grid; place-items: center;
        flex: none; box-shadow: 0 0 30px rgba(var(--accent-rgb),.5); }

      .bubble { position: absolute; left: 50%; margin-left: -300px; width: 600px; top: 520px; height: 300px; border-radius: 64px; display: grid; place-items: center;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 90px rgba(var(--accent-rgb),.5), inset 0 2px 0 rgba(255,255,255,.35); }
      .bubble::after { content: ""; position: absolute; left: 120px; bottom: -54px; width: 0; height: 0; border-right: 70px solid transparent; border-top: 60px solid var(--accent); }
      .bubble span { font-size: 170px; font-weight: 900; letter-spacing: -0.03em; color: var(--on-accent); line-height: 1; }
      .endtxt { position: absolute; left: 0; right: 0; top: 910px; text-align: center; font-size: 60px; font-weight: 800; }
      .endsub { position: absolute; left: 0; right: 0; top: 995px; text-align: center; font-size: 40px; font-weight: 500; color: #c9ccd3; }

      /* jasne wstawki "premium" (panel(..., jasna=True)), 24.11.2026 */
      .panel.light { color: #0f1012; }
      .panel.light .pbg { background: radial-gradient(110% 70% at 85% 0%, #e3f6ee 0%, #f5f5f2 48%, #f2f1ee 100%); }
      .panel.light .p-head { color: #0f1012; opacity: .45; font-size: 28px; letter-spacing: .18em; }
      .panel.light .lcard { background: #ffffff; border: 1px solid #e7e7e3; border-radius: 24px; box-shadow: 0 18px 48px rgba(15,16,18,.08); }
      .panel.light .tile { box-shadow: none; }
      .panel.glass-p .pbg { background: linear-gradient(160deg, rgba(255,255,255,.62), rgba(242,242,238,.42));
        -webkit-backdrop-filter: blur(54px) saturate(165%); backdrop-filter: blur(54px) saturate(165%); }
      .panel.glass-p .lcard { background: rgba(255,255,255,.62); border: 1px solid rgba(255,255,255,.8);
        -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px); box-shadow: 0 18px 48px rgba(15,16,18,.10), inset 0 1px 0 rgba(255,255,255,.9); }
      .cap.dk .w { background: none; -webkit-background-clip: border-box; background-clip: border-box; color: #0f1012; filter: none; }
      .cap.dk .w.hl { color: #0f1012; background: linear-gradient(transparent 58%, rgba(var(--accent-rgb),.6) 58%, rgba(var(--accent-rgb),.6) 92%, transparent 92%); }
      /* hook od klatki 0 (zasada 11) */
      .hk0 { position: absolute; left: 70px; right: 70px; text-align: center; z-index: 32; transform-origin: 50% 0; }
      .hk0-l { font-weight: 900; letter-spacing: -0.03em; line-height: 1.02; color: #fff; text-shadow: 0 6px 30px rgba(0,0,0,.6), 0 2px 6px rgba(0,0,0,.5); white-space: nowrap; }
      .hk0-ac { color: var(--accent); }
      /* C4527 "20 ofert w godzine" (prefiks c7-) */
      .c7-scrim { position: absolute; inset: 0; z-index: 5; pointer-events: none;
        background: radial-gradient(40% 5.2% at 50% 1158px, rgba(0,0,0,.34) 0%, rgba(0,0,0,.16) 50%, rgba(0,0,0,.05) 78%, rgba(0,0,0,0) 100%); }
      /* zielona sciana za Jakubem: mietowy akcent hasla jako zakreslenie z ciemnym tekstem, nie kolor liter */
      .hk0-ac { color: var(--on-accent); background: var(--accent); padding: 0 .14em; border-radius: .14em; text-shadow: none;
        -webkit-box-decoration-break: clone; box-decoration-break: clone; }
      .c7-cam { position: absolute; inset: 0; transform-origin: 50% 40%; }
      .c7-bot { position: absolute; left: 220px; width: 640px; top: 320px; padding: 24px 28px; display: flex; gap: 22px; align-items: center; }
      .c7-bot img { width: 88px; height: 88px; border-radius: 22px; object-fit: cover; flex: none; }
      .c7-bt { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
      .c7-bt b { font-size: 44px; font-weight: 800; letter-spacing: -0.01em; }
      .c7-bt span { font-size: 27px; font-weight: 500; color: #5c5f66; white-space: nowrap; }
      .c7-plat { position: absolute; left: 220px; width: 640px; top: 498px; display: flex; gap: 20px; }
      .c7-pc { flex: 1; height: 124px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; }
      .c7-pc img { width: 56px; height: 56px; border-radius: 14px; object-fit: cover; }
      .c7-pc b { font-size: 28px; font-weight: 750; }
      .c7-more b { font-size: 32px; color: #8a8d93; }
      .c7-jobs { position: absolute; left: 220px; width: 640px; top: 652px; display: flex; flex-direction: column; gap: 16px; }
      .c7-job { height: 104px; display: flex; align-items: center; gap: 20px; padding: 0 24px; }
      .c7-job img { width: 52px; height: 52px; border-radius: 12px; object-fit: cover; flex: none; }
      .c7-sk { display: flex; flex-direction: column; gap: 12px; flex: 1; }
      .c7-sk i { display: block; height: 14px; border-radius: 7px; background: #e9e9e5; }
      .c7-tag { font-size: 25px; font-weight: 700; color: #8a8d93; white-space: nowrap; }
      .panel.light .c7-job.c7-hit { border-width: 2px; }
      .c7-hit .c7-tag { color: #0f1012; background: rgba(var(--accent-rgb),.45); padding: 6px 16px; border-radius: 100px; }
      .c7-doc { position: absolute; left: 220px; width: 640px; top: 652px; padding: 26px 30px 30px; }
      .c7-dh { display: flex; align-items: center; gap: 16px; padding-bottom: 18px; border-bottom: 1px solid #ececea; margin-bottom: 24px; }
      .c7-dh img { width: 52px; height: 52px; border-radius: 50%; object-fit: cover; }
      .c7-dh b { font-size: 38px; font-weight: 800; }
      .c7-for { margin-left: auto; font-size: 24px; font-weight: 600; color: #8a8d93; white-space: nowrap; }
      .c7-lines { display: flex; flex-direction: column; gap: 18px; }
      .c7-lines i { display: block; height: 14px; border-radius: 7px; background: #e4e4df; transform-origin: left center; }
      .c7-chip { display: inline-flex; align-items: center; gap: 10px; margin-top: 26px; padding: 10px 24px 10px 16px; border-radius: 100px;
        background: var(--accent); color: var(--on-accent); font-size: 28px; font-weight: 800; }
      .c7-res { position: absolute; left: 220px; width: 640px; top: 400px; display: flex; flex-direction: column; gap: 22px; }
      .c7-row { height: 170px; display: flex; align-items: center; gap: 30px; padding: 0 38px; }
      .c7-nw { display: inline-flex; line-height: 1; font-variant-numeric: tabular-nums; font-size: 112px; font-weight: 900; letter-spacing: -0.04em; min-width: 150px; }
      .c7-nwd { display: inline-block; height: 1em; overflow: hidden; }
      .c7-nwc { display: flex; flex-direction: column; }
      .c7-nwc i { font-style: normal; display: block; height: 1em; line-height: 1; }
      .c7-nws { display: inline-block; line-height: 1; }
      .c7-rl { font-size: 40px; font-weight: 700; }
      .panel.glass-p .c7-row.c7-acc { background: var(--accent); border-color: rgba(255,255,255,.6); color: var(--on-accent); }
      /* C4528 "AI przypomina o fakturach" (prefiks c8-) */
      .c8-cam { position: absolute; inset: 0; transform-origin: 50% 40%; }
      .c8-p1, .c8-p2 { position: absolute; inset: 0; }
      .c8-grid { position: absolute; left: 230px; width: 620px; top: 350px; display: grid; grid-template-columns: repeat(6, 90px); gap: 16px; }
      .c8-fv { height: 108px; border-radius: 14px; background: #fff; border: 1px solid #e7e7e3; box-shadow: 0 10px 26px rgba(15,16,18,.06);
        padding: 14px 12px; display: flex; flex-direction: column; gap: 9px; }
      .c8-fv i { display: block; height: 8px; border-radius: 4px; background: #e6e6e1; }
      .c8-fv i:nth-child(2) { width: 70%; } .c8-fv i:nth-child(3) { width: 85%; }
      .c8-fv b { margin-top: auto; height: 14px; width: 46%; border-radius: 5px; background: rgba(var(--accent-rgb),.55); }
      .c8-rem { position: absolute; left: 230px; width: 620px; top: 742px; height: 108px; display: flex; align-items: center; gap: 16px; padding: 0 26px; }
      .c8-ic { color: #0f1012; display: grid; place-items: center; }
      .c8-rem b { font-size: 32px; font-weight: 750; margin-right: auto; }
      .c8-bd { width: 54px; height: 54px; border-radius: 50%; display: grid; place-items: center; font-size: 28px; font-weight: 800;
        background: #0f1012; color: #fff; }
      .c8-q { width: 54px; height: 54px; border-radius: 50%; display: grid; place-items: center; font-size: 32px; font-weight: 900;
        border: 2px dashed #b5b7bc; color: #8a8d93; margin-left: -70px; }
      .c8-cf { position: absolute; left: 230px; width: 620px; top: 872px; padding: 18px 30px 16px; }
      .c8-cfh { display: flex; align-items: baseline; gap: 14px; }
      .c8-cfh b { font-size: 32px; font-weight: 800; }
      .c8-cfh span { font-size: 24px; color: #8a8d93; font-weight: 600; }
      .c8-ch { display: block; margin-top: 8px; }
      .c8-now { position: absolute; left: 0; right: 0; top: 318px; margin: 0 auto; width: max-content; padding: 12px 30px; border-radius: 100px;
        background: var(--accent); color: var(--on-accent); font-size: 34px; font-weight: 850; }
      .c8-step { position: absolute; left: 230px; width: 620px; height: 116px; display: flex; align-items: center; gap: 22px; padding: 0 26px; }
      #c8s0 { top: 420px; } #c8s1 { top: 558px; } #c8s2 { top: 696px; }
      .c8-step b { font-size: 36px; font-weight: 800; margin-right: auto; white-space: nowrap; }
      .c8-tone { white-space: nowrap; font-size: 24px; font-weight: 700; color: #5c5f66; padding: 6px 14px; border-radius: 100px; background: #f0f0ec; }
      .c8-bar { position: absolute; left: 230px; width: 620px; top: 856px; height: 96px; display: flex; align-items: center; gap: 22px; padding: 0 28px; }
      .c8-bar span { font-size: 24px; font-weight: 800; letter-spacing: .16em; color: #8a8d93; }
      .c8-track { flex: 1; height: 26px; border-radius: 100px; background: #ececea; overflow: hidden; }
      .c8-fill { height: 100%; width: 100%; border-radius: 100px; transform-origin: left center;
        background: linear-gradient(90deg, rgba(var(--accent-rgb),.45), var(--accent) 60%, #0f1012); }
      .c8-inv, .c8-fold { position: absolute; left: 230px; width: 620px; display: flex; align-items: center; gap: 22px; padding: 0 28px; }
      .c8-inv { top: 400px; height: 140px; }
      .c8-fold { top: 628px; height: 160px; }
      .c8-it { display: flex; flex-direction: column; gap: 4px; margin-right: auto; }
      .c8-it b { font-size: 36px; font-weight: 800; }
      .c8-it span { font-size: 25px; color: #5c5f66; font-weight: 600; }
      .c8-late { font-size: 24px; font-weight: 800; padding: 8px 16px; border-radius: 100px; background: #0f1012; color: #fff; }
      .c8-fi { width: 84px; height: 84px; border-radius: 22px; display: grid; place-items: center; background: #0f1012; color: #fff; flex: none; }
      .c8-auto { position: absolute; left: 0; right: 0; top: 810px; margin: 0 auto; width: max-content; display: flex; align-items: center; gap: 10px;
        padding: 10px 24px 10px 16px; border-radius: 100px; background: var(--accent); color: var(--on-accent); font-size: 28px; font-weight: 800; }
      .c8-tel { position: absolute; left: 230px; width: 620px; top: 892px; height: 130px; display: flex; align-items: center; gap: 22px; padding: 0 28px; }
      .c8-pi { color: #0f1012; display: grid; place-items: center; }
      .c8-zero { font-size: 92px; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
      .c8-tt { font-size: 30px; font-weight: 700; line-height: 1.15; }
      /* C4529 "AI nie zabierze Ci klientow" (prefiks c9-) */
      .c9-cam { position: absolute; inset: 0; transform-origin: 50% 40%; }
      .c9-brief { position: absolute; left: 230px; width: 620px; top: 368px; height: 128px; display: flex; align-items: center; gap: 20px; padding: 0 26px; }
      .c9-bt { display: flex; flex-direction: column; gap: 12px; }
      .c9-bt b { font-size: 34px; font-weight: 800; }
      .c9-sk { display: flex; flex-direction: column; gap: 9px; }
      .c9-sk i { display: block; height: 11px; border-radius: 6px; background: rgba(15,16,18,.12); }
      .c9-odp { position: absolute; left: 230px; width: 620px; top: 524px; padding: 22px 26px 24px; }
      .c9-odp2 { top: 836px; padding: 20px 26px; }
      .c9-oh { display: flex; align-items: center; gap: 16px; }
      .c9-oh b { font-size: 32px; font-weight: 800; margin-right: auto; }
      .c9-nr { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; font-size: 24px; font-weight: 900; background: #0f1012; color: #fff; flex: none; }
      .c9-nr.acc { background: var(--accent); color: var(--on-accent); }
      .c9-gray { font-size: 24px; font-weight: 800; padding: 7px 16px; border-radius: 100px; background: rgba(15,16,18,.10); color: #3c3f45; white-space: nowrap; }
      .c9-msg { margin-top: 18px; font-size: 32px; font-weight: 600; line-height: 1.25; color: #2a2c31; }
      .c9-att { margin-top: 16px; display: inline-flex; align-items: center; gap: 10px; font-size: 24px; font-weight: 700; padding: 8px 16px;
        border-radius: 12px; background: rgba(15,16,18,.07); color: #3c3f45; }
      .c9-dots { display: flex; gap: 8px; }
      .c9-dots i { width: 12px; height: 12px; border-radius: 50%; background: #8a8d93; }
      .c9-hd { position: absolute; left: 230px; width: 620px; top: 330px; height: 108px; display: flex; align-items: center; gap: 18px; padding: 0 26px; }
      .c9-hd b { font-size: 36px; font-weight: 850; margin-right: auto; }
      .c9-fast { font-size: 26px; font-weight: 850; padding: 9px 18px; border-radius: 100px; background: var(--accent); color: var(--on-accent); white-space: nowrap; }
      .c9-row { position: absolute; left: 230px; width: 620px; height: 90px; display: flex; align-items: center; gap: 20px; padding: 0 24px; }
      .c9-row b { font-size: 32px; font-weight: 750; white-space: nowrap; }
      .c9-db { position: absolute; left: 0; right: 0; top: 884px; margin: 0 auto; width: max-content; display: flex; align-items: center; gap: 10px;
        padding: 9px 20px; border-radius: 100px; background: #0f1012; color: #fff; font-size: 26px; font-weight: 750; }
      .c9-ft { position: absolute; left: 230px; width: 620px; top: 950px; height: 96px; display: flex; align-items: center; gap: 14px; padding: 0 26px; }
      .c9-ft span { font-size: 28px; font-weight: 600; color: #5c5f66; }
      .c9-ft b { font-size: 34px; font-weight: 850; margin-right: auto; }
      .c9-ft .c9-2m { font-size: 30px; font-weight: 900; padding: 8px 20px; border-radius: 100px; background: var(--accent); color: var(--on-accent); }
      /* C4534 "81 mld $" (prefiks d1-) */
      .d1-cam { position: absolute; inset: 0; transform-origin: 50% 40%; }
      .d1-co { position: absolute; left: 230px; width: 620px; top: 350px; height: 150px; display: flex; align-items: center; gap: 22px; padding: 0 26px; }
      .d1-cl { width: 84px; height: 84px; border-radius: 22px; object-fit: cover; flex: none; }
      .d1-cn { display: flex; flex-direction: column; gap: 10px; margin-right: auto; }
      .d1-cn b { font-size: 40px; font-weight: 850; line-height: 1; }
      .d1-an { height: 22px; width: auto; display: block; }
      .d1-tk { font-size: 24px; font-weight: 800; padding: 8px 16px; border-radius: 100px; background: #0f1012; color: #fff; white-space: nowrap; }
      .d1-rek { position: absolute; left: 0; right: 0; top: 530px; margin: 0 auto; width: max-content; padding: 12px 26px; border-radius: 100px;
        background: var(--accent); color: var(--on-accent); font-size: 28px; font-weight: 850; }
      .d1-ch { position: absolute; left: 230px; width: 620px; top: 622px; padding: 22px 24px 18px; }
      .d1-chh { display: flex; align-items: center; justify-content: space-between; font-size: 28px; font-weight: 750; color: #3c3f45; }
      .d1-pct { font-size: 30px; font-weight: 900; color: var(--on-accent); background: var(--accent); padding: 6px 16px; border-radius: 100px; }
      .d1-svg { display: block; margin-top: 10px; }
      .d1-lab { display: flex; justify-content: space-between; font-size: 26px; font-weight: 700; color: #6b6e74; margin-top: 4px; }
      .d1-lab b { color: #0f1012; font-weight: 900; font-size: 30px; }
      .d1-k { position: absolute; left: 230px; width: 620px; height: 190px; display: flex; flex-direction: column; justify-content: center; padding: 0 40px; gap: 6px; }
      .d1-kl { font-size: 30px; font-weight: 700; color: #4a4d53; }
      .d1-k b { font-size: 86px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
      .panel.glass-p .d1-k.d1-acc { background: var(--accent); border-color: rgba(255,255,255,.6); }
      .d1-acc .d1-kl { color: rgba(15,16,18,.7); }
      .d1-same { position: absolute; left: 0; right: 0; top: 590px; margin: 0 auto; width: max-content; display: flex; align-items: center; gap: 12px;
        padding: 8px 22px 8px 10px; border-radius: 100px; background: #0f1012; color: #fff; font-size: 26px; font-weight: 750; z-index: 2; }
      .d1-same img { width: 40px; height: 40px; border-radius: 10px; }
      .leak { position: absolute; inset: -10%; z-index: 40; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(45% 35% at 30% 45%, rgba(var(--accent-rgb),.6), rgba(var(--accent-rgb),0) 70%),
                    radial-gradient(40% 30% at 70% 60%, rgba(255,255,255,.5), rgba(255,255,255,0) 70%),
                    radial-gradient(60% 50% at 50% 50%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920" data-fps="60">
    <div id="zwrap"><div id="vwrap">
      <video id="aroll" class="clip" src="aroll.mp4" data-start="0" data-duration="{{TOTAL}}" data-track-index="0" muted playsinline></video>
      <audio id="glos" src="glos.wav" data-start="0" data-duration="{{TOTAL}}" data-track-index="9"></audio>
    </div></div>
    {{ELEMENTS}}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      {{JS}}
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build()

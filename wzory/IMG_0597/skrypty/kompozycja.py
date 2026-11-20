#!/usr/bin/env python3
"""Kompozycja rolki PerfOS "Dałem AI 1000 zł na reklamy książek po 175 zł" (IMG_0597) -> ../hf/index.html (HyperFrames).
Marka PerfOS (branding z perfos.pl, 18.11.2026): tlo #0f0f0f z siatka jak w panelu, mieta #00E5A0, ciemny tekst na
miecie #04261c, kroj Geist w grafikach, logo (litera P z przelacznikiem + napis). Napisy i hook zostaja w zamrozonym
stylu (Inter Tight). Plansze to odtworzone karty z panelu PerfOS ze zrzutow Jakuba (lejek, ROAS, przychod, sredni
koszyk) i karta Shopify. Wszystko lezy w strefie bezpiecznej (SAFE), a nakladki na wideo stoja nad napisami, bo glowa
zajmuje gore kadru (wlosy od 8% wysokosci).
Dodatkowo ../napisy.srt (frazy napisow, do Premiere / uploadu).

Uzycie: python3 -I kompozycja.py            (STREFA=1 python3 -I kompozycja.py = tryb kontrolny dla strefa.py)
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
    # PerfOS (perfos.pl, motyw ciemny): --color-accent #00e5a0, --color-accent-ink #04261c
    "perfos": {"accent": "#00E5A0", "on_accent": "#04261c", "ok": None},
}
MARKA = "perfos"
LOGO = "perfos-logo-na-ciemne.svg"   # z naglowka perfos.pl (branding/), kopiowane do hf/
# Biala koszulka i jasne dlonie pod biala czcionka: miekkie owalne przyciemnienie wideo pod napisami (0 = wylaczone).
# Wygladu napisow nie zmienia, lezy pod nimi i pod planszami (jak w IMG_0583).
SCRIM = 0.44

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
KIN_TOP = 960   # gora bloku hooka (male slowa 60 px + haslo do 135 px + linia dopowiedzenia 66 px = do 1225 px)
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
KIN_W = safe_w(KIN_TOP, KIN_TOP + 265)  # caly blok hooka; przy 960 px wychodzi 620 px

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
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "funnel": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "banknote": '<rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "store": '<path d="M3 9h18v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M3 9l2-5h14l2 5"/><path d="M9 21v-6h6v6"/>',
    "power": '<path d="M12 2v10"/><path d="M18.4 6.6a9 9 0 1 1-12.77.04"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
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
PRZEJSCIA = ["iris", "wipe", "zoom", "diag", "slide", "blur"]
RUCH = {
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


def mount(el, mid, nazwa, t_in, dur, zmienne=None, track=6, styl="left:0;top:0;width:1080px;height:1920px"):
    """Montuje szablon z biblioteki jako pod-kompozycje: kopiuje jego plik (i zasoby blokow) do hf/ i dopisuje element
    z wartosciami zmiennych. Kolory bierze z tokenow --brand/--bg/--fg/--surface w :root szablonu, czyli z palety marki.
    Dziala dla pozycji oznaczonych w biblioteka.md jako "montowalne"; "wycinki" wkleja sie recznie."""
    src = next(BIBLIOTEKA.glob(f"compositions/**/{nazwa}.html"))
    rel = src.relative_to(BIBLIOTEKA)
    dst = P / "hf" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if "components" not in rel.parts:  # bloki maja wlasne zasoby (zdjecia, czcionki)
        shutil.copytree(BIBLIOTEKA / "assets", P / "hf/assets", dirs_exist_ok=True)
    vals = json.dumps(zmienne or {}, ensure_ascii=False).replace("&", "&amp;").replace("'", "&#39;")
    el.append(f'<div id="{mid}" class="clip" style="position:absolute;{styl}" data-composition-id="{mid}" data-composition-src="{rel}" '
              f"data-start=\"{t_in:.3f}\" data-duration=\"{dur:.3f}\" data-track-index=\"{track}\" data-variable-values='{vals}'></div>")



def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


# poprawki transkrypcji (whisper -> tekst napisow)
FIX = {"okolicę": "okolice", "kasę": "kasa"}
DROP = [("i", "przez", "ten")]           # artefakt DTW na poczatku kwestii: "i" przed "przez ten" (w nagraniu go nie ma)
MERGE = [("danej", "mi,", "danymi,")]    # whisper rozbil "danymi," na dwa tokeny

# Frazy napisow po hooku. *slowa* = wyroznienie akcentem. "~" na poczatku = fraza tylko w SRT, na ekranie ten tekst
# pokazuje grafika (pigulki "Drogie / niszowe / lokalne", dymek marketera). Tekst brany stad, czasy z transkrypcji.
# Fraza ma sie zmiescic w CAP_W (620 px): do ok. 17 znakow w pelnym rozmiarze, najwyzej 22.
PHRASES = [
    "I to nie byle jakich.", "To były *albumy*", "o architekturze", "*Bielska-Białej*",
    "z wydawnictwa", "mojego *dziadka.*",
    "~Drogie,", "~niszowe,", "~lokalne.",
    "Pewnie *marketer*", "powiedziałby:", "~odpuść", "~przez Metę", "~to bez szans.",
    "*Zasada* była jedna:", "*nic nie ruszamy.*", "Podpinamy", "i *lecimy.*",
    "Patrzymy tylko", "i wyłącznie", "na *wyniki.*", "O ile w ogóle", "jakiekolwiek", "z tego będą.",
    "*PerfOS* sam", "zrobił reklamy,", "sam je wypuścił,", "sam je optymalizował", "i sam *wyłączył*",
    "zestawy, które", "nie działały.",
    "No i *wynik.*",
    "Przez ten okres", "od *20 października*", "do dziś",
    "*PerfOS* zrobił", "*16 zestawów*", "reklamowych,", "co przekłada się", "na okolice", "*40 grafik.*",
    "Z czego *trzy*", "zestawy reklamowe", "*wyłączył,*", "czyli okolice", "niecałych *10 grafik.*",
    "Idąc dalej,", "wygenerował", "*571 wejść*", "na stronę,", "obejrzanych", "produktów było", "*484.*",
    "*32 ludzie*", "wsadzili", "produkt do koszyka,", "kasa: *16*", "i zakup,", "uwaga,", "*11 razy*",
    "został", "zrealizowany,",
    "co przełożyło się", "na średni koszyk", "*384 zł,*", "bo podpowiem,", "książek było", "*trzy rodzaje*",
    "na stronie,", "niektórzy kupowali", "sobie po", "*dwie, trzy.*",
    "*ROAS* wykręciliśmy", "na tym projekcie", "*3,38,*", "a przychód", "z tych reklam", "to było", "*4220 zł.*",
    "I jestem w *100%*", "pewny,", "co mam poparte", "danymi,", "że to źle się", "niestety zliczało",
    "ze względu", "na *piksela*", "na Facebooku,", "który był po prostu", "*źle skonfigurowany,*",
    "bo na *Shopify*", "pokazuje nam", "total sales", "*8251 zł,*",
    "oprócz PerfOS-a", "był tylko jeszcze", "*jeden kanał,*", "który wiemy,", "ile wygenerował,",
    "także możemy sobie", "wyestymować,", "że tutaj", "*zaniżyło*", "ten przychód", "o ponad", "*1700 zł.*",
    "Podsumowując:", "ciekawy projekt,", "byliśmy ciekawi,", "jak to wyjdzie.", "No i *wyszło.*",
    "Także jeśli *PerfOS*", "poradził sobie", "z książką", "o Bielsku", "i o architekturze", "za *175 zł,*",
    "to myślę, że", "z *Twoim sklepem*", "też sobie", "*da radę.*",
    "Napisz w komentarzu", "*PERFOS,*", "a pokażę Ci,", "jak to ustawić.",
]


def load_words():
    ws = [[a, b, t] for a, b, t in json.loads((P / "audio/slowa.json").read_text())]
    for txt, n1, n2 in DROP:
        hit = [k for k in range(len(ws) - 2) if (ws[k][2], ws[k + 1][2], ws[k + 2][2]) == (txt, n1, n2)]
        assert len(hit) <= 1, (txt, hit)
        if hit:
            del ws[hit[0]]
    for a, b, nowe in MERGE:
        hit = [k for k in range(len(ws) - 1) if (ws[k][2], ws[k + 1][2]) == (a, b)]
        assert len(hit) <= 1, (a, b, hit)
        if hit:
            i = hit[0]
            ws[i:i + 2] = [[ws[i][0], ws[i + 1][1], nowe]]
    return [[a, b, FIX.get(t, t)] for a, b, t in ws]


def manual_group(ws):
    phrases, k = [], 0
    for ph in PHRASES:
        cur, inhl = [], False
        ukryta = ph.startswith("~")
        for tok in ph.lstrip("~").split():
            start = tok.startswith("*")
            end = "*" in tok[1:]
            text = tok.replace("*", "")
            hl = inhl or start
            inhl = (inhl or start) and not end
            if k >= len(ws):
                raise SystemExit(f"Brak slow dla frazy: {ph}")
            if norm(ws[k][2]) != norm(text):
                raise SystemExit(f"Niezgodnosc: '{ws[k][2]}' vs '{text}' we frazie '{ph}' (t={ws[k][0]:.2f})")
            cur.append([ws[k][0], ws[k][1], text, hl, ukryta])
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


def wheel(wid, text, cls=""):
    """Liczba z toczacymi sie cyframi: kazda cyfra to kolumna 0-9 przesuwana transformem (yPercent), wiec wynik
    jest ten sam przy renderze klatka po klatce i przy skoku na dowolny czas (licznik w JS tego nie gwarantuje)."""
    out, k = [f'<span class="nw {cls}" id="{wid}" data-layout-ignore>'], 0
    for ch in text:
        if ch.isdigit():
            out.append(f'<span class="nwd"><span class="nwc" id="{wid}c{k}">' + "".join(f"<i>{d}</i>" for d in range(10)) + "</span></span>")
            k += 1
        else:
            out.append(f'<span class="nws">{html.escape(ch)}</span>')
    return "".join(out) + "</span>"


def krzywa(punkty, dni, w, h, vmax, vmin=0.0, probek=8):
    """Sciezka SVG z dziennych wartosci: kazdy dzien to dzwon cos^2 o szerokosci +-1 dnia (jak wygladzone linie w panelu
    PerfOS i w Shopify). punkty = {dzien: wartosc}. Zwraca (linia, wypelnienie do zera)."""
    import math
    pts = []
    for i in range(dni * probek + 1):
        t = i / probek
        v = sum(val * math.cos(math.pi * (t - d) / 2) ** 2 for d, val in punkty.items() if abs(t - d) < 1)
        pts.append((round(t / dni * w, 1), round(h - (v - vmin) / (vmax - vmin) * h, 1)))
    line = "M" + " L".join(f"{x},{y}" for x, y in pts)
    y0 = round(h - (0 - vmin) / (vmax - vmin) * h, 1)
    return line, line + f" L{w},{y0} L0,{y0} Z"


def lamana(punkty, dni, w, h, vmax, vmin=0.0, probek=8):
    """Gladka linia przez dzienne wartosci (interpolacja cosinusowa miedzy dniami) - wydatek dzienny."""
    import math
    ks = sorted(punkty)
    pts = []
    for i in range(dni * probek + 1):
        t = i / probek
        if t <= ks[0]:
            v = punkty[ks[0]] if t == ks[0] else 0.0
        elif t >= ks[-1]:
            v = punkty[ks[-1]]
        else:
            j = max(k for k in range(len(ks)) if ks[k] <= t)
            a, b = ks[j], ks[j + 1]
            m = (1 - math.cos(math.pi * (t - a) / (b - a))) / 2
            v = punkty[a] * (1 - m) + punkty[b] * m
        pts.append((round(t / dni * w, 1), round(h - (v - vmin) / (vmax - vmin) * h, 1)))
    return "M" + " L".join(f"{x},{y}" for x, y in pts)


def build():
    edl = json.loads((P / "aroll/edl.json").read_text())
    total = edl[-1]["t_out"]
    words = load_words()

    def W(text, after=0.0):
        for a, b, t in words:
            if a >= after - 1e-6 and norm(t) == norm(text):
                return a, b
        raise SystemExit(f"Nie znaleziono slowa: {text} po {after}")

    def K(poczatek):
        """Kwestia po poczatku tekstu z aroll.py (numery zmieniaja sie przy kazdej zmianie ciec)."""
        hit = [e for e in edl if e["text"].startswith(poczatek)]
        assert len(hit) == 1, (poczatek, len(hit))
        return hit[0]

    ujecie = lambda e, k: e["shots"][k]["t_in"]
    pauza = next((e for e in edl if e.get("hold")), None)  # zatrzymanie po "No i wynik."
    el, js, srt = [], [], []
    dzw = []  # efekty dzwiekowe: {"t": czas_trafienia, "typ": "pop" | "tik" | "swoosh" | "shh" | "powiad"}; opis w sfx.py

    def roll(wid, text, t, dur=0.7, pokaz=None):
        """Toczy cyfry od momentu t. `pokaz` = selektor elementu, ktory ma byc ukryty do tego momentu (domyslnie sama
        liczba), zeby przed wypowiedzeniem liczby nie stalo na ekranie "000"."""
        js.append(f'gsap.set("{pokaz or "#" + wid}",{{opacity:0}});')
        js.append(f'tl.to("{pokaz or "#" + wid}",{{opacity:1,duration:0.12,ease:"power1.out"}},{t - 0.03:.3f});')
        for k, ch in enumerate(c for c in text if c.isdigit()):
            js.append(f'tl.fromTo("#{wid}c{k}",{{yPercent:0}},{{yPercent:{-10 * int(ch)},duration:{dur},ease:"power3.out"}},{t + 0.05 * k:.3f});')

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1});')
    s_wynik = K("No i wynik")
    for e in edl:
        if e is s_wynik or e.get("hold"):
            continue
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')
    # "No i wynik." + pauza: napiecie przed liczbami (Jakub: "bardziej zbudowane napiecie, troszke przedluzone,
    # przyblizenie na moja twarz"). Na slowie "wynik" szybki dojazd do twarzy, potem przez cala pauze (zwolnienie
    # i zatrzymana klatka z aroll.py) powolne dociskanie, brzegi kadru ciemnieja, pod spodem cichy narastajacy szum.
    t_w = next(w[0] for w in words if s_wynik["t_in"] <= w[0] < s_wynik["t_out"] and norm(w[2]) == "wynik")
    t_p0, t_p1 = pauza["t_in"], pauza["t_out"]
    js.append(f'tl.set("#vwrap",{{scale:1}},{s_wynik["t_in"]:.3f});')
    js.append(f'tl.to("#vwrap",{{scale:1.02,duration:{t_w - s_wynik["t_in"]:.3f},ease:"none"}},{s_wynik["t_in"]:.3f});')
    js.append(f'tl.to("#vwrap",{{scale:1.13,duration:0.34,ease:"power3.out"}},{t_w - 0.03:.3f});')
    js.append(f'tl.to("#vwrap",{{scale:1.22,duration:{t_p1 - (t_w + 0.31) - 0.001:.3f},ease:"none"}},{t_w + 0.31:.3f});')
    el.append(f'<div id="focus" class="focus clip" data-layout-ignore data-start="{t_w:.3f}" data-duration="{t_p1 - t_w:.3f}" data-track-index="1"></div>')
    js.append(f'tl.fromTo("#focus",{{opacity:0}},{{opacity:1,duration:{t_p1 - t_w - 0.02:.3f},ease:"power1.in"}},{t_w:.3f});')
    if SCRIM:
        el.append(f'<div id="scrim" class="scrim clip" data-layout-ignore data-start="0" data-duration="{total:.3f}" data-track-index="1"></div>')

    dzw.append({"t": t_p0 + 0.05, "typ": "shh", "dl": t_p1 - t_p0 - 0.05})

    # --- hook kinetyczny (kwestie 0 i 1): "Dałem AI [1000 ZŁ]" -> "na reklamowanie książek po [175 ZŁ]"
    kin_end = K("I to nie byle")["t_in"]
    hook = [w for w in words if w[0] < kin_end]
    exp = ["Dałem", "AI", "tysiąc", "złotych", "na", "reklamowanie", "książek", "po", "175", "zł."]
    assert [norm(w[2]) for w in hook] == [norm(x) for x in exp], [w[2] for w in hook]
    hook[0][2] = "Dałem"
    kin = [  # (male, duze, male_po, duze_akcentem, tekst_duzych)
        (hook[0:2], hook[2:4], [], False, ["1000", "ZŁ"]),
        (hook[4:8], hook[8:10], [], True, ["175", "ZŁ"]),
    ]
    for k, (small, big, after, akcent, big_txt) in enumerate(kin):
        start = max(0.0, small[0][0] - 0.06)
        end = kin[k + 1][0][0][0] - 0.06 if k + 1 < len(kin) else kin_end
        # wersaliki Inter Tight 800 to ok. 0,63 rozmiaru na znak; szerokosc z KIN_W (strefa bezpieczna)
        size = min(132, int(KIN_W / (len(" ".join(big_txt)) * 0.63)))
        sid = f"k{k}"
        el.append(
            f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">'
            f'<div class="kin-s">{"".join(span(w) for w in small)}</div>'
            f'<div class="kin-b{" accent" if akcent else ""}" style="font-size:{size}px">'
            + "".join(f'<span class="b">{html.escape(t)}</span>' for t in big_txt) + "</div></div>")
        for i, w in enumerate(small):
            js.append(f'tl.fromTo("#{sid} .kin-s .w:nth-child({i + 1})",{{opacity:0,y:18,filter:"blur(8px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0] - 0.04):.3f});')
        for i, w in enumerate(big):
            js.append(f'tl.fromTo("#{sid} .kin-b .b:nth-child({i + 1})",{{opacity:0,scale:1.35,filter:"blur(14px)"}},'
                      f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(start, w[0] - 0.05):.3f});')
        srt.append((start, end, " ".join(w[2] for w in small + big)))

    # --- napisy slowo po slowie (od kwestii 2)
    s_cta = edl[-1]
    end_card_in = round(s_cta["speech"][1] - s_cta["a_in"] + s_cta["t_in"] + 0.12, 3)
    phrases = manual_group([w for w in words if w[0] >= kin_end - 0.02])
    za_dlugie = []
    for i, ph in enumerate(phrases):
        start = max(ph[0][0] - 0.06, kin_end if i == 0 else 0)
        nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
        end = min(nxt, ph[-1][1] + 0.6, end_card_in)
        if pauza and 0 <= pauza["t_in"] - ph[-1][1] < 0.4:  # po tej frazie jest pauza: napis stoi do jej konca
            end = pauza["t_out"] - 0.04
        txt = " ".join(w[2] for w in ph)
        srt.append((start, end, txt))
        if ph[0][4]:  # fraza pokazana grafika (pigulki, dymek) - na ekranie bez napisu
            continue
        cid = f"c{i}"
        fs = min(66, int(CAP_W / (len(txt) * 0.54)))  # Inter Tight 650: ok. 0,54 rozmiaru na znak
        if fs < CAP_MIN:
            za_dlugie.append((ph[0][0], fs, txt))
        el.append(f'<div id="{cid}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                  f'data-track-index="4" style="font-size:{fs}px">' + " ".join(span(w) for w in ph) + "</div>")
        for j, w in enumerate(ph):
            js.append(f'tl.fromTo("#{cid} .w:nth-child({j + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{max(start, w[0] - 0.03):.3f});')

    leak_n = [0]

    def leak(t):
        lid = f"lk{leak_n[0]}"
        leak_n[0] += 1
        el.append(f'<div id="{lid}" class="leak clip" data-layout-ignore data-start="{t - 0.22:.3f}" data-duration="0.55" data-track-index="8"></div>')
        js.append(f'tl.fromTo("#{lid}",{{opacity:0,xPercent:-18}},{{opacity:1,xPercent:0,duration:0.2,ease:"power2.out"}},{t - 0.22:.3f});')
        js.append(f'tl.to("#{lid}",{{opacity:0,xPercent:16,duration:0.3,ease:"power2.in"}},{t - 0.02:.3f});')

    def panel(pid, t_in, t_out, inner, track=2, leak_in=True, leak_out=True, cls="", fade_out=True, extend=0.0, wejscie=None):
        """extend/fade_out=False: plansza trwa dluzej pod nastepna plansza (przenikanie bez przeswitu wideo)."""
        rodzaj = wejscie or PRZEJSCIA[len(_uzyte_przejscia) % len(PRZEJSCIA)]
        _uzyte_przejscia.append(rodzaj)
        dzw.append({"t": t_in, "typ": "swoosh"})  # kazde wejscie planszy ma miekki swoosh
        r_od, r_do, r_czas, r_ease, w_do, w_czas, w_ease, r_leak = RUCH[rodzaj]
        el.append(f'<div id="{pid}" class="panel clip {cls}" data-layout-allow-overflow data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12 + extend:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div><div class="pin" id="{pid}in">{inner}</div></div>')
        js.append(f'tl.fromTo("#{pid}",{r_od},{r_do},duration:{r_czas},ease:"{r_ease}"}},{t_in - 0.12:.3f});')
        _okna_ruchu.append((t_in - 0.12, t_in - 0.12 + r_czas))
        # plansza zyje: tresc powoli najezdza przez caly czas trwania (sama tresc, tlo stoi)
        js.append(f'tl.fromTo("#{pid}in",{{scale:1}},{{scale:1.03,duration:{t_out - t_in:.3f},ease:"none",transformOrigin:"540px 700px"}},{t_in:.3f});')
        if leak_in and r_leak:
            leak(t_in)
        if t_out < total - 0.1 and fade_out:
            js.append(f'tl.to("#{pid}",{w_do},duration:{w_czas},ease:"{w_ease}"}},{t_out - w_czas:.3f});')
            _okna_ruchu.append((t_out - w_czas, t_out))
            if leak_out and r_leak:
                leak(t_out)

    def pop(sel, t, extra="", ease="back.out(1.6)", dur=0.3):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:26,scale:0.94{extra}}},{{opacity:1,y:0,scale:1,duration:{dur},ease:"{ease}"}},{t:.3f});')

    def rise(sel, t, dur=0.42):
        """Spokojne wejscie (expo.out, bez sprezyny) - dla kart i wierszy, zeby nie wszystko skakalo tak samo."""
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:34,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{dur},ease:"expo.out"}},{t:.3f});')

    def overlay(oid, t_in, t_out, inner, cls, track=5, y_from=30):
        """Nakladka na wideo. Stoi nad napisami (pas 950-1130 px), bo gore kadru zajmuje glowa; wjezdza od dolu."""
        el.append(f'<div id="{oid}" class="{cls} clip" data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
        js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.6:.0f},filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.22:.3f});')

    def chip(oid, t_in, t_out, ikona, tekst, ok=False, dzwiek=None):
        inner = (f'<div class="chip2"><span class="tile sm">{icon(ikona, 32)}</span><span>{html.escape(tekst)}</span>'
                 + (f'<span class="dot sm">{icon("check", 22)}</span>' if ok else "") + "</div>")
        overlay(oid, t_in, t_out, inner, "chipwrap")
        if dzwiek:
            dzw.append({"t": t_in + 0.1, "typ": dzwiek})

    # ================================================================= kwestie 2-6: wstep na wideo
    # --- pigulki "Drogie / niszowe / lokalne" (zamiast napisu, w jego miejscu)
    s4 = K("Drogie")
    tagi = [("DROGIE", W("drogie", s4["t_in"])[0]), ("NISZOWE", W("niszowe", s4["t_in"])[0]), ("LOKALNE", W("lokalne", s4["t_in"])[0])]
    inner = "".join(f'<span class="tag" id="tg{k}">{t}</span>' for k, (t, _) in enumerate(tagi))
    el.append(f'<div id="tags" class="tags clip" data-start="{tagi[0][1] - 0.1:.3f}" data-duration="{s4["t_out"] - tagi[0][1] + 0.08:.3f}" data-track-index="5">{inner}</div>')
    for k, (_, t) in enumerate(tagi):
        js.append(f'tl.fromTo("#tg{k}",{{opacity:0,scale:0.6,y:18}},{{opacity:1,scale:1,y:0,duration:0.32,ease:"back.out(2.2)"}},{t - 0.05:.3f});')
    js.append(f'tl.to("#tags",{{opacity:0,y:-16,filter:"blur(8px)",duration:0.2,ease:"power2.in"}},{s4["t_out"] - 0.22:.3f});')
    dzw.append({"t": tagi[0][1], "typ": "pop"})

    # --- dymek marketera: "Odpuść. Przez Metę to bez szans." (cytat zamiast napisu)
    s5 = K("Pewnie marketer")
    cyt = [("Odpuść.", W("odpuść", s5["t_in"])[0]), ("Przez", W("przez", s5["t_in"])[0]), ("Metę", W("metę", s5["t_in"])[0]),
           ("to", W("to", W("metę", s5["t_in"])[0])[0]), ("bez", W("bez", s5["t_in"])[0]), ("szans.", W("szans", s5["t_in"])[0])]
    inner = ('<div class="msg-n">MARKETER</div><div class="msg-b">'
             + f'<span class="mw" id="mw0">{cyt[0][0]}</span><br>'
             + " ".join(f'<span class="mw" id="mw{k}">{html.escape(t)}</span>' for k, (t, _) in enumerate(cyt) if k > 0) + "</div>")
    overlay("msg", cyt[0][1] - 0.16, s5["t_out"] - 0.02, inner, "msgw")
    for k, (_, t) in enumerate(cyt):
        js.append(f'tl.fromTo("#mw{k}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{t - 0.03:.3f});')
    dzw.append({"t": cyt[0][1] - 0.06, "typ": "powiad"})

    # --- chip "JEDNA ZASADA" (kwestia 6, zblizenie): uzupelnia napis "nic nie ruszamy", nie powtarza go
    s6 = K("Zasada")
    chip("rule", W("zasada", s6["t_in"])[0] - 0.1, ujecie(s6, 1) - 0.04, "lock", "JEDNA ZASADA", dzwiek="pop")

    # ================================================================= P1: PerfOS robi to sam (kwestia 7)
    s7 = K("PerfOS sam")
    rows = [("sparkles", "Robi reklamy", W("zrobił", s7["t_in"])[0]),
            ("send", "Wypuszcza je", W("wypuścił", s7["t_in"])[0]),
            ("trend", "Optymalizuje", W("optymalizował", s7["t_in"])[0]),
            ("power", "Wyłącza słabe zestawy", W("wyłączył", s7["t_in"])[0])]
    inner = (f'<img class="plogo" id="p1logo" src="{LOGO}" alt="PerfOS" style="top:300px">'
             '<div class="p-head" id="p1h" style="top:400px">ROBI TO SAM</div><div class="srows" style="top:478px">')
    for k, (ic, lbl, _) in enumerate(rows):
        inner += (f'<div class="srow" id="p1r{k}"><div class="tile md">{icon(ic, 38)}</div><div class="slbl">{html.escape(lbl)}</div>'
                  f'<div class="sw" id="p1s{k}"><span class="knob" id="p1k{k}"></span></div></div>')
    inner += "</div>"
    panel("p1", s7["t_in"], s_wynik["t_in"], inner)
    js.append(f'tl.fromTo("#p1logo",{{opacity:0,scale:0.8,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.4,ease:"expo.out"}},{s7["t_in"] + 0.02:.3f});')
    rise("#p1h", s7["t_in"] + 0.14)
    sam = [w[0] for w in words if s7["t_in"] <= w[0] < s7["t_out"] and norm(w[2]) == "sam"]
    for k, (_, _, t) in enumerate(rows):
        rise(f"#p1r{k}", sam[k] - 0.06, 0.36)  # wiersz wchodzi na "sam", przelacznik wlacza sie na czasowniku
        js.append(f'tl.to("#p1k{k}",{{x:42,backgroundColor:"{PALETY[MARKA]["on_accent"]}",duration:0.24,ease:"back.out(2.4)"}},{t:.3f});')
        js.append(f'tl.to("#p1s{k}",{{backgroundColor:"{PALETY[MARKA]["accent"]}",boxShadow:"0 0 26px rgba(0,229,160,.45)",duration:0.2,ease:"power2.out"}},{t:.3f});')
    dzw.append({"t": rows[3][2], "typ": "tik"})

    # --- chip z datami (kwestia 9): 20.10 -> 17.11 (17 listopada pada w nagraniu, wyciete z dzwieku jako wtret)
    s9 = K("Przez ten okres")
    chip("daty", W("od", s9["t_in"])[0] - 0.1, s9["t_out"] - 0.04, "calendar", "20.10 – 17.11")

    # ================================================================= P2: 16 zestawow, ok. 40 grafik, 3 wylaczone
    s10 = K("PerfOS zrobił")  # dwa zdania w jednej kwestii: 16 zestawow / z czego trzy wylaczyl
    s11 = s10
    t16 = W("16", s10["t_in"])[0]
    t40 = W("40", t16)[0]
    t3 = W("trzy", t40)[0]
    t_off = W("wyłączył", t3)[0]
    t10 = W("10", t_off)[0]
    OFF = (6, 9, 15)
    inner = ('<div class="p-head" id="p2h" style="top:300px">PERFOS ZROBIŁ</div>'
             f'<div class="bignum" id="p2n" style="top:338px">{wheel("p2w", "16")}</div>'
             '<div class="biglbl" id="p2l" style="top:548px">zestawów reklamowych</div>'
             '<div class="pills" style="top:618px">'
             '<span class="pl acc" id="p2a">ok. 40 grafik</span>'
             '<span class="pl gray" id="p2b"><b>3</b> wyłączone<span id="p2c">&nbsp;· niecałe 10 grafik</span></span></div>'
             '<div class="adgrid" style="top:722px">')
    for k in range(16):
        inner += (f'<div class="ad" id="ad{k}"><div class="adimg">{icon("image", 26)}</div><div class="adl"></div><div class="adl s"></div>'
                  + (f'<div class="adoff" id="ao{k}">{icon("power", 24)}</div>' if k in OFF else "") + "</div>")
    inner += "</div>"
    panel("p2", s10["t_in"], s11["t_out"], inner)
    rise("#p2h", s10["t_in"] + 0.05)
    js.append(f'tl.fromTo("#p2n",{{opacity:0,scale:1.4,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.34,ease:"power3.out"}},{t16 - 0.08:.3f});')
    roll("p2w", "16", t16 - 0.04, 0.8, pokaz="#p2none")
    rise("#p2l", W("zestawów", s10["t_in"])[0] - 0.05)
    js.append('gsap.set("#p2w",{opacity:1});')  # te liczbe odslania wejscie calego #p2n
    for k in range(16):  # kafelki reklam wysypuja sie jeden po drugim przez "zestawow reklamowych"
        js.append(f'tl.fromTo("#ad{k}",{{opacity:0,scale:0.5,y:20}},{{opacity:1,scale:1,y:0,duration:0.28,ease:"back.out(1.8)"}},{t16 + 0.12 + k * 0.085:.3f});')
    dzw.append({"t": t16 + 0.12, "typ": "shh", "dl": 1.4})
    pop("#p2a", t40 - 0.05, ease="back.out(2.0)")
    dzw.append({"t": t40, "typ": "pop"})
    pop("#p2b", t3 - 0.05, ease="back.out(2.0)")
    for n, k in enumerate(OFF):  # trzy zestawy gasna po kolei na "wylaczyl"
        t = t_off + n * 0.14
        js.append(f'tl.to("#ad{k}",{{opacity:0.38,filter:"grayscale(1)",duration:0.25,ease:"power2.out"}},{t:.3f});')
        js.append(f'tl.fromTo("#ao{k}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)"}},{t:.3f});')
    dzw.append({"t": t_off, "typ": "tik"})
    js.append(f'tl.fromTo("#p2c",{{opacity:0}},{{opacity:1,duration:0.25,ease:"power2.out"}},{t10 - 0.3:.3f});')

    # ================================================================= P3: lejek zakupowy (kwestie 12-14), karta z panelu PerfOS
    s12, s13, s14 = K("Idąc dalej"), K("32 ludzie"), K("produkt do koszyka")
    p4_in = ujecie(s14, 1)   # "co przełożyło się na średni koszyk": zmiana kadru w tej samej kwestii
    t_p3 = W("wygenerował", s12["t_in"])[0] - 0.12
    kroki = [  # (etykieta, liczba, moment wiersza, moment liczby, przejscie z poprzedniego kroku wg panelu)
        ("Wejścia na stronę", 571, t_p3 + 0.3, W("571", s12["t_in"])[0], None),
        ("Obejrzane produkty", 484, W("obejrzanych", s12["t_in"])[0], W("484", s12["t_in"])[0], "85%"),
        ("Do koszyka", 32, W("32", s13["t_in"])[0] - 0.08, W("32", s13["t_in"])[0], "6,6%"),
        ("Kasa", 16, W("kasa", s14["t_in"])[0] - 0.05, W("16", s14["t_in"])[0], "50%"),
        ("Zakup", 11, W("zakup", s14["t_in"])[0] - 0.05, W("11", s14["t_in"])[0], "69%"),
    ]
    inner = (f'<div class="card fun" id="p3card" style="top:292px"><div class="chead"><span class="ctile">{icon("funnel", 34)}</span>'
             '<span class="ctitle">Lejek zakupowy</span></div>')
    for k, (lbl, n, _, _, conv) in enumerate(kroki):
        if conv:
            inner += f'<div class="fconv" id="fc{k}">{icon("down", 26)}<span>{conv}</span></div>'
        szer = round((n / 571) ** 0.5 * 100, 1)  # skala pierwiastkowa, jak w panelu (32 z 571 to 24% paska)
        inner += (f'<div class="frow{" last" if k == 4 else ""}" id="fr{k}"><div class="fl"><span>{lbl}</span>{wheel(f"fw{k}", str(n), "fv")}</div>'
                  f'<div class="ftrack"><div class="ffill" id="ff{k}" style="width:{szer}%"></div></div></div>')
    inner += "</div>"
    panel("p3", t_p3, p4_in, inner, leak_out=False, fade_out=False, extend=0.3)
    rise("#p3card", t_p3 + 0.04, 0.5)
    for k, (_, n, t_row, t_num, conv) in enumerate(kroki):
        if conv:
            js.append(f'tl.fromTo("#fc{k}",{{opacity:0,y:-14}},{{opacity:1,y:0,duration:0.28,ease:"power2.out"}},{t_row - 0.02:.3f});')
        rise(f"#fr{k}", t_row, 0.34)
        roll(f"fw{k}", str(n), t_num - 0.04, 0.75)
        js.append(f'tl.fromTo("#ff{k}",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"expo.out"}},{t_num:.3f});')
    dzw += [{"t": kroki[0][3], "typ": "shh", "dl": 0.8}, {"t": kroki[2][3], "typ": "tik"}, {"t": kroki[4][3], "typ": "tik"}]
    # zakup: wiersz dostaje poswiate i obrys na "został zrealizowany"
    t_real = W("został", s14["t_in"])[0]
    js.append(f'tl.to("#fr4",{{backgroundColor:"rgba(0,229,160,.10)",boxShadow:"0 0 0 2px rgba(0,229,160,.75), 0 0 46px rgba(0,229,160,.28)",duration:0.35,ease:"power2.out"}},{t_real - 0.05:.3f});')
    js.append(f'tl.fromTo("#fr4",{{scale:1}},{{scale:1.035,duration:0.18,ease:"power2.out",yoyo:true,repeat:1}},{t_real - 0.05:.3f});')

    # ================================================================= P4: sredni koszyk (kwestia 15, pierwsze ujecie)
    p4_out = ujecie(s14, 2)
    t384 = W("384", p4_in)[0]
    inner = (f'<div class="card kpi" id="p4card" style="top:500px"><div class="klabel">Średni koszyk</div><span class="ctile kico">{icon("cart", 34)}</span>'
             f'<div class="kval xl" id="p4v">{wheel("p4w", "384")}<span class="unit">&nbsp;zł</span></div>'
             '<div class="ksub">11 zakupów · 1248 zł wydane</div></div>'
             f'<div class="pills" style="top:930px"><span class="pl acc" id="p4p">{icon("book", 30)} album: 175 zł</span></div>')
    panel("p4", p4_in, p4_out, inner, track=7)
    rise("#p4card", p4_in + 0.04, 0.45)
    roll("p4w", "384", t384 - 0.04, 0.8, pokaz="#p4v")
    dzw.append({"t": t384, "typ": "pop"})
    pop("#p4p", W("zł", t384)[0] - 0.02, ease="back.out(2.0)")


    # ================================================================= P5: ROAS i przychod (kwestia 16, pierwsze ujecie)
    s16 = K("ROAS")
    p5_out = ujecie(s16, 1)
    t_roas = W("3,38", s16["t_in"])[0]
    t_prz = W("przychód", s16["t_in"])[0]
    t4220 = W("4220", s16["t_in"])[0]
    # dane dzienne z wykresu "Przychod i wydatek" (zrzut Jakuba): os od 19.10 (dzien 0) do 17.11 (dzien 29)
    przychod = {9: 700, 10: 520, 12: 525, 16: 720, 18: 700, 20: 175, 24: 350, 28: 525}
    wydatek = {3: 0, 4: 30, 5: 45, 6: 80, 7: 50, 8: 35, 9: 48, 10: 50, 11: 50, 12: 40, 13: 58, 14: 50, 15: 47, 16: 46, 17: 50,
               18: 52, 19: 44, 20: 58, 21: 55, 22: 52, 23: 52, 24: 35, 25: 42, 26: 52, 27: 45, 28: 40, 29: 44}
    CW, CH = 614, 104
    ln, ar = krzywa(przychod, 29, CW, CH, 800)
    wy = lamana(wydatek, 29, CW, CH, 800)
    sl, _ = krzywa(przychod, 29, 220, 60, 760)
    spark = (f'<svg class="spark" width="220" height="64" viewBox="0 -2 220 64" data-layout-ignore><path d="{sl}" fill="none" stroke="var(--accent)" '
             'stroke-width="3" stroke-linejoin="round"/></svg>')
    inner = ('<div class="p-head" id="p5h" style="top:296px">WYNIK</div>'
             f'<div class="card kpi" id="p5a" style="top:346px"><div class="klabel">ROAS</div><span class="ctile kico">{icon("gauge", 34)}</span>'
             f'<div class="kval">{wheel("p5w", "3,38")}</div>{spark}</div>'
             f'<div class="card chartc" id="p5c" style="top:582px"><div class="chead sm"><span class="ctile sm">{icon("chart", 26)}</span>'
             '<span class="ctitle">Przychód i wydatek</span></div>'
             '<div class="legend"><span><i class="ld"></i>Przychód <b>4220 zł</b></span><span><i class="ll"></i>Wydatek <b>1248 zł</b></span></div>'
             f'<svg class="plot" width="{CW}" height="{CH + 6}" viewBox="0 -3 {CW} {CH + 6}" data-layout-ignore>'
             f'<line x1="0" y1="{CH}" x2="{CW}" y2="{CH}" stroke="#2a2a2a" stroke-width="2"/>'
             f'<line x1="0" y1="{CH / 2}" x2="{CW}" y2="{CH / 2}" stroke="#222" stroke-width="2" stroke-dasharray="4 8"/>'
             f'<path id="p5ar" d="{ar}" fill="rgba(0,229,160,.16)"/>'
             f'<path id="p5wy" d="{wy}" fill="none" stroke="#4f8ff7" stroke-width="3.5" stroke-linejoin="round" pathLength="1000" class="dash"/>'
             f'<path id="p5ln" d="{ln}" fill="none" stroke="#6ee7b7" stroke-width="4" stroke-linejoin="round" pathLength="1000" class="dash"/></svg></div>'
             f'<div class="card kpi" id="p5b" style="top:846px"><div class="klabel">Przychód z reklam</div><span class="ctile kico">{icon("banknote", 34)}</span>'
             f'<div class="kval" id="p5bv">{wheel("p5v", "4220")}<span class="unit">&nbsp;zł</span></div>{spark}</div>')
    panel("p5", s16["t_in"], p5_out, inner)
    rise("#p5h", s16["t_in"] + 0.05)
    rise("#p5a", s16["t_in"] + 0.1, 0.45)
    roll("p5w", "3,38", t_roas - 0.04, 0.8)
    dzw.append({"t": t_roas, "typ": "pop"})
    t_ch = t_roas + 0.75
    rise("#p5c", t_ch, 0.4)
    d_ch = max(1.2, t4220 - t_ch - 0.5)
    js.append('gsap.set("#p5ar",{opacity:0});')
    js.append(f'tl.fromTo("#p5wy",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{d_ch:.3f},ease:"power1.inOut"}},{t_ch + 0.2:.3f});')
    js.append(f'tl.fromTo("#p5ln",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{d_ch:.3f},ease:"power1.inOut"}},{t_ch + 0.2:.3f});')
    js.append(f'tl.to("#p5ar",{{opacity:1,duration:0.5,ease:"power2.out"}},{t_ch + 0.2 + d_ch - 0.3:.3f});')
    dzw.append({"t": t_ch + 0.2, "typ": "shh", "dl": min(d_ch, 2.0)})
    rise("#p5b", t_prz - 0.08, 0.4)
    roll("p5v", "4220", t4220 - 0.04, 0.8, pokaz="#p5bv")

    # --- chip: piksel (kwestia 16, wideo)
    chip("piks", W("piksela", s16["t_in"])[0] - 0.1, ujecie(s16, 3) - 0.04, "alert", "PIKSEL ŹLE SKONFIGUROWANY", dzwiek="pop")

    # ================================================================= P6: Shopify, total sales (kwestia 16, ujecia 4-5)
    p6_in, p6_out = ujecie(s16, 3), ujecie(s16, 5)
    t8251 = W("8251", s16["t_in"])[0]
    # dzienne total sales ze zrzutu Shopify: os od 1.10 (dzien 0) do 16.11 (dzien 46)
    shop = {6: 910, 9: 150, 13: 150, 19: 150, 24: 350, 25: -50, 27: 700, 28: 700, 30: 520, 32: 190, 34: 910, 36: 700, 37: 200,
            38: 170, 41: 910, 42: 700, 44: 350, 46: 520}
    SW, SH = 506, 190
    sln, _ = krzywa(shop, 46, SW, SH, 1000, -150)
    y0 = round(SH - 150 / 1150 * SH, 1)
    y5 = round(SH - 650 / 1150 * SH, 1)
    y10 = round(SH - 1150 / 1150 * SH, 1)
    inner = ('<div class="p-head" id="p6h" style="top:330px">SHOPIFY · TOTAL SALES</div>'
             '<div class="shop" id="p6card" style="top:392px">'
             f'<div class="sh-v" id="p6v">PLN&nbsp;{wheel("p6w", "8,251.18")}</div><div class="sh-t">Total sales over time</div>'
             f'<div class="sh-plot"><span class="sh-y" style="top:{y10 - 14}px">PLN 1K</span><span class="sh-y" style="top:{y5 - 14}px">PLN 500</span>'
             f'<span class="sh-y" style="top:{y0 - 14}px">PLN 0</span>'
             f'<svg width="{SW}" height="{SH + 8}" viewBox="0 -4 {SW} {SH + 8}" data-layout-ignore>'
             f'<line x1="0" y1="{y10}" x2="{SW}" y2="{y10}" stroke="#ececec" stroke-width="2"/><line x1="0" y1="{y5}" x2="{SW}" y2="{y5}" stroke="#ececec" stroke-width="2"/>'
             f'<line x1="0" y1="{y0}" x2="{SW}" y2="{y0}" stroke="#9fc9ee" stroke-width="2.5" stroke-dasharray="3 7"/>'
             f'<path id="p6ln" d="{sln}" fill="none" stroke="#4ba6ea" stroke-width="4" stroke-linejoin="round" pathLength="1000" class="dash"/></svg></div>'
             '<div class="sh-x"><span>Oct 1</span><span>Oct 16</span><span>Nov 1</span><span>Nov 16</span></div></div>'
             '<div class="pills" style="top:912px">'
             f'<span class="pl acc" id="p6a"><img src="perfos-litera-ciemna.svg" alt="">PerfOS</span>'
             '<span class="pl gray" id="p6b">+ 1 inny kanał</span></div>')
    panel("p6", p6_in, p6_out, inner)
    rise("#p6h", p6_in + 0.06)
    rise("#p6card", p6_in + 0.12, 0.5)
    t_sl = W("pokazuje", p6_in)[0]
    js.append(f'tl.fromTo("#p6ln",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{max(1.2, t8251 - t_sl):.3f},ease:"power1.inOut"}},{t_sl:.3f});')
    dzw.append({"t": t_sl, "typ": "shh", "dl": min(2.0, max(1.2, t8251 - t_sl))})
    roll("p6w", "8,251.18", t8251 - 0.04, 0.9, pokaz="#p6v")
    dzw.append({"t": t8251, "typ": "pop"})
    pop("#p6a", W("PerfOS-a", p6_in)[0] - 0.05, ease="back.out(2.0)")
    pop("#p6b", W("jeden", p6_in)[0] - 0.05, ease="back.out(2.0)")

    # --- chip: zanizone o ponad 1700 zl (kwestia 16, ostatnie ujecie)
    t_zan, t_1700 = W("zaniżyło", p6_out)[0], W("1700", p6_out)[0]
    inner = (f'<div class="chip2"><span class="tile sm">{icon("trend", 32)}</span><span>PRZYCHÓD ZANIŻONY</span>'
             '<span class="okpart" id="zan2">+1700 ZŁ</span></div>')
    overlay("zan", t_zan - 0.1, s16["t_out"] - 0.04, inner, "chipwrap")
    js.append('gsap.set("#zan2",{display:"none"});')
    js.append(f'tl.set("#zan2",{{display:"flex"}},{t_1700 - 0.06:.3f});')
    js.append(f'tl.fromTo("#zan2",{{opacity:0,x:-18}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{t_1700 - 0.06:.3f});')
    dzw.append({"t": t_1700, "typ": "pop"})

    # ================================================================= zakonczenie na wideo (kwestia 18)
    s18 = K("ciekawy projekt")
    chip("alb", W("książką", s18["t_in"])[0] - 0.1, W("to", W("zł", W("175", s18["t_in"])[0])[0])[0] - 0.05, "book", "ALBUM ZA 175 ZŁ", ok=True)
    chip("skl", W("Twoim", s18["t_in"])[0] - 0.1, s18["t_out"] - 0.04, "store", "A TWÓJ SKLEP?")

    # ================================================================= CTA: komentarz "PERFOS" (kwestia 19)
    s19 = edl[-1]
    t_cta = W("napisz", s19["t_in"])[0] - 0.05
    t_key = W("PERFOS", s19["t_in"])[0]
    letters = "PERFOS"
    inner = (f'<div class="cbox" id="cbox"><div class="cav">{icon("user", 40)}</div><div class="cin">'
             '<span class="cph" id="cph">Dodaj komentarz…</span><span class="ctyped">'
             + "".join(f'<span class="cl" id="cl{k}">{c}</span>' for k, c in enumerate(letters))
             + f'</span><span class="caret" id="caret"></span></div><div class="csend" id="csend">{icon("up", 40)}</div></div>')
    el.append(f'<div id="cta" class="ctawrap clip" data-start="{t_cta:.3f}" data-duration="{end_card_in - t_cta:.3f}" data-track-index="5">{inner}</div>')
    pop("#cbox", t_cta)
    js.append(f'tl.set("#cph",{{opacity:0}},{t_key - 0.04:.3f});')
    for k in range(len(letters)):
        js.append(f'tl.set("#cl{k}",{{display:"inline-block"}},{t_key - 0.04 + k * 0.07:.3f});')
    js.append(f'tl.fromTo("#caret",{{opacity:1}},{{opacity:0,duration:0.32,ease:"steps(1)",repeat:{int((end_card_in - t_cta) / 0.32)},yoyo:true}},{t_cta + 0.3:.3f});')
    js.append(f'tl.fromTo("#csend",{{scale:1}},{{scale:1.18,duration:0.16,ease:"power2.out",yoyo:true,repeat:1}},{t_key + 0.6:.3f});')

    # ================================================================= plansza koncowa: logo PerfOS + dymek ze slowem-kluczem
    inner = (f'<img class="plogo" id="endlogo" src="{LOGO}" alt="PerfOS" style="top:318px">'
             '<div class="bubble" id="bub"><span>PERFOS</span></div>'
             '<div class="endtxt" id="endtxt">Napisz w komentarzu</div>'
             '<div class="endsub" id="endsub">a pokażę Ci, jak to ustawić</div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    js.append(f'tl.fromTo("#endlogo",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.35,ease:"expo.out"}},{end_card_in + 0.02:.3f});')
    js.append(f'tl.fromTo("#bub",{{opacity:0,scale:0.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.9)"}},{end_card_in + 0.08:.3f});')
    pop("#endtxt", end_card_in + 0.28)
    pop("#endsub", end_card_in + 0.4)

    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el)) \
        .replace("{{JS}}", "\n      ".join(js)).replace("{{KIN_TOP}}", str(KIN_TOP)).replace("{{CAP_TOP}}", str(CAP_TOP)) \
        .replace("{{KIN_PAD}}", str((1080 - KIN_W) // 2)).replace("{{SCRIM}}", f"{SCRIM:.2f}")
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
        page = re.sub(r'<video id="aroll".*?</video>\s*<audio id="glos".*?</audio>', "", page, flags=re.S)
    out = P / "hf/index.html"
    out.write_text(page)
    shutil.copyfile(P / "branding" / LOGO, P / "hf" / LOGO)
    shutil.copyfile(P / "branding/perfos-litera-ciemna.svg", P / "hf/perfos-litera-ciemna.svg")
    glos = P / "hf/glos.wav"
    glos.unlink(missing_ok=True)
    # Efekty dzwiekowe: momenty zebrane w `dzw` ida do analiza/sfx.json, a sfx.py miksuje probki pod glos (z limiterem).
    # Bez efektow glos przechodzi tylko przez limiter -1,8 dBFS, bo kodowanie AAC w renderze dodaje ok. 0,2 dB szczytu.
    (P / "analiza/sfx.json").write_text(json.dumps(sorted(dzw, key=lambda e: e["t"]), indent=1))
    if SFX and dzw:
        subprocess.run(["uv", "run", "--no-project", "--with", "numpy", "python3", "-I", str(BIBLIOTEKA.parent / "scripts/sfx.py"),
                        str(GLOS), str(P / "analiza/sfx.json"), str(glos)], check=True)
    else:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(GLOS), "-af",
                        "alimiter=limit=0.81:attack=1:release=40:level=false", "-c:a", "pcm_s16le", str(glos)], check=True)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | {len(phrases)} fraz, {len(el)} elementow, {len(dzw)} dzwiekow ({len(dzw) / total * 60:.1f}/min), {total:.2f}s, "
          f"plansza koncowa od {end_card_in:.2f} | przejscia: {', '.join(_uzyte_przejscia)}")
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
      #vwrap, .pbg, .leak, .scrim, .focus { display: none !important; }
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
      /* Geist z perfos.pl (podzbiory latin i latin-ext, wagi 100-900) - kroj marki PerfOS w grafikach */
      @font-face { font-family: "Geist"; src: url("fonts/geist-latin-ext.woff2") format("woff2"); font-weight: 100 900;
        unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }
      @font-face { font-family: "Geist"; src: url("fonts/geist-latin.woff2") format("woff2"); font-weight: 100 900;
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }
      :root { --ground: #0f0f0f; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --on-accent: {{ON_ACCENT}};
        /* tokeny, z ktorych biora kolory szablony z biblioteki (katalog HyperFrames) */
        --brand: {{ACCENT}}; --accent-2: {{ACCENT_HI}}; --bg: #0f0f0f; --fg: #f5f5f5; --surface: #161616; --border: #262626; --radius: 28px;
        --font-body: "Geist", sans-serif; --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #a1a1aa; --soft: #7c7c85; --font-display: "Inter Tight", sans-serif;
        --font-brand: "Geist", "Inter Tight", sans-serif;
        --font-ui: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); color: var(--ink); }
      #vwrap { position: absolute; inset: 0; transform-origin: 50% 33%; }
      #aroll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .scrim { position: absolute; left: -60px; right: -60px; top: 760px; height: 860px; z-index: 5; pointer-events: none;
        background: radial-gradient(ellipse 50% 50% at 50% 47%, rgba(8,9,11,{{SCRIM}}) 0%, rgba(8,9,11,{{SCRIM}}) 34%, rgba(8,9,11,0) 100%); }

      .focus { position: absolute; inset: -40px; z-index: 6; pointer-events: none;
        background: radial-gradient(ellipse 62% 46% at 50% 34%, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 46%, rgba(0,0,0,.62) 100%); }

      /* ---------- hook i napisy: zamrozony styl (Inter Tight), szerokosc i pozycja ze strefy bezpiecznej */
      .kin { position: absolute; left: 0; right: 0; top: {{KIN_TOP}}px; text-align: center; z-index: 30; }
      .kin-s { font-size: 50px; font-weight: 600; letter-spacing: -0.01em; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 6px 16px; padding: 0 {{KIN_PAD}}px; }
      .kin-b { font-weight: 800; letter-spacing: -0.04em; line-height: 1.02; margin-top: 4px; display: flex; justify-content: center; gap: 0 0.22em; white-space: nowrap; }
      .kin .w, .kin .b, .cap .w { display: inline-block; }
      .kin-s .w, .cap .w, .kin-b .b {
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,255,255,.14));
      }
      .kin-b.accent .b, .cap .w.hl { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .cap { position: absolute; left: 0; right: 0; top: {{CAP_TOP}}px; text-align: center; font-size: 66px; font-weight: 650; letter-spacing: -0.015em; line-height: 1.1; z-index: 30; white-space: nowrap; }

      /* ---------- plansze: tlo jak w panelu PerfOS (#0f0f0f z delikatna siatka), tresc w kroju Geist */
      .panel { position: absolute; inset: 0; z-index: 10; overflow: hidden; font-family: var(--font-brand); }
      .panel.top { z-index: 35; }
      .pbg { position: absolute; inset: 0; background:
        radial-gradient(90% 46% at 50% 0%, rgba(var(--accent-rgb),.10) 0%, rgba(var(--accent-rgb),0) 70%),
        linear-gradient(rgba(255,255,255,.035) 2px, transparent 2px) 0 0 / 120px 120px,
        linear-gradient(90deg, rgba(255,255,255,.035) 2px, transparent 2px) 0 0 / 120px 120px, var(--ground); }
      .pin { position: absolute; inset: 0; }
      .plogo { position: absolute; left: 411px; width: 258px; height: 64px; }
      .p-head { position: absolute; left: 0; right: 0; text-align: center; color: var(--accent); font-size: 30px; font-weight: 600; letter-spacing: .16em; }
      .tile { width: 96px; height: 96px; border-radius: 24px; display: grid; place-items: center; color: var(--on-accent); flex: none;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 40px rgba(var(--accent-rgb),.45), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.md { width: 72px; height: 72px; border-radius: 20px; box-shadow: 0 0 28px rgba(var(--accent-rgb),.38), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.sm { width: 56px; height: 56px; border-radius: 16px; box-shadow: 0 0 24px rgba(var(--accent-rgb),.4), inset 0 1px 0 rgba(255,255,255,.35); }

      /* P1: wiersze z przelacznikiem (motyw marki: litera P z przelacznikiem) */
      .srows { position: absolute; left: 195px; width: 690px; display: flex; flex-direction: column; gap: 20px; }
      .srow { height: 112px; border-radius: 28px; background: #161616; border: 1.5px solid #262626; display: flex; align-items: center; gap: 24px; padding: 0 26px; }
      .slbl { flex: 1; font-size: 40px; font-weight: 600; letter-spacing: -0.01em; white-space: nowrap; }
      .sw { width: 92px; height: 50px; border-radius: 100px; background: #2a2a2a; position: relative; flex: none; }
      .knob { position: absolute; left: 5px; top: 5px; width: 40px; height: 40px; border-radius: 50%; background: #8a8a8f; }

      /* liczby z toczacymi sie cyframi */
      .nw { display: inline-flex; align-items: flex-start; line-height: 1; font-variant-numeric: tabular-nums; }
      .nwd { display: inline-block; height: 1em; overflow: hidden; }
      .nwc { display: flex; flex-direction: column; }
      .nwc i { display: block; height: 1em; line-height: 1em; font-style: normal; text-align: center; }
      .nws { display: inline-block; line-height: 1em; }

      /* P2: zestawy reklam */
      .bignum { position: absolute; left: 0; right: 0; text-align: center; font-size: 190px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; color: var(--accent);
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.4)); }
      .biglbl { position: absolute; left: 0; right: 0; text-align: center; font-size: 38px; font-weight: 500; color: #c4c4cc; }
      .pills { position: absolute; left: 0; right: 0; display: flex; justify-content: center; gap: 14px; }
      .pl { display: inline-flex; align-items: center; gap: 12px; height: 64px; padding: 0 26px; border-radius: 100px; font-size: 32px; font-weight: 600; white-space: nowrap; }
      .pl.acc { background: var(--accent); color: var(--on-accent); box-shadow: 0 0 34px rgba(var(--accent-rgb),.35); }
      .pl.gray { background: #1c1c1c; border: 1.5px solid #343434; color: #d4d4d8; }
      .pl.gray b { color: #fff; font-weight: 700; }
      .pl img { width: 26px; height: 32px; display: block; }
      .adgrid { position: absolute; left: 195px; width: 690px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
      .ad { position: relative; height: 78px; border-radius: 16px; background: #161616; border: 1.5px solid #2a2a2a; padding: 0 12px; display: grid;
        grid-template-columns: 50px 1fr; grid-template-rows: 1fr 1fr; column-gap: 12px; row-gap: 0; align-items: center; }
      .adimg { grid-row: 1 / 3; width: 50px; height: 54px; border-radius: 10px; background: rgba(var(--accent-rgb),.16); color: var(--accent); display: grid; place-items: center; }
      .adl { height: 9px; border-radius: 6px; background: #4a4a4f; width: 100%; align-self: end; margin-bottom: 5px; }
      .adl.s { width: 62%; background: #333336; align-self: start; margin: 5px 0 0; }
      .adoff { position: absolute; right: -9px; top: -11px; width: 40px; height: 40px; border-radius: 50%; background: #3f3f46; color: #fff; display: grid; place-items: center; border: 3px solid #0f0f0f; }

      /* karty z panelu PerfOS (odtworzone ze zrzutow) */
      .card { position: absolute; left: 195px; width: 690px; border-radius: 36px; background: #131313; border: 1.5px solid #262626; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .card.fun { padding: 32px 38px 30px; }
      .chead { display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
      .chead.sm { margin-bottom: 12px; gap: 14px; }
      .ctile { width: 64px; height: 64px; border-radius: 18px; background: #1c1c1c; border: 1.5px solid #2a2a2a; color: #d4d4d8; display: grid; place-items: center; flex: none; }
      .ctile.sm { width: 48px; height: 48px; border-radius: 14px; }
      .ctitle { font-size: 40px; font-weight: 600; letter-spacing: -0.01em; }
      .chead.sm .ctitle { font-size: 32px; }
      .frow { border-radius: 18px; padding: 4px 12px 10px; margin: 0 -12px; }
      .fl { display: flex; justify-content: space-between; align-items: center; height: 48px; font-size: 36px; font-weight: 500; color: #a1a1aa; }
      .fv { font-size: 40px; font-weight: 700; color: #fff; }
      .ftrack { height: 18px; border-radius: 100px; background: #1f1f1f; margin-top: 10px; overflow: hidden; }
      .ffill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #6ee7b7, var(--accent)); transform-origin: left center; }
      .fconv { display: flex; align-items: center; gap: 8px; height: 34px; margin: 6px 0 2px; font-size: 28px; font-weight: 500; color: var(--soft); }
      .card.kpi { padding: 28px 38px 28px; min-height: 220px; }
      .klabel { font-size: 34px; font-weight: 500; color: #a1a1aa; line-height: 40px; }
      .kico { position: absolute; right: 30px; top: 26px; }
      .kval { font-size: 112px; font-weight: 700; letter-spacing: -0.035em; line-height: 1; margin-top: 12px; color: #fff; white-space: nowrap; display: flex; align-items: flex-start; }
      .kval.xl { font-size: 176px; margin-top: 18px; }
      .kval .unit { line-height: 1em; }
      .ksub { font-size: 32px; font-weight: 500; color: var(--soft); margin-top: 22px; }
      .spark { position: absolute; right: 34px; bottom: 30px; }
      .card.chartc { padding: 22px 38px 20px; }
      .legend { display: flex; gap: 34px; font-size: 28px; font-weight: 500; color: #a1a1aa; margin-bottom: 12px; white-space: nowrap; }
      .legend b { color: #fff; font-weight: 700; margin-left: 6px; }
      .ld { display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: #6ee7b7; margin-right: 10px; }
      .ll { display: inline-block; width: 26px; height: 5px; border-radius: 3px; background: #4f8ff7; margin-right: 10px; vertical-align: middle; }
      .plot { display: block; }
      .dash { stroke-dasharray: 1000; }

      /* P6: karta Shopify (odtworzona ze zrzutu, jasna jak oryginal) */
      .shop { position: absolute; left: 195px; width: 690px; border-radius: 30px; background: #ffffff; color: #111; padding: 34px 40px 28px; font-family: var(--font-ui); box-shadow: 0 30px 90px rgba(0,0,0,.6); }
      .sh-v { font-size: 74px; font-weight: 700; letter-spacing: -0.02em; line-height: 1; display: flex; align-items: flex-start; white-space: nowrap; }
      .sh-t { font-size: 30px; font-weight: 600; margin-top: 14px; color: #111; }
      .sh-plot { position: relative; margin-top: 22px; padding-left: 104px; height: 198px; }
      .sh-y { position: absolute; left: 0; font-size: 28px; line-height: 28px; color: #4b4b4b; white-space: nowrap; }
      .sh-plot svg { display: block; }
      .sh-x { display: flex; justify-content: space-between; padding-left: 104px; margin-top: 8px; font-size: 28px; color: #4b4b4b; }

      /* ---------- nakladki na wideo: stoja nad napisami (pas 950-1130 px), bo gore kadru zajmuje glowa */
      .chipwrap { position: absolute; left: 0; right: 0; top: 985px; display: flex; justify-content: center; z-index: 25; }
      .chip2 { display: flex; align-items: center; gap: 18px; padding: 14px 30px 14px 14px; border-radius: 100px; background: rgba(15,15,15,.88);
        border: 1.5px solid rgba(255,255,255,.14); font-size: 30px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .okpart { display: flex; align-items: center; gap: 12px; color: var(--ok); padding-left: 18px; border-left: 1.5px solid rgba(255,255,255,.16); }
      .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: var(--on-accent); background: var(--ok); box-shadow: 0 0 24px rgba(var(--ok-rgb),.45); flex: none; }
      .dot.sm { width: 40px; height: 40px; }
      .tags { position: absolute; left: 0; right: 0; top: 1052px; display: flex; justify-content: center; gap: 14px; z-index: 26; }
      .tag { height: 76px; padding: 0 28px; border-radius: 100px; display: inline-flex; align-items: center; font-size: 34px; font-weight: 800; letter-spacing: .06em;
        background: rgba(15,15,15,.88); border: 2px solid rgba(var(--accent-rgb),.85); color: #fff; box-shadow: 0 14px 40px rgba(0,0,0,.4), 0 0 26px rgba(var(--accent-rgb),.25); }
      .msgw { position: absolute; left: 0; right: 0; top: 946px; display: flex; flex-direction: column; align-items: center; z-index: 26; }
      .msg-n { font-size: 28px; font-weight: 800; letter-spacing: .16em; color: #e4e4e7; margin-bottom: 10px; filter: drop-shadow(0 2px 8px rgba(0,0,0,.7)); }
      .msg-b { background: rgba(28,28,30,.95); border: 1.5px solid rgba(255,255,255,.12); border-radius: 34px 34px 34px 10px; padding: 20px 34px; font-size: 44px; font-weight: 650;
        line-height: 1.18; text-align: left; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.4); }
      .mw { display: inline-block; }

      .ctawrap { position: absolute; left: 0; right: 0; top: 990px; display: flex; justify-content: center; z-index: 26; }
      .cbox { width: 680px; display: flex; align-items: center; gap: 20px; padding: 14px 14px 14px 16px; border-radius: 100px; background: rgba(15,15,15,.9);
        border: 1.5px solid rgba(255,255,255,.16); box-shadow: 0 18px 50px rgba(0,0,0,.4); }
      .cav { width: 74px; height: 74px; border-radius: 50%; background: #2a2a2a; color: #b9bcc3; display: grid; place-items: center; flex: none; }
      .cin { flex: 1; position: relative; height: 74px; display: flex; align-items: center; font-size: 40px; white-space: nowrap; }
      .cph { position: absolute; left: 0; color: #8a8a93; font-weight: 500; }
      .ctyped { display: flex; font-weight: 750; color: #fff; letter-spacing: .02em; }
      .cl { display: none; }
      .caret { width: 4px; height: 48px; background: var(--accent); margin-left: 4px; border-radius: 2px; }
      .csend { width: 74px; height: 74px; border-radius: 50%; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); color: var(--on-accent); display: grid; place-items: center;
        flex: none; box-shadow: 0 0 30px rgba(var(--accent-rgb),.5); }

      .bubble { position: absolute; left: 240px; width: 600px; top: 446px; height: 250px; border-radius: 60px; display: grid; place-items: center;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 90px rgba(var(--accent-rgb),.45), inset 0 2px 0 rgba(255,255,255,.35); }
      .bubble::after { content: ""; position: absolute; left: 110px; bottom: -50px; width: 0; height: 0; border-right: 66px solid transparent; border-top: 56px solid var(--accent); }
      .bubble span { font-size: 128px; font-weight: 800; letter-spacing: -0.02em; color: var(--on-accent); line-height: 1; }
      .endtxt { position: absolute; left: 0; right: 0; top: 806px; text-align: center; font-size: 60px; font-weight: 700; letter-spacing: -0.01em; }
      .endsub { position: absolute; left: 0; right: 0; top: 892px; text-align: center; font-size: 40px; font-weight: 500; color: #c4c4cc; }

      .leak { position: absolute; inset: -10%; z-index: 40; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(45% 35% at 30% 45%, rgba(var(--accent-rgb),.6), rgba(var(--accent-rgb),0) 70%),
                    radial-gradient(40% 30% at 70% 60%, rgba(255,255,255,.5), rgba(255,255,255,0) 70%),
                    radial-gradient(60% 50% at 50% 50%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
    <div id="vwrap">
      <video id="aroll" class="clip" src="aroll.mp4" data-start="0" data-duration="{{TOTAL}}" data-track-index="0" muted playsinline></video>
      <audio id="glos" src="glos.wav" data-start="0" data-duration="{{TOTAL}}" data-track-index="9"></audio>
    </div>
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

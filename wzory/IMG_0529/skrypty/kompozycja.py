#!/usr/bin/env python3
"""Grafiki odcinka (HyperFrames): kazda grafika = osobna kompozycja 1920x1080 z przezroczystym tlem, renderowana
w 4K (DPR 2) do ProRes 4444 z alfa i nakladana na A-roll w ../skrypty/finalny.py.

Styl jak w zatwierdzonej rolce IMG_0526 (bez logo adGen): Inter Tight, ciemne plansze #0f1012, kwadraty i kafelki
w kolorze akcentu z paleta.py (personal brand: #00E5A0), wejscia z rozmyciem i light leakiem.
Czasy grafik biora sie ze slow (czas w nagraniu -> os montazu przez ../aroll/edl.json), nie sa wpisane na sztywno.

Uzycie: python3 -I kompozycja.py            -> ../hf/o_*.html + ../hf/grafiki.json (lista: plik, start, dlugosc)
        python3 -I kompozycja.py --lista    -> tylko wypisz czasy
"""
import html
import json
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
HF = P / "hf"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from paleta import MARKA, PALETY, kolory  # noqa: E402  (paleta: personal brand albo stary pomarancz)

ACCENT = PALETY[MARKA]["accent"]

EDL = json.loads((P / "aroll/edl.json").read_text())
WORDS = json.loads((P / "analiza/slowa_kawalki.json").read_text())
ALLW = sorted([(cid[:2], a, b, t) for cid, ws in WORDS.items() for a, b, t in ws], key=lambda w: (w[0], w[1]))
TOTAL = EDL[-1]["t_out"] + EDL[-1].get("video_extra", 0.0)
SPEECH_END = EDL[-1]["t_out"]


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


def out_t(src, t):
    for e in EDL:
        if e["src"] == src and e["a_in"] - 0.02 <= t < e["a_out"] + 0.02:
            return e["t_in"] + (t - e["a_in"])
    return None


def W(src, word, after=0.0, end=False):
    """Czas (os montazu) poczatku (albo konca) pierwszego slowa `word` w zrodle `src` po czasie `after`
    (czas w nagraniu), ktore jest w montazu."""
    for s, a, b, t in ALLW:
        if s == src and a >= after - 1e-6 and norm(t).startswith(norm(word)):
            o = out_t(src, b if end else a)
            if o is not None:
                return round(o, 3)
    raise SystemExit(f"Nie znaleziono slowa w montazu: {src} '{word}' po {after}")


ICON = {
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22 11 13 2 9z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>',
    "up": '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M19 10v1a7 7 0 0 1-14 0v-1"/><path d="M12 18v4"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98"/><path d="m15.41 6.51-6.82 3.98"/>',
    "film": '<rect x="2" y="2" width="20" height="20" rx="2.18"/><path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 17h5M17 7h5"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "thumb": '<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "snow": '<path d="M2 12h20M12 2v20M20 16l-4-4 4-4M4 8l4 4-4 4M16 4l-4 4-4-4M8 20l4-4 4 4"/>',
    "flow": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/>',
    "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
}


def icon(name, size, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def esc(t):
    return html.escape(t)


AGENTS = {
    "artur": ("Artur", "Szef Growth", "assets/artur_avatar.png", True),
    "kaja": ("Kaja", "Sprzedaż", "assets/kaja_avatar.png", True),
    "weronika": ("Weronika", "Marketing AdGen", "assets/weronika_avatar.png", True),
    "tymon": ("Tymon", "Marka osobista", "assets/tymon_avatar.png", False),
}


class Comp:
    """Jedna grafika = jedna kompozycja HyperFrames (czas lokalny od 0)."""

    def __init__(self, name, t_in, t_out, kind="overlay"):
        self.name, self.t_in, self.t_out, self.kind = name, round(t_in, 3), round(t_out, 3), kind
        self.el, self.js = [], []

    def L(self, t):  # czas globalny -> lokalny
        return max(0.0, round(t - self.t_in, 3))

    @property
    def dur(self):
        return round(self.t_out - self.t_in, 3)

    def add(self, html_):
        self.el.append(html_)

    def fromto(self, sel, a, b, t, dur=0.35, ease="power3.out"):
        self.js.append(f'tl.fromTo("{sel}",{a},{{...{b},duration:{dur},ease:"{ease}"}},{self.L(t):.3f});')

    def to(self, sel, b, t, dur=0.3, ease="power2.in"):
        self.js.append(f'tl.to("{sel}",{{...{b},duration:{dur},ease:"{ease}"}},{self.L(t):.3f});')

    def pop(self, sel, t, dy=26):
        self.fromto(sel, f"{{opacity:0,y:{dy},scale:0.94}}", "{opacity:1,y:0,scale:1}", t, 0.32, "back.out(1.6)")

    def blur_in(self, sel, t, x=0, y=0, dur=0.4):
        self.fromto(sel, f'{{opacity:0,x:{x},y:{y},filter:"blur(12px)"}}', '{opacity:1,x:0,y:0,filter:"blur(0px)"}', t, dur)

    def blur_out(self, sel, t, x=0, y=0, dur=0.25):
        self.to(sel, f'{{opacity:0,x:{x},y:{y},filter:"blur(10px)"}}', t, dur)

    def html(self):
        body = "\n      ".join(self.el)
        js = "\n      ".join(self.js)
        return kolory(TEMPLATE.replace("{{DUR}}", f"{self.dur:.3f}").replace("{{ELEMENTS}}", body)
                       .replace("{{JS}}", js))


COMPS = []


def comp(name, t_in, t_out, kind="overlay"):
    c = Comp(name, t_in, t_out, kind)
    COMPS.append(c)
    return c


# ---------------------------------------------------------------------------------------------------------
# elementy wielokrotnego uzytku

def board(c, inner, leak_in=True, leak_out=True, fade_out=True, cls=""):
    """Pelnoekranowa plansza (ciemne tlo), wejscie: rozmycie + light leak. Kwadraty dekoracyjne tylko w palecie adGen:
    w personal brandzie Jakub je odrzucil (IMG_0576, 17.11.2026: "nie podoba mi sie to")."""
    sq = '<div class="sq sq1"></div><div class="sq sq2"></div><div class="sq sq3"></div>' if MARKA == "adgen" else ""
    c.add(f'<div id="bd" class="board {cls}"><div class="pbg"></div>{sq}{inner}</div>')
    c.fromto("#bd", '{opacity:0,scale:1.06,filter:"blur(18px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', c.t_in, 0.34)
    d = c.dur
    if sq:
        c.js.append(f'tl.fromTo("#bd .sq1",{{rotation:-14,y:50}},{{rotation:-6,y:0,duration:{d:.3f},ease:"none"}},0);')
        c.js.append(f'tl.fromTo("#bd .sq2",{{rotation:18,y:30}},{{rotation:9,y:-20,duration:{d:.3f},ease:"none"}},0);')
        c.js.append(f'tl.fromTo("#bd .sq3",{{rotation:8}},{{rotation:20,duration:{d:.3f},ease:"none"}},0);')
    if leak_in:
        leak(c, c.t_in + 0.12)
    if fade_out:
        c.to("#bd", '{opacity:0,scale:1.03,filter:"blur(14px)"}', c.t_out - 0.22, 0.22)
        if leak_out:
            leak(c, c.t_out - 0.05)


def leak(c, t):
    k = len([e for e in c.el if 'class="leak' in e])
    lid = f"lk{k}"
    c.add(f'<div id="{lid}" class="leak"></div>')
    c.fromto(f"#{lid}", "{opacity:0,xPercent:-18}", "{opacity:1,xPercent:0}", t - 0.22, 0.2, "power2.out")
    c.to(f"#{lid}", "{opacity:0,xPercent:16}", t - 0.02, 0.3)


def side(c, inner, pos="left", top=150, width=560, cid="sc"):
    """Karta z boku kadru (szklo), wejscie z rozmyciem od krawedzi."""
    x = 70 if pos == "left" else 1920 - 70 - width
    c.add(f'<div id="{cid}" class="card" style="left:{x}px;top:{top}px;width:{width}px">{inner}</div>')
    dx = -50 if pos == "left" else 50
    c.blur_in(f"#{cid}", c.t_in, x=dx)
    c.blur_out(f"#{cid}", c.t_out - 0.28, x=dx * 0.6)


def avatar(key, size, ring=True, cls="av"):
    name, role, src, _ = AGENTS[key]
    r = " ring" if ring else ""
    return f'<span class="{cls}{r}" style="width:{size}px;height:{size}px"><img src="{src}" alt=""></span>'


def profile_card(key, cid):
    """Odtworzony profil agenta (jak na zrzucie z aplikacji): awatar, nazwa, udostepnienie, zakladki."""
    name, role, src, shared = AGENTS[key]
    sh = (f'<div class="pf-shared">{icon("users", 22)}<span>Udostępniono zespołowi Jakub\'s team</span></div>'
          if shared else '<div class="pf-shared" style="visibility:hidden">.</div>')
    return (f'<div class="pf" id="{cid}"><div class="pf-av"><img src="{src}" alt=""></div>'
            f'<div class="pf-name">{esc(name)} · {esc(role)}</div>{sh}'
            f'<div class="pf-tabs"><span class="pf-tab act">Aktywność</span><span class="pf-tab">Biblioteka</span></div></div>')


def rows(items, cls="rw"):
    """Wiersze z kafelkiem ikony: [(id, ikona, tekst)]"""
    return "".join(f'<div class="{cls}" id="{i}"><span class="tile">{icon(ic, 30)}</span><span>{t}</span></div>'
                   for i, ic, t in items)


def chip(c, cid, ic, text, t_in, t_out, pos="top", ok=False, x=None, y=None):
    style = ""
    if pos == "top":
        style = "left:0;right:0;top:64px;justify-content:center"
    elif pos == "topleft":
        style = "left:70px;top:70px"
    elif pos == "topright":
        style = "right:70px;top:70px;justify-content:flex-end"
    elif pos == "bottom":
        style = "left:0;right:0;bottom:90px;justify-content:center"
    if x is not None:
        style = f"left:{x}px;top:{y}px"
    okp = f'<span class="okpart">{icon("check", 22, "okic")}</span>' if ok else ""
    c.add(f'<div id="{cid}" class="chipwrap" style="{style}"><div class="chip2"><span class="tile sm">{icon(ic, 26)}</span>'
          f'<span>{text}</span>{okp}</div></div>')
    c.blur_in(f"#{cid}", t_in, y=-24)
    c.blur_out(f"#{cid}", t_out - 0.25, y=-16)


def kin_words(c, cid, parts, top=760, size=96):
    """Tekst kinetyczny: parts = [(tekst, t, styl)], styl: 's' maly, 'b' duzy, 'o' duzy w kolorze akcentu."""
    spans = []
    for k, (txt, t, st) in enumerate(parts):
        spans.append(f'<span class="kw {st}" id="{cid}w{k}">{esc(txt)}</span>')
    c.add(f'<div id="{cid}" class="kin" style="top:{top}px;font-size:{size}px">{"".join(spans)}</div>')
    for k, (txt, t, st) in enumerate(parts):
        if st == "s":
            c.fromto(f"#{cid}w{k}", '{opacity:0,y:18,filter:"blur(8px)"}', '{opacity:1,y:0,filter:"blur(0px)"}', t - 0.04, 0.18, "power2.out")
        else:
            c.fromto(f"#{cid}w{k}", '{opacity:0,scale:1.35,filter:"blur(14px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t - 0.05, 0.26)


def chapter(name, num, title, t_in, t_out, sub=""):
    c = comp(name, t_in, t_out, "board")
    inner = (f'<div class="ch-num" id="chn">{num}</div><div class="ch-title" id="cht">{esc(title)}</div>'
             + (f'<div class="ch-sub" id="chs">{esc(sub)}</div>' if sub else ""))
    board(c, inner)
    c.pop("#chn", t_in + 0.05, 30)
    c.blur_in("#cht", t_in + 0.15, y=24, dur=0.45)
    if sub:
        c.blur_in("#chs", t_in + 0.35, y=16)
    return c


# ---------------------------------------------------------------------------------------------------------
def build():
    # ===== WSTEP =====
    # Hook: "Zautomatyzowalem caly dzial growth. Co to znaczy? Marketing i sprzedaz"
    h0 = W("m7", "zautomatyzowałem", 49.0)
    c = comp("hook", max(0.0, h0 - 0.1), W("m7", "sprzedaż", 52.5, end=True) + 0.55)
    kin_words(c, "kh", [("Zautomatyzowałem", h0, "s"), ("cały", W("m7", "cały", 49.0), "s"),
                        ("dział", W("m7", "dział", 49.0), "s"), ("GROWTH", W("m7", "growth", 49.0), "o")], top=835, size=110)
    t_co = W("m7", "co", 50.9)
    c.to("#kh", '{opacity:0,y:-20,filter:"blur(10px)"}', t_co - 0.1, 0.22)
    kin_words(c, "km", [("Co to znaczy?", t_co, "s"), ("MARKETING", W("m7", "marketing", 51.5), "b"),
                        ("+", W("m7", "i", 52.5), "s"), ("SPRZEDAŻ", W("m7", "sprzedaż", 52.5), "o")], top=835, size=100)
    c.js.append(f'gsap.set("#km",{{opacity:1}});')
    c.to("#km", '{opacity:0,y:-16,filter:"blur(10px)"}', c.t_out - 0.25, 0.22)

    # adGen: kwalifikowane, przedzwonione leady -> prawo / finanse / OZE (karta po lewej)
    t0 = W("m7", "dla", 55.0)
    c = comp("adgen", t0 - 0.1, W("m7", "moi", 64.0) - 0.05)
    inner = ('<div class="cd-k">CZYM ZAJMUJE SIĘ ADGEN</div>'
             '<div class="cd-h" id="adh">Kwalifikowane, <span class="o">przedzwonione</span> leady</div>'
             '<div class="tags">'
             f'<span class="tag" id="ag0">{icon("handshake", 26)}Prawo</span>'
             f'<span class="tag" id="ag1">{icon("wallet", 26)}Finanse</span>'
             f'<span class="tag" id="ag2">{icon("zap", 26)}OZE</span></div>')
    side(c, inner, "left", top=160, width=600)
    c.blur_in("#adh", W("m7", "pozyskujemy", 58.0) - 0.05, y=14)
    c.pop("#ag0", W("m7", "prawnej", 61.0) - 0.06)
    c.pop("#ag1", W("m7", "finansowej", 61.0) - 0.06)
    c.pop("#ag2", W("m7", "o", 63.5) - 0.06)

    # Imie i nazwisko (dolna belka) przy "Moi drodzy"
    t0 = W("m7", "moi", 64.0)
    c = comp("belka_start", t0 + 0.2, t0 + 5.0)
    c.add('<div class="lower" id="lw"><span class="lw-bar"></span><div><div class="lw-n">Jakub Derda</div>'
          '<div class="lw-s">AI w biznesie · adGen</div></div></div>')
    c.blur_in("#lw", c.t_in, x=-40)
    c.blur_out("#lw", c.t_out - 0.3, x=-30)

    # "pol roku pracy" + "zredukowalismy zespol"
    t0 = W("m7", "półrocznej", 70.5)
    c = comp("pol_roku", t0 - 0.1, t0 + 3.0)
    chip(c, "cpr", "clock", "PÓŁ ROKU PRACY", t0 - 0.1, t0 + 3.0, pos="topleft")

    # Parenascie etatow -> 2
    t0 = W("m7", "zeszliśmy", 94.0)
    t2 = W("m7", "dwóch", 96.5)
    c = comp("etaty", t0 - 0.15, t2 + 1.6)
    c.add('<div class="kin" id="ket" style="top:850px;font-size:84px">'
          '<span class="kw s" id="ket0">paręnaście etatów</span><span class="kw s arrow" id="ket1">→</span>'
          '<span class="kw o" id="ket2">2</span></div>')
    c.fromto("#ket0", '{opacity:0,y:18,filter:"blur(8px)"}', '{opacity:1,y:0,filter:"blur(0px)"}', t0, 0.25)
    c.fromto("#ket1", '{opacity:0,x:-20}', '{opacity:1,x:0}', t2 - 0.4, 0.2)
    c.fromto("#ket2", '{opacity:0,scale:1.6,filter:"blur(14px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t2 - 0.05, 0.3)
    c.js.append(f'tl.to("#ket0",{{color:"#8a8d94",duration:0.3}},{c.L(t2):.3f});')
    c.to("#ket", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # Rok temu vs dzis (karta po prawej, buduje sie)
    t0 = W("m7", "zespół", 109.0)
    t_rev = W("m7", "dwa", 116.0)
    t_now = W("m7", "teraz", 121.5)
    t_end = W("m7", "niesamowite", 125.0)
    c = comp("porownanie", t0 - 0.2, t_end + 0.2)
    inner = ('<div class="cd-k">ZESPÓŁ</div>'
             '<div class="cmp">'
             '<div class="cmp-c" id="cp0"><div class="cmp-l">ROK TEMU</div><div class="cmp-v">14–15</div><div class="cmp-u">osób</div></div>'
             f'<div class="cmp-arr" id="cpa">{icon("up", 40)}</div>'
             '<div class="cmp-c o" id="cp1"><div class="cmp-l">DZIŚ</div><div class="cmp-v">5</div><div class="cmp-u">osób w sumie</div></div></div>'
             '<div class="cd-k" style="margin-top:26px">PRZYCHÓD</div>'
             '<div class="bars2"><div class="b2" id="bb0"><span class="b2l">rok temu</span><div class="b2t"><div class="b2f g" id="bf0"></div></div></div>'
             '<div class="b2" id="bb1"><span class="b2l o">dziś</span><div class="b2t"><div class="b2f o" id="bf1"></div></div><span class="b2x">×2,5</span></div></div>')
    side(c, inner, "left", top=150, width=620)
    c.js.append('gsap.set("#cp1,#cpa,#bb1",{opacity:0});')
    c.pop("#cp0", t0 + 0.6)
    c.pop("#bb0", t_rev - 0.1)
    c.js.append(f'tl.fromTo("#bf0",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{c.L(t_rev):.3f});')
    c.pop("#bb1", t_rev + 0.8)
    c.js.append(f'tl.fromTo("#bf1",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out"}},{c.L(t_rev + 0.9):.3f});')
    c.fromto("#cpa", '{opacity:0,rotation:-90}', '{opacity:1,rotation:90}', t_now - 0.3, 0.3)
    c.pop("#cp1", t_now)

    # Przychody x2,5 / zespol 3x mniejszy (plansza)
    t0 = W("m7", "przychody", 137.0)
    t_z = W("m7", "zespół", 140.9)
    t_end = W("m7", "pięknego", 143.3, end=True)
    c = comp("x25", t0 - 0.15, t_end + 0.25, "board")
    inner = ('<div class="big2">'
             '<div class="bg2" id="bx0"><div class="bg2-v o">×2,5</div><div class="bg2-l">PRZYCHÓD</div></div>'
             '<div class="bg2" id="bx1"><div class="bg2-v">3×</div><div class="bg2-l">MNIEJSZY ZESPÓŁ</div></div></div>')
    board(c, inner)
    c.fromto("#bx0", '{opacity:0,scale:1.4,filter:"blur(16px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', W("m7", "razy", 137.0) - 0.05, 0.32)
    c.fromto("#bx1", '{opacity:0,scale:1.4,filter:"blur(16px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t_z, 0.32)

    # Plan odcinka (karta po lewej, punkty pojawiaja sie, gdy je wymienia)
    t1 = W("m7", "po", 159.5)
    t2 = W("m7", "jaka", 175.0)
    t3 = W("m7", "następnie", 190.0)
    t4 = W("m7", "kosztach", 201.5)
    t_end = W("m7", "bardzo", 204.0)  # "jak bardzo udalo sie to zredukowac" -> potem plansza 30 tys.
    c = comp("plan", t1 - 0.3, t_end + 1.2)
    items = [("pl0", "trend", "Dlaczego growth"), ("pl1", "users", "Struktura działu"),
             ("pl2", "x", "Czego AI (jeszcze) nie zrobi"), ("pl3", "wallet", "Koszty")]
    inner = '<div class="cd-k">W TYM ODCINKU</div><div class="plan">' + "".join(
        f'<div class="pl" id="{i}"><span class="pl-n">{k + 1:02d}</span><span class="tile sm">{icon(ic, 26)}</span><span>{esc(t)}</span></div>'
        for k, (i, ic, t) in enumerate(items)) + "</div>"
    side(c, inner, "left", top=170, width=620)
    for (i, _, _), t in zip(items, (t1, t2, t3, t4)):
        c.pop(f"#{i}", t - 0.05)
        c.js.append(f'tl.to("#{i} .pl-n",{{color:"{ACCENT}",duration:0.2}},{c.L(t):.3f});')

    # 30 000 zl na poczatku roku (plansza)
    t0 = W("m7", "początkiem", 209.0)
    t30 = W("m7", "30", 211.5)
    t_end = W("m7", "marki", 217.0, end=True)
    c = comp("30k", t0 - 0.2, t_end + 0.35, "board")
    inner = ('<div class="k30-l" id="k30l">POCZĄTEK ROKU</div><div class="k30" id="k30">~30 000 zł</div>'
             '<div class="k30-s" id="k30s">marketing · sprzedaż · promocja marki</div>')
    board(c, inner)
    c.blur_in("#k30l", t0, y=14)
    c.fromto("#k30", '{opacity:0,scale:1.4,filter:"blur(16px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t30 - 0.05, 0.32)
    c.blur_in("#k30s", W("m7", "marketing", 213.5) - 0.05, y=12)

    # "Ile dzis? -> na koncu odcinka"
    t0 = W("m7", "jaka", 222.0)
    c = comp("ile_dzis", t0 - 0.1, W("m7", "wytrwałych", 229.5, end=True) + 0.3)
    chip(c, "cid", "wallet", "A ILE DZIŚ? &nbsp;<span class='o'>NA KOŃCU ODCINKA</span>", c.t_in, c.t_out, pos="topleft")

    # ===== ROZDZIAL 1 =====
    t0 = W("m7", "możemy", 233.5)
    chapter("roz1", "01", "Dlaczego growth", t0 - 0.15, t0 + 2.6, "pierwszy dział do automatyzacji")

    # Dlaczego growth: zwraca sie najszybciej
    t1 = W("m8", "ponieważ", 25.5)
    t2 = W("m8", "najszybciej", 28.9)
    t3 = W("m8", "motywację", 32.0)
    c = comp("dlaczego", t1 - 0.2, W("m8", "działy", 34.5, end=True) + 0.6)
    inner = ('<div class="cd-k">DLACZEGO OD GROWTH?</div><div class="chk">'
             + "".join(f'<div class="ck" id="ck{k}"><span class="dot">{icon("check", 22)}</span><span>{t}</span></div>'
                       for k, t in enumerate(["Najszybciej się zwraca", "Szybko widać efekty", "Motywacja do kolejnych działów"]))
             + "</div>")
    side(c, inner, "left", top=180, width=620)
    for k, t in enumerate((t1, t2, t3)):
        c.pop(f"#ck{k}", t)

    # ===== ROZDZIAL 2 =====
    t0 = W("m8", "jaka", 43.5)
    chapter("roz2", "02", "Struktura działu", t0 - 0.15, W("m8", "działu", 46.0, end=True) + 0.4, "4 agentów AI")

    # Lista agentow (odtworzony ekran "Growth")
    t0 = W("m8", "pokazuję", 51.0)
    c = comp("lista", t0 - 0.35, W("m8", "rzeczy", 58.5, end=True) + 0.3, "board")
    lst = [("tymon", "Ściąga do odcinka jest gotowa: 1…", False),
           ("kaja", 'Na karcie <span class="priv">Klimkowskiego</span> zapisała…', True),
           ("weronika", "Gotowe, wszystkie trzy rzeczy są…", True),
           ("artur", "Rytm rutyn jest ustawiony. Pierws…", True)]
    rws = ""
    for k, (key, prev, shared) in enumerate(lst):
        name, role, src, _ = AGENTS[key]
        ppl = icon("users", 22, "ppl") if shared else ""
        rws += (f'<div class="ag-r{" sel" if k == 0 else ""}" id="ar{k}"><span class="ag-av"><img src="{src}" alt=""></span>'
                f'<div class="ag-t"><div class="ag-n">{esc(name)} · {esc(role)} {ppl}</div><div class="ag-p">{prev}</div></div></div>')
    inner = f'<div class="ag" id="ag"><div class="ag-h">Growth 📈</div>{rws}</div><div class="ag-cap" id="agc">4 agentów działu growth</div>'
    board(c, inner)
    c.pop("#ag", t0 - 0.2, 40)
    for k in range(4):
        c.pop(f"#ar{k}", t0 + 0.15 + 0.22 * k, 18)
    c.blur_in("#agc", W("m8", "czterech", 51.5), y=12)

    # Artur - profil (karta po lewej)
    t0 = W("m8", "jest", 59.4)
    t_a = W("m8", "artur", 60.5)
    c = comp("artur1", t0 - 0.1, W("m8", "losowe", 64.5, end=True) + 0.2)
    inner = profile_card("artur", "pfa") + '<div class="pf-badge" id="pfab">' + icon("sparkles", 24) + 'AGENT GŁÓWNY</div>'
    side(c, inner, "left", top=140, width=600, cid="sca")
    c.fromto("#pfab", "{opacity:0,scale:0.5}", "{opacity:1,scale:1}", t_a - 0.05, 0.35, "back.out(2.2)")

    # "Imiona? Nadalo je AI"
    t0 = W("m8", "ciekawostka", 65.5)
    c = comp("imiona", t0 - 0.1, W("m8", "nadało", 68.0, end=True) + 0.5)
    chip(c, "cim", "sparkles", "IMIONA NADAŁO SAMO AI", c.t_in, c.t_out, pos="topleft")

    # Schemat: Artur na gorze, pod nim Kaja i Weronika (plansza)
    t0 = W("m8", "także", 69.0)
    t_pod = W("m8", "pod", 73.0)
    t_end = W("m8", "weronikę", 74.3, end=True)
    c = comp("schemat1", t0 - 0.15, t_end + 0.45, "board")
    board(c, org_html(["kaja", "weronika", "tymon"], top="artur", dim=["tymon"]))
    c.pop("#on-artur", t0 + 0.1, 30)
    c.js.append('gsap.set("#org .ln",{strokeDashoffset:400});')
    for k, key in enumerate(["kaja", "weronika", "tymon"]):
        tt = t_pod + 0.25 * k if key != "tymon" else t_pod + 0.9
        c.js.append(f'tl.to("#ln-{key}",{{strokeDashoffset:0,duration:0.4,ease:"power2.out"}},{c.L(tt - 0.25):.3f});')
        if key == "tymon":  # jeszcze nie omawiany - przygaszony
            c.fromto("#on-tymon", "{opacity:0,y:26,scale:0.94}", "{opacity:0.35,y:0,scale:1}", tt, 0.32, "back.out(1.6)")
        else:
            c.pop(f"#on-{key}", tt)

    # Kaja (profil + zadania)
    t0 = W("m8", "kaja", 74.5)
    t_r1 = W("m8", "porządki", 81.5)
    t_r2 = W("m8", "proces", 86.5)
    t_r3 = W("m8", "mierzalny", 90.5)
    c = comp("kaja", t0 + 0.1, W("m8", "closing", 95.5, end=True) + 0.3)
    inner = profile_card("kaja", "pfk") + '<div class="rws">' + rows([
        ("kr0", "kanban", "Porządek w CRM i pipeline"),
        ("kr1", "flow", "Powtarzalny proces sprzedaży"),
        ("kr2", "chart", "Mierzalny i optymalny")]) + "</div>"
    side(c, inner, "left", top=90, width=600, cid="sck")
    for k, t in enumerate((t_r1, t_r2, t_r3)):
        c.pop(f"#kr{k}", t - 0.08)

    # 4 closerow w rok
    t0 = W("m8", "przewinęło", 106.0)
    c = comp("closerzy", t0 - 0.1, W("m8", "handlowców", 109.5, end=True) + 0.9)
    kin_words(c, "kcl", [("4", W("m8", "czterech", 107.5), "o"), ("CLOSERÓW", W("m8", "kluzerów", 108.5), "b"),
                         ("w rok", W("m8", "handlowców", 109.5), "s")], top=835, size=96)
    c.to("#kcl", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # 1/4 etatu, 40-50 h
    t0 = W("m8", "nie", 135.0)
    t_h = W("m8", "40", 143.0)
    c = comp("etat", W("m8", "pomocy", 133.3) - 0.1, W("m8", "60", 146.0, end=True) + 0.5)
    inner = ('<div class="cd-k">SPRZEDAŻ Z SETTEREM AI</div>'
             '<div class="q4"><div class="q4-v" id="q4v">¼</div><div class="q4-t"><div class="q4-l">etatu</div><div class="q4-s">w skali miesiąca</div></div></div>'
             '<div class="hrs" id="hrs">' + icon("clock", 28) + '<span><b>40–50 h</b> / miesiąc</span><span class="hrs-s">czasem 60</span></div>')
    side(c, inner, "left", top=180, width=560)
    c.fromto("#q4v", '{opacity:0,scale:1.5,filter:"blur(14px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', W("m8", "¼", 135.5) - 0.05, 0.3)
    c.pop("#hrs", t_h - 0.05)

    # Weronika (profil + zadania)
    t0 = W("m8", "weronikę", 166.0)
    t_r1 = W("m8", "reklamować", 173.5)
    t_r2 = W("m8", "nailing", 186.0)
    t_r3 = W("m8", "nurturingowe", 189.5)
    c = comp("weronika", t0 - 0.1, W("m8", "tłumaczę", 192.5, end=True) + 0.3)
    inner = profile_card("weronika", "pfw") + '<div class="rws">' + rows([
        ("wr0", "megaphone", "Jak się reklamować"),
        ("wr1", "mail", "Mailing"),
        ("wr2", "flow", "Nurturing: dogrzewanie leadów")]) + "</div>"
    side(c, inner, "left", top=90, width=600, cid="scw")
    for k, t in enumerate((t_r1 - 0.4, t_r2, t_r3)):
        c.pop(f"#wr{k}", t - 0.08)

    # 3 sekwencje maili
    t0 = W("m8", "kampanie", 203.5)
    c = comp("sekwencje", t0 - 0.2, W("m8", "zaprojektowała", 214.0, end=True) + 0.3)
    inner = ('<div class="cd-k">KAMPANIE MAILOWE · 3 SEKWENCJE</div><div class="seq">'
             f'<div class="sq-i" id="sq0"><span class="tile sm">{icon("flow", 24)}</span>Leady w pipeline</div>'
             f'<div class="sq-i" id="sq1"><span class="tile sm">{icon("x", 24)}</span>Leady przegrane</div>'
             f'<div class="sq-i" id="sq2"><span class="tile sm">{icon("snow", 24)}</span>Leady zamrożone</div></div>'
             '<div class="seq-f" id="sqf">' + icon("sparkles", 22) + 'wymyśliła i zaprojektowała Weronika</div>')
    side(c, inner, "left", top=200, width=600)
    c.pop("#sq0", W("m8", "pipeline", 206.0) - 0.1)
    c.pop("#sq1", W("m8", "przegrane", 208.0) - 0.1)
    c.pop("#sq2", W("m8", "zamrożone", 209.0) - 0.1)
    c.blur_in("#sqf", W("m8", "weronika", 211.0), y=10)

    # Newsletter (plansza z przewijanym mailem)
    t0 = W("m8", "podrzucę", 215.5)
    t_end = W("m8", "następnie", 222.3)
    c = comp("mail", t0 - 0.5, t_end - 0.05, "board")
    inner = ('<div class="ml-k" id="mlk">' + icon("mail", 28) + 'Przykładowy mail z sekwencji</div>'
             '<div class="ml" id="ml"><div class="ml-top"><span class="ml-dot"></span><span class="ml-dot"></span><span class="ml-dot"></span>'
             '<span class="ml-subj">Cztery modele w pigułce</span></div>'
             '<div class="ml-vp"><img id="mli" src="assets/newsletter.png" alt=""></div></div>')
    board(c, inner)
    c.pop("#ml", c.t_in + 0.1, 40)
    c.blur_in("#mlk", c.t_in + 0.2, y=12)
    c.js.append(f'tl.fromTo("#mli",{{y:0}},{{y:-700,duration:{c.dur - 1.2:.3f},ease:"power1.inOut"}},0.8);')

    # Tymon (profil + zadania)
    t0 = W("m8", "tymona", 223.0)
    t_r1 = W("m8", "marki", 232.0)
    t_r2 = W("m8", "instagramie", 243.0)
    t_r3 = W("m8", "metryki", 246.0)
    t_r4 = W("m8", "decyzje", 250.5)
    c = comp("tymon", t0 - 0.1, W("m8", "lepsze", 253.4, end=True) + 0.3)
    inner = profile_card("tymon", "pft") + '<div class="rws">' + rows([
        ("tr0", "user", "Strategia marki osobistej"),
        ("tr1", "share", "Instagram · Facebook · YouTube"),
        ("tr2", "chart", "Metryki → lepsze decyzje")]) + "</div>"
    side(c, inner, "left", top=90, width=600, cid="sct")
    c.pop("#tr0", t_r1 - 0.1)
    c.pop("#tr1", t_r2 - 0.1)
    c.pop("#tr2", t_r3 - 0.1)

    # Artur - co robi (profil + zadania)
    t0 = W("m8", "artur", 258.5)
    t_r1 = W("m8", "rozwoju", 266.0)
    t_r2 = W("m8", "przekminiam", 272.0)
    c = comp("artur2", t0 - 0.1, W("m8", "zmniejszyć", 276.0, end=True) + 0.3)
    inner = profile_card("artur", "pfa2") + '<div class="rws">' + rows([
        ("ar0", "trend", "Rozwój sprzedaży i marketingu"),
        ("ar1", "brain", "Praca Kai i Weroniki: więcej czy mniej?")]) + "</div>"
    side(c, inner, "left", top=110, width=600, cid="sca2")
    c.pop("#ar0", t_r1 - 0.1)
    c.pop("#ar1", t_r2 - 0.1)

    # Schemat: raportuja do Artura, Artur decyduje, trudne -> do mnie
    t0 = W("m8", "oni", 278.5)
    t_rap = W("m8", "raportują", 280.0)
    t_dec = W("m8", "scope", 283.5)
    t_me = W("m8", "pisze", 288.5)
    c = comp("schemat2", t0 - 0.15, W("m8", "przekminiamy", 289.8, end=True) + 0.4, "board")
    board(c, org_html(["tymon", "kaja", "weronika"], top="artur", me=True, arrows=True))
    c.js.append('gsap.set("#org .ln",{strokeDashoffset:400});gsap.set("#on-me,#ln-me,#me-lbl",{opacity:0});')
    c.pop("#on-artur", t0, 30)
    for k, key in enumerate(["tymon", "kaja", "weronika"]):
        c.pop(f"#on-{key}", W("m8", AGENTS[key][0].lower(), 279.0) - 0.05)
    for key in ["tymon", "kaja", "weronika"]:
        c.js.append(f'tl.to("#ln-{key}",{{strokeDashoffset:0,duration:0.45,ease:"power2.out"}},{c.L(t_rap):.3f});')
    c.pop("#dec", t_dec - 0.1)
    c.js.append(f'tl.to("#on-me,#ln-me,#me-lbl",{{opacity:1,duration:0.3}},{c.L(t_me - 0.1):.3f});')
    c.js.append(f'tl.fromTo("#ln-me",{{strokeDashoffset:400}},{{strokeDashoffset:0,duration:0.45,ease:"power2.out"}},{c.L(t_me - 0.1):.3f});')

    # Voice call na zywo
    t0 = W("m8", "voice", 294.0)
    t_10 = W("m8", "10", 299.5)
    t_live = W("m8", "live", 307.5)
    c = comp("call", t0 - 0.3, W("m8", "żywo", 313.6, end=True) + 0.4)
    inner = ('<div class="call"><div class="call-av"><span class="pulse p1"></span><span class="pulse p2"></span>'
             '<img src="assets/artur_avatar.png" alt=""></div>'
             '<div class="call-n">Artur · Szef Growth</div><div class="call-s" id="cls"><span class="live-dot"></span>Rozmowa głosowa · na żywo</div>'
             '<div class="wave">' + "".join(f'<span class="wb" style="--d:{(k * 37) % 100 / 100:.2f}"></span>' for k in range(28)) + '</div>'
             f'<div class="call-cmp"><div class="cc-x" id="ccx">{icon("clock", 24)}<span>„odpowiem za 10 minut”</span></div>'
             f'<div class="cc-o" id="cco">{icon("zap", 24)}<span>zadania robione na żywo</span></div></div></div>')
    side(c, inner, "left", top=130, width=560, cid="scc")
    c.js.append(f'tl.fromTo(".p1",{{scale:1,opacity:0.6}},{{scale:1.7,opacity:0,duration:1.4,repeat:{int(c.dur / 1.4) + 1},ease:"power1.out"}},0);')
    c.js.append(f'tl.fromTo(".p2",{{scale:1,opacity:0.6}},{{scale:1.7,opacity:0,duration:1.4,repeat:{int(c.dur / 1.4) + 1},ease:"power1.out"}},0.7);')
    c.js.append(f'tl.fromTo(".wb",{{scaleY:0.25}},{{scaleY:1,duration:0.32,stagger:{{each:0.035,repeat:-1,yoyo:true}},ease:"sine.inOut"}},0);')
    c.pop("#ccx", t_10 - 0.1)
    c.js.append(f'tl.to("#ccx",{{opacity:0.45,duration:0.3}},{c.L(t_live - 0.3):.3f});')
    c.pop("#cco", t_live - 0.1)

    # Podzialy pod Weronika: grafiki / social media / montaz
    t0 = W("m8", "weronika", 356.0)
    t_g = W("m8", "grafik", 358.8)
    t_s = W("m8", "social", 360.4)
    t_m = W("m8", "montażu", 362.6)
    c = comp("poddzialy", t0 - 0.2, W("m8", "wewnętrznie", 366.5, end=True) + 0.4, "board")
    board(c, sub_html())
    c.pop("#on-weronika", t0 - 0.1, 30)
    c.js.append('gsap.set("#sub .ln",{strokeDashoffset:400});')
    for key, t in (("g", t_g), ("s", t_s), ("m", t_m)):
        c.js.append(f'tl.to("#ln-{key}",{{strokeDashoffset:0,duration:0.35,ease:"power2.out"}},{c.L(t - 0.3):.3f});')
        c.pop(f"#sn-{key}", t - 0.05)

    # 2 montazystow -> 80-90% montazu z AI
    t0 = W("m8", "wcześniej", 374.5)
    t_80 = W("m8", "80", 393.5)
    c = comp("montaz_ai", t0 - 0.1, t0 + 3.2)
    chip(c, "cm2", "film", "WCZEŚNIEJ: 2 MONTAŻYSTÓW", c.t_in, c.t_out, pos="topleft")
    c = comp("montaz_ai2", t_80 - 0.3, W("m8", "ai", 394.6, end=True) + 0.6)
    kin_words(c, "k80", [("80–90%", t_80, "o"), ("materiałów montuje AI", t_80 + 0.6, "s")], top=835, size=96)
    c.to("#k80", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # ===== ROZDZIAL 3 =====
    t0 = W("m8", "czego", 420.0)
    chapter("roz3", "03", "Czego AI (jeszcze) nie zrobi", t0 - 0.15, W("m8", "zrobi", 421.0, end=True) + 0.5)

    # 1. Nie zamknie sprzedazy
    t0 = W("m8", "nie", 440.8)
    c = comp("nie_zamknie", t0 - 0.1, W("m8", "nas", 442.1, end=True) + 0.5)
    kin_words(c, "kz", [("#1", t0 - 0.05, "s"), ("NIE ZAMKNIE", t0 + 0.1, "b"), ("SPRZEDAŻY", W("m8", "sprzedaży", 441.5), "o"),
                        ("za Ciebie", W("m8", "za", 442.0), "s")], top=835, size=96)
    c.to("#kz", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # Closing w B2B = czlowiek
    t0 = W("m8", "zastąpimy", 462.5)
    c = comp("closing", t0 - 0.1, W("m8", "długo", 467.2, end=True) + 0.6)
    chip(c, "ccl", "handshake", "CLOSING W B2B = CZŁOWIEK", c.t_in, c.t_out, pos="topleft")

    # 2. Nie zadzwoni
    t0 = W("m8", "nie", 525.0)
    c = comp("nie_zadzwoni", t0 - 0.1, W("m8", "spotkania", 532.0, end=True) + 0.6)
    kin_words(c, "kd", [("#2", t0 - 0.05, "s"), ("NIE ZADZWONI", W("m8", "zadzwoni", 526.5) - 0.1, "o")], top=835, size=104)
    t_k = W("m8", "klienta", 530.5)
    c.to("#kd", '{opacity:0,y:-14,filter:"blur(8px)"}', t_k - 1.0, 0.22)
    kin_words(c, "kd2", [("do klienta", t_k - 0.6, "s"), ("i nie umówi spotkania", W("m8", "umówi", 531.8) - 0.15, "s")], top=835, size=80)
    c.to("#kd2", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # ===== ROZDZIAL 4 =====
    t0 = W("m8", "zdradziłem", 614.8)
    c = chapter("roz4", "04", "Aplikacja i koszty", t0 - 0.4, W("m8", "nazywa", 617.0, end=True) + 1.6)
    # logo aplikacji od Jakuba (odtworzone wektorowo w assets/app_logo.svg), wchodzi na nazwie aplikacji.
    # Style inline, zeby nie zmieniac wspolnego CSS (to wymusiloby render wszystkich warstw).
    c.add('<div id="chapp" style="position:absolute;left:0;right:0;top:668px;display:flex;justify-content:center;'
          'align-items:center;gap:32px"><img src="assets/app_logo.svg" alt="" style="width:156px;height:156px;'
          'border-radius:36px;box-shadow:0 0 0 2px rgba(255,255,255,.14),0 26px 60px rgba(0,0,0,.6),'
          '0 0 60px rgba(var(--accent-rgb),.28)"><span style="font-size:66px;font-weight:850;letter-spacing:-0.02em">'
          'Grok Bot</span></div>')
    c.pop("#chapp", W("m8", "grogbot", 616.0) - 0.08, 24)

    # Plan 100 $
    t0 = W("m8", "planie", 676.0)
    t100 = W("m8", "100", 682.0)
    c = comp("plan100", t0 - 0.1, W("m8", "dolarów", 683.3, end=True) + 0.5)
    inner = ('<div class="cd-k">NASZ PLAN</div><div class="pr"><span class="pr-v" id="prv">100 $</span></div>'
             '<div class="pr-s">plan, na którym lecimy</div>')
    side(c, inner, "right", top=200, width=480)
    c.fromto("#prv", '{opacity:0,scale:1.5,filter:"blur(14px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t100 - 0.05, 0.3)

    # 24 agentow
    t0 = W("m8", "24", 708.0)
    c = comp("24", t0 - 0.1, W("m8", "fizyczną", 711.5, end=True) + 0.3)
    kin_words(c, "k24", [("24", t0, "o"), ("AGENTÓW", t0 + 0.35, "b"), ("każdy zastępuje osobę", W("m8", "każdy", 709.5), "s")],
              top=835, size=100)
    c.to("#k24", '{opacity:0,y:-14,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # Koszty: wtedy vs dzis (plansza) przy "mamy wykupionych pare tych subskrypcji"
    t0 = W("m8", "mamy", 719.0)
    c = comp("koszty", t0 - 0.2, W("m8", "subskrypcji", 720.4, end=True) + 2.2, "board")
    inner = ('<div class="cost">'
             '<div class="cost-c" id="co0"><div class="cost-l">POCZĄTEK ROKU</div><div class="cost-v">~30 000 zł</div>'
             '<div class="cost-s">marketing, sprzedaż, promocja</div></div>'
             f'<div class="cost-a" id="coa">{icon("up", 46)}</div>'
             '<div class="cost-c o" id="co1"><div class="cost-l">DZIŚ</div><div class="cost-v">kilka × 100 $</div>'
             '<div class="cost-s">parę subskrypcji · 24 agentów</div></div></div>')
    board(c, inner)
    c.pop("#co0", t0 - 0.1)
    c.fromto("#coa", "{opacity:0,rotation:-90}", "{opacity:1,rotation:90}", t0 + 0.5, 0.3)
    c.pop("#co1", W("m8", "parę", 719.8) - 0.1)

    # Na start: 30 $
    t0 = W("m8", "30", 728.8)
    c = comp("start30", t0 - 0.6, W("m8", "stworzyć", 731.0, end=True) + 1.0)
    inner = ('<div class="cd-k">NA START WYSTARCZY</div><div class="pr"><span class="pr-v o" id="p30">30 $</span></div>'
             '<div class="pr-s">żeby zbudować własny dział growth</div>')
    side(c, inner, "right", top=200, width=500)
    c.fromto("#p30", '{opacity:0,scale:1.5,filter:"blur(14px)"}', '{opacity:1,scale:1,filter:"blur(0px)"}', t0 - 0.05, 0.3)

    # ===== ZAKONCZENIE =====
    t_fb = W("m8", "feedback", 755.0)
    t_l = W("m8", "lajka", 758.0)
    t_s = W("m8", "subskrypcja", 759.5)
    c = comp("cta", t_fb - 0.25, W("m8", "subskrypcja", 759.5, end=True) + 1.6)
    c.add('<div class="cta" id="cta">'
          f'<div class="cta-b" id="cb0">{icon("msg", 30)}<span>Feedback w komentarzu</span></div>'
          f'<div class="cta-b" id="cb1">{icon("thumb", 30)}<span>Łapka w górę</span></div>'
          f'<div class="cta-b o" id="cb2">{icon("bell", 30)}<span>Subskrybuj</span></div></div>')
    for k, t in enumerate((t_fb, t_l, t_s)):
        c.pop(f"#cb{k}", t - 0.08)
    c.to("#cta", '{opacity:0,y:20,filter:"blur(8px)"}', c.t_out - 0.25, 0.22)

    # Nina i Iga
    t_n = W("m8", "nina", 785.0)
    t_i = W("m8", "igi", 795.0)
    c = comp("nina_iga", t_n - 0.3, W("m8", "nie", 800.6, end=True) + 0.3)
    inner = ('<div class="cd-k">INNE AGENTY W FIRMIE</div>'
             f'<div class="ni" id="ni0"><span class="tile sm">{icon("search", 24)}</span><div><b>Nina</b><span>research i scouting nowinek AI</span></div></div>'
             f'<div class="ni" id="ni1"><span class="tile sm">{icon("sparkles", 24)}</span><div><b>Iga</b><span>szefowa innowacji, decyduje o zmianach</span></div></div>')
    side(c, inner, "left", top=200, width=600)
    c.pop("#ni0", t_n - 0.05)
    c.pop("#ni1", t_i - 0.05)

    # Nastepny odcinek
    t0 = W("m8", "następny", 811.4)
    c = comp("nastepny", t0 - 0.1, W("m8", "działowi", 813.6, end=True) + 1.6)
    chip(c, "cnx", "film", "NASTĘPNY ODCINEK: <span class='o'>KOLEJNY DZIAŁ FIRMY</span>", c.t_in, c.t_out, pos="topleft")

    # Belka z imieniem na koncu
    t0 = W("m8", "jakub", 821.5)
    c = comp("belka_koniec", t0 - 0.3, W("m8", "biznesie", 827.5, end=True) + 0.8)
    c.add('<div class="lower" id="lw2"><span class="lw-bar"></span><div><div class="lw-n">Jakub Derda</div>'
          '<div class="lw-s">AI w biznesie dla małych i średnich firm</div></div></div>')
    c.blur_in("#lw2", c.t_in, x=-40)
    c.blur_out("#lw2", c.t_out - 0.3, x=-30)

    # Plansza koncowa (pod ekran koncowy YouTube)
    t0 = W("m8", "razu", 839.5, end=True)
    c = comp("koniec", t0 + 0.35, TOTAL, "board")
    inner = ('<div class="end-t" id="et">Dzięki za dzisiaj!</div><div class="end-s" id="es">Do następnego razu</div>'
             '<div class="end-n" id="en">Jakub Derda</div>')
    board(c, inner, leak_out=False, fade_out=False)
    c.pop("#et", c.t_in + 0.2, 30)
    c.blur_in("#es", c.t_in + 0.4, y=14)
    c.blur_in("#en", c.t_in + 0.6, y=14)


def org_html(children, top="artur", dim=(), me=False, arrows=False):
    """Schemat: agent na gorze, pod nim dzieci; opcjonalnie wezel "Jakub" nad szefem.
    Linie zaczynaja sie POD podpisem szefa i koncza nad awatarami dzieci (nie przecinaja tekstu)."""
    if me:
        y_me, y_top, s_top, y_ch, s_ch = 110, 370, 150, 705, 120
    else:
        y_top, s_top, y_ch, s_ch = 250, 170, 665, 140
    xs = {1: [960], 2: [700, 1220], 3: [520, 960, 1400]}[len(children)]
    y0 = y_top + s_top // 2 + 110          # pod imieniem i rola szefa
    y1 = y_ch - s_ch // 2 - 12             # nad awatarem dziecka
    svg = '<svg class="org-svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
    for key, x in zip(children, xs):
        svg += (f'<path id="ln-{key}" class="ln{" dim" if key in dim else ""}" '
                f'd="M960 {y0} C960 {(y0 + y1) // 2} {x} {(y0 + y1) // 2} {x} {y1}" stroke-dasharray="400"/>')
    if me:
        svg += f'<path id="ln-me" class="ln me" d="M960 {y_me + 120} L960 {y_top - s_top // 2 - 12}" stroke-dasharray="400"/>'
    svg += "</svg>"
    nodes = node_html(top, 960, y_top, size=s_top, big=True)
    for key, x in zip(children, xs):
        nodes += node_html(key, x, y_ch, size=s_ch, dim=key in dim)
    extra = ""
    if me:
        extra += (f'<div class="on me" id="on-me" style="left:{960 - 90}px;top:{y_me - 55}px"><span class="me-av">JD</span>'
                  '<div class="on-n">Jakub</div></div>'
                  f'<div class="me-lbl" id="me-lbl" style="left:990px;top:{y_me + 128}px">trudniejsze decyzje → pisze do mnie</div>')
        extra += (f'<div class="dec" id="dec" style="left:1150px;top:{y_top - 40}px">{icon("check", 22, "okic")}'
                  'decyzje w swoim zakresie<br><span>bez mojego udziału</span></div>')
    return f'<div id="org">{svg}{nodes}{extra}</div>'


def node_html(key, x, y, size=140, big=False, dim=False):
    name, role, src, _ = AGENTS[key]
    return (f'<div class="on{" big" if big else ""}{" dim" if dim else ""}" id="on-{key}" style="left:{x - 160}px;top:{y - size // 2}px">'
            f'<span class="on-av" style="width:{size}px;height:{size}px"><img src="{src}" alt=""></span>'
            f'<div class="on-n">{esc(name)}</div><div class="on-r">{esc(role)}</div></div>')


def sub_html():
    xs = [560, 960, 1360]
    svg = '<svg class="org-svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
    for key, x in zip("gsm", xs):
        svg += f'<path id="ln-{key}" class="ln" d="M960 470 C960 530 {x} 530 {x} 585" stroke-dasharray="400"/>'
    svg += "</svg>"
    nodes = node_html("weronika", 960, 235, size=160, big=True)
    for key, x, ic, lbl in zip("gsm", xs, ("image", "share", "film"), ("Grafiki", "Social media", "Montaż")):
        nodes += (f'<div class="sn" id="sn-{key}" style="left:{x - 150}px;top:600px"><span class="tile">{icon(ic, 40)}</span>'
                  f'<div class="sn-l">{lbl}</div><div class="sn-s">nowy agent</div></div>')
    return f'<div id="sub">{svg}{nodes}<div class="org-cap" style="top:830px">kolejne agenty pod Weroniką, gdy aplikacja się rozwinie</div></div>'


TEMPLATE = r"""<!doctype html>
<html lang="pl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      :root { --ground: #0f1012; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --on-accent: {{ON_ACCENT}};
        --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #8a8d94;
        --font-ui: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: transparent; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: "Inter Tight", sans-serif; color: var(--ink); }
      .o { color: var(--accent); }
      .ic { display: block; flex: none; }

      /* plansze */
      .board { position: absolute; inset: 0; overflow: hidden; }
      .pbg { position: absolute; inset: 0; background: radial-gradient(90% 80% at 50% 25%, #222327 0%, #141518 50%, var(--ground) 100%); }
      .sq { position: absolute; border-radius: 34px; }
      .sq1 { width: 300px; height: 300px; left: 1620px; top: 820px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 80px rgba(var(--accent-rgb),.35); }
      .sq2 { width: 170px; height: 170px; left: -40px; top: 760px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 60px rgba(var(--accent-rgb),.3); }
      .sq3 { width: 300px; height: 300px; left: 1500px; top: -130px; border: 5px solid rgba(var(--accent-rgb),.8); }
      .leak { position: absolute; inset: -10%; z-index: 40; pointer-events: none; mix-blend-mode: screen; opacity: 0;
        background: radial-gradient(45% 35% at 30% 45%, rgba(var(--accent-rgb),.6), rgba(var(--accent-rgb),0) 70%),
                    radial-gradient(40% 30% at 70% 60%, rgba(255,255,255,.5), rgba(255,255,255,0) 70%),
                    radial-gradient(60% 50% at 50% 50%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%); }

      /* rozdzialy */
      .ch-num { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 150px; font-weight: 900; letter-spacing: -0.04em;
        background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 75%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .ch-title { position: absolute; left: 0; right: 0; top: 520px; text-align: center; font-size: 86px; font-weight: 800; letter-spacing: -0.02em; }
      .ch-sub { position: absolute; left: 0; right: 0; top: 640px; text-align: center; font-size: 34px; font-weight: 600; color: #b9bcc3; letter-spacing: .02em; }
      .ch-app { position: absolute; left: 50%; transform: translateX(-50%); top: 720px; display: flex; align-items: center; gap: 14px;
        padding: 16px 34px; border-radius: 100px; font-size: 44px; font-weight: 800; background: rgba(var(--accent-rgb),.16);
        border: 2px solid rgba(var(--accent-rgb),.75); box-shadow: 0 0 40px rgba(var(--accent-rgb),.3); }
      .ch-app .ic { color: var(--accent); }

      /* karty boczne */
      .card { position: absolute; padding: 30px 32px; border-radius: 30px; background: rgba(15,16,18,.86); border: 1.5px solid rgba(255,255,255,.10);
        box-shadow: 0 30px 80px rgba(0,0,0,.40); backdrop-filter: blur(6px); }
      .cd-k { font-size: 25px; font-weight: 800; letter-spacing: .14em; color: var(--accent); }
      .cd-h { font-size: 40px; font-weight: 800; line-height: 1.12; margin-top: 12px; letter-spacing: -0.01em; }
      .tags { display: flex; gap: 12px; margin-top: 22px; }
      .tag { display: inline-flex; align-items: center; gap: 10px; padding: 12px 20px; border-radius: 100px; font-size: 28px; font-weight: 750;
        background: rgba(var(--accent-rgb),.16); border: 1.5px solid rgba(var(--accent-rgb),.65); }
      .tag .ic { color: var(--accent); }
      .tile { width: 64px; height: 64px; border-radius: 18px; display: grid; place-items: center; color: var(--on-accent); flex: none;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 30px rgba(var(--accent-rgb),.4), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.sm { width: 48px; height: 48px; border-radius: 14px; }
      .rws { display: flex; flex-direction: column; gap: 14px; margin-top: 22px; }
      .rw { display: flex; align-items: center; gap: 18px; font-size: 29px; font-weight: 750; }
      .rw .tile { width: 54px; height: 54px; border-radius: 15px; }

      /* profil agenta (odtworzony ekran aplikacji) */
      .pf { font-family: var(--font-ui); background: #131313; border-radius: 24px; padding: 26px 20px 20px; text-align: center; border: 1px solid #222; }
      .pf-av { width: 128px; height: 128px; border-radius: 50%; overflow: hidden; margin: 0 auto; box-shadow: 0 0 0 4px #1b1b1b, 0 0 30px rgba(var(--accent-rgb),.25); }
      .pf-av img, .av img, .on-av img, .ag-av img { width: 104%; height: 104%; margin: -2%; object-fit: cover; display: block; }
      .pf-name { font-size: 31px; font-weight: 600; margin-top: 16px; color: #f2f2f2; }
      .pf-shared { display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 8px; font-size: 23px; color: #9a9a9a; white-space: nowrap; }
      .pf-tabs { display: flex; justify-content: center; gap: 6px; margin-top: 16px; font-size: 24px; color: #a3a3a3; }
      .pf-tab { padding: 8px 18px; border-radius: 100px; }
      .pf-tab.act { background: #262626; color: #f2f2f2; }
      .pf-badge { position: absolute; right: 30px; top: 30px; display: flex; align-items: center; gap: 8px; font-size: 24px; font-weight: 800; letter-spacing: .06em;
        padding: 10px 18px; border-radius: 100px; color: var(--on-accent); background: linear-gradient(180deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 30px rgba(var(--accent-rgb),.5); }

      /* porownanie zespolu */
      .cmp { display: flex; align-items: center; gap: 18px; margin-top: 14px; }
      .cmp-c { flex: 1; padding: 16px 18px; border-radius: 20px; background: #1b1c20; border: 1.5px solid #2b2d32; }
      .cmp-c.o { background: rgba(var(--accent-rgb),.14); border-color: rgba(var(--accent-rgb),.7); }
      .cmp-l { font-size: 22px; font-weight: 800; letter-spacing: .12em; color: var(--muted); }
      .cmp-c.o .cmp-l { color: var(--accent-hi); }
      .cmp-v { font-size: 64px; font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }
      .cmp-u { font-size: 24px; color: #b9bcc3; font-weight: 600; }
      .cmp-arr { color: var(--accent); }
      .bars2 { display: flex; flex-direction: column; gap: 14px; margin-top: 14px; }
      .b2 { display: flex; align-items: center; gap: 14px; }
      .b2l { width: 120px; font-size: 25px; font-weight: 700; color: #b9bcc3; }
      .b2l.o { color: var(--accent-hi); }
      .b2t { flex: 1; height: 26px; border-radius: 100px; background: #24262b; overflow: hidden; }
      .b2f { height: 100%; border-radius: 100px; transform-origin: left center; }
      .b2f.g { width: 40%; background: linear-gradient(90deg, #6b6f77, #b3b7bf); }
      .b2f.o { width: 100%; background: linear-gradient(90deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 24px rgba(var(--accent-rgb),.6); }
      .b2x { font-size: 30px; font-weight: 900; color: var(--accent); }

      /* duze liczby na planszy */
      .big2 { position: absolute; left: 0; right: 0; top: 330px; display: flex; justify-content: center; gap: 120px; }
      .bg2 { text-align: center; }
      .bg2-v { font-size: 230px; font-weight: 900; letter-spacing: -0.05em; line-height: 1; }
      .bg2-v.o { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 75%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .bg2-l { font-size: 40px; font-weight: 800; letter-spacing: .16em; margin-top: 16px; }
      .k30-l { position: absolute; left: 0; right: 0; top: 330px; text-align: center; font-size: 36px; font-weight: 800; letter-spacing: .2em; color: var(--accent); }
      .k30 { position: absolute; left: 0; right: 0; top: 400px; text-align: center; font-size: 200px; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
      .k30-s { position: absolute; left: 0; right: 0; top: 640px; text-align: center; font-size: 40px; font-weight: 600; color: #c9ccd3; }

      /* plan odcinka */
      .plan { display: flex; flex-direction: column; gap: 16px; margin-top: 18px; }
      .pl { display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 750; white-space: nowrap; }
      .pl-n { width: 46px; font-size: 26px; font-weight: 900; color: #5d6068; }

      /* odhaczenia */
      .chk { display: flex; flex-direction: column; gap: 16px; margin-top: 18px; }
      .ck { display: flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 750; white-space: nowrap; }
      .dot { width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; color: #0f1012; background: var(--ok);
        box-shadow: 0 0 24px rgba(var(--ok-rgb),.45); flex: none; }

      /* lista agentow (odtworzony ekran) */
      .ag { position: absolute; left: 50%; margin-left: -470px; top: 170px; width: 940px; font-family: var(--font-ui); background: #131313; border-radius: 34px;
        padding: 28px 22px 22px; border: 1px solid #262626; box-shadow: 0 40px 120px rgba(0,0,0,.6); }
      .ag-h { font-size: 30px; color: #a6a6a6; padding: 0 16px 14px; }
      .ag-r { display: flex; align-items: center; gap: 22px; padding: 18px 16px; border-radius: 22px; }
      .ag-r.sel { background: #222222; }
      .ag-av { width: 92px; height: 92px; border-radius: 50%; overflow: hidden; flex: none; }
      .ag-t { min-width: 0; flex: 1; }
      .ag-n { font-size: 34px; font-weight: 600; color: #f1f1f1; display: flex; align-items: center; gap: 12px; }
      .ag-n .ppl { color: #9a9a9a; }
      .ag-p { font-size: 27px; color: #9a9a9a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 4px; }
      .priv { filter: blur(7px); }
      .ag-cap { position: absolute; left: 0; right: 0; top: 905px; text-align: center; font-size: 34px; font-weight: 800; letter-spacing: .14em; color: var(--accent); }

      /* schemat */
      .org-svg { position: absolute; left: 0; top: 0; }
      .ln { fill: none; stroke: var(--accent); stroke-width: 4; stroke-linecap: round; filter: drop-shadow(0 0 8px rgba(var(--accent-rgb),.6)); }
      .ln.dim { stroke: #3a3c42; filter: none; }
      .ln.me { stroke: #ffffff; filter: drop-shadow(0 0 8px rgba(255,255,255,.4)); }
      .on { position: absolute; width: 320px; text-align: center; }
      .on-av { display: block; margin: 0 auto; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 5px var(--accent), 0 0 40px rgba(var(--accent-rgb),.45); }
      .on.dim { opacity: .35; }
      .on.dim .on-av { box-shadow: 0 0 0 4px #3a3c42; }
      .on-n { font-size: 36px; font-weight: 800; margin-top: 16px; }
      .on-r { font-size: 27px; font-weight: 600; color: #b9bcc3; margin-top: 2px; }
      .on.big .on-n { font-size: 42px; }
      .me-av { display: grid; place-items: center; width: 110px; height: 110px; margin: 0 auto; border-radius: 50%; background: #f2f2f2; color: #0f1012;
        font-size: 40px; font-weight: 900; box-shadow: 0 0 0 5px #fff, 0 0 40px rgba(255,255,255,.35); }
      .on.me { width: 180px; }
      .me-lbl { position: absolute; font-size: 26px; font-weight: 700; color: #e9e9e9; }
      .dec { position: absolute; font-size: 26px; font-weight: 750; line-height: 1.25; padding: 14px 20px; border-radius: 18px; background: rgba(var(--ok-rgb),.12);
        border: 1.5px solid rgba(var(--ok-rgb),.55); display: flex; gap: 12px; align-items: flex-start; }
      .dec span { color: #a9e7c3; font-weight: 600; font-size: 26px; }
      .okic { color: var(--ok); margin-top: 3px; }
      .org-cap { position: absolute; left: 0; right: 0; text-align: center; font-size: 30px; font-weight: 800; letter-spacing: .12em; color: var(--accent); }
      .sn { position: absolute; width: 300px; text-align: center; }
      .sn .tile { width: 96px; height: 96px; border-radius: 26px; margin: 0 auto; }
      .sn-l { font-size: 36px; font-weight: 800; margin-top: 16px; }
      .sn-s { font-size: 26px; color: #b9bcc3; margin-top: 2px; }

      /* chipy */
      .chipwrap { position: absolute; display: flex; }
      .chip2 { display: flex; align-items: center; gap: 16px; padding: 12px 28px 12px 12px; border-radius: 100px; background: rgba(15,16,18,.86);
        border: 1.5px solid rgba(255,255,255,.14); font-size: 28px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .okpart { display: flex; align-items: center; padding-left: 14px; border-left: 1.5px solid rgba(255,255,255,.16); }

      /* tekst kinetyczny */
      .kin { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: baseline; flex-wrap: wrap; gap: 0 0.28em;
        text-align: center; padding: 0 160px; line-height: 1.05; }
      .kw { display: inline-block; font-weight: 850; letter-spacing: -0.03em;
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 16px rgba(0,0,0,.6)) drop-shadow(0 0 24px rgba(255,255,255,.12)); }
      .kw.s { font-size: 0.5em; font-weight: 700; letter-spacing: -0.01em; }
      .kw.o { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 16px rgba(0,0,0,.5)) drop-shadow(0 0 30px rgba(var(--accent-rgb),.35)); }
      .kw.arrow { color: var(--accent); background: none; -webkit-background-clip: border-box; }

      /* belka z imieniem */
      .lower { position: absolute; left: 80px; bottom: 205px; display: flex; align-items: center; gap: 20px; padding: 18px 34px 18px 22px; border-radius: 22px;
        background: rgba(15,16,18,.88); border: 1.5px solid rgba(255,255,255,.10); box-shadow: 0 20px 60px rgba(0,0,0,.4); }
      .lw-bar { width: 8px; height: 66px; border-radius: 4px; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 20px rgba(var(--accent-rgb),.6); }
      .lw-n { font-size: 40px; font-weight: 850; letter-spacing: -0.01em; }
      .lw-s { font-size: 27px; font-weight: 600; color: #b9bcc3; margin-top: 2px; }

      /* etat, ceny */
      .q4 { display: flex; align-items: center; gap: 22px; margin-top: 10px; }
      .q4-v { font-size: 150px; font-weight: 900; line-height: 1; color: var(--accent); filter: drop-shadow(0 0 30px rgba(var(--accent-rgb),.4)); }
      .q4-l { font-size: 48px; font-weight: 850; }
      .q4-s { font-size: 27px; color: #b9bcc3; font-weight: 600; }
      .hrs { display: flex; align-items: center; gap: 14px; margin-top: 18px; padding: 14px 18px; border-radius: 18px; background: #1b1c20; border: 1.5px solid #2b2d32; font-size: 28px; }
      .hrs .ic { color: var(--accent); }
      .hrs-s { margin-left: auto; font-size: 25px; color: var(--muted); font-weight: 600; }
      .pr { display: flex; align-items: baseline; gap: 12px; margin-top: 8px; }
      .pr-v { font-size: 120px; font-weight: 900; letter-spacing: -0.04em; line-height: 1.05; }
      .pr-v.o { color: var(--accent); filter: drop-shadow(0 0 30px rgba(var(--accent-rgb),.4)); }
      .pr-u { font-size: 34px; font-weight: 700; color: #b9bcc3; }
      .pr-s { font-size: 26px; color: #c9ccd3; font-weight: 600; }

      /* sekwencje */
      .seq { display: flex; flex-direction: column; gap: 12px; margin-top: 16px; }
      .sq-i { display: flex; align-items: center; gap: 16px; font-size: 30px; font-weight: 750; padding: 10px 14px; border-radius: 18px; background: #1b1c20; border: 1.5px solid #2b2d32; }
      .seq-f { display: flex; align-items: center; gap: 10px; margin-top: 16px; font-size: 26px; color: var(--accent-hi); font-weight: 700; }

      /* mail */
      .ml-k { position: absolute; left: 0; right: 0; top: 60px; display: flex; justify-content: center; align-items: center; gap: 12px; font-size: 30px; font-weight: 800;
        letter-spacing: .1em; color: var(--accent); text-transform: uppercase; }
      .ml { position: absolute; left: 50%; margin-left: -330px; top: 130px; width: 660px; height: 900px; border-radius: 28px; overflow: hidden; background: #fff;
        box-shadow: 0 40px 120px rgba(0,0,0,.6), 0 0 0 1.5px rgba(255,255,255,.12); }
      .ml-top { height: 64px; background: #f3f3f5; display: flex; align-items: center; gap: 10px; padding: 0 22px; border-bottom: 1px solid #e3e3e6; }
      .ml-dot { width: 14px; height: 14px; border-radius: 50%; background: #d9d9de; }
      .ml-subj { margin-left: 14px; font-family: var(--font-ui); font-size: 22px; font-weight: 600; color: #222; }
      .ml-vp { position: absolute; left: 0; right: 0; top: 64px; bottom: 0; overflow: hidden; }
      .ml-vp img { width: 660px; display: block; }

      /* rozmowa */
      .call { text-align: center; }
      .call-av { position: relative; width: 150px; height: 150px; margin: 6px auto 0; }
      .call-av img { position: relative; width: 150px; height: 150px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 0 4px var(--accent); }
      .pulse { position: absolute; inset: 0; border-radius: 50%; border: 3px solid var(--accent); }
      .call-n { font-size: 32px; font-weight: 800; margin-top: 20px; }
      .call-s { display: flex; justify-content: center; align-items: center; gap: 10px; font-size: 25px; color: #b9bcc3; font-weight: 650; margin-top: 4px; }
      .live-dot { width: 12px; height: 12px; border-radius: 50%; background: #ff3b30; box-shadow: 0 0 12px rgba(255,59,48,.8); }
      .wave { display: flex; justify-content: center; align-items: center; gap: 6px; height: 70px; margin-top: 18px; }
      .wb { width: 7px; height: 60px; border-radius: 4px; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); transform-origin: center; }
      .call-cmp { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; text-align: left; }
      .cc-x, .cc-o { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 16px; font-size: 26px; font-weight: 700; }
      .cc-x { background: #1b1c20; border: 1.5px solid #2b2d32; color: #b9bcc3; }
      .cc-o { background: rgba(var(--ok-rgb),.12); border: 1.5px solid rgba(var(--ok-rgb),.55); }
      .cc-o .ic { color: var(--ok); }

      /* koszty */
      .cost { position: absolute; left: 0; right: 0; top: 300px; display: flex; justify-content: center; align-items: center; gap: 50px; }
      .cost-c { width: 620px; padding: 40px 44px; border-radius: 34px; background: #1b1c20; border: 1.5px solid #2b2d32; }
      .cost-c.o { background: rgba(var(--accent-rgb),.14); border-color: rgba(var(--accent-rgb),.8); box-shadow: 0 0 60px rgba(var(--accent-rgb),.25); }
      .cost-l { font-size: 26px; font-weight: 800; letter-spacing: .16em; color: var(--muted); }
      .cost-c.o .cost-l { color: var(--accent-hi); }
      .cost-v { font-size: 92px; font-weight: 900; letter-spacing: -0.03em; margin-top: 10px; white-space: nowrap; }
      .cost-c.o .cost-v { color: var(--accent); }
      .cost-s { font-size: 28px; color: #c9ccd3; font-weight: 600; margin-top: 6px; }
      .cost-a { color: var(--accent); }

      /* CTA */
      .cta { position: absolute; left: 0; right: 0; bottom: 90px; display: flex; justify-content: center; gap: 22px; }
      .cta-b { display: flex; align-items: center; gap: 14px; padding: 18px 30px; border-radius: 100px; font-size: 32px; font-weight: 800;
        background: rgba(15,16,18,.9); border: 1.5px solid rgba(255,255,255,.16); box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .cta-b .ic { color: var(--accent); }
      .cta-b.o { color: var(--on-accent); background: linear-gradient(180deg, var(--accent-hi), var(--accent)); border-color: transparent; box-shadow: 0 0 40px rgba(var(--accent-rgb),.5); }
      .cta-b.o .ic { color: var(--on-accent); }

      /* Nina, Iga */
      .ni { display: flex; align-items: center; gap: 16px; margin-top: 16px; }
      .ni b { display: block; font-size: 34px; font-weight: 850; }
      .ni span { font-size: 27px; color: #b9bcc3; font-weight: 600; }

      /* koniec */
      .end-t { position: absolute; left: 0; right: 0; top: 150px; text-align: center; font-size: 110px; font-weight: 900; letter-spacing: -0.03em; }
      .end-s { position: absolute; left: 0; right: 0; top: 290px; text-align: center; font-size: 44px; font-weight: 650; color: #c9ccd3; }
      .end-n { position: absolute; left: 0; right: 0; top: 900px; text-align: center; font-size: 34px; font-weight: 800; letter-spacing: .2em; color: var(--accent); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{DUR}}" data-width="1920" data-height="1080">
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


def main():
    build()
    COMPS.sort(key=lambda c: c.t_in)
    manifest = []
    for k, c in enumerate(COMPS):
        if c.dur <= 0.2:
            raise SystemExit(f"Za krotka grafika: {c.name} {c.t_in}-{c.t_out}")
        fn = f"o_{k:02d}_{c.name}.html"
        manifest.append({"plik": fn, "nazwa": c.name, "start": c.t_in, "dlugosc": c.dur, "rodzaj": c.kind})
        if "--lista" not in sys.argv:
            (HF / fn).write_text(c.html())
        print(f"{k:2d} {c.t_in:7.2f}-{c.t_out:7.2f} ({c.dur:5.2f}s) {c.kind:7s} {c.name}")
    if "--lista" not in sys.argv:
        for old in HF.glob("o_*.html"):
            if old.name not in {m["plik"] for m in manifest}:
                old.unlink()
        (HF / "grafiki.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    tot = sum(m["dlugosc"] for m in manifest)
    print(f"{len(manifest)} grafik, lacznie {tot:.1f} s")


if __name__ == "__main__":
    main()

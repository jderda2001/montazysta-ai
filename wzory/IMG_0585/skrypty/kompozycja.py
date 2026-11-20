#!/usr/bin/env python3
"""Generuje ../<HOOK>/hf/index.html (HyperFrames) dla reklamy adGen "Służebność przesyłu" (IMG_0585):
hook kinetyczny (A / B / C), napisy slowo po slowie, grafiki w palecie adGen (pomarancz), przycisk CTA,
plansza koncowa bez logo. Dodatkowo ../<HOOK>/napisy.srt.

Uzycie: HOOK=A python3 -I kompozycja.py   (potem B, C)
"""
import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = os.environ.get("HOOK", "A")
P = ROOT / HOOK  # folder wersji: A/, B/, C/
# Glos: naturalny dzwiek z mikrofonu po lekkim masteringu z aroll.py (highpass 70 Hz, kompresja 2,5:1, -14 LUFS).
# Jakub, 17.11.2026 (po IMG_0576): "za bardzo uzywasz voice enhancer AI... bez tego, albo z duzo mniejszym filtrem".
# Wariant C (Sidon + lancuch radiowy) lezy w audio/aroll_studio_gleboki.wav - tylko na jego prosbe.
# Wideo A-rollu idzie bez dzwieku, glos jako osobna sciezka <audio>.
GLOS = P / "audio/aroll.wav"
# Dwie palety, ten sam uklad i ruch. Reklamy adGen zostaja pomaranczowe (decyzja Jakuba z 17.11.2026).
PALETY = {
    "personal": {"accent": "#00E5A0", "on_accent": "#0f1012", "ok": None},
    "adgen": {"accent": "#ff7018", "on_accent": "#ffffff", "ok": "#3ddc84"},
}
MARKA = "adgen"
# Biala koszulka wypada dokladnie pod napisami (bialy tekst na bialym). Wyglad napisow jest zamrozony, wiec
# czytelnosc daje miekkie przyciemnienie pasa wideo pod napisami (warstwa nad wideo, pod grafikami).
SCRIM = True

ICON = {
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "down": '<path d="M12 5v14"/><path d="M6 13l6 6 6-6"/>',
    "right": '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "phone-fwd": '<path d="M18 2l4 4-4 4"/><path d="M14 6h8"/><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "phone-in": '<path d="M16 2v6h6"/><path d="M22 2l-6 6"/><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "map": '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15"/><path d="M15 6v15"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "hash": '<path d="M4 9h16"/><path d="M4 15h16"/><path d="M10 3 8 21"/><path d="M16 3l-2 18"/>',
    "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M5 7h14"/><path d="M5 7 2 14a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
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
    lo = "#%02x%02x%02x" % tuple(round(c * 0.84) for c in acc)  # ciemniejszy koniec gradientu przycisku (bialy tekst)
    for key, val in (("ACCENT_RGB", ",".join(map(str, acc))), ("ACCENT_HI", hi), ("ACCENT_LO", lo), ("ACCENT", p["accent"]),
                     ("ON_ACCENT", p["on_accent"]), ("OK_RGB", ",".join(map(str, ok))), ("OK", p["ok"] or p["accent"])):
        page = page.replace("{{" + key + "}}", val)
    return page


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


# poprawki transkrypcji (whisper -> tekst napisow); porownanie i tak idzie po norm()
FIX = {"godziny": "godzin", "przyłączyć": "przełączyć", "dla": "do"}

# --- Hook: tekst (pisownia do napisow; czasy z transkrypcji, slowo po slowie w tej samej kolejnosci)
HOOK_TXT = {
    "A": "Po wyroku Trybunału Konstytucyjnego właściciele działek znowu pytają o wynagrodzenie.",
    "B": "Prowadzisz sprawy o służebność przesyłu? Możemy przełączyć właściciela działki zaraz po naszej rozmowie "
         "do Twojego handlowca. Na żywo.",
    "C": "Dzwonisz do leada o służebność przesyłu, a on kompletnie nie pamięta, że zostawiał gdziekolwiek kontakt? "
         "U nas każdy najpierw rozmawia z naszym zespołem.",
}
# bloki kinetyczne: (ile malych slow, [ile duzych slow w kolejnych liniach], ile malych po duzych, puenta akcentem)
KIN = {
    # Po wyroku | TRYBUNAŁU / KONSTYTUCYJNEGO ;  właściciele działek znowu pytają o | WYNAGRODZENIE
    "A": [(2, [1, 1], 0, False), (5, [1], 0, True)],
    # Prowadzisz sprawy o | SŁUŻEBNOŚĆ / PRZESYŁU? ;  Możemy przełączyć | WŁAŚCICIELA DZIAŁKI ;
    # zaraz po naszej rozmowie do | TWOJEGO HANDLOWCA ;  NA ŻYWO
    "B": [(3, [1, 1], 0, False), (2, [2], 0, False), (5, [2], 0, False), (0, [2], 0, True)],
    # Dzwonisz do leada o | SŁUŻEBNOŚĆ PRZESYŁU ;  a on kompletnie | NIE PAMIĘTA | że zostawiał gdziekolwiek kontakt? ;
    # U nas każdy najpierw rozmawia | Z NASZYM ZESPOŁEM
    "C": [(4, [2], 0, False), (3, [2], 4, False), (5, [3], 0, True)],
}

# Frazy napisow po hooku (korpus wspolny dla A/B/C). *slowa* = wyroznienie akcentem.
PHRASES = [
    "Dostarczamy *kancelariom*", "właścicieli działek", "ze *słupami* i służebnościami", "na gruncie,",
    "którzy chcą sprawdzić,", "czy należy im się", "*wynagrodzenie.*",
    "Nasz zespół", "za każdym razem", "najpierw *dzwoni*", "do każdego z nich,",
    "aby zapytać", "o wysokość napięcia,", "rodzaj działki,", "dokładny adres", "i numer działki,", "a także",
    "o księgę wieczystą.",
    "Dostajesz tylko tych,", "którzy *odebrali*", "i *potwierdzili,*", "że chcą rozmowy", "z prawnikiem.",
    "Każdy od razu ląduje", "w Twoim *CRM*", "z *notatką* z rozmowy.",
    "W tej niszy", "możemy też przełączyć", "rozmowę *na żywo*", "do Twojego handlowca.",
    "Dostajesz wtedy", "*nagranie* z całej rozmowy.",
    "Pierwsze leady masz", "do *24 godzin*", "od startu.",
    "Płacisz tylko i wyłącznie", "za *zapytania,*", "nie za jakiś", "budżet reklamowy", "czy godziny zespołu.",
    "Co ważne,", "każde zamówienie", "jest objęte *gwarancją.*",
    "*Zostaw kontakt* poniżej.", "Oddzwonię i powiem Ci,", "ile i do kiedy", "możemy dostarczyć Ci",
    "jaką ilość leadów", "na służebności.",
]


def load_words():
    return [[a, b, t] for a, b, t in json.loads((P / "audio/slowa.json").read_text())]


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
            got = ws[k][2]
            if norm(got) != norm(text) and norm(FIX.get(norm(got), got)) != norm(text):
                raise SystemExit(f"Niezgodnosc: '{got}' vs '{text}' we frazie '{ph}' (t={ws[k][0]:.2f})")
            cur.append([ws[k][0], ws[k][1], text, hl])
            k += 1
        phrases.append(cur)
    if k != len(ws):
        raise SystemExit(f"Nieprzypisane slowa: {[w[2] for w in ws[k:]]}")
    return phrases


def span(w, cls="w", text=None, sid=None):
    hl = " hl" if len(w) > 3 and w[3] else ""
    ident = f' id="{sid}"' if sid else ""
    return f'<span class="{cls}{hl}"{ident}>{html.escape(text if text is not None else w[2])}</span>'


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def build():
    edl = json.loads((P / "aroll/edl.json").read_text())
    total = edl[-1]["t_out"]
    words = load_words()
    n_hook = sum(1 for e in edl if e.get("hook"))

    def W(text, after=0.0):
        for a, b, t in words:
            if a >= after - 1e-6 and norm(text) in (norm(t), norm(FIX.get(norm(t), t))):
                return a, b
        raise SystemExit(f"Nie znaleziono slowa: {text} po {after}")

    seg = lambda i: edl[i]
    B = lambda k: edl[n_hook + k]  # k-ta kwestia korpusu (0..11)
    el, js, srt = [], [], []

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1});')
    for e in edl:
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')

    # --- hook kinetyczny
    kin_end = B(0)["t_in"]
    hw = [w for w in words if w[0] < kin_end - 0.02]
    toks = HOOK_TXT[HOOK].split()
    if len(hw) != len(toks):
        raise SystemExit(f"Hook {HOOK}: {len(hw)} slow w transkrypcji, {len(toks)} w tekscie: {[w[2] for w in hw]}")
    for w, t in zip(hw, toks):
        if norm(w[2]) != norm(t):
            print(f"   uwaga, hook: whisper '{w[2]}' -> napis '{t}' (t={w[0]:.2f})")
        w[2] = t
    blocks, k_i = [], 0
    for ns, lines, na, akcent in KIN[HOOK]:
        small = hw[k_i:k_i + ns]; k_i += ns
        big = []
        for n in lines:
            big.append(hw[k_i:k_i + n]); k_i += n
        after = hw[k_i:k_i + na]; k_i += na
        blocks.append((small, big, after, akcent))
    assert k_i == len(hw), (k_i, len(hw))
    first = lambda b: (b[0] or b[1][0])[0][0]
    for k, (small, big, after, akcent) in enumerate(blocks):
        start = max(0.0, first(blocks[k]) - 0.06)
        end = first(blocks[k + 1]) - 0.06 if k + 1 < len(blocks) else kin_end
        big_txt = [" ".join(w[2].upper().rstrip(".,") for w in line) for line in big]
        # wersaliki Inter Tight 800 to ok. 0,63 rozmiaru na znak; max 900 px szerokosci (przyciski Instagrama)
        size = min(132 if len(big) == 1 else 118, int(900 / (max(len(t) for t in big_txt) * 0.63)))
        sid = f"k{k}"
        parts = []
        if small:
            parts.append('<div class="kin-s">' + "".join(span(w, sid=f"{sid}s{i}") for i, w in enumerate(small)) + "</div>")
        bi = 0
        for line in big:
            parts.append(f'<div class="kin-b{" accent" if akcent else ""}" style="font-size:{size}px">'
                         + "".join(f'<span class="b" id="{sid}b{bi + i}">{html.escape(w[2].upper().rstrip(".,"))}</span>'
                                   for i, w in enumerate(line)) + "</div>")
            bi += len(line)
        if after:
            parts.append('<div class="kin-s kin-t">' + "".join(span(w, sid=f"{sid}t{i}") for i, w in enumerate(after)) + "</div>")
        el.append(f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                  f'data-track-index="3">' + "".join(parts) + "</div>")
        for i, w in enumerate(small):
            js.append(f'tl.fromTo("#{sid}s{i}",{{opacity:0,y:18,filter:"blur(8px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0] - 0.04):.3f});')
        for i, w in enumerate([w for line in big for w in line]):
            js.append(f'tl.fromTo("#{sid}b{i}",{{opacity:0,scale:1.35,filter:"blur(14px)"}},'
                      f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(start, w[0] - 0.05):.3f});')
        for i, w in enumerate(after):
            js.append(f'tl.fromTo("#{sid}t{i}",{{opacity:0,y:14,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{w[0] - 0.04:.3f});')
        srt.append((start, end, " ".join(w[2] for w in small + [w for line in big for w in line] + after)))

    # --- napisy slowo po slowie (korpus)
    last = edl[-1]
    end_card_in = round(last["speech"][1] - last["a_in"] + last["t_in"] + 0.12, 3)
    phrases = manual_group([w for w in words if w[0] >= kin_end - 0.02])
    for i, ph in enumerate(phrases):
        start = max(ph[0][0] - 0.06, kin_end if i == 0 else 0)
        nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
        end = min(nxt, ph[-1][1] + 0.6, end_card_in)
        cid = f"c{i}"
        txt = " ".join(w[2] for w in ph)
        fs = min(66, int(950 / (len(txt) * 0.54)))
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

    def panel(pid, t_in, t_out, inner, track=2, leak_in=True, leak_out=True, cls="", fade_out=True, extend=0.0):
        """extend/fade_out=False: plansza trwa dluzej pod nastepna plansza (przenikanie bez przeswitu wideo)."""
        el.append(f'<div id="{pid}" class="panel clip {cls}" data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12 + extend:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div><div class="sq sq1" data-layout-allow-overflow></div><div class="sq sq2" data-layout-allow-overflow></div><div class="sq sq3" data-layout-allow-overflow></div>{inner}</div>')
        js.append(f'tl.fromTo("#{pid}",{{opacity:0,scale:1.06,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{t_in - 0.12:.3f});')
        d = t_out - t_in
        js.append(f'tl.fromTo("#{pid} .sq1",{{rotation:-14,y:60}},{{rotation:-6,y:0,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        js.append(f'tl.fromTo("#{pid} .sq2",{{rotation:18,y:40}},{{rotation:9,y:-20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        js.append(f'tl.fromTo("#{pid} .sq3",{{rotation:8}},{{rotation:20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        if leak_in:
            leak(t_in)
        if t_out < total - 0.1 and fade_out:
            js.append(f'tl.to("#{pid}",{{opacity:0,scale:1.04,filter:"blur(14px)",duration:0.18,ease:"power2.in"}},{t_out - 0.18:.3f});')
            if leak_out:
                leak(t_out)

    def pop(sel, t, extra=""):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:26,scale:0.94{extra}}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')

    def overlay(oid, t_in, t_out, inner, cls, track=5, y_from=-30):
        el.append(f'<div id="{oid}" class="{cls} clip" data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
        js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.6:.0f},filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.22:.3f});')

    # --- G1: karta leada (korpus 0-1, na mowcy): kogo dostarczamy
    b0, b1 = B(0)["t_in"], B(1)["t_in"]
    pills = [("Słupy na gruncie", W("słupami", b0)[0]), ("Służebność", W("służebnościami", b0)[0]),
             ("Chce sprawdzić wynagrodzenie", W("sprawdzić", b1)[0])]
    inner = (f'<div class="tile nt-tile">{icon("user", 44)}</div><div class="nt-body">'
             '<div class="nt-top"><b>Lead</b><span>· dla kancelarii</span></div>'
             '<div class="nt-title">Właściciel działki</div><div class="nt-items wrap">'
             + "".join(f'<span class="nti" id="g1p{k}">{html.escape(t)}</span>' for k, (t, _) in enumerate(pills))
             + "</div></div>")
    overlay("g1", W("właścicieli", b0)[0] - 0.12, B(2)["t_in"] - 0.02, inner, "notif", y_from=-60)
    for k, (_, t) in enumerate(pills):
        pop(f"#g1p{k}", t - 0.06)

    # --- G2: chip "nasz zespol dzwoni do kazdego" (korpus 2)
    b2 = B(2)["t_in"]
    inner = (f'<div class="chip2"><span class="tile sm">{icon("phone", 30)}</span><span>NASZ ZESPÓŁ</span>'
             f'<span class="okpart" id="g2ok"><span class="dot sm">{icon("check", 22)}</span>DZWONI DO KAŻDEGO</span></div>')
    overlay("g2", W("zespół", b2)[0] - 0.1, B(3)["t_in"] - 0.02, inner, "chipwrap")
    js.append(f'tl.fromTo("#g2ok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{W("dzwoni", b2)[0] - 0.05:.3f});')

    # --- G3: plansza - o co pytamy w rozmowie (korpus 3)
    b3 = B(3)["t_in"]
    rows = [("zap", "WYSOKOŚĆ NAPIĘCIA", W("wysokość", b3)[0]), ("map", "RODZAJ DZIAŁKI", W("rodzaj", b3)[0]),
            ("pin", "DOKŁADNY ADRES", W("dokładny", b3)[0]), ("hash", "NUMER DZIAŁKI", W("numer", b3)[0]),
            ("book", "KSIĘGA WIECZYSTA", W("księgę", b3)[0])]
    inner = '<div class="p-head" style="top:285px">O CO PYTAMY W ROZMOWIE</div><div class="list" style="top:370px;gap:26px">'
    for k, (ic, lbl, _) in enumerate(rows):
        inner += f'<div class="row" id="g3r{k}"><div class="tile">{icon(ic, 46)}</div><div class="lbl">{html.escape(lbl)}</div></div>'
    inner += "</div>"
    panel("g3", b3, B(4)["t_in"], inner)
    for k, (_, _, t) in enumerate(rows):
        pop(f"#g3r{k}", t - 0.08)

    # --- G4: kafelki - odebral / chce rozmowy z prawnikiem (korpus 4, na mowcy)
    b4 = B(4)["t_in"]
    tiles = [("phone-in", "Odebrał<br>telefon", W("odebrali", b4)[0]),
             ("scale", "Chce rozmowy<br>z prawnikiem", W("potwierdzili", b4)[0])]
    inner = "".join(f'<div class="tcard" id="g4c{k}"><div class="tile">{icon(ic, 40)}</div><div class="tlbl">{lbl}</div>'
                    f'<span class="tok">{icon("check", 24)}</span></div>' for k, (ic, lbl, _) in enumerate(tiles))
    t0 = tiles[0][2] - 0.1
    el.append(f'<div id="g4" class="tiles clip" data-start="{t0:.3f}" data-duration="{B(5)["t_in"] - t0 - 0.02:.3f}" data-track-index="5">{inner}</div>')
    for k, (_, _, t) in enumerate(tiles):
        pop(f"#g4c{k}", t - 0.08)
    js.append(f'tl.to("#g4",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{B(5)["t_in"] - 0.26:.3f});')

    # --- G5: plansza - lead laduje w CRM z notatka (korpus 5)
    b5 = B(5)["t_in"]
    inner = ('<div class="p-head" style="top:300px">TWÓJ CRM</div>'
             f'<div class="crm" id="g5crm"><div class="crm-top">{icon("kanban", 40)}<span>Nowe leady</span>'
             '<span class="crm-d">Dziś</span></div><div class="crm-col">'
             f'<div class="crm-lead" id="g5lead"><span class="pulse" id="g5p" data-layout-ignore></span><div class="tile">{icon("user", 38)}</div><div>'
             '<div class="crm-lt">Właściciel działki</div><div class="crm-ls">Służebność przesyłu</div></div></div>'
             '<div class="crm-ghost"><span class="gav"></span><i style="width:300px"></i></div>'
             '<div class="crm-ghost"><span class="gav"></span><i style="width:220px"></i></div></div></div>'
             f'<div class="inv" style="top:900px"><div class="pill ok" id="g5note">{icon("file", 30)} NOTATKA Z ROZMOWY</div></div>')
    panel("g5", b5, B(6)["t_in"], inner)
    pop("#g5crm", b5 + 0.02)
    js.append(f'tl.fromTo("#g5lead",{{opacity:0,y:-150,scale:0.92}},{{opacity:1,y:0,scale:1,duration:0.42,ease:"bounce.out"}},{W("ląduje", b5)[0] - 0.12:.3f});')
    t_p = W("ląduje", b5)[0] + 0.2  # lead juz lezy: obrys "odbija" na zewnatrz
    js.append(f'tl.set("#g5p",{{opacity:0.9,scaleX:1,scaleY:1}},{t_p:.3f});')
    js.append(f'tl.to("#g5p",{{opacity:0,scaleX:1.06,scaleY:1.3,duration:0.55,ease:"power2.out"}},{t_p:.3f});')
    pop("#g5note", W("notatką", b5)[0] - 0.06)

    # --- G6: karta "rozmowa na zywo -> Twoj handlowiec" + nagranie (korpus 6-7, na mowcy)
    b6, b7 = B(6)["t_in"], B(7)["t_in"]
    inner = (f'<div class="tile nt-tile">{icon("phone-fwd", 44)}</div><div class="nt-body">'
             '<div class="nt-top"><b>Rozmowa z właścicielem</b>'
             '<span class="live" id="g6live"><i id="g6dot"></i>NA ŻYWO</span></div>'
             f'<div class="nt-title" id="g6to"><span id="g6arr" style="display:inline-flex">{icon("right", 40)}</span>Twój handlowiec</div><div class="nt-items">'
             f'<span class="nti" id="g6rec">{icon("mic", 26)}Nagranie całej rozmowy</span></div></div>')
    t6 = W("przełączyć", b6)[0] - 0.12
    overlay("g6", t6, B(8)["t_in"] - 0.02, inner, "notif", y_from=-60)
    t_live = W("żywo", b6)[0]
    js.append(f'tl.fromTo("#g6live",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.32,ease:"back.out(2.2)"}},{t_live - 0.08:.3f});')
    js.append(f'tl.fromTo("#g6dot",{{opacity:1}},{{opacity:0.25,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:{int((B(8)["t_in"] - t_live) / 0.4)}}},{t_live + 0.2:.3f});')
    t_to = W("twojego", b6)[0] - 0.06
    pop("#g6to", t_to)
    js.append(f'tl.fromTo("#g6arr",{{x:0}},{{x:10,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:{int((B(8)["t_in"] - t_to - 0.5) / 0.4)}}},{t_to + 0.35:.3f});')
    pop("#g6rec", W("nagranie", b7)[0] - 0.06)

    # --- G7: plansza - pierwsze leady do 24 h (korpus 8)
    b8 = B(8)["t_in"]
    inner = ('<div class="p-head" style="top:430px">PIERWSZE LEADY</div>'
             '<div class="wave" id="g7w" data-layout-ignore style="left:300px;top:400px;width:480px;height:480px"></div>'
             '<div class="bignum" id="g7n"><span class="pre">do</span>24<span class="unit">h</span></div>'
             '<div class="big30s" id="g7s" style="top:800px">OD STARTU</div>')
    panel("g7", b8, B(9)["t_in"], inner)
    js.append(f'tl.fromTo("#g7n",{{opacity:0,scale:1.5,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{W("do", b8)[0] - 0.05:.3f});')
    t_n = W("do", b8)[0] + 0.12  # fala: pierscien rosnie i gasnie w 0,7 s, gdy liczba juz stoi
    js.append(f'tl.set("#g7w",{{opacity:0.85,scale:0.45}},{t_n:.3f});')
    js.append(f'tl.to("#g7w",{{opacity:0,scale:1.45,duration:0.7,ease:"power2.out"}},{t_n:.3f});')
    pop("#g7s", W("od", b8)[0] - 0.05)

    # --- G8: kafelki - za co placisz (korpus 9, na mowcy)
    b9 = B(9)["t_in"]
    tiles = [("message", "Płacisz<br>za zapytania", W("za", b9)[0], True),
             ("megaphone", "Budżet<br>reklamowy", W("budżet", b9)[0], False),
             ("clock", "Godziny<br>zespołu", W("godziny", b9)[0], False)]
    inner = "".join(f'<div class="tcard{"" if ok else " no"}" id="g8c{k}"><div class="tile">{icon(ic, 40)}</div>'
                    f'<div class="tlbl">{lbl}</div><span class="tok">{icon("check" if ok else "x", 24)}</span></div>'
                    for k, (ic, lbl, _, ok) in enumerate(tiles))
    t0 = tiles[0][2] - 0.1
    el.append(f'<div id="g8" class="tiles clip" data-start="{t0:.3f}" data-duration="{B(10)["t_in"] - t0 - 0.02:.3f}" data-track-index="5">{inner}</div>')
    for k, (_, _, t, _) in enumerate(tiles):
        pop(f"#g8c{k}", t - 0.08)
    js.append(f'tl.to("#g8",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{B(10)["t_in"] - 0.26:.3f});')

    # --- G9: chip - gwarancja (korpus 10)
    b10 = B(10)["t_in"]
    inner = (f'<div class="chip2"><span class="tile sm">{icon("shield", 32)}</span><span>KAŻDE ZAMÓWIENIE</span>'
             f'<span class="okpart" id="g9ok"><span class="dot sm">{icon("check", 22)}</span>GWARANCJA</span></div>')
    overlay("g9", W("każde", b10)[0] - 0.1, B(11)["t_in"] - 0.02, inner, "chipwrap")
    js.append(f'tl.fromTo("#g9ok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{W("gwarancją", b10)[0] - 0.05:.3f});')

    # --- CTA na mowcy: przycisk "ZOSTAW KONTAKT" (korpus 11)
    b11 = B(11)["t_in"]
    t_cta = W("zostaw", b11)[0] + 0.05
    el.append(f'<div id="cta" class="ctawrap clip" data-start="{t_cta:.3f}" data-duration="{end_card_in - t_cta:.3f}" data-track-index="5">'
              f'<div class="btn" id="ctabtn">ZOSTAW KONTAKT <span class="arr" id="ctaarr">{icon("down", 44)}</span></div></div>')
    pop("#ctabtn", t_cta)
    js.append(f'tl.fromTo("#ctaarr",{{y:-6}},{{y:6,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:{int((end_card_in - t_cta - 0.4) / 0.35)}}},{t_cta + 0.4:.3f});')

    # --- plansza koncowa (bez logo: zasada Jakuba "nigdy logo adGen")
    inner = ('<div class="p-head" id="endhead" style="top:545px">SŁUŻEBNOŚĆ PRZESYŁU</div>'
             '<div class="endbig" id="endbig">Leady dla<br>Twojej kancelarii</div>'
             f'<div class="endbtnw"><div class="btn" id="endbtn">ZOSTAW KONTAKT <span class="arr" id="endarr">{icon("down", 44)}</span></div></div>'
             '<div class="endsub" id="endsub" style="top:1035px">Oddzwonię i powiem, ile leadów i do kiedy</div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    pop("#endhead", end_card_in + 0.05)
    pop("#endbig", end_card_in + 0.15)
    js.append(f'tl.fromTo("#endbtn",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.9)"}},{end_card_in + 0.3:.3f});')
    pop("#endsub", end_card_in + 0.34)
    js.append(f'tl.fromTo("#endarr",{{y:-6}},{{y:6,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:{int((total - end_card_in - 0.8) / 0.35)}}},{end_card_in + 0.75:.3f});')

    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el)) \
        .replace("{{JS}}", "\n      ".join(js)).replace("{{SCRIM}}", '<div id="scrim" data-layout-ignore></div>' if SCRIM else "")
    page = kolory(page)
    out = P / "hf/index.html"
    out.write_text(page)
    glos = P / "hf/glos.wav"
    glos.unlink(missing_ok=True)
    os.link(GLOS, glos)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | hook {HOOK}: {len(blocks)} blokow, {len(phrases)} fraz, {len(el)} elementow, {total:.2f}s, "
          f"plansza koncowa od {end_card_in:.2f}")
    for ph in phrases:
        print(f"   {ph[0][0]:6.2f} " + " ".join(("*" + w[2] + "*") if w[3] else w[2] for w in ph))


TEMPLATE = r"""<!doctype html>
<html lang="pl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      :root { --ground: #0f1012; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --accent-lo: {{ACCENT_LO}}; --on-accent: {{ON_ACCENT}}; --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #898989; --font-display: "Inter Tight", sans-serif;
        --font-ui: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); color: var(--ink); }
      #vwrap { position: absolute; inset: 0; transform-origin: 50% 36%; }
      #aroll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }

      .kin { position: absolute; left: 0; right: 0; top: 1030px; text-align: center; z-index: 30; }
      .kin-s { font-size: 50px; font-weight: 600; letter-spacing: -0.01em; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 6px 16px; padding: 0 70px; }
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

      .cap { position: absolute; left: 60px; right: 60px; top: 1120px; text-align: center; font-size: 66px; font-weight: 650; letter-spacing: -0.015em; line-height: 1.1; z-index: 30; white-space: nowrap; }

      .panel { position: absolute; inset: 0; z-index: 10; overflow: hidden; }
      .panel.top { z-index: 35; }
      .pbg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 18%, #222327 0%, #141518 45%, var(--ground) 100%); }
      .sq { position: absolute; border-radius: 34px; }
      .sq1 { width: 300px; height: 300px; left: 640px; top: 1560px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 80px rgba(var(--accent-rgb),.35); }
      .sq2 { width: 190px; height: 190px; left: -50px; top: 1480px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 60px rgba(var(--accent-rgb),.3); }
      .sq3 { width: 330px; height: 330px; left: 250px; top: 1640px; border: 5px solid rgba(var(--accent-rgb),.85); }

      .p-head { position: absolute; left: 0; right: 0; text-align: center; color: var(--accent); font-size: 32px; font-weight: 800; letter-spacing: .14em; }
      .p1av { position: absolute; left: 50%; margin-left: -75px; top: 250px; width: 150px; height: 150px; border-radius: 50%; padding: 6px;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 50px rgba(var(--accent-rgb),.45); }
      .p1av img { width: 138px; height: 138px; border-radius: 50%; object-fit: cover; display: block; border: 4px solid #141518; }
      .list { position: absolute; left: 160px; width: 780px; display: flex; flex-direction: column; gap: 30px; }
      .row { display: flex; align-items: center; gap: 30px; }
      .tile { width: 96px; height: 96px; border-radius: 24px; display: grid; place-items: center; color: var(--on-accent); flex: none;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 40px rgba(var(--accent-rgb),.45), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.sm { width: 56px; height: 56px; border-radius: 16px; box-shadow: 0 0 24px rgba(var(--accent-rgb),.4), inset 0 1px 0 rgba(255,255,255,.35); }
      .lbl { font-size: 48px; font-weight: 800; letter-spacing: .01em; white-space: nowrap; }

      .notif { position: absolute; left: 70px; width: 940px; top: 96px; padding: 24px 28px; border-radius: 38px; display: flex; gap: 24px; align-items: flex-start; z-index: 25;
        background: rgba(24,25,28,.9); border: 1.5px solid rgba(255,255,255,.10); box-shadow: 0 24px 70px rgba(0,0,0,.35); }
      .nt-av { width: 84px; height: 84px; border-radius: 22px; object-fit: cover; flex: none; }
      .nt-body { flex: 1; }
      .nt-top { display: flex; align-items: baseline; gap: 10px; font-size: 30px; color: #a0a3aa; font-weight: 500; }
      .nt-top b { color: #fff; font-weight: 700; }
      .nt-time { margin-left: auto; font-size: 28px; }
      .nt-title { font-size: 40px; font-weight: 750; margin-top: 2px; display: flex; align-items: center; gap: 12px; }
      .nt-title .ic { color: var(--accent); }
      .nt-items { display: flex; gap: 12px; margin-top: 14px; }
      .nti { font-size: 28px; font-weight: 700; padding: 9px 20px; border-radius: 100px; background: rgba(var(--accent-rgb),.16); border: 1.5px solid rgba(var(--accent-rgb),.6); white-space: nowrap; }

      .chipwrap { position: absolute; left: 0; right: 0; top: 150px; display: flex; justify-content: center; z-index: 25; }
      .chip2 { display: flex; align-items: center; gap: 18px; padding: 14px 32px 14px 14px; border-radius: 100px; background: rgba(15,16,18,.86);
        border: 1.5px solid rgba(255,255,255,.14); font-size: 34px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .okpart { display: flex; align-items: center; gap: 12px; color: var(--ok); padding-left: 18px; border-left: 1.5px solid rgba(255,255,255,.16); }
      .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: #0f1012; background: var(--ok); box-shadow: 0 0 24px rgba(var(--ok-rgb),.45); flex: none; }
      .dot.sm { width: 40px; height: 40px; }

      .cal { position: absolute; left: 140px; width: 800px; top: 380px; border-radius: 34px; padding: 26px 30px 30px;
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

      .tiles { position: absolute; left: 0; right: 0; top: 100px; display: flex; justify-content: center; gap: 22px; z-index: 25; }
      .tcard { position: relative; width: 300px; height: 206px; border-radius: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
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

      .pcard { position: absolute; left: 90px; top: 240px; width: 900px; height: 754px; border-radius: 40px; overflow: hidden; background: #121212;
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

      .ctawrap { position: absolute; left: 0; right: 0; top: 1262px; display: flex; justify-content: center; z-index: 26; }
      .cbox { width: 900px; display: flex; align-items: center; gap: 20px; padding: 14px 14px 14px 16px; border-radius: 100px; background: rgba(15,16,18,.88);
        border: 1.5px solid rgba(255,255,255,.16); box-shadow: 0 18px 50px rgba(0,0,0,.4); }
      .cav { width: 74px; height: 74px; border-radius: 50%; background: #2a2c31; color: #b9bcc3; display: grid; place-items: center; flex: none; }
      .cin { flex: 1; position: relative; height: 74px; display: flex; align-items: center; font-size: 42px; }
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


      /* --- IMG_0585 (reklama adGen): dodatki w tym samym jezyku wizualnym */
      #scrim { position: absolute; left: 0; right: 0; top: 940px; height: 580px; z-index: 1; pointer-events: none;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.46) 30%, rgba(0,0,0,.46) 66%, rgba(0,0,0,0) 100%); }
      .notif .nt-tile { width: 84px; height: 84px; border-radius: 22px; }
      .nt-items.wrap { flex-wrap: wrap; }
      .nti { display: inline-flex; align-items: center; gap: 10px; }
      .live { margin-left: auto; display: inline-flex; align-items: center; gap: 10px; font-size: 28px; font-weight: 800; letter-spacing: .06em; color: var(--on-accent);
        padding: 5px 18px; border-radius: 100px; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 24px rgba(var(--accent-rgb),.5); white-space: nowrap; }
      .live i { width: 14px; height: 14px; border-radius: 50%; background: var(--on-accent); display: block; }
      .crm { position: absolute; left: 140px; width: 800px; top: 380px; border-radius: 34px; padding: 26px 30px 30px;
        background: linear-gradient(180deg, #1d1e22, #16171a); border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .crm-top { display: flex; align-items: center; gap: 14px; font-size: 38px; font-weight: 750; padding-bottom: 18px; border-bottom: 1.5px solid #2b2d32; }
      .crm-top .ic { color: var(--accent); }
      .crm-d { margin-left: auto; color: var(--muted); font-size: 28px; font-weight: 600; }
      .crm-col { margin-top: 22px; display: flex; flex-direction: column; gap: 16px; }
      .pulse { position: absolute; inset: -3px; border-radius: 25px; border: 3px solid var(--accent); opacity: 0; pointer-events: none; }
      .wave { position: absolute; border-radius: 50%; border: 5px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 40px rgba(var(--accent-rgb),.35); opacity: 0; pointer-events: none; }
      .crm-lead { position: relative; display: flex; align-items: center; gap: 22px; height: 122px; border-radius: 22px; padding: 0 24px;
        background: linear-gradient(140deg, rgba(var(--accent-rgb),.30), rgba(var(--accent-rgb),.16)); border: 2px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 40px rgba(var(--accent-rgb),.25); }
      .crm-lead .tile { width: 74px; height: 74px; border-radius: 20px; }
      .crm-lt { font-size: 38px; font-weight: 800; }
      .crm-ls { font-size: 28px; color: var(--accent-hi); margin-top: 4px; font-weight: 600; }
      .crm-ghost { height: 92px; border-radius: 22px; background: #202226; border: 1.5px solid #2b2d32; display: flex; align-items: center; gap: 18px; padding: 0 24px; }
      .crm-ghost i { display: block; height: 18px; border-radius: 9px; background: #34373d; }
      .crm-ghost .gav { width: 52px; height: 52px; border-radius: 14px; background: #34373d; flex: none; }
      .bignum { position: absolute; left: 0; right: 0; top: 505px; text-align: center; font-size: 270px; font-weight: 900; letter-spacing: -0.05em; line-height: 1;
        background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .bignum .pre { font-size: 84px; font-weight: 800; letter-spacing: -0.01em; color: #fff; margin-right: 26px; }
      .bignum .unit { font-size: 150px; letter-spacing: -0.02em; margin-left: 14px; }
      .tcard.no .tile { background: #2a2c31; color: #9a9da5; box-shadow: none; }
      .tcard.no .tlbl { color: #9a9da5; text-decoration: line-through; text-decoration-thickness: 3px; }
      .tcard.no .tok { background: #4a4d54; color: #e6e7ea; box-shadow: none; }
      .btn { display: inline-flex; align-items: center; gap: 14px; white-space: nowrap; font-size: 46px; font-weight: 800; letter-spacing: .04em; color: var(--on-accent);
        padding: 26px 52px; border-radius: 100px; background: linear-gradient(180deg, var(--accent), var(--accent-lo));
        box-shadow: 0 0 60px rgba(var(--accent-rgb),.55), inset 0 1px 0 rgba(255,255,255,.35); text-shadow: 0 2px 10px rgba(0,0,0,.22); }
      .btn .arr { display: grid; }
      .endbig { position: absolute; left: 0; right: 0; top: 615px; text-align: center; font-size: 88px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.08; }
      .endbtnw { position: absolute; left: 0; right: 0; top: 865px; display: flex; justify-content: center; }

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
    {{SCRIM}}
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

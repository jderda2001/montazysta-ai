#!/usr/bin/env python3
"""Generuje ../hf/index.html (HyperFrames) dla reklam adGen "Leady z OC" (IMG_0583): hook kinetyczny (A / B / C),
napisy slowo po slowie, plansze i nakladki w palecie adGen (pomarancz), przycisk CTA, plansza koncowa bez logo.
Dodatkowo ../napisy.srt (frazy napisow, do Premiere / uploadu).

Wersje wybiera nazwa folderu roboczego (IMG_0583/A, B, C), tak jak w aroll.py.

Uzycie: python3 -I kompozycja.py
"""
import html
import json
import os
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
HOOK = P.name if P.name in ("A", "B", "C") else "A"
# Glos: naturalny, z mikrofonu, po lekkim masteringu z aroll.py (zasada z 17.11.2026: bez Sidona, chyba ze Jakub
# poprosi o wariant C - wtedy audio/aroll_studio_gleboki.wav ze studio.py). Wideo A-rollu idzie bez dzwieku.
GLOS = P / "audio/aroll.wav"
# Dwie palety, ten sam uklad i ruch. Reklamy adGen zostaja pomaranczowe (decyzja Jakuba z 17.11.2026).
PALETY = {
    "personal": {"accent": "#00E5A0", "on_accent": "#0f1012", "ok": None},
    "adgen": {"accent": "#ff7018", "on_accent": "#ffffff", "ok": "#3ddc84"},
}
MARKA = "adgen"
# Biala koszulka pod biala czcionka: delikatne przyciemnienie A-rollu w pasie napisow (0 = wylaczone).
# Samych napisow nie zmienia (ich wyglad jest zamrozony), lezy pod nimi i pod planszami.
SCRIM = 0.44

ICON = {
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "phonecall": '<path d="M15.05 5A5 5 0 0 1 19 8.95"/><path d="M15.05 1A9 9 0 0 1 23 8.94"/><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M5 7h14"/><path d="M5 7 2 14a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "landmark": '<path d="M3 21h18"/><path d="M5 21V10M9.5 21V10M14.5 21V10M19 21V10"/><path d="M2 10l10-6 10 6z"/>',
    "down": '<path d="M12 5v14"/><path d="M6 13l6 6 6-6"/>',
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

def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


# poprawki transkrypcji (whisper -> tekst napisow); teksty fraz i tak ida z PHRASES / KIN, FIX tylko pod W()
FIX = {"małe": "mało", "Poszkodowana": "Poszkodowany"}  # whisper slyszy "-a właśnie"; w skrypcie Jakuba "Poszkodowany"
# Slowa, ktore whisper zgubil (zlane z sasiednim): (po slowie, przed slowem, wstawka). Mowi "za mało z OC sprawcy",
# whisper slyszy "za małe OC sprawcy" - "z" dostaje ostatnie 60 ms przed "OC".
WSTAW = [("mało", "oc", "z")]

# Hook kinetyczny: bloki (male slowa, duze haslo, male slowa po hasle, czy haslo akcentem).
# Puenta akcentem, kontrast na bialo. Teksty stad, czasy z transkrypcji (liczba slow musi sie zgadzac).
KIN = {
    "A": [("Prowadzisz kancelarię zajmującą się", "szkodami OC?", "", False),
          ("Płać tylko i wyłącznie", "za leady,", "", False),
          ("które są", "zweryfikowane", "telefonicznie,", True)],
    "B": [("Dzwonisz do leada ze szkody OC.", "A tam cisza.", "", False),
          ("Gwarantuję Ci, nasze leady", "odebrały telefon,", "zanim dotarły do Twojego CRM-a.", True)],
    "C": [("Ubezpieczyciel", "zaniżył", "odszkodowanie OC.", False),
          ("Poszkodowany właśnie teraz", "szuka kancelarii,", "która to sprawdzi.", True)],
}
# Reszta hooka juz jako zwykle napisy. *slowa* = wyroznienie akcentem.
HOOK_CAPS = {
    "A": ["a nie za takie,", "które za każdym razem", "mówią:", "„Ej, ja *nie pamiętam,*", "żebym cokolwiek wypełniał”."],
    "B": [],
    "C": ["I teraz pytanie:", "trafi *do Ciebie,*", "czy do *konkurencji?*"],
}
KORPUS = [
    "Dostarczamy kancelariom", "osoby, którym ubezpieczyciel", "wypłacił *za mało*", "z *OC sprawcy*",
    "i które chcą sprawdzić,", "czy da się *odzyskać więcej.*",
    "Nasz zespół", "za każdym razem", "*najpierw dzwoni*", "do każdej z tych osób.",
    "Dostajesz tylko i wyłącznie te,", "które *odebrały*", "i chcą rozmawiać", "*z prawnikiem.*",
    "Każda od razu ląduje", "w *Twoim CRM*", "z notatką z rozmowy.",
    "Pierwsze leady masz", "do *48 godzin* od startu.",
    "Płacisz *za leady,*", "a nie za budżet reklamowy", "czy czas zespołu.",
    "I co warto dodać,", "każde zamówienie", "jest objęte *gwarancją.*",
    "*Zostaw kontakt* poniżej.",
    "Oddzwonię i powiem Ci,", "ile i na kiedy", "mógłbym Ci dostarczyć", "pierwsze *leady OC.*",
]
PHRASES = HOOK_CAPS[HOOK] + KORPUS


def load_words():
    ws = json.loads((P / "audio/slowa.json").read_text())
    ws = [[a, b, FIX.get(t, t)] for a, b, t in ws]
    out = []
    for i, w in enumerate(ws):
        out.append(w)
        for po, przed, wst in WSTAW:
            if norm(w[2]) == po and i + 1 < len(ws) and norm(ws[i + 1][2]) == przed:
                t = ws[i + 1][0]
                out.append([round(t - 0.07, 3), round(t - 0.01, 3), wst])
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

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1});')
    for e in edl:
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')

    nb = sum(1 for e in edl if e.get("hook"))  # ile pierwszych kwestii to hook
    K = lambda i: edl[nb + i]                    # kwestie korpusu: K(0) .. K(9)
    body_in = K(0)["t_in"]
    last = edl[-1]
    end_card_in = round(last["speech"][1] - last["a_in"] + last["t_in"] + 0.12, 3)

    if SCRIM:
        el.append(f'<div id="scrim" class="scrim clip" data-layout-ignore data-start="0" data-duration="{total:.3f}" data-track-index="1"></div>')

    # --- hook kinetyczny
    hook = [w for w in words if w[0] < body_in - 0.001]
    blocks, k = [], 0
    for small_t, big_t, after_t, akcent in KIN[HOOK]:
        parts = []
        for txt in (small_t, big_t, after_t):
            toks = txt.split()
            ws = hook[k:k + len(toks)]
            if [norm(w[2]) for w in ws] != [norm(t) for t in toks]:
                raise SystemExit(f"Hook: niezgodnosc slow: {[w[2] for w in ws]} vs {toks}")
            parts.append([[w[0], w[1], t] for w, t in zip(ws, toks)])
            k += len(toks)
        blocks.append((parts[0], parts[1], parts[2], akcent))
    n_kin = k
    kin_end = hook[n_kin][0] - 0.06 if n_kin < len(hook) else body_in
    for k, (small, big, after, akcent) in enumerate(blocks):
        start = max(0.0, small[0][0] - 0.06)
        end = blocks[k + 1][0][0][0] - 0.06 if k + 1 < len(blocks) else kin_end
        big_txt = [w[2].upper() for w in big]
        # wersaliki Inter Tight 800 to ok. 0,63 rozmiaru na znak; max 900 px (przyciski Instagrama przy prawej krawedzi)
        size = min(132, int(900 / (len(" ".join(big_txt)) * 0.63)))
        sid = f"k{k}"
        el.append(
            f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">'
            f'<div class="kin-s">{"".join(span(w) for w in small)}</div>'
            f'<div class="kin-b{" accent" if akcent else ""}" style="font-size:{size}px">'
            + "".join(f'<span class="b">{html.escape(t)}</span>' for t in big_txt) + "</div>"
            + (f'<div class="kin-s kin-t">{"".join(span(w) for w in after)}</div>' if after else "") + "</div>")
        for i, w in enumerate(small):
            js.append(f'tl.fromTo("#{sid} .kin-s:not(.kin-t) .w:nth-child({i + 1})",{{opacity:0,y:18,filter:"blur(8px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0] - 0.04):.3f});')
        for i, w in enumerate(big):
            js.append(f'tl.fromTo("#{sid} .kin-b .b:nth-child({i + 1})",{{opacity:0,scale:1.35,filter:"blur(14px)"}},'
                      f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(start, w[0] - 0.05):.3f});')
        for i, w in enumerate(after):
            js.append(f'tl.fromTo("#{sid} .kin-t .w:nth-child({i + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{w[0] - 0.04:.3f});')
        srt.append((start, end, " ".join(w[2] for w in small + big + after)))

    # --- napisy slowo po slowie (reszta hooka + korpus)
    phrases = manual_group(hook[n_kin:] + [w for w in words if w[0] >= body_in - 0.001])
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

    # ================= grafiki hooka (zalezne od wersji) =================
    if HOOK == "A":
        # chip przy "a nie za takie, ktore..." - kontrast do "zweryfikowane telefonicznie"
        t0 = W("takie", kin_end)[0] - 0.1
        inner = (f'<div class="chip2 off"><span class="tile sm off">{icon("phone", 30)}</span>'
                 '<span>LEAD BEZ WERYFIKACJI</span></div>')
        overlay("badlead", t0, body_in - 0.02, inner, "chipwrap")
    if HOOK == "C":
        # "trafi do Ciebie, czy do konkurencji?" - dwie pigulki
        t_a, t_b = W("ciebie", kin_end)[0], W("konkurencji", kin_end)[0]
        inner = (f'<div class="chip2" id="fk0"><span class="tile sm">{icon("landmark", 30)}</span><span>DO CIEBIE</span></div>'
                 f'<div class="chip2 off" id="fk1"><span class="tile sm off">{icon("users", 30)}</span><span>DO KONKURENCJI</span></div>')
        f_in = t_a - 0.12
        el.append(f'<div id="fork" class="forkwrap clip" data-start="{f_in:.3f}" data-duration="{body_in - 0.02 - f_in:.3f}" data-track-index="5">{inner}</div>')
        pop("#fk0", t_a - 0.08)
        pop("#fk1", t_b - 0.08)
        js.append(f'tl.to("#fork",{{opacity:0,y:-18,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{body_in - 0.24:.3f});')

    # ================= korpus =================
    # --- P1: kogo dostarczamy (K0 od "osoby" + K1)
    k0, k1 = K(0), K(1)
    t1 = W("osoby", k0["t_in"])[0] - 0.04
    rows = [("Ubezpieczyciel wypłacił za mało", W("wypłacił", k0["t_in"])[0]),
            ("Szkoda z OC sprawcy", W("oc", W("mało", k0["t_in"])[0])[0]),
            ("Chce sprawdzić, czy odzyska więcej", W("sprawdzić", k1["t_in"])[0])]
    inner = ('<div class="p-head" style="top:350px">KOGO DOSTARCZAMY</div>'
             f'<div class="lead" id="p1card"><div class="lead-top"><div class="tile">{icon("user", 46)}</div>'
             '<div><div class="lead-name">Poszkodowany</div><div class="lead-sub">lead z OC</div></div></div>'
             '<div class="lead-rows">'
             + "".join(f'<div class="lrow" id="p1r{k}"><span class="dot">{icon("check", 26)}</span><span>{html.escape(t)}</span></div>'
                       for k, (t, _) in enumerate(rows))
             + "</div></div>")
    panel("p1", t1, K(2)["t_in"], inner)
    pop("#p1card", t1 + 0.02)
    for k, (_, t) in enumerate(rows):
        pop(f"#p1r{k}", t - 0.08)

    # --- karta polaczenia (K2): nasz zespol najpierw dzwoni
    k2 = K(2)
    t_c = W("zespół", k2["t_in"])[0] - 0.1
    t_dz = W("dzwoni", k2["t_in"])[0]
    inner = (f'<div class="tile" id="calltile">{icon("phonecall", 42)}</div><div class="nt-body">'
             '<div class="nt-top"><b>Nasz zespół</b><span>· telefon</span><span class="nt-time">teraz</span></div>'
             '<div class="nt-title" id="calltxt">Dzwonimy do każdej osoby</div></div>')
    overlay("call", t_c, K(3)["t_in"] - 0.02, inner, "notif", y_from=-60)
    js.append(f'tl.fromTo("#calltxt",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{t_dz - 0.06:.3f});')
    js.append(f'tl.fromTo("#calltile",{{scale:1}},{{scale:1.12,duration:0.26,ease:"sine.inOut",yoyo:true,'
              f'repeat:{max(1, int((K(3)["t_in"] - t_dz) / 0.26) | 1)}}},{t_dz - 0.06:.3f});')

    # --- kafelki z ptaszkami (K3): odebrala / chce rozmawiac z prawnikiem
    k3 = K(3)
    tiles = [("phone", "Odebrała<br>telefon", W("odebrały", k3["t_in"])[0]),
             ("scale", "Chce rozmawiać<br>z prawnikiem", W("chcą", k3["t_in"])[0])]
    inner = "".join(f'<div class="tcard" id="tc{k}"><div class="tile">{icon(ic, 40)}</div><div class="tlbl">{lbl}</div>'
                    f'<span class="tok">{icon("check", 24)}</span></div>' for k, (ic, lbl, _) in enumerate(tiles))
    el.append(f'<div id="tiles" class="tiles two clip" data-start="{tiles[0][2] - 0.1:.3f}" '
              f'data-duration="{K(4)["t_in"] - tiles[0][2] + 0.08:.3f}" data-track-index="5">{inner}</div>')
    for k, (_, _, t) in enumerate(tiles):
        pop(f"#tc{k}", t - 0.08)
    js.append(f'tl.to("#tiles",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{K(4)["t_in"] - 0.24:.3f});')

    # --- P2: lead laduje w CRM z notatka (K4)
    k4 = K(4)
    inner = ('<div class="p-head" style="top:300px">TWÓJ CRM</div>'
             f'<div class="cal" id="p2crm"><div class="cal-top">{icon("kanban", 40)}<span>Leady</span>'
             '<span class="cal-d">nowe</span></div><div class="crm-grid">'
             '<div class="ghost" style="top:8px"></div>'
             f'<div class="evt crm" id="p2evt"><div class="evt-t">Poszkodowany · szkoda z OC</div>'
             f'<div class="evt-s">{icon("phone", 26)}odebrała, chce rozmawiać z prawnikiem</div></div>'
             '<div class="ghost" style="top:256px"></div></div></div>'
             f'<div class="inv"><div class="pill ok" id="p2note">{icon("file", 30)} NOTATKA Z ROZMOWY</div></div>')
    panel("p2", k4["t_in"], K(5)["t_in"], inner)
    pop("#p2crm", k4["t_in"] + 0.02)
    t_land = W("ląduje", k4["t_in"])[0]
    js.append(f'tl.fromTo("#p2evt",{{opacity:0,y:-150,scale:0.92}},{{opacity:1,y:0,scale:1,duration:0.42,ease:"bounce.out"}},{t_land - 0.12:.3f});')
    pop("#p2note", W("notatką", k4["t_in"])[0] - 0.06)

    # --- karta "do 48 h" (K5)
    k5 = K(5)
    t_s = W("pierwsze", k5["t_in"])[0] - 0.1
    inner = (f'<div class="tile">{icon("clock", 46)}</div><div class="st-txt"><div class="st-l">PIERWSZE LEADY</div>'
             '<div class="st-s">od startu</div></div>'
             '<div class="st-n" id="st48"><span class="st-do">do</span><span class="st-big">48 h</span></div>')
    overlay("stat", t_s, K(6)["t_in"] - 0.02, inner, "stat")
    js.append(f'tl.fromTo("#st48",{{opacity:0,scale:1.4,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{W("48", k5["t_in"])[0] - 0.05:.3f});')

    # --- P3: za co placisz (K6)
    k6 = K(6)
    pay = [("user", "LEADY", W("leady", k6["t_in"])[0], True),
           ("megaphone", "BUDŻET REKLAMOWY", W("budżet", k6["t_in"])[0], False),
           ("clock", "CZAS ZESPOŁU", W("czas", k6["t_in"])[0], False)]
    inner = '<div class="p-head" style="top:400px">ZA CO PŁACISZ</div><div class="list pay" style="top:490px">'
    for k, (ic, lbl, _, on) in enumerate(pay):
        mark = (f'<span class="dot">{icon("check", 26)}</span>' if on else f'<span class="xdot">{icon("x", 26)}</span>')
        strike = "" if on else f'<span class="strike" id="p3s{k}"></span>'
        inner += (f'<div class="row{"" if on else " off"}" id="p3r{k}"><div class="tile{"" if on else " off"}">{icon(ic, 46)}</div>'
                  f'<div class="lbl">{html.escape(lbl)}{strike}</div>{mark}</div>')
    inner += "</div>"
    panel("p3", k6["t_in"], K(7)["t_in"], inner)
    for k, (_, _, t, on) in enumerate(pay):
        pop(f"#p3r{k}", t - 0.08)
        if not on:
            js.append(f'tl.fromTo("#p3s{k}",{{scaleX:0}},{{scaleX:1,duration:0.28,ease:"power2.out"}},{t + 0.16:.3f});')

    # --- chip: gwarancja (K7)
    k7 = K(7)
    inner = (f'<div class="chip2" id="gw"><span class="tile sm">{icon("shield", 32)}</span><span>KAŻDE ZAMÓWIENIE</span>'
             f'<span class="okpart" id="gwok"><span class="dot sm">{icon("check", 22)}</span>GWARANCJA</span></div>')
    overlay("gww", W("każde", k7["t_in"])[0] - 0.1, K(8)["t_in"] - 0.02, inner, "chipwrap")
    js.append(f'tl.fromTo("#gwok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{W("gwarancją", k7["t_in"])[0] - 0.05:.3f});')

    # --- CTA: przycisk na mowcy (K8-K9) + chip "oddzwonie"
    k8, k9 = K(8), K(9)
    t_cta = W("zostaw", k8["t_in"])[0] + 0.05
    el.append(f'<div id="cta" class="ctawrap clip" data-start="{t_cta:.3f}" data-duration="{end_card_in - t_cta:.3f}" data-track-index="5">'
              f'<div class="btn" id="ctabtn">ZOSTAW KONTAKT <span class="arr" id="ctaarr">{icon("down", 44)}</span></div></div>')
    pop("#ctabtn", t_cta)
    js.append(f'tl.fromTo("#ctaarr",{{y:-6}},{{y:6,duration:0.35,ease:"sine.inOut",yoyo:true,'
              f'repeat:{max(1, int((end_card_in - t_cta - 0.4) / 0.35))}}},{t_cta + 0.4:.3f});')
    t_od = W("oddzwonię", k9["t_in"])[0] - 0.1
    inner = (f'<div class="chip2" id="odz"><span class="tile sm">{icon("phonecall", 30)}</span><span>ODDZWONIĘ</span>'
             '<span class="accpart" id="odzile">ILE I NA KIEDY</span></div>')
    overlay("odzw", t_od, end_card_in, inner, "chipwrap")
    js.append(f'tl.fromTo("#odzile",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{W("ile", k9["t_in"])[0] - 0.05:.3f});')

    # --- plansza koncowa (bez logo)
    inner = (f'<div class="endic" id="endic">{icon("phonecall", 104)}</div>'
             '<div class="endtxt" id="endtxt">Zostaw kontakt poniżej</div>'
             '<div class="endsub" id="endsub">Oddzwonię i powiem Ci, ile leadów OC i na kiedy</div>'
             f'<div class="btn endbtn" id="endbtn">ZOSTAW KONTAKT <span class="arr" id="endarr">{icon("down", 44)}</span></div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    js.append(f'tl.fromTo("#endic",{{opacity:0,scale:0.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.9)"}},{end_card_in + 0.05:.3f});')
    pop("#endtxt", end_card_in + 0.25)
    pop("#endsub", end_card_in + 0.38)
    pop("#endbtn", end_card_in + 0.52)
    js.append(f'tl.fromTo("#endarr",{{y:-6}},{{y:6,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:3}},{end_card_in + 0.9:.3f});')

    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el)) \
        .replace("{{JS}}", "\n      ".join(js)).replace("{{SCRIM}}", f"{SCRIM:.2f}")
    page = kolory(page)
    out = P / "hf/index.html"
    out.write_text(page)
    glos = P / "hf/glos.wav"
    glos.unlink(missing_ok=True)
    os.link(GLOS, glos)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | {len(phrases)} fraz, {len(el)} elementow, {total:.2f}s, plansza koncowa od {end_card_in:.2f}")
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
      :root { --ground: #0f1012; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --on-accent: {{ON_ACCENT}}; --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #898989; --font-display: "Inter Tight", sans-serif;
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

      .scrim { position: absolute; left: -60px; right: -60px; top: 760px; height: 860px; z-index: 5; pointer-events: none;
        background: radial-gradient(ellipse 50% 50% at 50% 47%, rgba(8,9,11,{{SCRIM}}) 0%, rgba(8,9,11,{{SCRIM}}) 34%, rgba(8,9,11,0) 100%); }
      .tile.off { background: #2a2c31; color: #a3a7af; box-shadow: inset 0 1px 0 rgba(255,255,255,.08); }
      .chip2.off { color: #c9ccd3; }
      .accpart { color: var(--accent-hi); padding-left: 18px; border-left: 1.5px solid rgba(255,255,255,.16); }
      .forkwrap { position: absolute; left: 0; right: 0; top: 150px; display: flex; justify-content: center; gap: 18px; z-index: 25; }
      .forkwrap .chip2 { font-size: 30px; padding: 12px 26px 12px 12px; gap: 14px; }

      .lead { position: absolute; left: 120px; width: 840px; top: 430px; border-radius: 34px; padding: 28px 32px 34px;
        background: linear-gradient(180deg, #1d1e22, #16171a); border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .lead-top { display: flex; align-items: center; gap: 24px; padding-bottom: 24px; border-bottom: 1.5px solid #2b2d32; }
      .lead-name { font-size: 50px; font-weight: 800; line-height: 1.1; }
      .lead-sub { font-size: 30px; font-weight: 600; color: var(--muted); margin-top: 4px; }
      .lead-rows { display: flex; flex-direction: column; gap: 22px; margin-top: 28px; }
      .lrow { display: flex; align-items: center; gap: 18px; font-size: 39px; font-weight: 700; white-space: nowrap; }

      .notif .tile { width: 84px; height: 84px; border-radius: 22px; }
      .tiles.two .tcard { width: 420px; }

      .crm-grid { position: relative; height: 360px; margin-top: 14px; }
      .ghost { position: absolute; left: 0; right: 0; height: 96px; border-radius: 22px; background: #1f2125; border: 1.5px solid #2b2d32; }
      .ghost::before { content: ""; position: absolute; left: 24px; top: 24px; width: 300px; height: 18px; border-radius: 9px; background: #30333a; }
      .ghost::after { content: ""; position: absolute; left: 24px; top: 56px; width: 190px; height: 14px; border-radius: 7px; background: #292b31; }
      .evt.crm { left: 0; top: 122px; height: 116px; }

      .stat { position: absolute; left: 90px; width: 900px; top: 96px; padding: 22px 38px 22px 22px; border-radius: 38px; display: flex; align-items: center; gap: 24px; z-index: 25;
        background: rgba(24,25,28,.9); border: 1.5px solid rgba(255,255,255,.10); box-shadow: 0 24px 70px rgba(0,0,0,.35); }
      .st-l { font-size: 30px; font-weight: 800; letter-spacing: .12em; color: var(--accent); white-space: nowrap; }
      .st-s { font-size: 30px; font-weight: 600; color: #c9ccd3; margin-top: 4px; }
      .st-n { margin-left: auto; display: flex; align-items: baseline; gap: 14px; white-space: nowrap; }
      .st-do { font-size: 40px; font-weight: 600; color: #c9ccd3; }
      .st-big { font-size: 104px; font-weight: 900; letter-spacing: -0.04em; line-height: 1;
        background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 28px rgba(var(--accent-rgb),.45)); }

      .list.pay { gap: 34px; }
      .list.pay .lbl { position: relative; }
      .row.off .lbl { color: #8b8f97; }
      .strike { position: absolute; left: -8px; right: -8px; top: 50%; height: 5px; margin-top: -2px; border-radius: 3px; background: #c9ccd3; transform-origin: left center; }
      .row .dot, .row .xdot { margin-left: auto; }
      .xdot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; background: #2a2c31; color: #a3a7af; flex: none; }

      .btn { display: inline-flex; align-items: center; gap: 14px; white-space: nowrap; font-size: 44px; font-weight: 800; letter-spacing: .04em; color: var(--on-accent);
        padding: 26px 52px; border-radius: 100px; background: linear-gradient(180deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 84%, black) 100%);
        text-shadow: 0 2px 6px rgba(90,30,0,.35);
        box-shadow: 0 0 60px rgba(var(--accent-rgb),.55), inset 0 1px 0 rgba(255,255,255,.35); }
      .arr { display: grid; }
      .endic { position: absolute; left: 50%; margin-left: -115px; top: 430px; width: 230px; height: 230px; border-radius: 60px; display: grid; place-items: center; color: var(--on-accent);
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 90px rgba(var(--accent-rgb),.5), inset 0 2px 0 rgba(255,255,255,.35); }
      .panel .endtxt { top: 730px; }
      .panel .endsub { top: 820px; }
      .endbtn { position: absolute; top: 950px; left: 50%; margin-left: -290px; width: 580px; justify-content: center; }

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

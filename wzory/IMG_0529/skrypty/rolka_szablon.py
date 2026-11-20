#!/usr/bin/env python3
"""Generuje ../hf/index.html (HyperFrames) dla rolki o Kaji: hook kinetyczny, napisy slowo po slowie,
plansze w palecie wybranej przez MARKA (personal brand albo adGen), odtworzony profil Kaji (odkrycie "agent AI"), CTA z komentarzem, plansza koncowa.
Dodatkowo ../napisy.srt (frazy napisow, do Premiere / uploadu).

Uzycie: python3 -I kompozycja.py
"""
import html
import json
import os
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Glos w rolce: wariant C (Sidon + "radiowy" lancuch, skrypty/studio.py), wybrany przez uzytkownika 13.11.
# Wideo A-rollu idzie bez dzwieku, glos jako osobna sciezka <audio> (ta sama os czasu co aroll.wav).
GLOS = P / "audio/aroll_studio_gleboki.wav"
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
AV = "kaja_avatar.png"

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


# poprawki transkrypcji (whisper -> tekst napisow)
FIX = {"czym,": "tym,", "Seter": "Setter", "seter": "setter", "setera,": "settera,"}

# Frazy napisow po hooku. *slowa* = wyroznienie akcentem. Tekst brany stad, czasy z transkrypcji.
PHRASES = [
    "Pilnuje pipeline'u,", "pisze do leadów,", "przygotowuje oferty.",
    "I każdego ranka dostaję", "od niej to, co jest", "*konkretnie* na ten dzień", "do zrobienia.",
    "CRM jest", "zawsze *uporządkowany.*",
    "Każde spotkanie ląduje", "w kalendarzu", "i wysyła się *zaproszenie*", "do klienta.",
    "Nie bierze urlopu, nie choruje", "i nigdy nie zapomina", "o *follow-upach.*",
    "Czy się myli? Czasem tak.", "Z tym, że setter", "też się myli, a kosztuje", "*30 razy* więcej.",
    "Kaja to *agent AI,*", "to oczywiste.", "Z tym, że teraz", "zadanie dla Ciebie.",
    "Zanim zatrudnisz", "kolejnego settera,", "bądź swojego pierwszego,", "zastanów się *dwa razy,*",
    "czy na pewno go potrzebujesz.", "Czy na pewno *agent AI*", "po prostu nie wystarczy?",
    "Jeśli interesuje Cię,", "skąd taką Kaję wytrzasnąć,", "napisz komentarz", "o treści *Kaja,*",
    "a nagram o tym osobną rolkę.",
]


def load_words():
    ws = json.loads((P / "audio/slowa.json").read_text())
    return [[a, b, FIX.get(t, t)] for a, b, t in ws]


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

    # --- hook kinetyczny (kwestie 0 i 1)
    hook = [w for w in words if w[0] < seg(2)["t_in"]]
    exp = ["Setter", "kosztuje", "Cię", "w", "okolicach", "5–6", "koła", "miesięcznie.",
           "Moja", "Kaja", "kosztuje", "mnie", "niecałe", "dwie", "stówki."]
    assert [norm(w[2]) for w in hook] == [norm(x) for x in exp], [w[2] for w in hook]
    kin_end = seg(2)["t_in"]
    kin = [  # (male, duze, male_po, duze_akcentem, tekst_duzych)
        (hook[0:5], hook[5:7], hook[7:8], False, ["5–6", "KOŁA"]),
        (hook[8:13], hook[13:15], [], True, ["DWIE", "STÓWKI"]),
    ]
    for k, (small, big, after, akcent, big_txt) in enumerate(kin):
        start = max(0.0, small[0][0] - 0.06)
        end = kin[k + 1][0][0][0] - 0.06 if k + 1 < len(kin) else kin_end
        size = min(132, int(960 / (len(" ".join(big_txt)) * 0.58)))
        sid = f"k{k}"
        smalls = "".join(
            (f'<span class="w mention"><img src="{AV}" alt="">Kaja</span>' if norm(w[2]) == "kaja" else span(w))
            for w in small)
        el.append(
            f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">'
            f'<div class="kin-s">{smalls}</div>'
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
    js.append(f'tl.fromTo("#k1 .mention img",{{scale:0.4}},{{scale:1,duration:0.35,ease:"back.out(2.2)"}},{W("kaja")[0] - 0.04:.3f});')

    # --- napisy slowo po slowie (od kwestii 2)
    end_card_in = round(seg(9)["speech"][1] - seg(9)["a_in"] + seg(9)["t_in"] + 0.12, 3)
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

    # --- P1: co robi Kaja
    s2 = seg(2)
    rows = [("kanban", "PILNUJE PIPELINE'U", W("pilnuje")[0]), ("send", "PISZE DO LEADÓW", W("pisze")[0]),
            ("file", "PRZYGOTOWUJE OFERTY", W("przygotowuje")[0])]
    inner = (f'<div class="p1av" id="p1av"><img src="{AV}" alt=""></div>'
             '<div class="p-head" style="top:440px">CO ROBI KAJA</div><div class="list" style="top:530px">')
    for k, (ic, lbl, _) in enumerate(rows):
        inner += f'<div class="row" id="p1r{k}"><div class="tile">{icon(ic, 46)}</div><div class="lbl">{html.escape(lbl)}</div></div>'
    inner += "</div>"
    panel("p1", s2["t_in"], seg(3)["t_in"], inner)
    pop("#p1av", s2["t_in"] - 0.02)
    for k, (_, _, t) in enumerate(rows):
        pop(f"#p1r{k}", t - 0.08)

    # --- powiadomienie "plan na dzis" (kwestia 3, pelny kadr)
    s3 = seg(3)
    items = [("3 follow-upy", W("konkretnie", s3["t_in"])[0]), ("2 spotkania", W("ten", s3["t_in"])[0]),
             ("1 oferta", W("zrobienia", s3["t_in"])[0])]
    inner = (f'<img class="nt-av" src="{AV}" alt=""><div class="nt-body">'
             '<div class="nt-top"><b>Kaja</b><span>· Sprzedaż</span><span class="nt-time">7:30</span></div>'
             f'<div class="nt-title">{icon("sun", 40)}Plan na dziś</div><div class="nt-items">'
             + "".join(f'<span class="nti" id="nti{k}">{html.escape(t)}</span>' for k, (t, _) in enumerate(items))
             + "</div></div>")
    overlay("nt", W("ranka", s3["t_in"])[0] - 0.12, seg(4)["t_in"] - 0.02, inner, "notif", y_from=-60)
    for k, (_, t) in enumerate(items):
        pop(f"#nti{k}", t - 0.06)

    # --- chip CRM (kwestia 4)
    s4 = seg(4)
    inner = (f'<div class="chip2" id="crm"><span class="tile sm">{icon("kanban", 32)}</span><span>CRM</span>'
             f'<span class="okpart" id="crmok"><span class="dot sm">{icon("check", 22)}</span>UPORZĄDKOWANY</span></div>')
    overlay("crmw", W("crm", s4["t_in"])[0] - 0.1, seg(5)["t_in"] - 0.02, inner, "chipwrap")
    js.append(f'tl.fromTo("#crmok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{W("uporządkowany", s4["t_in"])[0] - 0.05:.3f});')

    # --- P2: kalendarz + zaproszenie (kwestia 5)
    s5 = seg(5)
    inner = ('<div class="p-head" style="top:300px">KALENDARZ</div>'
             f'<div class="cal" id="p2cal"><div class="cal-top">{icon("calendar", 40)}<span>Dziś</span>'
             '<span class="cal-d">Twoje spotkania</span></div><div class="cal-grid">'
             '<div class="cal-row" style="top:0"><span>10:00</span></div>'
             '<div class="cal-row" style="top:120px"><span>11:00</span></div>'
             '<div class="cal-row" style="top:240px"><span>12:00</span></div>'
             f'<div class="evt" id="p2evt"><div class="evt-t">Spotkanie z klientem</div>'
             f'<div class="evt-s">{icon("clock", 26)}11:00 – 12:00</div></div></div></div>'
             f'<div class="inv"><div class="pill ok" id="p2inv">{icon("mail", 30)} ZAPROSZENIE WYSŁANE</div></div>')
    panel("p2", s5["t_in"], seg(6)["t_in"], inner)
    pop("#p2cal", s5["t_in"] + 0.02)
    t_land = W("ląduje", s5["t_in"])[0]
    js.append(f'tl.fromTo("#p2evt",{{opacity:0,y:-150,scale:0.92}},{{opacity:1,y:0,scale:1,duration:0.42,ease:"bounce.out"}},{t_land - 0.12:.3f});')
    pop("#p2inv", W("zaproszenie", s5["t_in"])[0] - 0.06)

    # --- kafelki: urlop / choroba / follow-upy (kwestia 6, pelny kadr)
    s6 = seg(6)
    tiles = [("palm", "Nie bierze<br>urlopu", W("nie", s6["t_in"])[0]),
             ("thermo", "Nie<br>choruje", W("choruje", s6["t_in"])[0] - 0.12),
             ("bell", "Nie zapomina<br>o follow-upach", W("nigdy", s6["t_in"])[0])]
    inner = "".join(f'<div class="tcard" id="tc{k}"><div class="tile">{icon(ic, 40)}</div><div class="tlbl">{lbl}</div>'
                    f'<span class="tok">{icon("check", 24)}</span></div>' for k, (ic, lbl, _) in enumerate(tiles))
    el.append(f'<div id="tiles" class="tiles clip" data-start="{tiles[0][2] - 0.1:.3f}" '
              f'data-duration="{seg(7)["t_in"] - tiles[0][2] + 0.08:.3f}" data-track-index="5">{inner}</div>')
    for k, (_, _, t) in enumerate(tiles):
        pop(f"#tc{k}", t - 0.08)
    js.append(f'tl.to("#tiles",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{seg(7)["t_in"] - 0.24:.3f});')

    # --- P3: koszt miesieczny, 30x (od "Z tym, ze setter" do konca kwestii 7)
    s7 = seg(7)
    t3 = W("z", s7["t_in"])[0]
    inner = ('<div class="p-head" style="top:330px">KOSZT MIESIĘCZNIE</div><div class="bars">'
             '<div class="brow" id="p3r0"><div class="bhead"><span class="bl">SETTER</span><span class="bv">5–6 tys. zł</span></div>'
             '<div class="btrack"><div class="bfill gray" id="p3b0"></div></div></div>'
             f'<div class="brow" id="p3r1"><div class="bhead"><span class="bl"><img src="{AV}" alt="">KAJA</span>'
             '<span class="bv o">&lt; 200 zł</span></div><div class="btrack"><div class="bfill accent" id="p3b1"></div></div></div></div>'
             '<div class="big30" id="p3x">30×</div><div class="big30s" id="p3xs">WIĘCEJ</div>')
    p4_in = seg(8)["t_in"]
    panel("p3", t3, p4_in, inner, leak_out=False, fade_out=False, extend=0.3)
    t_set = W("setter", s7["t_in"])[0]
    pop("#p3r0", t_set - 0.1)
    js.append(f'tl.fromTo("#p3b0",{{scaleX:0}},{{scaleX:1,duration:0.7,ease:"power2.out"}},{t_set:.3f});')
    t_k = W("kosztuje", s7["t_in"])[0]
    pop("#p3r1", t_k - 0.1)
    js.append(f'tl.fromTo("#p3b1",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power2.out"}},{t_k + 0.05:.3f});')
    t30 = W("30", s7["t_in"])[0]
    js.append(f'tl.fromTo("#p3x",{{opacity:0,scale:1.5,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{t30 - 0.05:.3f});')
    pop("#p3xs", W("więcej", s7["t_in"])[0] - 0.05)

    # --- P4: odkrycie - profil Kaji (kwestia 8, pierwsze ujecie)
    s8 = seg(8)
    p4_out = s8["shots"][1]["t_in"]
    inner = (f'<div class="pcard" id="pcard"><div class="pc-banner"></div><div class="pc-ring"></div>'
             f'<img class="pc-av" src="{AV}" alt=""><div class="pc-name">Kaja · Sprzedaż</div>'
             f'<div class="pc-bot" id="pcbot">{icon("users", 44)}<span>Bot zespołu</span></div>'
             '<div class="pc-tabs"><span class="pc-tab on">Ogólne</span><span class="pc-tab">Wiedza</span>'
             '<span class="pc-tab">Analityka</span></div>'
             f'<div class="pc-badge" id="pcbadge">{icon("sparkles", 34)}AGENT AI</div></div>')
    panel("p4", p4_in, p4_out, inner, track=7)
    pop("#pcard", p4_in + 0.02)
    t_ag = W("agent", p4_in)[0]
    js.append(f'tl.fromTo("#pcbadge",{{opacity:0,scale:0.5,rotation:-8}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"back.out(2.2)"}},{t_ag - 0.05:.3f});')
    js.append(f'tl.fromTo("#pcbot",{{color:"#9b9b9b"}},{{color:"#ffffff",duration:0.3}},{t_ag - 0.05:.3f});')

    # --- chip: zadanie dla Ciebie (kwestia 8, pelny kadr)
    t_task = W("zadanie", p4_in)[0] - 0.1
    inner = f'<div class="chip2" id="task"><span class="tile sm">{icon("target", 32)}</span><span>ZADANIE DLA CIEBIE</span></div>'
    overlay("taskw", t_task, s8["shots"][2]["t_in"] - 0.02, inner, "chipwrap")

    # --- CTA: komentarz "Kaja" (kwestia 9)
    s9 = seg(9)
    t_cta = W("napisz", s9["t_in"])[0] - 0.05
    t_kaja = W("kaja", W("treści", s9["t_in"])[0])[0]
    letters = "Kaja"
    inner = (f'<div class="cbox" id="cbox"><div class="cav">{icon("user", 40)}</div><div class="cin">'
             '<span class="cph" id="cph">Dodaj komentarz…</span><span class="ctyped">'
             + "".join(f'<span class="cl" id="cl{k}">{c}</span>' for k, c in enumerate(letters))
             + f'</span><span class="caret" id="caret"></span></div><div class="csend" id="csend">{icon("up", 40)}</div></div>')
    el.append(f'<div id="cta" class="ctawrap clip" data-start="{t_cta:.3f}" data-duration="{end_card_in - t_cta:.3f}" data-track-index="5">{inner}</div>')
    pop("#cbox", t_cta)
    js.append(f'tl.set("#cph",{{opacity:0}},{t_kaja - 0.04:.3f});')
    for k in range(len(letters)):
        js.append(f'tl.set("#cl{k}",{{display:"inline-block"}},{t_kaja - 0.04 + k * 0.08:.3f});')
    js.append(f'tl.fromTo("#caret",{{opacity:1}},{{opacity:0,duration:0.32,ease:"steps(1)",repeat:{int((end_card_in - t_cta) / 0.32)},yoyo:true}},{t_cta + 0.3:.3f});')
    t_send = t_kaja + 0.45
    js.append(f'tl.fromTo("#csend",{{scale:1}},{{scale:1.18,duration:0.16,ease:"power2.out",yoyo:true,repeat:1}},{t_send:.3f});')

    # --- plansza koncowa (bez logo adGen: rolki sa pod personal brand uzytkownika)
    inner = ('<div class="bubble" id="bub"><span>KAJA</span></div>'
             '<div class="endtxt" id="endtxt">Napisz w komentarzu</div>'
             '<div class="endsub" id="endsub">a nagram o tym osobną rolkę</div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    js.append(f'tl.fromTo("#bub",{{opacity:0,scale:0.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.9)"}},{end_card_in + 0.05:.3f});')
    pop("#endtxt", end_card_in + 0.25)
    pop("#endsub", end_card_in + 0.38)

    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el)) \
        .replace("{{JS}}", "\n      ".join(js))
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

#!/usr/bin/env python3
"""Generuje index.html (HyperFrames) dla wersji A i B: napisy, hook, plansze, CTA w brandingu adGen.

Uzycie: python3 -I kompozycja.py
"""
import html
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parent.parent
LOGO = (P / "branding/adGen_Logo.svg").read_text().strip()

ORANGE = "#ff7018"
HL = {"szybciej", "frustracja", "telefonicznie", "jedna", "kancelaria", "idealny", "wolumen"}

ICON = {
    "wallet": '<path d="M3 7a2 2 0 0 1 2-2h12v4"/><path d="M3 7v10a2 2 0 0 0 2 2h14V9H5a2 2 0 0 1-2-2z"/><circle cx="16" cy="14" r="1.2"/>',
    "fuel": '<path d="M4 20V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v15"/><path d="M3 20h12"/><path d="M6 8h6"/><path d="M14 10h2a2 2 0 0 1 2 2v4a1.5 1.5 0 0 0 3 0V8l-3-3"/>',
    "frown": '<circle cx="12" cy="12" r="9"/><path d="M8 16.5s1.5-2 4-2 4 2 4 2"/><path d="M9 9.5h.01M15 9.5h.01"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M5 7h14"/><path d="M5 7 2 14a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "landmark": '<path d="M3 21h18"/><path d="M5 21V10M9.5 21V10M14.5 21V10M19 21V10"/><path d="M2 10l10-6 10 6z"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "down": '<path d="M12 5v14"/><path d="M6 13l6 6 6-6"/>',
    "right": '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
}


def icon(name, size, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def load_words(path):
    d = json.loads(Path(path).read_text())
    out = []
    for s in d["transcription"]:
        t = s["text"].strip()
        if t:
            out.append([s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, t])
    return out


def fix_words(ws, version):
    res = []
    for a, b, t in ws:
        if t == "NATO":
            m = (a + b) / 2
            res += [[a, m, "na"], [m, b, "to"]]
            continue
        t = {"sprawdzanych": "sprawdzonych", "napięcia,": "napięcia.", "rośni": "rośnie",
             "służbność": "służebność"}.get(t, t)
        if t == "przesyłu," and a < 3.5 and version == "A":
            t = "przesyłu?"
        res.append([a, b, t])
    for i in range(1, len(res)):  # wielka litera po kropce / pytajniku
        if res[i - 1][2][-1] in ".?!":
            res[i][2] = res[i][2][0].upper() + res[i][2][1:]
    return res


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


def group(ws, cuts):
    phrases, cur = [], []
    for w in ws:
        if cur:
            prev = cur[-1]
            chars = sum(len(x[2]) + 1 for x in cur)
            cut_between = any(prev[1] - 0.05 <= c <= w[0] + 0.05 for c in cuts)
            if (len(cur) >= 3 or chars + len(w[2]) > 22 or prev[2][-1] in ",.?!"
                    or w[0] - prev[1] > 0.3 or cut_between):
                phrases.append(cur)
                cur = []
        cur.append(w)
    if cur:
        phrases.append(cur)
    return phrases


PHRASES = [
    "A oni jedyne co robią,", "to jeżdżą", "od drzwi do drzwi", "i odbijają się od nich,", "jakby nigdy tam nie było",
    "umówionego spotkania.",
    "Kancelarie rekrutują ludzi", "na odszkodowania", "za służebność przesyłu", "szybciej, niż zdobywają",
    "na to klientów.",
    "Po ostatnich wyrokach", "Trybunału Konstytucyjnego", "kancelarie ruszyły", "z rekrutacją", "przedstawicieli.",
    "Tyle, że przedstawiciel", "bez spotkań to", "pensja, paliwo", "i co najważniejsze", "ogromna frustracja,",
    "gdy nie sprzedaje.",
    "Dostarczamy właścicieli", "działek budowlanych", "pod liniami średniego", "i wysokiego napięcia.",
    "Sprawdzonych telefonicznie", "w województwach,", "w których pracuje", "Twój zespół.",
    "Wolumen dobieramy", "do liczby przedstawicieli,", "a każdy lead dostaje", "tylko jedna kancelaria.",
    "Zostaw kontakt poniżej", "i dobierzemy", "idealny wolumen", "dla Twojego zespołu.",
]


def manual_group(ws):
    """Dzieli slowa wg PHRASES; tekst bierze z PHRASES (poprawna interpunkcja), czasy z transkrypcji."""
    phrases, k = [], 0
    for ph in PHRASES:
        cur = []
        for tok in ph.split():
            if k >= len(ws):
                raise SystemExit(f"Brak slow dla frazy: {ph}")
            if norm(ws[k][2]) != norm(tok):
                raise SystemExit(f"Niezgodnosc: '{ws[k][2]}' vs '{tok}' we frazie '{ph}' (t={ws[k][0]:.2f})")
            cur.append([ws[k][0], ws[k][1], tok])
            k += 1
        phrases.append(cur)
    if k != len(ws):
        raise SystemExit(f"Nieprzypisane slowa: {[w[2] for w in ws[k:]]}")
    return phrases


def span(w, cls="w"):
    hl = " hl" if norm(w[2]) in HL else ""
    return f'<span class="{cls}{hl}">{html.escape(w[2])}</span>'


def build(version):
    edl = json.loads((P / f"aroll/edl_{version}.json").read_text())
    total = edl[-1]["t_out"]
    cuts = [e["t_in"] for e in edl[1:]]
    hook_end = edl[1]["t_in"] if version == "B" else edl[2]["t_in"]  # poczatek tresci glownej
    # przesuniecie osi wersji wzgledem A (dla wspolnych elementow tresci)
    edl_a = json.loads((P / "aroll/edl_A.json").read_text())
    shift = edl_a[2]["t_in"] - hook_end  # 0 dla A

    words_a = fix_words(load_words(P / "audio/slowa_A.json"), "A")
    body = [[a - shift, b - shift, t] for a, b, t in words_a if a >= edl_a[2]["t_in"] - 0.05]
    if version == "A":
        hook_words = [w for w in words_a if w[0] < edl_a[2]["t_in"] - 0.05]
        kin_end = 3.70
        kin = [  # (male slowa, duze slowa)
            ([w for w in hook_words if w[0] < 0.45], [w for w in hook_words if 0.45 <= w[0] < 1.2], False),
            ([w for w in hook_words if 1.2 <= w[0] < 2.65], [w for w in hook_words if 2.65 <= w[0] < kin_end], False),
        ]
        rest_hook = [w for w in hook_words if w[0] >= kin_end]
    else:
        hook_words = fix_words(load_words(P / "audio/slowa_B.json"), "B")
        hook_words = [w for w in hook_words if w[0] < hook_end - 0.05]
        kin_end = hook_end
        kin = [
            ([w for w in hook_words if w[0] < 1.2], [w for w in hook_words if 1.2 <= w[0] < 1.55], True),
            ([w for w in hook_words if 1.55 <= w[0] < 2.05], [w for w in hook_words if 2.05 <= w[0] < kin_end], False),
        ]
        rest_hook = []

    T = lambda t: round(t - shift, 3)  # czasy zdefiniowane na osi wersji A
    el, js, audio = [], [], []

    # --- wideo + delikatny najazd w kazdym ujeciu (stan bazowy + set/to na kazde ujecie)
    js.append('gsap.set("#vwrap",{scale:1});')
    for e in edl:
        js.append(f'tl.set("#vwrap",{{scale:1}},{e["t_in"]:.3f});')
        js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{e["t_out"]-e["t_in"]-0.001:.3f},ease:"none"}},{e["t_in"]:.3f});')

    # --- hook kinetyczny
    for k, (small, big, big_orange) in enumerate(kin):
        start = small[0][0] - 0.06 if small else big[0][0] - 0.06
        start = max(0, start)
        end = kin[k + 1][0][0][0] - 0.06 if k + 1 < len(kin) else kin_end
        big_txt = " ".join(w[2] for w in big)
        size = min(124, int(960 / (len(big_txt) * 0.56)))
        sid = f"k{k}"
        el.append(
            f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end-start:.3f}" data-track-index="3">'
            f'<div class="kin-s">{"".join(span(w) for w in small)}</div>'
            f'<div class="kin-b{" orange" if big_orange else ""}" style="font-size:{size}px">{"".join(span(w, "b") for w in big)}</div></div>')
        for i, w in enumerate(small):
            js.append(f'tl.fromTo("#{sid} .kin-s .w:nth-child({i+1})",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0]-0.04):.3f});')
        for i, w in enumerate(big):
            js.append(f'tl.fromTo("#{sid} .kin-b .b:nth-child({i+1})",{{opacity:0,scale:1.35,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(start, w[0]-0.05):.3f});')

    # --- napisy slowo po slowie
    end_card_in = T(43.15)
    all_phrases = manual_group(rest_hook + body if version == "A" else
                               [w for w in fix_words(load_words(P / "audio/slowa_A.json"), "A") if w[0] >= 3.70])
    if version == "B":  # tresc po hooku jest wspolna: te same frazy, przesuniete na os B
        all_phrases = [[[a - shift, b - shift, t] for a, b, t in ph] for ph in all_phrases
                       if ph[0][0] >= edl_a[2]["t_in"] - 0.05]
    phrases = all_phrases
    for i, ph in enumerate(phrases):
        start = max(ph[0][0] - 0.06, kin_end if i == 0 else 0)
        nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
        end = min(nxt, ph[-1][1] + 0.6, end_card_in)
        cid = f"c{i}"
        txt_len = len(" ".join(w[2] for w in ph))
        fs = min(66, int(950 / (txt_len * 0.54)))
        el.append(f'<div id="{cid}" class="cap clip" data-start="{start:.3f}" data-duration="{end-start:.3f}" data-track-index="4" style="font-size:{fs}px">'
                  + " ".join(span(w) for w in ph) + "</div>")
        for j, w in enumerate(ph):
            js.append(f'tl.fromTo("#{cid} .w:nth-child({j+1})",{{opacity:0,y:14,filter:"blur(7px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{max(start, w[0]-0.03):.3f});')

    def whoosh(t, vol=0.5):
        audio.append(f'<audio id="sfx{len(audio)}" src="sfx/whoosh.wav" data-start="{max(0, t-0.32):.3f}" data-duration="0.7" data-volume="{vol}" data-track-index="9"></audio>')

    def leak(t, idx):
        el.append(f'<div id="lk{idx}" class="leak clip" data-layout-ignore data-start="{t-0.22:.3f}" data-duration="0.55" data-track-index="8"></div>')
        js.append(f'tl.fromTo("#lk{idx}",{{opacity:0,xPercent:-18}},{{opacity:1,xPercent:0,duration:0.2,ease:"power2.out"}},{t-0.22:.3f});')
        js.append(f'tl.to("#lk{idx}",{{opacity:0,xPercent:16,duration:0.3,ease:"power2.in"}},{t-0.02:.3f});')

    def panel(pid, t_in, t_out, inner, track=2):
        el.append(f'<div id="{pid}" class="panel clip" data-start="{t_in-0.12:.3f}" data-duration="{t_out-t_in+0.12:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div><div class="sq sq1"></div><div class="sq sq2"></div><div class="sq sq3"></div>{inner}</div>')
        js.append(f'tl.fromTo("#{pid}",{{opacity:0,scale:1.06,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{t_in-0.12:.3f});')
        js.append(f'tl.fromTo("#{pid} .sq1",{{rotation:-14,y:60}},{{rotation:-6,y:0,duration:{t_out-t_in:.3f},ease:"none"}},{t_in:.3f});')
        js.append(f'tl.fromTo("#{pid} .sq2",{{rotation:18,y:40}},{{rotation:9,y:-20,duration:{t_out-t_in:.3f},ease:"none"}},{t_in:.3f});')
        js.append(f'tl.fromTo("#{pid} .sq3",{{rotation:8}},{{rotation:20,duration:{t_out-t_in:.3f},ease:"none"}},{t_in:.3f});')
        leak(t_in, pid + "i")
        whoosh(t_in)
        if t_out < total - 0.1:
            js.append(f'tl.to("#{pid}",{{opacity:0,scale:1.04,filter:"blur(14px)",duration:0.18,ease:"power2.in"}},{t_out-0.18:.3f});')
            leak(t_out, pid + "o")
            whoosh(t_out, 0.38)

    def pop(sel, t, extra=""):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:26,scale:0.94{extra}}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')

    # --- chip: wyroki TK (na mowcy)
    t_in, t_out = T(16.75), T(20.75)
    el.append(f'<div id="tk" class="chip clip" data-start="{t_in:.3f}" data-duration="{t_out-t_in:.3f}" data-track-index="5">'
              f'<span class="chip-ic">{icon("scale", 40)}</span><span>WYROKI TRYBUNAŁU KONSTYTUCYJNEGO</span></div>')
    js.append(f'tl.fromTo("#tk",{{opacity:0,y:-30,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
    js.append(f'tl.to("#tk",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.25,ease:"power2.in"}},{t_out-0.25:.3f});')

    # --- P1: koszty przedstawiciela
    rows = [("wallet", "PENSJA", 23.17), ("fuel", "PALIWO", 23.69), ("frown", "FRUSTRACJA", 25.59)]
    inner = '<div class="p-head" style="top:360px">PRZEDSTAWICIEL BEZ SPOTKAŃ</div><div class="list" style="top:450px">'
    for k, (ic, lbl, _) in enumerate(rows):
        inner += f'<div class="row" id="p1r{k}"><div class="tile">{icon(ic, 46)}</div><div class="lbl">{lbl}</div></div>'
    inner += "</div>"
    panel("p1", T(22.95), T(27.83), inner)
    for k, (_, _, t) in enumerate(rows):
        pop(f"#p1r{k}", T(t) - 0.08)

    # --- P2: karta leada
    checks = [("Właściciel działki budowlanej", 30.0), ("Linia średniego / wysokiego napięcia", 30.46),
              ("Zweryfikowany telefonicznie", 31.96), ("Z Twojego województwa", 33.08)]
    inner = ('<div class="card" id="p2card"><div class="avatar">' + icon("user", 52) + '</div>'
             '<div class="name">Jan Kowalski</div><div class="phone">+48 XXX XXX XXX</div>'
             '<div class="pills"><div class="pill gray" id="p2pend" data-layout-allow-overlap>WERYFIKACJA…</div>'
             f'<div class="pill green" id="p2ok" data-layout-allow-overlap>{icon("check", 26)} ZWERYFIKOWANY</div></div></div><div class="checks">')
    for k, (txt, _) in enumerate(checks):
        inner += f'<div class="chk" id="p2c{k}"><span class="dot">{icon("check", 24)}</span>{html.escape(txt)}</div>'
    inner += "</div>"
    panel("p2", T(29.90), T(35.10), inner)
    pop("#p2card", T(29.92))
    for k, (_, t) in enumerate(checks):
        pop(f"#p2c{k}", T(t) - 0.06)
    js.append(f'tl.fromTo("#p2ok",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{T(32.47):.3f});')
    js.append(f'tl.fromTo("#p2pend",{{opacity:1}},{{opacity:0,duration:0.15}},{T(32.42):.3f});')

    # --- P3: wylacznosc
    inner = ('<div class="excl"><div class="xt" id="p3a">' + icon("user", 92, "o") + '<div class="xl">1 LEAD</div></div>'
             f'<div class="xarrow" id="p3arr">{icon("right", 64)}</div>'
             '<div class="xt" id="p3b">' + icon("landmark", 92, "o") + '<div class="xl">1 KANCELARIA</div></div></div>'
             f'<div class="xpill" id="p3pill">{icon("lock", 34)} NA WYŁĄCZNOŚĆ</div>')
    panel("p3", T(37.37), T(39.87), inner)
    pop("#p3a", T(37.70))
    js.append(f'tl.fromTo("#p3arr",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.25,ease:"power2.out"}},{T(38.05):.3f});')
    pop("#p3b", T(38.58))
    pop("#p3pill", T(38.95))

    # --- CTA na mowcy
    t_in = T(40.10)
    el.append(f'<div id="cta" class="ctawrap clip" data-start="{t_in:.3f}" data-duration="{end_card_in-t_in:.3f}" data-track-index="5">'
              f'<div class="btn">ZOSTAW KONTAKT <span class="arr">{icon("down", 44)}</span></div></div>')
    pop("#cta .btn", t_in)
    js.append(f'tl.fromTo("#cta .arr",{{y:-6}},{{y:6,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:7}},{t_in+0.4:.3f});')

    # --- plansza koncowa
    inner = (f'<div class="endlogo" id="endlogo">{LOGO}</div>'
             '<div class="endtag" id="endtag">Leady dla kancelarii odszkodowawczych</div>'
             f'<div class="btn endbtn" id="endbtn">ZOSTAW KONTAKT {icon("down", 44)}</div>')
    panel("pend", end_card_in, total, inner, track=6)
    pop("#endlogo", end_card_in + 0.08)
    pop("#endtag", end_card_in + 0.25)
    pop("#endbtn", end_card_in + 0.4)

    page = TEMPLATE.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(el + audio)) \
        .replace("{{JS}}", "\n      ".join(js)).replace("{{ORANGE}}", ORANGE)
    out = P / f"hf_{version}/index.html"
    out.write_text(page)
    print(f"{version}: {out} | {len(phrases)} fraz, {len(el)} elementow, {len(audio)} sfx, {total:.2f}s")
    for ph in phrases:
        print(f"   {ph[0][0]:6.2f} " + " ".join(w[2] for w in ph))


TEMPLATE = r"""<!doctype html>
<html lang="pl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      :root { --ground: #0f1012; --ink: #ffffff; --orange: {{ORANGE}}; --muted: #898989; --font-display: "Inter Tight", sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); color: var(--ink); }
      #vwrap { position: absolute; inset: 0; transform-origin: 50% 38%; }
      #aroll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }

      .kin { position: absolute; left: 0; right: 0; top: 1030px; text-align: center; z-index: 30; }
      .kin-s { font-size: 50px; font-weight: 600; letter-spacing: -0.01em; display: flex; justify-content: center; flex-wrap: wrap; gap: 0 16px; padding: 0 70px; }
      .kin-b { font-weight: 800; letter-spacing: -0.04em; line-height: 1.02; margin-top: 2px; display: flex; justify-content: center; gap: 0 0.22em; white-space: nowrap; }
      .kin .w, .kin .b, .cap .w { display: inline-block; }
      .kin-s .w, .cap .w, .kin-b .b {
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,255,255,.14));
      }
      .kin-b.orange .b, .cap .w.hl, .kin .w.hl, .kin-b .b.hl { background: linear-gradient(180deg, #ffa25f 0%, var(--orange) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }

      .cap { position: absolute; left: 60px; right: 60px; top: 1120px; text-align: center; font-size: 66px; font-weight: 650; letter-spacing: -0.015em; line-height: 1.1; z-index: 30; white-space: nowrap; }

      .panel { position: absolute; inset: 0; z-index: 10; overflow: hidden; }
      .pbg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 18%, #222327 0%, #141518 45%, var(--ground) 100%); }
      .sq { position: absolute; border-radius: 34px; }
      .sq1 { width: 300px; height: 300px; left: 640px; top: 1560px; background: linear-gradient(140deg, #ff8f45, var(--orange)); box-shadow: 0 0 80px rgba(255,112,24,.35); }
      .sq2 { width: 190px; height: 190px; left: -50px; top: 1480px; background: linear-gradient(140deg, #ff8f45, var(--orange)); box-shadow: 0 0 60px rgba(255,112,24,.3); }
      .sq3 { width: 330px; height: 330px; left: 250px; top: 1640px; border: 5px solid rgba(255,112,24,.85); }

      .p-head { position: absolute; left: 0; right: 0; text-align: center; color: var(--orange); font-size: 32px; font-weight: 800; letter-spacing: .14em; }
      .list { position: absolute; left: 50%; transform: translateX(-50%); width: 480px; display: flex; flex-direction: column; gap: 30px; }
      .row { display: flex; align-items: center; gap: 34px; }
      .tile { width: 96px; height: 96px; border-radius: 24px; display: grid; place-items: center; color: #fff;
        background: linear-gradient(140deg, #ff9450, var(--orange)); box-shadow: 0 0 40px rgba(255,112,24,.45), inset 0 1px 0 rgba(255,255,255,.35); }
      .lbl { font-size: 54px; font-weight: 800; letter-spacing: .01em; }

      .card { position: absolute; left: 160px; width: 760px; top: 270px; padding: 40px 40px 36px; border-radius: 34px; text-align: center;
        background: linear-gradient(180deg, #1d1e22, #16171a); border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .avatar { width: 104px; height: 104px; border-radius: 50%; margin: 0 auto 18px; display: grid; place-items: center; background: #2a2c31; color: #b9bcc3; }
      .name { font-size: 50px; font-weight: 750; letter-spacing: -0.01em; }
      .phone { font-size: 32px; color: var(--muted); margin-top: 6px; font-weight: 500; letter-spacing: .04em; }
      .pills { position: relative; height: 56px; margin-top: 22px; }
      .pill { position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; display: inline-flex; align-items: center; gap: 10px;
        font-size: 29px; font-weight: 800; letter-spacing: .08em; padding: 12px 28px; border-radius: 100px; }
      .pill.gray { color: #9a9da4; background: #26282d; }
      .pill.green { color: #3ddc84; background: rgba(34,197,94,.14); border: 1.5px solid rgba(61,220,132,.55); box-shadow: 0 0 30px rgba(61,220,132,.25); }
      .checks { position: absolute; left: 160px; width: 760px; top: 700px; display: flex; flex-direction: column; gap: 18px; }
      .chk { display: flex; align-items: center; gap: 20px; font-size: 36px; font-weight: 600; }
      .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: #0f1012; background: #3ddc84; box-shadow: 0 0 24px rgba(61,220,132,.45); flex: none; }

      .excl { position: absolute; top: 400px; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: 22px; }
      .xt { width: 340px; height: 320px; border-radius: 36px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px;
        background: linear-gradient(180deg, #1f2024, #16171a); border: 1.5px solid #2e3035; box-shadow: 0 30px 80px rgba(0,0,0,.45); }
      .ic.o { color: var(--orange); filter: drop-shadow(0 0 18px rgba(255,112,24,.55)); }
      .xl { font-size: 42px; font-weight: 800; letter-spacing: .01em; white-space: nowrap; }
      .xarrow { color: var(--orange); filter: drop-shadow(0 0 14px rgba(255,112,24,.6)); }
      .xpill { position: absolute; top: 790px; left: 50%; transform: translateX(-50%); display: inline-flex; align-items: center; gap: 14px; white-space: nowrap;
        font-size: 36px; font-weight: 800; letter-spacing: .1em; color: #fff; padding: 18px 38px; border-radius: 100px;
        border: 2px solid var(--orange); background: rgba(255,112,24,.12); box-shadow: 0 0 40px rgba(255,112,24,.35); }

      .chip { position: absolute; top: 300px; left: 50%; margin-left: -415px; width: 830px; display: flex; align-items: center; justify-content: center; gap: 16px;
        padding: 20px 30px; border-radius: 100px; background: rgba(15,16,18,.82); border: 1.5px solid rgba(255,255,255,.14);
        font-size: 29px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); z-index: 25; }
      .chip-ic { color: var(--orange); display: grid; }

      .ctawrap { position: absolute; left: 0; right: 0; top: 1262px; display: flex; justify-content: center; z-index: 26; }
      .btn { display: inline-flex; align-items: center; gap: 14px; white-space: nowrap; font-size: 44px; font-weight: 800; letter-spacing: .04em; color: #fff;
        padding: 26px 52px; border-radius: 100px; background: linear-gradient(180deg, #ff8a3d, var(--orange));
        box-shadow: 0 0 60px rgba(255,112,24,.55), inset 0 1px 0 rgba(255,255,255,.35); }
      .arr { display: grid; }

      .endlogo { position: absolute; left: 250px; width: 580px; top: 690px; }
      .endlogo svg { width: 580px; height: auto; display: block; }
      .endtag { position: absolute; left: 0; right: 0; top: 860px; text-align: center; font-size: 40px; font-weight: 500; color: #c9ccd3; letter-spacing: -0.005em; }
      .endbtn { position: absolute; top: 990px; left: 50%; margin-left: -260px; width: 520px; justify-content: center; }

      .leak { position: absolute; inset: -10%; z-index: 40; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(45% 35% at 30% 45%, rgba(255,140,60,.85), rgba(255,112,24,0) 70%),
                    radial-gradient(40% 30% at 70% 60%, rgba(255,210,150,.7), rgba(255,180,120,0) 70%),
                    radial-gradient(60% 50% at 50% 50%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
    <div id="vwrap">
      <video id="aroll" class="clip" src="aroll.mp4" data-start="0" data-duration="{{TOTAL}}" data-track-index="0" data-has-audio="true" playsinline></video>
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
    build("A")
    build("B")

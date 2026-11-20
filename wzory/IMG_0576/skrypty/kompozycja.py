#!/usr/bin/env python3
"""Generuje ../hf/index.html (HyperFrames) dla rolki "10K vs 100K" (IMG_0576): hook kinetyczny z duzym "100K vs 10K",
napisy slowo po slowie, plansze i nakladki w palecie personal brandu (MARKA = "personal"), plansza koncowa bez CTA
(w nagraniu nie pada wezwanie do komentarza). Dodatkowo ../napisy.srt (frazy napisow, do Premiere / uploadu).

Uzycie: python3 -I kompozycja.py
"""
import html
import json
import os
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Glos w rolce: naturalny dzwiek z mikrofonu po lekkim masteringu z aroll.py (highpass 70 Hz, kompresja 2,5:1, -14 LUFS).
# Jakub 17.11.2026: "za bardzo uzywasz voice enhancer AI, kupilem dobre mikrofony, bez tego albo z duzo mniejszym filtrem".
# Wariant C (Sidon + lancuch radiowy, skrypty/studio.py) zostaje tylko na zyczenie: GLOS = P / "audio/aroll_studio_gleboki.wav".
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
AGENCI = ["artur_avatar.png", "kaja_avatar.png", "weronika_avatar.png", "tymon_avatar.png"]  # z IMG_0529/branding

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
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "cog": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
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
FIX = {"Wiesz": "Wie,", "mi,": "wiem,", "tysi.": "tysięcy."}  # "mi," pada tylko w "uwierz, wiem, co mówię"; "tysi." = sciszona koncowka hooka B

# Frazy napisow po hooku. *slowa* = wyroznienie akcentem. Tekst brany stad, czasy z transkrypcji.
PHRASES = [
    "Większość myśli tak:", "jeśli pierwsze *10 tysięcy*", "zajęło mi *rok,*", "to pierwsze *100 tysięcy*", "zajmie mi *10 lat.*",
    "Przeliczają to", "i *odpuszczają,*", "zanim w ogóle zaczną.",
    "Tylko że to", "*nie rośnie* liniowo.",
    "Na starcie", "nie masz *nic:*", "ani produktu,", "ani procesu,", "ani dowodu,", "że to w ogóle działa.",
    "Pracujesz, pracujesz,", "pracujesz i *bam!*", "Po paru tygodniach", "pierwsza sprzedaż.", "*Pięć stów* wlatuje", "na Twoje konto.",
    "I z tej perspektywy", "*10 tysięcy* to", "totalny *kosmos,*", "a *100 tysięcy*", "to jakiś", "totalny *żart.*",
    "I uwierz, wiem,", "co mówię,", "bo sam zaczynałem", "z *pięcioma stówami*", "w kieszeni.",
    "Ale ktoś, kto dobija", "do pierwszych *10 tysięcy*", "ma już *trzy rzeczy.*",
    "Wie, za co", "ludzie *płacą.*",
    "Wie, skąd biorą", "się *klienci.*",
    "I co najważniejsze,", "ma *proces,*", "który to powtarza.",
    "Tu właśnie", "jest różnica,", "której *5 lat temu*", "jeszcze nie było.",
    "Kiedyś *10 razy* więcej", "przychodu oznaczało", "*10 razy* więcej ludzi.",
    "Dziś powtarzanie", "oddajesz *AI.*",
    "U mnie *setki*", "nowych reklam,", "dla mnie i dla", "każdego z moich klientów", "robi *AI.*",
    "A nie grafik.",
    "I zamiast zatrudniać", "kolejną osobę,", "po prostu dokładamy", "następnych *agentów.*",
    "Na tę chwilę", "w samym adGenie", "jest już ich", "ponad *dwudziestu czterech.*",
    "I przy drodze", "ku pierwszym *10 tysiącom*", "to wcale nie chodzi", "o pieniądze.",
    "Tu chodzi o", "*budowę maszyny.*",
    "A *100 tysięcy*", "to praktycznie", "*ta sama* maszyna,", "której zamiast", "10 razy więcej ludzi", "dałeś po prostu",
    "odpowiednią ilość *AI.*",
    "Więc jeśli jesteś", "na etapie pierwszych", "paru tysięcy,", "nie patrz ku górze,", "ku stu tysiącom,", "tylko",
    "skup się na tym,", "żeby zbudować *proces,*", "który działa *raz.*",
    "Potem po prostu", "daj go *AI*", "do powtarzania", "i skup się na tym,", "żeby pozyskiwać", "*klientów.*",
]


def load_words():
    ws = [[a, b, FIX.get(t, t)] for a, b, t in json.loads((P / "audio/slowa.json").read_text())]
    # "oddajesz AI" whisper slyszy jako "oddaje, że jaj." (AI wymawiane "ej-aj"): 3 tokeny -> 2 slowa
    for k in range(len(ws) - 2):
        if [norm(w[2]) for w in ws[k:k + 3]] == ["oddaje", "że", "jaj"]:
            ws[k:k + 3] = [[ws[k][0], ws[k][1], "oddajesz"], [ws[k + 1][0], ws[k + 2][1], "AI."]]
            break
    # kwestia "ta sama maszyna..." zaczyna sie tuz po wycietym falstarcie i whisper dopisuje na jej poczatku "To"
    # (token 50 ms, w nagraniu go nie ma - kawalki.py od 306.43 slyszy samo "ta sama maszyna")
    for k in range(len(ws) - 1):
        if norm(ws[k][2]) == "to" and norm(ws[k + 1][2]) == "ta" and ws[k][1] - ws[k][0] < 0.08:
            ws[k:k + 2] = [[ws[k][0], ws[k + 1][1], ws[k + 1][2]]]
            break
    return ws


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
    Ws = lambda text, i: W(text, seg(i)["t_in"])[0]  # start slowa szukanego od poczatku kwestii i
    el, js, srt = [], [], []

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1});')
    for e in edl:
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')

    # --- hook kinetyczny (kwestia 0): male slowa fraza po frazie + stale duze "100K vs 10K" (hook B: "10K vs 100K")
    kin_end = seg(1)["t_in"]
    hook = [w for w in words if w[0] < kin_end - 0.02]
    hn = [norm(w[2]) for w in hook]
    if hn[1] == "100":   # A: Pierwsze 100 tysięcy jest 10 razy łatwiejsze niż pierwsze 10 tysięcy złotych w miesiąc.
        assert hn == ["pierwsze", "100", "tysięcy", "jest", "10", "razy", "łatwiejsze", "niż", "pierwsze", "10", "tysięcy",
                      "złotych", "w", "miesiąc"], hn
        chunks = [hook[0:4], hook[4:8], hook[8:11], hook[11:14]]
        big = [("100K", "b acc", hook[1][0]), ("vs", "vs", hook[7][0]), ("10K", "b", hook[9][0])]
    else:                # B: Pierwsze 10 tysięcy w miesiąc jest 10 razy trudniejsze niż pierwsze 100 tysięcy.
        assert hn == ["pierwsze", "10", "tysięcy", "w", "miesiąc", "jest", "10", "razy", "trudniejsze", "niż", "pierwsze",
                      "100", "tysięcy"], hn
        chunks = [hook[0:5], hook[5:9], hook[9:13]]
        big = [("10K", "b", hook[1][0]), ("vs", "vs", hook[9][0]), ("100K", "b acc", hook[11][0])]
    for k, ch in enumerate(chunks):
        start = max(0.0, ch[0][0] - 0.06)
        end = chunks[k + 1][0][0] - 0.06 if k + 1 < len(chunks) else kin_end
        el.append(f'<div id="h{k}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">'
                  f'<div class="kin-s">{"".join(span(w) for w in ch)}</div></div>')
        for i, w in enumerate(ch):
            js.append(f'tl.fromTo("#h{k} .w:nth-child({i + 1})",{{opacity:0,y:18,filter:"blur(8px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0] - 0.04):.3f});')
    b0 = max(0.0, big[0][2] - 0.1)
    el.append(f'<div id="hb" class="kin clip" style="top:1108px" data-start="{b0:.3f}" data-duration="{kin_end - b0:.3f}" data-track-index="7">'
              '<div class="kin-b" style="font-size:132px">'
              + "".join(f'<span class="{cls}" id="hb{i}">{txt}</span>' for i, (txt, cls, _) in enumerate(big)) + "</div></div>")
    for i, (txt, cls, t0) in enumerate(big):
        if cls == "vs":
            js.append(f'tl.fromTo("#hb{i}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},{t0 - 0.04:.3f});')
        else:
            js.append(f'tl.fromTo("#hb{i}",{{opacity:0,scale:1.35,filter:"blur(14px)"}},'
                      f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(b0, t0 - 0.05):.3f});')
    srt.append((0.0, kin_end, " ".join(w[2] for w in hook)))

    # --- napisy slowo po slowie (od kwestii 1)
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
        # kwadraty dekoracyjne u dolu planszy zostaja tylko w palecie adGen; w personal brandzie plansza jest czysta
        sq = ('<div class="sq sq1" data-layout-allow-overflow></div><div class="sq sq2" data-layout-allow-overflow></div>'
              '<div class="sq sq3" data-layout-allow-overflow></div>') if MARKA == "adgen" else ""
        el.append(f'<div id="{pid}" class="panel clip {cls}" data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12 + extend:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div>{sq}{inner}</div>')
        js.append(f'tl.fromTo("#{pid}",{{opacity:0,scale:1.06,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{t_in - 0.12:.3f});')
        d = t_out - t_in
        if sq:
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

    def fade(sel, t, dur=0.25, y=12):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.3f});')

    def blur_in(sel, t):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:1.5,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{t:.3f});')

    def overlay(oid, t_in, t_out, inner, cls, track=5, y_from=-30, style=""):
        st = f' style="{style}"' if style else ""
        el.append(f'<div id="{oid}" class="{cls} clip"{st} data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
        js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.6:.0f},filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.22:.3f});')

    def tiles(tid, cards, t_out, off=False):
        """cards: (ikona, podpis, czas). off=True: szare kafelki z bialym "x" (czego nie ma), inaczej akcent + ptaszek."""
        inner = "".join(
            f'<div class="tcard{" off" if off else ""}" id="{tid}{k}"><div class="tile">{icon(ic, 40)}</div><div class="tlbl">{lbl}</div>'
            f'<span class="tok{" x" if off else ""}">{icon("x" if off else "check", 24)}</span></div>' for k, (ic, lbl, _) in enumerate(cards))
        t0 = cards[0][2] - 0.1
        el.append(f'<div id="{tid}" class="tiles clip" data-start="{t0:.3f}" data-duration="{t_out - t0:.3f}" data-track-index="5">{inner}</div>')
        for k, (_, _, t) in enumerate(cards):
            pop(f"#{tid}{k}", t - 0.08)
        js.append(f'tl.to("#{tid}",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.24:.3f});')

    def chip(cid, ic, text, t_in, t_out, ok=None, t_ok=None, ok_dot="check", track=5, style=""):
        """Chip u gory kadru: kafelek + tekst, opcjonalnie druga czesc w akcencie (wchodzi w t_ok)."""
        tile = icon(ic, 32) if ic in ICON else f'<b class="stepn">{ic}</b>'
        part = ""
        if ok:
            dot = f'<span class="dot sm">{icon(ok_dot, 22)}</span>' if ok_dot else ""
            part = f'<span class="okpart" id="{cid}ok">{dot}{html.escape(ok)}</span>'
        inner = f'<div class="chip2"><span class="tile sm">{tile}</span><span>{html.escape(text)}</span>{part}</div>'
        overlay(cid, t_in, t_out, inner, "chipwrap", track=track, style=style)
        if ok:
            # druga czesc do t_ok ma display:none (pigulka bez pustego ogona); wlaczenie przez set, ruch tylko x/opacity,
            # bo tween wlasciwosci ukladu (szerokosc, margines) nie przechodzi hyperframes check i zacina sie w renderze
            js.append(f'tl.set("#{cid}ok",{{display:"flex"}},{t_ok:.3f});')
            js.append(f'tl.fromTo("#{cid}ok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{t_ok:.3f});')

    # Rysowanie linii: pathLength=1000 i dashoffset 1000 -> 0. Przy skali 0-1 render zaokragla wartosc do calosci
    # i linia wskakuje cala w polowie ruchu (IMG_0576).
    # --- P1: wykres (kwestie 1-3). Wszystko jest w ruchu: osie i siatka rysuja sie na wejsciu, punkt 10K wyskakuje z fala,
    #     prosta rysuje sie z jadaca kropka i odhacza kolejne lata na osi, na "odpuszczaja" caly plan trzesie sie i gasnie
    #     pod znakiem "x", a na "to nie rosnie liniowo" krzywa w akcencie wystrzeliwuje z jadaca glowica i wypelnieniem.
    t1 = Ws("jeśli", 1)
    X0, Y0, X1, Y1 = 70, 560, 840, 80                      # poczatek ukladu i koniec prostej (rok 10, 100K)
    yr = lambda k: (X0 + (X1 - X0) * k / 10, Y0 + (Y1 - Y0) * k / 10)   # punkt prostej dla roku k
    CV = ((70, 560), (400, 556), (540, 470), (600, 62))    # krzywa Beziera "naprawde"

    def bez(u):
        a = [(1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3]
        return sum(a[i] * CV[i][0] for i in range(4)), sum(a[i] * CV[i][1] for i in range(4))

    grid = "".join(f'<path class="gr" id="gr{k}" d="M70,{y} H870"/>' for k, y in enumerate((440, 320, 200, 80)))
    ticks = "".join(f'<path class="tk" id="tk{k}" d="M{yr(k)[0]:.0f},560 V574"/>' for k in range(1, 11))
    inner = ('<div class="p-head ph-a" id="ph1a" style="top:250px">JAK TO LICZĄ</div>'
             '<div class="p-head" id="ph1b" style="top:250px">TO NIE ROŚNIE LINIOWO</div>'
             '<svg class="chart" id="chart" viewBox="0 0 900 620" width="900" height="620"><defs>'
             '<linearGradient id="arg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--accent);stop-opacity:.34"/>'
             '<stop offset="1" style="stop-color:var(--accent);stop-opacity:0"/></linearGradient></defs>'
             f'{grid}<path class="ax" id="ax" pathLength="1000" d="M70,30 V560 H870"/>'
             '<text id="axy" x="92" y="54" font-size="28" font-weight="700" fill="#8a8d94" letter-spacing="2">ZŁ / MIES.</text>'
             '<g id="lin">' + ticks +
             '<text id="tl1" x="147" y="608" font-size="28" font-weight="700" fill="#8a8d94" text-anchor="middle">1</text>'
             '<text id="tl10" x="840" y="608" font-size="28" font-weight="700" fill="#8a8d94" text-anchor="middle">10 lat</text>'
             '<path id="lnl" class="ln-lin" pathLength="1000" d="M70,560 L840,80"/>'
             '<circle id="hl" class="hd-w" cx="70" cy="560" r="10"/>'
             '<circle id="d1r" class="rip" cx="147" cy="512" r="13"/><circle id="d1" cx="147" cy="512" r="13" fill="#fff"/>'
             '<path id="d1l" class="ldr" pathLength="1000" d="M147,494 V458"/>'
             '<text id="d1b" x="104" y="398" font-size="30" font-weight="700" fill="#c9ccd3">1 ROK</text>'
             '<text id="d1a" x="104" y="446" font-size="46" font-weight="850" fill="#fff">10K</text>'
             '<circle id="d2r" class="rip" cx="840" cy="80" r="13"/><circle id="d2" cx="840" cy="80" r="13" fill="#fff"/>'
             '<text id="d2a" x="800" y="86" font-size="46" font-weight="850" fill="#fff" text-anchor="end">100K</text>'
             '<text id="d2b" x="800" y="40" font-size="30" font-weight="700" fill="#c9ccd3" text-anchor="end">10 LAT</text>'
             '<path id="d2s" class="strk" pathLength="1000" d="M686,30 H808"/></g>'
             '<circle id="xr" class="rip" cx="455" cy="320" r="36"/>'
             '<g id="xb"><circle cx="455" cy="320" r="36" fill="#0f1012" stroke="#fff" stroke-width="4"/>'
             '<path d="M441,306 L469,334 M469,306 L441,334" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none"/></g>'
             '<path id="ar" fill="url(#arg)" d="M70,560 C400,556 540,470 600,62 L600,560 Z"/>'
             '<path id="lne" class="ln-exp" pathLength="1000" d="M70,560 C400,556 540,470 600,62"/>'
             '<circle id="der1" class="rip acc" cx="600" cy="62" r="15"/><circle id="der2" class="rip acc" cx="600" cy="62" r="15"/>'
             '<circle id="hd" class="hd-a" cx="70" cy="560" r="12"/>'
             '<circle id="de" cx="600" cy="62" r="15" fill="var(--accent)"/></svg>')
    p1_out = seg(4)["t_in"]
    panel("p1", t1, p1_out, inner)

    def dot(sel, t, ox, oy):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:0.2,svgOrigin:"{ox} {oy}"}},{{opacity:1,scale:1,duration:0.34,ease:"back.out(2.6)"}},{t:.3f});')

    def ripple(sel, t, r0, r1, dur=0.6):
        js.append(f'tl.fromTo("{sel}",{{opacity:0.75,attr:{{r:{r0}}}}},{{opacity:0,attr:{{r:{r1}}},duration:{dur},ease:"power2.out",immediateRender:false}},{t:.3f});')

    def label(sel, t, ox, oy):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:16,scale:0.8,svgOrigin:"{ox} {oy}"}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.9)"}},{t:.3f});')

    # wejscie: osie rysuja sie, siatka wchodzi od dolu, calosc powoli najezdza
    js.append('gsap.set("#ph1b,#hl,#hd,#d1r,#d2r,#xr,#der1,#der2,#ar",{opacity:0});')
    js.append(f'tl.fromTo("#ax",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:0.55,ease:"power2.out"}},{t1 - 0.08:.3f});')
    for k in range(4):
        js.append(f'tl.fromTo("#gr{k}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{t1 + 0.1 + k * 0.07:.3f});')
    js.append(f'tl.fromTo("#axy",{{opacity:0}},{{opacity:1,duration:0.3}},{t1 + 0.3:.3f});')
    js.append(f'tl.fromTo("#chart",{{scale:1,transformOrigin:"50% 60%"}},{{scale:1.05,duration:{p1_out - t1:.3f},ease:"none"}},{t1:.3f});')
    # 10K po roku: punkt z fala, kreska do podpisu, pierwszy rok na osi
    t10 = W("10", t1)[0]
    dot("#d1", t10 - 0.06, 147, 512)
    ripple("#d1r", t10 + 0.02, 13, 52)
    js.append(f'tl.fromTo("#d1l",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:0.2,ease:"power2.out"}},{t10 + 0.08:.3f});')
    label("#d1a", t10 + 0.1, 104, 446)
    js.append(f'tl.fromTo("#tk1,#tl1",{{opacity:0,y:-8}},{{opacity:1,y:0,duration:0.2}},{t10 + 0.05:.3f});')
    label("#d1b", W("rok", t1)[0] - 0.05, 104, 398)
    # prosta do 100K: rysuje sie razem z jadaca kropka, a kazdy miniety rok odhacza kreske na osi
    t_ln = W("pierwsze", W("to", t10)[0])[0]
    t_lat = W("lat", t_ln)[0]
    d_ln = t_lat - t_ln
    js.append(f'tl.fromTo("#lnl",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{d_ln:.3f},ease:"power1.inOut"}},{t_ln:.3f});')
    js.append(f'tl.set("#hl",{{opacity:1}},{t_ln:.3f});')
    js.append(f'tl.fromTo("#hl",{{attr:{{cx:{X0},cy:{Y0}}}}},{{attr:{{cx:{X1},cy:{Y1}}},duration:{d_ln:.3f},ease:"power1.inOut"}},{t_ln:.3f});')
    for k in range(2, 11):
        pr = k / 10  # odwrotnosc power1.inOut: kiedy prosta mija rok k
        tau = (pr / 2) ** 0.5 if pr < 0.5 else 1 - ((1 - pr) / 2) ** 0.5
        js.append(f'tl.fromTo("#tk{k}",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{t_ln + tau * d_ln - 0.03:.3f});')
    label("#d2a", W("100", t_ln)[0] - 0.05, 800, 86)
    js.append(f'tl.to("#hl",{{opacity:0,duration:0.12}},{t_lat - 0.02:.3f});')
    dot("#d2", t_lat - 0.08, 840, 80)
    ripple("#d2r", t_lat, 13, 58)
    label("#d2b", W("10", W("zajmie", t_ln)[0])[0] - 0.05, 800, 40)
    js.append(f'tl.fromTo("#tl10",{{opacity:0,y:-8}},{{opacity:1,y:0,duration:0.2}},{t_lat - 0.1:.3f});')
    # "odpuszczaja": caly plan trzesie sie, gasnie, "10 LAT" przekreslone, znak "x" wbija sie w prosta
    t_odp = Ws("odpuszczają", 2)
    js.append(f'tl.fromTo("#lin",{{x:0}},{{x:9,duration:0.045,ease:"sine.inOut",repeat:7,yoyo:true}},{t_odp - 0.02:.3f});')
    js.append(f'tl.to("#lin",{{opacity:0.3,duration:0.35,ease:"power2.out"}},{t_odp + 0.1:.3f});')
    js.append(f'tl.fromTo("#d2s",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:0.22,ease:"power2.out"}},{t_odp + 0.05:.3f});')
    js.append(f'tl.fromTo("#xb",{{opacity:0,scale:2.6,rotation:-40,svgOrigin:"455 320"}},{{opacity:1,scale:1,rotation:0,duration:0.3,ease:"power4.in"}},{t_odp - 0.12:.3f});')
    js.append(f'tl.fromTo("#xb",{{scale:1,svgOrigin:"455 320"}},{{scale:1.16,duration:0.1,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{t_odp + 0.18:.3f});')
    ripple("#xr", t_odp + 0.18, 36, 110, 0.55)
    # "tylko ze to nie rosnie liniowo": naglowek zmienia sie na akcent, krzywa wystrzeliwuje z jadaca glowica
    t_cv = Ws("tylko", 3)
    d_cv = 1.1
    js.append(f'tl.to("#ph1a",{{opacity:0,y:-18,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_cv - 0.05:.3f});')
    js.append(f'tl.fromTo("#ph1b",{{opacity:0,y:18,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{t_cv + 0.12:.3f});')
    js.append(f'tl.fromTo("#lne",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{d_cv},ease:"power2.in"}},{t_cv + 0.1:.3f});')
    pts = [bez(i / 600) for i in range(601)]               # glowica: te same ulamki dlugosci co power2.in w GSAP (p = tau^3)
    cum = [0.0]
    for (xa, ya), (xb_, yb_) in zip(pts, pts[1:]):
        cum.append(cum[-1] + ((xb_ - xa) ** 2 + (yb_ - ya) ** 2) ** 0.5)
    N = 22
    js.append(f'tl.set("#hd",{{opacity:1}},{t_cv + 0.1:.3f});')
    for i in range(1, N + 1):
        target = (i / N) ** 3 * cum[-1]
        j = next(k for k, c in enumerate(cum) if c >= target - 1e-9)
        js.append(f'tl.to("#hd",{{attr:{{cx:{pts[j][0]:.1f},cy:{pts[j][1]:.1f}}},duration:{d_cv / N:.4f},ease:"none"}},{t_cv + 0.1 + (i - 1) * d_cv / N:.4f});')
    t_end = t_cv + 0.1 + d_cv
    js.append(f'tl.fromTo("#ar",{{opacity:0}},{{opacity:1,duration:0.4,ease:"power2.out"}},{t_end - 0.03:.3f});')
    js.append(f'tl.to("#hd",{{opacity:0,duration:0.1}},{t_end:.3f});')
    dot("#de", t_end - 0.06, 600, 62)
    ripple("#der1", t_end, 15, 80, 0.6)
    ripple("#der2", t_end + 0.16, 15, 120, 0.7)
    js.append(f'tl.fromTo("#lne",{{strokeWidth:10}},{{strokeWidth:15,duration:0.16,ease:"power2.out",yoyo:true,repeat:1}},{t_end:.3f});')

    # --- kafelki "na starcie nie masz nic" (kwestia 4): produkt / proces / dowod z bialym "x"
    tiles("nic", [("box", "Produkt", Ws("produktu", 4)), ("repeat", "Proces", Ws("procesu", 4)),
                  ("trend", "Dowód,<br>że działa", Ws("dowodu", 4))], seg(5)["t_in"] - 0.02, off=True)

    # --- powiadomienie "pierwsza sprzedaz, +500 zl" (kwestia 5) - pogladowe, kwota z tego, co mowi
    inner = (f'<div class="tile" style="width:84px;height:84px;border-radius:22px">{icon("wallet", 44)}</div><div class="nt-body">'
             '<div class="nt-top"><b>Twoje konto</b><span class="nt-time">teraz</span></div>'
             '<div class="nt-title">Pierwsza sprzedaż</div><div class="nt-items"><span class="nti" id="nti0">+ 500 zł</span></div></div>')
    overlay("nt", Ws("pierwsza", 5) - 0.12, seg(6)["t_in"] - 0.02, inner, "notif", y_from=-60)
    pop("#nti0", Ws("pięć", 5) - 0.06)

    # --- P2: skala z perspektywy 500 zl (kwestia 6): 500 zl vs 10 000 (kosmos) vs 100 000 (zart), paski w proporcji
    t2 = Ws("10", 6)
    inner = ('<div class="p-head" style="top:330px">Z PERSPEKTYWY 500 ZŁ</div><div class="bars">'
             '<div class="brow" id="b0"><div class="bhead"><span class="bl">TY</span><span class="bv o">500 zł</span></div>'
             '<div class="btrack"><div class="bfill accent" id="b0f" style="width:0.5%;min-width:14px"></div></div></div>'
             '<div class="brow" id="b1"><div class="bhead"><span class="bl">10 000 zł</span><span class="bv" id="b1v">KOSMOS</span></div>'
             '<div class="btrack"><div class="bfill gray" id="b1f" style="width:10%"></div></div></div>'
             '<div class="brow" id="b2"><div class="bhead"><span class="bl">100 000 zł</span><span class="bv" id="b2v">ŻART</span></div>'
             '<div class="btrack"><div class="bfill gray" id="b2f"></div></div></div></div>')
    panel("p2", t2, seg(7)["t_in"], inner)
    pop("#b0", t2 - 0.08)
    pop("#b1", t2 + 0.1)
    js.append(f'tl.fromTo("#b1f",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{t2 + 0.2:.3f});')
    fade("#b1v", W("kosmos", t2)[0] - 0.05)
    t100 = W("100", t2)[0]
    pop("#b2", t100 - 0.08)
    js.append(f'tl.fromTo("#b2f",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out"}},{t100:.3f});')
    fade("#b2v", W("żart", t100)[0] - 0.05)

    # --- chip "moj start: 500 zl" (kwestia 7)
    chip("st", "wallet", "MÓJ START", Ws("sam", 7) - 0.1, seg(8)["t_in"] - 0.02, ok="500 ZŁ", t_ok=Ws("pięcioma", 7) - 0.05, ok_dot=None)

    # --- kafelki "trzy rzeczy" (kwestie 9-11): to samo miejsce co "nic", teraz z ptaszkami
    tiles("ma", [("wallet", "Wie, za co<br>ludzie płacą", Ws("wie", 9)), ("users", "Wie, skąd<br>biorą się klienci", Ws("wie", 10)),
                 ("repeat", "Ma proces,<br>który to powtarza", Ws("proces", 11))], seg(12)["t_in"] - 0.02)

    # --- P3: kiedys 10x przychodu = 10x ludzi, dzis powtarzanie robi AI (kwestie 13-14)
    s13 = seg(13)
    ppl = "".join(f'<span class="pp" id="pp{k}">{icon("user", 54)}</span>' for k in range(10))
    inner = ('<div class="p-head" style="top:270px">10× WIĘCEJ PRZYCHODU</div>'
             f'<div class="cmp" id="cA" style="top:360px"><div class="cmp-k">KIEDYŚ</div><div class="cmp-r"><div class="ppl">{ppl}</div>'
             '<div class="cmp-v" id="cAv">10× LUDZI</div></div></div>'
             '<div class="cmp now" id="cB" style="top:650px"><div class="cmp-k">DZIŚ</div><div class="cmp-r">'
             f'<div class="cmp-v">POWTARZANIE</div><div class="cmp-ai" id="cBai"><span class="tile">{icon("sparkles", 46)}</span>AI</div></div></div>')
    t3 = Ws("oznaczało", 13)
    panel("p3", t3, seg(15)["t_in"], inner)
    pop("#cA", t3 + 0.02)
    t_pp = t3 + 0.25
    for k in range(10):
        js.append(f'tl.fromTo("#pp{k}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.2,ease:"back.out(2)"}},{t_pp - 0.05 + k * 0.06:.3f});')
    fade("#cAv", Ws("ludzi", 13) - 0.05)
    pop("#cB", Ws("dziś", 14) - 0.08)
    js.append(f'tl.fromTo("#cBai",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{Ws("AI", 14) - 0.05:.3f});')

    # --- chip "setki reklam robi AI" (kwestie 15-16)
    chip("rek", "megaphone", "SETKI REKLAM", Ws("setki", 15) - 0.1, seg(17)["t_in"] - 0.02, ok="ROBI AI", t_ok=Ws("robi", 15) - 0.05)

    # --- chip "zamiast etatu: kolejny agent" (kwestia 17, pierwsze zdanie), potem P4: 24+ agentow
    t4 = W("na", Ws("agentów", 17))[0]
    chip("et", "user", "ZAMIAST ETATU", Ws("zamiast", 17) - 0.1, t4 - 0.16, ok="KOLEJNY AGENT", t_ok=Ws("dokładamy", 17) - 0.05, ok_dot="plus")
    inner = ('<div class="p-head" style="top:250px">NA TĘ CHWILĘ</div><div class="avs">'
             + "".join(f'<img id="av{k}" src="{a}" alt="">' for k, a in enumerate(AGENCI)) + "</div>"
             '<div class="big30" id="n24" style="top:570px">24+</div><div class="big30s" id="n24s" style="top:815px">AGENTÓW AI</div>')
    panel("p4", t4, seg(18)["t_in"], inner)
    for k in range(len(AGENCI)):
        pop(f"#av{k}", t4 + 0.02 + k * 0.09)
    t24 = W("dwudziestu", t4)[0]
    blur_in("#n24", t24 - 0.05)
    pop("#n24s", t24 + 0.22)

    # --- chip "pierwsze 10K = budowa maszyny" (kwestia 19)
    chip("bm", "cog", "PIERWSZE 10K", Ws("tu", 19) - 0.1, seg(20)["t_in"] - 0.02, ok="BUDOWA MASZYNY", t_ok=Ws("budowę", 19) - 0.05, ok_dot=None)

    # --- P5: ta sama maszyna, zamiast 10x ludzi - AI (kwestia 21)
    t5 = Ws("ta", 21)
    inner = (f'<div class="mach" id="mach">{icon("cog", 124)}</div><div class="mach-l" id="machl">TA SAMA MASZYNA</div>'
             '<div class="inv" style="top:735px"><div class="pill off big" id="pl">10× WIĘCEJ LUDZI<span class="strike" id="pls"></span></div></div>'
             f'<div class="inv" style="top:862px"><div class="pill ok big" id="pa">{icon("sparkles", 40)} AI</div></div>')
    panel("p5", t5, seg(22)["t_in"], inner)
    pop("#mach", t5 - 0.02)
    js.append(f'tl.fromTo("#mach svg",{{rotation:0}},{{rotation:140,duration:{seg(22)["t_in"] - t5:.3f},ease:"none"}},{t5:.3f});')
    pop("#machl", Ws("sama", 21) - 0.05)
    t_l = W("10", Ws("zamiast", 21))[0]
    pop("#pl", t_l - 0.06)
    js.append(f'tl.fromTo("#pls",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power2.out"}},{Ws("dałeś", 21) - 0.05:.3f});')
    js.append(f'tl.to("#pl",{{opacity:0.55,duration:0.3}},{Ws("dałeś", 21) + 0.1:.3f});')
    pop("#pa", W("AI", Ws("ilość", 21))[0] - 0.06)

    # --- dwa kroki na koniec (kwestie 23-24): 1 zbuduj proces, 2 daj go AI
    chip("k1", "1", "ZBUDUJ PROCES", Ws("zbudować", 23) - 0.1, end_card_in + 0.1)
    chip("k2", "2", "DAJ GO AI", Ws("daj", 24) - 0.1, end_card_in + 0.1, track=7, style="top:262px")

    # --- plansza koncowa: bez logo (personal brand) i bez CTA, bo w nagraniu nie pada wezwanie do komentarza
    inner = (f'<div class="endbig"><span class="b" id="eb0">10K</span><span class="arr" id="eb1">{icon("arrow", 116)}</span>'
             '<span class="b acc" id="eb2">100K</span></div>'
             '<div class="endtxt" id="endtxt" style="top:770px">Zbuduj proces. Daj go AI.</div>'
             '<div class="endsub" id="endsub" style="top:862px">Jakub Derda</div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    blur_in("#eb0", end_card_in + 0.05)
    js.append(f'tl.fromTo("#eb1",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{end_card_in + 0.22:.3f});')
    blur_in("#eb2", end_card_in + 0.36)
    pop("#endtxt", end_card_in + 0.6)
    pop("#endsub", end_card_in + 0.75)

    page = TEMPLATE.replace("    </style>", EXTRA_CSS + "    </style>").replace("{{TOTAL}}", f"{total:.3f}") \
        .replace("{{ELEMENTS}}", "\n    ".join(el)).replace("{{JS}}", "\n      ".join(js))
    page = kolory(page)
    out = P / "hf/index.html"
    out.write_text(page)
    glos = P / "hf/glos.wav"
    glos.unlink(missing_ok=True)
    # Glos naturalny ma po loudnorm szczyt -1,5 dBFS, ale kodowanie AAC w renderze dodaje ok. 0,2 dB (wyszlo -1,3).
    # Limiter na -1,8 dBFS (0,81) rusza tylko pojedyncze szczyty, glosnosc zostaje na -14 LUFS.
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(GLOS), "-af",
                    "alimiter=limit=0.81:attack=1:release=40:level=false", "-c:a", "pcm_s16le", str(glos)], check=True)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | {len(phrases)} fraz, {len(el)} elementow, {total:.2f}s, plansza koncowa od {end_card_in:.2f}")
    for ph in phrases:
        print(f"   {ph[0][0]:6.2f} " + " ".join(("*" + w[2] + "*") if w[3] else w[2] for w in ph))


# Dodatki do CSS szablonu dla tej rolki (wspolny CSS z IMG_0526 zostaje bez zmian). Kolory tylko przez zmienne palety.
EXTRA_CSS = r"""
      .kin-b .b.acc { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .kin-b .vs { display: inline-block; align-self: center; font-size: .36em; font-weight: 700; letter-spacing: .02em; color: #c9ccd3; padding: 0 .12em;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.55)); }
      .chart { position: absolute; left: 90px; top: 330px; width: 900px; height: 620px; overflow: visible; }
      .chart text { font-family: "Inter Tight", sans-serif; }
      .ax { stroke: rgba(255,255,255,.22); stroke-width: 3; fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1000; }
      .gr { stroke: rgba(255,255,255,.07); stroke-width: 2; fill: none; stroke-dasharray: 6 12; }
      .tk { stroke: rgba(255,255,255,.5); stroke-width: 3; fill: none; stroke-linecap: round; }
      .ldr { stroke: rgba(255,255,255,.55); stroke-width: 3; fill: none; stroke-linecap: round; stroke-dasharray: 1000; }
      .rip { fill: none; stroke: #fff; stroke-width: 4; }
      .rip.acc { stroke: var(--accent); }
      .hd-w { fill: #fff; filter: drop-shadow(0 0 10px rgba(255,255,255,.9)); }
      .hd-a { fill: #fff; filter: drop-shadow(0 0 14px rgba(var(--accent-rgb),1)) drop-shadow(0 0 30px rgba(var(--accent-rgb),.8)); }
      .p-head.ph-a { color: #c9ccd3; }
      .ln-lin { stroke: #c9ccd3; stroke-width: 7; fill: none; stroke-linecap: round; stroke-dasharray: 1000; }
      .strk { stroke: #fff; stroke-width: 5; fill: none; stroke-linecap: round; stroke-dasharray: 1000; }
      .ln-exp { stroke: var(--accent); stroke-width: 10; fill: none; stroke-linecap: round; stroke-dasharray: 1000; filter: drop-shadow(0 0 14px rgba(var(--accent-rgb),.7)); }
      .tcard.off .tile { background: #2a2c31; color: #9a9da5; box-shadow: none; }
      .tok.x { background: #fff; box-shadow: 0 0 20px rgba(255,255,255,.3); }
      .stepn { font-size: 32px; font-weight: 900; line-height: 1; }
      .chip2 .okpart { display: none; white-space: nowrap; }
      .cmp { position: absolute; left: 140px; width: 800px; border-radius: 34px; padding: 26px 34px 30px; background: linear-gradient(180deg, #1d1e22, #16171a);
        border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .cmp.now { border: 2px solid rgba(var(--accent-rgb),.85); box-shadow: 0 0 60px rgba(var(--accent-rgb),.22), 0 30px 80px rgba(0,0,0,.5); }
      .cmp-k { font-size: 30px; font-weight: 800; letter-spacing: .14em; color: #8a8d94; }
      .cmp.now .cmp-k { color: var(--accent); }
      .cmp-r { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-top: 18px; }
      .cmp-v { font-size: 52px; font-weight: 850; letter-spacing: -0.01em; white-space: nowrap; }
      .ppl { display: grid; grid-template-columns: repeat(5, 54px); gap: 8px 12px; color: #c9ccd3; }
      .pp { display: block; }
      .cmp-ai { display: flex; align-items: center; gap: 18px; font-size: 76px; font-weight: 900; letter-spacing: -0.02em; color: var(--accent); }
      .avs { position: absolute; left: 0; right: 0; top: 340px; display: flex; justify-content: center; }
      .avs img { width: 170px; height: 170px; border-radius: 50%; object-fit: cover; border: 5px solid var(--accent); margin-left: -26px;
        box-shadow: 0 12px 34px rgba(0,0,0,.55); background: #1b1c20; }
      .avs img:first-child { margin-left: 0; }
      .mach { position: absolute; left: 50%; margin-left: -110px; top: 320px; width: 220px; height: 220px; border-radius: 54px; display: grid; place-items: center;
        color: var(--on-accent); background: linear-gradient(140deg, var(--accent-hi), var(--accent));
        box-shadow: 0 0 80px rgba(var(--accent-rgb),.45), inset 0 2px 0 rgba(255,255,255,.35); }
      .mach-l { position: absolute; left: 0; right: 0; top: 592px; text-align: center; font-size: 60px; font-weight: 850; letter-spacing: .01em; }
      .pill.big { font-size: 42px; padding: 18px 40px; gap: 14px; }
      .pill.off { position: relative; color: #c9ccd3; background: #1d1e22; border: 1.5px solid #34363d; }
      .pill.off .strike { position: absolute; left: 22px; right: 22px; top: 50%; height: 5px; margin-top: -2px; border-radius: 3px; background: #fff; transform-origin: left center; }
      .endbig { position: absolute; left: 0; right: 0; top: 560px; display: flex; justify-content: center; align-items: center; gap: .16em;
        font-size: 150px; font-weight: 900; letter-spacing: -0.04em; line-height: 1; }
      .endbig .b { display: inline-block; background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .endbig .b.acc { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .endbig .arr { display: grid; place-items: center; color: var(--accent); }
"""


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

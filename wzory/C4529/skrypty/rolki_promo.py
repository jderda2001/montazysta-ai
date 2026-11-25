#!/usr/bin/env python3
"""Trzy pionowe rolki promocyjne z odcinka (zasada: long-form > 10 min => 3 rolki po 10-15 s, razem z odcinkiem).
Styl rolek z IMG_0526: szablon CSS/GSAP i napisy z skrypty/rolka_szablon.py (= skill scripts/kompozycja.py).

Kazda rolka to fragmenty OSI ODCINKA (SEGS: od, do, ujecia). Ciecia leza w pauzach (minimum obwiedni glosu C),
sprawdzone transkrypcja kawalkow bez promptu (bez "Eee", bez urwanych slow).
- obraz: prosto z IMG_0529.MOV (4K 60p) przez aroll/edl.json (v_in ujecia odcinka), kadr 9:16 pod twarz
  (srodek x per ujecie, twarz chodzi 1940-2320 px), grading jak w odcinku, delikatny najazd w HyperFrames;
- glos: C z odcinka (audio/aroll_studio_gleboki.wav), 8 ms fade na kazdym cieciu, -14 LUFS, limiter -2,5 dBFS
  (po AAC szczyt <= -1,5);
- napisy: slowa z analiza/napisy_slowa.json (poprawiony tekst odcinka), czasy przeliczone na os rolki.

Uzycie: uv run --no-project --with numpy python3 -I rolki.py [1 2 3]
Wynik:  ../rolki/rN/hf/{index.html,aroll.mp4,glos.wav} + ../rolki/rN/napisy.srt
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import wave
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SK = Path(__file__).resolve().parent
VIDEO = Path.home() / "Downloads/IMG_0529.MOV"
GLOS = P / "audio/aroll_studio_gleboki.wav"
OUT = P / "rolki"
FPS = 30
END_HOLD = 2.5
FADE = 0.008
GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
FR = {"W": (1215, 2160, 0), "M": (1056, 1878, 40), "C": (935, 1662, 100)}  # (szer, wys, y) na zrodle 3840x2160
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
TITLE = "Zautomatyzowany dział growth"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


SZ = load("rolka_szablon", SK / "rolka_szablon.py")
SZ.ICON.update({
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>'
              '<path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>'
              '<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
})
icon, norm, span, srt_time = SZ.icon, SZ.norm, SZ.span, SZ.srt_time
PLAY = ('<svg width="150" height="150" viewBox="0 0 24 24"><path d="M8 5.14v13.72a1 1 0 0 0 1.52.85l10.6-6.86'
        'a1 1 0 0 0 0-1.7L9.52 4.29A1 1 0 0 0 8 5.14z" style="fill:var(--on-accent)"/></svg>')
END_INNER = (f'<div class="playb" id="bub">{PLAY}</div>'
             '<div class="endtxt" id="endtxt">Cały odcinek na YouTube</div>'
             f'<div class="endsub" id="endsub">{html.escape(TITLE)}</div>')

# Ujecie: (od_w_odcinku albo None = start fragmentu, kadr, srodek_x twarzy na zrodle 4K)
REELS = {
    1: {"segs": [(0.02, 1.75, [(None, "C", 1944)]),            # Zautomatyzowalem caly dzial growth.
                 (41.37, 44.97, [(None, "W", 2160)]),          # Zeszlismy z parunastu etatow do doslownie dwoch.
                 (82.17, 86.60, [(None, "M", 2160)])],         # Przychody razy 2,5 do przodu, ponad, a zespol 3x mniejszy.
        "hook": [(2, 2, 0, True, ["DZIAŁ", "GROWTH"]), (2, 1, 1, False, ["PARUNASTU"]), (2, 1, 0, True, ["DWÓCH"])],
        "hook_segs": 2,
        "phrases": ["Przychody *razy 2,5*", "do przodu, ponad,", "a zespół *trzykrotnie* mniejszy."],
        "fix_last": None},
    2: {"segs": [(529.58, 532.32, [(None, "C", 2210)]),        # Czego AI nie zrobi?
                 (548.16, 551.77, [(None, "W", 2260)]),        # Ten bot, ten agent nie zamknie sprzedazy za nas.
                 (618.62, 624.61, [(None, "W", 2110), (622.40, "C", 2110), (623.73, "M", 2050)])],
        "hook": [(1, 3, 0, True, ["AI", "NIE", "ZROBI?"])],
        "hook_segs": 1,
        "phrases": ["Ten bot, ten agent", "*nie zamknie* sprzedaży", "za nas.", "AI nam jeszcze",
                    "*nie zadzwoni* do klienta", "i *nie umówi* spotkania.", "Już tutaj wiem,", "że będzie *fala krytyki…*"],
        "fix_last": "krytyki…"},
    3: {"segs": [(774.54, 779.04, [(None, "C", 2290)]),        # 24 agentow, ktorzy kazdy zastepuje ... osobe fizyczna.
                 (789.40, 796.52, [(None, "W", 2240)])],       # Z tym, ze Tobie na start ... plan za 30 dolarow wystarczy,
        "hook": [(0, 2, 3, True, ["24", "AGENTÓW"]), (2, 2, 0, False, ["OSOBĘ", "FIZYCZNĄ"])],
        "hook_segs": 1,
        "phrases": ["Z tym, że Tobie", "*na start,*", "do takiego testowania,", "klikania, to w zupełności", "ten plan",
                    "za *30 dolarów*", "wystarczy."],
        "fix_last": "wystarczy."},
}


# ---------------------------------------------------------------- os czasu rolki
def timeline(segs):
    shots, bounds, R = [], [], 0.0
    for a, b, subs in segs:
        for k, (t, fr, cx) in enumerate(subs):
            s0 = a if t is None else t
            s1 = subs[k + 1][0] if k + 1 < len(subs) else b
            shots.append({"l0": s0, "l1": s1, "r0": R + (s0 - a), "fr": fr, "cx": cx})
        bounds.append((a, b, R))
        R += b - a
    return shots, bounds, R


# ---------------------------------------------------------------- obraz
def video(d, shots, speech_end, total):
    edl = json.loads((P / "aroll/edl.json").read_text())
    parts = []
    for k, sh in enumerate(shots):
        last = k == len(shots) - 1
        for e in edl:
            a, b = max(sh["l0"], e["t_in"]), min(sh["l1"], e["t_out"] + e.get("video_extra", 0.0))
            if b - a < 1e-4:
                continue
            r = sh["r0"] + (a - sh["l0"])
            dur = b - a + (END_HOLD if last and b >= sh["l1"] - 1e-4 else 0.0)  # pod plansza koncowa zrodlo plynie dalej
            w, h, y = FR[sh["fr"]]
            x = int(min(max(0, sh["cx"] - w / 2), 3840 - w))
            f0 = round(r * FPS)  # pierwsza klatka kawalka: zrodlo z dokladnie jej czasu (bez bledu zaokraglenia do klatki)
            parts.append({"v0": round(e["v_in"] + (a - e["t_in"]) + (f0 / FPS - r), 4), "f0": f0,
                          "f1": round((r + dur) * FPS), "crop": (w, h, x, y)})
    nf = round(total * FPS)
    parts[-1]["f1"] = nf
    for p, q in zip(parts, parts[1:]):
        assert p["f1"] == q["f0"], (p, q)
    key = hashlib.md5(json.dumps([parts, GRADE, "x264-crf14"]).encode()).hexdigest()[:10]
    out = d / "hf/aroll.mp4"
    stamp = d / "aroll.key"
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return parts
    tmp = d / "kawalki"
    tmp.mkdir(exist_ok=True)
    files = []
    for i, p in enumerate(parts):
        w, h, x, y = p["crop"]
        vf = f"crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{GRADE},fps={FPS},format=yuv420p,setsar=1"
        f = tmp / f"k{i:02d}.mp4"
        subprocess.run(FF + ["-hwaccel", "videotoolbox", "-ss", f"{p['v0']:.4f}", "-i", str(VIDEO), "-vf", vf,
                             "-frames:v", str(p["f1"] - p["f0"]), "-r", str(FPS), "-c:v", "libx264", "-preset", "slow",
                             "-crf", "14", "-profile:v", "high", "-pix_fmt", "yuv420p", "-color_range", "tv",
                             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an", str(f)],
                       check=True)
        files.append(f)
    lst = tmp / "lista.txt"
    lst.write_text("".join(f"file '{f}'\n" for f in files))
    subprocess.run(FF + ["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out)],
                   check=True)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_packets", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
    assert n == nf, f"aroll.mp4: {n} klatek zamiast {nf}"
    for f in files:
        f.unlink()
    lst.unlink()
    tmp.rmdir()
    stamp.write_text(key)
    return parts


# ---------------------------------------------------------------- dzwiek
def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))


def audio(d, segs, total):
    out = d / "hf/glos.wav"
    stamp = d / "glos.key"
    key = hashlib.md5(json.dumps([[s[:2] for s in segs], total, FADE, "lim-0.7499"]).encode()).hexdigest()[:10]
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return loudness(out)
    with wave.open(str(GLOS)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float32) / 32768
    nf = int(FADE * sr)
    ramp = (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, nf)))[:, None]
    parts = []
    for a, b, _ in segs:
        y = x[int(round(a * sr)):int(round(b * sr))].copy()
        y[:nf] *= ramp
        y[-nf:] *= ramp[::-1]
        parts.append(y)
    y = np.concatenate(parts)
    y = np.concatenate([y, np.zeros((int(round(total * sr)) - len(y), ch), np.float32)])
    raw = d / "glos_surowy.wav"
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    gain = -14.0 - loudness(raw)[0]
    for _ in range(3):
        subprocess.run(FF + ["-i", str(raw), "-af", f"volume={gain:.3f}dB,alimiter=limit=0.7499:attack=1:release=60:"
                             "level=false:latency=true", "-c:a", "pcm_s24le", str(out)], check=True)
        lu, tp = loudness(out)
        if abs(lu + 14.0) <= 0.04:
            break
        gain += -14.0 - lu
    raw.unlink()
    stamp.write_text(key)
    return lu, tp


# ---------------------------------------------------------------- slowa
def words(bounds, cfg):
    src = json.loads((P / "analiza/napisy_slowa.json").read_text())
    ws = []
    for a, b, r0 in bounds:
        first = True
        for w in src:
            if w["b"] > a + 0.05 and w["a"] < b - 0.05:
                t = w["t"]
                if first and t[:1].islower():
                    t = t[:1].upper() + t[1:]
                first = False
                ws.append([round(max(w["a"], a) - a + r0, 3), round(min(w["b"], b) - a + r0, 3), t])
    if cfg["fix_last"]:
        ws[-1][2] = cfg["fix_last"]
    return ws


def manual_group(ws, phrases_spec):
    phrases, k = [], 0
    for ph in phrases_spec:
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


# ---------------------------------------------------------------- kompozycja
class Comp:
    def __init__(self, ws, total):
        self.ws, self.total = ws, total
        self.el, self.js, self.srt = [], [], []
        self.n_leak = 0

    def W(self, text, after=0.0):
        for a, b, t in self.ws:
            if a >= after - 1e-6 and norm(t) == norm(text):
                return a, b
        raise SystemExit(f"Nie znaleziono slowa: {text} po {after}")

    def leak(self, t):
        lid = f"lk{self.n_leak}"
        self.n_leak += 1
        self.el.append(f'<div id="{lid}" class="leak clip" data-layout-ignore data-start="{t - 0.22:.3f}" data-duration="0.55" data-track-index="8"></div>')
        self.js.append(f'tl.fromTo("#{lid}",{{opacity:0,xPercent:-18}},{{opacity:1,xPercent:0,duration:0.2,ease:"power2.out"}},{t - 0.22:.3f});')
        self.js.append(f'tl.to("#{lid}",{{opacity:0,xPercent:16,duration:0.3,ease:"power2.in"}},{t - 0.02:.3f});')

    def panel(self, pid, t_in, t_out, inner, track=2, leak_in=True, leak_out=True, cls="", fade_out=True):
        # Kwadraty dekoracyjne u dolu planszy zostaja tylko w palecie adGen. W personal brandzie plansza jest czysta:
        # Jakub o mietowych kwadratach (IMG_0576, 17.11.2026): "nie podoba mi sie to".
        sq = ('<div class="sq sq1" data-layout-allow-overflow></div><div class="sq sq2" data-layout-allow-overflow></div>'
              '<div class="sq sq3" data-layout-allow-overflow></div>') if SZ.MARKA == "adgen" else ""
        self.el.append(f'<div id="{pid}" class="panel clip {cls}" data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12:.3f}" data-track-index="{track}">'
                       f'<div class="pbg"></div>{sq}{inner}</div>')
        self.js.append(f'tl.fromTo("#{pid}",{{opacity:0,scale:1.06,filter:"blur(18px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.32,ease:"power3.out"}},{t_in - 0.12:.3f});')
        d = t_out - t_in
        if sq:
            self.js.append(f'tl.fromTo("#{pid} .sq1",{{rotation:-14,y:60}},{{rotation:-6,y:0,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            self.js.append(f'tl.fromTo("#{pid} .sq2",{{rotation:18,y:40}},{{rotation:9,y:-20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            self.js.append(f'tl.fromTo("#{pid} .sq3",{{rotation:8}},{{rotation:20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        if leak_in:
            self.leak(t_in)
        if t_out < self.total - 0.1 and fade_out:
            self.js.append(f'tl.to("#{pid}",{{opacity:0,scale:1.04,filter:"blur(14px)",duration:0.18,ease:"power2.in"}},{t_out - 0.18:.3f});')
            if leak_out:
                self.leak(t_out)

    def pop(self, sel, t, extra=""):
        self.js.append(f'tl.fromTo("{sel}",{{opacity:0,y:26,scale:0.94{extra}}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')

    def blur_in(self, sel, t, scale=1.5):
        self.js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:{scale},filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{t:.3f});')

    def overlay(self, oid, t_in, t_out, inner, cls, track=5, y_from=-30):
        self.el.append(f'<div id="{oid}" class="{cls} clip" data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        self.js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
        self.js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.6:.0f},filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.22:.3f});')

    def kinetic(self, hook_words, parts, kin_end):
        """parts: (ile_malych, ile_duzych, ile_malych_po, akcentem, tekst_duzych) - jak w IMG_0526."""
        groups, k = [], 0
        for ns, nb, na, akcent, big_txt in parts:
            groups.append((hook_words[k:k + ns], hook_words[k + ns:k + ns + nb], hook_words[k + ns + nb:k + ns + nb + na],
                           akcent, big_txt))
            k += ns + nb + na
        assert k == len(hook_words), (k, [w[2] for w in hook_words])
        for i, (small, big, after, akcent, big_txt) in enumerate(groups):
            first = (small + big + after)[0]
            start = 0.0 if i == 0 else max(0.0, first[0] - 0.06)
            nxt = groups[i + 1] if i + 1 < len(groups) else None
            end = (nxt[0] + nxt[1] + nxt[2])[0][0] - 0.06 if nxt else kin_end
            # zmierzone: wersaliki Inter Tight 800 to ok. 0,63 rozmiaru na znak; szerokosc ze strefy bezpiecznej
            # szablonu (KIN_W = 620 px), zeby haslo nie wchodzilo pod przyciski Instagrama
            size = min(132, int(getattr(SZ, "KIN_W", 620) / (len(" ".join(big_txt)) * 0.63)))
            sid = f"k{i}"
            self.el.append(
                f'<div id="{sid}" class="kin clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="3">'
                f'<div class="kin-s">{"".join(span(w) for w in small)}</div>'
                f'<div class="kin-b{" accent" if akcent else ""}" style="font-size:{size}px">'
                + "".join(f'<span class="b">{html.escape(t)}</span>' for t in big_txt) + "</div>"
                + (f'<div class="kin-s kin-t">{"".join(span(w) for w in after)}</div>' if after else "") + "</div>")
            for j, w in enumerate(small):
                self.js.append(f'tl.fromTo("#{sid} .kin-s:not(.kin-t) .w:nth-child({j + 1})",{{opacity:0,y:18,filter:"blur(8px)"}},'
                               f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{max(start, w[0] - 0.04):.3f});')
            # duze slowa: przy wiekszej liczbie niz tekstow (np. "dzial growth" -> 2 bloki) i odwrotnie licz po indeksie
            for j in range(len(big_txt)):
                w = big[min(j, len(big) - 1)]
                self.js.append(f'tl.fromTo("#{sid} .kin-b .b:nth-child({j + 1})",{{opacity:0,scale:1.35,filter:"blur(14px)"}},'
                               f'{{opacity:1,scale:1,filter:"blur(0px)",duration:0.26,ease:"power3.out"}},{max(start, w[0] - 0.05):.3f});')
            for j, w in enumerate(after):
                self.js.append(f'tl.fromTo("#{sid} .kin-t .w:nth-child({j + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                               f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.18,ease:"power2.out"}},{w[0] - 0.04:.3f});')
            self.srt.append((start, end, " ".join(w[2] for w in small + big + after)))

    def captions(self, phrases, kin_end, end_card_in):
        for i, ph in enumerate(phrases):
            start = max(ph[0][0] - 0.06, kin_end if i == 0 else 0)
            nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
            end = min(nxt, ph[-1][1] + 0.6, end_card_in)
            cid = f"c{i}"
            txt = " ".join(w[2] for w in ph)
            fs = min(66, int(getattr(SZ, "CAP_W", 620) / (len(txt) * 0.54)))  # strefa bezpieczna: frazy do ok. 20 znakow
            self.el.append(f'<div id="{cid}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                           f'data-track-index="4" style="font-size:{fs}px">' + " ".join(span(w) for w in ph) + "</div>")
            for j, w in enumerate(ph):
                self.js.append(f'tl.fromTo("#{cid} .w:nth-child({j + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                               f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{max(start, w[0] - 0.03):.3f});')
            self.srt.append((start, end, txt))

    def end_card(self, t_in, host=None, hide=()):
        """Plansza koncowa promo: przycisk play + "Caly odcinek na YouTube". Bez logo (personal brand).
        host: plansza, na ktorej juz jest END_INNER (rolka konczy sie plansza) - jej tresc znika, a w tym samym
        tle wchodzi plansza koncowa. Bez nakladania dwoch pelnoekranowych plansz (check: text_occluded)."""
        if host is None:
            self.panel("pend", t_in, self.total, END_INNER, track=6, cls="top")
        else:
            for sel in hide:
                self.js.append(f'tl.to("{sel}",{{opacity:0,y:-24,filter:"blur(10px)",duration:0.22,ease:"power2.in"}},{t_in - 0.16:.3f});')
            self.leak(t_in)
        self.js.append(f'tl.fromTo("#bub",{{opacity:0,scale:0.6,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.45,ease:"back.out(1.9)"}},{t_in + 0.05:.3f});')
        self.pop("#endtxt", t_in + 0.2)
        self.pop("#endsub", t_in + 0.3)
        self.js.append(f'tl.to("#bub",{{scale:1.06,duration:0.45,ease:"sine.inOut",yoyo:true,repeat:1}},{t_in + 0.95:.3f});')


def graphics(n, c, bounds, end_card_in):
    if n == 1:
        # plansza: przychody x2,5 / zespol 3x mniejszy (jak plansza "x25" w odcinku, ulozona pionowo)
        r3 = bounds[2][2]
        inner = ('<div class="bigs">'
                 f'<div class="bgx" id="bx0"><div class="bgx-v o" id="bx0v">×2,5</div><div class="bgx-l" id="bx0l">{icon("up", 40)}PRZYCHODY</div></div>'
                 f'<div class="bgx" id="bx1"><div class="bgx-v" id="bx1v">3×</div><div class="bgx-l" id="bx1l">{icon("down", 40)}MNIEJSZY ZESPÓŁ</div></div></div>'
                 + END_INNER)
        c.panel("p1", r3, c.total, inner, fade_out=False)  # plansza przechodzi w plansze koncowa
        c.js.append('gsap.set("#bx0v,#bx0l,#bx1v,#bx1l",{opacity:0});')
        c.pop("#bx0l", c.W("przychody", r3)[0] - 0.08)
        c.blur_in("#bx0v", c.W("razy", r3)[0] - 0.05)
        c.pop("#bx1l", c.W("zespół", r3)[0] - 0.08)
        c.blur_in("#bx1v", c.W("trzykrotnie", r3)[0] - 0.05)
        return "p1", ["#p1 .bigs"]
    elif n == 2:
        # plansza: lista "czego AI nie zrobi" (rosnie z kazda rzecza), potem twarz + chip "fala krytyki"
        r2, r3 = bounds[1][2], bounds[2][2]
        rows = [("NIE ZAMKNIE SPRZEDAŻY", c.W("zamknie", r2)[0]), ("NIE ZADZWONI DO KLIENTA", c.W("zadzwoni", r3)[0]),
                ("NIE UMÓWI SPOTKANIA", c.W("umówi", r3)[0])]
        inner = '<div class="p-head" style="top:330px">CZEGO AI NIE ZROBI</div><div class="list r2" style="top:430px">'
        for k, (lbl, _) in enumerate(rows):
            inner += f'<div class="row" id="p1r{k}"><div class="tile">{icon("x", 46)}</div><div class="lbl">{html.escape(lbl)}</div></div>'
        inner += "</div>"
        t_out = c.W("spotkania", r3)[1] + 0.1
        c.panel("p1", c.W("nie", r2)[0], t_out, inner)  # wchodzi na "nie zamknie" (bez pustej planszy)
        for k, (_, t) in enumerate(rows):
            c.pop(f"#p1r{k}", t - 0.08)
        t_f = c.W("fala", r3)[0]
        inner = f'<div class="chip2" id="chf"><span class="tile sm">{icon("msg", 32)}</span><span>FALA KRYTYKI</span></div>'
        c.overlay("chfw", t_f - 0.1, end_card_in + 0.35, inner, "chipwrap")
    elif n == 3:
        # chip "na start", potem plansza: plan na start 30 $ -> wystarczy
        r2 = bounds[1][2]
        t30 = c.W("30", r2)[0]  # plansza wchodzi razem z kwota (bez pustej planszy)
        inner = f'<div class="chip2" id="chs"><span class="tile sm">{icon("rocket", 32)}</span><span>NA START</span></div>'
        c.overlay("chsw", c.W("start", r2)[0] - 0.1, t30 - 0.1, inner, "chipwrap")
        inner = ('<div class="p-head" style="top:390px">PLAN NA START</div>'
                 '<div class="big30" id="p30" style="top:480px">30&nbsp;$</div>'
                 f'<div class="inv" style="top:790px"><div class="pill ok big" id="pok">{icon("check", 38)} WYSTARCZY</div></div>'
                 + END_INNER)
        c.panel("p1", t30, c.total, inner, fade_out=False)  # plansza przechodzi w plansze koncowa
        c.js.append('gsap.set("#pok",{opacity:0});')
        c.blur_in("#p30", t30 - 0.05)
        c.pop("#pok", c.W("wystarczy", r2)[0] - 0.06)
        return "p1", ["#p1 .p-head", "#p30", "#p1 .inv"]


EXTRA_CSS = r"""
      .bigs { position: absolute; left: 0; right: 0; top: 300px; display: flex; flex-direction: column; align-items: center; gap: 64px; }
      .bgx { text-align: center; }
      .bgx-v { font-size: 230px; font-weight: 900; letter-spacing: -0.05em; line-height: 1; color: #fff;
        filter: drop-shadow(0 10px 40px rgba(0,0,0,.45)); }
      .bgx-v.o { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .bgx-l { font-size: 44px; font-weight: 800; letter-spacing: .16em; margin-top: 16px; display: flex; align-items: center; justify-content: center; gap: 14px; }
      .bgx-l .ic { color: var(--accent); }
      .list.r2 { left: 184px; width: 700px; gap: 34px; }
      .list.r2 .lbl { font-size: 44px; }
      .pill.big { font-size: 42px; padding: 18px 40px; gap: 14px; }
      .playb { position: absolute; left: 50%; margin-left: -160px; top: 520px; width: 320px; height: 320px; border-radius: 50%; display: grid; place-items: center;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 90px rgba(var(--accent-rgb),.5), inset 0 2px 0 rgba(255,255,255,.35); }
      .playb svg { margin-left: 22px; }
"""


def setup_hf(d, n):
    hf = d / "hf"
    (hf / "fonts").mkdir(parents=True, exist_ok=True)
    (hf / "renders").mkdir(exist_ok=True)
    font = hf / "fonts/InterTight.ttf"
    if not font.exists():
        os.link(P / "hf/fonts/InterTight.ttf", font)
    name = f"hf_growth_rolka{n}"
    src = P.parent / "IMG_0526/hf"
    (hf / "hyperframes.json").write_text((src / "hyperframes.json").read_text())
    (hf / "package.json").write_text((src / "package.json").read_text().replace("hf_kaja", name))
    if not (hf / "meta.json").exists():
        (hf / "meta.json").write_text(json.dumps({"id": name, "name": name,
                                                  "createdAt": datetime.now(timezone.utc).isoformat()}, indent=2) + "\n")


def build(n):
    cfg = REELS[n]
    d = OUT / f"r{n}"
    setup_hf(d, n)
    shots, bounds, speech_end = timeline(cfg["segs"])
    total = round((speech_end + END_HOLD) * FPS) / FPS
    video(d, shots, speech_end, total)
    lu, tp = audio(d, cfg["segs"], total)
    ws = words(bounds, cfg)
    c = Comp(ws, total)
    end_card_in = round(speech_end + 0.12, 3)

    # najazd w kazdym ujeciu (ostatnie trwa pod plansza koncowa)
    c.js.append('gsap.set("#vwrap",{scale:1});')
    for k, sh in enumerate(shots):
        dur = (sh["l1"] - sh["l0"]) + (END_HOLD if k == len(shots) - 1 else 0.0)
        c.js.append(f'tl.set("#vwrap",{{scale:1}},{sh["r0"]:.3f});')
        c.js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{dur - 0.001:.3f},ease:"none"}},{sh["r0"]:.3f});')

    kin_end = bounds[cfg["hook_segs"]][2]
    c.kinetic([w for w in ws if w[0] < kin_end - 0.02], cfg["hook"], kin_end)
    phrases = manual_group([w for w in ws if w[0] >= kin_end - 0.02], cfg["phrases"])
    c.captions(phrases, kin_end, end_card_in)
    c.end_card(end_card_in, *(graphics(n, c, bounds, end_card_in) or ()))

    page = SZ.TEMPLATE.replace("    </style>", EXTRA_CSS + "    </style>")
    page = page.replace("{{TOTAL}}", f"{total:.3f}").replace("{{ELEMENTS}}", "\n    ".join(c.el)) \
        .replace("{{JS}}", "\n      ".join(c.js)) \
        .replace("{{KIN_TOP}}", str(getattr(SZ, "KIN_TOP", 960))).replace("{{CAP_TOP}}", str(getattr(SZ, "CAP_TOP", 1120))) \
        .replace("{{KIN_PAD}}", str((1080 - getattr(SZ, "KIN_W", 620)) // 2))
    page = SZ.kolory(page)
    (d / "hf/index.html").write_text(page)
    (d / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(c.srt)))
    print(f"rolka {n}: {total:.2f} s (mowa {speech_end:.2f} s), glos {lu:.1f} LUFS / szczyt {tp:.1f} dBFS, "
          f"{len(phrases)} fraz, plansza koncowa od {end_card_in:.2f}")
    for a, b, t in c.srt:
        print(f"   {a:6.2f}-{b:6.2f} {t}")


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or sorted(REELS):
        build(n)

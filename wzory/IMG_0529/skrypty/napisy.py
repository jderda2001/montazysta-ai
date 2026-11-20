#!/usr/bin/env python3
"""Napisy slowo po slowie (styl zatwierdzony w IMG_0526, przeniesiony na 16:9) + ../napisy.srt dla YouTube.

1. Slowa: whisper z DTW dla kawalkow (analiza/slowa_kawalki.json) -> os montazu (aroll/edl.json).
2. Tekst: poprawiony recznie (tekst.py); czasy przenoszone z whispera dopasowaniem sekwencji (difflib).
3. Frazy po 2-5 slow (koniec zdania, przecinek, pauza > 0,4 s, ciecie, max 28 znakow), jedno wyroznienie
   (w kolorze akcentu) na fraze: liczby > imiona/nazwy > slowa kluczowe; co druga fraza bez wyroznienia, chyba ze liczba.
4. Napisy chowane, gdy ten sam tekst pokazuje grafika (tekst kinetyczny, belka z imieniem, CTA, plansze z tekstem na dole).
5. Kompozycje HyperFrames po ~60 s: ../hf/n_XX.html + ../hf/napisy.json; SRT: ../napisy.srt (pelny tekst, bez ukrywania).

Uzycie: python3 -I napisy.py
"""
import difflib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tekst import TEXT  # noqa: E402
from paleta import kolory  # noqa: E402

P = Path(__file__).resolve().parent.parent
HF = P / "hf"
EDL = json.loads((P / "aroll/edl.json").read_text())
WORDS = json.loads((P / "analiza/slowa_kawalki.json").read_text())
ALLW = sorted([(cid[:2], a, b, t) for cid, ws in WORDS.items() for a, b, t in ws], key=lambda w: (w[0], w[1]))
HIDE = {"hook", "etaty", "closerzy", "montaz_ai2", "nie_zamknie", "nie_zadzwoni", "24", "cta", "lista", "mail",
        "poddzialy", "koniec"}
CHUNK = 60.0
KEYS = [
    (re.compile(r"^(\d|¼|dwa$|pięć$|trzykrotnie|cztery|czterech|dwóch|pół)"), 3),
    (re.compile(r"^(artur|kaj|kai$|weronik|tymon|nin[aę]|ig[ia]$|grok|adgen|elon)"), 2),
    (re.compile(r"^(growth|ai$|ai-|agent|sprzedaż|marketing|lead|closing|closer|crm|pipeline|b2b|b2c|automatyz|"
                r"zautomatyz|przych|koszt|etat|nurturing|mailing|live|żywo|voice|struktur|setter|montaż|subskryp|"
                r"feedback|komentarz|piramid|szok|kwalifikowane|przedzwonione|oze)"), 1),
]


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż¼]", "", t.lower())


def piece_words(e):
    out = []
    for s, a, b, t in ALLW:
        if s == e["src"] and e["a_in"] <= (a + b) / 2 < e["a_out"]:
            ta = e["t_in"] + max(0.0, a - e["a_in"])
            tb = e["t_in"] + min(e["a_out"] - e["a_in"], b - e["a_in"])
            out.append([ta, max(tb, ta + 0.05), t])
    return out


def align(e, text):
    ws = piece_words(e)
    toks = text.split()
    if not ws:
        span0, span1 = e["t_in"] + 0.1, e["t_out"] - 0.2
        step = (span1 - span0) / len(toks)
        return [[span0 + k * step, span0 + (k + 1) * step, t] for k, t in enumerate(toks)]
    nw, nc = [norm(w[2]) for w in ws], [norm(t) for t in toks]
    res = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, nw, nc, autojunk=False).get_opcodes():
        if op in ("equal", "replace") and i2 > i1:
            if i2 - i1 == j2 - j1:
                for k in range(j2 - j1):
                    res[j1 + k] = [ws[i1 + k][0], ws[i1 + k][1], toks[j1 + k]]
            else:
                a, b = ws[i1][0], ws[i2 - 1][1]
                lens = [max(1, len(nc[j])) for j in range(j1, j2)]
                tot, acc = sum(lens), 0
                for k, j in enumerate(range(j1, j2)):
                    s = a + (b - a) * acc / tot
                    acc += lens[k]
                    res[j] = [s, a + (b - a) * acc / tot, toks[j]]
    # wstawione slowa (bez odpowiednika u whispera): interpolacja miedzy sasiadami
    k = 0
    while k < len(res):
        if res[k] is not None:
            k += 1
            continue
        j = k
        while j < len(res) and res[j] is None:
            j += 1
        a = res[k - 1][1] if k > 0 else e["t_in"] + 0.05
        b = res[j][0] if j < len(res) else min(e["t_out"] - 0.05, a + 0.35 * (j - k))
        if b - a < 0.08 * (j - k):  # brak miejsca: zabierz czesc poprzedniego slowa
            if k > 0:
                a = max(res[k - 1][0] + 0.05, b - 0.12 * (j - k))
                res[k - 1][1] = a
            else:
                b = a + 0.12 * (j - k)
        step = (b - a) / (j - k)
        for m in range(k, j):
            res[m] = [a + (m - k) * step, a + (m - k + 1) * step, toks[m]]
        k = j
    for r in res:
        r[0] = min(max(r[0], e["t_in"]), e["t_out"] - 0.05)
        r[1] = min(max(r[1], r[0] + 0.05), e["t_out"])
    return res


def all_words():
    out = []
    for e in EDL:
        for a, b, t in align(e, TEXT[e["i"]]):
            out.append({"a": round(a, 3), "b": round(b, 3), "t": t, "i": e["i"]})
    for k in range(1, len(out)):  # monotonicznosc
        if out[k]["a"] < out[k - 1]["a"] + 0.03:
            out[k]["a"] = round(out[k - 1]["a"] + 0.03, 3)
        if out[k]["b"] <= out[k]["a"]:
            out[k]["b"] = round(out[k]["a"] + 0.05, 3)
    return out


FUNC = {"u", "w", "z", "o", "i", "a", "na", "do", "za", "od", "po", "że", "przy", "dla", "ze", "we", "bo", "czy", "jak",
        "ten", "tej", "te", "to", "tak", "nie", "się", "by", "co", "który", "która", "które", "jest", "są"}


def split_run(run):
    """Podzial ciagu slow (miedzy twardymi przerwami) na frazy 2-5 slow, mozliwie rowne (~20 znakow), max 30."""
    n = len(run)
    L = lambda a, b: len(" ".join(x["t"] for x in run[a:b]))
    best = [0.0] + [1e18] * n
    back = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(max(0, i - 5), i):
            c = L(j, i)
            last = norm(run[i - 1]["t"])
            cost = (c - 20) ** 2 / 10 + (400 if c > 30 else 0) + (60 if i - j == 1 and n > 1 else 0) + \
                (35 if i < n and last in FUNC else 0)
            if best[j] + cost < best[i]:
                best[i], back[i] = best[j] + cost, j
    parts, i = [], n
    while i > 0:
        parts.append(run[back[i]:i])
        i = back[i]
    return parts[::-1]


def phrases_of(words):
    cont = {e["i"]: e["cont"] for e in EDL}
    runs, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        end_s = w["t"][-1] in ".?!…:"
        comma = w["t"][-1] in ",;"
        gap = nxt["a"] - w["b"] if nxt else 99
        if nxt is None or end_s or gap > 0.4 or (comma and len(cur) >= 2):
            runs.append(cur)
            cur = []
    # pojedyncze slowa: koniec zdania -> do poprzedniego ciagu, inaczej -> do nastepnego (jesli pauza < 1 s)
    merged = []
    for k, r in enumerate(runs):
        if len(r) == 1 and merged and r[0]["t"][-1] in ".?!…" and merged[-1][-1]["t"][-1] not in ".?!…:" \
                and r[0]["a"] - merged[-1][-1]["b"] < 1.0:
            merged[-1] = merged[-1] + r
        else:
            merged.append(r)
    runs, carry = [], []
    for k, r in enumerate(merged):
        r = carry + r
        carry = []
        nxt = merged[k + 1] if k + 1 < len(merged) else None
        if len(r) == 1 and nxt is not None and r[0]["t"][-1] not in ".?!…:" and nxt[0]["a"] - r[0]["b"] < 1.0:
            carry = r
            continue
        runs.append(r)
    if carry:
        runs.append(carry)
    out = []
    for r in runs:
        out += split_run(r)
    # liczebniki: "dwa i pol" wyrozniane razem
    for p in out:
        ts = [norm(w["t"]) for w in p]
        for k in range(len(ts) - 2):
            if ts[k:k + 3] == ["dwa", "i", "pół"]:
                for w in p[k:k + 3]:
                    w["hl"] = True
    prev_hl = False
    for p in out:
        if any(w.get("hl") for w in p):
            prev_hl = True
            continue
        best, pri = None, 0
        for w in p:
            n = norm(w["t"])
            for rx, pr in KEYS:
                if rx.search(n) and pr > pri:
                    best, pri = w, pr
        if best is not None and (pri >= 3 or not prev_hl):
            best["hl"] = True
            prev_hl = True
        else:
            prev_hl = False
    return out


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(words):
    cues, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        txt = " ".join(x["t"] for x in cur)
        if nxt is None or (w["t"][-1] in ".?!…" and len(txt) > 20) or len(txt) + 1 + len(nxt["t"]) > 84 \
                or nxt["a"] - cur[0]["a"] > 6.0 or nxt["a"] - w["b"] > 1.0:
            cues.append(cur)
            cur = []
    lines = []
    for k, c in enumerate(cues):
        a = c[0]["a"]
        b = min(c[-1]["b"] + 0.3, cues[k + 1][0]["a"] - 0.02) if k + 1 < len(cues) else c[-1]["b"] + 0.5
        txt = " ".join(x["t"] for x in c)
        if len(txt) > 42:  # dwie linie, podzial przy srodku na spacji
            mid = len(txt) // 2
            sp = min((i for i, ch in enumerate(txt) if ch == " "), key=lambda i: abs(i - mid))
            txt = txt[:sp] + "\n" + txt[sp + 1:]
        lines.append(f"{k + 1}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n")
    (P / "napisy.srt").write_text("\n".join(lines))
    return len(cues)


def comp_html(phr, t0, t1):
    el, js = [], []
    for k, p in enumerate(phr):
        start = p["start"] - t0
        dur = p["end"] - p["start"]
        txt = " ".join(w["t"] for w in p["w"])
        fs = min(58, int(1500 / (len(txt) * 0.54)))
        spans = " ".join(f'<span class="w{" hl" if w.get("hl") else ""}">{html.escape(w["t"])}</span>' for w in p["w"])
        el.append(f'<div id="c{k}" class="cap clip" data-start="{start:.3f}" data-duration="{dur:.3f}" '
                  f'data-track-index="1" style="font-size:{fs}px">{spans}</div>')
        for j, w in enumerate(p["w"]):
            ta = max(start, w["a"] - t0 - 0.03)
            js.append(f'tl.fromTo("#c{k} .w:nth-child({j + 1})",{{opacity:0,y:12,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{ta:.3f});')
    return kolory(TEMPLATE.replace("{{DUR}}", f"{t1 - t0:.3f}").replace("{{ELEMENTS}}", "\n      ".join(el))
                  .replace("{{JS}}", "\n      ".join(js)))


TEMPLATE = r"""<!doctype html>
<html lang="pl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: transparent; }
      #root { position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: "Inter Tight", sans-serif; color: #fff; }
      .cap { position: absolute; left: 60px; right: 60px; top: 905px; text-align: center; font-weight: 650; letter-spacing: -0.015em;
        line-height: 1.1; white-space: nowrap; }
      .cap .w { display: inline-block; background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text;
        background-clip: text; color: transparent; filter: drop-shadow(0 4px 14px rgba(0,0,0,.6)) drop-shadow(0 0 22px rgba(255,255,255,.14)); }
      .cap .w.hl { background: linear-gradient(180deg, {{ACCENT_HI}} 0%, {{ACCENT}} 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
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
    words = all_words()
    phr_w = phrases_of(words)
    phr = []
    for k, p in enumerate(phr_w):
        start = p[0]["a"] - 0.06
        nxt = phr_w[k + 1][0]["a"] - 0.06 if k + 1 < len(phr_w) else p[-1]["b"] + 0.6
        phr.append({"w": p, "start": round(start, 3), "end": round(min(nxt, p[-1]["b"] + 0.6), 3)})
    grafiki = json.loads((HF / "grafiki.json").read_text())
    wins = [(g["start"], g["start"] + g["dlugosc"]) for g in grafiki if g["nazwa"] in HIDE]
    vis = []
    for p in phr:
        hit = [w for w in wins if p["start"] < w[1] and p["end"] > w[0]]
        if not hit:
            vis.append(p)
            continue
        w0 = min(w[0] for w in hit)
        if p["start"] >= w0 - 0.1:
            continue  # fraza w trakcie grafiki - pomijamy
        ws = [w for w in p["w"] if w["a"] < w0 - 0.15]
        if len(ws) >= 2 or (ws and len(p["w"]) == 1):
            vis.append({"w": ws, "start": p["start"], "end": round(w0 - 0.05, 3)})
    # kompozycje po ~60 s
    for old in HF.glob("n_*.html"):
        old.unlink()
    chunks, cur = [], []
    for p in vis:
        if cur and p["end"] - cur[0]["start"] > CHUNK:
            chunks.append(cur)
            cur = []
        cur.append(p)
    if cur:
        chunks.append(cur)
    man = []
    for k, ch in enumerate(chunks):
        t0, t1 = round(ch[0]["start"] - 0.05, 3), round(ch[-1]["end"] + 0.05, 3)
        fn = f"n_{k:02d}.html"
        (HF / fn).write_text(comp_html(ch, t0, t1))
        man.append({"plik": fn, "start": t0, "dlugosc": round(t1 - t0, 3), "frazy": len(ch)})
    (HF / "napisy.json").write_text(json.dumps(man, indent=1))
    n_srt = write_srt(words)
    (P / "analiza/napisy_slowa.json").write_text(json.dumps(words, ensure_ascii=False))
    lines = [f"{p['start']:7.2f}-{p['end']:7.2f}  " + " ".join(("*" + w["t"] + "*") if w.get("hl") else w["t"] for w in p["w"])
             for p in vis]
    (P / "analiza/napisy_frazy.txt").write_text("\n".join(lines) + "\n")
    print(f"slowa {len(words)}, frazy {len(phr)} (widoczne {len(vis)}), kompozycje {len(man)}, SRT {n_srt} wpisow")
    print("\n".join(lines[:40]))


if __name__ == "__main__":
    main()

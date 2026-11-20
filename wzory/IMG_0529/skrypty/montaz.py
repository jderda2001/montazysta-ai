#!/usr/bin/env python3
"""Lista ciec odcinka (EDL) -> ../aroll/edl.json + ../analiza/montaz_tekst.txt (tekst po montazu do kontroli).

Zrodla dzwieku: m7 = "Salon kosmetyczny Dreams 7.m4a" (wstep), m8 = "Salon kosmetyczny Dreams 8.m4a" (reszta).
Obraz: IMG_0529.MOV. Czas w wideo = czas w audio - offset (analiza/sync_m*.json, dopasowanie liniowe).

SEGS: (zrodlo, od, do, pomijane_kawalki). Czasy w pliku audio. None = granica kawalka (+/- margines).
Wewnatrz segmentu: przerwy miedzy kawalkami > MAXGAP sa skracane do ~0,3 s (ciecie), kawalki z listy
pominietych (szumy, "eee", falstarty) wypadaja. Jawne czasy ciec sa przyciagane do minimum obwiedni (+/-50 ms).

Uzycie: uv run --no-project --with numpy python3 -I montaz.py
"""
import json
import re
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
FPS = 30
PRE, POST = 0.10, 0.20       # margines przed poczatkiem mowy / po koncu mowy przy cieciu
MAXGAP = 0.60                # dluzsze przerwy miedzy kawalkami sa skracane (ciecie)
END_HOLD = 0.25              # po ostatnim slowie
ENDCARD = 8.0                # plansza koncowa (obraz wydluzony, dzwiek: cisza)
MIN_PIECE = 1.5              # krotszy kawalek po skroceniu pauzy -> zostaw naturalna pauze (do MAXKEEP)
MAXKEEP = 1.3
MAX_SHOT, MIN_SHOT = 10.0, 4.0  # dlugie ujecia dzielimy w pauzach zmiana kadru (bez wycinania czasu)

# --- lista ciec ------------------------------------------------------------------------------------------
SEGS = [  # (zrodlo, od, do, pomijane_kawalki); od/do: liczba (czas) albo "<id" (poczatek kawalka - PRE) / ">id" (koniec + POST)
    # ===== WSTEP (m7) =====
    ("m7", 49.33, ">m7_0028", []),        # hook (3. podejscie): Zautomatyzowalem caly dzial growth ... oraz OZE.
    ("m7", "<m7_0030", 69.50, []),        # Moi drodzy, dzisiejszy odcinek jest o tak naprawde | (1. "polrocznej")
    ("m7", 70.85, 75.64, []),             # polrocznej, bardzo... mocnej pracy z naszej strony w tym roku, bo | (eee)
    ("m7", 77.30, 115.30, []),            # w wielkim skrocie co sie udalo ... generowal | (psst)
    ("m7", 116.55, 130.72, []),           # dwa i pol raza mniejszy przychod ... aktualnie. Bo, | (nope)
    ("m7", 131.42, 139.72, []),           # jakby rok temu ... Przychody razy 2,5 do przodu ponad, | (uhhh)
    ("m7", 140.90, 184.45, []),           # a zespol trzykrotnie mniejszy. ... To jest oczywistosc.
    ("m7", 190.40, 239.74, []),           # Nastepnie, czego z tym AI ... i dlaczego go tak bardzo czuje.
    # (m7 od 249,44 s to petla bufora; watek "to ja bylem odpowiedzialny..." + dubel "Dlatego tez czuje" pomijamy)
    # ===== m8 =====
    ("m8", 22.10, 35.25, []),             # I dlaczego to jest pierwszy odcinek ... nastepne dzialy. | (podeszlem/podszedlem)
    ("m8", 37.98, ">m8_0012", []),        # i uwazam, ze to jest dobra kolejnosc ... jak on w ogole wyglada.
    ("m8", "<m8_0013", 96.75, ["m8_0026"]),  # Teraz przed Wami pokazuje czterech agentow ... na closing, | (zszedlem z tronu)
    ("m8", 102.25, 114.22, ["m8_0033"]),  # bo ciekawostka, w tamtym roku ... super ludzie i w ogole, | (zeby ich praca...)
    ("m8", 122.25, ">m8_0040", []),       # z tym, ze po prostu nam sie to nie spinalo ... powodzi.
    ("m8", "<m8_0042", 159.76, ["m8_0051"]),  # I ja wrocilem ... nie musze tracic czasu na spotkania, | (ktore)
    ("m8", 160.33, ">m8_0055", []),       # na ktore przychodza ludzie, ktorzy sa faktycznie | (tak)
    ("m8", 164.45, ">m8_0073", []),       # tacy do grzania, nie? Potem mamy Weronike ... sprzedazy u nas.
    ("m8", "<m8_0074", 225.12, []),       # Nastepnie mamy Tymona. Tymon jest |
    ("m8", 227.88, ">m8_0081", []),       # agentem odpowiedzialnym za ... lepsze.
    ("m8", "<m8_0083", ">m8_0090", ["m8_0087"]),  # Takze tak to wyglada ... razem to przekminiamy.
    ("m8", "<m8_0091", ">m8_0102", ["m8_0093"]),  # Co jest swietne w tej aplikacji ... szybciej sie ona wtedy wydarza.
    # (wypada: "Takze... Tyle mysle, jesli chodzi o sama strukture tego dzialu. Wyglada to w ten sposob i")
    ("m8", "<m8_0109", ">m8_0114", ["m8_0110"]),  # Jakie jeszcze tutaj osoby planuje dorzucic? ... nowe funkcjonalnosci.
    ("m8", "<m8_0116", ">m8_0134", ["m8_0128", "m8_0132"]),  # to po prostu bedziemy rozbudowywac ... strukture tego dzialu growth.
    ("m8", "<m8_0136", ">m8_0165", ["m8_0159", "m8_0160", "m8_0161"]),  # Ok, teraz idac dalej ... bot tez moze robic.
    ("m8", "<m8_0166", 504.40, []),       # Druga rzecza, |
    ("m8", 508.66, 560.72, ["m8_0167", "m8_0170"]),  # ktorej AI ... nie zadzwoni ... zeby dac Kai telefon, no to | (yyy)
    ("m8", 561.75, 568.38, []),           # jeszcze nie jestesmy w stanie ... Twilio, i | (yyy)
    ("m8", 568.98, 612.07, []),           # tam po prostu to wszystko pospinalismy ... ale jesli tylko wyjdzie, |
    ("m8", 612.88, ">m8_0196", []),       # to dzialamy.
    ("m8", "<m8_0198", ">m8_0222", ["m8_0203", "m8_0210"]),  # No i tutaj zdradzilem nazwe apki ... jest za 100 dolarow.
    ("m8", "<m8_0224", 692.56, []),       # Drogi widzu ... ale ogolnie |
    ("m8", 693.12, ">m8_0225", []),       # w calym tym Grok bocie mamy | (dwadziescia... 24 boty)
    ("m8", "<m8_0230", 746.86, ["m8_0237"]),       # 24 agentow ... I tutaj zmierzamy ku koncowi | (eeee)
    ("m8", 748.02, 750.06, []),           # Jesli spodobalo sie | (eeee)
    ("m8", 751.30, 782.00, []),           # ten pierwszy odcinek ... lubie wylapywac te |
    ("m8", 782.62, ">m8_0259", []),       # wszystkie nowinki ... jaki tez bedzie tego wydzwiek.
    ("m8", "<m8_0262", ">m8_0271", []),   # Dziekuje bardzo, ja mam na imie Jakub Derda ... do nastepnego razu.
]
# Dodatkowe ciecia wewnatrz segmentow (zrodlo, od, do): zawahania wewnatrz kawalkow i powtorzenia slow.
CUTS = [
    ("m8", 402.37, 402.97),   # "by [eee] przekminialy"
    ("m8", 534.05, 534.61),   # "ze [eee] bedzie fala krytyki"
    ("m8", 537.97, 538.38),   # pierwsze, ciche "od" ("sa juz od | od dluzszego czasu")
    ("m8", 643.26, 644.08),   # pierwsze "ktora" ("firmie, ktora | ktora ma")
    ("m8", 646.93, 647.52),   # "i [eee] finanse"
]
FRAMES = {  # (w, h, x, y) w px zrodla 3840x2160; twarz ~ (2170, 740)
    "W": (3840, 2160, 0, 0),
    "M": (3200, 1800, 570, 52),
    "C": (2744, 1544, 798, 120),
}


def load_env(name):
    with wave.open(str(P / f"audio/{name}_16k.wav")) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 200, sr // 50  # 5 ms / 20 ms
    n = (len(x) - win) // hop
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    db = 20 * np.log10(np.sqrt(np.mean(x[idx] ** 2, axis=1)) + 1e-7)
    return db, len(x) / sr


ENV = {n: load_env(n) for n in ("m7", "m8")}
WORDS = json.loads((P / "analiza/slowa_kawalki.json").read_text())


def snap(src, t, rad=0.05):
    db, _ = ENV[src]
    i0, i1 = max(0, int((t - rad) * 200)), min(len(db) - 1, int((t + rad) * 200))
    k = i0 + int(np.argmin(db[i0:i1 + 1]))
    return round(k / 200 + 0.01, 3)  # srodek okna 20 ms


def video_time(src, t):
    s = json.loads((P / f"analiza/sync_{src}.json").read_text())
    b, k = s["fit"]
    # czas_audio = t_v + b + k*t_v  ->  t_v = (t - b) / (1 + k)
    return (t - b) / (1 + k)


def fr(t):
    return round(t * FPS) / FPS


def build():
    chunks = json.loads((P / "analiza/kawalki.json").read_text())
    by_src = {}
    for c in chunks:
        by_src.setdefault(c["src"], []).append(c)
    cid = {c["id"]: c for c in chunks}
    ranges = []  # (src, a, b) zakresy do zachowania (czas audio), po wszystkich cieciach
    for seg in SEGS:
        src, a, b, skip = seg

        def resolve(v, side):
            if isinstance(v, str):
                c = cid[v[1:]]
                return c["a"] - PRE if v[0] == "<" else c["b"] + POST
            return snap(src, v)
        a, b = resolve(a, "a"), resolve(b, "b")
        # kawalki w zakresie
        cs = [c for c in by_src[src] if c["b"] > a + 0.02 and c["a"] < b - 0.02]
        keep = [c for c in cs if c["id"] not in skip]
        skipped = [c for c in cs if c["id"] in skip]
        pieces, cur = [], [a, None, None]  # [od, do, (luka_oryginalna jesli ciecie tylko z ciszy)]
        for k, c in enumerate(keep):
            if k == 0:
                continue
            prev = keep[k - 1]
            gap = c["a"] - prev["b"]
            between = [s for s in skipped if prev["b"] <= s["a"] and s["b"] <= c["a"]]
            if gap > MAXGAP or between:
                out = prev["b"] + POST
                inn = c["a"] - PRE
                for s in between:
                    out = min(out, s["a"] - 0.03)
                    inn = max(inn, s["b"] + 0.03)
                if inn - out < 0.05:  # nic do wyciecia
                    continue
                cur[1] = out
                pieces.append(cur)
                cur = [inn, None, None if between else gap]
        cur[1] = b
        pieces.append(cur)
        # zbyt krotki kawalek po skroceniu samej ciszy -> zostaw naturalna pauze (bez ciecia)
        merged = [pieces[0]]
        for pc in pieces[1:]:
            last = merged[-1]
            short = (pc[1] - pc[0] < MIN_PIECE) or (last[1] - last[0] < MIN_PIECE)
            if pc[2] is not None and pc[2] <= MAXKEEP and short:
                last[1] = pc[1]
            else:
                merged.append(pc)
        for pa, pb, _ in merged:
            ranges.append([src, max(a, pa), min(b, pb)])
    # dodatkowe ciecia wewnatrz zakresow
    for src, ca, cb in CUTS:
        ca, cb = snap(src, ca), snap(src, cb)
        new = []
        for r in ranges:
            if r[0] == src and r[1] < ca < r[2] and r[1] < cb <= r[2] + 0.5:
                new.append([src, r[1], ca])
                if cb < r[2]:
                    new.append([src, cb, r[2]])
            else:
                new.append(r)
        ranges = new
    ranges = [r for r in ranges if r[2] - r[1] > 0.15]
    return ranges


def split_long(ranges):
    """Dlugie ujecia dzielimy w pauzach miedzy kawalkami (zmiana kadru bez wycinania czasu).
    Preferowane konce zdan; ujecia 4-10 s, celujemy w ~7 s."""
    chunks = json.loads((P / "analiza/kawalki.json").read_text())
    out = []
    for src, a, b in ranges:
        cs = sorted([c for c in chunks if c["src"] == src and c["b"] > a + 0.05 and c["a"] < b - 0.05],
                    key=lambda c: c["a"])
        cand = []
        for k in range(len(cs) - 1):
            g0, g1 = cs[k]["b"], cs[k + 1]["a"]
            if g1 - g0 >= 0.15 and a + 0.5 < g0 and g1 < b - 0.5:
                txt = cs[k]["text"].strip()
                sc = (2.0 if txt[-1:] in ".?!" else 1.0 if txt[-1:] in ",;:" else 0.0) + min(g1 - g0, 0.6)
                cand.append(((g0 + g1) / 2, sc))
        # granice slow po interpunkcji wewnatrz dlugich kawalkow (slabszy wybor)
        for c in cs:
            ws = WORDS.get(c["id"], [])
            for k in range(len(ws) - 1):
                if ws[k][2][-1:] in ".?!," and a + 0.5 < ws[k][1] < b - 0.5:
                    t = (ws[k][1] + ws[k + 1][0]) / 2 if ws[k + 1][0] > ws[k][1] else ws[k][1] + 0.02
                    cand.append((snap(src, t, 0.04), 1.2 if ws[k][2][-1:] in ".?!" else 0.6))
        pos, parts = a, []
        while b - pos > MAX_SHOT:
            ok = [(t, sc) for t, sc in cand if pos + MIN_SHOT <= t <= min(pos + MAX_SHOT, b - MIN_SHOT)]
            if not ok:
                ok = [(t, sc) for t, sc in cand if pos + 3.0 <= t <= b - 3.0 and t <= pos + 20.0]
            if not ok:
                break
            t, _ = max(ok, key=lambda x: x[1] - 0.25 * abs((x[0] - pos) - 7.0))
            t = pos + fr(t - pos)
            parts.append([src, pos, t, True])
            pos = t
        parts.append([src, pos, b, False])
        out += parts
    return out  # [src, a, b, ciagle_z_nastepnym]


def frame_plan(ranges):
    """Kadr dla kazdego ujecia: co drugie ujecie W, pomiedzy na zmiane C i M. Hook = C."""
    out, alt = [], ["C", "M"]
    k_alt = 0
    for i, r in enumerate(ranges):
        if i == 0:
            out.append("C")
            continue
        prev = out[-1]
        if prev != "W":
            out.append("W")
        else:
            out.append(alt[k_alt % 2])
            k_alt += 1
    return out


def main():
    ranges = split_long(build())
    frames = frame_plan(ranges)
    edl, t = [], 0.0
    for i, ((src, a, b, cont), f) in enumerate(zip(ranges, frames)):
        last = i == len(ranges) - 1
        if last:
            b += END_HOLD
        dur = fr(b - a)
        edl.append({"i": i, "src": src, "a_in": round(a, 4), "a_out": round(a + dur, 4),
                    "v_in": round(video_time(src, a), 4), "t_in": round(t, 4), "t_out": round(t + dur, 4),
                    "frame": f, "cont": cont, "video_extra": ENDCARD if last else 0.0})
        t += dur
    (P / "aroll").mkdir(exist_ok=True)
    (P / "aroll/edl.json").write_text(json.dumps(edl, indent=1))
    # tekst po montazu: slowa kawalkow, ktorych srodek wpada w zachowany zakres
    words = json.loads((P / "analiza/slowa_kawalki.json").read_text())
    allw = []
    for k, ws in words.items():
        for a, b, txt in ws:
            allw.append((k[:2], a, b, txt))
    lines = []
    for e in edl:
        ws = [w for w in allw if w[0] == e["src"] and e["a_in"] <= (w[1] + w[2]) / 2 < e["a_out"]]
        ws.sort(key=lambda w: w[1])
        lines.append(f"[{e['i']:3d}] {e['t_in']:7.2f} {e['frame']}{'~' if e['cont'] else ' '} {e['src']} {e['a_in']:7.2f}-{e['a_out']:7.2f} | "
                     + " ".join(w[3] for w in ws))
    (P / "analiza/montaz_tekst.txt").write_text("\n".join(lines) + "\n")
    tt = t + ENDCARD
    print(f"{len(edl)} ujec, mowa {t:.2f} s + plansza {ENDCARD} s = {tt:.2f} s ({int(tt // 60)}:{tt % 60:04.1f})")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

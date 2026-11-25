#!/usr/bin/env python3
"""Kontrola pierwszych 5 s gotowej rolki, slowo po slowie (po bledzie HOOK A C4537_v2, 25.11.2026).

Dlaczego osobno od powtorzenia.py: tamten szuka powtorzonych SLOW na calej rolce. Sklejka dwoch podejsc tego samego
zdania (hook z dwoch dubli) zostawia na cieciu ulamek glosu z drugiego dubla (koncowka poprzedniego slowa, "u" przed
"niech"), ktory whisper w dlugim oknie wygladza, a w oknie zaczynajacym sie dokladnie na cieciu slyszy ("O nich").

Co robi na pliku MP4 (gotowy eksport):
  1. whisper bez promptu na 0-6,5 s, slowa ze znacznikami (DTW) i porownanie z napisami .srt z 0-5 s:
     slowa spoza napisow, brakujace, to samo slowo/fraza dwa razy, ktorych nie ma w napisach;
  2. kazde ciecie w 0-5 s (z aroll/edl.json projektu albo ze skoku obrazu): whisper w oknie OD ciecia i DO ciecia,
     pierwsze/ostatnie slowo musi byc slowem z napisow w tym miejscu;
  3. nagranie zrodlowe (audio/nowe_16k.wav projektu): czy przed a_in / po a_out kwestii z 0-5 s jest jeszcze glos
     (ciecie w srodku mowy = ryzyko ulamka gloski z sasiedniego slowa);
  4. obraz: zamrozenia, powrot do klatki sprzed >= 0,4 s (zdublowane ujecie), napis .srt dwa razy pod rzad;
  5. stykowka klatek co 0,5 s (0-4,5 s) do obejrzenia: <out>/<nazwa>_klatki.jpg.

Uzycie: uv run --no-project --with numpy python3 -I poczatek.py PLIK.mp4 NAPISY.srt [--projekt KATALOG] [--out KATALOG]
Kod wyjscia 1, gdy sa alarmy. Kazdy alarm rozstrzygnij uchem i okiem (klip / klatki), jak w powtorzenia.py.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
SR = 16000
OKNO = 5.0
STOP = {"i", "a", "to", "że", "w", "z", "na", "do", "się", "nie", "jest", "po", "o", "co", "ten", "ta", "tak", "czyli",
        "bo", "jak", "mi", "ci", "mnie", "cię", "go", "je", "już", "też", "tylko", "albo", "oraz", "u", "od", "za", "ze"}


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


def rdzen(w):
    return w[:min(5, len(w) - 1)] if len(w) >= 4 else w


def podobne(a, b):
    a, b = norm(a), norm(b)
    if len(a) >= 2 and len(b) >= 2 and (a.startswith(b) or b.startswith(a)):
        return True  # whisper skleja albo rozbija slowa ("Tensam", "note taker")
    return a == b or rdzen(a) == rdzen(b) or difflib.SequenceMatcher(a=a, b=b).ratio() >= 0.7


def fon(s):
    """Luzna fonetyka do porownania koncowek ("po callu" ~ "pokolu" u whispera)."""
    s = re.sub(r"[^a-ząćęłńóśźż]", "", s.lower())
    for a_, b_ in (("ch", "h"), ("c", "k"), ("w", "f"), ("ó", "u"), ("rz", "ż"), ("ą", "o"), ("ę", "e")):
        s = s.replace(a_, b_)
    return re.sub(r"(.)\1+", r"\1", s)


def ta_sama_koncowka(zrodlo, tekst):
    S, t = fon(zrodlo), fon(tekst)
    if len(t) < 4 or not S:
        return False
    return max(difflib.SequenceMatcher(a=S[-n:], b=t).ratio() for n in range(max(1, len(t) - 3), len(t) + 5)) >= 0.72


def czytaj_wav(f):
    with wave.open(str(f)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def zapisz_wav(f, x):
    with wave.open(str(f), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def whisper(x, a, b, td, k, dtw=False):
    f = Path(td) / f"w{k}.wav"
    zapisz_wav(f, x[int(a * SR):int(b * SR)])
    if not dtw:
        r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-nfa", "-np"],
                           capture_output=True, text=True)
        return " ".join(r.stdout.split())
    subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-ml", "1", "-sow", "-dtw",
                    "large.v3.turbo", "-nfa", "-ojf", "-of", str(f.with_suffix("")), "-np"], capture_output=True, check=True)
    d = json.loads(f.with_suffix(".json").read_text())
    out = []
    for s in d["transcription"]:
        txt = s["text"].strip()
        toks = [t for t in s.get("tokens", []) if re.search(r"\w", t["text"]) and not t["text"].startswith("[_")]
        if not norm(txt) or not toks:
            continue
        od = s["offsets"]["from"] / 1000
        do = max(t.get("t_dtw", -1) for t in toks) / 100
        if do <= 0:
            do = s["offsets"]["to"] / 1000
        out.append([a + od, a + max(do, od + 0.03), txt])
    return out


def srt(f):
    cues = []
    for blok in re.split(r"\n\s*\n", Path(f).read_text(encoding="utf-8-sig").strip()):
        ls = blok.strip().splitlines()
        if len(ls) < 3:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", ls[1])
        if not m:
            continue
        g = [int(v) for v in m.groups()]
        cues.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000,
                     " ".join(ls[2:])))
    return cues


def slowa_srt(cues, a, b):
    out = []
    for c0, c1, t in cues:
        if c1 <= a or c0 >= b:
            continue
        ws = [w for w in t.split() if norm(w)]
        for j, w in enumerate(ws):
            out.append((c0 + (c1 - c0) * j / max(1, len(ws)), w))
    return out


def db_env(x):
    hop = SR // 100
    n = len(x) // hop
    return 20 * np.log10(np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-7)


def klatki(mp4, n):
    W, H = 54, 96
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                          "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip().split("/")
    fps = float(fps[0]) / float(fps[1] if len(fps) > 1 else 1)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", str(n), "-i", str(mp4), "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return fps, np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("srt")
    ap.add_argument("--projekt")
    ap.add_argument("--out", default="analiza/poczatek")
    a = ap.parse_args()
    mp4, out = Path(a.mp4), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    nazwa = mp4.stem
    alarmy, info, uwagi = [], [], []
    cues = srt(a.srt)
    oczek = slowa_srt(cues, 0, OKNO + 0.3)

    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", "7.5", "-i", str(mp4), "-vn", "-ac", "1", "-ar", str(SR), w],
                       check=True)
        x = czytaj_wav(w)

        # 1. slowa 0-6,5 s vs napisy
        sl = whisper(x, 0, 6.5, td, "pelne", dtw=True)
        znane = {norm(w) for _, w in oczek}
        scal = []
        for s_ in sl:
            if scal and norm(scal[-1][2] + s_[2]) in znane and norm(s_[2]) not in znane:
                scal[-1] = [scal[-1][0], s_[1], scal[-1][2] + s_[2]]
            else:
                scal.append(list(s_))
        sl = scal
        sl5 = [s for s in sl if s[0] < OKNO]
        info.append("słyszę 0–5 s: " + " ".join(f"{s[0]:.2f}:{s[2]}" for s in sl5))
        info.append("napisy 0–5 s: " + " | ".join(f"{c0:.2f} {t}" for c0, c1, t in cues if c0 < OKNO))
        A = [rdzen(norm(s[2])) for s in sl5]
        B = [rdzen(norm(w)) for _, w in oczek if _ < OKNO]
        sm = difflib.SequenceMatcher(a=B, b=A, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            slysze = " ".join(s[2] for s in sl5[j1:j2])
            napis = " ".join(w for _, w in [o for o in oczek if o[0] < OKNO][i1:i2])
            if op == "replace" and all(podobne(p, q) for p, q in zip(slysze.split(), napis.split())) and \
                    len(slysze.split()) == len(napis.split()):
                continue
            # koniec okna: slowo przeciete granica 5 s
            if (j2 == len(A) and i1 >= len(B) - 1) or (i2 == len(B) and j1 >= len(A) - 1):
                continue
            t = sl5[j1][0] if j1 < len(sl5) else (sl5[-1][1] if sl5 else 0)
            alarmy.append((t, f"tekst: słychać „{slysze or '—'}”, w napisach „{napis or '—'}”"))
        for i in range(len(A) - 1):
            if A[i] == A[i + 1] and len(A[i]) >= 2 and not any(B[k] == B[k + 1] == A[i] for k in range(len(B) - 1)):
                alarmy.append((sl5[i + 1][0], f"to samo słowo dwa razy: „{sl5[i][2]} {sl5[i + 1][2]}”"))
        for n in (3, 2):
            for i in range(len(A) - n + 1):
                g = A[i:i + n]
                if not any(len(v) >= 4 and v not in STOP for v in g):
                    continue
                ile_a = sum(1 for k in range(len(A) - n + 1) if A[k:k + n] == g)
                ile_b = sum(1 for k in range(len(B) - n + 1) if B[k:k + n] == g)
                if ile_a > ile_b and ile_a > 1:
                    alarmy.append((sl5[i][0], f"fraza dwa razy: „{' '.join(s[2] for s in sl5[i:i + n])}” "
                                              f"(słychać {ile_a}×, w napisach {ile_b}×)"))

        # 2. ciecia
        ciecia = []
        edl = None
        if a.projekt and (Path(a.projekt) / "aroll/edl.json").exists():
            edl = json.loads((Path(a.projekt) / "aroll/edl.json").read_text())
            ciecia = [e["t_in"] for e in edl if 0.05 < e["t_in"] < OKNO]
        fps, fr = klatki(mp4, OKNO + 0.5)
        d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
        med = float(np.median(d))
        for i in range(1, len(d) - 1):
            if d[i] > max(8, 6 * med) and d[i - 1] < d[i] / 2.5 and d[i + 1] < d[i] / 1.5:
                t = (i + 1) / fps
                if t < OKNO and not any(abs(t - c) < 0.05 for c in ciecia):
                    ciecia.append(t)
        ciecia = sorted(set(round(c, 3) for c in ciecia))
        info.append("cięcia 0–5 s: " + (", ".join(f"{c:.2f}" for c in ciecia) or "brak"))
        for k, c in enumerate(ciecia):
            po_sl = [s[2] for s in sl if s[1] > c + 0.05][:2]
            przed_sl = [s[2] for s in sl if s[0] < c - 0.05][-2:]
            for m, start in enumerate((c - 0.03, c - 0.01, c + 0.01)):
                for dl in (1.0, 1.4):
                    pw = [v for v in whisper(x, max(0, start), min(start + dl, 7.4), td, f"po{k}{m}").split() if norm(v)]
                    zlaczone = norm("".join(pw[:2])) if len(pw) > 1 else ""  # "w puściła" = "wpuściła"
                    if pw and po_sl and not any(podobne(pw[0], v) or zlaczone == norm(v) for v in po_sl):
                        alarmy.append((c, f"cięcie {c:.2f} s: w oknie od {start:.2f} s słychać „{' '.join(pw[:3])}”, "
                                          f"w całości „{' '.join(po_sl)}” (ułamek głosu z sąsiedniego słowa/dubla?)"))
                        break
                else:
                    continue
                break
            for m, koniec in enumerate((c + 0.01, c + 0.03)):
                ww = [v for v in whisper(x, max(0, koniec - 1.2), koniec, td, f"przed{k}{m}").split() if norm(v)]
                if ww and przed_sl and not any(podobne(ww[-1], v) for v in przed_sl + po_sl[:1]):
                    alarmy.append((c, f"cięcie {c:.2f} s: w oknie do {koniec:.2f} s słychać „{' '.join(ww[-3:])}”, "
                                      f"w całości „{przed_sl[-1]}”"))
                    break
            zapisz_wav(out / f"{nazwa}_ciecie_{c:05.2f}.wav", x[int(max(0, c - 1.0) * SR):int((c + 1.0) * SR)])

        # 3. zrodlo: glos tuz przed a_in / po a_out
        if edl is not None:
            src = Path(a.projekt) / "audio/nowe_16k.wav"
            if src.exists():
                xs = czytaj_wav(src)
                dbs = db_env(xs)
                for k, e in enumerate(edl):
                    if e["t_in"] >= OKNO:
                        continue
                    if k and not edl[k - 1].get("hold"):
                        przed_src = whisper(xs, max(0, e["a_in"] - 1.6), e["a_in"], td, f"src{k}")
                        koniec_pop = " ".join([v for v in edl[k - 1].get("text", "").split() if norm(v)][-3:])
                        if ta_sama_koncowka(przed_src, koniec_pop):
                            alarmy.append((e["t_in"], f"sklejka dwóch podejść tego samego zdania: w nagraniu tuż przed "
                                                      f"a_in={e['a_in']:.2f} pada „…{przed_src[-30:]}”, a poprzednia "
                                                      f"kwestia (inne miejsce nagrania) kończy się „{koniec_pop}”. "
                                                      f"Bezpiecznie tylko przy wyraźnej pauzie przed a_in (albo to wycięty wtręt z tego samego podejścia – uchem)"))
                    sp = e.get("speech") or [e["a_in"], e["a_out"]]
                    mowa = dbs[int(sp[0] * 100):int(sp[1] * 100)]
                    if not len(mowa):
                        continue
                    poziom = float(np.percentile(mowa, 70))
                    przed = dbs[max(0, int(e["a_in"] * 100) - 6):int(e["a_in"] * 100)]
                    po = dbs[int(e["a_out"] * 100):int(e["a_out"] * 100) + 6]
                    if e["t_in"] > 0.05 and len(przed) and przed.max() > poziom - 14:
                        (alarmy if przed.max() > poziom - 6 else uwagi).append((e["t_in"], f"kwestia {e['i']} („{e.get('text', '')[:40]}”) zaczyna się w środku "
                                                  f"mowy: w nagraniu 60 ms przed a_in={e['a_in']:.2f} głos "
                                                  f"{przed.max():.0f} dB (mowa {poziom:.0f} dB)"))
                    if len(po) and po.max() > poziom - 14 and e["t_out"] < OKNO:
                        (alarmy if po.max() > poziom - 6 else uwagi).append((e["t_out"], f"kwestia {e['i']} kończy się w środku mowy: 60 ms po "
                                                   f"a_out={e['a_out']:.2f} głos {po.max():.0f} dB (mowa {poziom:.0f} dB)"))

        # 4. obraz
        run = 0
        for i, v in enumerate(d):
            if v < 0.12:
                run += 1
                continue
            if run >= int(0.3 * fps):
                info.append(f"stały obraz {(i - run) / fps:.2f}–{i / fps:.2f} s (grafika/zamrożenie – obejrzyj)")
            run = 0
        gap = int(0.4 * fps)
        zgl = -9
        for i in range(gap + 1, min(len(fr), int(OKNO * fps)), max(1, int(fps / 20))):
            dist = np.abs(fr[:i - gap] - fr[i]).mean(axis=(1, 2))
            j = int(dist.argmin())
            if dist[j] < 1.0 and np.abs(fr[j:i] - fr[i]).mean(axis=(1, 2)).max() > 8 and i / fps - zgl > 0.5:
                alarmy.append((i / fps, f"obraz: klatka {i / fps:.2f} s jak {j / fps:.2f} s (zdublowane ujęcie?)"))
                zgl = i / fps
        for (a0, a1, ta), (b0, b1, tb) in zip(cues, cues[1:]):
            if b0 < OKNO and norm(ta) and norm(ta) == norm(tb):
                alarmy.append((b0, f"napis „{tb}” dwa razy pod rząd ({a0:.2f} i {b0:.2f} s)"))
            if b0 < OKNO and b0 < a1 - 0.05:
                alarmy.append((b0, f"napisy nachodzą na siebie: „{ta}” do {a1:.2f}, „{tb}” od {b0:.2f}"))

    # 5. stykowka co 0,5 s
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", "5", "-i", str(mp4), "-vf",
                    "fps=2,scale=162:288,tile=10x1:padding=3:color=red", "-frames:v", "1",
                    str(out / f"{nazwa}_klatki.jpg")], check=True)

    print(f"== {mp4.name}")
    for i in info:
        print("   " + i)
    alarmy.sort()
    for t, o in sorted(uwagi):
        print(f"   uwaga {t:5.2f} s: {o} (sprawdź uchem)")
    if alarmy:
        for t, o in alarmy:
            print(f"   ALARM {t:5.2f} s: {o}")
    else:
        print("   czysto")
    sys.exit(1 if alarmy else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Walidacja czasow slow w napisach: whisper na [poczatek kwestii, koniec slowa + MARGINES] musi juz zawierac to slowo.
Jesli nie zawiera, napis tego slowa pojawialby sie przed mowa.

Artefakty, ktore NIE sa bledem: slowa 1-2 literowe ("w", "o", "a") i slowa otwierajace zdanie ("Zanim", "czy", "Z tym")
whisper czesto gubi na samym koncu wycinka. Pojedyncze takie wpisy sprawdz na obwiedni, zamiast poprawiac czasy.

Uzycie (z katalogu skrypty/ projektu): python3 -I waliduj_napisy.py [MARGINES=0.15]
Czyta ../aroll/edl.json, ../audio/slowa.json, ../audio/nowe_16k.wav.
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
SRC = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
MARGIN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.15


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


def similar(a, b):
    a, b = norm(a), norm(b)
    if {a, b} == {"tym", "czym"}:
        return True
    if any(c.isdigit() for c in b) and (any(c.isdigit() for c in a) or a in ("dwie", "stówki", "trzy", "pięć", "sześć")):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.6


def matched(exp, got):
    j, m = 0, 0
    for w in exp:
        for jj in range(j, min(len(got), j + 3)):
            if similar(w, got[jj]):
                m, j = m + 1, jj + 1
                break
    return m


def main():
    edl = json.loads((P / "aroll/edl.json").read_text())
    words = json.loads((P / "audio/slowa.json").read_text())
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "c.wav"
        for e in edl:
            ws = [w for w in words if e["t_in"] - 0.001 <= w[0] < e["t_out"] - 0.001]
            exp = [w[2] for w in ws]
            line = []
            for k, w in enumerate(ws):
                t = w[1] - e["t_in"] + e["a_in"] + MARGIN
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{e['a_in']:.3f}", "-to",
                                f"{t:.3f}", "-i", str(SRC), "-c:a", "pcm_s16le", str(f)], check=True)
                r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-np"],
                                   capture_output=True, text=True)
                got = r.stdout.split()
                ok = matched(exp[:k + 1], got) >= k + 1 or len(norm(w[2])) <= 2
                bad += not ok
                line.append(w[2] if ok else f"[{w[2]}?]")
                if not ok:
                    print(f"   {e['i']} '{w[2]}' (koniec {t - MARGIN:.2f}): do {t:.2f} slychac: {' '.join(got)}")
            print(f"== {e['i']}: {' '.join(line)}")
    print(f"nie przeszlo: {bad} z {len(words)} (margines {MARGIN} s)")


if __name__ == "__main__":
    main()

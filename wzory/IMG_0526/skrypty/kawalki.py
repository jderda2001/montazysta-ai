#!/usr/bin/env python3
"""Wykrywanie falstartow i powtorzen w wybranych dublach.

Whisper na calej kwestii (zwlaszcza z --prompt) wygladza zajakniecia: "I każdego ranka dosta... I każdego ranka
dostaję..." wychodzi jako jedno czyste zdanie. Dlatego kazda kwestie z EDL dzielimy w pauzach (>= 0,15 s ponizej
-45 dB) i transkrybujemy kazdy kawalek osobno, bez promptu. Kawalek, ktory powtarza poczatek nastepnego,
to falstart - kwestia powinna startowac od powtorzenia (zmiana startu w SEGS w aroll.py).

Uzycie: uv run --no-project --with numpy python3 -I kawalki.py [nr_kwestii ...]
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SRC = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
SILENCE_DB, MIN_PAUSE = -45.0, 0.15


def main():
    with wave.open(str(SRC)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 100, sr // 50
    edl = json.loads((P / "aroll/edl.json").read_text())
    only = [int(a) for a in sys.argv[1:]]
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "c.wav"
        for e in edl:
            if only and e["i"] not in only:
                continue
            a, b = e["a_in"], e["speech"][1] + 0.15
            seg = x[int(a * sr):int(b * sr)]
            n = max(1, (len(seg) - win) // hop)
            db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i * hop:i * hop + win] ** 2)) + 1e-7) for i in range(n)])
            bounds, start = [a], None
            for i, v in enumerate(db):
                if v < SILENCE_DB and start is None:
                    start = i
                if v >= SILENCE_DB and start is not None:
                    if (i - start) * 0.01 >= MIN_PAUSE:
                        bounds += [a + start * 0.01 + 0.01, a + i * 0.01 + 0.01]
                    start = None
            bounds.append(b)
            chunks = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds) - 1, 2) if bounds[k + 1] - bounds[k] > 0.12]
            print(f"== {e['i']} {e['text'][:70]}")
            for s, t in chunks:
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0, s - 0.05):.3f}",
                                "-to", f"{t + 0.05:.3f}", "-i", str(SRC), "-c:a", "pcm_s16le", str(f)], check=True)
                r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-np"],
                                   capture_output=True, text=True)
                print(f"   {s:7.2f}-{t:7.2f}  {' '.join(r.stdout.split())}")


if __name__ == "__main__":
    main()

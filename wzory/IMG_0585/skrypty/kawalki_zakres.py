#!/usr/bin/env python3
"""Kawalki miedzy pauzami w dowolnym zakresie nagrania (przed wyborem dubli), whisper bez promptu.

Uzycie: uv run --no-project --with numpy python3 -I kawalki_zakres.py OD DO [OD DO ...] [--pauza 0.15] [--db -45]
"""
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SRC = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"


def main():
    args = sys.argv[1:]
    min_pause, sil = 0.15, -45.0
    if "--pauza" in args:
        k = args.index("--pauza"); min_pause = float(args[k + 1]); del args[k:k + 2]
    if "--db" in args:
        k = args.index("--db"); sil = float(args[k + 1]); del args[k:k + 2]
    rng = [(float(args[i]), float(args[i + 1])) for i in range(0, len(args), 2)]
    with wave.open(str(SRC)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 100, sr // 50
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "c.wav"
        for a, b in rng:
            seg = x[int(a * sr):int(b * sr)]
            n = max(1, (len(seg) - win) // hop)
            db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i * hop:i * hop + win] ** 2)) + 1e-7) for i in range(n)])
            bounds, start = [a], None
            for i, v in enumerate(db):
                if v < sil and start is None:
                    start = i
                if v >= sil and start is not None:
                    if (i - start) * 0.01 >= min_pause:
                        bounds += [a + start * 0.01 + 0.01, a + i * 0.01 + 0.01]
                    start = None
            if start is not None:
                bounds += [a + start * 0.01 + 0.01, b]
            bounds.append(b)
            chunks = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds) - 1, 2) if bounds[k + 1] - bounds[k] > 0.12]
            print(f"== {a:.2f}-{b:.2f}")
            for s, t in chunks:
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0, s - 0.05):.3f}",
                                "-to", f"{t + 0.05:.3f}", "-i", str(SRC), "-c:a", "pcm_s16le", str(f)], check=True)
                r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-np"],
                                   capture_output=True, text=True)
                pk = 20 * np.log10(np.max(np.abs(x[int(s * sr):int(t * sr)])) + 1e-7)
                print(f"   {s:7.2f}-{t:7.2f} ({t - s:4.2f}s, szczyt {pk:5.1f} dB)  {' '.join(r.stdout.split())}")


if __name__ == "__main__":
    main()

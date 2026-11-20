#!/usr/bin/env python3
"""LTAS z ramek mowy w pasmach (dB wzgledem pasma 500-1000 Hz) - porownanie brzmienia glosu miedzy plikami.
Uzycie: uv run --no-project --with numpy python3 -I widmo.py PLIK.wav [PLIK2.wav ...]"""
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

BANDS = [(60, 100), (100, 150), (150, 250), (250, 400), (400, 600), (600, 1000), (1000, 2000), (2000, 3500),
         (3500, 5000), (5000, 7000), (7000, 10000), (10000, 16000)]


def ltas(path):
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "x.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(f)], check=True)
        with wave.open(str(f)) as w:
            sr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = 4096
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::n // 2]
    lvl = 10 * np.log10((fr ** 2).mean(axis=1) + 1e-12)
    sp = fr[lvl > lvl.max() - 30]
    S = (np.abs(np.fft.rfft(sp * np.hanning(n), axis=1)) ** 2).mean(axis=0)
    fq = np.fft.rfftfreq(n, 1 / sr)
    out = np.array([10 * np.log10(S[(fq >= a) & (fq < b)].mean() + 1e-20) for a, b in BANDS])
    ref = 10 * np.log10(S[(fq >= 500) & (fq < 1000)].mean())
    return out - ref


if __name__ == "__main__":
    rows = [(Path(p).parent.parent.name + "/" + Path(p).name, ltas(p)) for p in sys.argv[1:]]
    print(" " * 44 + "".join(f"{a:>6d}" for a, _ in BANDS))
    for name, v in rows:
        print(f"{name[-43:]:>43} " + "".join(f"{x:6.1f}" for x in v))
    for name, v in rows[1:]:
        print(f"{'roznica wzgl. 1.: ' + name[-24:]:>43} " + "".join(f"{x:+6.1f}" for x in v - rows[0][1]))

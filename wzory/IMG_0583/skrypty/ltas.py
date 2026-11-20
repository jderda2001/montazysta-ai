#!/usr/bin/env python3
"""LTAS (srednie widmo z ramek mowy) w pasmach tercjowych: porownanie barwy dwoch nagran glosu po wyrownaniu
glosnosci. Uzycie: uv run --no-project --with numpy python3 -I ltas.py WZORZEC.wav BADANY.wav"""
import sys
import wave

import numpy as np


def ltas(path):
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch).mean(axis=1)
    n = 4096
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::n // 2]
    lvl = 10 * np.log10((fr ** 2).mean(axis=1) + 1e-12)
    sp = fr[lvl > lvl.max() - 30]
    S = (np.abs(np.fft.rfft(sp * np.hanning(n), axis=1)) ** 2).mean(axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    bands = [80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]
    out = []
    for c in bands:
        m = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))
        out.append(10 * np.log10(S[m].sum() + 1e-20))
    out = np.array(out)
    return bands, out - 10 * np.log10(np.sum(10 ** (out / 10)))


b, a = ltas(sys.argv[1])
_, c = ltas(sys.argv[2])
print("pasmo Hz   wzorzec  badany  roznica (badany - wzorzec)")
for k, bb in enumerate(b):
    print(f"{bb:7d}   {a[k]:6.1f}  {c[k]:6.1f}  {c[k] - a[k]:+5.1f}")

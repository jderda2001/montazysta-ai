#!/usr/bin/env python3
"""Obwiednia glosnosci (RMS w dB, okno 20 ms, krok 10 ms) dla zakresu czasu w nowym audio.
Wypisuje lokalne minima (doliny miedzy sylabami/slowami) i tekstowy wykres co 40 ms.

Uzycie: uv run --no-project --with numpy python3 -I obwiednia.py OD DO
"""
import sys
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
a, b = float(sys.argv[1]), float(sys.argv[2])
with wave.open(str(P / "audio/nowe_16k.wav")) as w:
    sr = w.getframerate()
    w.setpos(int(a * sr))
    x = np.frombuffer(w.readframes(int((b - a) * sr)), dtype=np.int16).astype(np.float32) / 32768
hop, win = sr // 100, sr // 50
n = (len(x) - win) // hop
rms = np.array([np.sqrt(np.mean(x[i * hop:i * hop + win] ** 2)) for i in range(n)])
db = 20 * np.log10(rms + 1e-7)
t = a + np.arange(n) * 0.01 + 0.01
# doliny: lokalne minima w oknie +-60 ms ponizej -38 dB
print("doliny (t, dB):")
for i in range(6, n - 6):
    if db[i] == db[i - 6:i + 7].min() and db[i] < -38:
        print(f"  {t[i]:8.2f}  {db[i]:6.1f}")
if "--wykres" in sys.argv:
    for i in range(0, n, 4):
        v = db[i:i + 4].max()
        print(f"{t[i]:8.2f} {v:6.1f} " + "#" * max(0, int((v + 60) / 1.5)))

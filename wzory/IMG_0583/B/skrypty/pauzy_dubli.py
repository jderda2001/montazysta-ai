#!/usr/bin/env python3
"""Dla podanych zakresow (OD-DO w nagraniu) wypisuje: poczatek i koniec mowy z obwiedni oraz pauzy wewnatrz.
Uzycie: uv run --no-project --with numpy python3 -I pauzy_dubli.py 12.4-14.9 18.1-25.9 ..."""
import sys
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
with wave.open(str(P / "audio/nowe_16k.wav")) as w:
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
hop, win = sr // 100, sr // 50
n = (len(x) - win) // hop
db = 20 * np.log10(np.sqrt(np.mean(np.lib.stride_tricks.sliding_window_view(x, win)[::hop][:n] ** 2, axis=1)) + 1e-7)
print(f"szum tla (5. percentyl): {np.percentile(db, 5):.1f} dB, mediana {np.median(db):.1f} dB, 95. percentyl {np.percentile(db, 95):.1f} dB")
for arg in sys.argv[1:]:
    a, b = map(float, arg.split("-"))
    i0, i1 = int((a - 0.4) * 100), int((b + 0.4) * 100)
    seg = db[i0:i1]
    sp = np.where(seg > -38)[0]
    # poczatek: pierwsze 3 kolejne klatki > -38; koniec: ostatnia klatka > -38
    on = next(i for i in range(len(seg) - 3) if all(seg[i:i + 3] > -38))
    off = sp[-1]
    out, start = [], None
    for i in range(on, off + 1):
        if seg[i] < -45 and start is None:
            start = i
        if seg[i] >= -45 and start is not None:
            if i - start >= 15:
                out.append((start, i))
            start = None
    t = lambda i: (i0 + i) * 0.01 + 0.01
    print(f"{a:7.2f}-{b:7.2f}: mowa {t(on):7.2f}-{t(off):7.2f} | pauzy: " + "  ".join(f"{t(s):.2f}-{t(e):.2f} ({(e - s) * 0.01:.2f}s)" for s, e in out))

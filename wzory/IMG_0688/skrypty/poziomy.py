#!/usr/bin/env python3
"""Poziom mowy kazdej kwestii (RMS z ramek aktywnych) -> ../analiza/poziomy.json.
Hooki sa nagrane o 3-7 dB glosniej niz korpus, a miedzy sasiednimi kwestiami bywa 5 dB roznicy. aroll.py i glos.py
wyrownuja to wzmocnieniem per kwestia: 80% roznicy do mediany, max +-4 dB (reszte robi kompresja w lancuchu glosu).

Uzycie (po `aroll.py --edl-only`): uv run --no-project --with numpy python3 -I poziomy.py
"""
import json
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
with wave.open(str(ROOT / "audio/nowe_16k.wav")) as w:
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
lv = {}
for h in [""]:
    for e in json.loads((ROOT / "aroll/edl.json").read_text()):
        if e.get("hold"):
            continue
        s, t = e["speech"]
        seg = x[int(s * sr):int(t * sr)]
        hop = sr // 100
        fr = seg[:len(seg) // hop * hop].reshape(-1, hop)
        db = 10 * np.log10((fr ** 2).mean(axis=1) + 1e-12)
        lv[f"{s:.2f}-{t:.2f}"] = round(float(10 * np.log10((fr[db > db.max() - 25] ** 2).mean() + 1e-12)), 2)
med = float(np.median(list(lv.values())))
out = {"mediana": round(med, 2), "poziom": lv,
       "gain_db": {k: round(float(np.clip(0.8 * (med - v), -4, 4)), 2) for k, v in lv.items()}}
(ROOT / "analiza/poziomy.json").write_text(json.dumps(out, indent=1))
for k, v in lv.items():
    print(f"{k:>15}  {v:6.1f} dB  ->  {out['gain_db'][k]:+.1f} dB")
print("mediana", round(med, 2))

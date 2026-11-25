#!/usr/bin/env python3
"""Pomiar przerw w zmontowanym glosie (audio/aroll.wav albo podany plik), w folderze projektu po aroll.py.

Jakub, 24.11.2026 (C4534-C4538): "dalej sa przerwy pomiedzy scinkami... pol sekundy albo sekunda... bardzo
niplynne, wycinaj to za kazdym razem". Cel: ok. 0,15 s ciszy na kazdym styku kwestii. Skrypt wypisuje:
  - kazda przerwe >= 0,25 s (prog -38 dBFS na glosie po masteringu), z oznaczeniem STYK albo "w kwestii";
  - srednia cisze na stykach kwestii.
Przerwa >= 0,25 s moze zostac tylko celowo (pauza przed puenta, dwukropek "prompt: kim jestem", przed CTA).
Kazda inna: zmniejsz margines albo ustaw dokladna granice kwestii ({"a_in": ...} / {"a_out": ...} w SEGS).
Czeste zrodlo dziury: ciche "mmm" / buczenie przed slowem (C4537: 0,72 s) - wytnij je dokladnym "a_in".

Uzycie: uv run --no-project --with numpy python3 -I skrypty/przerwy.py [plik]
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

P = Path.cwd()
src = Path(sys.argv[1]) if len(sys.argv) > 1 else P / "audio/aroll.wav"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + 320] ** 2)) + 1e-9) for i in range(0, len(x) - 320, 160)])
edl = json.loads((P / "aroll/edl.json").read_text())
koniec = edl[-1]["t_in"] + edl[-1]["speech"][1] - edl[-1]["a_in"]
ciecia = [e["t_in"] for e in edl[1:]]
PROG = -38

cisza = db < PROG
dziury, k = [], 0
while k < len(cisza):
    if cisza[k]:
        j = k
        while j < len(cisza) and cisza[j]:
            j += 1
        a, b = k / 100, j / 100
        if b - a >= 0.25 and a > 0.2 and b < koniec:
            dziury.append((a, b, any(a - 0.05 <= c <= b + 0.05 for c in ciecia)))
        k = j
    else:
        k += 1
for a, b, styk in dziury:
    print(f"  {a:6.2f}-{b:6.2f}  {b - a:.2f} s  {'STYK' if styk else 'w kwestii'}")
print(f"przerwy >= 0,25 s: {len(dziury)} (suma {sum(b - a for a, b, _ in dziury):.1f} s)")

na_stykach = []
for t in ciecia:
    i = int(t * 100)
    a = i
    while a > 0 and db[a] < PROG:
        a -= 1
    b = i
    while b < len(db) - 1 and db[b] < PROG:
        b += 1
    na_stykach.append((b - a) / 100)
if na_stykach:
    print(f"cisza na stykach: srednio {np.mean(na_stykach):.2f} s, najdluzsza {max(na_stykach):.2f} s (cel ok. 0,15 s)")

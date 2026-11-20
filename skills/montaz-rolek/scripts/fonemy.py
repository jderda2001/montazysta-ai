#!/usr/bin/env python3
"""Drobna obwiednia do ciecia w srodku slowa: co 20 ms glosnosc (dB) i liczba przejsc przez zero (setki na sekunde).

Po tym widac gloski bez sluchania: samogloska = glosno i malo przejsc (ponizej ok. 15), "s/sz/c/cz" = cicho i duzo
przejsc (powyzej ok. 80), zwarcie "p/t/k/d" i pauza = dolek. Tak wyszlo "sukce- cesu" w IMG_0591
(s-u-k-c-e [pauza] c-e-s-u) i miejsce ciecia miedzy "c" a "e", w ktorym sklejka daje czyste "sukcesu".

Uzycie: uv run --no-project --with numpy python3 -I fonemy.py PLIK.wav OD DO [OD DO ...]   (zwykle audio/nowe_16k.wav)
Wynik:  czas:dB/przejscia, np. 14.27: -28/05 (samogloska), 14.57: -37/99 (s)
"""
import sys
import wave

import numpy as np

w = wave.open(sys.argv[1])
sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
if w.getnchannels() > 1:
    x = x.reshape(-1, w.getnchannels()).mean(axis=1)
for a, b in zip(sys.argv[2::2], sys.argv[3::2]):
    a, b = float(a), float(b)
    out, t = [], a
    while t < b:
        s = x[int(t * sr):int((t + 0.02) * sr)]
        db = 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9)
        z = int(((s[:-1] * s[1:]) < 0).sum() / 0.02 / 100)
        out.append(f"{t:.2f}:{db:4.0f}/{z:02d}")
        t += 0.02
    print(f"--- {a}-{b} (czas:dB/przejscia)")
    print(" ".join(out))

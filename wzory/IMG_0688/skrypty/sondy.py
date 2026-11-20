#!/usr/bin/env python3
"""Sondy: zakres surowego nagrania dzielony w pauzach i transkrybowany kawalek po kawalku, bez promptu.
Uzycie: sondy.py WAV OD DO [OD DO ...] [--pauza 0.12] [--db -45]"""
import json, subprocess, sys, tempfile, wave
from pathlib import Path
import numpy as np
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = {sys.argv[i]: float(sys.argv[i + 1]) for i in range(len(sys.argv)) if sys.argv[i].startswith("--")}
if opt:
    args = [a for a in args if a not in [str(v) for v in opt.values()] and a not in [sys.argv[i + 1] for i in range(len(sys.argv)) if sys.argv[i].startswith("--")]]
wav = args[0]
rng = [(float(args[i]), float(args[i + 1])) for i in range(1, len(args) - 1, 2)]
PAUZA, DB = opt.get("--pauza", 0.12), opt.get("--db", -45.0)
with wave.open(wav) as w:
    sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
hop, win = sr // 100, sr // 50
with tempfile.TemporaryDirectory() as td:
    for a, b in rng:
        seg = x[int(a * sr):int(b * sr)]
        n = (len(seg) - win) // hop
        db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i * hop:i * hop + win] ** 2)) + 1e-7) for i in range(n)])
        loud = db > DB
        chunks, i = [], 0
        while i < n:
            if loud[i]:
                j = i
                last = i
                while j < n and (loud[j] or (j - last) * 0.01 < PAUZA):
                    if loud[j]: last = j
                    j += 1
                chunks.append((a + i * 0.01, a + last * 0.01 + 0.02)); i = j
            else: i += 1
        print(f"=== {a:.2f}-{b:.2f}")
        for k, (ca, cb) in enumerate(chunks):
            if cb - ca < 0.06: continue
            f = Path(td) / f"c{k}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, ca - 0.08):.3f}", "-to", f"{cb + 0.08:.3f}", "-i", wav, "-af", "apad=pad_dur=0.4", "-c:a", "pcm_s16le", str(f)], check=True)
            subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-np", "-nt", "-otxt", "-of", str(f.with_suffix(""))], capture_output=True)
            t = f.with_suffix(".txt").read_text().strip().replace("\n", " ") if f.with_suffix(".txt").exists() else "?"
            pk = 20 * np.log10(np.abs(x[int(ca * sr):int(cb * sr)]).max() + 1e-7)
            print(f"  {ca:7.2f}-{cb:7.2f} ({cb - ca:4.2f}s, szczyt {pk:5.1f} dB) | {t}")

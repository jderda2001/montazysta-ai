#!/usr/bin/env python3
"""Kontrola synchronizacji A-rollu: dla kazdej kwestii porownuje dzwiek A-rollu (nowe nagranie)
z dzwiekiem telefonu z tych samych klatek wideo. Lag ~0 ms = usta zgadzaja sie z dzwiekiem.
Uzycie: uv run --no-project --with numpy python3 -I sprawdz_sync.py"""
import json, subprocess, tempfile, wave
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent.parent
edl = json.loads((P / "aroll/edl.json").read_text())
VIDEO = Path.home() / "Downloads/IMG_0576.MOV"
def rd(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
def lag(a, b, maxlag):
    n = len(a) + len(b); nfft = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(a, nfft) * np.conj(np.fft.rfft(b, nfft)), nfft)
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]])
    return int(np.argmax(c)) - maxlag
with tempfile.TemporaryDirectory() as td:
    for e in edl:
        d = e["t_out"] - e["t_in"]
        a, b = Path(td) / "a.wav", Path(td) / "b.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{e['t_in']:.4f}", "-t", f"{d:.4f}", "-i", str(P / "aroll/aroll.mp4"),
                        "-ac", "1", "-ar", "16000", str(a)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{e['v_in']:.4f}", "-t", f"{d:.4f}", "-i", str(VIDEO),
                        "-map", "0:a:0", "-ac", "1", "-ar", "16000", str(b)], check=True)
        x, y = rd(a), rd(b)
        m = min(len(x), len(y))
        l = lag(x[:m] - x[:m].mean(), y[:m] - y[:m].mean(), 1600)
        print(f"kwestia {e['i']}: przesuniecie dzwieku wzgledem obrazu {l / 16:+.1f} ms")

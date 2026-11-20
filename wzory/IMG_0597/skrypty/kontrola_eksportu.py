#!/usr/bin/env python3
"""Kontrola gotowego eksportu przed oddaniem.

1. Glosnosc: ebur128 (cel -14,0 LUFS, szczyt <= -1,5 dBFS).
2. Dzwiek = zamierzona sciezka glosu (przesuniecie 0 ms, roznica na poziomie szumu AAC ok. -30 dB lub nizej).
   Duza roznica znaczy, ze w renderze jest inny dzwiek albo dwa zmiksowane.
3. Transkrypcja calego filmu kawalkami miedzy pauzami (>= 0,15 s ponizej -45 dB): szukaj powtorzen i falstartow.
   "Dziekuje." na samej ciszy to halucynacja whispera, nie blad montazu.

Uzycie: uv run --no-project --with numpy python3 -I kontrola_eksportu.py FILM.mp4 [GLOS.wav]
"""
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def read(p):
    with wave.open(str(p)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return sr, x.reshape(-1, ch).mean(axis=1)


def main():
    film = sys.argv[1]
    glos = sys.argv[2] if len(sys.argv) > 2 else None
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", film, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary"):]
    print(f"glosnosc: {re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1)} LUFS, "
          f"szczyt {re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1)} dBFS (cel -14,0 / <= -1,5)")
    with tempfile.TemporaryDirectory() as td:
        a48 = Path(td) / "a48.wav"
        subprocess.run(FF + ["-i", film, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(a48)], check=True)
        sr, f = read(a48)
        if glos:
            g48 = Path(td) / "g48.wav"
            subprocess.run(FF + ["-i", glos, "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(g48)], check=True)
            _, g = read(g48)
            n = min(len(f), len(g))
            x, y = f[:min(n, sr * 30)], g[:min(n, sr * 30)]
            M = 1 << (2 * len(x) - 1).bit_length()
            c = np.fft.irfft(np.fft.rfft(x, M) * np.conj(np.fft.rfft(y, M)), M)
            c = np.concatenate([c[-2400:], c[:2401]])
            lag = (np.argmax(c) - 2400) / sr * 1000
            res = 20 * np.log10(np.sqrt(np.mean((f[:n] - g[:n]) ** 2)) / np.sqrt(np.mean(g[:n] ** 2)))
            print(f"dzwiek vs {Path(glos).name}: przesuniecie {lag:+.2f} ms, roznica {res:+.1f} dB")
        hop, win = sr // 100, sr // 50
        db = np.array([20 * np.log10(np.sqrt(np.mean(f[i * hop:i * hop + win] ** 2)) + 1e-7)
                       for i in range((len(f) - win) // hop)])
        bounds, start = [0.0], None
        for i, v in enumerate(db):
            if v < -45 and start is None:
                start = i
            if v >= -45 and start is not None:
                if i - start >= 15:
                    bounds += [start * 0.01 + 0.01, i * 0.01 + 0.01]
                start = None
        bounds.append(len(f) / sr)
        chunks = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds) - 1, 2) if bounds[k + 1] - bounds[k] > 0.12]
        print("transkrypcja kawalkami (szukaj powtorzen):")
        c16 = Path(td) / "c.wav"
        for s0, t0 in chunks:
            subprocess.run(FF + ["-ss", f"{max(0, s0 - 0.05):.3f}", "-to", f"{t0 + 0.05:.3f}", "-i", str(a48), "-ar", "16000",
                                 "-c:a", "pcm_s16le", str(c16)], check=True)
            out = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(c16), "-l", "pl", "-nt", "-np"],
                                 capture_output=True, text=True).stdout
            print(f"  {s0:6.2f}-{t0:6.2f}  {' '.join(out.split())}")


if __name__ == "__main__":
    main()

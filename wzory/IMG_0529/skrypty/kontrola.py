#!/usr/bin/env python3
"""Kontrola zmontowanego dzwieku: dzieli ../audio/montaz_surowy_16k.wav w pauzach (>= 0,15 s) i transkrybuje KAZDY
kawalek osobno, bez promptu. Oznacza kawalki przy prawdziwych cieciach (*) - tam szukamy resztek slow, falstartow
i szumow (whisper zamienia je w "Dziekuje za uwage", "Wszystkie prawa zastrzezone" itp.).

Uzycie: uv run --no-project --with numpy python3 -I kontrola.py [od_s do_s] [--plik FILM_LUB_WAV]
Wynik:  ../analiza/kontrola.txt
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
THR, MIN_PAUSE = -47.0, 0.15
SUSPECT = ("dziękuj", "prawa zastrz", "napisy", "amara", "oglądanie", "subskryb")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    plik = sys.argv[sys.argv.index("--plik") + 1] if "--plik" in sys.argv else None
    if plik:
        args = [a for a in args if a != plik]
    lo, hi = (float(args[0]), float(args[1])) if len(args) > 1 else (0, 1e9)
    src = P / "audio/montaz_surowy_16k.wav"
    if plik:
        src = Path(tempfile.gettempdir()) / "kontrola_16k.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", plik, "-ac", "1", "-ar", "16000",
                        "-c:a", "pcm_s16le", str(src)], check=True)
    edl = json.loads((P / "aroll/edl.json").read_text())
    cuts = [e["t_in"] for k, e in enumerate(edl) if k > 0 and not edl[k - 1]["cont"]]
    with wave.open(str(src)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 100, sr // 50
    n = (len(x) - win) // hop
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    db = 20 * np.log10(np.sqrt(np.mean(x[idx] ** 2, axis=1)) + 1e-7)
    sp = db >= THR
    chunks, k = [], 0
    while k < n:
        if not sp[k]:
            k += 1
            continue
        s = k
        while True:
            while k < n and sp[k]:
                k += 1
            j = k
            while j < n and not sp[j]:
                j += 1
            if j < n and (j - k) * 0.01 < MIN_PAUSE:
                k = j
                continue
            break
        a, b = s * 0.01, k * 0.01 + 0.02
        if b - a >= 0.08 and lo <= a <= hi:
            chunks.append((a, b))
    with tempfile.TemporaryDirectory() as td:
        files = []
        for i, (a, b) in enumerate(chunks):
            f = Path(td) / f"c{i:04d}.wav"
            seg = x[int(max(0, a - 0.05) * sr):int((b + 0.05) * sr)]
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes((seg * 32767).astype(np.int16).tobytes())
            files.append(f)
        cmd = ["whisper-cli", "-m", str(MODEL), "-l", "pl", "-ojf", "-np", "-sns"]
        for f in files:
            cmd += ["-f", str(f)]
        subprocess.run(cmd, capture_output=True, check=True)
        lines = []
        for (a, b), f in zip(chunks, files):
            d = json.loads(Path(str(f) + ".json").read_text())
            txt = " ".join(s["text"].strip() for s in d["transcription"]).strip()
            near = any(a - 0.7 <= c <= b + 0.7 for c in cuts)
            shot = max(e["i"] for e in edl if e["t_in"] <= a + 0.001)
            flag = ("*" if near else " ") + ("!" if any(s in txt.lower() for s in SUSPECT) or b - a < 0.35 else " ")
            lines.append(f"{flag} {a:7.2f}-{b:7.2f} [{shot:3d}] {txt}")
    (P / "analiza/kontrola.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Kontrola fragmentow: whisper (slowa + DTW, bez promptu) i obwiednia glosnosci dla podanych okien.

Uzycie: uv run --no-project --with numpy python3 -I sprawdz.py m7:43.6-46.4 m8:21.8-22.6 ...
        (dodaj --wykres, zeby zobaczyc obwiednie co 50 ms)
"""
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"


def main():
    wins = [a for a in sys.argv[1:] if not a.startswith("--")]
    plot = "--wykres" in sys.argv
    src = {}
    with tempfile.TemporaryDirectory() as td:
        files = []
        for k, wdef in enumerate(wins):
            name, rng = wdef.split(":")
            a, b = map(float, rng.split("-"))
            if name not in src:
                with wave.open(str(P / f"audio/{name}_16k.wav")) as w:
                    src[name] = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768,
                                 w.getframerate())
            x, sr = src[name]
            seg = x[int(a * sr):int(b * sr)]
            f = Path(td) / f"w{k}.wav"
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
            files.append((wdef, a, f, seg, sr))
        cmd = ["whisper-cli", "-m", str(MODEL), "-l", "pl", "-ml", "1", "-sow", "-dtw", "large.v3.turbo", "-nfa",
               "-ojf", "-np"]
        for _, _, f, _, _ in files:
            cmd += ["-f", str(f)]
        subprocess.run(cmd, capture_output=True, check=True)
        for wdef, a, f, seg, sr in files:
            d = json.loads(Path(str(f) + ".json").read_text())
            words = []
            for s in d["transcription"]:
                toks = [t for t in s.get("tokens", []) if re.search(r"\w", t["text"]) and not t["text"].startswith("[_")]
                if s["text"].strip() and toks:
                    words.append(f"{a + max(t['t_dtw'] for t in toks) / 100:.2f}<{s['text'].strip()}")
            print(f"== {wdef}:  " + "  ".join(words) + "   (czas = KONIEC slowa)")
            hop = sr // 20
            n = len(seg) // hop
            db = [20 * np.log10(np.sqrt(np.mean(seg[i * hop:(i + 1) * hop] ** 2)) + 1e-7) for i in range(n)]
            if plot:
                for i in range(n):
                    print(f"   {a + i * 0.05:8.2f} {db[i]:6.1f} " + "#" * max(0, int((db[i] + 62) / 1.5)))
            else:
                print("   " + "".join(" .:-=+*#%@"[min(9, max(0, int((v + 62) / 5)))] for v in db) + f"   (co 50 ms od {a:.2f})")


if __name__ == "__main__":
    main()

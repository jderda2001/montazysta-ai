#!/usr/bin/env python3
"""Mapa nagrania: dzieli oba pliki z mikrofonu (m7 = wstep, m8 = reszta) na kawalki mowy miedzy pauzami
(>= MIN_PAUSE ponizej progu) i transkrybuje KAZDY kawalek osobno, bez promptu (whisper na calym dublu
wygladza falstarty i powtorzenia - zob. notatki z IMG_0526). Jedno wywolanie whisper-cli na wszystkie kawalki.

Uzycie: uv run --no-project --with numpy python3 -I kawalki.py
Wynik:  ../analiza/kawalki.json  [{id, src, a, b, v_a, v_b, gap, text}]  (a/b - czas w pliku audio, v_* - czas w wideo)
        ../analiza/kawalki.txt   czytelna lista
"""
import json
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
# prog ciszy per plik (m8 ma wyzszy szum tla i glosniejsza mowe niz m7)
SRC = {"m7": -50.0, "m8": -45.0}
MIN_PAUSE, MIN_CHUNK, PAD = 0.15, 0.12, 0.05


def envelope(x, sr):
    hop, win = sr // 100, sr // 50
    n = max(1, (len(x) - win) // hop)
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    return 20 * np.log10(np.sqrt(np.mean(x[idx] ** 2, axis=1)) + 1e-7)


def chunks_for(name, thr):
    with wave.open(str(P / f"audio/{name}_16k.wav")) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    db = envelope(x, sr)
    speech = db >= thr
    out, k, n = [], 0, len(db)
    while k < n:
        if not speech[k]:
            k += 1
            continue
        s = k
        while True:
            while k < n and speech[k]:
                k += 1
            j = k
            while j < n and not speech[j]:
                j += 1
            if j < n and (j - k) * 0.01 < MIN_PAUSE:
                k = j  # krotka przerwa - ten sam kawalek
                continue
            break
        a, b = s * 0.01, k * 0.01 + 0.02
        if b - a >= MIN_CHUNK:
            out.append((round(a, 2), round(b, 2)))
    return out, len(x) / sr


def main():
    offs = {n: json.loads((P / f"analiza/sync_{n}.json").read_text())["offset"] for n in SRC}
    items = []
    with tempfile.TemporaryDirectory() as td:
        files = []
        for name, thr in SRC.items():
            ch, dur = chunks_for(name, thr)
            src = P / f"audio/{name}_16k.wav"
            for i, (a, b) in enumerate(ch):
                f = Path(td) / f"{name}_{i:04d}.wav"
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0, a - PAD):.3f}",
                                "-to", f"{min(dur, b + PAD):.3f}", "-i", str(src), "-c:a", "pcm_s16le", str(f)], check=True)
                files.append(f)
                items.append({"id": f"{name}_{i:04d}", "src": name, "a": a, "b": b,
                              "v_a": round(a - offs[name], 2), "v_b": round(b - offs[name], 2)})
            print(f"{name}: {len(ch)} kawalkow", flush=True)
        cmd = ["whisper-cli", "-m", str(MODEL), "-l", "pl", "-ojf", "-np", "-sns"]
        for f in files:
            cmd += ["-f", str(f)]
        subprocess.run(cmd, capture_output=True, check=True)
        for it, f in zip(items, files):
            d = json.loads(Path(str(f) + ".json").read_text())
            it["text"] = " ".join(s["text"].strip() for s in d["transcription"]).strip()
    prev = {}
    for it in items:
        it["gap"] = round(it["a"] - prev[it["src"]], 2) if it["src"] in prev else None
        prev[it["src"]] = it["b"]
    (P / "analiza/kawalki.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
    lines = [f"{it['id']}  {it['a']:7.2f}-{it['b']:7.2f}  v{it['v_a']:7.2f}  "
             f"gap {it['gap'] if it['gap'] is not None else '-':>5}  | {it['text']}" for it in items]
    (P / "analiza/kawalki.txt").write_text("\n".join(lines) + "\n")
    print(f"zapisano {len(items)} kawalkow")


if __name__ == "__main__":
    main()

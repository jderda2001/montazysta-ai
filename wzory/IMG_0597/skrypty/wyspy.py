#!/usr/bin/env python3
"""Dzieli nowe audio na wysepki mowy (detekcja ciszy) i transkrybuje kazda osobno (whisper, slowa + DTW).

Uzycie: python3 -I wyspy.py
Wynik:  ../analiza/wyspy.json  [{i, a, b, v_a, v_b, words:[[od, do, tekst], ...]}]  (a/b - czas w nowym audio,
        v_a/v_b - czas w wideo; slowa w czasie nowego audio)
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
WAV = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
PROMPT = "PerfOS, AI, reklamy na Facebooku i Instagramie, Meta Ads, budżet, tysiąc złotych, 175 zł, 3700 zł, album, książki, sklep internetowy, grafiki, teksty, raport."
OFFSET = json.loads((P / "analiza/sync.json").read_text())["offset"]


def islands(wav, noise="-42dB", d=0.30, merge=0.35, min_len=0.25):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", f"silencedetect=noise={noise}:d={d}",
                        "-f", "null", "-"], capture_output=True, text=True)
    ev = re.findall(r"silence_(start|end): ([0-9.]+)", r.stderr)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(wav)], capture_output=True, text=True).stdout)
    out, cur = [], 0.0
    for k, v in ev:
        t = float(v)
        if k == "start":
            if t > cur:
                out.append([cur, t])
        else:
            cur = t
    if dur > cur:
        out.append([cur, dur])
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] < merge:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged if b - a >= min_len]


def transcribe(wav, a, b, td, i):
    seg = Path(td) / f"w{i}.wav"
    a0 = max(0.0, a - 0.15)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a0:.3f}", "-to", f"{b + 0.15:.3f}",
                    "-i", str(wav), "-c:a", "pcm_s16le", str(seg)], check=True)
    subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(seg), "-l", "pl", "-ml", "1", "-sow",
                    "-dtw", "large.v3.turbo", "-ojf", "-of", str(seg.with_suffix("")), "--prompt", PROMPT],
                   capture_output=True, check=True)
    d = json.loads(seg.with_suffix(".json").read_text())
    return [[round(s["offsets"]["from"] / 1000 + a0, 3), round(s["offsets"]["to"] / 1000 + a0, 3), s["text"].strip()]
            for s in d["transcription"] if s["text"].strip()]


def main():
    res = []
    with tempfile.TemporaryDirectory() as td:
        for i, (a, b) in enumerate(islands(WAV)):
            words = transcribe(WAV, a, b, td, i)
            res.append({"i": i, "a": round(a, 3), "b": round(b, 3), "v_a": round(a - OFFSET, 3),
                        "v_b": round(b - OFFSET, 3), "words": words})
            print(f"{i:3d} {a:7.2f}-{b:7.2f} (wideo {a-OFFSET:7.2f}) | {' '.join(w[2] for w in words)}", flush=True)
    (P / "analiza/wyspy.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

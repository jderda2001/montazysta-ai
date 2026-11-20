#!/usr/bin/env python3
"""Czasy slow (whisper + DTW) dla kazdego kawalka z ../analiza/kawalki.json, bez promptu, jedno wywolanie
whisper-cli na wszystkie kawalki. DTW dziala tylko z -nfa (bez tego t_dtw = -1).

Koniec slowa = t_dtw jego ostatniego tokenu z litera/cyfra (t_dtw w whisper.cpp 1.9.5 wypada ~na koncu tokenu).
Start slowa = koniec poprzedniego slowa, przesuniety do konca pauzy / powrotu glosnosci (logika z IMG_0526/slowa.py).

Uzycie: uv run --no-project --with numpy python3 -I slowa_kawalki.py
Wynik:  ../analiza/slowa_kawalki.json  {id: [[od, do, tekst], ...]}  (czas w pliku audio m7/m8)
        ../analiza/slowa_kawalki.txt   czytelnie
"""
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
PAD = 0.08
# progi wzgledem pliku: m7 jest ~4,5 dB cichszy niz m8
THR = {"m7": (-43.0, -50.0), "m8": (-38.0, -45.0)}  # (SPEECH_DB, SILENCE_DB)


def envelope(x, sr):
    hop, win = sr // 100, sr // 50
    n = max(1, (len(x) - win) // hop)
    idx = np.arange(n)[:, None] * hop + np.arange(win)[None, :]
    return 20 * np.log10(np.sqrt(np.mean(x[idx] ** 2, axis=1)) + 1e-7)


def onset_after(db, t, sp, need=3):
    i = max(0, int(t * 100))
    while i + need <= len(db):
        if all(db[i:i + need] > sp):
            return i * 0.01 + 0.01
        i += 1
    return None


def pauses(db, si, min_len=0.12):
    out, start = [], None
    for i, v in enumerate(db):
        if v < si:
            start = i if start is None else start
        else:
            if start is not None and (i - start) * 0.01 >= min_len:
                out.append((start * 0.01 + 0.01, i * 0.01 + 0.01))
            start = None
    if start is not None and (len(db) - start) * 0.01 >= min_len:
        out.append((start * 0.01 + 0.01, len(db) * 0.01 + 0.01))
    return out


def rise_after(db, t, sp, max_wait=0.04, need=3):
    i0 = max(0, int(t * 100))
    dip = next((i for i in range(i0, min(len(db), i0 + int(max_wait * 100) + 1)) if db[i] <= sp), None)
    return None if dip is None else onset_after(db, dip * 0.01, sp, need)


def words_dtw(d, db, pz, onset, seg_len, sp):
    words, prev_end, nxt = [], onset, onset
    for s in d["transcription"]:
        txt = s["text"].strip()
        toks = [t for t in s.get("tokens", []) if not t["text"].startswith("[_") and t["text"].strip()]
        alnum = [t for t in toks if re.search(r"\w", t["text"])]
        if not txt or not alnum:
            continue
        if any(t.get("t_dtw", -1) < 0 for t in toks):
            raise SystemExit("Brak czasow DTW (t_dtw = -1) - whisper musi dostac -dtw i -nfa")
        end = min(max(t["t_dtw"] for t in alnum) / 100, seg_len)
        punct = prev_end + 0.01 < nxt < end - 0.05
        start = max(prev_end, nxt - 0.15) if punct else prev_end
        for a, b in pz:
            if start - 0.02 < b < end - 0.03:
                start = max(start, b)
        r = rise_after(db, start, sp)
        if r is not None and r < end - 0.02:
            start = max(start, r)
        elif punct and nxt > start:
            start = nxt
        if words:
            start = max(start, words[-1][0] + 0.03)
        end = max(end, start + 0.05)
        words.append([start, end, txt])
        prev_end = end
        nxt = max(end, max(t["t_dtw"] for t in toks) / 100)
    return words


def main():
    items = json.loads((P / "analiza/kawalki.json").read_text())
    src = {}
    for n in THR:
        with wave.open(str(P / f"audio/{n}_16k.wav")) as w:
            src[n] = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768,
                      w.getframerate())
    out = {}
    with tempfile.TemporaryDirectory() as td:
        files = []
        for it in items:
            x, sr = src[it["src"]]
            a0 = max(0.0, it["a"] - PAD)
            b0 = min(len(x) / sr, it["b"] + PAD)
            seg = x[int(a0 * sr):int(b0 * sr)]
            f = Path(td) / f"{it['id']}.wav"
            with wave.open(str(f), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(sr)
                w.writeframes((np.clip(seg, -1, 1) * 32767).astype(np.int16).tobytes())
            files.append((it, f, a0, seg, sr))
        cmd = ["whisper-cli", "-m", str(MODEL), "-l", "pl", "-ml", "1", "-sow", "-dtw", "large.v3.turbo", "-nfa",
               "-ojf", "-np", "-sns"]
        for _, f, _, _, _ in files:
            cmd += ["-f", str(f)]
        subprocess.run(cmd, capture_output=True, check=True)
        for it, f, a0, seg, sr in files:
            sp, si = THR[it["src"]]
            d = json.loads(Path(str(f) + ".json").read_text())
            db = envelope(seg, sr)
            pz = pauses(db, si)
            onset = onset_after(db, 0.0, sp) or 0.0
            ws = words_dtw(d, db, pz, onset, len(seg) / sr, sp)
            out[it["id"]] = [[round(a + a0, 3), round(b + a0, 3), t] for a, b, t in ws]
    (P / "analiza/slowa_kawalki.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    lines = []
    for it in items:
        ws = out[it["id"]]
        lines.append(f"{it['id']} [{it['a']:.2f}-{it['b']:.2f}] " + " ".join(f"{a:.2f}|{t}" for a, b, t in ws))
    (P / "analiza/slowa_kawalki.txt").write_text("\n".join(lines) + "\n")
    print(f"slowa dla {len(out)} kawalkow")


if __name__ == "__main__":
    main()

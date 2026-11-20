#!/usr/bin/env python3
"""Dokladniejsze czasy slow: transkrypcja kazdego ujecia osobno (whisper + DTW), przesuniecie o poczatek ujecia,
i dociagniecie pierwszego slowa ujecia do faktycznego poczatku mowy (detekcja ciszy).

Uzycie: python3 -I slowa.py A B
Wynik: ../audio/slowa_<V>.json (ten sam format co whisper -ojf, czytany przez kompozycja.py)
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
PROMPT = "Kancelarie odszkodowawcze, służebność przesyłu, przedstawiciele, leady, wolumen, Trybunał Konstytucyjny."


def speech_onsets(wav):
    """Lista (start, koniec) fragmentow mowy w pliku wg detekcji ciszy."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "silencedetect=noise=-34dB:d=0.04",
                        "-f", "null", "-"], capture_output=True, text=True)
    ev = re.findall(r"silence_(start|end): ([0-9.]+)", r.stderr)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(wav)], capture_output=True, text=True).stdout)
    islands, cur = [], 0.0
    for k, v in ev:
        t = float(v)
        if k == "start":
            if t - cur > 0.05:
                islands.append((cur, t))
        else:
            cur = t
    if dur - cur > 0.05:
        islands.append((cur, dur))
    return islands


def run(version):
    edl = json.loads((P / f"aroll/edl_{version}.json").read_text())
    wav = P / f"audio/aroll_{version}.wav"
    out, report = [], []
    with tempfile.TemporaryDirectory() as td:
        for e in edl:
            seg = Path(td) / f"s{e['i']}.wav"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{e['t_in']:.3f}",
                            "-to", f"{e['t_out']:.3f}", "-i", str(wav), "-c:a", "pcm_s16le", str(seg)], check=True)
            subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(seg), "-l", "pl", "-ml", "1", "-sow",
                            "-dtw", "large.v3.turbo", "-ojf", "-of", str(seg.with_suffix("")), "--prompt", PROMPT],
                           capture_output=True, check=True)
            d = json.loads(seg.with_suffix(".json").read_text())
            words = [[s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, s["text"].strip()]
                     for s in d["transcription"] if s["text"].strip()]
            isl = speech_onsets(seg)
            if words and isl:
                onset = isl[0][0]
                delta = onset - words[0][0]
                # pierwsze slowo zaczyna sie za wczesnie/za pozno wzgledem realnej mowy -> dociagnij
                if abs(delta) > 0.04:
                    words[0][0] = onset
                    if words[0][1] <= onset:
                        words[0][1] = onset + 0.15
                report.append(f"{e['i']:2d} {e['t_in']:6.2f} onset {onset:5.2f} whisper {onset-delta:5.2f} "
                              f"(korekta {delta:+.2f}) | {' '.join(w[2] for w in words)[:60]}")
                # slowa nie moga zaczynac sie w ciszy dluzszej niz 0.15 s: przesun na najblizszy start mowy
                for w in words[1:]:
                    inside = any(a - 0.15 <= w[0] <= b for a, b in isl)
                    if not inside:
                        nxt = [a for a, b in isl if a > w[0]]
                        if nxt:
                            w[0] = nxt[0]
            for w in words:
                out.append({"offsets": {"from": int(round((w[0] + e["t_in"]) * 1000)),
                                        "to": int(round((w[1] + e["t_in"]) * 1000))}, "text": " " + w[2]})
    target = P / f"audio/slowa_{version}.json"
    if target.exists() and not (P / f"audio/slowa_{version}_v1.json").exists():
        target.rename(P / f"audio/slowa_{version}_v1.json")
    target.write_text(json.dumps({"transcription": out}, ensure_ascii=False, indent=1))
    print(f"== {version}: {len(out)} slow -> {target.name}")
    print("\n".join(report))


if __name__ == "__main__":
    for v in sys.argv[1:] or ["A", "B"]:
        run(v)

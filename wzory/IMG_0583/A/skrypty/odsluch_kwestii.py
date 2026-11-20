#!/usr/bin/env python3
"""Odsluch gotowego pliku kwestia po kwestii (granice z EDL), bez promptu: szuka powtorzen, falstartow i ucietych
slow tam, gdzie kontrola_eksportu.py zlala kilka kwestii w jeden dlugi kawalek (whisper gubi wtedy zdania).
Uzycie: python3 -I odsluch_kwestii.py FILM.mp4   (z folderu wersji: czyta ../aroll/edl.json wzgledem skryptu)"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
edl = json.loads((P / "aroll/edl.json").read_text())
with tempfile.TemporaryDirectory() as td:
    full, c = Path(td) / "f.wav", Path(td) / "c.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sys.argv[1], "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(full)], check=True)
    for e in edl:
        end = min(e["t_out"], e["t_in"] + (e["speech"][1] - e["a_in"]) + 0.2)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{e['t_in']:.3f}", "-to", f"{end:.3f}", "-i", str(full), "-c:a", "pcm_s16le", str(c)], check=True)
        out = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(c), "-l", "pl", "-nt", "-np"], capture_output=True, text=True).stdout
        print(f"{e['i']:2d} {e['t_in']:6.2f}-{end:6.2f}  {' '.join(out.split())}")

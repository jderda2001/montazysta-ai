#!/usr/bin/env python3
"""Szybki podglad kadrow przed renderem A-rollu: jedna klatka ze srodka kazdego ujecia, po kadrowaniu, z linia
srodka i liniami 1/3. Sprawdza, czy twarz jest tam, gdzie ma byc (srodek twarzy podany w SEGS).
Uzycie: python3 -I podglad_kadrow.py WYNIK.jpg"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
_s = importlib.util.spec_from_file_location("aroll", Path(__file__).with_name("aroll.py"))
aroll = importlib.util.module_from_spec(_s)
_s.loader.exec_module(aroll)
edl = aroll.make_edl()
with tempfile.TemporaryDirectory() as td:
    n = 0
    for e in edl:
        for sh in e["shots"]:
            w, h, x, y = aroll.crop(sh["frame"], e["face"])
            t = e["v_in"] + sh["rel"] + sh["dur"] / 2
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(aroll.VIDEO), "-frames:v", "1", "-vf",
                            f"crop={w}:{h}:{x}:{y},scale=270:480,drawgrid=w=135:h=160:t=1:c=red@0.5",
                            f"{td}/{n:02d}.jpg"], check=True)
            n += 1
    cols = min(n, 9)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-pattern_type", "glob", "-i", f"{td}/*.jpg", "-vf",
                    f"tile={cols}x{-(-n // cols)}", "-frames:v", "1", sys.argv[1]], check=True)
print(n, "ujec ->", sys.argv[1])

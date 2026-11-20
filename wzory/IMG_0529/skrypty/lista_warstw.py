#!/usr/bin/env python3
"""Odtwarza ../hf/renders/warstwy.json z juz wyrenderowanych plikow (np. w trakcie renderu, do podgladu).
Uzycie: python3 -I lista_warstw.py
"""
import glob
import json
import os
from pathlib import Path

P = Path(__file__).resolve().parent.parent
R = P / "hf/renders"
items = [dict(m, typ="grafika") for m in json.loads((P / "hf/grafiki.json").read_text())]
items += [dict(m, typ="napisy", nazwa=m["plik"][:-5]) for m in json.loads((P / "hf/napisy.json").read_text())]
movs = {}
for m in sorted(glob.glob(str(R / "[on]_*.mov")), key=os.path.getmtime):
    b = os.path.basename(m)
    movs[b.rsplit("_", 1)[0] + ".html"] = b
out = [{"plik": m["plik"], "nazwa": m["nazwa"], "typ": m["typ"], "start": m["start"], "dlugosc": m["dlugosc"],
        "mov": movs[m["plik"]]} for m in items if m["plik"] in movs]
(R / "warstwy.json").write_text(json.dumps(out, indent=1))
print(f"{len(out)} z {len(items)} warstw gotowych")

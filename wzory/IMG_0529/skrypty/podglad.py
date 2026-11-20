#!/usr/bin/env python3
"""Podglad klatek gotowego montazu bez renderu calosci: A-roll (ujecie z aroll/ujecia) + wszystkie warstwy aktywne
w danej chwili (hf/renders/warstwy.json). Zapisuje PNG 1920x1080 i arkusz z miniaturami.

Uzycie: python3 -I podglad.py T1 T2 ... [--out katalog]
"""
import json
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def frame(t, out):
    edl = json.loads((P / "aroll/edl.json").read_text())
    lista = [l.split("'")[1] for l in (P / "aroll/lista.txt").read_text().splitlines()]
    e = max((x for x in edl if x["t_in"] <= t + 1e-6), key=lambda x: x["t_in"])
    k = edl.index(e)
    cmd = FF + ["-ss", f"{t - e['t_in']:.3f}", "-i", lista[k]]
    lay = [w for w in json.loads((P / "hf/renders/warstwy.json").read_text())
           if w["start"] <= t < w["start"] + w["dlugosc"] and (P / "hf/renders" / w["mov"]).exists()]
    fc = "[0:v]setpts=PTS-STARTPTS,scale=1920:1080,format=yuv444p[b0]"
    for j, w in enumerate(lay):
        cmd += ["-ss", f"{t - w['start']:.3f}", "-i", str(P / "hf/renders" / w["mov"])]
        fc += f";[{j + 1}:v]setpts=PTS-STARTPTS,scale=1920:1080[o{j}];[b{j}][o{j}]overlay=0:0:format=auto[b{j + 1}]"
    cmd += ["-filter_complex", fc, "-map", f"[b{len(lay)}]", "-frames:v", "1", str(out)]
    subprocess.run(cmd, check=True)
    return [w["nazwa"] for w in lay]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    od = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else P / "klatki/podglad"
    if "--out" in sys.argv:
        args = [a for a in args if a != str(od)]
    od.mkdir(parents=True, exist_ok=True)
    pngs = []
    for a in args:
        t = float(a)
        out = od / f"t_{t:07.2f}.png"
        names = frame(t, out)
        pngs.append(out)
        print(f"{t:7.2f}: {', '.join(names) or '(sam A-roll)'} -> {out}")
    if len(pngs) > 1:
        cols = 2
        cmd = FF[:]
        for pth in pngs:
            cmd += ["-i", str(pth)]
        fc = "".join(f"[{i}:v]scale=960:540[s{i}];" for i in range(len(pngs)))
        rows = (len(pngs) + cols - 1) // cols
        lay = "|".join(f"{(i % cols) * 960}_{(i // cols) * 540}" for i in range(len(pngs)))
        fc += "".join(f"[s{i}]" for i in range(len(pngs))) + f"xstack=inputs={len(pngs)}:layout={lay}:fill=black"
        subprocess.run(cmd + ["-filter_complex", fc, "-frames:v", "1", str(od / "arkusz.jpg")], check=True)
        print(f"arkusz: {od / 'arkusz.jpg'} ({rows} x {cols})")


if __name__ == "__main__":
    main()

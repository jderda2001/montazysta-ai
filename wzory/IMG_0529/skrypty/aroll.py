#!/usr/bin/env python3
"""A-roll odcinka (obraz) wg ../aroll/edl.json: kazde ujecie osobno z IMG_0529.MOV (4K HEVC 60p) -> kadr W/M/C,
grading jak w rolkach, 3840x2160 30p, HEVC VideoToolbox ~100 Mb/s; potem sklejenie (concat, bez ponownego kodowania).
Ujecia sa cache'owane po parametrach (zmiana jednego ujecia = render tylko jego).

Uzycie: python3 -I aroll.py [--workers 4]
Wynik:  ../aroll/aroll_video.mp4 (bez dzwieku; dzwiek: ../audio/montaz.wav)
"""
import concurrent.futures as cf
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

P = Path(__file__).resolve().parent.parent
VIDEO = Path.home() / "Downloads/IMG_0529.MOV"
OUT = P / "aroll"
PIECES = OUT / "ujecia"
FPS = 30
W, H = 3840, 2160
FRAMES = {  # (w, h, x, y) w px zrodla 3840x2160; twarz ~ (2170, 740)
    "W": (3840, 2160, 0, 0),
    "M": (3200, 1800, 570, 52),
    "C": (2744, 1544, 798, 120),
}
GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
ENC = ["-c:v", "hevc_videotoolbox", "-b:v", "100M", "-maxrate", "140M", "-tag:v", "hvc1", "-profile:v", "main",
       "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-an"]


def piece(e):
    n = round((e["t_out"] - e["t_in"] + e.get("video_extra", 0.0)) * FPS)
    w, h, x, y = FRAMES[e["frame"]]
    vf = (f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos," if e["frame"] != "W" else "") + \
        f"{GRADE},fps={FPS},format=yuv420p,setsar=1"
    key = hashlib.md5(json.dumps([e["v_in"], n, vf, ENC]).encode()).hexdigest()[:10]
    out = PIECES / f"p{e['i']:03d}_{key}.mp4"
    if not out.exists():
        tmp = out.with_suffix(".tmp.mp4")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-hwaccel", "videotoolbox",
                        "-ss", f"{e['v_in']:.4f}", "-i", str(VIDEO), "-vf", vf, "-frames:v", str(n),
                        "-r", str(FPS)] + ENC + [str(tmp)], check=True)
        tmp.rename(out)
    return out, n


def main():
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    edl = json.loads((OUT / "edl.json").read_text())
    PIECES.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with cf.ThreadPoolExecutor(workers) as ex:
        res = list(ex.map(piece, edl))
    keep = {p.name for p, _ in res}
    for f in PIECES.glob("p*.mp4"):
        if f.name not in keep:
            f.unlink()
    lst = OUT / "lista.txt"
    lst.write_text("".join(f"file '{p}'\n" for p, _ in res))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-movflags", "+faststart", str(OUT / "aroll_video.mp4")], check=True)
    nf = sum(n for _, n in res)
    print(f"aroll_video.mp4: {len(res)} ujec, {nf} klatek ({nf / FPS:.2f} s), {time.time() - t0:.0f} s renderu")


if __name__ == "__main__":
    main()

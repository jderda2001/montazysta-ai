#!/usr/bin/env python3
"""Film koncowy: A-roll (ujecia z aroll/ujecia) + warstwy HyperFrames (grafiki i napisy, ProRes 4444 z alfa)
+ glos C (audio/aroll_studio_gleboki.wav). Skladany w oknach po 60 s (mniej pamieci i miejsca), potem sklejany
bez ponownego kodowania i laczony z dzwiekiem.

Uzycie: python3 -I finalny.py [--bez-napisow] [--glos sciezka.wav] [--wyjscie plik.mp4]
Wynik:  ../render/odcinek.mp4 (3840x2160, 30 kl./s, HEVC ~45 Mb/s, AAC 320 kb/s) albo --wyjscie
"""
import concurrent.futures as cf
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

P = Path(__file__).resolve().parent.parent
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
FPS = 30
WIN = 60.0
ENC = ["-c:v", "hevc_videotoolbox", "-b:v", "45M", "-maxrate", "70M", "-tag:v", "hvc1", "-profile:v", "main",
       "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-an"]


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def window(k, w0, w1, edl, lista, layers, out):
    cmd, fc, vin = FF[:], [], []
    n = 0
    for e, f in zip(edl, lista):
        e_end = e["t_out"] + e.get("video_extra", 0.0)
        if e_end <= w0 + 1e-6 or e["t_in"] >= w1 - 1e-6:
            continue
        a, b = max(w0, e["t_in"]), min(w1, e_end)
        f0, f1 = round((a - e["t_in"]) * FPS), round((b - e["t_in"]) * FPS)  # dokladne numery klatek ujecia
        cmd += ["-i", f]
        fc.append(f"[{n}:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS[p{n}]")
        vin.append(f"[p{n}]")
        n += 1
    fc.append("".join(vin) + f"concat=n={len(vin)}:v=1:a=0,trim=duration={w1 - w0:.4f},format=yuv444p[b0]")
    lay = [w for w in layers if w["start"] < w1 and w["start"] + w["dlugosc"] > w0]
    for j, w in enumerate(lay):
        ss = max(0.0, w0 - w["start"])
        off = max(0.0, w["start"] - w0)
        cmd += ["-ss", f"{ss:.4f}", "-i", str(P / "hf/renders" / w["mov"])]
        fc.append(f"[{n + j}:v]setpts=PTS-STARTPTS+{off:.4f}/TB[o{j}];"
                  f"[b{j}][o{j}]overlay=0:0:format=auto:eof_action=pass:repeatlast=0[b{j + 1}]")
    fc.append(f"[b{len(lay)}]format=yuv420p,setsar=1,tpad=stop_mode=clone:stop=1[v]")
    nf = round((w1 - w0) * FPS)
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", str(nf), "-r", str(FPS)] + ENC + [str(out)]
    t0 = time.time()
    subprocess.run(cmd, check=True)
    return k, len(lay), time.time() - t0


def main():
    edl = json.loads((P / "aroll/edl.json").read_text())
    lista = [l.split("'")[1] for l in (P / "aroll/lista.txt").read_text().splitlines()]
    layers = json.loads((P / "hf/renders/warstwy.json").read_text())
    if "--bez-napisow" in sys.argv:
        layers = [w for w in layers if w["typ"] != "napisy"]
    missing = [w["mov"] for w in layers if not (P / "hf/renders" / w["mov"]).exists()]
    if missing:
        raise SystemExit(f"Brak {len(missing)} warstw (najpierw render_warstwy.py): {missing[:5]}")
    glos = Path(arg("--glos", str(P / "audio/glos_finalny.wav")))
    out = Path(arg("--wyjscie", str(P / "render/odcinek.mp4")))
    wd = P / "render/okna"
    wd.mkdir(parents=True, exist_ok=True)
    total = edl[-1]["t_out"] + edl[-1].get("video_extra", 0.0)
    bounds = []
    t = 0.0
    while t < total - 1e-6:
        bounds.append((t, min(total, t + WIN)))
        t += WIN
    a0 = 0.0
    if "--zakres" in sys.argv:  # tylko fragment (kontrola): --zakres OD DO (s), okna wyrownane do OD
        k = sys.argv.index("--zakres")
        a0, b0 = float(sys.argv[k + 1]), float(sys.argv[k + 2])
        bounds = [(a0, b0)]
        total = b0 - a0
    t0 = time.time()

    def key(a, b):  # okno zalezy od ujec, warstw i ustawien kodera w swoim zakresie
        lay = [w["mov"] for w in layers if w["start"] < b and w["start"] + w["dlugosc"] > a]
        pcs = [f for e, f in zip(edl, lista) if e["t_in"] < b and e["t_out"] + e.get("video_extra", 0.0) > a]
        return hashlib.md5(json.dumps([a, b, lay, pcs, ENC, "klatki-v2"]).encode()).hexdigest()[:10]
    files = [wd / f"w{k:02d}_{key(a, b)}.mp4" for k, (a, b) in enumerate(bounds)]
    todo = [k for k in range(len(bounds)) if not files[k].exists()]
    print(f"okien: {len(bounds)}, do zlozenia: {len(todo)} (reszta bez zmian)", flush=True)
    with cf.ThreadPoolExecutor(2) as ex:
        futs = [ex.submit(window, k, bounds[k][0], bounds[k][1], edl, lista, layers, files[k]) for k in todo]
        for f in cf.as_completed(futs):
            k, nl, dt = f.result()
            print(f"okno {k:2d} ({bounds[k][0]:6.1f}-{bounds[k][1]:6.1f} s): {nl:2d} warstw, {dt:5.1f} s", flush=True)
    lst = wd / "okna.txt"
    lst.write_text("".join(f"file '{f}'\n" for f in files))
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(FF + ["-f", "concat", "-safe", "0", "-i", str(lst), "-ss", f"{a0:.4f}", "-i", str(glos),
                         "-map", "0:v", "-map", "1:a",
                         "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-t", f"{total:.4f}",
                         "-movflags", "+faststart", str(out)], check=True)
    if "--zakres" not in sys.argv:
        for old in wd.glob("w*.mp4"):
            if old not in files:
                old.unlink()
    print(f"{out}: {total:.2f} s, {out.stat().st_size / 1e9:.2f} GB, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()

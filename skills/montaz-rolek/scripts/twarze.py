#!/usr/bin/env python3
"""Pomiar twarzy w ujeciach A-rollu -> ../analiza/twarze.json (do automatycznego kadrowania pod strefe bezpieczna).

Jakub, 18.11.2026: napisy maja stac w strefie bezpiecznej (do 1245 px), a w nagraniach, gdzie siedzi nisko albo pochyla
sie do kamery, broda siega 1200-1400 px. Zamiast zgadywac kadr na oko, mierzymy twarz w kazdej probce ujecia
systemowym wykrywaniem twarzy z macOS (Vision, bez pobierania czegokolwiek) i `aroll.py` dobiera zoom tak, zeby broda
konczyla sie przed napisami.

Uzycie (w folderze projektu, po `aroll.py --edl-only`):
  python3 -I skrypty/twarze.py [--flip]      # --flip: nagranie lustrzane (hflip przed kadrowaniem, jak w aroll.py)
Wynik: analiza/twarze.json  {"t": [x, y, w, h], ...}  (t = czas w nagraniu; prostokat twarzy w pikselach zrodla po obrocie,
os y od gory). Wymaga `~/.local/bin/twarz` (kompilacja: `swiftc -O -o ~/.local/bin/twarz scripts/twarz.swift`).
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

P = Path(__file__).resolve().parent.parent
FLIP = "--flip" in sys.argv
KROK = 0.4          # co ile sekund probka w ujeciu
SKALA = (540, 960)  # klatki do wykrywania (zrodlo 2160x3840, czyli /4)
TWARZ = Path.home() / ".local/bin/twarz"

spec = importlib.util.spec_from_file_location("aroll", P / "skrypty/aroll.py")
aroll = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aroll)
edl = json.loads((P / "aroll/edl.json").read_text())
czasy = set()
for e in edl:
    if e.get("hold"):
        continue
    # ujecia w kolejnosci montazu; wersja z wycinkami ze srodka kwestii ma je w "clips", starsza w "shots"
    for sh in (e.get("clips") or [{"v_in": e["v_in"] + x["rel"], "dur": x["dur"]} for x in e["shots"]]):
        t0 = sh["v_in"]
        t1 = t0 + sh["dur"]
        t = t0 + 0.05
        while t < t1:
            czasy.add(round(t, 2))
            t += KROK
        czasy.add(round(t1 - 0.05, 2))
czasy = sorted(czasy)
print(f"{len(czasy)} probek z {len(edl)} kwestii")

with tempfile.TemporaryDirectory() as td:
    vf = ("hflip," if FLIP else "") + f"scale={SKALA[0]}:{SKALA[1]}"

    def klatka(t):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(aroll.VIDEO), "-frames:v", "1", "-vf", vf,
                        f"{td}/{t:09.2f}.png"], check=True)

    with ThreadPoolExecutor(3) as ex:
        list(ex.map(klatka, czasy))
    pliki = sorted(Path(td).glob("*.png"))
    out = {}
    for i in range(0, len(pliki), 60):
        r = subprocess.run([str(TWARZ)] + [str(f) for f in pliki[i:i + 60]], capture_output=True, text=True)
        for linia in r.stdout.splitlines():
            c = linia.split()
            if len(c) == 7:
                t = float(c[0][:-4])
                # klatki 540x960 -> wymiary zrodla z aroll.py (IMG_0717 mialo 1908x3304, nie 2160x3840)
                kx, ky = aroll.SRC_W / SKALA[0], aroll.SRC_H / SKALA[1]
                out[f"{t:.2f}"] = [round(float(c[3]) * kx), round(float(c[4]) * ky), round(float(c[5]) * kx), round(float(c[6]) * ky)]
(P / "analiza/twarze.json").write_text(json.dumps(out))
print(f"wykryto twarz w {len(out)} z {len(czasy)} probek -> analiza/twarze.json")
if out:
    dol = max((y + h * 1.05) / aroll.SRC_H for x, y, w, h in out.values())
    print(f"najnizsza broda: {dol:.0%} wysokosci zrodla")

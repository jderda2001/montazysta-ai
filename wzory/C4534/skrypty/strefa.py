#!/usr/bin/env python3
"""Kontrola strefy bezpiecznej (safe zone) w gotowej kompozycji rolki 1080x1920.

Jakub, 18.11.2026: "napisy i animacje czasem sa za wysoko badz za szeroko". Zdany `hyperframes check` tego nie lapie,
a na pojedynczych klatkach latwo przeoczyc jedna za dluga fraze. Ten skrypt sprawdza caly film.

Uzycie (w folderze projektu, po `kompozycja.py`):
  uv run --no-project --with numpy python3 -I skrypty/strefa.py              kontrola automatyczna
  uv run --no-project --with numpy python3 -I skrypty/strefa.py --obrys KAT  obrys strefy na klatkach z katalogu KAT

Kontrola automatyczna:
  1. generuje kompozycje w trybie kontrolnym (STREFA=1): same grafiki i napisy na czarnym tle, bez wideo, tel plansz,
     cieni i poswiat,
  2. robi klatki w momentach z analiza/strefa_czasy.json (koniec kazdego napisu i hooka, siatka co 0,75 s),
  3. ZAWSZE generuje kompozycje jeszcze raz normalnie (takze po bledzie), zeby w hf/ nie zostal tryb kontrolny,
  4. w kazdej klatce szuka jasnych pikseli (tekst, ikony, wypelnienia akcentem, jasne karty) poza strefa.
Ciemne tla kart i pigulek nie licza sie jako naruszenie: poza strefe moze wystawac tlo, ale nie tresc.
Wynik: lista naruszen (czas, strona, prostokat) i arkusz klatek z obrysem w analiza/strefa/. Kod wyjscia 1 = sa naruszenia.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
HF = str(Path.home() / ".local/bin/hyperframes")
JASNE = 110      # prog jasnosci (max z R, G, B): tekst pomocniczy #898989 ma 137, tla kart ok. 20-30
MIN_PIKSELI = 60  # mniej to wygladzanie krawedzi, nie tresc
PARTIA = 60      # ile momentow na jedno wywolanie `hyperframes snapshot`


def wielokat(safe):
    """Wierzcholki strefy (zgodnie z ruchem wskazowek zegara) i lista prostokatow POZA strefa (x, y, w, h)."""
    t, b, l, r = safe["top"], safe["bottom"], safe["left"], safe["right"]
    poza = [(0, 0, 1080, t), (0, b, 1080, 1920 - b), (0, t, l, b - t), (r, t, 1080 - r, b - t)]
    pts, x = [(l, t), (r, t)], r
    for y, nx in safe["wciecia"]:
        pts += [(x, y), (nx, y)]
        poza.append((nx, y, r - nx, b - y))
        x = nx
    pts += [(x, b), (l, b)]
    return pts, poza


def obrys(src, dst, poza, skala=0.5):
    """Klatka z przyciemnionym na czerwono obszarem poza strefa (ffmpeg drawbox, bez dodatkowych bibliotek)."""
    vf = ",".join(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=red@0.30:t=fill" for x, y, w, h in poza)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"{vf},scale=iw*{skala}:-2", "-q:v", "3", str(dst)], check=True)


def arkusz(pliki, dst, kolumny=6):
    if not pliki:
        return
    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(pliki):
            shutil.copyfile(f, Path(td) / f"{i:04d}.jpg")
        n = len(pliki)
        k = min(kolumny, n)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", f"{td}/%04d.jpg", "-vf",
                        f"scale=360:-2,tile={k}x{-(-n // k)}:padding=6:color=black", "-frames:v", "1", "-q:v", "3", str(dst)], check=True)


def tryb_obrys(kat):
    safe = json.loads((P / "analiza/strefa_czasy.json").read_text())["safe"]
    _, poza = wielokat(safe)
    kat = Path(kat)
    out = kat / "strefa"
    out.mkdir(exist_ok=True)
    pliki = []
    for f in sorted(kat.glob("frame-*.png")) + sorted(kat.glob("at-*.png")):
        d = out / (f.stem + ".jpg")
        obrys(f, d, poza)
        pliki.append(d)
    arkusz(pliki, out / "arkusz.jpg")
    print(f"{len(pliki)} klatek z obrysem -> {out}/arkusz.jpg")


def kontrola():
    import numpy as np
    komp = ["python3", "-I", str(P / "skrypty/kompozycja.py")]
    out = P / "analiza/strefa"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    tmp = Path(tempfile.mkdtemp(prefix="strefa-"))
    try:
        subprocess.run(komp, check=True, capture_output=True, env={**os.environ, "STREFA": "1"})
        dane = json.loads((P / "analiza/strefa_czasy.json").read_text())
        czasy = dane["czasy"]
        for i in range(0, len(czasy), PARTIA):
            subprocess.run([HF, "snapshot", "--at", ",".join(f"{t:g}" for t in czasy[i:i + PARTIA]), "--no-end", "--keep",
                            "-o", str(tmp)], cwd=P / "hf", check=True, capture_output=True)
    finally:
        r = subprocess.run(komp, capture_output=True, text=True)  # przywraca wlasciwy index.html
        if r.returncode:
            print("UWAGA: nie udalo sie przywrocic kompozycji, uruchom kompozycja.py recznie:\n" + r.stderr[-600:])
    safe = dane["safe"]
    pts, poza = wielokat(safe)
    maska = np.zeros((1920, 1080), dtype=bool)   # True = poza strefa
    for x, y, w, h in poza:
        maska[y:y + h, x:x + w] = True
    zle, klatki = [], []
    pliki = sorted(tmp.glob("at-*.png"), key=lambda f: float(f.stem[3:].rstrip("s")))
    for f in pliki:
        t = float(f.stem[3:].rstrip("s"))
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        a = np.frombuffer(raw, dtype=np.uint8).reshape(1920, 1080, 3)
        m = (a.max(axis=2) >= JASNE) & maska
        n = int(m.sum())
        if n < MIN_PIKSELI:
            continue
        ys, xs = np.where(m)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        strony = []
        if y0 < safe["top"]:
            strony.append("za wysoko")
        if y1 >= safe["bottom"]:
            strony.append("za nisko")
        if x0 < safe["left"]:
            strony.append("za szeroko z lewej")
        if x1 >= safe["right"]:
            strony.append("za szeroko z prawej")
        if not strony or (x1 < safe["right"] and x1 >= min(x for _, x in safe["wciecia"])):
            strony.append("wchodzi pod przyciski z prawej")
        zle.append((t, n, ", ".join(dict.fromkeys(strony)), (x0, y0, x1, y1)))
        d = out / f"{t:07.2f}.jpg"
        obrys(f, d, poza)
        klatki.append(d)
    shutil.rmtree(tmp, ignore_errors=True)
    arkusz(klatki, out / "naruszenia.jpg")
    (out / "raport.json").write_text(json.dumps([{"t": t, "piksele": n, "strona": s, "prostokat": b} for t, n, s, b in zle], ensure_ascii=False, indent=1))
    print(f"strefa bezpieczna: {len(pliki)} klatek sprawdzonych, {len(zle)} z trescia poza strefa "
          f"(gora {safe['top']}, dol {safe['bottom']}, boki {safe['left']}-{safe['right']}, wciecia {safe['wciecia']})")
    for t, n, s, (x0, y0, x1, y1) in zle:
        print(f"  {t:7.2f} s  {s:42s} x {x0}-{x1}, y {y0}-{y1}  ({n} px)")
    if zle:
        print(f"klatki z obrysem: {out}/naruszenia.jpg")
    return 1 if zle else 0


if __name__ == "__main__":
    if "--obrys" in sys.argv:
        tryb_obrys(sys.argv[sys.argv.index("--obrys") + 1])
    else:
        sys.exit(kontrola())

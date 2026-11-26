"""Kandydaci na okładkę z aroll.mp4: klatki co 0,1 s, otwarcie ust i oczu (Vision), najlepsze N z odstępem >= 1 s.
Uzycie: python3 kandydaci.py <aroll.mp4> <folder_wyjscia> [N]
Wyjscie: folder/kand/*.jpg (pełna rozdzielczość), folder/kandydaci.csv, folder/kandydaci.jpg (stykówka)."""
import csv, subprocess, sys, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

USTA_BIN = Path(__file__).with_name("usta")  # skompiluj raz: swiftc -O usta.swift -o usta
src, out = Path(sys.argv[1]), Path(sys.argv[2])
N = int(sys.argv[3]) if len(sys.argv) > 3 else 8
probki = out / "probki"
kand = out / "kand"
for d in (probki, kand):
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "fps=10,scale=540:960",
                "-q:v", "3", str(probki / "p_%05d.jpg")], check=True)
pliki = sorted(probki.glob("p_*.jpg"))
wynik = subprocess.run([str(USTA_BIN), *map(str, pliki)], capture_output=True, text=True, check=True).stdout
rows = []
for r in csv.DictReader(wynik.splitlines()):
    if r.get("twarz_x") in (None, "BLAD", "BRAK"):
        continue
    t = (int(r["plik"][2:7]) - 1) / 10
    if t > (len(pliki) - 3) / 10:  # ostatnie klatki: seek za koniec pliku
        continue
    usta, oczy, yaw = float(r["usta"]), float(r["oczy"]), abs(float(r["yaw"]))
    if usta < 0 or oczy < 0:
        continue
    # niżej = lepiej: zamknięte usta, otwarte oczy, twarz na wprost
    score = usta * 10 + max(0.0, 0.24 - oczy) * 6 + yaw * 0.6
    rows.append(dict(t=t, usta=usta, oczy=oczy, yaw=yaw, score=score,
                     broda=float(r["broda_y"]) * 2, twarz_y=float(r["twarz_y"]) * 2,
                     twarz_x=float(r["twarz_x"]) * 2, twarz_w=float(r["twarz_w"]) * 2))
rows.sort(key=lambda r: r["score"])
wybrane = []
for r in rows:
    if all(abs(r["t"] - w["t"]) >= 1.0 for w in wybrane):
        wybrane.append(r)
    if len(wybrane) >= N:
        break
wybrane.sort(key=lambda r: r["t"])
with open(out / "kandydaci.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(wybrane[0].keys()) + ["plik"])
    w.writeheader()
    for r in wybrane:
        p = kand / f"k_{r['t']:06.1f}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{r['t'] + 0.05:.2f}", "-i", str(src),
                        "-frames:v", "1", "-q:v", "1", str(p)], check=True)
        r["plik"] = p.name
        w.writerow(r)
# stykówka: kadr od czubka głowy do pasa, żeby ocenić usta
cols = 4
tw, th = 400, 560
sheet = Image.new("RGB", (cols * tw, ((len(wybrane) + cols - 1) // cols) * (th + 30)), "white")
d = ImageDraw.Draw(sheet)
for k, r in enumerate(wybrane):
    im = Image.open(kand / r["plik"])
    cx = r["twarz_x"] + r["twarz_w"] / 2
    top = max(0, r["twarz_y"] - 250)
    box = (int(max(0, min(1080 - 640, cx - 320))), int(top), 0, 0)
    box = (box[0], box[1], box[0] + 640, min(1920, box[1] + 896))
    im = im.crop(box).resize((tw, th))
    x, y = (k % cols) * tw, (k // cols) * (th + 30)
    sheet.paste(im, (x, y + 30))
    d.text((x + 6, y + 6), f"{k+1}. t={r['t']:.1f}s usta={r['usta']:.3f} oczy={r['oczy']:.2f}", fill="black")
sheet.save(out / "kandydaci.jpg", quality=85)
shutil.rmtree(probki)
print(f"{len(rows)} klatek z twarzą, wybrano {len(wybrane)} -> {out/'kandydaci.jpg'}")

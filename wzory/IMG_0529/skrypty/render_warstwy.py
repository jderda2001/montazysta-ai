#!/usr/bin/env python3
"""Render warstw HyperFrames (grafiki o_*.html i napisy n_*.html) do ProRes 4444 z alfa w 4K (DPR 2).
Pomija warstwy, ktorych HTML i zasoby sie nie zmienily (hash w nazwie pliku).

Uzycie: python3 -I render_warstwy.py [nazwa_lub_plik ...]   (bez argumentow: wszystkie)
Wynik:  ../hf/renders/<plik>_<hash>.mov + ../hf/renders/warstwy.json (plik, start, dlugosc, mov)
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

P = Path(__file__).resolve().parent.parent
HF = P / "hf"
R = HF / "renders"


def assets_hash(names=None, skip=()):
    """Hash zasobow. names: tylko te pliki z assets (None = wszystkie); fonty zawsze."""
    h = hashlib.md5()
    for f in sorted((HF / "assets").glob("*")) + sorted((HF / "fonts").glob("*")):
        if f.parent.name == "assets" and ((names is not None and f.name not in names) or f.name in skip):
            continue
        h.update(f.name.encode())
        h.update(str(f.stat().st_size).encode())
    return h.hexdigest()


def layer_key(html):
    """Klucz warstwy: HTML + tylko zasoby, ktorych ta warstwa uzywa (nowy plik w assets nie uniewaznia reszty)."""
    used = {f.name for f in (HF / "assets").glob("*") if f.name in html}
    return hashlib.md5((html + assets_hash(used)).encode()).hexdigest()[:10]


def migrate(m, html, mov):
    """Jednorazowo: plik z poprzedniego schematu (hash z wszystkimi zasobami, z logo albo bez) -> nowa nazwa."""
    stem = m["plik"][:-5]
    for ah in (assets_hash(), assets_hash(skip={"app_logo.svg"})):
        old = R / f"{stem}_{hashlib.md5((html + ah).encode()).hexdigest()[:10]}.mov"
        if old.exists() and old != mov:
            old.rename(mov)
            return True
    return False


def main():
    R.mkdir(exist_ok=True)
    only = sys.argv[1:]
    items = [dict(m, typ="grafika") for m in json.loads((HF / "grafiki.json").read_text())]
    items += [dict(m, typ="napisy", nazwa=m["plik"][:-5]) for m in json.loads((HF / "napisy.json").read_text())]
    out = []
    for m in items:
        src = HF / m["plik"]
        html = src.read_text()
        mov = R / f"{m['plik'][:-5]}_{layer_key(html)}.mov"
        if not mov.exists() and migrate(m, html, mov):
            print(f"{m['plik']:28s} bez zmian (przeniesiony na nowa nazwe)")
        out.append({"plik": m["plik"], "nazwa": m["nazwa"], "typ": m["typ"], "start": m["start"],
                    "dlugosc": m["dlugosc"], "mov": mov.name})
        if mov.exists() or (only and not any(o in (m["nazwa"], m["plik"]) for o in only)):
            continue
        t0 = time.time()
        tmp = R / f"tmp_{mov.name}"
        r = subprocess.run(["hyperframes", "render", "-c", m["plik"], "--format", "mov", "--resolution", "landscape-4k",
                            "-o", str(tmp), "--quiet"], cwd=HF, capture_output=True, text=True)
        if r.returncode != 0 or not tmp.exists():
            print(f"BLAD {m['plik']}:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
            sys.exit(1)
        tmp.rename(mov)
        for old in R.glob(f"{m['plik'][:-5]}_*.mov"):
            if old.name != mov.name:
                old.unlink()
        print(f"{m['plik']:28s} {m['dlugosc']:6.2f} s -> {time.time() - t0:5.1f} s renderu, {mov.stat().st_size / 1e6:7.1f} MB",
              flush=True)
    (R / "warstwy.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

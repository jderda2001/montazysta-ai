#!/usr/bin/env python3
"""Dzwiek kwestii po wycieciach ze srodka (pole "parts" w edl.json: [[poczatek w nagraniu, dlugosc], ...]).

Kwestia z wycietym zacieciem sklada sie z kilku kawalkow nagrania. Skrypty, ktore sluchaja kwestii ze zrodla
(slowa.py, kawalki.py, waliduj_napisy.py), biora dzwiek stad, zeby slyszec to samo, co trafia do filmu.
"""
import subprocess


def czesci(e):
    return e.get("parts") or [[e["a_in"], e["a_out"] - e["a_in"]]]


def wytnij(e, src, out, dl=None):
    """Zapisuje dzwiek kwestii e (z pliku src) do out. dl = tylko pierwsze dl sekund kwestii."""
    cmd, n, zostalo = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"], 0, dl
    for p_in, d in czesci(e):
        if zostalo is not None:
            d = min(d, zostalo)
            zostalo -= d
            if d <= 0.001:
                break
        cmd += ["-ss", f"{p_in:.4f}", "-t", f"{d:.4f}", "-i", str(src)]
        n += 1
    flt = "".join(f"[{k}:a]" for k in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    subprocess.run(cmd + ["-filter_complex", flt, "-map", "[o]", "-c:a", "pcm_s16le", str(out)], check=True)


def na_zrodlo(e, rel):
    """Czas liczony od poczatku kwestii -> czas w nagraniu."""
    o = 0.0
    for p_in, d in czesci(e):
        if rel <= o + d + 1e-6:
            return p_in + (rel - o)
        o += d
    return p_in + d

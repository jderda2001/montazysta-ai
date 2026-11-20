#!/usr/bin/env python3
"""Cichy podklad lo-fi pod odcinek. Utwory z Biblioteki audio YouTube (licencja bez wymogu podawania autora),
pobrane za zgoda Jakuba do ~/Desktop/Montażysta AI/Muzyka/.

Kazda czesc odcinka ma swoj utwor; przejscia (rownomocowy crossfade 3 s) leza na planszach rozdzialow.
Lancuch: kazdy utwor -14 LUFS -> EQ (miejsce na glos: mniej dolu i pasma 2-3 kHz) -> poziom bazowy
-> ducking sterowany glosem C (sciszanie, gdy mowi) -> miks z glosem -> -14 LUFS calosci -> limiter
(-2,5 dBFS, po AAC szczyt <= -1,5). Na planszy koncowej podklad lekko rosnie, potem sie wycisza.

Uzycie: uv run --no-project --with numpy python3 -I muzyka.py
Wynik:  ../audio/podklad.wav (sama muzyka po duckingu), ../audio/glos_z_muzyka.wav (do filmu)
"""
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
MUZ = Path.home() / "Desktop/Montażysta AI/Muzyka"
GLOS = P / "audio/aroll_studio_gleboki.wav"
SR = 48000
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]

# (start czesci w odcinku [s], utwor, start w utworze [s]) - granice na planszach rozdzialow (hf/grafiki.json)
SECTIONS = [
    (0.0, "On The Flip - The Grey Room _ Density & Time.mp3", 0.0),       # intro
    (171.75, "Twinkle - The Grey Room _ Density & Time.mp3", 0.9),        # 01 Dlaczego growth, struktura (Twinkle: 0,9 s ciszy)
    (355.2, "Misdirection - The Grey Room _ Density & Time.mp3", 0.0),    # Tymon, Artur, voice call, co dalej
    (529.5, "High Noon - The Grey Room _ Density & Time.mp3", 0.0),       # 03 Czego AI nie zrobi
    (698.4, "No Rush - Dyalla.mp3", 0.7),                                 # 04 Aplikacja i koszty
    (811.2, "Kicking It - Dyalla.mp3", 1.3),                              # podsumowanie i plansza koncowa
]
XF = 3.0              # crossfade (srodek na starcie czesci)
FADE_IN = 1.2         # wejscie muzyki na poczatku odcinka
BASE_LUFS = -29.0     # podklad bez duckingu
DUCK_DB = -5.0        # dodatkowo, gdy mowi (pod mowa ok. -34 LUFS, ok. 19-20 dB pod glosem)
SWELL_AT, SWELL_DB = 901.5, 4.0     # plansza koncowa (koniec mowy ok. 902 s)
FADE_OUT = 4.0        # wyciszenie na koniec filmu
EQ = "highpass=f=45,equalizer=f=170:t=q:w=0.9:g=-3,equalizer=f=2700:t=q:w=1.0:g=-3.5,equalizer=f=9000:t=q:w=0.8:g=-1.5"


def decode(path, extra=()):
    raw = subprocess.run(["ffmpeg", "-v", "error", *extra, "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def write(path, x, bits=24):
    if bits == 32:
        subprocess.run(FF + ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", str(path)],
                       input=x.astype(np.float32).tobytes(), check=True)
    else:
        subprocess.run(FF + ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", str(path)],
                       input=np.clip(x, -1, 1).astype(np.float32).tobytes(), check=True)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind("Summary"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))


def main():
    voice = decode(GLOS)
    n = len(voice)
    total = n / SR
    tmp = P / "audio/tmp_muzyka"
    tmp.mkdir(exist_ok=True)

    # 1. podklad: utwory na swoich miejscach, kazdy znormalizowany do -14 LUFS, crossfade rownomocowy
    bed = np.zeros((n, 2), np.float32)
    bounds = [s[0] for s in SECTIONS[1:]] + [total]
    for k, (t0, name, off) in enumerate(SECTIONS):
        src = MUZ / name
        lu = loudness(src)[0]
        a = 0.0 if k == 0 else t0 - XF / 2
        b = min(total, bounds[k] + XF / 2)
        x = decode(src, ["-ss", f"{off:.3f}"])[: int(round((b - a) * SR))] * 10 ** ((-14.0 - lu) / 20)
        if len(x) < int(round((b - a) * SR)) - 1:
            raise SystemExit(f"{name}: za krotki na czesc {a:.1f}-{b:.1f} s")
        g = np.ones(len(x), np.float32)
        nx = int(XF * SR)
        u = np.linspace(0, 1, nx, dtype=np.float32)
        if k == 0:
            nf = int(FADE_IN * SR)
            g[:nf] = np.linspace(0, 1, nf)
        else:
            g[:nx] = np.sin(u * np.pi / 2)
        if k < len(SECTIONS) - 1:
            g[-nx:] *= np.cos(u * np.pi / 2)
        i0 = int(round(a * SR))
        bed[i0:i0 + len(x)] += x * g[:, None]
        print(f"{a:7.2f}-{b:7.2f} s  {name[:44]:44s} od {off:.1f} s, {lu:+.1f} LUFS -> -14")

    # 2. EQ (miejsce na glos) i poziom bazowy
    raw, eqd = tmp / "podklad_surowy.wav", tmp / "podklad_eq.wav"
    write(raw, bed, bits=32)
    subprocess.run(FF + ["-i", str(raw), "-af", EQ, "-c:a", "pcm_f32le", str(eqd)], check=True)
    bed = decode(eqd)[:n]
    bed *= 10 ** ((BASE_LUFS - loudness(eqd)[0]) / 20)

    # 3. ducking od glosu: mowa = RMS 10 ms > -45 dBFS, podtrzymanie 0,3 s, wygladzenie (atak 80 ms, powrot 600 ms)
    hop = SR // 100
    vm = voice.mean(axis=1)
    nfr = n // hop
    rms = np.sqrt(np.mean(vm[:nfr * hop].reshape(nfr, hop) ** 2, axis=1))
    act = 20 * np.log10(rms + 1e-9) > -45
    hold = 30
    idx = np.where(act)[0]
    act2 = np.zeros(nfr, bool)
    for i in idx:
        act2[i:i + hold] = True
    target = np.where(act2, DUCK_DB, 0.0)
    gdb = np.zeros(nfr)
    a_att, a_rel = np.exp(-0.01 / 0.08), np.exp(-0.01 / 0.6)
    cur = 0.0
    for i in range(nfr):
        c = a_att if target[i] < cur else a_rel
        cur = c * cur + (1 - c) * target[i]
        gdb[i] = cur
    t_fr = (np.arange(nfr) + 0.5) * 0.01
    t = np.arange(n) / SR
    g = np.interp(t, t_fr, gdb)
    g += SWELL_DB * np.clip((t - SWELL_AT) / 1.0, 0, 1)       # plansza koncowa: troche glosniej
    gl = 10 ** (g / 20)
    gl *= np.clip((total - t) / FADE_OUT, 0, 1)                # wyciszenie na koniec
    bed *= gl[:, None].astype(np.float32)
    write(P / "audio/podklad.wav", bed)

    # 4. miks: glos + podklad -> -14 LUFS -> limiter
    mix = voice + bed
    mraw = tmp / "miks_surowy.wav"
    write(mraw, mix, bits=32)
    gain = -14.0 - loudness(mraw)[0]
    out = P / "audio/glos_z_muzyka.wav"
    for _ in range(3):
        subprocess.run(FF + ["-i", str(mraw), "-af", f"volume={gain:.3f}dB,alimiter=limit=0.7499:attack=1:release=60:"
                             "level=false:latency=true", "-c:a", "pcm_s24le", str(out)], check=True)
        lu, tp = loudness(out)
        if abs(lu + 14.0) <= 0.03:
            break
        gain += -14.0 - lu
    for f in (raw, eqd, mraw):
        f.unlink()
    tmp.rmdir()

    # 5. kontrola poziomow: muzyka wzgledem glosu w ramkach mowy i w pauzach
    sp = np.repeat(act, hop)[:n]
    if len(sp) < n:
        sp = np.concatenate([sp, np.zeros(n - len(sp), bool)])
    bm, vmm = bed.mean(axis=1), vm
    lvl = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
    print(f"muzyka pod mowa: {lvl(bm[sp]) - lvl(vmm[sp]):+.1f} dB wzgledem glosu; "
          f"podklad sam (pauzy): {lvl(bm[~sp & (t < 900)]):.1f} dBFS RMS")
    print(f"{out.name}: {lu:.1f} LUFS, szczyt {tp:.1f} dBFS, {total:.2f} s")


if __name__ == "__main__":
    main()

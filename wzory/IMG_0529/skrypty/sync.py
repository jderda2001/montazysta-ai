#!/usr/bin/env python3
"""Przesuniecie miedzy dzwiekiem z telefonu (IMG_0529.MOV) a nagraniem z mikrofonu (korelacja krzyzowa)
oraz dryf zegara w oknach co 15 s.

Uzycie: uv run --no-project --with numpy python3 -I sync.py m7|m8   (audio/<nazwa>_16k.wav)
Wynik:  ../analiza/sync_<nazwa>.json  {"offset": s, "drift_ppm": ..., "fit": [b, k]}
        czas_w_nowym_audio = czas_w_wideo + offset (+ k * czas_w_wideo, jesli dryf nie jest pomijalny)
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SR = 16000
DEC = 4  # globalne szukanie na 4 kHz (szybciej), potem doprecyzowanie na 16 kHz


def load(path):
    with wave.open(str(path)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    x -= x.mean()
    return x / (np.abs(x).max() + 1e-9)


def xcorr_lag(a, b, excl=800):
    """Lag (w probkach), o ktory trzeba przesunac b, by pasowalo do a: a[n] ~ b[n - lag]."""
    n = len(a) + len(b)
    nfft = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(a, nfft) * np.conj(np.fft.rfft(b, nfft)), nfft)
    c = np.concatenate([c[-(len(b) - 1):], c[:len(a)]])
    k = int(np.argmax(c))
    cc = c.copy()
    cc[max(0, k - excl):k + excl] = 0
    return k - (len(b) - 1), float(c[k] / (np.abs(cc).max() + 1e-9))


def main():
    vid = load(P / "audio/wideo_16k.wav")
    name = sys.argv[1]
    new = load(P / f"audio/{name}_16k.wav")
    v4 = vid[: len(vid) // DEC * DEC].reshape(-1, DEC).mean(1)
    n4 = new[: len(new) // DEC * DEC].reshape(-1, DEC).mean(1)
    lag4, q = xcorr_lag(n4, v4, excl=200)
    lag = lag4 * DEC
    print(f"globalnie (4 kHz): offset = {lag / SR:+.4f} s (jakosc piku {q:.1f})")

    rows = []
    for t0 in np.arange(0, len(vid) / SR - 15, 15.0):
        a0 = int(t0 * SR)
        seg = vid[a0:a0 + 12 * SR]
        if np.sqrt(np.mean(seg ** 2)) < 0.01:
            continue
        b0 = a0 + lag - SR
        if b0 < 0 or b0 + 14 * SR > len(new):
            continue
        l2, q2 = xcorr_lag(new[b0:b0 + 14 * SR], seg)
        rows.append((float(t0), (b0 + l2 - a0) / SR, q2))
        print(f"  wideo t={t0:7.1f}s  offset={rows[-1][1]:+.4f}  jakosc={q2:5.1f}")
    good = [(t, o) for t, o, qq in rows if qq > 2.0]
    t, o = np.array(good).T
    k, b = np.polyfit(t, o, 1)
    res = o - (k * t + b)
    print(f"okien dobrych: {len(good)}/{len(rows)}; dryf {k * 1e6:+.1f} ppm; offset(t) = {b:+.4f} + {k:.3e}*t; "
          f"rozrzut {np.std(res) * 1000:.1f} ms, max {np.abs(res).max() * 1000:.1f} ms")
    off_mid = float(np.median(o))
    (P / f"analiza/sync_{name}.json").write_text(json.dumps({
        "offset": off_mid, "quality": q, "drift_ppm": k * 1e6, "fit": [b, k],
        "covered_video": [float(-off_mid), float(len(new) / SR - off_mid)], "windows": rows}, indent=1))


if __name__ == "__main__":
    main()

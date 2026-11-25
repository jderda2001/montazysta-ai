#!/usr/bin/env python3
"""Szuka przesuniecia miedzy dzwiekiem z telefonu (wideo) a nowym nagraniem (korelacja krzyzowa)
i sprawdza dryf zegara w oknach co ~20 s.

Uzycie: uv run --no-project --with numpy python3 sync.py
Wynik:  ../analiza/sync.json  {"offset": s, "drift_ppm": ...}
        offset > 0 oznacza: zdarzenie w czasie t wideo jest w nowym audio w czasie t + offset
"""
import json
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SR = 16000


def load(path):
    with wave.open(str(path)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    x -= x.mean()
    return x / (np.abs(x).max() + 1e-9)


def xcorr_lag(a, b):
    """Lag (w probkach), o ktory trzeba przesunac b, by pasowalo do a: a[n] ~ b[n - lag]."""
    n = len(a) + len(b)
    nfft = 1 << (n - 1).bit_length()
    A = np.fft.rfft(a, nfft)
    B = np.fft.rfft(b, nfft)
    c = np.fft.irfft(A * np.conj(B), nfft)
    c = np.concatenate([c[-(len(b) - 1):], c[:len(a)]])  # lagi od -(len(b)-1) do len(a)-1
    k = int(np.argmax(c))
    lag = k - (len(b) - 1)
    # jakosc piku: stosunek do drugiego maksimum poza +-50 ms
    cc = c.copy()
    lo, hi = max(0, k - 800), min(len(cc), k + 800)
    cc[lo:hi] = 0
    return lag, float(c[k] / (np.abs(cc).max() + 1e-9))


def main():
    vid = load(P / "audio/wideo_16k.wav")
    new = load(P / "audio/nowe_16k.wav")
    # nowe[t + off] ~ vid[t]  ->  szukamy lag dla a=nowe, b=vid
    lag, q = xcorr_lag(new, vid)
    off = lag / SR
    print(f"globalnie: offset = {off:+.4f} s (jakosc piku {q:.1f})")

    # dryf: okna 12 s z wideo, szukane w nowym audio w otoczeniu +-1 s od offsetu
    rows = []
    for t0 in np.arange(5, len(vid) / SR - 15, 15.0):
        a0 = int(t0 * SR)
        seg = vid[a0:a0 + 12 * SR]
        if np.sqrt(np.mean(seg ** 2)) < 0.01:
            continue
        b0 = a0 + lag - SR
        if b0 < 0 or b0 + 14 * SR > len(new):
            continue
        ref = new[b0:b0 + 14 * SR]
        l2, q2 = xcorr_lag(ref, seg)
        local = (b0 + l2 - a0) / SR
        rows.append((float(t0), local, q2))
        print(f"  t={t0:6.1f}s  offset={local:+.4f}  jakosc={q2:5.1f}")
    good = [(t, o) for t, o, qq in rows if qq > 2.0]
    drift = 0.0
    if len(good) >= 3:
        t, o = np.array(good).T
        k, b = np.polyfit(t, o, 1)
        drift = k * 1e6
        print(f"dryf: {drift:+.1f} ppm (offset(t) = {b:+.4f} + {k:.3e}*t), rozrzut {np.std(o - (k*t+b))*1000:.1f} ms")
    (P / "analiza/sync.json").write_text(json.dumps({"offset": off, "quality": q, "drift_ppm": drift,
                                                      "windows": rows}, indent=1))


if __name__ == "__main__":
    main()

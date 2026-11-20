#!/usr/bin/env python3
"""Dzwiek "studyjny" z AI: Sidon (sidon_infer.py) + wykonczenie. Dwa warianty na cala rolke, ta sama os czasu co A.

1. audio/studio/surowe.wav  - te same ciecia co A-roll, bez obrobki (glos.raw_concat)
2. audio/studio/sidon.wav   - wynik Sidona (48 kHz), robiony osobno:
   uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub \
          --with numpy python -I sidon_infer.py ../audio/studio/surowe.wav ../audio/studio/sidon.wav
3. ten skrypt: wyrownanie w czasie (obwiednia, korelacja), kontrola tonu (F0), dwa wykonczenia, -14 LUFS:
   audio/aroll_studio.wav          - Sidon + de-esser + ta sama kompresja co A
   audio/aroll_studio_gleboki.wav  - Sidon + "radiowy" lancuch: glebia w dole, gladka gora, gestsza kompresja

Uzycie: uv run --no-project --with numpy python3 -I studio.py
"""
import importlib.util
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("glos", Path(__file__).with_name("glos.py"))
glos = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(glos)
FF = glos.FF

LIGHT = "highpass=f=60"
COMP = "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5"
# Sidon daje srodek i gore jak glos z bliska z dobrego mikrofonu, ale ma o 4-6 dB mniej dolu niz oryginal (100-250 Hz)
# -> odbudowa dolu (glebia), lekkie czyszczenie mulu, odrobina powietrza (Sidon tnie powyzej ~10 kHz), gesta kompresja.
DEEP = ("highpass=f=55,"
        "lowshelf=f=170:t=s:w=0.7:g=5.5,"     # glebia; IMG_0576 (mikrofon krawatowy przez iPhone'a): 5,5 zamiast 7,5 dB,
        "equalizer=f=400:t=q:w=1.2:g=-2,"     # bo po Sidonie srodek i gora byly 2-5 dB nizej niz w glosie C z IMG_0526
        "highshelf=f=5000:t=s:w=0.7:g=2.5,"   # (pomiar LTAS z ramek mowy) -> mniej dolu, wiecej obecnosci
        "highshelf=f=10000:t=s:w=0.7:g=1.5")  # odrobina powietrza
# gesta kompresja wyciaga spolgloski, wiec w tym wariancie de-esser stoi PO kompresorze
COMP_DEEP = "acompressor=threshold=-28dB:ratio=4:attack=5:release=120:knee=4:makeup=2"


def env_ms(x, sr):
    h = sr // 1000
    n = len(x) // h
    return np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(axis=1) + 1e-12)


def lag_ms(a, b, sr, max_ms=150):
    """Przesuniecie b wzgledem a (ms) z korelacji obwiedni 1 ms (Sidon syntezuje fale od nowa, faza sie nie zgadza)."""
    ea, eb = np.log(env_ms(a, sr)), np.log(env_ms(b, sr))
    n = min(len(ea), len(eb))
    ea, eb = ea[:n] - ea[:n].mean(), eb[:n] - eb[:n].mean()
    best = max(range(-max_ms, max_ms + 1), key=lambda k: np.dot(ea[max(0, -k):n - max(0, k)], eb[max(0, k):n - max(0, -k)]))
    return best


def f0_track(x, sr):
    """Proste F0 z autokorelacji (ramki 40 ms co 10 ms, 70-300 Hz), tylko ramki dzwieczne."""
    win, hop = int(0.04 * sr), int(0.01 * sr)
    lo, hi = int(sr / 300), int(sr / 70)
    out = []
    for i in range(0, len(x) - win, hop):
        f = x[i:i + win] * np.hanning(win)
        if np.sqrt(np.mean(f ** 2)) < 0.01:
            out.append(np.nan)
            continue
        ac = np.correlate(f, f, mode="full")[win - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        out.append(sr / k if ac[k] > 0.4 * ac[0] else np.nan)
    return np.array(out)


def finish(src, chain, comp, out, td, label, deess_after=False):
    """EQ -> de-esser -> kompresja (albo EQ -> kompresja -> de-esser) -> -14 LUFS. Prog de-essera liczony na sygnale,
    ktory de-esser faktycznie dostaje."""
    eq = Path(td) / f"{label}_eq.wav"
    pre_chain = chain + ("," + comp if deess_after else "")
    subprocess.run(FF + ["-i", str(src), "-af", pre_chain, "-c:a", "pcm_s32le", str(eq)], check=True)
    thr = glos.deess_threshold(eq, td)
    post = glos.DEESS.format(thr=thr) + ("" if deess_after else "," + comp)
    pre = Path(td) / f"{label}_pre.wav"
    subprocess.run(FF + ["-i", str(eq), "-af", post, "-ac", "2", "-c:a", "pcm_s24le", str(pre)], check=True)
    st = glos.loudnorm(pre, out)
    print(f"{label}: {out} | loudnorm in {st['input_i']} LUFS")


def main():
    raw, sid = P / "audio/studio/surowe.wav", P / "audio/studio/sidon.wav"
    sr, x = glos.read(raw)
    sr2, y = glos.read(sid)
    assert sr == sr2 == 48000, (sr, sr2)
    lag = lag_ms(x, y, sr)
    print(f"przesuniecie Sidona wzgledem oryginalu: {lag:+d} ms")
    with tempfile.TemporaryDirectory() as td:
        al = Path(td) / "sidon_al.wav"
        if lag:  # wyrownanie: przesun wynik o -lag
            k = lag * sr // 1000
            y = np.concatenate([y[k:], np.zeros(k, np.float32)]) if k > 0 else np.concatenate([np.zeros(-k, np.float32), y[:k]])
        y = y[:len(x)] if len(y) >= len(x) else np.concatenate([y, np.zeros(len(x) - len(y), np.float32)])
        with wave.open(str(al), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
        print(f"po wyrownaniu: {lag_ms(x, y, sr):+d} ms")
        fa, fb = f0_track(x[::3], sr // 3), f0_track(y[::3], sr // 3)
        m = ~np.isnan(fa) & ~np.isnan(fb)
        print(f"F0 (ton glosu): oryginal mediana {np.nanmedian(fa):.1f} Hz, Sidon {np.nanmedian(fb):.1f} Hz, "
              f"zgodnosc przebiegu r={np.corrcoef(fa[m], fb[m])[0, 1]:.3f} ({m.sum()} ramek)")
        finish(al, LIGHT, COMP, P / "audio/aroll_studio.wav", td, "studio")
        finish(al, DEEP, COMP_DEEP, P / "audio/aroll_studio_gleboki.wav", td, "gleboki", deess_after=True)


if __name__ == "__main__":
    main()

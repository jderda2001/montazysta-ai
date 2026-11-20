#!/usr/bin/env python3
"""Dzwiek odcinka wg ../aroll/edl.json: tylko nagrania z mikrofonu (m7 = wstep, m8 = reszta).

1. m7 dopasowany do m8: korekcja barwy (match EQ z usrednionych widm mowy, wygladzona 1/3 oktawy, 75% roznicy,
   ograniczona do -10..+4 dB) i glosnosc (LUFS mowy rowny m8).
2. Skladanie kawalkow: na prawdziwych cieciach krotkie wyciszenia 8 ms, na zmianach kadru bez ciecia (cont) nic.
   Po ostatnim slowie cisza pod plansze koncowa (video_extra).
3. Lancuch jak w rolkach: highpass 70 Hz, lagodna kompresja, loudnorm dwuprzebiegowy -14 LUFS, TP -1,5.

Uzycie: uv run --no-project --with numpy python3 -I audio.py
Wynik:  ../audio/montaz.wav (48 kHz, 24 bit, gotowy), ../audio/montaz_surowy_16k.wav (do kontroli whisperem)
"""
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SR = 48000
FADE = 0.008


def read(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(P / f"audio/{name}_48k.wav"), "-f", "f32le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def write(path, x, sr=SR, bits=24):
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(bits // 8)
        w.setframerate(sr)
        if bits == 24:
            v = (x * (2 ** 23 - 1)).astype(np.int32)
            b = np.stack([(v & 0xFF), (v >> 8) & 0xFF, (v >> 16) & 0xFF], axis=1).astype(np.uint8).tobytes()
        else:
            b = (x * 32767).astype(np.int16).tobytes()
        w.writeframes(b)


def ltas(x, a, b, n=4096):
    s = x[int(a * SR):int(b * SR)]
    fr = np.lib.stride_tricks.sliding_window_view(s, n)[::n // 2]
    e = 10 * np.log10(np.mean(fr ** 2, axis=1) + 1e-12)
    sp = np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2
    return sp[e > np.percentile(e, 60)].mean(0)


def match_fir(x7, x8, ntap=4097):
    f = np.fft.rfftfreq(4096, 1 / SR)
    s7, s8 = ltas(x7, 47, 239), ltas(x8, 0, 840)
    d = 10 * np.log10(s8 / s7)
    d -= np.mean(d[(f > 300) & (f < 3000)])
    # wygladzenie 1/3 oktawy
    sm = np.array([np.mean(d[(f >= fc / 1.122) & (f <= fc * 1.122)]) if fc > 40 else 0.0 for fc in f])
    g = np.clip(0.75 * sm, -10.0, 4.0)
    g[f < 60] = g[np.argmin(np.abs(f - 60))]
    g[f > 14000] = g[np.argmin(np.abs(f - 14000))]
    # filtr liniowo-fazowy z probkowania czestotliwosci
    fg = np.fft.rfftfreq(ntap - 1, 1 / SR)
    H = 10 ** (np.interp(fg, f, g) / 20)
    h = np.fft.irfft(H)
    h = np.roll(h, len(h) // 2) * np.hanning(len(h))
    return h, f, g


def lufs(x):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.wav"
        write(p, x)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                           capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def loudnorm_stats(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def main():
    edl = json.loads((P / "aroll/edl.json").read_text())
    x7, x8 = read("m7"), read("m8")
    h, f, g = match_fir(x7, x8)
    x7 = np.convolve(x7, h, mode="same")
    gain = lufs(x8[:840 * SR]) - lufs(x7[47 * SR:239 * SR])
    x7 *= 10 ** (gain / 20)
    print(f"m7: korekcja barwy (dB) " + ", ".join(f"{fc}:{g[np.argmin(np.abs(f - fc))]:+.1f}"
                                                  for fc in (100, 250, 500, 800, 1000, 2000, 4000, 6300, 10000))
          + f"; wzmocnienie {gain:+.2f} dB")
    src = {"m7": x7, "m8": x8}
    out = []
    for k, e in enumerate(edl):
        x = src[e["src"]]
        n = int(round((e["t_out"] - e["t_in"]) * SR))
        a = int(round(e["a_in"] * SR))
        seg = x[a:a + n].copy()
        if len(seg) < n:
            seg = np.concatenate([seg, np.zeros(n - len(seg))])
        prev_cont = k > 0 and edl[k - 1]["cont"]
        nf = int(FADE * SR)
        if not prev_cont:
            seg[:nf] *= np.linspace(0, 1, nf)
        if not e["cont"]:
            seg[-nf:] *= np.linspace(1, 0, nf)
        out.append(seg)
        if e.get("video_extra"):
            out.append(np.zeros(int(round(e["video_extra"] * SR))))
    y = np.concatenate(out)
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        write(raw, y)
        write(P / "audio/montaz_surowy_16k.wav", y[::3], sr=16000, bits=16)
        (P / "audio/studio").mkdir(exist_ok=True)
        write(P / "audio/studio/surowe.wav", y, bits=16)  # wejscie Sidona (glos C)
        comp = Path(td) / "comp.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw), "-af",
                        "highpass=f=70,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5",
                        "-c:a", "pcm_s24le", str(comp)], check=True)
        st = loudnorm_stats(comp)
        ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
              f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
              "linear=true,aresample=48000")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(comp), "-af", ln,
                        "-c:a", "pcm_s24le", str(P / "audio/montaz.wav")], check=True)
    st2 = loudnorm_stats(P / "audio/montaz.wav")
    print(f"montaz.wav: {len(y) / SR:.2f} s | wejscie {st['input_i']} LUFS -> {st2['input_i']} LUFS, TP {st2['input_tp']}")


if __name__ == "__main__":
    main()

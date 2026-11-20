#!/usr/bin/env python3
"""Wersja B dzwieku rolki: miekszy, cieplejszy glos. Te same ciecia co A-roll (aroll/edl.json), inny lancuch.

Analiza glosu (13.11, LTAS tylko z ramek mowy, wzgledem typowego widma mowy):
- gora 2,5-8 kHz o ok. 8-12 dB mocniejsza (ostrosc, sybilanty) - glowny powod "twardego" brzmienia,
- "pudlo" 300-450 Hz ok. +5 dB (pokoj, mikrofon ok. pol metra od ust),
- dolina ok. 800 Hz (prawdopodobnie odbicie od blatu); doly 100-200 Hz juz mocne, wiec ich nie podbijam,
- poglos krotki (RT60 ok. 0,25 s), wiec bez ekspandera.

Lancuch B: highpass 70 -> EQ -> de-esser (dynamiczny EQ ~6 kHz; prog = 95. percentyl poziomu pasma detekcji
w ramkach mowy bez sybilantow, wiec tnie praktycznie tylko "s/sz/cz/ś") -> ta sama kompresja co A
-> loudnorm -14 LUFS / TP -1,5 (2 przebiegi). A i B maja te sama glosnosc, wiec porownanie jest uczciwe.

Uzycie: uv run --no-project --with numpy python3 -I glos.py
Wynik:  ../audio/aroll_miekki.wav (B, 48 kHz / 16 bit, ta sama os czasu co aroll.wav)
"""
import importlib.util
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("aroll", Path(__file__).with_name("aroll.py"))
aroll = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aroll)

A_CHAIN = "highpass=f=70,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5"
EQ = ("highpass=f=70,"
      "equalizer=f=360:t=q:w=1.4:g=-3,"     # "pudlo" pokoju
      "equalizer=f=820:t=q:w=1.6:g=2,"      # dolina ~800 Hz
      "equalizer=f=3000:t=q:w=1.0:g=-4,"    # ostrosc
      "highshelf=f=5000:t=s:w=0.6:g=-4")    # cala gora lagodniej
# detekcja waska (ok. 4,6-8,9 kHz), zeby samogloski z mocnym pasmem 3 kHz nie wyzwalaly de-essera.
# Uwaga na adynamicequalizer (zrodlo FFmpeg): wzmocnienie wygladzane jest ze stala 4x dluzsza niz detekcja, a w trybie
# cutabove wchodzenie ciecia idzie galezia "release", wychodzenie - "attack". Stad release=2 (ciecie wchodzi w ok. 8 ms,
# zdazy na sybilant 50-150 ms), attack=4 (detekcja rosnie w 4 ms, ciecie puszcza w ok. 16 ms).
DET = "dfrequency=6500:dqfactor=1.5:dftype=bandpass"
DEESS = ("adynamicequalizer=threshold={thr:.6f}:" + DET + ":tfrequency=6500:tqfactor=1.0:tftype=bell:"
         "attack=4:release=2:ratio=0.7:range=9:mode=cutabove")
COMP = "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5"
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def read(p):
    with wave.open(str(p)) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768 if sw == 2 else \
        np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2 ** 31
    return sr, x.reshape(-1, ch).mean(axis=1)


def raw_concat(edl, out):
    """Te same ciecia i fade'y co w aroll.py, bez obrobki."""
    cmd, af, al = list(FF), [], []
    for e in edl:
        dur, k = e["t_out"] - e["t_in"], e["i"]
        cmd += ["-ss", f"{e['a_in']:.4f}", "-t", f"{dur:.4f}", "-i", str(aroll.AUDIO)]
        af.append(f"[{k}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(0.0, dur - 0.04):.4f}:d=0.04[a{k}]")
        al.append(f"[a{k}]")
    af.append("".join(al) + f"concat=n={len(al)}:v=0:a=1[ac]")
    subprocess.run(cmd + ["-filter_complex", ";".join(af), "-map", "[ac]", "-c:a", "pcm_s32le", str(out)], check=True)


def deess_threshold(eq_wav, td):
    """Prog de-essera z rozkladu poziomu pasma detekcji w ramkach 10 ms: srednia z |pasma|, bo tak widzi to detektor
    filtra (jednobiegunowe wygladzanie |x| ze stala kilku ms; szczyt w ramce bylby ok. 10 dB wyzej).
    Tnie ok. 60% ramek sybilantow (glosniejsze mocniej), samogloski zostawia w spokoju (ich 98. percentyl nizej)."""
    lw = Path(td) / "listen.wav"
    subprocess.run(FF + ["-i", str(eq_wav), "-af", f"adynamicequalizer=mode=listen:{DET}", "-c:a", "pcm_s32le", str(lw)],
                   check=True)
    sr, det = read(lw)
    _, x = read(eq_wav)
    h = sr // 100  # 10 ms
    n = min(len(det), len(x)) // h
    fr = x[:n * h].reshape(n, h)
    d_db = 20 * np.log10(np.abs(det[:n * h]).reshape(n, h).mean(axis=1) + 1e-9)
    S = np.abs(np.fft.rfft(fr * np.hanning(h), axis=1)) ** 2
    f = np.fft.rfftfreq(h, 1 / sr)
    e_hi, e_mid = S[:, (f >= 4500) & (f < 9000)].sum(axis=1), S[:, (f >= 300) & (f < 2000)].sum(axis=1)
    lvl = 10 * np.log10(S.sum(axis=1) + 1e-12)
    speech = lvl > lvl.max() - 35
    sib, vow = speech & (e_hi > e_mid), speech & (e_mid > 10 * e_hi)
    v98, s40 = float(np.percentile(d_db[vow], 98)), float(np.percentile(d_db[sib], 40))
    thr_db = max(v98, s40)
    print(f"de-esser: ramki mowy {speech.sum()}, sybilanty {sib.sum()}, samogloski {vow.sum()} | pasmo detekcji: "
          f"samogloski p50 {np.percentile(d_db[vow], 50):.1f} / p98 {v98:.1f} dB, "
          f"sybilanty p40 {s40:.1f} / p90 {np.percentile(d_db[sib], 90):.1f} dB -> prog {thr_db:.1f} dB")
    return 10 ** (thr_db / 20)


def loudnorm(src, out, extra=""):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    st = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
          f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
          "linear=true,aresample=48000")
    subprocess.run(FF + ["-i", str(src), "-af", ln, "-c:a", "pcm_s16le", str(out)], check=True)
    return st


def main():
    edl = json.loads((P / "aroll/edl.json").read_text())
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        raw_concat(edl, raw)
        # kontrola: lancuch A z tych samych surowych ciec musi dac to samo co aroll.wav
        a_pre, a_chk = Path(td) / "a_pre.wav", Path(td) / "a_chk.wav"
        subprocess.run(FF + ["-i", str(raw), "-af", A_CHAIN, "-c:a", "pcm_s24le", str(a_pre)], check=True)
        loudnorm(a_pre, a_chk)
        _, a1 = read(P / "audio/aroll.wav")
        _, a2 = read(a_chk)
        m = min(len(a1), len(a2))
        res = 20 * np.log10(np.sqrt(np.mean((a1[:m] - a2[:m]) ** 2)) / np.sqrt(np.mean(a1[:m] ** 2)) + 1e-12)
        print(f"kontrola A (odtworzone z surowych ciec vs aroll.wav): roznica {res:.1f} dB")
        # B
        eq = Path(td) / "eq.wav"
        subprocess.run(FF + ["-i", str(raw), "-af", EQ, "-c:a", "pcm_s32le", str(eq)], check=True)
        thr = deess_threshold(eq, td)
        b_pre = Path(td) / "b_pre.wav"
        subprocess.run(FF + ["-i", str(eq), "-af", DEESS.format(thr=thr) + "," + COMP, "-c:a", "pcm_s24le", str(b_pre)],
                       check=True)
        st = loudnorm(b_pre, P / "audio/aroll_miekki.wav")
        print(f"B: {P / 'audio/aroll_miekki.wav'} | loudnorm in {st['input_i']} LUFS, prog de-essera {20 * np.log10(thr):.1f} dB")


if __name__ == "__main__":
    main()

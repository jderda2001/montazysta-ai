#!/usr/bin/env python3
"""Buduje A-roll (ciecie dubli, kadrowanie 9:16, grading, dzwiek) dla wersji A i B.

Uzycie: python3 -I aroll.py A|B
Wynik:  ../aroll/aroll_<wersja>.mp4 oraz ../aroll/edl_<wersja>.json (czasy segmentow na osi montazu)
"""
import json
import subprocess
import sys
from pathlib import Path

SRC = Path.home() / "Desktop/Montażysta AI/Nagrania /IMG_0361.mov"  # do 13.11.2026 w Eksporty
OUT = Path(__file__).resolve().parent.parent / "aroll"
OUT.mkdir(exist_ok=True)

# Zrodlo po obrocie: 2160x3840. Twarz ok. x=0.555, y=0.4375 wysokosci.
# Kadry (crop w px zrodla): W = szeroki, M = sredni, C = bliski (1:1 piksel).
FRAMES = {
    "W": (1728, 3072, 281, 461),   # zoom 1.25
    "M": (1350, 2400, 524, 816),   # zoom 1.6
    "C": (1080, 1920, 659, 950),   # zoom 2.0
}

PRE, POST = 0.10, 0.15

# (start_wyspy, koniec_wyspy, kadr, opis) - czasy z detekcji ciszy w zrodle
HOOK_A = [
    (25.47, 29.11, "M", "Zatrudniłeś przedstawicieli, którzy mieli Ci dostarczać sprawy na służebność przesyłu?"),
    (33.12, 38.73, "C", "A oni jedyne co robią, to jeżdżą od drzwi do drzwi..."),
]
HOOK_B = [
    (59.13, 62.05, "C", "Przedstawiciel bez leadów to koszt, który rośnie każdego miesiąca."),
]
BODY = [
    (96.72, 100.01, "W", "Kancelarie rekrutują ludzi na odszkodowania za służebność przesyłu,"),
    (105.05, 107.30, "C", "szybciej, niż zdobywają na to klientów."),
    (113.32, 118.31, "M", "Po ostatnich wyrokach TK kancelarie ruszyły z rekrutacją przedstawicieli."),
    (124.34, 128.01, "W", "Tyle, że przedstawiciel bez spotkań to pensja, paliwo."),
    (130.17, 132.79, "C", "I co najważniejsze, ogromna frustracja, gdy nie sprzedaje."),
    (143.00, 144.80, "M", "Dostarczamy właścicieli działek budowlanych"),
    (147.62, 149.49, "M", "pod liniami średniego i wysokiego napięcia."),
    (161.43, 163.21, "W", "Sprawdzonych telefonicznie w województwach,"),
    (166.75, 167.53, "W", "w których pracuje Twój zespół."),
    (172.32, 174.32, "C", "Wolumen dobieramy do liczby przedstawicieli."),
    (176.93, 179.18, "M", "A każdy lead dostaje tylko jedna kancelaria."),
    (188.37, 191.42, "C", "Zostaw kontakt poniżej i dobierzemy idealny wolumen dla Twojego zespołu."),
]
END_HOLD = 2.5  # przytrzymanie ostatniego ujecia pod plansze koncowa

GRADE = (
    "eq=contrast=1.07:saturation=1.12:gamma=0.97,"
    "colortemperature=temperature=6200:mix=0.35,"
    "vignette=angle=PI/5:mode=forward"
)


def build(version: str) -> None:
    segs = (HOOK_A if version == "A" else HOOK_B) + BODY
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    filters, vlabels, alabels, edl = [], [], [], []
    t = 0.0
    for i, (a, b, frame, text) in enumerate(segs):
        start = max(0.0, a - PRE)
        end = b + POST + (END_HOLD if i == len(segs) - 1 else 0.0)
        dur = round((end - start) * 30) / 30  # rowno w klatkach 30 fps
        cmd += ["-ss", f"{start:.3f}", "-t", f"{dur:.4f}", "-i", str(SRC)]
        w, h, x, y = FRAMES[frame]
        filters.append(
            f"[{i}:v:0]crop={w}:{h}:{x}:{y},"
            f"scale=1080:1920:flags=lanczos:in_range=pc:out_range=tv,"
            f"{GRADE},fps=30,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{i}]"
        )
        fade_out_st = max(0.0, dur - 0.04)
        filters.append(
            f"[{i}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.02,afade=t=out:st={fade_out_st:.4f}:d=0.04[a{i}]"
        )
        vlabels.append(f"[v{i}]")
        alabels.append(f"[a{i}]")
        edl.append({"i": i, "src_in": round(start, 3), "src_out": round(start + dur, 3),
                    "t_in": round(t, 3), "t_out": round(t + dur, 3), "frame": frame, "text": text})
        t += dur
    n = len(segs)
    filters.append("".join(v + a for v, a in zip(vlabels, alabels)) + f"concat=n={n}:v=1:a=1[vc][ac]")
    filters.append(
        "[ac]highpass=f=80,afftdn=nr=10:nf=-60,"
        "acompressor=threshold=-26dB:ratio=3:attack=5:release=90:makeup=2,"
        "loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000[aout]"
    )
    out = OUT / f"aroll_{version}.mp4"
    cmd += ["-filter_complex", ";".join(filters), "-map", "[vc]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
            "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    (OUT / f"edl_{version}.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1))
    print(f"{version}: {out} ({t:.2f}s, {n} segmentow)")


if __name__ == "__main__":
    for v in sys.argv[1:] or ["A", "B"]:
        build(v)

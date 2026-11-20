#!/usr/bin/env python3
"""A-roll rolki o Kaji: obraz z telefonu (IMG_0526.mov), dzwiek z osobnego nagrania (mikrofon),
zsynchronizowany korelacja krzyzowa (analiza/sync.json). Ciecie dubli, kadry 9:16, grading, mastering dzwieku.

Uzycie: python3 -I aroll.py            -> ../aroll/aroll.mp4 + ../aroll/edl.json
        python3 -I aroll.py --edl-only -> tylko ../aroll/edl.json (bez renderu)
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
VIDEO = Path.home() / "Downloads/IMG_0526.mov"
AUDIO = Path.home() / "Desktop/Montażysta AI/Nagrania /Audio do rolki o Kaji.m4a"
OUT = P / "aroll"
OUT.mkdir(exist_ok=True)
OFFSET = round(json.loads((P / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie: 1080x1920. Twarz ok. (508, 653). Kadry (w, h, x, y) w px zrodla.
FRAMES = {
    "W": (1080, 1920, 0, 0),      # pelny kadr
    "M": (940, 1672, 38, 102),    # zoom 1.15
    "C": (832, 1478, 92, 180),    # zoom 1.30
}
PRE, POST = 0.10, 0.15
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst) - czasy w NOWYM AUDIO.
# Zasada: ostatni pelny dubel kazdej kwestii. Kolejne pozycje listy kadrow = zmiana kadru w trakcie kwestii.
# Falstarty na poczatku dubla (whisper je wygladza - sprawdzac kawalki miedzy pauzami osobno):
#   55.61 "I każdego ranka dosta-", 70.57 "CRM jest wz-", 202.40 "Jeśli interesuje Cię, jak sobie tak-"
#   -> kwestie startuja od powtorzenia (56.97 / 71.73 / 203.97).
SEGS = [
    (10.28, 13.38, [(None, "W")], "Setter kosztuje Cię w okolicach 5–6 koła miesięcznie."),
    (13.76, 15.72, [(None, "C")], "Moja Kaja kosztuje mnie niecałe dwie stówki."),
    (29.80, 32.93, [(None, "M")], "Pilnuje pipeline'u, pisze do leadów, przygotowuje oferty."),
    (56.97, 60.49, [(None, "W")], "I każdego ranka dostaję od niej to, co jest konkretnie na ten dzień do zrobienia."),
    (71.73, 73.28, [(None, "M")], "CRM jest zawsze uporządkowany."),
    (88.25, 91.60, [(None, "C")], "Każde spotkanie ląduje w kalendarzu i wysyła się zaproszenie do klienta."),
    (102.77, 105.73, [(None, "W")], "Nie bierze urlopu, nie choruje i nigdy nie zapomina o follow-upach."),
    (113.43, 118.62, [(None, "C")], "Czy się myli? Czasem tak. Z tym, że setter też się myli, a kosztuje 30 razy więcej."),
    # zmiany kadru w pauzach: po "oczywiste." / po "pierwszego," / przed "Czy na pewno agent AI"
    (132.15, 144.20, [(None, "M"), (134.23, "W"), (138.73, "C"), (141.58, "M")],
     "Kaja to agent AI, to oczywiste. Z tym, że teraz zadanie dla Ciebie. Zanim zatrudnisz kolejnego settera, "
     "bądź swojego pierwszego, zastanów się dwa razy, czy na pewno go potrzebujesz. "
     "Czy na pewno agent AI po prostu nie wystarczy?"),
    (203.97, 209.80, [(None, "C")],
     "Jeśli interesuje Cię, skąd taką Kaję wytrzasnąć, napisz komentarz o treści Kaja, a nagram o tym osobną rolkę."),
]

GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
FPS = 30


def fr(t):
    return round(t * FPS) / FPS


def make_edl():
    edl, t = [], 0.0
    for i, (s, e, shots, text) in enumerate(SEGS):
        a_in = s - PRE
        a_out = e + POST + (END_HOLD if i == len(SEGS) - 1 else 0.0)
        dur = fr(a_out - a_in)
        sh = []
        for k, (frm, frame) in enumerate(shots):
            rel = 0.0 if frm is None else fr(frm - a_in)
            sh.append({"frame": frame, "rel": rel, "t_in": round(t + rel, 4)})
        for k in range(len(sh)):
            sh[k]["dur"] = round((sh[k + 1]["rel"] if k + 1 < len(sh) else dur) - sh[k]["rel"], 4)
        edl.append({"i": i, "a_in": round(a_in, 4), "a_out": round(a_in + dur, 4),
                    "v_in": round(a_in - OFFSET, 4), "t_in": round(t, 4), "t_out": round(t + dur, 4),
                    "speech": [s, e], "shots": sh, "text": text})
        t += dur
    return edl


def loudnorm_stats(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def build(edl):
    vcmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    acmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    vf, af, vl, al = [], [], [], []
    n_in = 0
    for e in edl:
        for sh in e["shots"]:
            vcmd += ["-ss", f"{e['v_in'] + sh['rel']:.4f}", "-t", f"{sh['dur']:.4f}", "-i", str(VIDEO)]
            w, h, x, y = FRAMES[sh["frame"]]
            vf.append(f"[{n_in}:v:0]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range=pc:out_range=tv,"
                      f"{GRADE},fps={FPS},trim=duration={sh['dur']:.4f},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{n_in}]")
            vl.append(f"[v{n_in}]")
            n_in += 1
        dur = e["t_out"] - e["t_in"]
        k = e["i"]
        acmd += ["-ss", f"{e['a_in']:.4f}", "-t", f"{dur:.4f}", "-i", str(AUDIO)]
        af.append(f"[{k}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(0.0, dur - 0.04):.4f}:d=0.04[a{k}]")
        al.append(f"[a{k}]")
    vf.append("".join(vl) + f"concat=n={len(vl)}:v=1:a=0[vc]")
    af.append("".join(al) + f"concat=n={len(al)}:v=0:a=1,highpass=f=70,"
              "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5[ac]")
    with tempfile.TemporaryDirectory() as td:
        vtmp, atmp = Path(td) / "v.mp4", Path(td) / "a.wav"
        subprocess.run(vcmd + ["-filter_complex", ";".join(vf), "-map", "[vc]", "-c:v", "libx264", "-preset", "slow",
                               "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                               "-color_primaries", "bt709", "-color_trc", "bt709", str(vtmp)], check=True)
        subprocess.run(acmd + ["-filter_complex", ";".join(af), "-map", "[ac]", "-c:a", "pcm_s24le", str(atmp)],
                       check=True)
        st = loudnorm_stats(atmp)
        ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
              f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
              "linear=true,aresample=48000")
        wav = P / "audio/aroll.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(atmp), "-af", ln,
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        out = OUT / "aroll.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(vtmp), "-i", str(wav),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest",
                        "-movflags", "+faststart", str(out)], check=True)
    print(f"aroll: {out} ({edl[-1]['t_out']:.2f}s, {len(edl)} kwestii, {n_in} ujec) | loudnorm in {st['input_i']} LUFS")


if __name__ == "__main__":
    edl = make_edl()
    (OUT / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1))
    for e in edl:
        print(f"{e['i']:2d} {e['t_in']:6.2f}-{e['t_out']:6.2f}  audio {e['a_in']:7.2f}  wideo {e['v_in']:7.2f}  "
              f"{'/'.join(s['frame'] for s in e['shots'])}  {e['text'][:60]}")
    if "--edl-only" not in sys.argv:
        build(edl)

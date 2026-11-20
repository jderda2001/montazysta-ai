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
# Po zdaniu 0,22 s, przed zdaniem 0,14 s. Przy 0,10 / 0,15 Jakub uznal czesc ciec za zbyt szybkie (IMG_0597, 18.11.2026):
# naturalne pauzy kurczyly sie do 0,25 s, a ciche koncowki slow wpadaly w wyciszenie. Ciecia w srodku zdania wymagaja
# ciasniejszych wartosci per kwestia - patrz projekty/IMG_0597/skrypty/aroll.py.
PRE, POST = 0.14, 0.22
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst[, wytnij]) - czasy w NOWYM AUDIO.
# wytnij = [(od, do), ...]: kawalki usuwane ze SRODKA kwestii (zajakniecie w slowie, powtorzone slowo, pauza w srodku slowa
#   "do... kładnie"). Ciecie jest ciasne (bez PRE/POST, zanik 6 ms): "od" wyrownuje sie do klatki liczac od poczatku kawalka,
#   "do" jest co do milisekundy. Tnij w ciszy albo w zwarciu spolgloski (fonemy.py), a skok obrazu schowaj zmiana kadru
#   ustawiona dokladnie na "do", np. (9.99, 16.00, [(None, "W"), (14.40, "C")], "...", [(14.2567, 14.40)]).
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


def src_range():
    """Zakres kolorow zrodla: "pc" (pelny, np. iPhone 1080p yuvj420p) albo "tv" (ograniczony, np. iPhone 4K HEVC).
    Wpisany na sztywno "pc" splaszczal kontrast nagran 4K (czern 49 -> 58, biel 192 -> 181; IMG_0576, IMG_0585)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_range",
                        "-of", "csv=p=0", str(VIDEO)], capture_output=True, text=True).stdout.strip().strip(",")
    return "pc" if r in ("pc", "jpeg") else "tv"


def make_edl():
    edl, t = [], 0.0
    for i, seg in enumerate(SEGS):
        s, e, shots, text = seg[:4]
        cuts = sorted(seg[4]) if len(seg) > 4 else []
        a_in = s - PRE
        a_out = e + POST + (END_HOLD if i == len(SEGS) - 1 else 0.0)
        parts, p, o = [], a_in, 0.0      # kawalki nagrania: [poczatek w nagraniu, dlugosc, poczatek w kwestii]
        for c0, c1 in cuts + [(a_out, None)]:
            d = fr(c0 - p)
            parts.append([round(p, 4), round(d, 4), round(o, 4)])
            o, p = fr(o + d), c1
        dur = o

        def rel_of(frm):  # czas w nagraniu -> czas od poczatku kwestii (po wycieciach)
            for p_in, d, o_k in reversed(parts):
                if frm >= p_in - 1e-6:
                    return fr(o_k + min(frm - p_in, d))
            return 0.0

        sh = []
        for k, (frm, frame) in enumerate(shots):
            rel = 0.0 if frm is None else rel_of(frm)
            sh.append({"frame": frame, "rel": rel, "t_in": round(t + rel, 4)})
        for k in range(len(sh)):
            sh[k]["dur"] = round((sh[k + 1]["rel"] if k + 1 < len(sh) else dur) - sh[k]["rel"], 4)
        clips = []  # ujecia pociete na kawalki nagrania, w kolejnosci montazu
        for x in sh:
            for p_in, d, o_k in parts:
                c0, c1 = max(x["rel"], o_k), min(x["rel"] + x["dur"], o_k + d)
                if c1 - c0 > 0.001:
                    clips.append({"frame": x["frame"], "v_in": round(p_in - OFFSET + (c0 - o_k), 4), "dur": round(c1 - c0, 4)})
        edl.append({"i": i, "a_in": round(a_in, 4), "a_out": round(parts[-1][0] + parts[-1][1], 4),
                    "v_in": round(a_in - OFFSET, 4), "t_in": round(t, 4), "t_out": round(t + dur, 4),
                    "speech": [s, e], "shots": sh, "parts": [[p_in, d] for p_in, d, _ in parts], "clips": clips, "text": text})
        t = fr(t + dur)
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
    rng = src_range()
    n_a = 0
    for e in edl:
        for c in e["clips"]:
            vcmd += ["-ss", f"{c['v_in']:.4f}", "-t", f"{c['dur']:.4f}", "-i", str(VIDEO)]
            w, h, x, y = FRAMES[c["frame"]]
            vf.append(f"[{n_in}:v:0]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range={rng}:out_range=tv,"
                      f"{GRADE},fps={FPS},trim=duration={c['dur']:.4f},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{n_in}]")
            vl.append(f"[v{n_in}]")
            n_in += 1
        for k, (p_in, d) in enumerate(e["parts"]):
            # zaniki: na brzegach kwestii jak zawsze, na cieciu w srodku kwestii tylko 6 ms (ciecie wypada w ciszy albo w zwarciu)
            fi = 0.02 if k == 0 else 0.006
            fo = 0.04 if k == len(e["parts"]) - 1 else 0.006
            acmd += ["-ss", f"{p_in:.4f}", "-t", f"{d:.4f}", "-i", str(AUDIO)]
            af.append(f"[{n_a}:a:0]aresample=48000,atrim=0:{d:.4f},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d={fi},afade=t=out:st={max(0.0, d - fo):.4f}:d={fo}[a{n_a}]")
            al.append(f"[a{n_a}]")
            n_a += 1
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
        if len(e["parts"]) > 1:
            print("     wyciete ze srodka: " + ", ".join(f"{a[0] + a[1]:.3f}-{b[0]:.3f}" for a, b in zip(e["parts"], e["parts"][1:])))
    if "--edl-only" not in sys.argv:
        build(edl)

#!/usr/bin/env python3
"""A-roll reklamy adGen "Służebność przesyłu" (IMG_0585): obraz i dzwiek z telefonu (mikrofon DJI podpiety do
iPhone'a, brak osobnego nagrania), wiec offset 0. Trzy wersje: hook A / B / C + wspolny korpus.
Ciecie dubli, kadry 9:16 ze zrodla 4K, grading, mastering dzwieku.

Uzycie: HOOK=A python3 -I aroll.py            -> ../A/aroll/aroll.mp4 + ../A/aroll/edl.json
        HOOK=B python3 -I aroll.py --edl-only -> tylko ../B/aroll/edl.json (bez renderu)
        HOOK=A python3 -I aroll.py --audio-only -> tylko dzwiek (audio/aroll.wav + podmiana w aroll.mp4), obraz bez zmian
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = os.environ.get("HOOK", "A")
P = ROOT / HOOK                      # kazda wersja ma swoj folder: A/, B/, C/ (aroll, audio, hf)
VIDEO = Path.home() / "Downloads/IMG_0585.MOV"
AUDIO = VIDEO  # dzwiek z tego samego pliku
OUT = P / "aroll"
OUT.mkdir(parents=True, exist_ok=True)
(P / "audio").mkdir(exist_ok=True)
OFFSET = round(json.loads((ROOT / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie: 2160x3840 (4K, 60 kl./s, zakres tv). Twarz ok. (950, 1700), miedzy dublami chodzi o +-80 px.
# Kadry (w, h, x, y) w px zrodla.
FRAMES = {
    "W": (2160, 3840, 0, 0),       # pelny kadr (twarz na ok. 44% wysokosci, nad glowa miejsce na nakladki)
    "M": (1800, 3200, 50, 420),    # zoom 1.2
    "C": (1544, 2744, 178, 644),   # zoom 1.4 (zrodlo 4K, wiec jest zapas)
}
PRE, POST = 0.10, 0.15
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst[, {"post": s}]) - czasy w nagraniu.
# Zasada: ostatni pelny dubel kazdej kwestii. W tym nagraniu przed prawie kazdym dublem jest cicha proba
# (czytanie skryptu polglosem, szczyt -20...-30 dB) - "wykonania" maja szczyt -5...-12 dB.
# Falstarty wykryte kawalkami (skrypty/kawalki_zakres.py), kwestie startuja od powtorzenia:
#   20.31 "Po wyroku..." -> 21.47; 64.80/66.02 "U nas / U nas za..." -> 69.59; 173.45 "Każdy od razu ląduje" -> 175.24;
#   230.58 urwane "Płacisz za li..." -> 231.77; 213.18 "Dostajesz wtedy ... rozmowę z całej rozmowy" (przejezyczenie) -> 218.46.
HOOKS = {
    "A": [(21.47, 25.84, [(None, "C")],
           "Po wyroku Trybunału Konstytucyjnego właściciele działek znowu pytają o wynagrodzenie.")],
    "B": [(31.92, 33.74, [(None, "M")], "Prowadzisz sprawy o służebność przesyłu?"),
          (41.00, 46.22, [(None, "C")],
           "Możemy przełączyć właściciela działki zaraz po naszej rozmowie do Twojego handlowca. Na żywo.")],
    "C": [(55.09, 59.89, [(None, "M")],
           "Dzwonisz do leada o służebność przesyłu, a on kompletnie nie pamięta, że zostawiał gdziekolwiek kontakt?"),
          (69.59, 71.79, [(None, "C")], "U nas każdy najpierw rozmawia z naszym zespołem.")],
}
BODY = [
    (118.26, 122.74, [(None, "W")], "Dostarczamy kancelariom właścicieli działek ze słupami i służebnościami na gruncie,"),
    (127.77, 130.18, [(None, "M")], "którzy chcą sprawdzić, czy należy im się wynagrodzenie."),
    (134.16, 137.34, [(None, "C")], "Nasz zespół za każdym razem najpierw dzwoni do każdego z nich,"),
    (146.08, 153.69, [(None, "W")],
     "aby zapytać o wysokość napięcia, rodzaj działki, dokładny adres i numer działki, a także o księgę wieczystą."),
    (164.73, 168.95, [(None, "M")], "Dostajesz tylko tych, którzy odebrali i potwierdzili, że chcą rozmowy z prawnikiem."),
    (175.24, 177.97, [(None, "W")], "Każdy od razu ląduje w Twoim CRM z notatką z rozmowy."),
    # 213.18 zaczyna sie odrzucony dubel nastepnego zdania; cisza tylko 213.03-213.15 -> krotszy ogon
    (210.14, 213.01, [(None, "C")], "W tej niszy możemy też przełączyć rozmowę na żywo do Twojego handlowca.", {"post": 0.09}),
    (218.46, 220.64, [(None, "M")], "Dostajesz wtedy nagranie z całej rozmowy."),
    (224.85, 227.06, [(None, "W")], "Pierwsze leady masz do 24 godzin od startu."),
    (231.77, 236.25, [(None, "C")], "Płacisz tylko i wyłącznie za zapytania, nie za jakiś budżet reklamowy czy godziny zespołu."),
    (240.61, 242.97, [(None, "W")], "Co ważne, każde zamówienie jest objęte gwarancją."),
    (247.69, 253.97, [(None, "M"), (248.84, "C")],
     "Zostaw kontakt poniżej. Oddzwonię i powiem Ci, ile i do kiedy możemy dostarczyć Ci jaką ilość leadów na służebności."),
]
SEGS = HOOKS[HOOK] + BODY
N_HOOK = len(HOOKS[HOOK])  # ile pierwszych kwestii to hook
# wyrownanie glosnosci miedzy kwestiami (skrypty/poziomy.py); brak pliku = bez korekty
_lv = ROOT / "analiza/poziomy.json"
GAIN = json.loads(_lv.read_text())["gain_db"] if _lv.exists() else {}

GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
FPS = 30


def fr(t):
    return round(t * FPS) / FPS


def src_range():
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_range",
                        "-of", "csv=p=0", str(VIDEO)], capture_output=True, text=True).stdout.strip()
    return "pc" if r in ("pc", "jpeg") else "tv"


def make_edl():
    edl, t = [], 0.0
    for i, (s, e, shots, text, *opt) in enumerate(SEGS):
        o = opt[0] if opt else {}
        a_in = s - o.get("pre", PRE)
        a_out = e + o.get("post", POST) + (END_HOLD if i == len(SEGS) - 1 else 0.0)
        dur = fr(a_out - a_in)
        sh = []
        for k, (frm, frame) in enumerate(shots):
            rel = 0.0 if frm is None else fr(frm - a_in)
            sh.append({"frame": frame, "rel": rel, "t_in": round(t + rel, 4)})
        for k in range(len(sh)):
            sh[k]["dur"] = round((sh[k + 1]["rel"] if k + 1 < len(sh) else dur) - sh[k]["rel"], 4)
        edl.append({"i": i, "a_in": round(a_in, 4), "a_out": round(a_in + dur, 4),
                    "v_in": round(a_in - OFFSET, 4), "t_in": round(t, 4), "t_out": round(t + dur, 4),
                    "speech": [s, e], "shots": sh, "text": text, "hook": i < N_HOOK,
                    "gain_db": GAIN.get(f"{s:.2f}-{e:.2f}", 0.0),
                    "hold": END_HOLD if i == len(SEGS) - 1 else 0.0})
        t += dur
    return edl


def loudnorm_stats(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def audio_filter(edl):
    """Wejscia i filtr dzwieku: ciecia jak w obrazie, wyrownanie glosnosci kwestii, cisza pod plansze koncowa,
    lekki mastering (highpass 70 Hz, kompresja 2,5:1). To jest glos w filmie (naturalny, bez AI) - audio/aroll.wav."""
    acmd, af, al = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"], [], []
    for e in edl:
        dur, k = e["t_out"] - e["t_in"], e["i"]
        acmd += ["-ss", f"{e['a_in']:.4f}", "-t", f"{dur:.4f}", "-i", str(AUDIO)]
        af.append(f"[{k}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,volume={e.get('gain_db', 0.0):.2f}dB,"
                  f"afade=t=in:d=0.02," + (
                      # ostatnia kwestia: po mowie cisza pod plansze koncowa (w nagraniu jest tam szmer przy siegnieciu
                      # po telefon; po kompresji i normalizacji bylby slyszalnym stuknieciem)
                      f"afade=t=out:st={dur - e['hold']:.4f}:d=0.10[a{k}]" if e.get("hold") else
                      f"afade=t=out:st={max(0.0, dur - 0.04):.4f}:d=0.04[a{k}]"))
        al.append(f"[a{k}]")
    af.append("".join(al) + f"concat=n={len(al)}:v=0:a=1,highpass=f=70,"
              "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5[ac]")
    return acmd, af


def build_audio(edl, td):
    acmd, af = audio_filter(edl)
    atmp = Path(td) / "a.wav"
    subprocess.run(acmd + ["-filter_complex", ";".join(af), "-map", "[ac]", "-c:a", "pcm_s24le", str(atmp)], check=True)
    st = loudnorm_stats(atmp)
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
          f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
          "linear=true,aresample=48000,"
          # kodowanie AAC podbija szczyt o 0,1-0,2 dB, wiec plik wychodzil z -1,3 dBFS zamiast -1,5.
          # Limiter tylko przycina najwyzsze szczyty do -1,9 dBFS (glosnosc bez zmian).
          "alimiter=limit=0.8035:level=false:attack=5:release=50,aresample=48000")
    wav = P / "audio/aroll.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(atmp), "-af", ln,
                    "-c:a", "pcm_s16le", str(wav)], check=True)
    return wav, st


def mux(video, wav, out):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest",
                    "-movflags", "+faststart", str(out)], check=True)


def build(edl, audio_only=False):
    out = OUT / "aroll.mp4"
    with tempfile.TemporaryDirectory() as td:
        if audio_only:  # obraz bez zmian (te same ciecia), tylko nowy dzwiek
            wav, st = build_audio(edl, td)
            tmp = Path(td) / "mux.mp4"
            mux(out, wav, tmp)
            os.replace(tmp, out)
            print(f"aroll (tylko dzwiek): {wav} | loudnorm in {st['input_i']} LUFS")
            return
        vcmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        vf, vl, n_in = [], [], 0
        rng = src_range()
        for e in edl:
            for sh in e["shots"]:
                vcmd += ["-ss", f"{e['v_in'] + sh['rel']:.4f}", "-t", f"{sh['dur']:.4f}", "-i", str(VIDEO)]
                w, h, x, y = FRAMES[sh["frame"]]
                vf.append(f"[{n_in}:v:0]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range={rng}:out_range=tv,"
                          f"{GRADE},fps={FPS},trim=duration={sh['dur']:.4f},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{n_in}]")
                vl.append(f"[v{n_in}]")
                n_in += 1
        vf.append("".join(vl) + f"concat=n={len(vl)}:v=1:a=0[vc]")
        vtmp = Path(td) / "v.mp4"
        subprocess.run(vcmd + ["-filter_complex", ";".join(vf), "-map", "[vc]", "-c:v", "libx264", "-preset", "slow",
                               "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                               "-color_primaries", "bt709", "-color_trc", "bt709", str(vtmp)], check=True)
        wav, st = build_audio(edl, td)
        mux(vtmp, wav, out)
    print(f"aroll: {out} ({edl[-1]['t_out']:.2f}s, {len(edl)} kwestii, {n_in} ujec) | loudnorm in {st['input_i']} LUFS")


if __name__ == "__main__":
    edl = make_edl()
    (OUT / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1))
    for e in edl:
        print(f"{e['i']:2d} {e['t_in']:6.2f}-{e['t_out']:6.2f}  audio {e['a_in']:7.2f}  wideo {e['v_in']:7.2f}  "
              f"{'/'.join(s['frame'] for s in e['shots'])}  {e['text'][:60]}")
    if "--edl-only" not in sys.argv:
        build(edl, audio_only="--audio-only" in sys.argv)

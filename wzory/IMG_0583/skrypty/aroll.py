#!/usr/bin/env python3
"""A-roll reklam adGen "Leady z OC" (IMG_0583): obraz i dzwiek z telefonu (mikrofon krawatowy podpiety do iPhone'a,
brak osobnego nagrania), wiec offset 0. Ciecie dubli, kadry 9:16 ze zrodla 4K, grading, mastering dzwieku.

Trzy wersje (hook A / B / C + wspolny korpus i CTA). Wersje wybiera nazwa folderu roboczego: skrypty leza w
IMG_0583/skrypty (zrodlo prawdy) i sa kopiowane do IMG_0583/A|B|C/skrypty przez przebieg.sh.

Uzycie: python3 -I aroll.py              -> ../aroll/aroll.mp4 + ../aroll/edl.json + ../audio/aroll.wav
        python3 -I aroll.py --edl-only   -> tylko ../aroll/edl.json (bez renderu)
        python3 -I aroll.py --audio-only -> tylko dzwiek (audio/aroll.wav + podmiana w aroll.mp4), obraz bez zmian
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
VIDEO = Path.home() / "Downloads/IMG_0583.MOV"
AUDIO = VIDEO  # dzwiek z tego samego pliku
HOOK = P.name if P.name in ("A", "B", "C") else "A"
OUT = P / "aroll"
OUT.mkdir(exist_ok=True)
OFFSET = round(json.loads((P / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie: 2160x3840 (4K, 60 kl./s, zakres tv). Jakub siedzi nisko w kadrze (twarz na ok. 44% wysokosci,
# zajmuje 19% wysokosci), wiec kadry sa ciasniejsze niz "pelny kadr" - tak, zeby twarz miala wielkosc jak we wzorcu
# IMG_0526 (ok. 25-33% wysokosci). Kadr = (zoom, pozycja srodka twarzy w pionie jako ulamek wysokosci wyjscia).
# Srodek twarzy (px zrodla) podany osobno dla kazdej kwestii, bo miedzy dublami sie przesuwa.
SRC_W, SRC_H = 2160, 3840
FRAMES = {
    "W": (1.30, 0.345),
    "M": (1.50, 0.335),
    "C": (1.72, 0.330),
}
PRE, POST = 0.10, 0.15
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa
# Wyrownanie glosnosci miedzy kwestiami (skrypty/poziomy.py -> IMG_0583/analiza/poziomy.json): 80% roznicy do mediany,
# max +-4 dB. Glos idzie naturalny (bez Sidona), wiec roznice miedzy dublami nie sa juz zbijane gesta kompresja:
# "A tam cisza" jest o 8 dB cichsze od mediany, "Gwarantuję Ci" o 4 dB glosniejsze. Brak pliku = bez korekty.
_lv = P.parent / "analiza/poziomy.json"
GAIN = json.loads(_lv.read_text())["gain_db"] if _lv.exists() else {}

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst, (x, y) srodka twarzy) - czasy w nagraniu.
# Zasada: ostatni pelny dubel kazdej kwestii. Kolejne pozycje listy kadrow = zmiana kadru w trakcie kwestii (w pauzie).
# Falstarty wykryte kawalki.py (whisper na calym dublu je wygladzil), kwestie startuja od powtorzenia:
#   hook B:  36.81 "Dzwoni-" -> 37.27
#   hook C:  77.74 "Poszko-", 78.18 "Poszkodowany właśnie" -> 79.29 (trzecie podejscie, pelne zdanie, szybkie tempo)
#   korpus: 159.45 "Dostajesz tylko-" -> 160.34;  226.17 "Zostaw kontakt," -> 227.04
HOOKS = {
    "A": [
        (12.56, 14.66, [(None, "W")], "Prowadzisz kancelarię zajmującą się szkodami OC?", (1024, 1663)),
        # zmiany kadru w pauzach: po "telefonicznie," i przed cytatem
        (18.17, 25.80, [(None, "C"), (21.58, "M"), (23.92, "C")],
         "Płać tylko i wyłącznie za leady, które są zweryfikowane telefonicznie, a nie za takie, "
         "które za każdym razem mówią: „Ej, ja nie pamiętam, żebym cokolwiek wypełniał”.", (1080, 1640)),
    ],
    "B": [
        (37.27, 38.79, [(None, "W")], "Dzwonisz do leada ze szkody OC.", (983, 1720)),
        (39.47, 40.13, [(None, "C")], "A tam cisza.", (983, 1759)),
        (40.99, 45.57, [(None, "M"), (42.92, "C")],
         "Gwarantuję Ci, nasze leady odebrały telefon, zanim dotarły do Twojego CRM-a.", (1037, 1705)),
    ],
    "C": [
        (63.63, 65.45, [(None, "W")], "Ubezpieczyciel zaniżył odszkodowanie OC.", (1024, 1705)),
        (79.29, 81.48, [(None, "M")], "Poszkodowany właśnie teraz szuka kancelarii, która to sprawdzi.", (1000, 1705)),
        (84.71, 86.85, [(None, "C")], "I teraz pytanie: trafi do Ciebie, czy do konkurencji?", (1000, 1705)),
    ],
}
KORPUS = [
    (134.25, 137.93, [(None, "W")], "Dostarczamy kancelariom osoby, którym ubezpieczyciel wypłacił za mało z OC sprawcy", (1015, 1705)),
    (141.89, 144.33, [(None, "M")], "i które chcą sprawdzić, czy da się odzyskać więcej.", (983, 1720)),
    (149.41, 153.59, [(None, "C")], "Nasz zespół za każdym razem najpierw dzwoni do każdej z tych osób.", (960, 1680)),
    (160.34, 165.52, [(None, "W")], "Dostajesz tylko i wyłącznie te, które odebrały i chcą rozmawiać z prawnikiem.", (960, 1680)),
    (186.94, 189.96, [(None, "M")], "Każda od razu ląduje w Twoim CRM z notatką z rozmowy.", (976, 1720)),
    (194.19, 196.82, [(None, "C")], "Pierwsze leady masz do 48 godzin od startu.", (960, 1690)),
    (199.90, 202.72, [(None, "W")], "Płacisz za leady, a nie za budżet reklamowy czy czas zespołu.", (896, 1690)),
    (215.04, 217.76, [(None, "M")], "I co warto dodać, każde zamówienie jest objęte gwarancją.", (1000, 1690)),
    (227.04, 228.14, [(None, "W")], "Zostaw kontakt poniżej.", (944, 1690)),
    (228.75, 233.33, [(None, "C"), (230.37, "M")],
     "Oddzwonię i powiem Ci, ile i na kiedy mógłbym Ci dostarczyć pierwsze leady OC.", (1000, 1690)),
]
SEGS = HOOKS[HOOK] + KORPUS
N_HOOK = len(HOOKS[HOOK])  # ile pierwszych kwestii to hook


def crop(frame, face):
    """Kadr (w, h, x, y) w px zrodla: zoom i pozycja twarzy z FRAMES, srodek twarzy z kwestii."""
    z, fy = FRAMES[frame]
    w = int(SRC_W / z / 2) * 2
    h = int(round(w * 16 / 9 / 2)) * 2
    x = min(max(0, int(round(face[0] - w / 2))), SRC_W - w)
    y = min(max(0, int(round(face[1] - fy * h))), SRC_H - h)
    return w, h, x, y


GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
FPS = 30


def fr(t):
    return round(t * FPS) / FPS


def make_edl():
    edl, t = [], 0.0
    for i, (s, e, shots, text, face) in enumerate(SEGS):
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
                    "speech": [s, e], "shots": sh, "text": text, "face": list(face), "hook": i < N_HOOK,
                    "gain_db": GAIN.get(f"{s:.2f}-{e:.2f}", 0.0)})
        t += dur
    return edl


def loudnorm_stats(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def build_audio(edl, td):
    """Glos w filmie: naturalny, z mikrofonu (bez AI). Ciecia jak w obrazie, wyrownanie glosnosci kwestii,
    lekki mastering (highpass 70 Hz, kompresja 2,5:1), -14 LUFS dwuprzebiegowo -> audio/aroll.wav."""
    acmd, af, al = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"], [], []
    for e in edl:
        dur, k = e["t_out"] - e["t_in"], e["i"]
        acmd += ["-ss", f"{e['a_in']:.4f}", "-t", f"{dur:.4f}", "-i", str(AUDIO)]
        af.append(f"[{k}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,volume={e.get('gain_db', 0.0):.2f}dB,"
                  f"afade=t=in:d=0.02,afade=t=out:st={max(0.0, dur - 0.04):.4f}:d=0.04[a{k}]")
        al.append(f"[a{k}]")
    af.append("".join(al) + f"concat=n={len(al)}:v=0:a=1,highpass=f=70,"
              "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=1.5[ac]")
    atmp = Path(td) / "a.wav"
    subprocess.run(acmd + ["-filter_complex", ";".join(af), "-map", "[ac]", "-c:a", "pcm_s24le", str(atmp)], check=True)
    st = loudnorm_stats(atmp)
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
          f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:"
          "linear=true,"
          # Naturalny glos ma wyzsze szczyty niz glos po Sidonie i gestej kompresji: po loudnorm szczyt siedzi na -1,5,
          # a kodowanie AAC podbija go o ok. 0,1 dB (kontrola eksportu: -1,4 dBFS). Limiter zdejmuje tylko czubki
          # najwyzszych szczytow (do -2,0 dBFS); +0,15 dB wyrownuje glosnosc do -14,0 LUFS (szczyt ok. -1,8).
          "alimiter=level_in=1:level_out=1:limit=0.794:attack=2:release=60:level=disabled,volume=0.15dB,aresample=48000")
    wav = P / "audio/aroll.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(atmp), "-af", ln,
                    "-c:a", "pcm_s16le", str(wav)], check=True)
    return wav, st


def mux(video, wav, out):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                    "-movflags", "+faststart", str(out)], check=True)


def build(edl, audio_only=False):
    out = OUT / "aroll.mp4"
    with tempfile.TemporaryDirectory() as td:
        if audio_only:  # obraz bez zmian (te same ciecia), tylko nowy dzwiek
            wav, st = build_audio(edl, td)
            tmp = Path(td) / "mux.mp4"
            mux(out, wav, tmp)
            out.unlink()
            tmp.rename(out) if tmp.stat().st_dev == OUT.stat().st_dev else __import__("shutil").move(str(tmp), str(out))
            print(f"aroll (tylko dzwiek): {wav} | loudnorm in {st['input_i']} LUFS")
            return
        vcmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        vf, vl, n_in = [], [], 0
        for e in edl:
            for sh in e["shots"]:
                # Ujecie ciete co do klatki (zrodlo ma 60 kl./s): czytamy z zapasem i bierzemy dokladnie n klatek
                # po zmianie na 30 kl./s.
                n = round(sh["dur"] * FPS)
                vcmd += ["-ss", f"{e['v_in'] + sh['rel']:.4f}", "-t", f"{sh['dur'] + 0.25:.4f}", "-i", str(VIDEO)]
                w, h, x, y = crop(sh["frame"], e["face"])
                # zrodlo ma zakres tv (IMG_0526 mial pc), wiec bez przeliczania zakresu
                vf.append(f"[{n_in}:v:0]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range=tv:out_range=tv,"
                          f"{GRADE},fps={FPS},trim=end_frame={n},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{n_in}]")
                vl.append(f"[v{n_in}]")
                n_in += 1
        vf.append("".join(vl) + f"concat=n={len(vl)}:v=1:a=0[vc]")
        vtmp = Path(td) / "v.mp4"
        subprocess.run(vcmd + ["-filter_complex", ";".join(vf), "-map", "[vc]", "-c:v", "libx264", "-preset", "slow",
                               "-crf", "14", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                               "-color_primaries", "bt709", "-color_trc", "bt709", str(vtmp)], check=True)
        wav, st = build_audio(edl, td)
        mux(vtmp, wav, out)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                              "stream=nb_read_packets", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip())
    want = round(edl[-1]["t_out"] * FPS)
    # Mux bez -shortest, wiec klatek ma byc dokladnie tyle, ile wynika z EDL. (Z -shortest brakowalo 3 ostatnich
    # klatek pod plansza koncowa; ciecia i tak zgadzaly sie z EDL co do klatki - sprawdzone detekcja scen.)
    print(f"aroll: {out} ({edl[-1]['t_out']:.2f}s, {len(edl)} kwestii, {n_in} ujec) | loudnorm in {st['input_i']} LUFS"
          f" | klatki {got}/{want}" + ("" if want - 3 <= got <= want else "  <-- NIEZGODNE, sprawdz momenty ciec"))


if __name__ == "__main__":
    edl = make_edl()
    (OUT / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1))
    for e in edl:
        print(f"{e['i']:2d} {e['t_in']:6.2f}-{e['t_out']:6.2f}  audio {e['a_in']:7.2f}  wideo {e['v_in']:7.2f}  "
              f"{'/'.join(s['frame'] for s in e['shots'])}  {e['text'][:60]}")
    if "--edl-only" not in sys.argv:
        build(edl, audio_only="--audio-only" in sys.argv)

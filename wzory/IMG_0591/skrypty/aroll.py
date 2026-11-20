#!/usr/bin/env python3
"""A-roll rolki "Szczęście, plan czy głód" (IMG_0591): obraz i dzwiek z telefonu (przednia kamera, mikrofon krawatowy),
offset 0. Nagranie jest lustrzane (tytul ksiazki czyta sie wspak), wiec kazde ujecie przechodzi przez hflip.
Kadr jest niski (twarz w 40-72% wysokosci), dlatego kadry sa dosuniete do dolu, a napisy stoja nizej (kompozycja.py).

Uzycie: python3 -I aroll.py            -> ../aroll/aroll.mp4 + ../aroll/edl.json
        python3 -I aroll.py --edl-only -> tylko ../aroll/edl.json (bez renderu)
Wersja z hookiem B: ../hookB/skrypty/aroll.py (ten sam plik, HOOK = "B").
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
VIDEO = Path.home() / "Downloads/IMG_0591.MOV"
AUDIO = VIDEO  # dzwiek z tego samego pliku
HOOK = "A"
OUT = P / "aroll"
OUT.mkdir(exist_ok=True)
OFFSET = round(json.loads((P / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie i odbiciu: 2160x3840 (4K, 60 kl./s). Twarz ok. (950, 2150), broda na ok. 72% wysokosci.
# Kadry (w, h, x, y) dosuniete do dolnej krawedzi, zeby twarz stala jak najwyzej.
# Kadry dobiera `kadr()` z pomiaru twarzy (analiza/twarze.json, skrypty/twarze.py --flip), zeby broda konczyla sie przed
# napisami (strefa bezpieczna, Jakub 18.11.2026: napisy na 1150 px, a nie 1420). ZMIN to minimalny zoom rodzaju kadru;
# gdy Jakub pochyla sie do kamery (broda nawet na 73% wysokosci), zoom rosnie tak, zeby broda siegala najnizej CHIN_OUT px.
FRAMES = {"W": (2160, 3840, 0, 0), "M": (1928, 3428, 20, 412), "C": (1728, 3072, 86, 768)}  # rezerwa, gdy brak pomiaru
ZMIN = {"W": 1.15, "M": 1.25, "C": 1.35}
CHIN_OUT = 1200   # najnizszy punkt brody na wyjsciu (px z 1920); napisy zaczynaja sie na 1170, wiec przy pochyleniu do
                  # kamery zachodza na sam dol brody (przyciemnienie pod napisami robi je czytelnymi), ale twarz nie jest wielka
ZMAX = 1.6
_tw = P / "analiza/twarze.json"
FACES = {float(k): v for k, v in json.loads(_tw.read_text()).items()} if _tw.exists() else {}
_ostatni = {"zoom": None, "frame": None}


def kadr(frame, t0, t1):
    """Kadr (w, h, x, y) w px zrodla dla ujecia [t0, t1] (czas nagrania): najnizsza broda i zakres twarzy z pomiaru."""
    fs = [f for t, f in FACES.items() if t0 - 0.05 <= t <= t1 + 0.05]
    if not fs:
        return FRAMES[frame]
    chin = max(y + h * 1.05 for x, y, w, h in fs)                 # broda z zapasem na zarost
    cx = (min(x for x, y, w, h in fs) + max(x + w for x, y, w, h in fs)) / 2
    z = ZMIN[frame]
    zl = _ostatni["zoom"]
    zmiana = zl is not None and frame != _ostatni["frame"]        # po zmianie rodzaju kadru zoom ma sie wyraznie roznic
    if zmiana and abs(z - zl) < 0.07:
        z = zl + 0.10
    while True:
        h_ = 3840 / z
        y0 = min(max(chin - CHIN_OUT / 1920 * h_, 0), 3840 - h_)
        if (chin - y0) / h_ * 1920 <= CHIN_OUT + 8 or z >= ZMAX:
            break
        z += 0.02
    if zmiana and abs(z - zl) < 0.05:
        z = min(ZMAX, z + 0.08)
        h_ = 3840 / z
        y0 = min(max(chin - CHIN_OUT / 1920 * h_, 0), 3840 - h_)
    _ostatni["zoom"], _ostatni["frame"] = z, frame
    w_ = h_ * 9 / 16
    x0 = min(max(cx - w_ / 2, 0), 2160 - w_)
    return int(w_ // 2 * 2), int(h_ // 2 * 2), int(round(x0)), int(round(y0))


PRE, POST = 0.10, 0.15
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst[, wytnij]) - czasy w nagraniu. Ostatni pelny dubel kazdej kwestii.
# wytnij = [(od, do), ...]: kawalki usuwane ze SRODKA kwestii (zajakniecie, powtorzone slowo). Ciecie jest ciasne (bez PRE/POST,
# zanik 6 ms), "od" wyrownuje sie do klatki liczac od poczatku kawalka, "do" jest co do milisekundy. Skok obrazu chowa zmiana
# kadru ustawiona dokladnie na "do".
# Hook A = prowokacja o Europie, potem cytaty. Hook B = od razu cytaty (Buffett, Bezos, Gates), bez zdania o Europie.
HOOKS = {
    "A": [
        # "sukce- cesu": powtorzona sylaba w srodku slowa. Wyciete od konca pierwszego "c" do poczatku drugiego (14.26-14.40),
        # w miejscu ciecia zblizenie. Z kilku wariantow tylko ten whisper slyszy jako "sukcesu" w kazdym kontekscie.
        (9.99, 16.00, [(None, "W"), (14.40, "C")], "Według Petera Thiela Europa siedzi w najgorszej ćwiartce sukcesu, no i Ty w sumie razem z nią.",
         [(14.2567, 14.40)]),
        (48.21, 54.37, [(None, "M"), (51.15, "C")], "Warren Buffett uważa siebie za członka Klubu Szczęśliwej Spermy. Jeff Bezos przypisuje sukces Amazona niezwykłemu ustawieniu się planet."),
    ],
    "B": [
        (48.21, 54.37, [(None, "W"), (51.15, "M")], "Warren Buffett uważa siebie za członka Klubu Szczęśliwej Spermy. Jeff Bezos przypisuje sukces Amazona niezwykłemu ustawieniu się planet."),
        (54.73, 59.52, [(None, "C")], "A Bill Gates posuwa się tak daleko, że twierdzi, iż miał szczęście urodzić się z pewnymi umiejętnościami."),
    ],
}
BODY = [
    (63.56, 66.47, [(None, "W")], "Coś takiego możemy przeczytać w Zero to One od Petera Thiela,"),
    # zdanie pada dwa razy (82.57-84.69 urwane na "umiejetn...", potem cale od 85.06) - zostaje drugie podejscie
    (85.06, 87.44, [(None, "M")], "gdzie autor pyta: sukces to szczęście czy umiejętności?"),
    (118.84, 120.60, [(None, "C")], "Ale Thiel uważa skrajnie inaczej."),
    (121.28, 122.49, [(None, "W")], "Nie jesteś losem na loterii."),
    (129.06, 132.57, [(None, "M")], "Dwie osie. Masz plan albo nie. Wierzysz, że Ci się uda, albo nie."),
    (169.51, 172.72, [(None, "C")], "USA w latach 50. i 60.: totalny optymizm."),
    # po "w 61," pada urwane "a w 70..." (start ok. 206.60) - kwestia konczy sie w ciszy przed nim
    (197.52, 206.40, [(None, "W"), (202.30, "M")], "32 tysiące kilometrów gotowych dróg wybudowali w niespełna 9 lat, a jeśli chodzi o lot na Księżyc, to tak naprawdę zaplanowali go w 61,"),
    (209.42, 213.50, [(None, "C")], "a do końca '72 wylądowało na nim aż 12 osób."),
    (223.31, 228.31, [(None, "W")], "A co potem? Od lat 80. aż do dziś to jest totalny optymizm, ale kompletnie bez planu."),
    # Chiny: zdanie uciete po "niepewna," (dalej 4 s o minimalizowaniu ryzyka); po "pesymistów" nie ma pauzy do ciecia
    (245.45, 251.10, [(None, "M")], "Za to Chiny dzisiaj są w tej zdefiniowanej ćwiartce pesymistów, gdzie wiedzą, że przyszłość może być bardzo niepewna,"),
    (260.31, 264.55, [(None, "C")], "Europa, no… co ja mogę rzec? Ani planu, ani wiary. Klasycznie."),
    (274.66, 279.51, [(None, "W")], "Moim zdaniem nie ma kompletnie znaczenia, czy jesteś optymistą, czy pesymistą. Liczy się plan."),
    # po "połowa." (koniec 292.23) pada falstart "Drugą" (292.41-292.93) - wyciety
    (290.40, 292.22, [(None, "M")], "Ale plan to jedna połowa."),
    (296.44, 301.95, [(None, "C")], "Druga połowa, z którą ja się bardzo mocno utożsamiam, jest palące pragnienie, o którym zawsze pisał Napoleon Hill."),
    # 336.48 "Chcę wolność? Nie. Ja od zawsze, czyli ja" to falstart; kwestia startuje od "od praktycznie" (cisza 339.63-339.78)
    # "do... kładnie": pauza 0,15 s w srodku slowa (to NIE jest powtorzone "do": po pauzie pada samo "kładnie", dwie sylaby).
    # Wycieta sama pauza (0,09 s, zostaje zwarcie "k"); skok 2-3 klatek, wiec bez zmiany kadru.
    (339.80, 344.28, [(None, "W")], "Od praktycznie szesnastego, siedemnastego roku życia już wiedziałem dokładnie, czego chcę.",
     [(343.3333, 343.42)]),
    (344.99, 351.61, [(None, "M")], "Chcę wolność i chcę biznes online i przez ostatnie 7, 8, 9 lat cały czas do tego dążyłem."),
    # po "jestem." pada urwane "Także" (354.37-354.75) - wyciete
    (352.18, 354.18, [(None, "C")], "No i można powiedzieć, że jestem tu, gdzie jestem."),
    (368.02, 371.64, [(None, "W")], "A Ty co myślisz? Szczęście, plan czy palące pragnienie?"),
    (374.56, 375.72, [(None, "M")], "Daj znać koniecznie w komentarzu."),
]
SEGS = HOOKS[HOOK] + BODY

GRADE = "eq=contrast=1.08:saturation=1.04:gamma=0.96,vignette=angle=PI/5:mode=forward"
FPS = 30


def fr(t):
    return round(t * FPS) / FPS


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
    n_in = n_a = 0
    for e in edl:
        for c in e["clips"]:
            vcmd += ["-ss", f"{c['v_in']:.4f}", "-t", f"{c['dur']:.4f}", "-i", str(VIDEO)]
            w, h, x, y = kadr(c["frame"], c["v_in"], c["v_in"] + c["dur"])
            vf.append(f"[{n_in}:v:0]hflip,crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range=pc:out_range=tv,"
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

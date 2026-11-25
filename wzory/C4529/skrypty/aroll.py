#!/usr/bin/env python3
"""A-roll rolki "AI nie zabierze Ci klientow" (C4529, kamera Sony XAVC 4K 29,97 kl./s, nagrana pionowo; dzwiek z mikrofonu
podpietego do kamery, wiec offset 0). Szablon: IMG_0717 aroll_v3.py.

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
VIDEO = Path.home() / "Desktop/C4529.MP4"
AUDIO = VIDEO  # dzwiek z tego samego pliku
OUT = P / "aroll"
OUT.mkdir(exist_ok=True)
OFFSET = round(json.loads((P / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie: 2160x3840 (4K, 60 kl./s, zakres tv). Jakub siedzi blisko: glowa zajmuje ok. 32% wysokosci kadru
# (wlosy od 8%, broda na ok. 40%), wiec W to pelny kadr, a zblizenia sa lekkie (1,10 / 1,20) - mocniej nie zblizac.
# Kadr = (zoom, pozycja srodka twarzy w pionie jako ulamek wysokosci wyjscia). Srodek twarzy (px zrodla) podany osobno
# dla kazdej kwestii (a w dlugiej kwestii dla ujecia), bo miedzy dublami sie przesuwa (x od 755 do 1300).
SRC_W, SRC_H = 2160, 3840  # C4527: 3840x2160 z obrotem 90 st. w metadanych (kamera stala pionowo)
# C4527: Jakub siedzi blisko i wysoko w kadrze (wlosy od ok. 12%, broda na ok. 40% wysokosci), wiec W = pelny kadr,
# a zblizenia lekkie (1,12 / 1,25), jak przy selfie w pipeline.md.
# Kadr = (zoom, pozycja srodka twarzy w pionie jako ulamek wysokosci wyjscia). Srodek twarzy kazdego ujecia liczy sie
# z pomiaru (analiza/twarze.json, skrypty/twarze.py), a gdy pomiaru brak, z wartosci podanej w kwestii.
FRAMES = {
    "W": (1.00, 0.28),
    "M": (1.12, 0.30),
    "C": (1.25, 0.32),
}
_tw = P / "analiza/twarze.json"
FACES = {float(k): v for k, v in json.loads(_tw.read_text()).items()} if _tw.exists() else {}


def twarz_ujecia(t0, t1, domyslna):
    fs = [f for t, f in FACES.items() if t0 - 0.05 <= t <= t1 + 0.05]
    if not fs:
        return domyslna
    xs = sorted(x + w / 2 for x, y, w, h in fs)
    ys = sorted(y + h / 2 for x, y, w, h in fs)
    return xs[len(xs) // 2], ys[len(ys) // 2]


PRE, POST = 0.10, 0.22
# Ciasniejsze styki (Jakub, 24.11.2026: "czasami wkradaja sie krotkie przerwy pomiedzy jednym a drugim elementem...
# chcialbym, zeby byly minimalnie krotsze, zeby flow bylo plynniejsze"). Koniec kwestii liczony od faktycznego wygasniecia
# glosu (prog -52 dB, koncowki slow zostaja), a nie od konca wyspy z silencedetect (-42 dB). Po nim ogon: 0,12 s
# w srodku zdania (przecinek, brak kropki), 0,22 s po zdaniu (.?!). Na styku wychodzi ok. 0,25 s ciszy w srodku zdania
# i ok. 0,35 s miedzy zdaniami zamiast srednio 0,53 s. Puenta z celowa pauza: opcja kwestii {"post": ...}.
POST_SRODEK, POST_ZDANIE = 0.12, 0.22
_WAV16 = P / "audio/nowe_16k.wav"


def _db(t0, t1, hop=0.01, win=0.02):
    import array, math, wave
    with wave.open(str(_WAV16)) as w:
        sr = w.getframerate()
        w.setpos(max(0, int(t0 * sr)))
        x = array.array("h", w.readframes(int((t1 - t0 + win) * sr)))
    step, L, out, k = int(hop * sr), int(win * sr), [], 0
    while k + L <= len(x):
        rms = math.sqrt(sum(v * v for v in x[k:k + L]) / L) / 32768
        out.append((t0 + k / sr, 20 * math.log10(rms + 1e-9)))
        k += step
    return out


def poczatek_mowy(s, prog=-45.0, szukaj=0.5):
    """Faktyczny poczatek glosu od s: wyspy z silencedetect zaczynaja sie nawet 0,2 s przed pierwsza gloska
    (C4528: wyspa 47.27, glos 47.48), co dokladalo ciszy na styku. Pierwsze miejsce powyzej progu."""
    for t, d in _db(s - 0.06, s + szukaj):
        if d > prog:
            return max(s - 0.06, t - 0.02)
    return s


def koniec_mowy(e, prog=-52.0, szukaj=0.45):
    """Faktyczny koniec glosu po e: pierwsze miejsce, od ktorego przez 30 ms jest ponizej progu."""
    env = _db(e - 0.08, e + szukaj)
    for i in range(len(env) - 2):
        if env[i][0] >= e - 0.05 and all(env[j][1] < prog for j in range(i, i + 3)):
            return env[i][0]
    return e + 0.12
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa
# Wyrownanie glosnosci miedzy kwestiami (skrypty/poziomy.py -> analiza/poziomy.json): 80% roznicy do mediany,
# max +-4 dB. Brak pliku = bez korekty.
_lv = P / "analiza/poziomy.json"
GAIN = json.loads(_lv.read_text())["gain_db"] if _lv.exists() else {}

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr), ...], tekst, (x, y) srodka twarzy[, opcje]) - czasy w nagraniu.
# C4529 (24.11.2026), scenariusz 3 ("AI nie zabierze Ci klientow"). Ostatni pelny dubel. Pominiete: "To jest huk pierwszy,
# teraz huk drugi, klient wybral nie Ciebie, bo tamten opis" (7.0), "Dobra, teraz body..." (26.5), "Pierwsza..." (38.1),
# falstart "Pierwszy odpisuje pod..." (42.4 -> 43.92), "Wycena, termin, trzy pytania, czekaj" (61.5), "A napisal to AI..." (76.8, 81.6), "Kogo wybiera klient?" (91.0),
# "Dobra. Dzieki bardzo." (113.4).
HOOK = "B" if (P / "HOOK_B").exists() else "A"
F0 = (920, 1010)  # srodek twarzy (px zrodla), gdy brak pomiaru
HOOKI = {
    "A": (1.65, 5.89, [(None, "W")], "AI nie zabierze Ci klientów. Zabierze ich freelancer, który dobrze go używa.", F0),
    "B": (20.66, 24.88, [(None, "W")], "Klient nie wybrał Ciebie, tylko konkurencję, z tego względu, że ona po prostu odpisała w 3 minuty.", F0),
}
SEGS = [
    HOOKI[HOOK],
    (33.31, 35.33, [(None, "M")], "Ten sam brief od klienta, ale dwie odpowiedzi.", F0),  # 32.5 "Ten sam..." = falstart
    (43.92, 47.58, [(None, "W")], "Pierwszy odpisuje po 2 dniach: „Dzień dobry, w załączniku znajdziesz ofertę”.", F0),
    (52.99, 54.40, [(None, "C")], "Druga firma po 3 minutach.", F0, {"pre": 0.06}),  # 52.2 "Druga" = falstart
    (65.81, 67.88, [(None, "M")], "Wycena, termin, 3 pytania o projekt", F0),
    (70.35, 73.25, [(None, "W")], "i przykład podobnej realizacji. Wszystko z Twojej bazy danych.", F0),
    (85.00, 88.61, [(None, "C")], "A napisał i wysłał to jeden z agentów AI, dosłownie w 2 minuty.", F0),
    (96.56, 99.25, [(None, "M")], "Kogo wybiera klient? Oczywiste.", F0),  # pauza 0,8 s przed "Oczywiste" zostaje (napiecie)
    (105.69, 107.86, [(None, "W")], "A którym Ty jesteś? Daj znać w komentarzu.", F0, {"pre": 0.04}),  # 105.3 "Ktory..." = falstart
    (109.93, 112.33, [(None, "M")], "No i zaobserwuj, jeśli chcesz być tym drugim.", F0),
]
N_HOOK = 1  # ile pierwszych kwestii to hook


def crop(frame, face):
    """Kadr (w, h, x, y) w px zrodla: zoom i pozycja twarzy z FRAMES, srodek twarzy z kwestii."""
    z, fy = FRAMES[frame]
    w = int(min(SRC_W, SRC_H * 9 / 16) / z / 2) * 2  # zrodlo szersze niz 9:16 (IMG_0717): kadr ograniczony wysokoscia
    h = int(round(w * 16 / 9 / 2)) * 2
    x = min(max(0, int(round(face[0] - w / 2))), SRC_W - w)
    y = min(max(0, int(round(face[1] - fy * h))), SRC_H - h)
    return w, h, x, y


GRADE = "eq=contrast=1.04:saturation=1.02:gamma=1.00,vignette=angle=PI/7:mode=forward"  # do korekty po pomiarze YAVG
FPS = 30


def fr(t):
    return round(t * FPS) / FPS


def src_range():
    """Zakres kolorow zrodla: "pc" (pelny, np. iPhone 1080p yuvj420p) albo "tv" (ograniczony, np. iPhone 4K HEVC)."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_range",
                        "-of", "csv=p=0", str(VIDEO)], capture_output=True, text=True).stdout.strip().strip(",")
    return "pc" if r in ("pc", "jpeg") else "tv"


def make_edl():
    edl, t = [], 0.0
    for i, seg in enumerate(SEGS):
        if seg[0] == "HOLD":
            # Pauza bez slow: kawalek obrazu [v0, v1] w zwolnieniu `speed`, potem zatrzymana ostatnia klatka przez
            # `freeze` sekund. Dzwiek w tym miejscu to cisza (kompozycja dodaje pod nia cichy narastajacy szum).
            _, v0, v1, speed, freeze, frame, face = seg
            dur = fr((v1 - v0) / speed + freeze)
            edl.append({"i": i, "hold": True, "a_in": round(v0, 4), "a_out": round(v0 + dur, 4), "v_in": round(v0 - OFFSET, 4),
                        "t_in": round(t, 4), "t_out": round(t + dur, 4), "speech": [v0, v0], "text": "", "face": list(face),
                        "hook": False, "gain_db": 0.0,
                        "shots": [{"frame": frame, "rel": 0.0, "t_in": round(t, 4), "dur": round(dur, 4), "face": list(face),
                                   "speed": speed, "src": round(v1 - v0, 4)}]})
            t += dur
            continue
        s, e, shots, text, face = seg[:5]
        opts = seg[5] if len(seg) > 5 else {}
        a_in = poczatek_mowy(s) - min(opts.get("pre", PRE), PRE)
        if "post" in opts:
            a_out = e + opts["post"]
        else:
            a_out = koniec_mowy(e) + (POST_ZDANIE if text.rstrip()[-1:] in ".?!" else POST_SRODEK)
        a_out += END_HOLD if i == len(SEGS) - 1 else 0.0
        dur = fr(a_out - a_in)
        sh = []
        for k, shot in enumerate(shots):
            frm, frame = shot[0], shot[1]
            rel = 0.0 if frm is None else fr(frm - a_in)
            sh.append({"frame": frame, "rel": rel, "t_in": round(t + rel, 4),
                       "face": list(shot[2] if len(shot) > 2 else face)})
        for k in range(len(sh)):
            sh[k]["dur"] = round((sh[k + 1]["rel"] if k + 1 < len(sh) else dur) - sh[k]["rel"], 4)
        edl.append({"i": i, "a_in": round(a_in, 4), "a_out": round(a_in + dur, 4),
                    "v_in": round(a_in - OFFSET, 4), "t_in": round(t, 4), "t_out": round(t + dur, 4),
                    "speech": [s, e], "shots": sh, "text": text, "face": list(face), "hook": i < N_HOOK,
                    "gain_db": GAIN.get(f"{s:.2f}-{e:.2f}", 0.0),
                    "mute_after": round(opts["cisza_od"] - a_in, 4) if "cisza_od" in opts else None})
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
        st_out, d_out = max(0.0, dur - 0.04), 0.04
        if e is edl[-1]:
            # Ogon pod plansza koncowa: po ostatnim slowie slychac szmery (siegniecie po telefon, do -22 dB), ktore po
            # normalizacji wychodza pod plansza. Wyciszenie 0,1 s po koncu mowy, potem cisza.
            st_out, d_out = e["speech"][1] - e["a_in"] + 0.10, 0.20
        if e.get("mute_after") is not None:  # dzwiek konczy sie wczesniej niz obraz (cisza do konca kwestii)
            st_out, d_out = e["mute_after"] - 0.04, 0.04
        glosnosc = "volume=0" if e.get("hold") else f"volume={e.get('gain_db', 0.0):.2f}dB"
        af.append(f"[{k}:a:0]aresample=48000,atrim=0:{dur:.4f},asetpts=PTS-STARTPTS,{glosnosc},"
                  f"afade=t=in:d=0.02,afade=t=out:st={st_out:.4f}:d={d_out:.2f}[a{k}]")
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
        rng = src_range()
        for e in edl:
            for sh in e["shots"]:
                # Ujecie ciete co do klatki (zrodlo ma 60 kl./s): czytamy z zapasem i bierzemy dokladnie n klatek
                # po zmianie na 30 kl./s.
                n = round(sh["dur"] * FPS)
                vcmd += ["-ss", f"{e['v_in'] + sh['rel']:.4f}", "-t", f"{sh.get('src', sh['dur']) + 0.25:.4f}", "-i", str(VIDEO)]
                w, h, x, y = crop(sh["frame"], twarz_ujecia(e["v_in"] + sh["rel"], e["v_in"] + sh["rel"] + sh.get("src", sh["dur"]), sh["face"]))
                # pauza: `src` sekund nagrania w zwolnieniu (60 kl./s -> przy 50% kazda klatka jest prawdziwa), potem
                # ostatnia klatka powielona do konca ujecia
                tempo = (f"trim=duration={sh['src']:.4f},setpts=(PTS-STARTPTS)/{sh['speed']},fps={FPS},"
                         f"tpad=stop_mode=clone:stop_duration=3," if sh.get("speed") else f"fps={FPS},tpad=stop_mode=clone:stop_duration=3,")
                # tpad: ostatnie ujecie z przytrzymaniem pod plansze koncowa moze siegac za koniec zrodla (IMG_0720: 1,8 s)
                vf.append(f"[{n_in}:v:0]crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos:in_range={rng}:out_range=tv,"
                          f"{GRADE},{tempo}trim=end_frame={n},format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v{n_in}]")
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
              f"{'/'.join(s['frame'] for s in e['shots'])}  {e['text'][:60] or '(pauza: zwolnienie i zatrzymana klatka)'}")
    if "--edl-only" not in sys.argv:
        build(edl, audio_only="--audio-only" in sys.argv)

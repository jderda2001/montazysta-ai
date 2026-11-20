#!/usr/bin/env python3
"""A-roll rolki PerfOS "Dałem AI 1000 zł na reklamy książek po 175 zł" (IMG_0597): obraz i dzwiek z telefonu
(tylna kamera, mikrofon krawatowy podpiety do iPhone'a, brak osobnego nagrania), wiec offset 0.
Ciecie dubli, kadry 9:16 ze zrodla 4K, grading, wyrownanie glosnosci kwestii, lekki mastering dzwieku.

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
VIDEO = Path.home() / "Downloads/IMG_0597.MOV"
AUDIO = VIDEO  # dzwiek z tego samego pliku
OUT = P / "aroll"
OUT.mkdir(exist_ok=True)
OFFSET = round(json.loads((P / "analiza/sync.json").read_text())["offset"], 4)  # czas_audio = czas_wideo + OFFSET

# Zrodlo po obrocie: 2160x3840 (4K, 60 kl./s, zakres tv). Jakub siedzi blisko: glowa zajmuje ok. 32% wysokosci kadru
# (wlosy od 8%, broda na ok. 40%), wiec W to pelny kadr, a zblizenia sa lekkie (1,10 / 1,20) - mocniej nie zblizac.
# Kadr = (zoom, pozycja srodka twarzy w pionie jako ulamek wysokosci wyjscia). Srodek twarzy (px zrodla) podany osobno
# dla kazdej kwestii (a w dlugiej kwestii dla ujecia), bo miedzy dublami sie przesuwa (x od 755 do 1300).
SRC_W, SRC_H = 2160, 3840
FRAMES = {
    "W": (1.00, 0.32),
    "M": (1.10, 0.33),
    "C": (1.20, 0.335),
}
# Marginesy ciec. Jakub po pierwszej wersji (18.11.2026): "w niektorych miejscach troszeczke za szybko przyciales".
# Pomiar: przy 0,10 / 0,15 naturalne pauzy 0,4-0,7 s miedzy zdaniami kurczyly sie do 0,25 s, a ciche koncowki slow
# (-45...-55 dB, ponizej progu detekcji kawalkow) wpadaly w wyciszenie. Teraz po zdaniu zostaje 0,22 s, przed 0,14 s
# (razem 0,36 s), sasiednie kwestie z naturalna pauza sa scalone, a ciecia w srodku zdania maja wlasne, ciasne wartosci
# (slownik {"pre": ..., "post": ...} na koncu kwestii).
PRE, POST = 0.14, 0.22
END_HOLD = 2.5  # przytrzymanie po ostatnim slowie pod plansze koncowa
# Wyrownanie glosnosci miedzy kwestiami (skrypty/poziomy.py -> analiza/poziomy.json): 80% roznicy do mediany,
# max +-4 dB. Brak pliku = bez korekty.
_lv = P / "analiza/poziomy.json"
GAIN = json.loads(_lv.read_text())["gain_db"] if _lv.exists() else {}
# "z wydawnictwa mojego dziadka" jest powiedziane polglosem (-35 dB, 10,6 dB ponizej mediany): reczne +7 dB zamiast limitu +4.
GAIN.update({"37.96-39.11": 7.0} if GAIN else {})

# Kwestie: (start_mowy, koniec_mowy, [(od, kadr[, (x, y)]), ...], tekst, (x, y) srodka twarzy) - czasy w nagraniu.
# Zasada: ostatni pelny dubel kazdej kwestii. Kolejne pozycje listy kadrow = zmiana kadru w trakcie kwestii (w pauzie).
# Falstarty i ciecia (sondy whisperem bez promptu, kawalek po kawalku):
#   hook:   16.29 "Dałem AI tysiąc złotych" (uzyty jako poczatek hooka), 18.68 "Dałem AI ponad tysiąc złotych na
#           reklamowanie" (porzucony), 21.53 "Dałem..." (falstart), 22.90 ostatni dubel (uzyty od "na reklamowanie")
#   49.12 "Każdy marketer powiedziałby..." poprawione przez niego na "Pewnie marketer..." (56.67 falstart) -> 59.79
#   71.17 "Zasada była jedna." -> 73.72;  96.85 "No i..." -> 97.78;  100.37-108.91 porzucony dubel (27 pazdziernika)
#   116.94: z kwestii wyciety wtret "gdzie na dziś dzień mamy 17 listopada" (119.90-123.60) - daty sa na planszy.
#           "listopada" konczy sie dopiero o 123.50 (glosne "-pada" 123.23-123.47), "PerfOS" startuje o 123.67
#   142.61 "Do koszyka ludzi wsadziło 32." -> poprawione dublem 149.07 "32 ludzie wsadzili" (pauza 0.8 s skrocona)
#   166.60 "dwie, trzy książki" (powtorzenie konca zdania) - wyciete
#   watek piksela: zostaje do "o ponad 1700 zł" (198.42); "złotych" po 4220 konczy sie o 174.98. Wypada powtorzenie 198.69-202.27 ("także ten ROAS też jest
#   zaniżony, także ten średni zakup też jest zaniżony")
#   205.43 "No ciekawy projekt." -> 206.72;  219.12 "Jeśli" -> 225.29
SEGS = [
    # Hook zlozony z dwoch dubli: w ostatnim (22.90) "AI" jest polkniete (0,14 s, whisper bez podpowiedzi slyszy
    # "Dałem jej"), wiec pierwsze slowa ida z dubla 1, gdzie "Dałem AI tysiąc złotych" jest wyrazne, a reszta zdania
    # z ostatniego dubla od zwarcia przed "na" (23.82). Ciecie w srodku zdania, wiec ciasno.
    (16.29, 17.85, [(None, "W")], "Dałem AI tysiąc złotych", (1020, 1220), {"post": 0.13}),
    (23.92, 26.09, [(None, "M")], "na reklamowanie książek po 175 zł.", (1020, 1220), {"pre": 0.10}),
    (29.81, 33.40, [(None, "C")], "I to nie byle jakich. To były albumy o architekturze Bielska-Białej", (970, 1180), {"post": 0.16}),
    # po "dziadka." jest mlasniecie (39.28), wiec koniec zostaje ciasny, a oddech idzie przed nastepna kwestie
    (37.96, 39.11, [(None, "M")], "z wydawnictwa mojego dziadka.", (1290, 1220), {"pre": 0.12, "post": 0.15}),
    (44.78, 46.62, [(None, "W")], "Drogie, niszowe, lokalne.", (1265, 1110), {"pre": 0.20}),
    (59.79, 62.94, [(None, "M")], "Pewnie marketer powiedziałby: odpuść, przez Metę to bez szans.", (1085, 1110)),
    (73.72, 80.85, [(None, "C"), (77.56, "W")],
     "Zasada była jedna: nic nie ruszamy. Podpinamy i lecimy. Patrzymy tylko i wyłącznie na wyniki. "
     "O ile w ogóle jakiekolwiek z tego będą.", (950, 1110)),
    (85.70, 91.40, [(None, "M")],
     "PerfOS sam zrobił reklamy, sam je wypuścił, sam je optymalizował i sam wyłączył zestawy, które nie działały.", (1080, 1110)),
    # "No i wynik." + pauza z najazdem na twarz (Jakub: "powinno byc bardziej zbudowane napiecie, troszke przedluzone,
    # przyblizenie na moja twarz"). Po slowie patrzy w kamere tylko do 98.45, potem mruga i schyla sie do laptopa,
    # wiec pauza to 0,12 s nagrania w zwolnieniu 50% i zatrzymana klatka z 98.43 (oczy w kamerze), razem ok. 1,1 s.
    # Przed "No" jest tylko 0,15 s ciszy po falstarcie (koniec 97.63).
    (97.78, 98.27, [(None, "C")], "No i wynik.", (1185, 1000), {"pre": 0.12, "post": 0.04}),
    ("HOLD", 98.31, 98.43, 0.5, 0.86, "C", (1185, 1000)),
    # "dziś" konczy sie o 119.83 (sybilant 119.75-119.83, widmo powyzej 3 kHz). Dalej do 120.07 idzie juz dzwieczna
    # zapowiedz nastepnego slowa ("gdzie"), ktora whisper w gotowym pliku slyszal jako "Gli-": dzwiek jest wyciszany
    # od 119.86, obraz trwa do konca kwestii (5 klatek, potem zmiana kadru).
    (116.94, 119.89, [(None, "W")], "Przez ten okres od 20 października do dziś", (950, 1035), {"post": 0.15, "cisza_od": 119.86}),
    # dwa zdania z naturalna pauza 0,43 s (129.41-129.84) - jedna kwestia, zmiana kadru w pauzie
    (123.69, 134.41, [(None, "M"), (129.62, "C", (1030, 1075))],
     "PerfOS zrobił 16 zestawów reklamowych, co przekłada się na okolice 40 grafik. Z czego trzy zestawy reklamowe "
     "wyłączył, czyli okolice niecałych 10 grafik.", (1300, 1150), {"pre": 0.10}),
    (135.12, 142.21, [(None, "W")], "Idąc dalej, wygenerował 571 wejść na stronę, obejrzanych produktów było 484.", (1015, 1220)),
    # w nagraniu po "wsadzili" jest 0,5 s pauzy; zostaje 0,45 s (bylo sciete do 0,25 s)
    (149.07, 150.92, [(None, "M")], "32 ludzie wsadzili", (1110, 1075), {"post": 0.25}),
    # "…został zrealizowany, co przełożyło się…" to ciagla wypowiedz (pauza 0,25 s) - jedna kwestia
    (151.71, 166.17, [(None, "C"), (159.02, "W", (1300, 1180)), (162.22, "M", (1300, 1180))],
     "produkt do koszyka, kasa 16 i zakup, uwaga, 11 razy został zrealizowany, co przełożyło się na średni koszyk "
     "384 zł, bo podpowiem, książek było trzy rodzaje na stronie, niektórzy kupowali sobie po dwie, trzy.", (1020, 1110), {"pre": 0.20}),
    # ROAS i watek piksela to jedna ciagla wypowiedz (przerwa 0,14 s przed "I jestem"), wiec jedna kwestia;
    # zmiany kadru w pauzach. Watek piksela w calosci, bo Jakub doslal zrzut z Shopify.
    (168.22, 198.42, [(None, "C"), (175.07, "W", (875, 1365)), (178.72, "M", (875, 1365)), (184.75, "C", (930, 1300)),
                      (190.04, "W"), (193.31, "M", (970, 1255))],
     "ROAS wykręciliśmy na tym projekcie 3,38, a przychód z tych reklam to było 4220 zł. I jestem w 100% pewny, "
     "co mam poparte danymi, że to źle się niestety zliczało ze względu na piksela na Facebooku, który był po prostu "
     "źle skonfigurowany, bo na Shopify pokazuje nam total sales 8251 zł, oprócz PerfOSa był tylko jeszcze jeden "
     "kanał, który wiemy, ile wygenerował, także możemy sobie wyestymować, że tutaj zaniżyło ten przychód "
     "o ponad 1700 zł.", (1035, 1220), {"post": 0.20}),
    (203.76, 204.56, [(None, "W")], "Podsumowując,", (880, 1220), {"post": 0.18}),
    (206.72, 218.43, [(None, "M"), (210.14, "C", (1145, 1180)), (216.63, "W")],
     "ciekawy projekt, byliśmy ciekawi, jak to wyjdzie. No i wyszło. Także jeśli PerfOS poradził sobie z książką "
     "o Bielsku i o architekturze za 175 zł, to myślę, że z Twoim sklepem też sobie da radę.", (755, 1290), {"pre": 0.12, "post": 0.25}),
    (225.29, 228.05, [(None, "M")], "Napisz w komentarzu PERFOS, pokażę Ci, jak to ustawić.", (1130, 1180), {"pre": 0.16}),
]
N_HOOK = 2  # ile pierwszych kwestii to hook


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
        a_in = s - opts.get("pre", PRE)
        a_out = e + opts.get("post", POST) + (END_HOLD if i == len(SEGS) - 1 else 0.0)
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
                w, h, x, y = crop(sh["frame"], sh["face"])
                # pauza: `src` sekund nagrania w zwolnieniu (60 kl./s -> przy 50% kazda klatka jest prawdziwa), potem
                # ostatnia klatka powielona do konca ujecia
                tempo = (f"trim=duration={sh['src']:.4f},setpts=(PTS-STARTPTS)/{sh['speed']},fps={FPS},"
                         f"tpad=stop_mode=clone:stop_duration=3," if sh.get("speed") else f"fps={FPS},")
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

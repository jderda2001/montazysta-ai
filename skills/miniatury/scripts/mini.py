#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Narzędzia do miniatur: skan klatek, ranking, dopracowanie klatki, wycinanie, render, kontrola, eksport.

Tylko biblioteka standardowa. Z zewnątrz potrzebne są: ffmpeg/ffprobe, swiftc (Apple Vision przez
wizja.swift, kompilowane przy pierwszym użyciu do ~/.cache/miniatury) i Chrome z HyperFrames.
Twarz jest analizowana wyłącznie na tym Macu.

  python3 mini.py skanuj   WIDEO --wyj KATALOG [--edl aroll/edl.json] [--momenty momenty.json]
  python3 mini.py ranking  KATALOG [--edl …] [--momenty …]          (ponownie, bez skanowania)
  python3 mini.py dopracuj WIDEO --t 17:10.4 --wyj KATALOG/A [--okno 0.4] [--klatka K]
  python3 mini.py wytnij   KATALOG/A/klatka.png
  python3 mini.py render   PLIK.html [--wyj PLIK.png]               (PNG i JPG 3840×2160)
  python3 mini.py kontrola A.jpg B.jpg C.jpg [--tytul "…"]
  python3 mini.py eksport  --tytul "…" --folder "…/Eksporty/YouTube/RRRR-MM-DD Tytuł" A.jpg B.jpg C.jpg
"""
import argparse
import bisect
import datetime
import glob
import html
import json
import os
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

SKRYPTY = Path(__file__).resolve().parent
SKILL = SKRYPTY.parent
CACHE = Path.home() / ".cache" / "miniatury"
CZCIONKA = SKILL / "assets" / "InterTight.ttf"

KATEGORIE = {
    "usmiech": "uśmiech",
    "akcent": "akcent (otwarte usta, uniesione brwi)",
    "spokoj": "spokój (zamknięte usta, pewna mina)",
    "gest": "gest (dłonie w kadrze)",
    "najlepsze": "najlepszy wygląd ogółem",
}


# ------------------------------------------------------------------ pomocnicze

def blad(msg):
    sys.exit("BŁĄD: " + msg)


def uruchom(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        blad("%s\n%s" % (" ".join(str(c) for c in cmd[:6]) + " …", (r.stderr or r.stdout)[-1500:]))
    return r.stdout


def wizja_bin():
    """Kompiluje wizja.swift, gdy brak pliku wykonywalnego albo źródło jest nowsze."""
    src = SKRYPTY / "wizja.swift"
    out = CACHE / "wizja"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        CACHE.mkdir(parents=True, exist_ok=True)
        print("Kompiluję wizja.swift (jednorazowo, kilka sekund)…", file=sys.stderr)
        r = subprocess.run(["swiftc", "-Ounchecked", "-o", str(out), str(src)], capture_output=True, text=True)
        if r.returncode != 0:
            blad("kompilacja wizja.swift nie powiodła się:\n" + r.stderr[-2000:])
    return str(out)


def wizja(*args):
    return uruchom([wizja_bin()] + [str(a) for a in args])


def chrome_bin():
    kand = sorted(glob.glob(str(Path.home() / ".cache/hyperframes/chrome/chrome-headless-shell/*/*/chrome-headless-shell")))
    if kand:
        return kand[-1]
    for p in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.path.exists(p):
            return p
    blad("nie znalazłem Chrome (ani w ~/.cache/hyperframes, ani w /Applications)")


def info_wideo(p):
    out = uruchom(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                   "stream=width,height,avg_frame_rate,color_transfer,color_space,color_range:format=duration",
                   "-of", "json", str(p)])
    d = json.loads(out)
    s = d["streams"][0]
    a, b = s.get("avg_frame_rate", "30/1").split("/")
    return {
        "w": s["width"], "h": s["height"], "fps": float(a) / float(b or 1),
        "dlugosc": float(d["format"]["duration"]),
        "hdr": s.get("color_transfer") in ("arib-std-b67", "smpte2084"),
        "color_transfer": s.get("color_transfer"),
    }


def czas(t):
    if t is None:
        return "–"
    m = int(t // 60)
    return "%d:%04.1f" % (m, t - 60 * m)


def sekundy(s):
    """Czas z wiersza poleceń: sekundy (1030.4) albo minuty:sekundy tak jak na arkuszach (17:10.4)."""
    try:
        w = 0.0
        for cz in str(s).strip().replace(",", ".").split(":"):
            w = w * 60 + float(cz)
        return w
    except ValueError:
        raise argparse.ArgumentTypeError("czas ma mieć postać 1030.4 albo 17:10.4, a jest „%s”" % s)


def render_html(sciezka_html, sciezka_png, szer=1920, wys=1080, skala=2, budzet_ms=4000):
    """Zrzut strony przez Chrome bez okna. skala=2 daje nadpróbkowanie (ostrzejsze krawędzie po pomniejszeniu)."""
    sciezka_png = Path(sciezka_png)
    if sciezka_png.exists():
        sciezka_png.unlink()
    binarka = chrome_bin()
    cmd = [binarka, "--headless", "--hide-scrollbars", "--allow-file-access-from-files", "--disable-gpu",
           "--force-device-scale-factor=%g" % skala, "--window-size=%d,%d" % (szer, wys),
           "--default-background-color=00000000", "--virtual-time-budget=%d" % budzet_ms,
           "--screenshot=%s" % sciezka_png, Path(sciezka_html).resolve().as_uri()]
    if "headless-shell" not in binarka:
        cmd[1] = "--headless=new"
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not sciezka_png.exists():
        blad("Chrome nie zapisał zrzutu:\n" + r.stderr[-1500:])
    return sciezka_png


def do_jpg(png, jpg, szer=None, max_bajty=1_900_000):
    args = ["jpg", png, jpg, "--max-bajty", max_bajty]
    if szer:
        args += ["--szer", szer]
    return json.loads(wizja(*args).strip().splitlines()[-1])


# ------------------------------------------------------------------ oś czasu

def wczytaj_edl(sciezka):
    """Lista cięć ze skilla montażu: każdy wpis ma v_in (czas w źródle), t_in i t_out (czas w filmie)."""
    if not sciezka:
        return []
    seg = []
    for e in json.loads(Path(sciezka).read_text(encoding="utf-8")):
        if all(k in e for k in ("v_in", "t_in", "t_out")):
            seg.append((float(e["v_in"]), float(e["v_in"]) + float(e["t_out"]) - float(e["t_in"]), float(e["t_in"])))
    return sorted(seg)


def zrodlo_na_film(t, edl):
    for v0, v1, t0 in edl:
        if v0 <= t < v1:
            return t0 + (t - v0)
    return None


def film_na_zrodlo(t, edl):
    for v0, v1, t0 in edl:
        if t0 <= t < t0 + (v1 - v0):
            return v0 + (t - t0)
    return None


def wczytaj_momenty(sciezka, edl):
    """momenty.json: [{"nazwa": "hook", "od": 0.0, "do": 6.3, "os": "film"}]. Oś "film" wymaga --edl."""
    if not sciezka:
        return []
    wynik = []
    for m in json.loads(Path(sciezka).read_text(encoding="utf-8")):
        os_ = m.get("os", "film" if edl else "zrodlo")
        if os_ == "film" and not edl:
            blad("momenty na osi filmu wymagają --edl (albo podaj \"os\": \"zrodlo\")")
        wynik.append({"nazwa": m["nazwa"], "od": float(m["od"]), "do": float(m["do"]), "os": os_})
    return wynik


# ------------------------------------------------------------------ arkusze poglądowe

def arkusz(sciezka_jpg, tytul, komorki, kolumny=6, kom_w=310, kadr_h=330, szeroki=False):
    """Arkusz z przyciętymi twarzami. komorki: [{src, w, h, twarz{x,y,w,h}, gora, dol, sekcja?}]

    szeroki=True pokazuje prawie cały kadr (5,5 szerokości twarzy), żeby było widać dłonie."""
    czesci = []
    sekcja = None
    for k in komorki:
        if k.get("sekcja") != sekcja:
            sekcja = k.get("sekcja")
            czesci.append('<div class="sek">%s</div>' % html.escape(sekcja or ""))
        t = k["twarz"]
        # Kadr: głowa z ramionami (3,3 szerokości twarzy), twarz w górnej połowie.
        cw = (5.5 if szeroki else 3.3) * t["w"]
        x0 = t["x"] + t["w"] / 2 - cw / 2
        y0 = t["y"] - (0.8 if szeroki else 0.85) * t["h"]
        sk = kom_w / cw
        styl = "background-image:url('%s');background-size:%.1fpx %.1fpx;background-position:%.1fpx %.1fpx" % (
            Path(k["src"]).resolve().as_uri(), k["w"] * sk, k["h"] * sk, -x0 * sk, -y0 * sk)
        czesci.append('<div class="k"><div class="o" style="%s"></div><div class="g">%s</div><div class="d">%s</div></div>'
                      % (styl, html.escape(k.get("gora", "")), html.escape(k.get("dol", ""))))
    szer = kolumny * (kom_w + 10) + 30
    strona = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'IT';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0}
body{width:%dpx;background:#16171a;color:#fff;font-family:'IT',-apple-system,sans-serif;padding:14px 15px 18px}
h1{font-size:24px;font-weight:800;margin:0 0 10px 4px}
.w{display:flex;flex-wrap:wrap;gap:10px}
.sek{flex:0 0 100%%;font-size:20px;font-weight:800;color:#00E5A0;margin:8px 0 -2px 4px}
.sek:empty{display:none}
.k{width:%dpx;background:#0f1012;border-radius:10px;overflow:hidden}
.o{width:%dpx;height:%dpx;background-color:#000;background-repeat:no-repeat}
.g{font-size:21px;font-weight:800;padding:6px 8px 0}
.d{font-size:15px;font-weight:500;color:#c9ccd3;padding:1px 8px 7px;white-space:nowrap;overflow:hidden}
</style></head><body><h1>%s</h1><div class="w">%s</div></body></html>""" % (
        CZCIONKA.resolve().as_uri(), szer, kom_w, kom_w, kadr_h, html.escape(tytul), "".join(czesci))
    sciezka_jpg = Path(sciezka_jpg)
    tmp_html = sciezka_jpg.with_suffix(".html")
    tmp_png = sciezka_jpg.with_suffix(".png")
    tmp_html.write_text(strona, encoding="utf-8")
    # Wysokość liczymy z góry: każda sekcja zaczyna nowy wiersz.
    licznik = {}
    for k in komorki:
        licznik[k.get("sekcja")] = licznik.get(k.get("sekcja"), 0) + 1
    wiersze = sum((n + kolumny - 1) // kolumny for n in licznik.values())
    sekcje = len([s for s in licznik if s])
    wys = 66 + wiersze * (kadr_h + 74) + sekcje * 40
    render_html(tmp_html, tmp_png, szer=szer, wys=wys, skala=1)
    do_jpg(tmp_png, sciezka_jpg, max_bajty=3_500_000)
    tmp_png.unlink()
    tmp_html.unlink()
    return sciezka_jpg


# ------------------------------------------------------------------ skanuj / ranking

def cmd_skanuj(a):
    wyj = Path(a.wyj)
    skan = wyj / "skan"
    skan.mkdir(parents=True, exist_ok=True)
    inf = info_wideo(a.wideo)
    if inf["hdr"]:
        print("UWAGA: nagranie jest w HDR (%s). Ten ffmpeg nie ma zscale, więc kolory klatek mogą wyjść sprane. "
              "Obejrzyj klatkę po `dopracuj`; w razie czego weź wersję SDR z montażu." % inf["color_transfer"])
    edl = wczytaj_edl(a.edl)
    od = a.od if a.od is not None else (max(0.0, edl[0][0] - 1) if edl else 0.0)
    do = a.do if a.do is not None else (min(inf["dlugosc"], max(e[1] for e in edl) + 1) if edl else inf["dlugosc"])
    meta = {"wideo": str(Path(a.wideo).resolve()), "fps": a.fps, "od": round(od, 3), "do": round(do, 3), "szer": a.szer}
    meta_p = wyj / "skan_meta.json"
    stare_meta = json.loads(meta_p.read_text()) if meta_p.exists() else {}
    gotowe = all(stare_meta.get(k) == v for k, v in meta.items()) and any(skan.glob("*.jpg"))
    if not gotowe or a.od_nowa:
        for f in skan.glob("*.jpg"):
            f.unlink()
        print("Skanuję %s → %s co %.2f s (ok. %d klatek, kilka minut przy 4K)…" % (czas(od), czas(do), 1 / a.fps, (do - od) * a.fps))
        vf = "fps=%g,scale='if(gt(iw,ih),%d,-2)':'if(gt(iw,ih),-2,%d)'" % (a.fps, a.szer, a.szer)
        uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "%.3f" % od, "-t", "%.3f" % (do - od),
                 "-i", str(a.wideo), "-vf", vf, "-q:v", "4", "-start_number", "0", str(skan / "%06d.jpg")])
    # Filtr fps oddaje ostatnią klatkę z każdego przedziału, więc klatka n leży pod koniec swojej 1/3 sekundy.
    # Bez tej poprawki czasy na arkuszach były o ok. 0,17 s za wczesne (zmierzone na IMG_0529).
    meta["korekta"] = round(0.5 / a.fps - 0.5 / inf["fps"], 4)
    meta_p.write_text(json.dumps(meta))
    pliki = sorted(skan.glob("*.jpg"))
    if not pliki:
        blad("ffmpeg nie zapisał żadnej klatki")
    lista = wyj / "skan_lista.txt"
    lista.write_text("\n".join(str(p) for p in pliki), encoding="utf-8")
    wiersze = []
    for linia in wizja("ocen", "--lista", lista).splitlines():
        d = json.loads(linia)
        n = int(Path(d["plik"]).stem)
        d["n"] = n
        d["t"] = round(od + n / a.fps + meta["korekta"], 3)
        wiersze.append(d)
    (wyj / "skan.jsonl").write_text("\n".join(json.dumps(w, ensure_ascii=False) for w in wiersze), encoding="utf-8")
    print("Oceniono %d klatek, twarz na %d." % (len(wiersze), sum(1 for w in wiersze if w.get("twarz"))))
    ranking(wyj, wiersze, edl, wczytaj_momenty(a.momenty, edl), a.ile, a.odstep,
            [] if a.z_zajetymi else zajete_klatki(wyj))


def korekta_starego_skanu(katalog):
    """Skany zrobione przed poprawką czasu mają czasy klatek o ok. 0,17 s za wczesne. Zwraca brakującą poprawkę."""
    mp = Path(katalog) / "skan_meta.json"
    if not mp.exists():
        return 0.0
    meta = json.loads(mp.read_text())
    if "korekta" in meta or not meta.get("fps"):
        return 0.0
    return round(0.5 / meta["fps"] - 0.5 / 60, 4)


def wiersz_skanu(katalog, t):
    """Klatka skanu o czasie z arkusza (jej miary miny służą potem za wzorzec w dopracuj)."""
    sj = Path(katalog) / "skan.jsonl"
    if not sj.exists():
        return None
    najbl = None
    for linia in sj.read_text(encoding="utf-8").splitlines():
        if not linia.strip():
            continue
        d = json.loads(linia)
        if d.get("twarz") and all(x in d["twarz"] for x in POTRZEBNE):
            dt = abs(d["t"] - t)
            if dt <= 0.17 and (najbl is None or dt < najbl[0]):
                najbl = (dt, d)
    return najbl[1] if najbl else None


def zajete_klatki(wyj):
    """Czasy klatek już użytych w wariantach (A/klatka.json, B/klatka.json…), żeby nowy ranking ich nie powtarzał."""
    czasy = []
    for kj in sorted(Path(wyj).glob("*/klatka.json")):
        try:
            czasy.append(float(json.loads(kj.read_text(encoding="utf-8"))["t"]))
        except (ValueError, KeyError, OSError):
            pass
    return czasy


def cmd_ranking(a):
    wyj = Path(a.katalog)
    p = wyj / "skan.jsonl"
    if not p.exists():
        blad("brak %s — najpierw `skanuj`" % p)
    wiersze = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    k = korekta_starego_skanu(wyj)
    if k:
        # Zapis na stałe, żeby czas na arkuszu i czas w skan.jsonl były tym samym czasem.
        for w in wiersze:
            w["t"] = round(w["t"] + k, 3)
        p.write_text("\n".join(json.dumps(w, ensure_ascii=False) for w in wiersze), encoding="utf-8")
        mp = wyj / "skan_meta.json"
        meta = json.loads(mp.read_text())
        meta["korekta"] = k
        mp.write_text(json.dumps(meta))
        print("Skan sprzed poprawki czasu: dodałem %.2f s do czasów klatek (arkusze pokażą nowe czasy)." % k)
    edl = wczytaj_edl(a.edl)
    ranking(wyj, wiersze, edl, wczytaj_momenty(a.momenty, edl), a.ile, a.odstep,
            [] if a.z_zajetymi else zajete_klatki(wyj))


POTRZEBNE = ("usta_szer", "usta_otw", "kaciki", "brwi", "oko_l", "oko_p", "jakosc", "ostrosc")


def statystyki(tw):
    st = {}
    for k in ("usta_szer", "usta_otw", "kaciki", "brwi", "oko", "h"):
        v = [r["twarz"][k] for r in tw]
        m = statistics.median(v)
        s = statistics.median([abs(x - m) for x in v]) * 1.4826
        st[k] = {"med": round(m, 4), "mad": round(max(s, 1e-4), 4)}
    return st


def ocen_wyraz(t, st):
    """Miary miny względem tego, jak ta osoba wygląda zwykle w tym nagraniu (odchylenia od mediany)."""
    def z(k):
        return (t[k] - st[k]["med"]) / st[k]["mad"]
    zs, zo, zk, zb = z("usta_szer"), z("usta_otw"), z("kaciki"), z("brwi")
    return {
        "usmiech": zs + 0.5 * zk - 0.4 * max(0.0, zo - 1),
        "akcent": 0.7 * max(zo, 0.0) + 0.8 * max(zb, 0.0),
        "spokoj": -zo - 0.3 * abs(zs),
    }


def ranking(wyj, wiersze, edl, momenty, ile=18, odstep=1.5, zajete=()):
    tw = [r for r in wiersze if r.get("twarz") and all(k in r["twarz"] for k in POTRZEBNE)]
    if len(tw) < 10:
        blad("za mało klatek z twarzą (%d) — sprawdź zakres --od/--do" % len(tw))
    for r in tw:
        r["twarz"]["oko"] = (r["twarz"]["oko_l"] + r["twarz"]["oko_p"]) / 2
    st = statystyki(tw)
    # Odrzuć detekcje o nietypowym rozmiarze (odchylony do tyłu, wstaje, ktoś inny w kadrze).
    tw = [r for r in tw if 0.7 * st["h"]["med"] <= r["twarz"]["h"] <= 1.6 * st["h"]["med"]]
    js = sorted(r["twarz"]["jakosc"] for r in tw)
    os_ = sorted(r["twarz"]["ostrosc"] for r in tw)

    def ranga(posortowane, x):
        return bisect.bisect_right(posortowane, x) / len(posortowane)

    for r in tw:
        t = r["twarz"]
        poza = max(0.0, 1 - (abs(t.get("yaw", 0)) / 40) ** 2 - (abs(t.get("pitch", 0)) / 30) ** 2 - (abs(t.get("roll", 0)) / 35) ** 2)
        wygl = 0.5 * ranga(js, t["jakosc"]) + 0.3 * ranga(os_, t["ostrosc"]) + 0.2 * poza
        if (t["oko"] - st["oko"]["med"]) / st["oko"]["mad"] < -2.2:
            wygl *= 0.6  # mrugnięcie
        oc = ocen_wyraz(t, st)
        # Dłoń liczy się jako gest, gdy jest wyraźnie nad blatem.
        uniesione = [h for h in r.get("rece", []) if h["pewnosc"] >= 0.5 and h["y"] + h["h"] / 2 < 0.78 and h["h"] >= 0.1]
        oc["gest"] = len(uniesione) + (max((0.78 - (h["y"] + h["h"] / 2)) for h in uniesione) * 2 if uniesione else -1)
        oc["najlepsze"] = 1.0
        r["t_film"] = zrodlo_na_film(r["t"], edl) if edl else None
        if edl and r["t_film"] is not None:
            wygl += 0.04  # klatka z ujęcia, które weszło do filmu
        r["wyglad"] = round(wygl, 3)
        r["wyraz"] = {k: round(v, 2) for k, v in oc.items()}

    # Statystyki liczymy ze wszystkich klatek, ale kandydatów szukamy poza okolicą klatek już użytych.
    wolne = [r for r in tw if all(abs(r["t"] - z) > 3.0 for z in zajete)]
    if zajete:
        print("Pomijam okolice klatek użytych już w wariantach (%s). Opcja --z-zajetymi je przywraca."
              % ", ".join(czas(z) for z in zajete))

    def wybierz(pula, klucz, n, przerwa):
        wybrane = []
        for r in sorted(pula, key=klucz, reverse=True):
            if all(abs(r["t"] - w["t"]) >= przerwa for w in wybrane):
                wybrane.append(r)
                if len(wybrane) >= n:
                    break
        return wybrane

    wynik = {"statystyki": st, "kategorie": {}, "momenty": {}}
    progi = {"usmiech": 1.0, "akcent": 1.0, "spokoj": 0.6, "gest": 1.0, "najlepsze": 0.0}

    def wpis(r, kat=None):
        d = {"n": r["n"], "t": r["t"], "t_film": None if r["t_film"] is None else round(r["t_film"], 2),
             "wyglad": r["wyglad"], "wyraz": r["wyraz"], "plik": r["plik"]}
        if kat:
            d["wynik"] = round(r["wyglad"] + 0.2 * min(r["wyraz"][kat], 3.0), 3)
        return d

    for kat in KATEGORIE:
        pula = [r for r in wolne if r["wyraz"][kat] >= progi[kat]]
        if len(pula) < ile:  # mało wyrazistych klatek: bierz najlepsze, jakie są
            pula = sorted(wolne, key=lambda r: r["wyraz"][kat], reverse=True)[:max(ile * 4, 40)]
        wyb = wybierz(pula, lambda r: r["wyglad"] + 0.2 * min(r["wyraz"][kat], 3.0), ile, odstep)
        wynik["kategorie"][kat] = [wpis(r, kat) for r in wyb]
        kom = [{"src": r["plik"], "w": r["w"], "h": r["h"], "twarz": r["twarz"],
                "gora": "#%d  ·  %s" % (r["n"], czas(r["t"])),
                "dol": "wygląd %.2f · %s %+.1f%s" % (r["wyglad"], kat, r["wyraz"][kat],
                                                    "" if r["t_film"] is None else " · film " + czas(r["t_film"]))}
               for r in wyb]
        if kom:
            # Arkusz gestów pokazuje prawie cały kadr, bo w ciasnym kadrze twarzy dłoni nie widać.
            arkusz(wyj / ("arkusz_%s.jpg" % kat), "Kandydaci: %s" % KATEGORIE[kat], kom,
                   kadr_h=205 if kat == "gest" else 330, szeroki=(kat == "gest"))

    if momenty:
        kom = []
        for m in momenty:
            if m["os"] == "film":
                pula = [r for r in wolne if r["t_film"] is not None and m["od"] <= r["t_film"] <= m["do"]]
            else:
                pula = [r for r in wolne if m["od"] <= r["t"] <= m["do"]]
            wyb = wybierz(pula, lambda r: r["wyglad"] + 0.12 * max(min(r["wyraz"]["usmiech"], 3), min(r["wyraz"]["akcent"], 3), 0), 6, 0.6)
            wynik["momenty"][m["nazwa"]] = [wpis(r) for r in wyb]
            for r in wyb:
                kom.append({"src": r["plik"], "w": r["w"], "h": r["h"], "twarz": r["twarz"], "sekcja": m["nazwa"],
                            "gora": "#%d  ·  %s" % (r["n"], czas(r["t"])),
                            "dol": "wygląd %.2f · uśm %+.1f · akc %+.1f" % (r["wyglad"], r["wyraz"]["usmiech"], r["wyraz"]["akcent"])})
        if kom:
            arkusz(wyj / "arkusz_momenty.jpg", "Najlepsze klatki w wybranych momentach filmu", kom)

    (wyj / "kandydaci.json").write_text(json.dumps(wynik, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Kandydaci: %s" % (wyj / "kandydaci.json"))
    for kat in KATEGORIE:
        top = wynik["kategorie"][kat][:5]
        print("  %-10s %s" % (kat, "  ".join("#%d@%s" % (k["n"], czas(k["t"])) for k in top)))
    print("Arkusze do obejrzenia: %s" % ", ".join(sorted(p.name for p in wyj.glob("arkusz_*.jpg"))))
    print("Numer po # to plik w skan/ (np. #2550 → skan/002550.jpg): otwórz go, gdy chcesz zobaczyć cały kadr z dłońmi.")


# ------------------------------------------------------------------ dopracuj

def cmd_dopracuj(a):
    wyj = Path(a.wyj)
    seria = wyj / "seria"
    if seria.exists():
        shutil.rmtree(seria)
    seria.mkdir(parents=True)
    inf = info_wideo(a.wideo)
    fps = inf["fps"]
    katalog_skanu = Path(a.skan) if a.skan else wyj.parent
    # Czas z arkusza starszego skanu jest o ok. 0,17 s za wczesny: przesuwamy środek serii o brakującą poprawkę.
    srodek = a.t + korekta_starego_skanu(katalog_skanu)
    t0 = max(0.0, srodek - a.okno)
    dl = max(2 * a.okno, 1.0 / fps)
    uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "%.3f" % t0, "-t", "%.3f" % dl, "-i", str(a.wideo),
             "-q:v", "1", "-start_number", "0", str(seria / "%03d.jpg")])
    pliki = sorted(seria.glob("*.jpg"))
    if not pliki:
        blad("brak klatek w oknie %.2f–%.2f s" % (t0, t0 + dl))
    lista = wyj / "seria_lista.txt"
    lista.write_text("\n".join(str(p) for p in pliki), encoding="utf-8")
    wiersze = []
    for linia in wizja("ocen", "--lista", lista).splitlines():
        d = json.loads(linia)
        d["k"] = int(Path(d["plik"]).stem)
        d["t"] = round(t0 + d["k"] / fps, 4)
        wiersze.append(d)
    lista.unlink()
    tw = [r for r in wiersze if r.get("twarz") and all(k in r["twarz"] for k in POTRZEBNE)]
    if not tw:
        blad("w tym oknie nie widać twarzy")
    # Wzorzec miny. Gdy obok leży skan, bierzemy z niego klatkę o tym czasie i szukamy w serii tej,
    # która ma tę samą minę i to samo położenie twarzy: czas z arkusza trafia z dokładnością do kilku
    # klatek, a mina zmienia się szybciej. Bez skanu wzorcem jest klatka najbliższa w czasie.
    ze_skanu = wiersz_skanu(katalog_skanu, a.t)
    if ze_skanu:
        ws, sw, sh = ze_skanu["twarz"], ze_skanu["w"], ze_skanu["h"]

        def roznica(r):
            t = r["twarz"]
            return (abs(t["usta_szer"] - ws["usta_szer"]) / 0.05 + abs(t["usta_otw"] - ws["usta_otw"]) / 0.04
                    + abs(t["brwi"] - ws["brwi"]) / 0.03 + abs(t.get("roll", 0) - ws.get("roll", 0)) / 1.0
                    + abs((t["x"] + t["w"] / 2) / r["w"] - (ws["x"] + ws["w"] / 2) / sw) / 0.003
                    + abs((t["y"] + t["h"] / 2) / r["h"] - (ws["y"] + ws["h"] / 2) / sh) / 0.003)
        # Szukamy tylko w pobliżu oczekiwanego czasu (±0,08 s): dalej podobna mina to już inny moment.
        wzorzec = min([r for r in tw if abs(r["t"] - srodek) <= 0.08] or tw, key=roznica)
    else:
        wzorzec = min(tw, key=lambda r: abs(r["t"] - srodek))
    wzor = wzorzec["twarz"]
    js = sorted(r["twarz"]["jakosc"] for r in tw)
    os_ = sorted(r["twarz"]["ostrosc"] for r in tw)
    for r in tw:
        t = r["twarz"]
        r["odl"] = round((abs(t["usta_szer"] - wzor["usta_szer"]) / 0.05 + abs(t["usta_otw"] - wzor["usta_otw"]) / 0.04
                          + abs(t["brwi"] - wzor["brwi"]) / 0.03) / 3, 2)
        r["mrug"] = ((t["oko_l"] + t["oko_p"]) / 2) < 0.75 * ((wzor["oko_l"] + wzor["oko_p"]) / 2)
        r["wynik"] = round(0.55 * bisect.bisect_right(os_, t["ostrosc"]) / len(os_)
                           + 0.45 * bisect.bisect_right(js, t["jakosc"]) / len(js), 3)
    # Wybór tylko spośród klatek z miną bliską wzorcowi. Bez tej granicy wygrywała klatka ostrzejsza,
    # ale już z inną miną (uśmiech znika w 0,3 s).
    blisko = [r for r in tw if r["odl"] <= a.mina and not r["mrug"]] or [wzorzec]
    # Przy podobnej jakości wygrywa klatka bliżej wzorca (to samo spojrzenie i ułożenie głowy).
    najl = max(blisko, key=lambda r: r["wynik"] - 0.3 * abs(r["t"] - wzorzec["t"]))
    if a.klatka is not None:
        wyb = [r for r in wiersze if r["k"] == a.klatka]
        if not wyb:
            blad("nie ma klatki %d w serii (0–%d)" % (a.klatka, len(pliki) - 1))
        najl = wyb[0]
    klatka = wyj / "klatka.png"
    uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "%.3f" % t0, "-i", str(a.wideo),
             "-vf", "select=eq(n\\,%d)" % najl["k"], "-frames:v", "1", str(klatka)])
    # Arkusz po kolei w czasie: 18 klatek rozłożonych równo, zawsze ze wskazaną i wybraną.
    krok = max(1, len(tw) // 16)
    pokaz = {r["k"] for r in tw[::krok]} | {wzorzec["k"], najl["k"]}
    kom = []
    for r in tw:
        if r["k"] not in pokaz:
            continue
        znaki = ("  ← wybrana" if r["k"] == najl["k"] else "") + ("  (wskazana)" if r["k"] == wzorzec["k"] else "")
        kom.append({"src": r["plik"], "w": r["w"], "h": r["h"], "twarz": r["twarz"],
                    "gora": "klatka %d%s" % (r["k"], znaki),
                    "dol": "ostr %.0f · jak %.2f · mina Δ%.1f%s" % (r["twarz"]["ostrosc"], r["twarz"]["jakosc"], r["odl"],
                                                                " · mrugnięcie" if r["mrug"] else "")})
    arkusz(wyj / "seria.jpg", "Seria wokół %s, klatki po kolei (mina Δ = odległość od wskazanej)" % czas(a.t), kom)
    info = {"wideo": str(Path(a.wideo).resolve()), "t": najl["t"], "t_wskazany": a.t, "okno": a.okno, "klatka_w_serii": najl["k"],
            "twarz": najl.get("twarz"), "rece": najl.get("rece"), "w": najl["w"], "h": najl["h"]}
    (wyj / "klatka.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    if not a.zostaw:
        shutil.rmtree(seria)
    print("Klatka: %s  (t = %s, klatka %d z %d w serii, ostrość %.0f, jakość %.2f)" % (
        klatka, czas(najl["t"]), najl["k"], len(pliki), najl["twarz"]["ostrosc"] if najl.get("twarz") else 0,
        najl["twarz"]["jakosc"] if najl.get("twarz") else 0))
    print("Obejrzyj %s (klatki po kolei). Inną wymusisz przez --klatka K; --mina 1.5 dopuszcza większą zmianę miny."
          % (wyj / "seria.jpg"))


# ------------------------------------------------------------------ wytnij

def cmd_wytnij(a):
    wej = Path(a.klatka)
    wyj = Path(a.wyj) if a.wyj else wej.with_name("postac.png")
    args = ["wytnij", wej, wyj, "--tryb", a.tryb, "--skurcz", a.skurcz, "--wtop", a.wtop]
    for g in a.wymaz or []:
        args += ["--wymaz", g]
    info = json.loads(wizja(*args).strip().splitlines()[-1])
    info["wymazane"] = a.wymaz or []
    wyj.with_suffix(".json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    podglad = wyj.with_name(wyj.stem + "_podglad.jpg")
    podglad_wyciecia(wyj, info, podglad)
    k = info["kadr"]
    if a.lupa:
        cz = [float(x) for x in a.lupa.split(",")]
        if len(cz) not in (2, 3):
            blad("--lupa oczekuje X,Y albo X,Y,R w pikselach klatki")
        lupa = wyj.with_name(wyj.stem + "_lupa.jpg")
        lupa_wyciecia(wyj, info, lupa, cz[0], cz[1], cz[2] if len(cz) == 3 else 120)
        print("Lupa: %s (siatka co 20 px klatki)." % lupa)
    print("Postać: %s (%d×%d, tryb %s)  twarz: %s" % (wyj, k["w"], k["h"], info["tryb"], info.get("twarz")))
    print("Obejrzyj %s: szyja i okolice uszu, przestrzeń między palcami, dziura po mikrofonie." % podglad)
    print("Linijki na podglądzie są w pikselach klatki; resztkę tła usuniesz przez --wymaz x,y,r (środek koła na resztce).")
    if info["tryb"] != a.tryb:
        print("UWAGA: tryb „%s” nie dał maski, użyłem „%s”." % (a.tryb, info["tryb"]))


def podglad_wyciecia(png, info, jpg, panel=900):
    """Wycięcie na ciemnym tle i na tle w kolorze akcentu (#00E5A0), z linijkami w pikselach klatki (do celowania gumką)."""
    k = info["kadr"]
    sk = panel / k["w"]
    wys = k["h"] * sk
    krok = 200
    znaczniki = []
    x = (k["x"] // krok + 1) * krok
    while x < k["x"] + k["w"]:
        znaczniki.append('<i class="x" style="left:%.1fpx">%d</i>' % ((x - k["x"]) * sk, x))
        x += krok
    y = (k["y"] // krok + 1) * krok
    while y < k["y"] + k["h"]:
        znaczniki.append('<i class="y" style="top:%.1fpx">%d</i>' % ((y - k["y"]) * sk, y))
        y += krok
    linijki = "".join(znaczniki)
    strona = """<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:%dpx;display:flex;font:600 15px -apple-system,sans-serif;background:#000}
.p{position:relative;width:%dpx;height:%.0fpx;overflow:hidden}
.p img{width:%dpx;display:block}
i{position:absolute;font-style:normal;color:#fff;text-shadow:0 0 3px #000,0 0 3px #000;opacity:.9}
i.x{top:0;border-left:2px solid rgba(255,255,255,.85);padding:1px 0 0 4px;height:18px}
i.y{left:0;border-top:2px solid rgba(255,255,255,.85);padding:0 0 0 3px;width:60px}
</style></head><body>
<div class="p" style="background:#0f1012"><img src="%s">%s</div>
<div class="p" style="background:#00E5A0"><img src="%s">%s</div>
</body></html>""" % (2 * panel, panel, wys, panel, Path(png).resolve().as_uri(), linijki, Path(png).resolve().as_uri(), linijki)
    jpg = Path(jpg)
    tmp_html = jpg.with_suffix(".html")
    tmp_png = jpg.with_suffix(".tmp.png")
    tmp_html.write_text(strona, encoding="utf-8")
    render_html(tmp_html, tmp_png, szer=2 * panel, wys=int(wys), skala=1)
    do_jpg(tmp_png, jpg, max_bajty=2_500_000)
    tmp_png.unlink()
    tmp_html.unlink()


def lupa_wyciecia(png, info, jpg, x, y, r, panel=900):
    """Powiększony wycinek wycięcia wokół punktu klatki (x, y) z siatką co 20 px: do celowania gumką."""
    k = info["kadr"]
    sk = panel / (2 * r)
    x0, y0 = x - r, y - r
    linie = []
    gx = int(x0 // 20 + 1) * 20
    while gx < x0 + 2 * r:
        gruba = gx % 100 == 0
        linie.append('<i class="x%s" style="left:%.1fpx">%s</i>' % (" g" if gruba else "", (gx - x0) * sk, gx if gruba or 2 * r <= 300 else ""))
        gx += 20
    gy = int(y0 // 20 + 1) * 20
    while gy < y0 + 2 * r:
        gruba = gy % 100 == 0
        linie.append('<i class="y%s" style="top:%.1fpx">%s</i>' % (" g" if gruba else "", (gy - y0) * sk, gy if gruba or 2 * r <= 300 else ""))
        gy += 20
    siatka = "".join(str(l) for l in linie)
    styl_img = "width:%.1fpx;left:%.1fpx;top:%.1fpx" % (k["w"] * sk, -(x0 - k["x"]) * sk, -(y0 - k["y"]) * sk)
    adres = Path(png).resolve().as_uri()
    strona = """<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;box-sizing:border-box}
body{width:%dpx;display:flex;font:600 14px -apple-system,sans-serif;background:#000}
.p{position:relative;width:%dpx;height:%dpx;overflow:hidden}
.p img{position:absolute;max-width:none}
i{position:absolute;font-style:normal;color:#fff;text-shadow:0 0 3px #000,0 0 3px #000}
i.x{top:0;bottom:0;border-left:1px solid rgba(255,255,255,.28);padding:2px 0 0 3px}
i.y{left:0;right:0;border-top:1px solid rgba(255,255,255,.28);padding:0 0 0 3px}
i.g{border-color:rgba(255,255,255,.7)}
</style></head><body>
<div class="p" style="background:#0f1012"><img src="%s" style="%s">%s</div>
<div class="p" style="background:#00E5A0"><img src="%s" style="%s">%s</div>
</body></html>""" % (2 * panel, panel, panel, adres, styl_img, siatka, adres, styl_img, siatka)
    jpg = Path(jpg)
    tmp_html = jpg.with_suffix(".html")
    tmp_png = jpg.with_suffix(".tmp.png")
    tmp_html.write_text(strona, encoding="utf-8")
    render_html(tmp_html, tmp_png, szer=2 * panel, wys=panel, skala=1)
    do_jpg(tmp_png, jpg, max_bajty=2_500_000)
    tmp_png.unlink()
    tmp_html.unlink()


# ------------------------------------------------------------------ render

def cmd_render(a):
    src = Path(a.html)
    png = Path(a.wyj) if a.wyj else src.with_suffix(".png")
    render_html(src, png, a.szer, a.wys, a.skala)
    print("PNG: %s (%d×%d)" % (png, a.szer * a.skala, a.wys * a.skala))
    if not a.bez_jpg:
        # JPG w pełnej rozdzielczości renderu (YouTube zaleca 3840×2160), ale poniżej 2 MB,
        # bo tyle przyjmuje aplikacja na telefonie (z komputera limit to 50 MB).
        d = do_jpg(png, png.with_suffix(".jpg"), szer=a.jpg_szer)
        print("JPG: %s (%d×%d, %.0f kB, jakość %.2f)" % (d["plik"], d["w"], d["h"], d["bajty"] / 1000, d["jakosc"]))


# ------------------------------------------------------------------ kontrola

# OCR czasem oddaje łacińskie wersaliki cyrylicą albo greką („АРКА” zamiast „APKA”). To te same kształty,
# więc przed porównaniem sprowadzamy je do łacińskich.
SOBOWTORY = {"А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P", "С": "C", "Т": "T",
             "Х": "X", "У": "Y", "І": "I", "Ј": "J", "Ѕ": "S", "а": "a", "е": "e", "о": "o", "р": "p", "с": "c",
             "х": "x", "у": "y", "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K", "Μ": "M",
             "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X"}


def normalizuj(s):
    zam = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    s = "".join(SOBOWTORY.get(ch, ch) for ch in s)
    return "".join(ch for ch in s.translate(zam).upper() if ch.isalnum())


def slowa_rozpoznane(oczekiwane, linie):
    """Które z oczekiwanych słów OCR odczytał (bez polskich znaków, bez interpunkcji)."""
    calosc = normalizuj(" ".join(l["tekst"] for l in linie))
    return [(w, normalizuj(w) in calosc) for w in oczekiwane if normalizuj(w)]


def cmd_kontrola(a):
    raport = []
    karty = []
    wszystko_ok = True
    wszystkie_tytuly = []
    for sciezka in a.pliki:
        p = Path(sciezka)
        if not p.exists():
            blad("brak pliku %s" % p)
        uwagi, bledy = [], []
        meta_p = p.with_suffix(".json")
        meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
        o = json.loads(wizja("ocen", p).strip().splitlines()[-1])
        W, H = o["w"], o["h"]
        if abs(W / H - 16 / 9) > 0.01:
            bledy.append("proporcje %d×%d to nie 16:9" % (W, H))
        if W < 1280:
            bledy.append("szerokość %d px: poniżej 1280 YouTube pomniejsza wszystkie warianty testu A/B do 480p" % W)
        rozmiar = p.stat().st_size
        if rozmiar > 50_000_000:
            bledy.append("plik ma %.1f MB, limit YouTube to 50 MB" % (rozmiar / 1e6))
        elif rozmiar > 2_000_000:
            uwagi.append("plik ma %.2f MB: z komputera wejdzie (limit 50 MB), z telefonu nie (limit 2 MB)" % (rozmiar / 1e6))
        # Twarz.
        t = o.get("twarz")
        if t:
            udzial = t["h"] / H
            if udzial < a.min_twarz:
                uwagi.append("twarz zajmuje %.0f%% wysokości (zalecane ≥ %.0f%%)" % (udzial * 100, a.min_twarz * 100))
        elif not meta.get("bez_twarzy"):
            uwagi.append("Vision nie widzi twarzy na miniaturze")
        # Tekst: pełny rozmiar i rozmiar z listy filmów.
        duzy = json.loads(wizja("tekst", p).strip().splitlines()[-1])
        maly = json.loads(wizja("tekst", p, "--szer", a.maly).strip().splitlines()[-1])
        # Duże linie muszą dać się przeczytać w obu rozmiarach. Dopiski (pigułka) tylko w pełnym:
        # w rozmiarze listy są z założenia za małe.
        glowne = [w for linia in meta.get("tekst", []) for w in str(linia).split()]
        dopiski = [w for linia in meta.get("tekst_dodatkowy", []) for w in str(linia).split()]
        if glowne or dopiski:
            brak_d = [w for w, ok in slowa_rozpoznane(glowne + dopiski, duzy["linie"]) if not ok]
            brak_m = [w for w, ok in slowa_rozpoznane(glowne, maly["linie"]) if not ok]
            if brak_d:
                uwagi.append("OCR nie czyta w pełnym rozmiarze: %s (sprawdź kontrast albo zasłonięcie)" % ", ".join(brak_d))
            if brak_m:
                uwagi.append("przy %d px nieczytelne dla OCR: %s" % (a.maly, ", ".join(brak_m)))
            # Słowa liczymy tylko w dużych liniach i tylko te z literą lub cyfrą („$”, „→” to nie słowa).
            n_slow = len([w for w in glowne if any(ch.isalnum() for ch in w)])
            if n_slow > 5:
                uwagi.append("%d słów w dużych liniach — celuj w 2–4" % n_slow)
        # Strefa znacznika czasu (prawy dolny róg) i tekst na twarzy.
        for l in duzy["linie"]:
            if l["pewnosc"] < 0.3 or len(normalizuj(l["tekst"])) < 2:
                continue
            x1, y1 = l["x"] + l["w"], l["y"] + l["h"]
            if x1 > 0.86 and y1 > 0.86:
                uwagi.append("napis „%s” wchodzi w prawy dolny róg, gdzie YouTube pokazuje czas filmu" % l["tekst"])
            if t:
                fx0, fy0 = t["x"] / W, t["y"] / H
                fx1, fy1 = fx0 + t["w"] / W, fy0 + t["h"] / H
                wsp = max(0, min(x1, fx1) - max(l["x"], fx0)) * max(0, min(y1, fy1) - max(l["y"], fy0))
                if wsp > 0.15 * (t["w"] / W) * (t["h"] / H):
                    uwagi.append("napis „%s” zasłania twarz" % l["tekst"])
        # Jasność: bardzo ciemna miniatura ginie w ciemnym motywie YouTube.
        st = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-vf", "scale=96:54,signalstats,metadata=print:file=-",
                             "-f", "null", "-"], capture_output=True, text=True).stdout
        yavg = [float(l.split("=")[1]) for l in st.splitlines() if "signalstats.YAVG" in l]
        if yavg and yavg[0] < 38:
            uwagi.append("średnia jasność %.0f/255 — miniatura może ginąć w ciemnym motywie" % yavg[0])
        # Tytuły: do każdej miniatury dwie propozycje (Jakub puszcza test jako pary tytuł + miniatura).
        tyt = [str(x).strip() for x in meta.get("tytuly", []) if str(x).strip()]
        if meta_p.exists():
            if len(tyt) != 2:
                uwagi.append("tytuły: jest %d, a ma być 2 propozycje do tej miniatury (pole „tytuly” w sklad.py)" % len(tyt))
            for x in tyt:
                if len(x) > 100:
                    bledy.append("tytuł „%s” ma %d znaków, limit YouTube to 100" % (x, len(x)))
                elif len(x) > 60:
                    uwagi.append("tytuł „%s” ma %d znaków: na liście zostanie ucięty po ok. 60" % (x, len(x)))
            if len(tyt) == 2 and normalizuj(tyt[0]) == normalizuj(tyt[1]):
                uwagi.append("obie propozycje tytułu są takie same")
            for linia_napisu in meta.get("tekst", []):
                nl = normalizuj(str(linia_napisu))
                for x in tyt:
                    if len(nl) >= 6 and nl in normalizuj(x):
                        uwagi.append("tytuł „%s” powtarza napis z miniatury („%s”): tytuł ma dokładać powód do kliknięcia, a nie to samo"
                                     % (x, linia_napisu))
            wszystkie_tytuly += [(p.name, x) for x in tyt]
        ok = not bledy
        wszystko_ok = wszystko_ok and ok
        raport.append({"plik": str(p), "w": W, "h": H, "kB": round(rozmiar / 1000), "twarz_udzial": round(t["h"] / H, 3) if t else None,
                       "jasnosc": round(yavg[0], 1) if yavg else None, "bledy": bledy, "uwagi": uwagi,
                       "ocr_maly": [l["tekst"] for l in maly["linie"]], "tytuly": tyt})
        karty.append((p, meta))
        print("%s  %d×%d  %d kB  twarz %s  jasność %s" % (p.name, W, H, rozmiar / 1000,
              ("%.0f%%" % (t["h"] / H * 100)) if t else "–", ("%.0f" % yavg[0]) if yavg else "–"))
        for b in bledy:
            print("   BŁĄD: " + b)
        for u in uwagi:
            print("   uwaga: " + u)
        if not bledy and not uwagi:
            print("   OK")
    # Każda miniatura ma własne tytuły: ten sam tytuł przy dwóch miniaturach nie rozróżni par w teście.
    gdzie = {}
    for plik_t, x in wszystkie_tytuly:
        gdzie.setdefault(normalizuj(x), set()).add(plik_t)
    for nx, pliki_t in gdzie.items():
        if len(pliki_t) > 1:
            print("uwaga zestawu: ten sam tytuł jest przy kilku miniaturach (%s)" % ", ".join(sorted(pliki_t)))
    wyj = Path(a.wyj) if a.wyj else Path(a.pliki[0]).with_name("podglad.jpg")
    podglad_listy(wyj, karty, a.tytul or "Tytuł filmu", a.czas)
    wyj.with_suffix(".json").write_text(json.dumps(raport, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Podgląd w rozmiarach z YouTube: %s — obejrzyj go, zanim oddasz miniatury." % wyj)
    if not wszystko_ok:
        sys.exit(1)


def podglad_listy(sciezka_jpg, karty, tytul, czas_filmu):
    """Makieta listy filmów: każda miniatura w rozmiarze strony głównej i paska bocznego, na ciemnym i jasnym tle."""
    def karta(p, meta, szer):
        # Para tytuł + miniatura: pierwsza propozycja stoi jak na liście filmów, druga pod spodem (tylko w dużym rozmiarze).
        tyt = [str(x) for x in meta.get("tytuly", []) if str(x).strip()]
        glowny = tyt[0] if tyt else tytul
        drugi = ('<div class="s">tytuł 2: %s</div>' % html.escape(tyt[1])) if (szer >= 300 and len(tyt) > 1) else ""
        return ('<div class="f" style="width:%dpx"><div class="m"><img src="%s"><span class="c">%s</span></div>'
                '<div class="t">%s</div><div class="s">wariant %s · %s</div>%s</div>'
                % (szer, Path(p).resolve().as_uri(), html.escape(czas_filmu), html.escape(glowny),
                   html.escape(str(meta.get("id", Path(p).stem))), html.escape(str(meta.get("hipoteza", ""))), drugi))

    def wiersz(szer):
        return '<div class="r">%s</div>' % "".join(karta(p, m, szer) for p, m in karty)

    szer = max(1180, 60 + len(karty) * 392)
    strona = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'IT';src:url('%s');font-weight:100 900}
*{box-sizing:border-box;margin:0}
html{background:#fff}
body{width:%dpx;font-family:'IT',-apple-system,sans-serif}
.p{padding:22px 26px 26px}
.ciemny{background:#0f0f0f;color:#f1f1f1}.jasny{background:#fff;color:#0f0f0f}
h2{font-size:17px;font-weight:700;opacity:.6;margin-bottom:12px}
.r{display:flex;gap:24px;margin-bottom:20px;align-items:flex-start}
.m{position:relative;border-radius:12px;overflow:hidden;aspect-ratio:16/9}
.m img{width:100%%;height:100%%;display:block}
.c{position:absolute;right:6px;bottom:6px;background:rgba(0,0,0,.82);color:#fff;font-size:12px;font-weight:600;padding:2px 5px;border-radius:5px}
.t{font-size:16px;font-weight:650;line-height:1.3;margin-top:9px;max-height:2.6em;overflow:hidden}
.s{font-size:13px;opacity:.62;margin-top:3px}
.maly .t{font-size:13px}.maly .s{font-size:11px}.maly .c{font-size:10px;right:4px;bottom:4px}
</style></head><body>
<div class="p ciemny"><h2>Strona główna (360 px), ciemny motyw</h2>%s<h2>Pasek boczny (168 px)</h2><div class="maly">%s</div></div>
<div class="p jasny"><h2>Strona główna (360 px), jasny motyw</h2>%s<h2>Pasek boczny (168 px)</h2><div class="maly">%s</div></div>
</body></html>""" % (CZCIONKA.resolve().as_uri(), szer, wiersz(360), wiersz(168), wiersz(360), wiersz(168))
    sciezka_jpg = Path(sciezka_jpg)
    tmp_html = sciezka_jpg.with_suffix(".podglad.html")
    tmp_png = sciezka_jpg.with_suffix(".podglad.png")
    tmp_html.write_text(strona, encoding="utf-8")
    render_html(tmp_html, tmp_png, szer=szer, wys=1230, skala=2)
    do_jpg(tmp_png, sciezka_jpg, max_bajty=3_500_000)
    tmp_png.unlink()
    tmp_html.unlink()


# ------------------------------------------------------------------ eksport

def cmd_eksport(a):
    folder = Path(os.path.expanduser(a.folder)) / "Miniatury"
    folder.mkdir(parents=True, exist_ok=True)
    dzis = datetime.date.today()
    znacznik = "%02d.%02d" % (dzis.month, dzis.year % 100)
    for i, sciezka in enumerate(a.pliki):
        p = Path(sciezka)
        meta_p = p.with_suffix(".json")
        ident = json.loads(meta_p.read_text(encoding="utf-8")).get("id") if meta_p.exists() else None
        ident = ident or "ABCDEFGH"[i]
        cel = folder / ("%s_MINIATURA %s_%s%s" % (a.tytul, ident, znacznik, p.suffix.lower()))
        shutil.copy2(p, cel)
        print("→ %s" % cel)
    if a.opis:
        # test_AB_2.txt (drugi zestaw) trafia jako „… - test AB 2.txt”, żeby nie nadpisać pierwszego.
        dop = Path(a.opis).stem.replace("test_AB", "").replace("_", " ").strip()
        cel = folder / ("%s_MINIATURY_%s - test AB%s.txt" % (a.tytul, znacznik, (" " + dop) if dop else ""))
        shutil.copy2(a.opis, cel)
        print("→ %s" % cel)


# ------------------------------------------------------------------ CLI

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("skanuj", help="próbkuje nagranie, ocenia twarz na każdej klatce i układa ranking kandydatów")
    p.add_argument("wideo")
    p.add_argument("--wyj", required=True, help="katalog roboczy miniatur (np. projekty/IMG_xxxx/miniatury)")
    p.add_argument("--fps", type=float, default=3.0, help="ile klatek na sekundę oceniać (domyślnie 3)")
    p.add_argument("--od", type=sekundy, help="początek zakresu w źródle (sekundy albo M:SS)")
    p.add_argument("--do", type=sekundy, help="koniec zakresu w źródle (sekundy albo M:SS)")
    p.add_argument("--szer", type=int, default=1280, help="dłuższy bok klatek do oceny")
    p.add_argument("--edl", help="aroll/edl.json ze skilla montażu: oznacza klatki, które weszły do filmu")
    p.add_argument("--momenty", help="JSON z fragmentami, z których chcesz najlepsze klatki")
    p.add_argument("--ile", type=int, default=18, help="kandydatów na kategorię")
    p.add_argument("--odstep", type=float, default=1.5, help="minimalny odstęp między kandydatami [s]")
    p.add_argument("--od-nowa", action="store_true", help="wymuś ponowne wyciągnięcie klatek")
    p.add_argument("--z-zajetymi", action="store_true", help="nie pomijaj okolic klatek użytych już w wariantach")
    p.set_defaults(f=cmd_skanuj)

    p = sub.add_parser("ranking", help="przelicza ranking z istniejącego skanu (np. po dodaniu momentów)")
    p.add_argument("katalog")
    p.add_argument("--edl")
    p.add_argument("--momenty")
    p.add_argument("--ile", type=int, default=18)
    p.add_argument("--odstep", type=float, default=1.5)
    p.add_argument("--z-zajetymi", action="store_true", help="nie pomijaj okolic klatek użytych już w wariantach")
    p.set_defaults(f=cmd_ranking)

    p = sub.add_parser("dopracuj", help="wyciąga serię klatek wokół chwili t w pełnej jakości i zapisuje najlepszą jako klatka.png")
    p.add_argument("wideo")
    p.add_argument("--t", type=sekundy, required=True, help="czas w źródle z arkusza kandydatów: 1030.4 albo 17:10.4")
    p.add_argument("--wyj", required=True, help="katalog wariantu, np. miniatury/A")
    p.add_argument("--okno", type=float, default=0.4, help="ile sekund w każdą stronę przeszukać")
    p.add_argument("--klatka", type=int, help="wymuś klatkę o tym numerze z serii")
    p.add_argument("--skan", help="katalog ze skan.jsonl (domyślnie folder nad --wyj); stamtąd brany jest wzorzec miny")
    p.add_argument("--mina", type=float, default=0.7,
                   help="jak bardzo mina może odbiegać od wskazanej klatki (Δ z arkusza serii); domyślnie 0.7")
    p.add_argument("--zostaw", action="store_true", help="nie usuwaj klatek serii")
    p.set_defaults(f=cmd_dopracuj)

    p = sub.add_parser("wytnij", help="wycina postać z klatki (PNG z przezroczystością) i zapisuje położenie twarzy")
    p.add_argument("klatka")
    p.add_argument("--wyj")
    p.add_argument("--tryb", default="plan", choices=["plan", "plan-pelny", "osoba"],
                   help="plan: postać z tym, co ma przed sobą (mikrofon), bez fotela; "
                        "plan-pelny: także rzeczy trzymane obok ciała; osoba: sama sylwetka")
    p.add_argument("--skurcz", type=int, default=2, help="o ile pikseli cofnąć krawędź")
    p.add_argument("--wtop", type=int, default=1, help="zmiękczenie krawędzi [px]")
    p.add_argument("--wymaz", action="append", metavar="X,Y,R[,TOL]",
                   help="gumka: w kole o promieniu R wokół X,Y (piksele klatki, patrz linijki na podglądzie) znikają "
                        "piksele o kolorze podobnym do środka koła; TOL domyślnie 45, 0 = wszystko; można powtarzać")
    p.add_argument("--lupa", metavar="X,Y[,R]",
                   help="dodatkowy powiększony podgląd wokół punktu klatki (siatka co 20 px), do celowania gumką")
    p.set_defaults(f=cmd_wytnij)

    p = sub.add_parser("render", help="HTML → PNG 3840×2160 i JPG tej samej wielkości poniżej 2 MB")
    p.add_argument("html")
    p.add_argument("--wyj")
    p.add_argument("--szer", type=int, default=1920)
    p.add_argument("--wys", type=int, default=1080)
    p.add_argument("--skala", type=float, default=2, help="2 = render 3840×2160 z kadru 1920×1080")
    p.add_argument("--jpg-szer", type=int, help="szerokość JPG, gdy ma być mniejszy niż render")
    p.add_argument("--bez-jpg", action="store_true")
    p.set_defaults(f=cmd_render)

    p = sub.add_parser("kontrola", help="sprawdza gotowe miniatury i robi podgląd w rozmiarach z YouTube")
    p.add_argument("pliki", nargs="+")
    p.add_argument("--tytul", help="tytuł filmu do makiety listy")
    p.add_argument("--czas", default="15:10", help="czas filmu do znacznika w rogu")
    p.add_argument("--wyj", help="plik podglądu (domyślnie podglad.jpg obok pierwszej miniatury)")
    p.add_argument("--maly", type=int, default=320, help="szerokość, przy której tekst ma być czytelny")
    p.add_argument("--min-twarz", type=float, default=0.26, help="minimalny udział twarzy w wysokości kadru")
    p.set_defaults(f=cmd_kontrola)

    p = sub.add_parser("eksport", help="kopiuje miniatury do Eksporty/…/Miniatury z właściwymi nazwami")
    p.add_argument("pliki", nargs="+")
    p.add_argument("--tytul", required=True)
    p.add_argument("--folder", required=True, help="folder filmu w Eksporty (bez /Miniatury)")
    p.add_argument("--opis", help="plik z opisem wariantów do testu A/B")
    p.set_defaults(f=cmd_eksport)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

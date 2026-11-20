#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skład trzech miniatur do testu A/B (kadr roboczy 1920×1080, pliki wynikowe 3840×2160).

Skopiuj ten plik do projekty/<film>/miniatury/ i zmieniaj tylko dane w sekcji DANE.
Każdy wariant bierze wyciętą postać (A/postac.png + A/postac.json z `mini.py wytnij`),
ustawia ją według położenia twarzy i dokłada tło, tekst oraz dodatki.

  python3 sklad.py            # wszystkie warianty + kontrola + podglad.jpg + test_AB.txt
  python3 sklad.py B          # tylko wariant B (szybka iteracja)
  python3 sklad.py --strefy   # osobne pliki A_strefy.jpg… z naniesionymi strefami (znacznik czasu, marginesy)
"""
import html
import json
import os
import subprocess
import sys
from pathlib import Path

TU = Path(__file__).resolve().parent


def znajdz_skill():
    for k in (os.environ.get("MINIATURY_SKILL"), Path.home() / ".claude" / "skills" / "miniatury", TU.parent):
        if k and (Path(k) / "scripts" / "mini.py").exists():
            return Path(k)
    raise SystemExit("Nie znalazłem skilla miniatury. Ustaw MINIATURY_SKILL=/ścieżka/do/skilla.")


SKILL = znajdz_skill()
MINI = SKILL / "scripts" / "mini.py"
# Kolejny zestaw do tego samego filmu: skopiuj ten plik jako sklad_2.py i nazwij warianty D, E, F.
# Podgląd i opis testu dostaną wtedy przyrostek (podglad_2.jpg, test_AB_2.txt) i nie nadpiszą pierwszego zestawu.
PRZYROSTEK = Path(__file__).stem[len("sklad"):] if Path(__file__).stem.startswith("sklad") else ""
CZCIONKA = SKILL / "assets" / "InterTight.ttf"
W, H = 1920, 1080

# Paleta personal brandu Jakuba (17.11.2026): czerń, biel, ciemny szary i JEDEN akcent.
# Domyślny akcent to #00E5A0. Inny tylko wtedy, gdy wymaga tego temat filmu; reszta odcieni liczy się sama.
# Tekst i znaki NA akcencie są zawsze ciemne (#0f1012): biały na #00E5A0 ma kontrast 1,6:1.
AKCENT = "#00E5A0"


def paleta(akcent=None):
    """Odcienie liczone z akcentu: jasny (gradienty), ciemny (brzeg tła `akcent`), cień i składowe pod rgba()."""
    h = (akcent or AKCENT).lstrip("#")
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    jasny = [round(c + (255 - c) * 0.35) for c in rgb]
    return {"akcent": "#" + h, "akcent_rgb": "%d,%d,%d" % tuple(rgb),
            "akcent2": "#%02x%02x%02x" % tuple(jasny), "akcent2_rgb": "%d,%d,%d" % tuple(jasny),
            "akcent_ciemny": "#%02x%02x%02x" % tuple(round(c * 0.82) for c in rgb),
            "cien_rgb": "%d,%d,%d" % tuple(round(c * 0.3) for c in rgb)}

# ============================================================ DANE (zmieniasz tylko to)

TYTUL = "Tytuł filmu"          # do makiety listy YouTube, opisu testu i nazw plików
TYTUL_YT = ""                 # zapasowy tytuł do makiety listy, gdy wariant nie ma własnych `tytuly`; pusty = TYTUL
CZAS = "12:34"                 # długość filmu, pokazywana w rogu makiety

# Trzy warianty = trzy różne hipotezy (references/koncepcje.md), a nie trzy kolory jednego pomysłu.
# Kolejność ma znaczenie: gdy test nie wyłoni zwycięzcy, YouTube zostawia pierwszy wgrany plik,
# więc A to wariant, na który stawiasz.
#
# Współrzędne są w pikselach kadru 1920×1080 (render wychodzi w 3840×2160).
# Pola wariantu:
#   postac           wycięta postać z `mini.py wytnij`; obok musi leżeć postac.json
#   twarz            x, y: środek twarzy jako ułamek kadru; wys: wysokość twarzy jako ułamek kadru (0,34–0,42)
#   lustro           True odbija postać w poziomie (napisy na ubraniu wyjdą wspak, więc ukryj je kadrem)
#   obrys            "bialy" | "akcent": twarda obwódka jak naklejka
#   swiatlo          "akcent" | "biale" | "ciemne" | "brak": poświata wokół postaci (domyślnie dobrana do tła)
#   jasnosc_postaci  1.05 domyślnie; podnieś, gdy twarz jest ciemna
#   zaslona_dol      True przyciemnia dół kadru (ucięte ręce, blat)
#   tlo              typ: "ciemne" | "akcent" | "kadr" (klatka=…) | "obraz" (plik=…)
#                    opcje: zaslony ["lewa" | "prawa" | "dol"], rozmycie, jasnosc, winieta, poswiata,
#                    kwadraty [(x, y, bok, obrót, "pelny" | "obrys")]
#   tekst            x, szer oraz y (góra bloku) albo dol (dół bloku); linie: (napis, styl[, rozmiar])
#                    style: bialy, akcent, ciemny, klocek, klocek-ciemny, klocek-bialy, maly, skreslony
#                    ("zielony" zostaje jako alias akcentu dla starych układów)
#                    wyrownanie: "do-prawej" | "srodek"; max: największy rozmiar czcionki; za_postacia: True
#                    Linia bez rozmiaru sama dopasowuje się do szerokości, więc krótsza wychodzi większa.
#   tekst_dodatkowy  napisy z dodatków (np. z pigułki), które kontrola też ma umieć odczytać
#   uwaga            co jest poglądowe albo wygenerowane; trafia do opisu testu dla Jakuba
#   tytuly           DWIE propozycje tytułu YouTube do tej miniatury (lista dwóch napisów). Jakub puszcza test
#                    jako pary tytuł + miniatura: każda miniatura ma własny tytuł, a on wybiera jeden z dwóch.
#                    Różne kątem, do ok. 60 znaków, bez powtarzania napisu z miniatury (koncepcje.md §4)
#   dodatki          lista elementów z polami x, y (opcjonalnie obrot, za_postacia):
#                    {"rodzaj": "pigulka", "tekst": …, "rozmiar": 60}
#                    {"rodzaj": "awatary", "pliki": […], "bok": 200, "zachodzenie": 0.12, "ksztalt": "kafle"}
#                    {"rodzaj": "obraz", "plik": …, "szer": 400, "karta": True}
#                    {"rodzaj": "strzalka", "x2": …, "y2": …, "wygiecie": 0.25}
#                    {"rodzaj": "znak", "symbol": "x" | "ptaszek", "bok": 170}
#                    {"rodzaj": "html", "html": "<div …>"}

WARIANTY = [
    {
        # Ciemne tło marki, liczba jako bohater. Postać po prawej, tekst po lewej.
        "id": "A",
        "hipoteza": "Wynik w liczbach",
        "tytuly": ["Zautomatyzowałem cały dział growth w mojej firmie",
                   "Pół roku automatyzacji działu growth: co zadziałało"],
        "postac": "A/postac.png",
        "twarz": {"x": 0.735, "y": 0.41, "wys": 0.38},
        "tlo": {"typ": "ciemne"},
        "tekst": {"x": 90, "y": 130, "szer": 880, "max": 470, "linie": [("PRZYCHÓD", "bialy"), ("×2,5", "akcent")]},
        "tekst_dodatkowy": ["zespół 3× mniejszy"],
        "dodatki": [{"rodzaj": "pigulka", "x": 96, "y": 840, "tekst": "zespół 3× mniejszy", "rozmiar": 60}],
    },
    {
        # Prawdziwy pokój z tej samej klatki jako rozmyte tło. Postać po lewej, tekst i dowód po prawej.
        "id": "B",
        "hipoteza": "Mechanizm: co jest w środku",
        "tytuly": ["Agenci AI robią u nas marketing i sprzedaż. Pokazuję jak",
                   "Artur, Kaja, Weronika i Tymon: mój zespół agentów AI"],
        "postac": "B/postac.png",
        "twarz": {"x": 0.25, "y": 0.41, "wys": 0.37},
        "tlo": {"typ": "kadr", "klatka": "B/klatka.png", "zaslony": ["prawa"]},
        "tekst": {"x": 900, "y": 120, "szer": 940, "linie": [("4 AGENTÓW AI", "bialy"), ("ZAMIAST DZIAŁU", "klocek")]},
        "dodatki": [],
    },
    {
        # Tło w kolorze akcentu: najmocniej odcina się na liście filmów. Teza przeciwna do oczekiwań.
        "id": "C",
        "hipoteza": "Teza pod prąd",
        "tytuly": ["Czego AI jeszcze nie zastąpi w sprzedaży B2B",
                   "AI nie zamknie za Ciebie sprzedaży: to zostaje człowiekowi"],
        "postac": "C/postac.png",
        "twarz": {"x": 0.71, "y": 0.42, "wys": 0.40},
        "tlo": {"typ": "akcent"},
        "tekst": {"x": 90, "y": 110, "szer": 820, "linie": [("TEGO AI", "ciemny"), ("NIE ZROBI", "klocek-ciemny")]},
        "dodatki": [],
    },
]

# ============================================================ SZABLON (zwykle bez zmian)

CSS = """
@font-face{font-family:'Inter Tight';src:url('%(czcionka)s');font-weight:100 900}
:root{--akcent:%(akcent)s;--akcent2:%(akcent2)s;--akcent-rgb:%(akcent_rgb)s;--akcent-ciemny:%(akcent_ciemny)s;--cien-rgb:%(cien_rgb)s;
  --tlo:#0f1012;--zielony:var(--akcent);--szary:#c9ccd3}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:var(--tlo);font-family:'Inter Tight',sans-serif}
.w{position:absolute;inset:0;overflow:hidden}

/* --- tła --- */
.tlo{position:absolute;inset:0}
.tlo.ciemne{background:radial-gradient(1250px 950px at var(--px) var(--py),#34363d 0%%,#1b1c20 42%%,#0f1012 78%%)}
.tlo.akcent{background:radial-gradient(1300px 1000px at var(--px) var(--py),var(--akcent2) 0%%,var(--akcent) 45%%,var(--akcent-ciemny) 100%%)}
.tlo img{position:absolute;max-width:none}
.tlo.kadr img{filter:blur(var(--rozmycie,13px)) brightness(var(--jasnosc,.62)) saturate(.95)}
.tlo.obraz img{width:100%%;height:100%%;object-fit:cover;filter:blur(var(--rozmycie,0px)) brightness(var(--jasnosc,.75))}
.zaslona{position:absolute;inset:0}
.zaslona.lewa{background:linear-gradient(90deg,rgba(15,16,18,.94) 0%%,rgba(15,16,18,.78) 34%%,rgba(15,16,18,0) 64%%)}
.zaslona.prawa{background:linear-gradient(270deg,rgba(15,16,18,.94) 0%%,rgba(15,16,18,.78) 34%%,rgba(15,16,18,0) 64%%)}
.zaslona.dol{background:linear-gradient(0deg,rgba(15,16,18,.9) 0%%,rgba(15,16,18,0) 30%%)}
.winieta{position:absolute;inset:0;background:radial-gradient(ellipse at 50%% 45%%,rgba(0,0,0,0) 55%%,rgba(0,0,0,.42) 100%%)}

/* --- poświata i dekoracje marki --- */
.poswiata{position:absolute;width:1100px;height:1100px;border-radius:50%%;transform:translate(-50%%,-50%%);
  background:radial-gradient(circle,rgba(var(--akcent-rgb),.5) 0%%,rgba(var(--akcent-rgb),.16) 38%%,rgba(var(--akcent-rgb),0) 68%%)}
.kw{position:absolute;border-radius:14%%}
.kw.pelny{background:linear-gradient(180deg,var(--akcent2),var(--akcent));box-shadow:0 0 60px rgba(var(--akcent-rgb),.45)}
.kw.obrys{border:7px solid var(--akcent)}
.tlo.akcent ~ .kw.pelny{background:#0f1012;box-shadow:none}
.tlo.akcent ~ .kw.obrys{border-color:#0f1012}

/* --- postać --- */
.postac{position:absolute;max-width:none}
.postac.lustro{transform:scaleX(-1)}

/* --- tekst --- */
.tekst{position:absolute;display:flex;flex-direction:column;align-items:flex-start;gap:6px;
  filter:drop-shadow(0 8px 26px rgba(0,0,0,.5))}
.tekst.do-prawej{align-items:flex-end}
.tekst.srodek{align-items:center}
.linia{display:block;white-space:nowrap;font-weight:900;line-height:.96;letter-spacing:-.022em;text-transform:uppercase;color:#fff}
.linia.akcent{background:linear-gradient(180deg,var(--akcent2) 10%%,var(--akcent) 85%%);-webkit-background-clip:text;background-clip:text;color:transparent}
.linia.ciemny{color:#0f1012}
.linia.zielony{color:var(--zielony)}
.linia.klocek{background:linear-gradient(180deg,var(--akcent2),var(--akcent));color:#0f1012;padding:.04em .16em .07em;border-radius:.09em;
  transform:rotate(-2deg);margin:.06em 0}
.linia.klocek-ciemny{background:#0f1012;color:#fff;padding:.04em .16em .07em;border-radius:.09em;transform:rotate(-2deg);margin:.06em 0}
.linia.klocek-bialy{background:#fff;color:#0f1012;padding:.04em .16em .07em;border-radius:.09em;transform:rotate(-2deg);margin:.06em 0}
.linia.maly{font-weight:800;letter-spacing:.02em;color:var(--szary)}
.linia.skreslony{color:#8d9098;text-decoration:line-through;text-decoration-color:var(--akcent);text-decoration-thickness:.09em}
.tekst.bez-cienia{filter:none}
.tekst.na-akcencie{filter:drop-shadow(0 10px 22px rgba(var(--cien-rgb),.32))}

/* --- dodatki --- */
.dod{position:absolute}
.pigulka{display:inline-flex;align-items:center;gap:16px;background:rgba(15,16,18,.88);border:2px solid rgba(255,255,255,.16);
  color:#fff;font-weight:800;font-size:44px;line-height:1;padding:18px 30px;border-radius:999px;white-space:nowrap}
.pigulka i{width:22px;height:22px;border-radius:50%%;background:var(--akcent);display:block;box-shadow:0 0 22px rgba(var(--akcent-rgb),.8)}
.pigulka.zielona i{background:var(--zielony);box-shadow:0 0 22px rgba(var(--akcent-rgb),.8)}
.awatary{display:flex}
.awatary .a{border-radius:50%%;border:6px solid var(--akcent);background:#1b1c20 center/cover;box-shadow:0 12px 34px rgba(0,0,0,.55)}
.awatary.kafle{gap:18px}
.awatary.kafle .a{border-radius:22%%}
.obrazek{display:block;max-width:none}
.obrazek.karta{border-radius:26px;box-shadow:0 22px 70px rgba(0,0,0,.6);border:2px solid rgba(255,255,255,.14)}

/* --- strefy pomocnicze (--strefy) --- */
.strefa{position:absolute;border:3px dashed rgba(0,255,200,.9);color:rgba(0,255,200,.95);font:700 22px 'Inter Tight';padding:6px}
"""

FILTRY_SVG = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="obrys-bialy" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>
<feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="obrys-akcent" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>
<feFlood flood-color="{akcent}"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs></svg>""".replace("{akcent}", AKCENT)

# Dopasowanie rozmiaru każdej linii do szerokości kolumny (krótsza linia wychodzi większa).
SKRYPT = """<script>
document.fonts.ready.then(function(){
  document.querySelectorAll('[data-dopasuj]').forEach(function(el){
    var szer=+el.dataset.szer, max=+el.dataset.max, lo=20, hi=max;
    for(var i=0;i<14;i++){var m=(lo+hi)/2; el.style.fontSize=m+'px'; if(el.getBoundingClientRect().width<=szer*1.0+0.5&&el.offsetWidth<=szer){lo=m}else{hi=m}}
    el.style.fontSize=Math.floor(lo)+'px';
  });
});
</script>"""


def adres(p):
    return (TU / p).resolve().as_uri()


def uloz_postac(w):
    """Skala i położenie wycięcia tak, by twarz trafiła w zadane miejsce i miała zadaną wysokość."""
    info = json.loads((TU / w["postac"]).with_suffix(".json").read_text(encoding="utf-8"))
    k, t = info["kadr"], info["twarz"]
    s = w["twarz"]["wys"] * H / t["h"]
    fx = t["x"] + t["w"] / 2
    if w.get("lustro"):
        fx = k["w"] - fx
    lewo = w["twarz"]["x"] * W - fx * s
    gora = w["twarz"]["y"] * H - (t["y"] + t["h"] / 2) * s
    uklad = {"s": s, "lewo": lewo, "gora": gora, "szer": k["w"] * s, "wys": k["h"] * s, "info": info}
    uwagi = []
    if gora + k["h"] * s < H - 2 and info["kadr"]["y"] + info["kadr"]["h"] >= info["zrodlo"]["h"] - 30:
        uwagi.append("postać kończy się %d px nad dolną krawędzią (widać ucięcie kadru): zwiększ twarz.wys albo twarz.y"
                     % (H - gora - k["h"] * s))
    if s > 1.25:
        uwagi.append("postać powiększona %.2f× względem źródła: może wyjść miękko, weź ciaśniejszy kadr albo mniejszą twarz" % s)
    return uklad, uwagi


def html_tla(w, u):
    t = w.get("tlo", {"typ": "ciemne"})
    typ = t.get("typ", "ciemne")
    px, py = "%.0fpx" % (w["twarz"]["x"] * W), "%.0fpx" % (w["twarz"]["y"] * H)
    zm = "--px:%s;--py:%s;" % (px, py)
    if "rozmycie" in t:
        zm += "--rozmycie:%spx;" % t["rozmycie"]
    if "jasnosc" in t:
        zm += "--jasnosc:%s;" % t["jasnosc"]
    cz = []
    if typ == "kadr":
        # Ta sama klatka co postać, wyrównana piksel w piksel: wygląda jak prawdziwy pokój z małą głębią ostrości.
        zr, k = u["info"]["zrodlo"], u["info"]["kadr"]
        s = u["s"]
        if w.get("lustro"):
            lewo = u["lewo"] - (zr["w"] - k["x"] - k["w"]) * s
            styl = "left:%.1fpx;top:%.1fpx;width:%.1fpx;transform:scaleX(-1)" % (lewo, u["gora"] - k["y"] * s, zr["w"] * s)
        else:
            styl = "left:%.1fpx;top:%.1fpx;width:%.1fpx" % (u["lewo"] - k["x"] * s, u["gora"] - k["y"] * s, zr["w"] * s)
        # Pod spodem to samo zdjęcie na cały kadr, na wypadek gdyby wyrównana klatka nie zakryła brzegów.
        cz.append('<div class="tlo obraz" style="%s--rozmycie:40px;--jasnosc:.35"><img src="%s"></div>' % (zm, adres(t["klatka"])))
        cz.append('<div class="tlo kadr" style="%s"><img src="%s" style="%s"></div>' % (zm, adres(t["klatka"]), styl))
    elif typ == "obraz":
        cz.append('<div class="tlo obraz" style="%s"><img src="%s"></div>' % (zm, adres(t["plik"])))
    else:
        cz.append('<div class="tlo %s" style="%s"></div>' % (typ, zm))
    for z in t.get("zaslony", []):
        cz.append('<div class="zaslona %s"></div>' % z)
    if t.get("winieta", typ != "akcent"):
        cz.append('<div class="winieta"></div>')
    if t.get("poswiata", typ == "ciemne"):
        cz.append('<div class="poswiata" style="left:%s;top:%s"></div>' % (px, "%.0fpx" % (w["twarz"]["y"] * H + 60)))
    for kw in t.get("kwadraty", []):
        # (x, y, bok, obrót w stopniach, "pelny" | "obrys")
        x, y, bok, obr, rodzaj = kw
        cz.append('<div class="kw %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;transform:rotate(%sdeg)"></div>' % (rodzaj, x, y, bok, bok, obr))
    return "\n".join(cz)


def html_tekstu(w):
    t = w.get("tekst")
    if not t:
        return ""
    klasy = "tekst " + t.get("wyrownanie", "")
    if w.get("tlo", {}).get("typ") == "akcent":
        klasy += " na-akcencie"
    poz = "left:%dpx;width:%dpx;" % (t["x"], t["szer"])
    poz += ("bottom:%dpx;" % (H - t["dol"])) if "dol" in t else ("top:%dpx;" % t["y"])
    linie = []
    for l in t["linie"]:
        tekst, styl = l[0], l[1]
        rozmiar = l[2] if len(l) > 2 else None
        if rozmiar:
            linie.append('<div class="linia %s" style="font-size:%dpx">%s</div>' % (styl, rozmiar, html.escape(tekst)))
        else:
            linie.append('<div class="linia %s" data-dopasuj data-szer="%d" data-max="%d">%s</div>'
                         % (styl, t["szer"], t.get("max", 300), html.escape(tekst)))
    return '<div class="%s" style="%s">%s</div>' % (klasy, poz, "".join(linie))


def html_dodatku(d):
    rodzaj = d["rodzaj"]
    obr = "transform:rotate(%sdeg);" % d["obrot"] if d.get("obrot") else ""
    poz = "left:%dpx;top:%dpx;%s" % (d["x"], d["y"], obr)
    if rodzaj == "pigulka":
        kolor = " zielona" if d.get("kolor") == "zielony" else ""
        rozm = "font-size:%dpx;" % d["rozmiar"] if d.get("rozmiar") else ""
        return '<div class="dod" style="%s"><div class="pigulka%s" style="%s"><i></i>%s</div></div>' % (poz, kolor, rozm, html.escape(d["tekst"]))
    if rodzaj == "awatary":
        bok = d.get("bok", 150)
        zachodzenie = d.get("zachodzenie", 0.22)
        kafle = d.get("ksztalt") == "kafle"
        el = []
        for i, p in enumerate(d["pliki"]):
            ml = 0 if (i == 0 or kafle) else -bok * zachodzenie
            el.append('<div class="a" style="width:%dpx;height:%dpx;margin-left:%dpx;background-image:url(\'%s\')"></div>' % (bok, bok, ml, adres(p)))
        return '<div class="dod awatary%s" style="%s">%s</div>' % (" kafle" if kafle else "", poz, "".join(el))
    if rodzaj == "obraz":
        karta = " karta" if d.get("karta") else ""
        cien = "" if d.get("karta") or d.get("bez_cienia") else "filter:drop-shadow(0 20px 50px rgba(0,0,0,.55));"
        return '<img class="dod obrazek%s" src="%s" style="%swidth:%dpx;%s">' % (karta, adres(d["plik"]), poz, d["szer"], cien)
    if rodzaj == "strzalka":
        # Łuk od (x, y) do (x2, y2); `wygiecie` przesuwa środek łuku w bok (dodatnie = w prawo od kierunku).
        x1, y1, x2, y2 = d["x"], d["y"], d["x2"], d["y2"]
        wyg = d.get("wygiecie", 0.25)
        mx, my = (x1 + x2) / 2 - (y2 - y1) * wyg, (y1 + y2) / 2 + (x2 - x1) * wyg
        kolor = d.get("kolor", AKCENT)
        gr = d.get("grubosc", 16)
        return ('<svg class="dod" style="left:0;top:0" width="%d" height="%d" viewBox="0 0 %d %d"><defs>'
                '<marker id="g%d" markerWidth="5" markerHeight="5" refX="2.6" refY="2.5" orient="auto"><path d="M0,0 L5,2.5 L0,5 Z" fill="%s"/></marker></defs>'
                '<path d="M%d,%d Q%.0f,%.0f %d,%d" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" marker-end="url(#g%d)" '
                'style="filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))"/></svg>'
                % (W, H, W, H, x1, kolor, x1, y1, mx, my, x2, y2, kolor, gr, x1))
    if rodzaj == "znak":
        # Okrągły znaczek: "x" (nie) albo "ptaszek" (tak). Rysowany wektorowo, więc nie zależy od czcionki.
        bok = d.get("bok", 150)
        tla = {"ciemny": "#0f1012", "akcent": AKCENT, "zielony": AKCENT, "bialy": "#ffffff"}  # "zielony" = akcent (stare układy)
        tlo = tla[d.get("kolor", "zielony" if d.get("symbol") == "ptaszek" else "ciemny")]
        kreska = "#0f1012" if tlo in (AKCENT, "#ffffff") else "#ffffff"
        sciezka = "M30,52 L45,67 L72,36" if d.get("symbol") == "ptaszek" else "M33,33 L67,67 M67,33 L33,67"
        return ('<svg class="dod" style="%sfilter:drop-shadow(0 12px 26px rgba(0,0,0,.45))" width="%d" height="%d" viewBox="0 0 100 100">'
                '<circle cx="50" cy="50" r="46" fill="%s" stroke="rgba(255,255,255,.9)" stroke-width="5"/>'
                '<path d="%s" fill="none" stroke="%s" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                % (poz, bok, bok, tlo, sciezka, kreska))
    if rodzaj == "html":
        return '<div class="dod" style="%s">%s</div>' % (poz, d["html"])
    raise SystemExit("Nieznany dodatek: %s" % rodzaj)


def zbuduj(w, strefy=False):
    u, uwagi = uloz_postac(w)
    k = u["info"]["kadr"]
    # Przelicznik z pikseli klatki (linijki na postac_podglad.jpg) na kadr miniatury: do stawiania dodatków
    # przy dłoni albo przy twarzy.
    def ze_znakiem(v):
        return "%s %.0f" % ("+" if v >= 0 else "−", abs(v))

    if w.get("lustro"):
        wzor = "x = %.0f − (X − %d) × %.3f" % (u["lewo"] + k["w"] * u["s"], k["x"], u["s"])
    else:
        wzor = "x = (X − %d) × %.3f %s" % (k["x"], u["s"], ze_znakiem(u["lewo"]))
    uwagi.insert(0, "postać w skali %.3f; punkt klatki (X, Y) leży na kadrze w %s, y = (Y − %d) × %.3f %s"
                 % (u["s"], wzor, k["y"], u["s"], ze_znakiem(u["gora"])))
    typ_tla = w.get("tlo", {}).get("typ", "ciemne")
    klasy = "postac" + (" lustro" if w.get("lustro") else "")
    # Filtr postaci: lekka korekta, opcjonalny obrys, światło kontrowe odcinające od tła, cień.
    filtr = ["contrast(1.06) saturate(1.1) brightness(%s)" % w.get("jasnosc_postaci", 1.05)]
    if w.get("obrys"):
        filtr.append("url(#obrys-%s)" % w["obrys"])
    swiatlo = w.get("swiatlo", "akcent" if typ_tla == "ciemne" else ("ciemne" if typ_tla == "akcent" else "brak"))
    if swiatlo == "akcent":
        filtr.append("drop-shadow(0 0 4px rgba(%(akcent2_rgb)s,.5)) drop-shadow(0 0 46px rgba(%(akcent_rgb)s,.42))" % paleta())
    elif swiatlo == "biale":
        filtr.append("drop-shadow(0 0 4px rgba(255,255,255,.5)) drop-shadow(0 0 40px rgba(255,255,255,.28))")
    elif swiatlo == "ciemne":
        filtr.append("drop-shadow(0 0 3px rgba(%(cien_rgb)s,.5)) drop-shadow(0 18px 50px rgba(%(cien_rgb)s,.55))" % paleta())
    if swiatlo != "ciemne":
        filtr.append("drop-shadow(0 26px 60px rgba(0,0,0,.6))")
    postac = '<img class="%s" src="%s" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;filter:%s">' % (
        klasy, adres(w["postac"]), u["lewo"], u["gora"], u["szer"], " ".join(filtr))
    przed = [html_dodatku(d) for d in w.get("dodatki", []) if not d.get("za_postacia")]
    za = [html_dodatku(d) for d in w.get("dodatki", []) if d.get("za_postacia")]
    tekst = html_tekstu(w)
    tekst_za = w.get("tekst", {}).get("za_postacia")
    dol = '<div class="zaslona dol"></div>' if w.get("zaslona_dol") else ""
    siatka = ""
    if strefy:
        siatka = ('<div class="strefa" style="right:0;bottom:0;width:270px;height:130px">znacznik czasu</div>'
                  '<div class="strefa" style="left:60px;top:50px;right:60px;bottom:50px;border-color:rgba(255,255,255,.5);color:#fff">margines</div>')
    cialo = "\n".join([html_tla(w, u), "\n".join(za), tekst if tekst_za else "", postac, dol, "" if tekst_za else tekst, "\n".join(przed), siatka])
    strona = '<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s<div class="w">%s</div>%s</body></html>' % (
        html.escape("%s — miniatura %s" % (TYTUL, w["id"])), CSS % dict(paleta(), czcionka=CZCIONKA.resolve().as_uri()), FILTRY_SVG, cialo, SKRYPT)
    return strona, uwagi


def opis_testu():
    """Krótka ściąga do testu A/B: co sprawdza każdy wariant i jak puścić test w YouTube Studio."""
    linie = ["%s: miniatury do testu A/B" % TYTUL, ""]
    for w in WARIANTY:
        linie.append("Wariant %s: %s" % (w["id"], w.get("hipoteza", "")))
        napisy = [l[0] for l in w.get("tekst", {}).get("linie", [])] + list(w.get("tekst_dodatkowy", []))
        if napisy:
            linie.append("  napis na miniaturze: %s" % " / ".join(napisy))
        for i, tyt in enumerate(w.get("tytuly", []), 1):
            linie.append("  tytuł %d: %s" % (i, tyt))
        if len(w.get("tytuly", [])) != 2:
            linie.append("  tytuł: BRAK, do każdej miniatury mają być 2 propozycje (pole tytuly)")
        kl = (TU / w["postac"]).with_name("klatka.json")
        if kl.exists():
            t = json.loads(kl.read_text(encoding="utf-8"))["t"]
            linie.append("  klatka: %d:%04.1f surowego nagrania" % (t // 60, t % 60))
        if w.get("uwaga"):
            linie.append("  uwaga: %s" % w["uwaga"])
        linie.append("")
    linie += [
        "Jak puścić test (YouTube Studio na komputerze, w telefonie tej funkcji nie ma):",
        "1. Treści → kliknij film → w polu Tytuł albo pod miniaturą wybierz A/B Testing → typ testu „tytuł i miniatura”",
        "   (w angielskim interfejsie „Title and thumbnail”).",
        "2. Wgraj do trzech par w kolejności %s: miniatura i jeden z jej dwóch tytułów (wybierz wyżej)." % ", ".join(w["id"] for w in WARIANTY),
        "   Pierwsza para zostaje domyślna, gdy test nie wyłoni zwycięzcy.",
        "3. W trakcie testu nie zmieniaj tytułu ani miniatury, bo to go zatrzymuje.",
        "4. Wynik przychodzi po kilku dniach, najpóźniej po 2 tygodniach. Wygrywa para z największym",
        "   udziałem czasu oglądania, a nie z najwyższym CTR. Wynik mówi, która para wygrała, a nie czy",
        "   zadziałała miniatura, czy tytuł.",
        "",
        "Po teście: Statystyki → Zasięg → „Zarządzaj testem”. Zrób zrzut wyniku i wrzuć go do rozmowy,",
        "żeby wynik trafił do dziennika skilla i kolejne miniatury korzystały z tego, co zadziałało.",
    ]
    plik = TU / ("test_AB%s.txt" % PRZYROSTEK)
    plik.write_text("\n".join(linie) + "\n", encoding="utf-8")
    return plik


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strefy = "--strefy" in sys.argv
    wybrane = [w for w in WARIANTY if not args or w["id"] in args]
    if not wybrane:
        raise SystemExit("Nie ma wariantu: %s" % ", ".join(args))
    for w in wybrane:
        strona, uwagi = zbuduj(w, strefy)
        # Wersja ze strefami idzie do osobnych plików, żeby nie nadpisać gotowej miniatury.
        plik = TU / ("%s%s.html" % (w["id"], "_strefy" if strefy else ""))
        plik.write_text(strona, encoding="utf-8")
        print("[%s] %s" % (w["id"], uwagi[0]))
        for uw in uwagi[1:]:
            print("[%s] uwaga: %s" % (w["id"], uw))
        r = subprocess.run([sys.executable, str(MINI), "render", str(plik)], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(r.stdout + r.stderr)
        print("[%s] %s" % (w["id"], plik.with_suffix(".jpg")))
        if not strefy:
            (TU / ("%s.json" % w["id"])).write_text(json.dumps(
                {"id": w["id"], "hipoteza": w.get("hipoteza", ""),
                 "tekst": [l[0] for l in w.get("tekst", {}).get("linie", [])],
                 "tekst_dodatkowy": list(w.get("tekst_dodatkowy", [])), "tytuly": list(w.get("tytuly", [])),
                 "postac": w["postac"]},
                ensure_ascii=False, indent=1), encoding="utf-8")
    if strefy:
        print("Pliki *_strefy.jpg są tylko do podglądu stref; gotowych miniatur nie ruszyłem.")
        return
    wszystkie = [str(TU / ("%s.jpg" % w["id"])) for w in WARIANTY if (TU / ("%s.jpg" % w["id"])).exists()]
    r = subprocess.run([sys.executable, str(MINI), "kontrola"] + wszystkie
                       + ["--tytul", TYTUL_YT or TYTUL, "--czas", CZAS, "--wyj", str(TU / ("podglad%s.jpg" % PRZYROSTEK))],
                       capture_output=True, text=True)
    print(r.stdout + r.stderr)
    print("Opis testu A/B: %s" % opis_testu())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Kompozycja rolki "Szczęście, plan czy głód" (IMG_0591) w dwoch trybach:
  python3 -I kompozycja.py efekty  -> ../hf/index.html   hook z duzymi haslami nad glowa, macierz 2x2, karty z liczbami,
                                      szablon z biblioteki, rozne przejscia plansz, efekty dzwiekowe, plansza koncowa
  python3 -I kompozycja.py napisy  -> ../hfn/index.html  tylko ciecia i napisy slowo po slowie, bez grafik i dzwiekow
Hook (A albo B) rozpoznaje sie sam po pierwszym slowie nagrania. Dodatkowo ../napisy.srt.

Kadr jest niski (broda siega 72% wysokosci), wiec napisy stoja na 1420 px zamiast 1120, a nakladki ida w pusta
przestrzen nad glowa (sufit), gdzie niczego nie zaslaniaja.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Glos w rolce: naturalny dzwiek z mikrofonu po lekkim masteringu z aroll.py (highpass 70 Hz, kompresja 2,5:1, -14 LUFS).
# Jakub 17.11.2026: "za bardzo uzywasz voice enhancer AI, kupilem dobre mikrofony, bez tego albo z duzo mniejszym filtrem".
# Wariant C (Sidon + lancuch radiowy, skrypty/studio.py) zostaje tylko na zyczenie: GLOS = P / "audio/aroll_studio_gleboki.wav".
# Wideo A-rollu idzie bez dzwieku, glos jako osobna sciezka <audio> (ta sama os czasu co aroll.wav).
GLOS = P / "audio/aroll.wav"
# Dwie palety, ten sam uklad i ruch. MARKA wybiera, w ktorej jest caly film:
#   "personal" - personal brand Jakuba (rolki, long-form, rolki promo): czern, biel, ciemny szary + akcent #00E5A0
#   "adgen"    - reklamy adGen (Eksporty/Reklamy adGen): akcent pomaranczowy #ff7018, jak w IMG_0361 / IMG_0526
# accent    - kolor akcentu; inny akcent pod temat filmu (tylko "personal") = zmiana tej jednej wartosci
# on_accent - tekst i ikony NA akcencie (bialy na #00E5A0 ma kontrast 1,6:1, wiec tam ciemny; na pomaranczu bialy)
# ok        - kolor "zrobione" (ptaszki, pigulka potwierdzenia); None = akcent
PALETY = {
    "personal": {"accent": "#00E5A0", "on_accent": "#0f1012", "ok": None},
    "adgen": {"accent": "#ff7018", "on_accent": "#ffffff", "ok": "#3ddc84"},
}
MARKA = "personal"
TRYB = sys.argv[1] if len(sys.argv) > 1 else "efekty"
assert TRYB in ("efekty", "napisy"), TRYB

ICON = {
    "kanban": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 7v7"/><path d="M12 7v4"/><path d="M16 7v9"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22 11 13 2 9z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "palm": '<path d="M13 8c0-2.76-2.46-5-5.5-5S2 5.24 2 8h2l1-1 1 1h4"/><path d="M13 7.14A5.82 5.82 0 0 1 16.5 6c3.04 0 5.5 2.24 5.5 5h-3l-1-1-1 1h-3"/><path d="M5.89 9.71c-2.15 2.15-2.3 5.47-.35 7.43l4.24-4.25.7-.7.71-.71 2.12-2.12c-1.95-1.96-5.27-1.8-7.42.35"/><path d="M11 15.5c.5 2.5-.17 4.5-1 6.5h4c2-5.5-.5-12-1-14"/>',
    "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
    "up": '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "cog": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}


def icon(name, size, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


def kolory(page, marka=None):
    """Wstawia palete do szablonu: akcent, {{ACCENT_RGB}} (pod rgba), {{ACCENT_HI}} (jasny koniec gradientu),
    kolor tekstu na akcencie i kolor "zrobione". Reszta CSS korzysta tylko ze zmiennych, bez kolorow na sztywno."""
    p = PALETY[marka or MARKA]

    def rgb(h):
        h = h.lstrip("#")
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

    acc, ok = rgb(p["accent"]), rgb(p["ok"] or p["accent"])
    hi = "#%02x%02x%02x" % tuple(round(c + (255 - c) * 0.35) for c in acc)
    for key, val in (("ACCENT_RGB", ",".join(map(str, acc))), ("ACCENT_HI", hi), ("ACCENT", p["accent"]),
                     ("ON_ACCENT", p["on_accent"]), ("OK_RGB", ",".join(map(str, ok))), ("OK", p["ok"] or p["accent"])):
        page = page.replace("{{" + key + "}}", val)
    return page

# ---------------------------------------------------------------- przejscia plansz i biblioteka grafik
# Przejscia plansz: kolejne plansze biora kolejne pozycje z PRZEJSCIA, wiec dwie pod rzad nigdy nie wchodza tak samo
# (Jakub po IMG_0576: "bardzo generyczne sa przejscia"). Wymuszenie konkretnego: panel(..., wejscie="iris").
# Wartosci w px, nie w %: render zaokragla liczby do calosci, a 1% kadru to 19 px skoku.
# Krotka: (stan poczatkowy, stan otwarty, czas wejscia, ease, stan wyjscia, czas wyjscia, ease, czy z light leakiem).
PRZEJSCIA = ["iris", "wipe", "zoom", "diag", "slide", "blur"]
RUCH = {
    "blur": ('{opacity:0,scale:1.06,filter:"blur(18px)"}', '{opacity:1,scale:1,filter:"blur(0px)"', 0.32, "power3.out",
             '{opacity:0,scale:1.04,filter:"blur(14px)"', 0.18, "power2.in", True),
    "iris": ('{clipPath:"circle(0px at 540px 760px)"}', '{clipPath:"circle(2300px at 540px 760px)"', 0.55, "power3.out",
             '{clipPath:"circle(0px at 540px 760px)"', 0.26, "power3.in", False),
    "wipe": ('{clipPath:"inset(1920px 0px 0px 0px)"}', '{clipPath:"inset(0px 0px 0px 0px)"', 0.45, "expo.out",
             '{clipPath:"inset(0px 0px 1920px 0px)"', 0.24, "power3.in", False),
    "zoom": ('{opacity:0,scale:0.35,filter:"blur(14px)",transformOrigin:"50% 40%"}', '{opacity:1,scale:1,filter:"blur(0px)"', 0.42, "expo.out",
             '{opacity:0,scale:1.9,filter:"blur(12px)"', 0.22, "power3.in", False),
    "diag": ('{clipPath:"polygon(0px 0px, 0px 0px, -400px 1920px, -400px 1920px)"}',
             '{clipPath:"polygon(0px 0px, 1480px 0px, 1080px 1920px, -400px 1920px)"', 0.5, "expo.out",
             '{clipPath:"polygon(1480px 0px, 1480px 0px, 1080px 1920px, 1080px 1920px)"', 0.26, "power3.in", False),
    "slide": ('{y:1920}', '{y:0', 0.5, "expo.out", '{y:-1920', 0.26, "power3.in", False),
}
_uzyte_przejscia = []

# Subtelne efekty dzwiekowe pod animacje (Jakub, 17.11.2026). False = film bez efektow.
SFX = True

# Biblioteka gotowych grafik z katalogu HyperFrames (opis i arkusze: references/biblioteka.md).
BIBLIOTEKA = Path.home() / ".claude/skills/montaz-rolek/biblioteka"


def mount(el, mid, nazwa, t_in, dur, zmienne=None, track=6, styl="left:0;top:0;width:1080px;height:1920px"):
    """Montuje szablon z biblioteki jako pod-kompozycje: kopiuje jego plik (i zasoby blokow) do hf/ i dopisuje element
    z wartosciami zmiennych. Kolory bierze z tokenow --brand/--bg/--fg/--surface w :root szablonu, czyli z palety marki.
    Dziala dla pozycji oznaczonych w biblioteka.md jako "montowalne"; "wycinki" wkleja sie recznie."""
    src = next(BIBLIOTEKA.glob(f"compositions/**/{nazwa}.html"))
    rel = src.relative_to(BIBLIOTEKA)
    dst = P / "hf" / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if "components" not in rel.parts:  # bloki maja wlasne zasoby (zdjecia, czcionki)
        shutil.copytree(BIBLIOTEKA / "assets", P / "hf/assets", dirs_exist_ok=True)
    vals = json.dumps(zmienne or {}, ensure_ascii=False).replace("&", "&amp;").replace("'", "&#39;")
    el.append(f'<div id="{mid}" class="clip" style="position:absolute;{styl}" data-composition-id="{mid}" data-composition-src="{rel}" '
              f"data-start=\"{t_in:.3f}\" data-duration=\"{dur:.3f}\" data-track-index=\"{track}\" data-variable-values='{vals}'></div>")



def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


# poprawki transkrypcji (whisper -> tekst napisow); uzupelniane po pierwszym przebiegu slowa.py
FIX = {"niepewną,": "niepewna,", "naprawę": "naprawdę"}

# Frazy napisow. *slowa* = wyroznienie akcentem. Tekst brany stad, czasy z transkrypcji.
FR_HOOK_A = ["Według Petera Thiela", "*Europa* siedzi", "w *najgorszej ćwiartce*", "sukcesu,", "no i *Ty* w sumie", "razem z nią."]
FR_Q1 = ["Warren *Buffett*", "uważa siebie za członka", "Klubu *Szczęśliwej Spermy.*", "Jeff *Bezos* przypisuje", "sukces Amazona",
         "niezwykłemu ustawieniu", "się *planet.*"]
FR_Q2 = ["A Bill *Gates*", "posuwa się tak daleko,", "że twierdzi, iż miał", "*szczęście* urodzić się", "z pewnymi umiejętnościami."]
FR_BODY = [
    "Coś takiego możemy", "przeczytać w *Zero to One*", "od Petera Thiela,",
    "gdzie autor pyta:", "sukces to *szczęście*", "czy *umiejętności?*",
    "Ale Thiel uważa", "skrajnie *inaczej.*",
    "Nie jesteś", "*losem na loterii.*",
    "*Dwie osie.*", "Masz *plan* albo nie.", "Wierzysz, że Ci się uda,", "albo nie.",
    "USA w latach", "50. i 60.:", "totalny *optymizm.*",
    "*32 tysiące* kilometrów", "gotowych dróg", "wybudowali w niespełna", "*9 lat,*", "a jeśli chodzi", "o lot na *Księżyc,*",
    "to tak naprawdę", "zaplanowali go w *61,*",
    "a do końca *'72*", "wylądowało na nim", "aż *12 osób.*",
    "A co potem?", "Od lat *80.*", "aż do dziś", "to jest totalny optymizm,", "ale kompletnie *bez planu.*",
    "Za to *Chiny* dzisiaj", "są w tej zdefiniowanej", "ćwiartce *pesymistów,*", "gdzie wiedzą,", "że przyszłość może być", "bardzo niepewna,",
    "*Europa,* no…", "co ja mogę rzec?", "*Ani planu,* ani wiary.", "Klasycznie.",
    "Moim zdaniem", "nie ma kompletnie znaczenia,", "czy jesteś optymistą,", "czy pesymistą.", "Liczy się *plan.*",
    "Ale plan to", "*jedna połowa.*",
    "Druga połowa,", "z którą ja się", "bardzo mocno utożsamiam,", "jest *palące pragnienie,*", "o którym zawsze pisał", "*Napoleon Hill.*",
    "Ja od praktycznie", "szesnastego, siedemnastego", "roku życia już wiedziałem", "dokładnie, *czego chcę.*",
    "Chcę *wolność*", "i chcę *biznes online*", "i przez ostatnie", "*7, 8, 9 lat*", "cały czas do tego dążyłem.",
    "No i można powiedzieć,", "że jestem tu,", "gdzie jestem.",
    "A Ty co myślisz?", "*Szczęście,* *plan*", "czy *palące pragnienie?*",
    "Daj znać koniecznie", "*w komentarzu.*",
]



# ---------------------------------------------------------------- strefa bezpieczna (safe zone), kadr 1080x1920
# Czesc wspolna szablonow Instagram Reels i Jon Loomer (Jakub, 18.11.2026): y 270-1245, x 70-1010, od 860 px w dol prawa
# krawedz 885 px, od 1145 px 850 px. Opis: skill montaz-rolek, references/styl.md, punkt 8. Kontrola: skrypty/strefa.py.
SAFE = {"top": 270, "bottom": 1245, "left": 70, "right": 1010, "wciecia": [(860, 885), (1145, 850)]}
CAP_TOP = 1160  # niski kadr: broda siega do ok. 1200 px po podniesieniu kadru (aroll.py), napisy tuz pod nia; dol linii z "g" i "p" 1235 px
CAP_MIN = 52
STREFA = os.environ.get("STREFA") == "1"  # tryb kontrolny dla strefa.py: same grafiki na czarnym tle


def safe_right(y0, y1):
    return min([SAFE["right"]] + [x for y, x in SAFE["wciecia"] if y1 > y])


def safe_w(y0, y1, srodek=540):
    if y0 < SAFE["top"] or y1 > SAFE["bottom"]:
        raise SystemExit(f"Poza strefa bezpieczna: pas {y0}-{y1} px, dozwolone {SAFE['top']}-{SAFE['bottom']}")
    return int(2 * min(srodek - SAFE["left"], safe_right(y0, y1) - srodek))


CAP_W = safe_w(CAP_TOP, CAP_TOP + 73)  # 620 px
SCRIM = 0.44  # miekkie przyciemnienie pod napisami (biala koszulka i jasne dlonie), jak w IMG_0583 i IMG_0597
_okna_ruchu = []
STREFA_CSS = """
      #vwrap, .pbg, .leak, .scrim { display: none !important; }
      html, body, #root { background: #000 !important; }
      * { box-shadow: none !important; text-shadow: none !important; filter: none !important; }
"""


def rozbij(frazy, limit=21):
    """Dzieli frazy dluzsze niz `limit` znakow (bez gwiazdek) na dwie w najblizszej polowie granicy slow; wyroznienie
    *...* rozciagniete przez granice jest zamykane i otwierane na nowo."""
    out = []
    for fr in frazy:
        tok = fr.split()
        if len(fr.replace("*", "")) <= limit or len(tok) < 2:
            out.append(fr)
            continue
        plain = [t.replace("*", "") for t in tok]
        best, bd = 1, 10 ** 9
        for k in range(1, len(tok)):
            l1, l2 = len(" ".join(plain[:k])), len(" ".join(plain[k:]))
            d = abs(l1 - l2) + (50 if max(l1, l2) > limit + 3 else 0)
            if d < bd:
                best, bd = k, d
        a, b = tok[:best], tok[best:]
        inhl = False
        for t in a:
            if t.startswith("*"):
                inhl = True
            if "*" in t[1:]:
                inhl = False
        if inhl:
            a[-1] += "*"
            b[0] = "*" + b[0]
        out += [" ".join(a), " ".join(b)]
        if len(plain) > 0 and max(len(" ".join(plain[:best])), len(" ".join(plain[best:]))) > limit + 6:
            out[-2:] = [" ".join(a), " ".join(b)]
    return out


def load_words():
    return [[a, b, FIX.get(t, t)] for a, b, t in json.loads((P / "audio/slowa.json").read_text())]


def manual_group(ws, frazy):
    phrases, k = [], 0
    for ph in frazy:
        cur, inhl = [], False
        for tok in ph.split():
            start = tok.startswith("*")
            end = "*" in tok[1:]
            text = tok.replace("*", "")
            hl = inhl or start
            inhl = (inhl or start) and not end
            if k >= len(ws):
                raise SystemExit(f"Brak slow dla frazy: {ph}")
            if norm(ws[k][2]) != norm(text):
                raise SystemExit(f"Niezgodnosc: '{ws[k][2]}' vs '{text}' we frazie '{ph}' (t={ws[k][0]:.2f})")
            cur.append([ws[k][0], ws[k][1], text, hl])
            k += 1
        phrases.append(cur)
    if k != len(ws):
        raise SystemExit(f"Nieprzypisane slowa: {[w[2] for w in ws[k:]]}")
    return phrases


def span(w, cls="w", text=None):
    hl = " hl" if len(w) > 3 and w[3] else ""
    return f'<span class="{cls}{hl}">{html.escape(text if text is not None else w[2])}</span>'


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def grafiki(edl, total, end_card_in, hook_a, el, js, dzw, W, Ws, seg, panel, pop, fade, blur_in, overlay, tiles, chip):
    """Grafiki wersji "efekty". Kwestie: 0-1 hook (A: Europa + cytaty, B: cytaty + Gates), 2-20 wspolne body."""
    esc = html.escape
    ACC = PALETY[MARKA]["accent"]
    licz = [0]

    def beats(items, t_end):
        """Duze hasla nad glowa (pusty sufit): items = [(t, tekst, klasa, podpis, t_podpisu)], kazde trwa do nastepnego."""
        for k, (t0, txt, cls, sub, ts) in enumerate(items):
            t1 = items[k + 1][0] - 0.08 if k + 1 < len(items) else t_end
            bid = f"bt{licz[0]}"
            licz[0] += 1
            size = min(124, int(900 / (len(txt) * 0.62)))
            subh = f'<div class="bt-s" id="{bid}s">{esc(sub)}</div>' if sub else ""
            el.append(f'<div id="{bid}" class="bt clip" data-start="{t0 - 0.06:.3f}" data-duration="{t1 - t0 + 0.06:.3f}" data-track-index="3">'
                      f'<div class="bt-b {cls}" id="{bid}b" style="font-size:{size}px">{esc(txt)}</div>{subh}</div>')
            blur_in(f"#{bid}b", t0 - 0.05)
            if sub:
                fade(f"#{bid}s", ts - 0.05)
            dzw.append({"t": t0, "typ": "pop", "db": -1})

    # --- hook: hasla nad glowa (napisy ida normalnie na dole)
    if hook_a:
        beats([(Ws("Europa", 0), "EUROPA", "", None, 0), (Ws("najgorszej", 0), "NAJGORSZA ĆWIARTKA", "acc", None, 0),
               (Ws("Ty", 0), "I TY RAZEM Z NIĄ", "", None, 0)], seg(1)["t_in"] - 0.05)
    q1 = 1 if hook_a else 0
    cyt = [(Ws("Warren", q1), "BUFFETT", "", "„klub szczęśliwej spermy”", Ws("Klubu", q1)),
           (Ws("Jeff", q1), "BEZOS", "", "„niezwykłe ustawienie planet”", Ws("niezwykłemu", q1))]
    if not hook_a:
        cyt.append((Ws("Bill", 1), "GATES", "", "„szczęście urodzić się z umiejętnościami”", Ws("szczęście", 1)))
    beats(cyt, seg(2)["t_in"] - 0.05)

    # --- ksiazka (kwestia 2): chip z tytulem i autorem
    t = Ws("Zero", 2) - 0.1
    chip("bk", "file", "ZERO TO ONE", t, seg(3)["t_in"] - 0.02, ok="PETER THIEL", t_ok=Ws("Petera", 2) - 0.05, ok_dot=None)
    dzw.append({"t": t + 0.1, "typ": "pop", "db": -2})

    # --- pytanie (kwestia 3): szablon z biblioteki "kinetic-type-swap" - "Sukces to" + wymieniajace sie slowo
    t_s, t_e = Ws("sukces", 3) - 0.12, seg(4)["t_in"] + 0.9   # pytanie wisi jeszcze chwile na "Ale Thiel uważa", zeby dalo sie je przeczytac
    t_um = Ws("umiejętności", 3)
    mount(el, "kts", "kinetic-type-swap", t_s, t_e - t_s,
          {"prefix": "Sukces to", "options": "szczęście?,umiejętności?", "suffix": "", "cues": f"{t_um - t_s:.2f}", "accent": "green", "exit": "fade"},
          track=2, styl="left:0;top:0;width:1080px;height:1920px;z-index:10")
    dzw.append({"t": t_s + 0.12, "typ": "swoosh"})
    dzw.append({"t": t_um, "typ": "tik"})

    # --- cytat Thiela nad glowa (kwestia 5): "Nie jestes losem na loterii" z podkresleniem
    inner = ('<div class="qt-k">PETER THIEL</div><div class="qt-t">NIE JESTEŚ<br>'
             '<span class="qt-h">LOSEM NA LOTERII<i id="qtu"></i></span></div>')
    overlay("qt", Ws("Nie", 5) - 0.1, seg(6)["t_in"] - 0.02, inner, "qt")
    js.append(f'tl.fromTo("#qtu",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power3.out"}},{Ws("losem", 5):.3f});')
    dzw.append({"t": Ws("Nie", 5), "typ": "pop"})

    # --- macierz 2x2 (glowna grafika): osie plan x wiara, cwiartki zapalaja sie, gdy o nich mowi
    def macierz(p):
        cells = [("USA", "lata 50. i 60.", "plan + optymizm"), ("USA", "od lat 80.", "optymizm bez planu"),
                 ("CHINY", "dziś", "plan + pesymizm"), ("EUROPA", "dziś", "ani planu, ani wiary")]
        pos = [(80, 80), (520, 80), (80, 520), (520, 520)]
        h = ('<div class="p-head" style="top:285px">PLAN × WIARA</div><div class="mxw"><div class="mx" id="%smx">' % p
             + f'<div class="mx-c" id="{p}c0" style="left:80px">MA PLAN</div><div class="mx-c" id="{p}c1" style="left:520px">BEZ PLANU</div>'
             + f'<div class="mx-r" id="{p}r0" style="top:80px"><span>WIERZY</span></div><div class="mx-r" id="{p}r1" style="top:520px"><span>NIE WIERZY</span></div>')
        for k, ((a, b, c), (x, y)) in enumerate(zip(cells, pos)):
            h += (f'<div class="mx-q" id="{p}q{k}" style="left:{x}px;top:{y}px"><div class="mx-in" id="{p}i{k}">'
                  f'<b>{a}</b><i>{b}</i><span>{c}</span></div></div>')
        return h + "</div></div>"

    def zapal(p, k, t, kolor=None):
        kol = kolor or ACC
        js.append(f'tl.to("#{p}q{k}",{{backgroundColor:"{kol}",borderColor:"{kol}",duration:0.22,ease:"power2.out"}},{t:.3f});')
        js.append(f'tl.fromTo("#{p}q{k}",{{scale:1}},{{scale:1.06,duration:0.14,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{t:.3f});')
        js.append(f'tl.fromTo("#{p}i{k}",{{opacity:0,scale:0.8,color:"#0f1012"}},{{opacity:1,scale:1,color:"#0f1012",duration:0.3,ease:"back.out(1.8)"}},{t + 0.04:.3f});')
        dzw.append({"t": t, "typ": "pop"})

    def zgas(p, k, t):   # cwiartka juz omowiona: zostaje obrys w akcencie i bialy tekst
        js.append(f'tl.to("#{p}q{k}",{{backgroundColor:"#16171a",borderColor:"{ACC}",duration:0.3}},{t:.3f});')
        js.append(f'tl.to("#{p}i{k}",{{color:"#ffffff",duration:0.3}},{t:.3f});')

    t6 = Ws("Dwie", 6)
    panel("m1", t6, seg(8)["t_in"], macierz("m1"))
    for k in range(4):
        js.append(f'tl.fromTo("#m1q{k}",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t6 + 0.05 + k * 0.07:.3f});')
        js.append(f'gsap.set("#m1i{k}",{{opacity:0}});')
    t_pl = Ws("plan", 6)
    fade("#m1c0", t_pl - 0.05)
    fade("#m1c1", W("albo", t_pl)[0] - 0.05)
    t_wi = Ws("Wierzysz", 6)
    fade("#m1r0", t_wi - 0.05)
    fade("#m1r1", W("albo", t_wi)[0] - 0.05)
    dzw.append({"t": t_pl, "typ": "tik"})
    dzw.append({"t": t_wi, "typ": "tik"})
    zapal("m1", 0, Ws("USA", 7))

    t10 = seg(10)["t_in"]
    panel("m2", t10, seg(13)["t_in"], macierz("m2"))
    js.append(f'gsap.set("#m2q0",{{borderColor:"{ACC}"}});')
    js.append('gsap.set("#m2i1,#m2i2,#m2i3",{opacity:0});')
    zapal("m2", 1, Ws("lat", 10) - 0.05)
    zgas("m2", 1, seg(11)["t_in"] - 0.1)
    zapal("m2", 2, Ws("Chiny", 11))
    zgas("m2", 2, seg(12)["t_in"] - 0.1)
    zapal("m2", 3, Ws("Europa", 12), "#ffffff")
    js.append(f'tl.fromTo("#m2mx",{{x:0}},{{x:8,duration:0.05,ease:"sine.inOut",repeat:5,yoyo:true}},{Ws("Klasycznie", 12):.3f});')

    # --- dowody z lat 50. i 60. nad glowa (kwestie 8-9): licznik drog, potem os czasu lotu na Ksiezyc
    s8 = seg(8)
    t_rd = Ws("32", 8) - 0.1
    t_mn = W("lot", s8["t_in"])[0] - 0.15
    inner = ('<div class="st-n"><span id="rdn">32</span><em>tys. km</em></div>'
             '<div class="st-l" id="rdl">gotowych dróg w niespełna 9 lat</div>')
    overlay("rd", t_rd, t_mn - 0.06, inner, "stat")
    js.append(f'tl.fromTo("#rdn",{{textContent:0}},{{textContent:32,duration:0.9,snap:{{textContent:1}},ease:"power2.out"}},{t_rd + 0.12:.3f});')
    fade("#rdl", Ws("gotowych", 8) - 0.05)
    dzw.append({"t": t_rd + 0.12, "typ": "pop"})
    inner = ('<div class="st-k">LOT NA KSIĘŻYC</div><svg class="tlv" viewBox="0 0 860 170" width="860" height="170">'
             '<path class="tl-b" d="M70,84 H790"/><path class="tl-a" id="mnl" pathLength="1000" d="M70,84 H790"/>'
             '<circle id="mnh" class="hd-a" cx="70" cy="84" r="11"/>'
             '<circle id="mn0" cx="70" cy="84" r="14" fill="#fff"/><circle id="mn1" cx="790" cy="84" r="14" fill="var(--accent)"/>'
             '<text id="mny0" x="70" y="146" text-anchor="middle" font-size="40" font-weight="850" fill="#fff">1961</text>'
             '<text id="mnp" x="70" y="44" text-anchor="middle" font-size="28" font-weight="700" fill="#c9ccd3" letter-spacing="2">PLAN</text>'
             '<text id="mny1" x="790" y="146" text-anchor="middle" font-size="40" font-weight="850" fill="var(--accent)">1972</text>'
             '<text id="mno" x="826" y="44" text-anchor="end" font-size="30" font-weight="800" fill="#fff"><tspan id="mnc">12</tspan> osób na Księżycu</text></svg>')
    overlay("mn", t_mn, seg(10)["t_in"] - 0.02, inner, "stat")
    js.append('gsap.set("#mnh,#mn0,#mny0,#mnp,#mn1,#mny1,#mno",{opacity:0});')
    t61 = Ws("61", 8)
    js.append(f'tl.to("#mn0,#mny0,#mnp",{{opacity:1,duration:0.25,ease:"power2.out"}},{t61 - 0.05:.3f});')
    dzw.append({"t": t61, "typ": "tik"})
    t_l0 = seg(9)["t_in"] + 0.12
    t72 = Ws("72", 9)
    d_l = max(0.6, t72 + 0.35 - t_l0)
    js.append(f'tl.fromTo("#mnl",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:{d_l:.3f},ease:"power1.inOut"}},{t_l0:.3f});')
    js.append(f'tl.set("#mnh",{{opacity:1}},{t_l0:.3f});')
    js.append(f'tl.fromTo("#mnh",{{attr:{{cx:70}}}},{{attr:{{cx:790}},duration:{d_l:.3f},ease:"power1.inOut"}},{t_l0:.3f});')
    js.append(f'tl.to("#mnh",{{opacity:0,duration:0.1}},{t_l0 + d_l:.3f});')
    js.append(f'tl.to("#mn1,#mny1",{{opacity:1,duration:0.2}},{t_l0 + d_l - 0.05:.3f});')
    dzw.append({"t": t_l0, "typ": "shh", "dl": d_l})
    t12 = Ws("12", 9)
    js.append(f'tl.to("#mno",{{opacity:1,duration:0.2}},{t12 - 0.08:.3f});')
    js.append(f'tl.fromTo("#mnc",{{textContent:0}},{{textContent:12,duration:0.6,snap:{{textContent:1}},ease:"power2.out"}},{t12 - 0.05:.3f});')
    dzw.append({"t": t12, "typ": "pop"})

    # --- "nie ma znaczenia, czy optymista, czy pesymista. Liczy sie plan." (kwestia 13): pigulki nad glowa
    inner = ('<div class="pill off big" id="po">OPTYMISTA<span class="strike" id="pos"></span></div>'
             '<div class="pill off big" id="pp">PESYMISTA<span class="strike" id="pps"></span></div>'
             '<div class="pill ok big" id="pl2">LICZY SIĘ PLAN</div>')
    t_o = Ws("optymistą", 13)
    overlay("pls", t_o - 0.12, seg(14)["t_in"] - 0.02, inner, "pillcol")
    pop("#po", t_o - 0.06)
    pop("#pp", Ws("pesymistą", 13) - 0.06)
    t_li = Ws("Liczy", 13)
    js.append(f'tl.fromTo("#pos,#pps",{{scaleX:0}},{{scaleX:1,duration:0.28,ease:"power2.out",stagger:0.08}},{t_li - 0.1:.3f});')
    js.append(f'tl.to("#po,#pp",{{opacity:0.55,duration:0.3}},{t_li + 0.1:.3f});')
    t_p = W("plan", t_li)[0]
    pop("#pl2", t_p - 0.06)
    dzw.append({"t": t_li, "typ": "tik"})
    dzw.append({"t": t_p, "typ": "pop"})

    # --- dwie polowy (kwestie 14-15): pierscien, polowa "plan", druga polowa "palace pragnienie"
    inner = ('<div class="p-head" style="top:285px">DWIE POŁOWY</div>'
             '<svg class="rg" viewBox="0 0 620 620" ><circle cx="310" cy="310" r="250" class="rg-b"/>'
             '<path id="rg1" class="rg-w" pathLength="1000" d="M310,60 A250,250 0 0 1 310,560"/>'
             '<path id="rg2" class="rg-a" pathLength="1000" d="M310,560 A250,250 0 0 1 310,60"/>'
             '<text x="310" y="352" text-anchor="middle" font-size="130" font-weight="900" fill="#fff"><tspan id="rgn">0</tspan>%</text></svg>'
             '<div class="inv" style="top:905px"><div class="pill big wht" id="rp1">PLAN</div></div>'
             '<div class="inv" style="top:995px"><div class="pill ok big" id="rp2">PALĄCE PRAGNIENIE</div></div>')
    panel("rg", seg(14)["t_in"], seg(16)["t_in"], inner)
    t_j = Ws("jedna", 14)
    js.append(f'tl.fromTo("#rg1",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:0.8,ease:"power2.out"}},{t_j:.3f});')
    js.append(f'tl.fromTo("#rgn",{{textContent:0}},{{textContent:50,duration:0.8,snap:{{textContent:1}},ease:"power2.out"}},{t_j:.3f});')
    pop("#rp1", Ws("plan", 14) - 0.06)
    dzw.append({"t": t_j, "typ": "shh", "dl": 0.8})
    t_pa = Ws("palące", 15)
    js.append(f'tl.fromTo("#rg2",{{strokeDashoffset:1000}},{{strokeDashoffset:0,duration:0.9,ease:"power2.out"}},{t_pa:.3f});')
    js.append(f'tl.fromTo("#rgn",{{textContent:50}},{{textContent:100,duration:0.9,snap:{{textContent:1}},ease:"power2.out",immediateRender:false}},{t_pa:.3f});')
    pop("#rp2", t_pa - 0.06)
    # "Napoleon Hill" mowi napis na dole (po zejsciu napisow do strefy stal tuz nad nim ten sam tekst drugi raz)
    dzw.append({"t": t_pa, "typ": "shh", "dl": 0.9})

    # --- dowod osobisty (kwestie 16-18): haslo nad glowa, potem trzy kafelki z ptaszkami
    beats([(Ws("Od", 16) + 0.05, "16–17 LAT", "", "już wiedziałem, czego chcę", Ws("wiedziałem", 16))], seg(17)["t_in"] - 0.05)
    karty = [("sun", "Wolność", Ws("wolność", 17)), ("trend", "Biznes<br>online", Ws("biznes", 17)), ("clock", "7–9 lat<br>dążenia", Ws("7", 17))]
    tiles("cel", karty, seg(19)["t_in"] - 0.02)
    for _, _, tk in karty:
        dzw.append({"t": tk, "typ": "pop", "db": -2})

    # --- pytanie do widza (kwestia 19): trzy odpowiedzi jako chipy, zostaja do planszy koncowej
    t_a = Ws("Szczęście", 19)
    odp = [("o1", "1", "SZCZĘŚCIE", t_a, 5, ""), ("o2", "2", "PLAN", W("plan", t_a)[0], 7, "top:402px"),
           ("o3", "3", "PALĄCE PRAGNIENIE", Ws("palące", 19), 10, "top:514px")]
    for oid, n, txt, tt, tr, st in odp:
        chip(oid, n, txt, tt - 0.1, end_card_in + 0.1, track=tr, style=st)
        dzw.append({"t": tt, "typ": "pop", "db": -2})

    # --- plansza koncowa: trzy slowa i wezwanie do komentarza (jego CTA), bez logo
    inner = ('<div class="ew"><div class="ew-l" id="e0">SZCZĘŚCIE</div><div class="ew-l acc" id="e1">PLAN</div>'
             '<div class="ew-l" id="e2">PRAGNIENIE</div></div>'
             '<div class="endtxt" id="endtxt" style="top:1000px">Daj znać w komentarzu</div>'
             '<div class="endsub" id="endsub" style="top:1090px">Jakub Derda</div>')
    panel("pend", end_card_in, total, inner, track=6, cls="top")
    for k in range(3):
        blur_in(f"#e{k}", end_card_in + 0.08 + k * 0.16)
    pop("#endtxt", end_card_in + 0.65)
    pop("#endsub", end_card_in + 0.8)


def build():
    edl = json.loads((P / "aroll/edl.json").read_text())
    total = edl[-1]["t_out"]
    words = load_words()

    def W(text, after=0.0):
        for a, b, t in words:
            if a >= after - 1e-6 and norm(t) == norm(text):
                return a, b
        raise SystemExit(f"Nie znaleziono slowa: {text} po {after}")

    seg = lambda i: edl[i]
    Ws = lambda text, i: W(text, seg(i)["t_in"])[0]  # start slowa szukanego od poczatku kwestii i
    el, js, srt = [], [], []
    dzw = []  # efekty dzwiekowe: dzw.append({"t": czas_trafienia, "typ": "pop" | "tik" | "swoosh" | "shh" | "powiad"}); opis w sfx.py

    # --- wideo: delikatny najazd w kazdym ujeciu
    js.append('gsap.set("#vwrap",{scale:1});')
    for e in edl:
        for sh in e["shots"]:
            js.append(f'tl.set("#vwrap",{{scale:1}},{sh["t_in"]:.3f});')
            js.append(f'tl.to("#vwrap",{{scale:1.035,duration:{sh["dur"] - 0.001:.3f},ease:"none"}},{sh["t_in"]:.3f});')

    # --- napisy slowo po slowie przez caly film (hook tez; w trybie "efekty" nad glowa dochodza do niego duze hasla)
    hook_a = norm(words[0][2]) == "według"
    frazy = rozbij((FR_HOOK_A + FR_Q1 if hook_a else FR_Q1 + FR_Q2) + FR_BODY)
    last = edl[-1]
    speech_end = last["speech"][1] - last["a_in"] + last["t_in"]
    end_card_in = round(speech_end + 0.12, 3)
    if TRYB == "napisy":   # bez planszy koncowej: film konczy sie pol sekundy po ostatnim slowie
        total = round((speech_end + 0.5) * 30) / 30
        end_card_in = total
    phrases = manual_group(words, frazy)
    for i, ph in enumerate(phrases):
        start = max(ph[0][0] - 0.06, 0)
        nxt = phrases[i + 1][0][0] - 0.06 if i + 1 < len(phrases) else end_card_in
        end = min(nxt, ph[-1][1] + 0.6, end_card_in)
        cid = f"c{i}"
        txt = " ".join(w[2] for w in ph)
        fs = min(66, int(CAP_W / (len(txt) * 0.54)))  # strefa bezpieczna: frazy do ok. 21 znakow
        if fs < CAP_MIN:
            print(f"UWAGA: fraza za dluga na strefe ({fs} px): {txt}")
        el.append(f'<div id="{cid}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" '
                  f'data-track-index="4" style="font-size:{fs}px">' + " ".join(span(w) for w in ph) + "</div>")
        for j, w in enumerate(ph):
            js.append(f'tl.fromTo("#{cid} .w:nth-child({j + 1})",{{opacity:0,y:14,filter:"blur(7px)"}},'
                      f'{{opacity:1,y:0,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{max(start, w[0] - 0.03):.3f});')
        srt.append((start, end, txt))

    leak_n = [0]

    def leak(t):
        lid = f"lk{leak_n[0]}"
        leak_n[0] += 1
        el.append(f'<div id="{lid}" class="leak clip" data-layout-ignore data-start="{t - 0.22:.3f}" data-duration="0.55" data-track-index="8"></div>')
        js.append(f'tl.fromTo("#{lid}",{{opacity:0,xPercent:-18}},{{opacity:1,xPercent:0,duration:0.2,ease:"power2.out"}},{t - 0.22:.3f});')
        js.append(f'tl.to("#{lid}",{{opacity:0,xPercent:16,duration:0.3,ease:"power2.in"}},{t - 0.02:.3f});')

    def panel(pid, t_in, t_out, inner, track=2, leak_in=True, leak_out=True, cls="", fade_out=True, extend=0.0, wejscie=None):
        """extend/fade_out=False: plansza trwa dluzej pod nastepna plansza (przenikanie bez przeswitu wideo)."""
        # kwadraty dekoracyjne u dolu planszy zostaja tylko w palecie adGen; w personal brandzie plansza jest czysta
        sq = ('<div class="sq sq1" data-layout-allow-overflow></div><div class="sq sq2" data-layout-allow-overflow></div>'
              '<div class="sq sq3" data-layout-allow-overflow></div>') if MARKA == "adgen" else ""
        rodzaj = wejscie or PRZEJSCIA[len(_uzyte_przejscia) % len(PRZEJSCIA)]
        _uzyte_przejscia.append(rodzaj)
        dzw.append({"t": t_in, "typ": "swoosh"})  # kazde wejscie planszy ma miekki swoosh
        r_od, r_do, r_czas, r_ease, w_do, w_czas, w_ease, r_leak = RUCH[rodzaj]
        el.append(f'<div id="{pid}" class="panel clip {cls}" data-layout-allow-overflow data-start="{t_in - 0.12:.3f}" data-duration="{t_out - t_in + 0.12 + extend:.3f}" data-track-index="{track}">'
                  f'<div class="pbg"></div>{sq}{inner}</div>')
        js.append(f'tl.fromTo("#{pid}",{r_od},{r_do},duration:{r_czas},ease:"{r_ease}"}},{t_in - 0.12:.3f});')
        _okna_ruchu.append((t_in - 0.12, t_in - 0.12 + r_czas))
        d = t_out - t_in
        if sq:
            js.append(f'tl.fromTo("#{pid} .sq1",{{rotation:-14,y:60}},{{rotation:-6,y:0,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            js.append(f'tl.fromTo("#{pid} .sq2",{{rotation:18,y:40}},{{rotation:9,y:-20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
            js.append(f'tl.fromTo("#{pid} .sq3",{{rotation:8}},{{rotation:20,duration:{d:.3f},ease:"none"}},{t_in:.3f});')
        if leak_in and r_leak:
            leak(t_in)
        if t_out < total - 0.1 and fade_out:
            js.append(f'tl.to("#{pid}",{w_do},duration:{w_czas},ease:"{w_ease}"}},{t_out - w_czas:.3f});')
            _okna_ruchu.append((t_out - w_czas, t_out))
            if leak_out and r_leak:
                leak(t_out)

    def pop(sel, t, extra=""):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:26,scale:0.94{extra}}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t:.3f});')

    def fade(sel, t, dur=0.25, y=12):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.3f});')

    def blur_in(sel, t):
        js.append(f'tl.fromTo("{sel}",{{opacity:0,scale:1.5,filter:"blur(16px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.3,ease:"power3.out"}},{t:.3f});')

    def overlay(oid, t_in, t_out, inner, cls, track=5, y_from=-30, style=""):
        st = f' style="{style}"' if style else ""
        el.append(f'<div id="{oid}" class="{cls} clip"{st} data-start="{t_in:.3f}" data-duration="{t_out - t_in:.3f}" data-track-index="{track}">{inner}</div>')
        js.append(f'tl.fromTo("#{oid}",{{opacity:0,y:{y_from},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.35,ease:"power3.out"}},{t_in:.3f});')
        js.append(f'tl.to("#{oid}",{{opacity:0,y:{y_from * 0.6:.0f},filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.22:.3f});')

    def tiles(tid, cards, t_out, off=False):
        """cards: (ikona, podpis, czas). off=True: szare kafelki z bialym "x" (czego nie ma), inaczej akcent + ptaszek."""
        inner = "".join(
            f'<div class="tcard{" off" if off else ""}" id="{tid}{k}"><div class="tile">{icon(ic, 40)}</div><div class="tlbl">{lbl}</div>'
            f'<span class="tok{" x" if off else ""}">{icon("x" if off else "check", 24)}</span></div>' for k, (ic, lbl, _) in enumerate(cards))
        t0 = cards[0][2] - 0.1
        el.append(f'<div id="{tid}" class="tiles clip" data-start="{t0:.3f}" data-duration="{t_out - t0:.3f}" data-track-index="5">{inner}</div>')
        for k, (_, _, t) in enumerate(cards):
            pop(f"#{tid}{k}", t - 0.08)
        js.append(f'tl.to("#{tid}",{{opacity:0,y:-20,filter:"blur(8px)",duration:0.22,ease:"power2.in"}},{t_out - 0.24:.3f});')

    def chip(cid, ic, text, t_in, t_out, ok=None, t_ok=None, ok_dot="check", track=5, style=""):
        """Chip u gory kadru: kafelek + tekst, opcjonalnie druga czesc w akcencie (wchodzi w t_ok)."""
        tile = icon(ic, 32) if ic in ICON else f'<b class="stepn">{ic}</b>'
        part = ""
        if ok:
            dot = f'<span class="dot sm">{icon(ok_dot, 22)}</span>' if ok_dot else ""
            part = f'<span class="okpart" id="{cid}ok">{dot}{html.escape(ok)}</span>'
        inner = f'<div class="chip2"><span class="tile sm">{tile}</span><span>{html.escape(text)}</span>{part}</div>'
        overlay(cid, t_in, t_out, inner, "chipwrap", track=track, style=style)
        if ok:
            # druga czesc do t_ok ma display:none (pigulka bez pustego ogona); wlaczenie przez set, ruch tylko x/opacity,
            # bo tween wlasciwosci ukladu (szerokosc, margines) nie przechodzi hyperframes check i zacina sie w renderze
            js.append(f'tl.set("#{cid}ok",{{display:"flex"}},{t_ok:.3f});')
            js.append(f'tl.fromTo("#{cid}ok",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.28,ease:"power2.out"}},{t_ok:.3f});')

    if TRYB == "efekty":
        grafiki(edl, total, end_card_in, hook_a, el, js, dzw, W, Ws, seg, panel, pop, fade, blur_in, overlay, tiles, chip)

    if SCRIM:
        el.append(f'<div id="scrim" class="scrim clip" data-layout-ignore data-start="0" data-duration="{total:.3f}" data-track-index="1"></div>')
    page = TEMPLATE.replace("    </style>", EXTRA_CSS + "    </style>").replace("{{TOTAL}}", f"{total:.3f}") \
        .replace("{{ELEMENTS}}", "\n    ".join(el)).replace("{{JS}}", "\n      ".join(js)) \
        .replace("{{CAP_TOP}}", str(CAP_TOP)).replace("{{SCRIM}}", f"{SCRIM:.2f}")
    page = kolory(page)
    czasy = sorted({round(float(m) + float(d) - 0.05, 2) for m, d in re.findall(
        r'class="cap clip" data-start="([0-9.]+)" data-duration="([0-9.]+)"', page)}
        | {round(0.4 + 0.75 * k, 2) for k in range(int((total - 0.5) / 0.75))})
    czasy = [t for t in czasy if not any(a - 0.03 <= t <= b + 0.03 for a, b in _okna_ruchu)]
    (P / "analiza").mkdir(exist_ok=True)
    (P / "analiza/strefa_czasy.json").write_text(json.dumps({"safe": SAFE, "czasy": czasy}))
    if STREFA:
        page = page.replace("</style>", STREFA_CSS + "</style>", 1)
        page = re.sub(r'<video id="aroll".*?</video>\s*<audio id="glos".*?</audio>', "", page, flags=re.S)
    hf = P / ("hf" if TRYB == "efekty" else "hfn")
    if TRYB == "napisy":   # wersja "tylko napisy" ma wlasny folder HyperFrames z tymi samymi plikami
        (hf / "renders").mkdir(parents=True, exist_ok=True)
        for f in ("package.json", "hyperframes.json", "meta.json"):
            (hf / f).write_text((P / "hf" / f).read_text().replace('_glod', '_glod_napisy'))
        for f in ("aroll.mp4", "fonts"):
            if not (hf / f).exists():
                os.symlink(P / "hf" / f, hf / f)
    out = hf / "index.html"
    out.write_text(page)
    glos = hf / "glos.wav"
    glos.unlink(missing_ok=True)
    # Efekty dzwiekowe: momenty zebrane w `dzw` ida do analiza/sfx.json, a sfx.py miksuje probki pod glos (z limiterem).
    # Bez efektow glos przechodzi tylko przez limiter -1,8 dBFS, bo kodowanie AAC w renderze dodaje ok. 0,2 dB szczytu.
    (P / "analiza").mkdir(exist_ok=True)
    (P / f"analiza/sfx_{TRYB}.json").write_text(json.dumps(sorted(dzw, key=lambda e: e["t"]), indent=1))
    if SFX and dzw and TRYB == "efekty":
        subprocess.run(["uv", "run", "--no-project", "--with", "numpy", "python3", "-I", str(BIBLIOTEKA.parent / "scripts/sfx.py"),
                        str(GLOS), str(P / f"analiza/sfx_{TRYB}.json"), str(glos)], check=True)
    else:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(GLOS), "-af",
                        "alimiter=limit=0.81:attack=1:release=40:level=false", "-c:a", "pcm_s16le", str(glos)], check=True)
    (P / "napisy.srt").write_text("\n".join(f"{i + 1}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n" for i, (a, b, t) in enumerate(srt)))
    print(f"{out} | hook {'A' if hook_a else 'B'}, tryb {TRYB}, {len(phrases)} fraz, {len(el)} elementow, {total:.2f}s, koniec mowy {speech_end:.2f}")


# Dodatki do CSS szablonu dla tej rolki (wspolny CSS z IMG_0526 zostaje bez zmian). Kolory tylko przez zmienne palety.
EXTRA_CSS = r"""
      /* niski kadr: kadr podniesiony w aroll.py, napisy tuz pod broda, w strefie bezpiecznej (CAP_TOP) */
      .chip2 .okpart { display: none; white-space: nowrap; }
      .stepn { font-size: 32px; font-weight: 900; line-height: 1; }
      .pill.big { font-size: 42px; padding: 18px 40px; gap: 14px; }
      .pill.off { position: relative; color: #c9ccd3; background: #1d1e22; border: 1.5px solid #34363d; }
      .pill.off .strike { position: absolute; left: 22px; right: 22px; top: 50%; height: 5px; margin-top: -2px; border-radius: 3px; background: #fff; transform-origin: left center; }
      .pill.wht { color: #0f1012; background: #fff; }
      .hd-a { fill: #fff; filter: drop-shadow(0 0 14px rgba(var(--accent-rgb),1)) drop-shadow(0 0 30px rgba(var(--accent-rgb),.8)); }
      /* hasla nad glowa */
      .bt { position: absolute; left: 0; right: 0; top: 282px; text-align: center; z-index: 30; }
      .bt-b { display: inline-block; font-weight: 900; letter-spacing: -0.03em; line-height: 1.02; white-space: nowrap;
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 6px 18px rgba(0,0,0,.6)); }
      .bt-b.acc { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .bt-s { margin-top: 6px; font-size: 36px; font-weight: 650; color: #fff; filter: drop-shadow(0 4px 14px rgba(0,0,0,.65)); }
      /* cytat Thiela */
      .qt { position: absolute; left: 0; right: 0; top: 285px; text-align: center; z-index: 25; filter: drop-shadow(0 6px 18px rgba(0,0,0,.6)); }
      .qt-k { font-size: 30px; font-weight: 800; letter-spacing: .16em; color: var(--accent); margin-bottom: 14px; }
      .qt-t { font-size: 80px; font-weight: 900; letter-spacing: -0.03em; line-height: 1.1; }
      .qt-h { position: relative; display: inline-block; }
      .qt-h i { position: absolute; left: 0; right: 0; bottom: -8px; height: 12px; border-radius: 6px; background: var(--accent); transform-origin: left center;
        box-shadow: 0 0 24px rgba(var(--accent-rgb),.6); }
      /* macierz 2x2 */
      .mxw { position: absolute; left: 178px; top: 336px; width: 940px; height: 940px; transform: scale(0.734); transform-origin: 0 0; }
      .mx { position: absolute; left: 0; top: 0; width: 940px; height: 940px; }
      .mx-c { position: absolute; top: 0; width: 420px; height: 60px; line-height: 60px; text-align: center; font-size: 30px; font-weight: 800; letter-spacing: .14em; color: #c9ccd3; }
      .mx-r { position: absolute; left: 0; width: 60px; height: 420px; display: grid; place-items: center; }
      .mx-r span { writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-size: 30px; font-weight: 800; letter-spacing: .14em; color: #c9ccd3; }
      .mx-q { position: absolute; width: 420px; height: 420px; border-radius: 34px; background: #16171a; border: 2px solid #2b2d32; display: grid; place-items: center; }
      .mx-in { text-align: center; color: #fff; }
      .mx-in b { display: block; font-size: 78px; font-weight: 900; letter-spacing: -0.02em; line-height: 1; }
      .mx-in i { display: block; font-style: normal; font-size: 34px; font-weight: 700; margin-top: 10px; }
      .mx-in span { display: inline-block; max-width: 350px; margin-top: 24px; font-size: 30px; font-weight: 800; letter-spacing: .04em; line-height: 1.15; text-transform: uppercase; }
      /* karty z liczbami nad glowa */
      .stat { position: absolute; left: 70px; width: 940px; top: 285px; padding: 24px 34px 28px; border-radius: 34px; text-align: center; z-index: 25;
        background: rgba(15,16,18,.88); border: 1.5px solid rgba(255,255,255,.14); box-shadow: 0 24px 70px rgba(0,0,0,.4); }
      .st-n { font-size: 150px; font-weight: 900; letter-spacing: -0.04em; line-height: 1; color: var(--accent); }
      .st-n em { font-style: normal; font-size: .4em; font-weight: 800; letter-spacing: 0; color: #fff; margin-left: .28em; }
      .st-l { font-size: 36px; font-weight: 700; color: #c9ccd3; margin-top: 8px; }
      .st-k { font-size: 30px; font-weight: 800; letter-spacing: .14em; color: var(--accent); margin-bottom: 4px; }
      .tlv { display: block; margin: 0 auto; overflow: visible; }
      .tlv text { font-family: "Inter Tight", sans-serif; }
      .tl-b { stroke: #34363d; stroke-width: 8; stroke-linecap: round; fill: none; }
      .tl-a { stroke: var(--accent); stroke-width: 8; stroke-linecap: round; fill: none; stroke-dasharray: 1000; }
      .pillcol { position: absolute; left: 0; right: 0; top: 285px; display: flex; flex-direction: column; align-items: center; gap: 18px; z-index: 25; }
      /* pierscien "dwie polowy" */
      .rg { position: absolute; left: 260px; top: 330px; width: 560px; height: 560px; overflow: visible; }
      .rg text { font-family: "Inter Tight", sans-serif; }
      .rg-b { fill: none; stroke: #24262b; stroke-width: 34; }
      .rg-w { fill: none; stroke: #fff; stroke-width: 34; stroke-linecap: butt; stroke-dasharray: 1000; }
      .rg-a { fill: none; stroke: var(--accent); stroke-width: 34; stroke-linecap: butt; stroke-dasharray: 1000; filter: drop-shadow(0 0 16px rgba(var(--accent-rgb),.6)); }
      /* plansza koncowa */
      .ew { position: absolute; left: 0; right: 0; top: 400px; text-align: center; }
      .ew-l { font-size: 128px; font-weight: 900; letter-spacing: -0.03em; line-height: 1.14;
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .ew-l.acc { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
"""


TEMPLATE = r"""<!doctype html>
<html lang="pl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }
      :root { --ground: #0f1012; --ink: #ffffff; --accent: {{ACCENT}}; --accent-rgb: {{ACCENT_RGB}}; --accent-hi: {{ACCENT_HI}}; --on-accent: {{ON_ACCENT}};
        /* tokeny, z ktorych biora kolory szablony z biblioteki (katalog HyperFrames) */
        --brand: {{ACCENT}}; --accent-2: {{ACCENT_HI}}; --bg: #0f1012; --fg: #ffffff; --surface: #16171a; --border: #2b2d32; --radius: 28px;
        --font-body: "Inter Tight", sans-serif; --ok: {{OK}}; --ok-rgb: {{OK_RGB}}; --muted: #898989; --font-display: "Inter Tight", sans-serif;
        --font-ui: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ground); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--font-display); color: var(--ink); }
      #vwrap { position: absolute; inset: 0; transform-origin: 50% 36%; }
      #aroll { position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }
      .scrim { position: absolute; left: -60px; right: -60px; top: 760px; height: 860px; z-index: 5; pointer-events: none;
        background: radial-gradient(ellipse 50% 50% at 50% 47%, rgba(8,9,11,{{SCRIM}}) 0%, rgba(8,9,11,{{SCRIM}}) 34%, rgba(8,9,11,0) 100%); }

      .kin { position: absolute; left: 0; right: 0; top: 1030px; text-align: center; z-index: 30; }
      .kin-s { font-size: 50px; font-weight: 600; letter-spacing: -0.01em; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 6px 16px; padding: 0 70px; }
      .kin-t { margin-top: 6px; }
      .kin-b { font-weight: 800; letter-spacing: -0.04em; line-height: 1.02; margin-top: 4px; display: flex; justify-content: center; gap: 0 0.22em; white-space: nowrap; }
      .kin .w, .kin .b, .cap .w { display: inline-block; }
      .kin-s .w, .cap .w, .kin-b .b {
        background: linear-gradient(180deg, #ffffff 30%, #cfd2d8 100%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 4px 14px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,255,255,.14));
      }
      .kin-b.accent .b, .cap .w.hl { background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent; }
      .kin-s .w.mention { display: inline-flex; align-items: center; gap: 12px; padding: 5px 24px 5px 5px; border-radius: 100px;
        background: rgba(var(--accent-rgb),.22); -webkit-background-clip: border-box; background-clip: border-box; color: #fff;
        border: 2px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 30px rgba(var(--accent-rgb),.35); filter: drop-shadow(0 4px 14px rgba(0,0,0,.45)); }
      .kin-s .w.mention img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; display: block; }

      .cap { position: absolute; left: 0; right: 0; top: {{CAP_TOP}}px; text-align: center; font-size: 66px; font-weight: 650; letter-spacing: -0.015em; line-height: 1.1; z-index: 30; white-space: nowrap; }

      .panel { position: absolute; inset: 0; z-index: 10; overflow: hidden; }
      .panel.top { z-index: 35; }
      .pbg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 18%, #222327 0%, #141518 45%, var(--ground) 100%); }
      .sq { position: absolute; border-radius: 34px; }
      .sq1 { width: 300px; height: 300px; left: 640px; top: 1560px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 80px rgba(var(--accent-rgb),.35); }
      .sq2 { width: 190px; height: 190px; left: -50px; top: 1480px; background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 60px rgba(var(--accent-rgb),.3); }
      .sq3 { width: 330px; height: 330px; left: 250px; top: 1640px; border: 5px solid rgba(var(--accent-rgb),.85); }

      .p-head { position: absolute; left: 0; right: 0; text-align: center; color: var(--accent); font-size: 32px; font-weight: 800; letter-spacing: .14em; }
      .p1av { position: absolute; left: 50%; margin-left: -75px; top: 250px; width: 150px; height: 150px; border-radius: 50%; padding: 6px;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 50px rgba(var(--accent-rgb),.45); }
      .p1av img { width: 138px; height: 138px; border-radius: 50%; object-fit: cover; display: block; border: 4px solid #141518; }
      .list { position: absolute; left: 160px; width: 780px; display: flex; flex-direction: column; gap: 30px; }
      .row { display: flex; align-items: center; gap: 30px; }
      .tile { width: 96px; height: 96px; border-radius: 24px; display: grid; place-items: center; color: var(--on-accent); flex: none;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 40px rgba(var(--accent-rgb),.45), inset 0 1px 0 rgba(255,255,255,.35); }
      .tile.sm { width: 56px; height: 56px; border-radius: 16px; box-shadow: 0 0 24px rgba(var(--accent-rgb),.4), inset 0 1px 0 rgba(255,255,255,.35); }
      .lbl { font-size: 48px; font-weight: 800; letter-spacing: .01em; white-space: nowrap; }

      .notif { position: absolute; left: 70px; width: 940px; top: 96px; padding: 24px 28px; border-radius: 38px; display: flex; gap: 24px; align-items: flex-start; z-index: 25;
        background: rgba(24,25,28,.9); border: 1.5px solid rgba(255,255,255,.10); box-shadow: 0 24px 70px rgba(0,0,0,.35); }
      .nt-av { width: 84px; height: 84px; border-radius: 22px; object-fit: cover; flex: none; }
      .nt-body { flex: 1; }
      .nt-top { display: flex; align-items: baseline; gap: 10px; font-size: 30px; color: #a0a3aa; font-weight: 500; }
      .nt-top b { color: #fff; font-weight: 700; }
      .nt-time { margin-left: auto; font-size: 28px; }
      .nt-title { font-size: 40px; font-weight: 750; margin-top: 2px; display: flex; align-items: center; gap: 12px; }
      .nt-title .ic { color: var(--accent); }
      .nt-items { display: flex; gap: 12px; margin-top: 14px; }
      .nti { font-size: 28px; font-weight: 700; padding: 9px 20px; border-radius: 100px; background: rgba(var(--accent-rgb),.16); border: 1.5px solid rgba(var(--accent-rgb),.6); white-space: nowrap; }

      .chipwrap { position: absolute; left: 0; right: 0; top: 290px; display: flex; justify-content: center; z-index: 25; }
      .chip2 { display: flex; align-items: center; gap: 18px; padding: 14px 32px 14px 14px; border-radius: 100px; background: rgba(15,16,18,.86);
        border: 1.5px solid rgba(255,255,255,.14); font-size: 34px; font-weight: 800; letter-spacing: .06em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0,0,0,.35); }
      .okpart { display: flex; align-items: center; gap: 12px; color: var(--ok); padding-left: 18px; border-left: 1.5px solid rgba(255,255,255,.16); }
      .dot { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: #0f1012; background: var(--ok); box-shadow: 0 0 24px rgba(var(--ok-rgb),.45); flex: none; }
      .dot.sm { width: 40px; height: 40px; }

      .cal { position: absolute; left: 140px; width: 800px; top: 380px; border-radius: 34px; padding: 26px 30px 30px;
        background: linear-gradient(180deg, #1d1e22, #16171a); border: 1.5px solid #2b2d32; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
      .cal-top { display: flex; align-items: center; gap: 14px; font-size: 38px; font-weight: 750; padding-bottom: 18px; border-bottom: 1.5px solid #2b2d32; }
      .cal-top .ic { color: var(--accent); }
      .cal-d { margin-left: auto; color: var(--muted); font-size: 28px; font-weight: 600; }
      .cal-grid { position: relative; height: 360px; margin-top: 10px; }
      .cal-row { position: absolute; left: 0; right: 0; height: 120px; border-top: 1.5px dashed #2f3136; }
      .cal-row span { position: absolute; left: 0; top: 12px; font-size: 28px; color: #6b6f77; font-weight: 600; }
      .evt { position: absolute; left: 118px; right: 0; top: 128px; height: 106px; border-radius: 22px; padding: 14px 24px;
        background: linear-gradient(140deg, rgba(var(--accent-rgb),.30), rgba(var(--accent-rgb),.16)); border: 2px solid rgba(var(--accent-rgb),.9); box-shadow: 0 0 40px rgba(var(--accent-rgb),.25); }
      .evt-t { font-size: 36px; font-weight: 800; }
      .evt-s { font-size: 28px; color: var(--accent-hi); margin-top: 6px; font-weight: 600; display: flex; gap: 10px; align-items: center; }
      .inv { position: absolute; top: 905px; left: 0; right: 0; display: flex; justify-content: center; }
      .pill { display: inline-flex; align-items: center; gap: 12px; white-space: nowrap; font-size: 31px; font-weight: 800; letter-spacing: .08em; padding: 14px 30px; border-radius: 100px; }
      .pill.ok { color: var(--ok); background: rgba(var(--ok-rgb),.14); border: 1.5px solid rgba(var(--ok-rgb),.55); box-shadow: 0 0 30px rgba(var(--ok-rgb),.25); }

      .tiles { position: absolute; left: 0; right: 0; top: 290px; display: flex; justify-content: center; gap: 20px; z-index: 25; }
      .tcard { position: relative; width: 290px; height: 206px; border-radius: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px;
        background: rgba(15,16,18,.86); border: 1.5px solid rgba(255,255,255,.12); box-shadow: 0 18px 50px rgba(0,0,0,.3); }
      .tcard .tile { width: 76px; height: 76px; border-radius: 20px; }
      .tlbl { font-size: 29px; font-weight: 750; text-align: center; line-height: 1.12; }
      .tok { position: absolute; top: -12px; right: -12px; width: 46px; height: 46px; border-radius: 50%; background: var(--ok); color: #0f1012;
        display: grid; place-items: center; box-shadow: 0 0 20px rgba(var(--ok-rgb),.45); }

      .bars { position: absolute; left: 140px; width: 800px; top: 420px; display: flex; flex-direction: column; gap: 46px; }
      .bhead { display: flex; align-items: center; justify-content: space-between; font-size: 40px; font-weight: 800; margin-bottom: 14px; }
      .bl { display: flex; align-items: center; gap: 14px; letter-spacing: .04em; }
      .bl img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; border: 2px solid var(--accent); }
      .bv { font-weight: 700; color: #d6d8dd; }
      .bv.o { color: var(--accent-hi); }
      .btrack { height: 40px; border-radius: 100px; background: #24262b; overflow: hidden; }
      .bfill { height: 100%; border-radius: 100px; transform-origin: left center; }
      .bfill.gray { width: 100%; background: linear-gradient(90deg, #6b6f77, #b3b7bf); }
      .bfill.accent { width: 4%; min-width: 30px; background: linear-gradient(90deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 24px rgba(var(--accent-rgb),.6); }
      .big30 { position: absolute; left: 0; right: 0; top: 690px; text-align: center; font-size: 230px; font-weight: 900; letter-spacing: -0.05em; line-height: 1;
        background: linear-gradient(180deg, var(--accent-hi) 0%, var(--accent) 70%); -webkit-background-clip: text; background-clip: text; color: transparent;
        filter: drop-shadow(0 0 40px rgba(var(--accent-rgb),.45)); }
      .big30s { position: absolute; left: 0; right: 0; top: 935px; text-align: center; font-size: 44px; font-weight: 800; letter-spacing: .2em; }

      .pcard { position: absolute; left: 90px; top: 240px; width: 900px; height: 754px; border-radius: 40px; overflow: hidden; background: #121212;
        box-shadow: 0 40px 120px rgba(0,0,0,.6), 0 0 0 1.5px rgba(255,255,255,.08); font-family: var(--font-ui); }
      .pc-banner { position: absolute; left: 0; right: 0; top: 0; height: 203px; background: linear-gradient(100deg, #c3c3c3, #cdcdcd 60%, #cacaca); }
      .pc-ring { position: absolute; left: 78px; top: 77px; width: 248px; height: 248px; border-radius: 50%; background: #141414; }
      .pc-av { position: absolute; left: 90px; top: 89px; width: 224px; height: 224px; border-radius: 50%; object-fit: cover; }
      .pc-name { position: absolute; left: 92px; top: 336px; font-size: 78px; font-weight: 500; color: #f5f5f5; letter-spacing: -0.01em; white-space: nowrap; }
      .pc-bot { position: absolute; left: 89px; top: 470px; display: flex; align-items: center; gap: 16px; font-size: 47px; color: #9b9b9b; }
      .pc-tabs { position: absolute; left: 58px; top: 590px; display: flex; align-items: center; gap: 8px; font-size: 46px; color: #a8a8a8; }
      .pc-tab { padding: 17px 30px; border-radius: 100px; }
      .pc-tab.on { background: #1f1f1f; color: #f5f5f5; }
      .pc-badge { position: absolute; right: 56px; top: 462px; display: flex; align-items: center; gap: 12px; font-family: var(--font-display); font-size: 36px; font-weight: 800;
        letter-spacing: .06em; color: var(--on-accent); padding: 14px 28px; border-radius: 100px; background: linear-gradient(180deg, var(--accent-hi), var(--accent));
        box-shadow: 0 0 40px rgba(var(--accent-rgb),.55), inset 0 1px 0 rgba(255,255,255,.35); }

      .ctawrap { position: absolute; left: 0; right: 0; top: 1262px; display: flex; justify-content: center; z-index: 26; }
      .cbox { width: 900px; display: flex; align-items: center; gap: 20px; padding: 14px 14px 14px 16px; border-radius: 100px; background: rgba(15,16,18,.88);
        border: 1.5px solid rgba(255,255,255,.16); box-shadow: 0 18px 50px rgba(0,0,0,.4); }
      .cav { width: 74px; height: 74px; border-radius: 50%; background: #2a2c31; color: #b9bcc3; display: grid; place-items: center; flex: none; }
      .cin { flex: 1; position: relative; height: 74px; display: flex; align-items: center; font-size: 42px; }
      .cph { position: absolute; left: 0; color: #7c8089; font-weight: 500; }
      .ctyped { display: flex; font-weight: 750; color: #fff; }
      .cl { display: none; }
      .caret { width: 4px; height: 48px; background: var(--accent); margin-left: 4px; border-radius: 2px; }
      .csend { width: 74px; height: 74px; border-radius: 50%; background: linear-gradient(180deg, var(--accent-hi), var(--accent)); color: var(--on-accent); display: grid; place-items: center;
        flex: none; box-shadow: 0 0 30px rgba(var(--accent-rgb),.5); }

      .bubble { position: absolute; left: 50%; margin-left: -300px; width: 600px; top: 520px; height: 300px; border-radius: 64px; display: grid; place-items: center;
        background: linear-gradient(140deg, var(--accent-hi), var(--accent)); box-shadow: 0 0 90px rgba(var(--accent-rgb),.5), inset 0 2px 0 rgba(255,255,255,.35); }
      .bubble::after { content: ""; position: absolute; left: 120px; bottom: -54px; width: 0; height: 0; border-right: 70px solid transparent; border-top: 60px solid var(--accent); }
      .bubble span { font-size: 170px; font-weight: 900; letter-spacing: -0.03em; color: var(--on-accent); line-height: 1; }
      .endtxt { position: absolute; left: 0; right: 0; top: 910px; text-align: center; font-size: 60px; font-weight: 800; }
      .endsub { position: absolute; left: 0; right: 0; top: 995px; text-align: center; font-size: 40px; font-weight: 500; color: #c9ccd3; }

      .leak { position: absolute; inset: -10%; z-index: 40; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(45% 35% at 30% 45%, rgba(var(--accent-rgb),.6), rgba(var(--accent-rgb),0) 70%),
                    radial-gradient(40% 30% at 70% 60%, rgba(255,255,255,.5), rgba(255,255,255,0) 70%),
                    radial-gradient(60% 50% at 50% 50%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
    <div id="vwrap">
      <video id="aroll" class="clip" src="aroll.mp4" data-start="0" data-duration="{{TOTAL}}" data-track-index="0" muted playsinline></video>
      <audio id="glos" src="glos.wav" data-start="0" data-duration="{{TOTAL}}" data-track-index="9"></audio>
    </div>
    {{ELEMENTS}}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      {{JS}}
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""

if __name__ == "__main__":
    build()

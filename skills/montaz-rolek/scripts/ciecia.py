#!/usr/bin/env python3
"""Kontrola KAZDEGO ciecia w calej gotowej rolce (zlecenie PB Managera 25.11.2026, po bledzie HOOK A C4537_v2).

poczatek.py sprawdza tylko 0-5 s. Ten sam blad (ciecie w srodku mowy, ulamek gloski z sasiedniego dubla, sklejka dwoch
podejsc tego samego zdania) moze wypasc na kazdym styku kwestii w dalszej czesci filmu. Ciecie = t_in kwestii i>=1
z aroll/edl.json projektu (A-roll sklejany kwestia po kwestii: dzwiek i obraz tna sie w tym samym miejscu; zmiany kadru
w srodku kwestii nie tna dzwieku, wiec ich tu nie ma; wyciecia ze srodka kwestii ("parts") tez sa sprawdzane).

Dla kazdego ciecia:
  1. obwiednia nagrania (audio/nowe_16k.wav) +-0,5 s przy a_in kwestii i a_out poprzedniej: glos w 60 ms przed a_in /
     po a_out (ALARM > mowa-6 dB, uwaga > mowa-14 dB), dlugosc ciszy przed a_in i po a_out;
  2. whisper-cli (bez promptu, -nfa) na gotowym MP4 w oknach ZACZYNAJACYCH sie dokladnie na cieciu (1,0 i 1,5 s)
     i KONCZACYCH sie dokladnie na cieciu (1,2 i 1,6 s): pierwsze / ostatnie slowo vs audio/slowa.json i .srt
     (ALARM, gdy zle w obu dlugosciach okna, uwaga w jednej);
  3. urwane slowo: slowo z audio/slowa.json, ktore zaczyna sie przed cieciem i konczy po nim;
  4. sklejka podejsc: whisper nagrania tuz przed a_in (czy pada tam koncowka poprzedniej kwestii = drugie podejscie
     tego samego zdania) i tuz po a_out poprzedniej (czy pada tam poczatek tej kwestii). Dozwolona tylko przy pauzie
     >= 0,15 s w nagraniu na styku (ZASADY: hook z jednego podejscia); krotsza pauza = ALARM. Pomijane, gdy kwestia
     zaczyna sie w nagraniu do 1,6 s po koncu poprzedniej (ten sam dubel, wycieta tylko pauza);
  5. okno przez ciecie (+-1 s): to samo slowo dwa razy na styku, ktorego nie ma w slowach.

Uzycie: uv run --no-project --with numpy python3 -I ciecia.py PLIK.mp4 NAPISY.srt --projekt KATALOG [--out KATALOG]
Wynik: tekst na stdout + <out>/<nazwa>_ciecia.json; przy alarmie/uwadze klip <out>/<nazwa>_ciecie_SS.ss.wav (+-1 s).
Kod wyjscia 1, gdy sa alarmy. Kazdy alarm i uwage rozstrzygnij (klip, fonemy.py, dluzsze okno) i opisz w raporcie.
"""
import argparse
import difflib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from poczatek import (SR, czytaj_wav, db_env, fon, norm, podobne, rdzen, srt, slowa_srt,  # noqa: E402
                      ta_sama_koncowka, whisper, zapisz_wav)

PAUZA_MIN = 0.15  # s ciszy w nagraniu na styku, przy ktorej sklejka dwoch podejsc jest bezpieczna


def ten_sam_poczatek(zrodlo, tekst):
    """Czy nagranie tuz po a_out zaczyna sie od poczatku nastepnej kwestii (drugie podejscie tego samego zdania)."""
    S, t = fon(zrodlo), fon(tekst)
    if len(t) < 4 or not S:
        return False
    return max(difflib.SequenceMatcher(a=S[:n], b=t).ratio() for n in range(max(1, len(t) - 3), len(t) + 5)) >= 0.72


def pasuje(w, oczek):
    """Slowo whispera pasuje do ktoregos z oczekiwanych (takze sklejonych parami: "Grogbota" ~ "Grok Bota",
    i fonetycznie: "kanbie" ~ "Canvie")."""
    kand = list(oczek) + [a_ + b_ for a_, b_ in zip(oczek, oczek[1:])]
    if norm(w) in ("ej", "ei", "aj", "eja", "ejaj") and any(norm(v) == "ai" for v in oczek):
        return True  # "AI" w krotkim oknie whisper pisze "Ej, ej" (C4538, 15,97 s)
    return any(podobne(w, v) or difflib.SequenceMatcher(a=fon(w), b=fon(v)).ratio() >= 0.75 for v in kand if norm(v))


def cisza(dbs, t, prog, kierunek, maks=0.6):
    """Dlugosc ciszy (ponizej progu) tuz przed t (kierunek -1) albo tuz po t (+1), w s."""
    i, n = int(round(t * 100)), 0
    while n < maks * 100:
        k = i - 1 - n if kierunek < 0 else i + n
        if k < 0 or k >= len(dbs) or dbs[k] > prog:
            break
        n += 1
    return n / 100


def profil(dbs, t):
    """Obwiednia +-0,5 s co 0,1 s (max dB w kazdym przedziale) - do raportu."""
    i, out = int(round(t * 100)), []
    for k in range(-50, 50, 10):
        m = dbs[max(0, i + k):max(0, i + k + 10)]
        out.append(round(float(m.max()), 1) if len(m) else None)
    return out


def przesuniecie(x, y):
    """Przesuniecie y wzgledem x (s) z korelacji obwiedni (gotowy MP4 vs audio/aroll.wav)."""
    n = min(len(x), len(y), 40 * SR)
    ex, ey = db_env(x[:n]), db_env(y[:n])
    ex, ey = np.clip(ex, -60, 0) + 60, np.clip(ey, -60, 0) + 60
    best, bo = -1e18, 0
    for o in range(-50, 51):
        a = ex[max(0, o):len(ex) + min(0, o)]
        b = ey[max(0, -o):len(ey) + min(0, -o)]
        m = min(len(a), len(b))
        v = float(np.dot(a[:m] - a[:m].mean(), b[:m] - b[:m].mean()))
        if v > best:
            best, bo = v, o
    return bo / 100


def wav_z(plik, td, nazwa):
    w = Path(td) / f"{nazwa}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(plik), "-vn", "-ac", "1", "-ar", str(SR), str(w)], check=True)
    return czytaj_wav(w)


def slowa_txt(ws):
    return [w for w in ws.split() if norm(w)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("srt")
    ap.add_argument("--projekt", required=True)
    ap.add_argument("--out", default="analiza/ciecia")
    a = ap.parse_args()
    mp4, out, P = Path(a.mp4), Path(a.out), Path(a.projekt)
    out.mkdir(parents=True, exist_ok=True)
    nazwa = mp4.stem
    edl = json.loads((P / "aroll/edl.json").read_text())
    sl = [tuple(v) for v in json.loads((P / "audio/slowa.json").read_text())]  # [od, do, slowo] w czasie A-rollu
    cues = srt(a.srt)
    alarmy, uwagi, info, wyniki = [], [], [], []

    with tempfile.TemporaryDirectory() as td:
        x = wav_z(mp4, td, "mp4")
        xs = czytaj_wav(P / "audio/nowe_16k.wav")
        dbs = db_env(xs)
        off = 0.0
        if (P / "audio/aroll.wav").exists():
            off = przesuniecie(wav_z(P / "audio/aroll.wav", td, "aroll"), x)
            if abs(off) > 0.02:
                uwagi.append((0, f"gotowy MP4 przesunięty względem A-rollu o {off:+.2f} s – cięcia przesunięte o tyle"))
        info.append(f"przesunięcie MP4 vs aroll.wav: {off:+.2f} s, długość MP4 {len(x) / SR:.2f} s")

        # ciecia: granice kwestii + wyciecia ze srodka kwestii (nowszy edl z "parts")
        ciecia = []
        for k, e in enumerate(edl):
            if k and not edl[k - 1].get("hold"):
                ciecia.append(("kwestie", k, e["t_in"]))
            parts = e.get("parts") or []
            o = 0.0
            for j in range(1, len(parts)):
                o += parts[j - 1][1]
                ciecia.append(("wewnątrz", k, round(e["t_in"] + o, 4), parts[j - 1], parts[j]))
        info.append(f"cięć: {len(ciecia)} (" + ", ".join(f"{c[2]:.2f}" for c in ciecia) + ")")

        for n, cc in enumerate(ciecia):
            rodzaj, k, t0 = cc[:3]
            c = t0 + off
            e = edl[k]
            p = edl[k - 1] if rodzaj == "kwestie" else e
            if rodzaj == "kwestie":
                a_out, a_in = p["a_out"], e["a_in"]
            else:
                a_out, a_in = cc[3][0] + cc[3][1], cc[4][0]
            wr = {"t": round(c, 3), "rodzaj": rodzaj, "kwestia": k, "a_out_pop": round(a_out, 3), "a_in": round(a_in, 3),
                  "tekst_pop": p.get("text", "")[-50:], "tekst": e.get("text", "")[:50]}
            al, uw = [], []

            # 1. obwiednia nagrania
            def poziom_mowy(q):
                sp = q.get("speech") or [q["a_in"], q["a_out"]]
                m = dbs[int(sp[0] * 100):int(sp[1] * 100)]
                return float(np.percentile(m, 70)) if len(m) else -30.0
            pz_pop, pz = poziom_mowy(p), poziom_mowy(e)
            przed = dbs[max(0, int(round(a_in * 100)) - 6):int(round(a_in * 100))]
            po = dbs[int(round(a_out * 100)):int(round(a_out * 100)) + 6]
            pauza_przed = cisza(dbs, a_in, pz - 20, -1)
            pauza_po = cisza(dbs, a_out, pz_pop - 20, +1)
            wr.update({"mowa_db": round(pz, 1), "przed_a_in_db": round(float(przed.max()), 1) if len(przed) else None,
                       "po_a_out_db": round(float(po.max()), 1) if len(po) else None,
                       "cisza_przed_a_in": pauza_przed, "cisza_po_a_out": pauza_po,
                       "obwiednia_a_in": profil(dbs, a_in), "obwiednia_a_out": profil(dbs, a_out)})
            if len(przed) and przed.max() > pz - 14:
                (al if przed.max() > pz - 6 else uw).append(
                    f"nagranie: 60 ms przed a_in={a_in:.2f} głos {przed.max():.0f} dB (mowa {pz:.0f} dB) – cięcie w trakcie głoski?")
            if len(po) and po.max() > pz_pop - 14:
                (al if po.max() > pz_pop - 6 else uw).append(
                    f"nagranie: 60 ms po a_out={a_out:.2f} głos {po.max():.0f} dB (mowa {pz_pop:.0f} dB) – urwany koniec / początek następnego słowa?")

            # oczekiwane slowa
            po_sl = [w for s0, s1, w in sl if c - 0.12 <= s0 <= c + 0.8][:2]
            przed_sl = [w for s0, s1, w in sl if c - 1.0 <= s1 <= c + 0.12][-2:]
            po_srt = [w for _, w in slowa_srt(cues, c, c + 1.2)][:3]
            przed_srt = [w for _, w in slowa_srt(cues, c - 1.2, c)][-3:]
            ok_po, ok_przed = po_sl + po_srt, przed_sl + przed_srt
            wr.update({"oczek_po": po_sl, "oczek_przed": przed_sl})

            # 3. urwane slowo
            for s0, s1, w in sl:
                if s0 < c - 0.04 and s1 > c + 0.04:
                    al.append(f"słowo „{w}” ({s0:.2f}–{s1:.2f} s w slowa.json) przecina cięcie")

            # 2. whisper od / do ciecia
            od = []
            for dl in (1.0, 1.5):
                pw = slowa_txt(whisper(x, c, min(c + dl, len(x) / SR), td, f"od{n}"))
                zl = norm("".join(pw[:2])) if len(pw) > 1 else ""
                dobre = (not pw) or (not ok_po) or pasuje(pw[0], ok_po) or any(zl == norm(v) for v in ok_po)
                od.append((" ".join(pw[:4]), dobre))
            do = []
            for dl in (1.2, 1.6):
                ww = slowa_txt(whisper(x, max(0, c - dl), c, td, f"do{n}"))
                zl = norm("".join(ww[-2:])) if len(ww) > 1 else ""
                dobre = (not ww) or (not ok_przed) or pasuje(ww[-1], ok_przed + ok_po[:1]) or \
                    any(zl == norm(v) for v in ok_przed + ok_po[:1])
                do.append((" ".join(ww[-4:]), dobre))
            wr.update({"whisper_od": od, "whisper_do": do})
            zle_od = [o for o in od if not o[1]]
            if zle_od:
                (al if len(zle_od) == len(od) else uw).append(
                    f"od cięcia słychać „{zle_od[0][0]}”, w slowach/napisach „{' '.join(po_sl or po_srt[:2])}”")
            zle_do = [o for o in do if not o[1]]
            if zle_do:
                (al if len(zle_do) == len(do) else uw).append(
                    f"do cięcia słychać „…{zle_do[0][0]}”, w slowach/napisach „…{' '.join(przed_sl or przed_srt[-2:])}”")

            # 5. okno przez ciecie: to samo slowo dwa razy na styku
            prz = slowa_txt(whisper(x, max(0, c - 1.0), min(c + 1.0, len(x) / SR), td, f"przez{n}"))
            wr["whisper_przez"] = " ".join(prz)
            A = [rdzen(norm(v)) for v in prz]
            B = [rdzen(norm(w)) for s0, s1, w in sl if c - 1.3 <= s0 <= c + 1.1]
            for i in range(len(A) - 1):
                if A[i] == A[i + 1] and len(A[i]) >= 2 and not any(B[j] == B[j + 1] == A[i] for j in range(len(B) - 1)):
                    al.append(f"to samo słowo dwa razy na styku: „{prz[i]} {prz[i + 1]}”")

            # 4. sklejka podejsc (nagranie zrodlowe)
            przed_src = whisper(xs, max(0, a_in - 1.6), a_in, td, f"src{n}")
            po_src = whisper(xs, a_out, min(a_out + 1.6, len(xs) / SR), td, f"srcpo{n}")
            # ten sam dubel: kwestia zaczyna sie w nagraniu tuz po poprzedniej (wycieta tylko pauza) - to nie sklejka
            ten_sam = 0 <= a_in - a_out <= 1.6
            wr["ten_sam_dubel"] = ten_sam
            kon_pop = " ".join(slowa_txt(p.get("text", ""))[-3:]) if rodzaj == "kwestie" and not ten_sam else ""
            pocz = " ".join(slowa_txt(e.get("text", ""))[:3]) if rodzaj == "kwestie" and not ten_sam else ""
            wr.update({"nagranie_przed_a_in": przed_src[-40:], "nagranie_po_a_out": po_src[:40]})
            if kon_pop and ta_sama_koncowka(przed_src, kon_pop):
                m = (f"sklejka dwóch podejść: w nagraniu tuż przed a_in pada „…{przed_src[-30:]}”, poprzednia kwestia "
                     f"kończy się „{kon_pop}”; cisza przed a_in {pauza_przed:.2f} s")
                (al if pauza_przed < PAUZA_MIN else info).append(m if pauza_przed < PAUZA_MIN else f"{c:.2f} s: {m} (dozwolona)")
            if pocz and ten_sam_poczatek(po_src, pocz):
                m = (f"sklejka dwóch podejść: w nagraniu tuż po a_out poprzedniej pada „{po_src[:30]}…”, ta kwestia "
                     f"zaczyna się „{pocz}”; cisza po a_out {pauza_po:.2f} s")
                (al if pauza_po < PAUZA_MIN else info).append(m if pauza_po < PAUZA_MIN else f"{c:.2f} s: {m} (dozwolona)")

            wr["alarmy"], wr["uwagi"] = al, uw
            wyniki.append(wr)
            alarmy += [(c, v) for v in al]
            uwagi += [(c, v) for v in uw]
            if al or uw:
                zapisz_wav(out / f"{nazwa}_ciecie_{c:05.2f}.wav", x[int(max(0, c - 1.0) * SR):int((c + 1.0) * SR)])

    (out / f"{nazwa}_ciecia.json").write_text(json.dumps({"plik": str(mp4), "projekt": str(P), "przesuniecie": off,
                                                          "ciecia": wyniki}, ensure_ascii=False, indent=1))
    print(f"== {mp4.name}")
    for i in info:
        print("   " + i)
    for t, o in sorted(uwagi):
        print(f"   uwaga {t:5.2f} s: {o} (sprawdź uchem)")
    for t, o in sorted(alarmy):
        print(f"   ALARM {t:5.2f} s: {o}")
    if not alarmy and not uwagi:
        print("   czysto")
    sys.exit(1 if alarmy else 0)


if __name__ == "__main__":
    main()

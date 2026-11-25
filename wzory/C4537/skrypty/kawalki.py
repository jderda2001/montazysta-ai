#!/usr/bin/env python3
"""Wykrywanie falstartow, powtorzen i zajakniec w wybranych dublach.

Whisper na calej kwestii (zwlaszcza z --prompt) wygladza zajakniecia: "I każdego ranka dosta... I każdego ranka
dostaję..." wychodzi jako jedno czyste zdanie, a zdanie powiedziane dwa razy pod rzad jako jedno (IMG_0591: "gdzie autor
pyta: sukces to szczęście czy umiejętn... gdzie autor pyta: sukces to szczęście czy umiejętności?" - DTW rozciagnal
slowo "szczęście" na 1,5 s i nic nie zglosil). Dlatego kazda kwestie z EDL dzielimy w pauzach i transkrybujemy kazdy
kawalek osobno, bez promptu.

Skrypt sam podnosi alarm, bo czytanie 20 kwestii na oko zawodzi:
  POWTORKA?  w kawalkach slychac wyraznie wiecej sylab, niz ma tekst kwestii -> cos pada dwa razy
  ?          kawalek, w ktorym zadne slowo nie pasuje do tekstu kwestii -> zajakniecie, urwane slowo albo przeslyszenie
Kazde oznaczone miejsce sprawdz osobnym whisperem na samym kawalku i drobna obwiednia (fonemy.py), zanim uznasz je za
przeslyszenie. Na koncu jest lista kwestii do sprawdzenia.

Tryby: domyslny (pauzy >= 0,15 s ponizej -45 dB) lapie falstarty i powtorki; --drobne (pauzy >= 0,09 s ponizej -42 dB)
lapie zajakniecia w srodku zdania ("sukce- cesu", "do... kładnie"). Przed oddaniem filmu pusc OBA.

Kwestie z wycieciem ze srodka (pole "parts" w edl.json, czesci.py) sa sluchane juz po wycieciu.

Uzycie: uv run --no-project --with numpy python3 -I kawalki.py [--drobne] [nr_kwestii ...]
"""
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from czesci import czesci, na_zrodlo  # noqa: E402

P = Path(__file__).resolve().parent.parent
SRC = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
DROBNE = "--drobne" in sys.argv
SILENCE_DB, MIN_PAUSE, MIN_KAW = (-42.0, 0.09, 0.2) if DROBNE else (-45.0, 0.15, 0.12)
# co whisper dopisuje na ciszy albo oddechu (nie liczymy tego do sylab)
HALUCYNACJE = ("dziękuję za uwagę", "wszystkie prawa zastrzeżone", "wszelkie prawa zastrzeżone", "zdjęcia i montaż",
               "napisy stworzone", "koniec", "dziękuję")


def norm(t):
    return re.sub(r"[^a-ząćęłńóśźż0-9]", "", t.lower())


def sylaby(t):
    return len(re.findall(r"[aeiouyąęó]+", re.sub(r"\d+", "aa", t.lower())))


def main():
    with wave.open(str(SRC)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 100, sr // 50
    edl = json.loads((P / "aroll/edl.json").read_text())
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    alarmy = []
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "c.wav"
        for e in edl:
            if only and e["i"] not in only:
                continue
            # kwestia po wycieciach ze srodka (czesci.py), bez ogona po koncu mowy; czasy liczone od poczatku kwestii
            seg = np.concatenate([x[int(p * sr):int((p + d) * sr)] for p, d in czesci(e)])
            # dlugosc liczona z EDL, nie z tablicy: przy ostatniej kwestii nagranie bywa krotsze niz a_out (przytrzymanie konca)
            dl = sum(d for _, d in czesci(e)) - max(0.0, e["a_out"] - (e["speech"][1] + 0.15))
            seg = seg[:int(dl * sr)]
            a, b = 0.0, len(seg) / sr
            n = max(1, (len(seg) - win) // hop)
            db = np.array([20 * np.log10(np.sqrt(np.mean(seg[i * hop:i * hop + win] ** 2)) + 1e-7) for i in range(n)])
            bounds, start = [a], None
            for i, v in enumerate(db):
                if v < SILENCE_DB and start is None:
                    start = i
                if v >= SILENCE_DB and start is not None:
                    if (i - start) * 0.01 >= MIN_PAUSE:
                        bounds += [a + start * 0.01 + 0.01, a + i * 0.01 + 0.01]
                    start = None
            bounds.append(b)
            chunks = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds) - 1, 2) if bounds[k + 1] - bounds[k] > MIN_KAW]
            slowa_tekstu = {norm(s) for s in e["text"].split()}
            wiersze, slychac = [], 0
            for s, t in chunks:
                with wave.open(str(f), "w") as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
                    kaw = seg[int(max(0, s - 0.05) * sr):int((t + 0.05) * sr)]
                    w.writeframes((np.concatenate([kaw, np.zeros(sr // 2, dtype=np.float32)]) * 32767).astype(np.int16).tobytes())
                r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-np"],
                                   capture_output=True, text=True)
                txt = " ".join(r.stdout.split())
                hal = norm(txt) in {norm(h) for h in HALUCYNACJE}
                if not hal:
                    slychac += sylaby(txt)
                obce = not hal and not any(norm(s) in slowa_tekstu for s in txt.split() if len(norm(s)) >= 2)
                wiersze.append(f" {'?' if obce else ' '} {na_zrodlo(e, s):7.2f}-{na_zrodlo(e, t):7.2f}  {txt}{'   (cisza/oddech?)' if hal else ''}")
                if obce:
                    alarmy.append(f"{e['i']}: ? {na_zrodlo(e, s):.2f} „{txt}”")
            ma = sylaby(e["text"])
            powt = slychac - ma >= 3 and slychac >= ma * 1.15
            if powt:
                alarmy.append(f"{e['i']}: POWTORKA? sylab w tekscie {ma}, w kawalkach {slychac}")
            print(f"== {e['i']} [sylab {ma}, slychac {slychac}{' POWTORKA?' if powt else ''}] {e['text'][:70]}")
            print("\n".join(wiersze))
    print("\nDo sprawdzenia (osobny whisper na kawalku + fonemy.py): " + ("nic" if not alarmy else ""))
    for a in alarmy:
        print("  " + a)


if __name__ == "__main__":
    main()

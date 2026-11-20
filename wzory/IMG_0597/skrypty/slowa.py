#!/usr/bin/env python3
"""Czasy slow do napisow: kazda kwestia transkrybowana osobno (whisper + DTW), przesunieta na os montazu.

DTW w whisper.cpp dziala TYLKO z wylaczonym flash attention (-nfa). Bez tego t_dtw = -1 i zostaja zgrubne czasy
heurystyczne, ktore bywaly 0,3-0,6 s za wczesnie (np. "agent AI po prostu" w IMG_0526).
t_dtw tokenu to w praktyce jego KONIEC - sprawdzone sondami: whisper na [poczatek, t] pokazuje slowo dopiero,
gdy t minie t_dtw jego ostatniego tokenu.

Slowo: koniec = t_dtw ostatniego tokenu z litera/cyfra (interpunkcja ma t_dtw w pauzie, wiec jej nie liczymy),
poczatek = koniec poprzedniego slowa albo koniec pauzy z obwiedni RMS, jesli pauza wypada pomiedzy.
Pierwsze slowo kwestii startuje od faktycznego poczatku mowy (obwiednia, okno 20 ms).

Uzycie: uv run --no-project --with numpy python3 -I slowa.py
Wynik:  ../audio/slowa.json  [[od, do, tekst], ...] na osi montazu
        ../audio/pauzy.json  [[od, do], ...] na osi montazu
"""
import json
import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
SRC = P / "audio/nowe_16k.wav"
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
SPEECH_DB, SILENCE_DB = -38.0, -45.0


def envelope(wav):
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    hop, win = sr // 100, sr // 50
    n = max(1, (len(x) - win) // hop)
    rms = np.array([np.sqrt(np.mean(x[i * hop:i * hop + win] ** 2)) for i in range(n)])
    return 20 * np.log10(rms + 1e-7)  # klatka i ~ czas i*0.01 + 0.01


def onset_after(db, t, need=3):
    """Pierwszy moment >= t, od ktorego RMS przekracza SPEECH_DB przez `need` kolejnych klatek."""
    i = max(0, int(t * 100))
    while i + need <= len(db):
        if all(db[i:i + need] > SPEECH_DB):
            return i * 0.01 + 0.01
        i += 1
    return None


def pauses(db, min_len=0.12):
    out, start = [], None
    for i, v in enumerate(db):
        if v < SILENCE_DB:
            start = i if start is None else start
        else:
            if start is not None and (i - start) * 0.01 >= min_len:
                out.append((start * 0.01 + 0.01, i * 0.01 + 0.01))
            start = None
    if start is not None and (len(db) - start) * 0.01 >= min_len:
        out.append((start * 0.01 + 0.01, len(db) * 0.01 + 0.01))
    return out


def rise_after(db, t, max_wait=0.04, need=3):
    """Powrot glosnosci po krotkim spadku: jesli od razu po t (do max_wait) RMS jest na poziomie SPEECH_DB lub
    nizej, zwraca moment, od ktorego znow jest powyzej (need klatek). Bez spadku (mowa ciagla) - None.
    Krotkie max_wait jest wazne: dluzsze lapie zwarcie wewnatrz slowa ("a|gent", "wy|starczy")."""
    i0 = max(0, int(t * 100))
    dip = next((i for i in range(i0, min(len(db), i0 + int(max_wait * 100) + 1)) if db[i] <= SPEECH_DB), None)
    return None if dip is None else onset_after(db, dip * 0.01, need)


def words_dtw(d, db, pz, onset, seg_len):
    """Slowa [od, do, tekst] (czas wzgledem poczatku kwestii) z tokenow DTW whispera.
    Start slowa: od konca poprzedniego slowa (a gdy po nim byla interpunkcja - od 0,15 s przed jej t_dtw, bo
    przecinek/kropka zajmuja przerwe, takze plytka) szukamy konca pauzy z obwiedni i powrotu glosnosci po
    krotkim spadku (zwarcie, oddech). Gdy spadku nie ma (mowa ciagla), zostaje ten punkt albo t_dtw interpunkcji."""
    words, prev_end, nxt = [], onset, onset
    for s in d["transcription"]:
        txt = s["text"].strip()
        toks = [t for t in s.get("tokens", []) if not t["text"].startswith("[_") and t["text"].strip()]
        alnum = [t for t in toks if re.search(r"\w", t["text"])]
        if not txt or not alnum:
            continue
        if any(t.get("t_dtw", -1) < 0 for t in toks):
            raise SystemExit("Brak czasow DTW (t_dtw = -1) - whisper musi dostac -dtw i -nfa")
        end = min(max(t["t_dtw"] for t in alnum) / 100, seg_len)
        punct = prev_end + 0.01 < nxt < end - 0.05
        start = max(prev_end, nxt - 0.15) if punct else prev_end
        for a, b in pz:  # pauza konczaca sie przed koncem tego slowa -> start po pauzie
            if start - 0.02 < b < end - 0.03:
                start = max(start, b)
        r = rise_after(db, start)
        if r is not None and r < end - 0.02:  # krotkie slowa ("Z", "w") tez maja swoj powrot glosnosci
            start = max(start, r)
        elif punct and nxt > start:
            start = nxt
        if words:
            start = max(start, words[-1][0] + 0.03)
        end = max(end, start + 0.05)
        words.append([start, end, txt])
        prev_end = end
        nxt = max(end, max(t["t_dtw"] for t in toks) / 100)
    return words


def main():
    edl = json.loads((P / "aroll/edl.json").read_text())
    res, all_pauses = [], []
    with tempfile.TemporaryDirectory() as td:
        for e in edl:
            if e.get("hold"):  # pauza bez slow: whisper halucynowalby na ciszy
                continue
            seg = Path(td) / f"s{e['i']}.wav"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{e['a_in']:.4f}",
                            "-to", f"{e['a_out']:.4f}", "-i", str(SRC), "-c:a", "pcm_s16le", str(seg)], check=True)
            subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(seg), "-l", "pl", "-ml", "1", "-sow",
                            "-dtw", "large.v3.turbo", "-nfa", "-ojf", "-of", str(seg.with_suffix("")),
                            "--prompt", e["text"]], capture_output=True, check=True)
            d = json.loads(seg.with_suffix(".json").read_text())
            db = envelope(seg)
            # Progi SPEECH_DB / SILENCE_DB byly strojone na IMG_0526 (90. percentyl ramek mowy = -19,3 dB). Mikrofon DJI
            # przez iPhone'a nagrywa ciszej, wiec ciche poczatki slow wypadaly ponizej progu i napis wchodzil za pozno
            # (IMG_0585). Obwiednia kazdej kwestii jest przesuwana do tego samego poziomu odniesienia.
            db = db - (float(np.percentile(db[db > -60], 90)) + 19.3)
            pz = pauses(db)
            onset = onset_after(db, 0.0) or 0.0
            words = words_dtw(d, db, pz, onset, e["t_out"] - e["t_in"])
            for w in words:
                res.append([round(w[0] + e["t_in"], 3), round(w[1] + e["t_in"], 3), w[2]])
            all_pauses += [[round(a + e["t_in"], 3), round(b + e["t_in"], 3)] for a, b in pz]
    (P / "audio/slowa.json").write_text(json.dumps(res, ensure_ascii=False, indent=0))
    (P / "audio/pauzy.json").write_text(json.dumps(all_pauses))
    for e in edl:
        ws = [w for w in res if e["t_in"] - 0.001 <= w[0] < e["t_out"] - 0.001]
        pz = [p for p in all_pauses if e["t_in"] <= p[0] < e["t_out"]]
        print(f"== {e['i']} [{e['t_in']:.2f}-{e['t_out']:.2f}] " + "  ".join(f"{a:.2f} {t}" for a, b, t in ws))
        print("   pauzy: " + "  ".join(f"{a:.2f}-{b:.2f}" for a, b in pz))


if __name__ == "__main__":
    main()

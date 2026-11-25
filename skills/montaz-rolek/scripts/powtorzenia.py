#!/usr/bin/env python3
"""Kontrola powtorzen i szybkich poprawek na CALEJ zmontowanej rolce (Jakub, 24.11.2026: "sa jeszcze czasem miejsca,
w ktorych sie powtarzam albo poprawiam bardzo szybko... dodaj sprawdzenie, czy na pewno nie ma powtorzenia na calej rolce").

Dlaczego osobno od kawalki.py: kawalki.py patrzy na kazda kwestie z osobna, wiec nie widzi powtorzenia na styku dwoch
kwestii z roznych dubli (koniec jednej mowi to samo co poczatek nastepnej), a whisper na dluzszym kawalku wygladza
"to to", "sukce- cesu" i zdanie powiedziane dwa razy.

Co robi:
  1. Tnie glos z montazu (audio/aroll.wav albo podany plik) na kawalki miedzy pauzami, w trzech przebiegach:
     mikro (dolki ponizej -30 dB od 0,05 s, na glosie po masteringu), drobnym (pauzy >= 0,09 s) i zwyklym (>= 0,2 s). Kazdy kawalek idzie do
     whispera BEZ promptu (prompt wygladza). Mikro (25.11.2026, C4538): "Jed... jeden folder" mial dolek tylko do -48 dB
     przez 0,06 s, wiec drobny przebieg go nie rozcinal, a whisper na calosci slyszal jedno "Jeden".
  2. Szuka trzech rzeczy:
     A. ta sama fraza (2-4 slowa z co najmniej jednym slowem tresci) powiedziana wiecej razy niz w tekscie kwestii,
        blisko siebie (do 12 slow), oraz to samo slowo dwa razy pod rzad ("to to", "zeby zeby");
     B. falstart: kawalek, ktory jest poczatkiem nastepnego ("Pewnie widzisz," -> "Pewnie widzisz, ze..."),
        albo urwane slowo poprawione od razu ("sukce- sukcesu", "do- dokladnie"), albo restart slowa: krotki kawalek
        (do 0,6 s, 1-2 slowa), po ktorym nastepny zaczyna sie od slowa o tym samym poczatku ("Jed..." -> "jeden folder");
     C. slowa, ktorych nie ma w tekscie kwestii (SEGS w aroll.py -> aroll/edl.json), a ktore sa powtorzeniem sasiednich.
  3. Kazde podejrzane miejsce: czas w rolce, numer kwestii, czas w nagraniu, kontekst, oraz klip do odsluchu
     analiza/powtorzenia/NN_<czas>.wav (+-1,2 s). Kod wyjscia 1, gdy sa alarmy.

Kazdy alarm rozstrzygnij uchem (klip) i fonemy.py, jak alarmy z kawalki.py. Powtorzenie, ktore jest w tresci celowo
(np. "od jakiegos czasu" w dwoch zdaniach), skrypt pomija, jesli tekst kwestii tez je ma.

Uzycie (w folderze projektu, po aroll.py):
  uv run --no-project --with numpy python3 -I skrypty/powtorzenia.py [plik_audio_albo_mp4]
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

P = Path.cwd()
MODEL = Path.home() / ".local/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
SR = 16000
STOP = {"i", "a", "to", "że", "w", "z", "na", "do", "się", "nie", "jest", "po", "o", "co", "ten", "ta", "tak", "czyli",
        "bo", "jak", "mi", "ci", "mnie", "cię", "go", "je", "już", "też", "tylko", "albo", "oraz", "u", "od", "za", "ze"}


def norm(t):
    return re.sub(r"[^\wąćęłńóśźż]", "", t.lower())


def rdzen(w):
    """Polska odmiana i literowki whispera ("rolka"/"rolkę", "Grokbot"/"grok"): porownujemy pierwsze 5 liter."""
    return w[:min(5, len(w) - 1)] if len(w) >= 4 else w


def wczytaj(src):
    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", str(SR), w], check=True)
        with wave.open(str(w)) as f:
            return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def kawalki(x, prog_db, min_pauza, min_kaw=0.2):
    hop = int(0.01 * SR)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    glos = db > prog_db
    out, start, cisza = [], None, 0
    for i, g in enumerate(glos):
        if g:
            if start is None:
                start = i
            cisza = 0
        elif start is not None:
            cisza += 1
            if cisza * 0.01 >= min_pauza:
                out.append([start * 0.01, (i - cisza + 1) * 0.01])
                start, cisza = None, 0
    if start is not None:
        out.append([start * 0.01, n * 0.01])
    scal = []
    for a, b in out:
        if scal and (b - a < min_kaw or scal[-1][1] - scal[-1][0] < min_kaw) and a - scal[-1][1] < 0.35:
            scal[-1][1] = b
        else:
            scal.append([a, b])
    return [(max(0.0, a - 0.04), b + 0.06) for a, b in scal if b - a >= 0.08]


def whisper(x, a, b, td, k):
    f = Path(td) / f"k{k}.wav"
    seg = (np.clip(x[int(a * SR): int(b * SR)], -1, 1) * 32767).astype(np.int16)
    with wave.open(str(f), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(seg.tobytes())
    r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(f), "-l", "pl", "-nt", "-np"], capture_output=True, text=True)
    t = " ".join(r.stdout.split()).strip()
    if re.fullmatch(r"(Dziękuj[eę] za (uwagę|oglądanie)[.!]?\s*)+", t):  # halucynacja na ciszy
        t = ""
    return t


def transkrybuj(x, kaw):
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(3) as ex:
        teksty = list(ex.map(lambda ka: whisper(x, ka[1][0], ka[1][1], td, ka[0]), enumerate(kaw)))
    return [(a, b, t) for (a, b), t in zip(kaw, teksty)]


def cechy(x):
    """MFCC (13) co 10 ms, znormalizowane: do porownania brzmienia fragmentow."""
    hop, win = 160, 400
    n = (len(x) - win) // hop
    fr = np.lib.stride_tricks.as_strided(x, (n, win), (x.strides[0] * hop, x.strides[0])) * np.hanning(win)
    sp = np.abs(np.fft.rfft(fr, 512)) ** 2
    f = np.linspace(0, SR / 2, sp.shape[1])
    m = np.linspace(2595 * np.log10(1 + 80 / 700), 2595 * np.log10(1 + 7600 / 700), 42)
    hz = 700 * (10 ** (m / 2595) - 1)
    fb = np.zeros((40, len(f)))
    for i in range(40):
        l, c, r = hz[i], hz[i + 1], hz[i + 2]
        fb[i] = np.clip(np.minimum((f - l) / (c - l), (r - f) / (r - c)), 0, None)
    lm = np.log(sp @ fb.T + 1e-9)
    k = np.arange(40)
    cc = lm @ np.cos(np.pi / 40 * (k[None, :] + 0.5) * np.arange(1, 14)[:, None]).T
    e = 10 * np.log10(np.mean(fr ** 2, axis=1) + 1e-12)
    cc = (cc - cc.mean(0)) / (cc.std(0) + 1e-6)
    return cc / (np.linalg.norm(cc, axis=1, keepdims=True) + 1e-9), e


# Kalibracja na IMG_0717 (24.11.2026): czysta rolka maks. 0,60 (okno 0,4 s) i 0,67 (okno 0,25 s przy odstepie 0,27 s);
# prawdziwe powtorzenia Jakuba 0,73-0,85; wklejone 0,92-1,0. Dwa przebiegi: (odstep od, do, okno, prog)
#   - zdanie albo kilka slow powtorzone (odstep 0,4-3 s), - jedno slowo powtorzone od razu (odstep 0,2-0,4 s).
PRZEBIEGI = [(0.4, 3.0, 0.4, 0.68), (0.2, 0.4, 0.25, 0.78)]


def akustyka(x):
    """Fragment (>= 0,4 s), ktory brzmi tak samo jak fragment 0,4-3 s wczesniej: zdanie albo poczatek powtorzony
    bez pauzy, ktorego whisper nie zapisuje drugi raz. Zwraca [(czas_powtorzenia, odstep, podobienstwo)]."""
    cc, e = cechy(x)
    mowa = e > e.max() - 35
    traf = []
    for lmin, lmax, okno, prog in PRZEBIEGI:
        k = int(okno * 100)
        for L in range(int(lmin * 100), min(int(lmax * 100), len(cc) - k - 1)):
            s_ = np.where(mowa[:-L] & mowa[L:], np.sum(cc[:-L] * cc[L:], axis=1), -1)
            sm = np.convolve(s_, np.ones(k) / k, "valid")
            for i in np.where(sm > prog)[0]:
                traf.append(((i + L) / 100, L / 100, float(sm[i])))
    traf.sort(key=lambda z: -z[2])
    wyb = []
    for t, L, v in traf:
        if all(abs(t - t2) > 1.0 for t2, _, _ in wyb):
            wyb.append((t, L, v))
    return sorted(wyb)


def gdzie(t, edl):
    for e in edl:
        if e["t_in"] - 1e-6 <= t < e["t_out"]:
            return e["i"], e["a_in"] + (t - e["t_in"])
    return None, None


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else P / "audio/aroll.wav"
    edl = json.loads((P / "aroll/edl.json").read_text())
    oczek = [rdzen(norm(w)) for e in edl for w in e.get("text", "").split() if norm(w)]
    x = wczytaj(src)
    alarmy = []

    for nazwa, prog, pauza in (("mikro", -30.0, 0.05), ("drobny", -42.0, 0.09), ("zwykly", -45.0, 0.2)):
        kaw = transkrybuj(x, kawalki(x, prog, pauza))
        slowa = []  # (czas, slowo) - czas slowa przyblizony liniowo w kawalku
        for a, b, t in kaw:
            ws = [w for w in t.split() if norm(w)]
            for j, w in enumerate(ws):
                slowa.append((a + (b - a) * j / max(1, len(ws)), w))
        sl = [rdzen(norm(w)) for _, w in slowa]
        if nazwa == "drobny":
            slowa_drobne = list(slowa)

        # A. ta sama fraza blisko siebie, czesciej niz w tekscie
        for n in (4, 3, 2):
            for i in range(len(sl) - n + 1):
                g = sl[i:i + n]
                if not any(len(w) >= 4 and w not in STOP for w in g):
                    continue
                for j in range(i + 1, min(len(sl) - n + 1, i + n + 12)):
                    if sl[j:j + n] == g:
                        ile_ocz = sum(1 for k in range(len(oczek) - n + 1) if oczek[k:k + n] == g)
                        ile_sl = sum(1 for k in range(len(sl) - n + 1) if sl[k:k + n] == g)
                        if ile_sl > ile_ocz:
                            alarmy.append((slowa[j][0], f"[{nazwa}] fraza powtórzona: „{' '.join(w for _, w in slowa[i:i + n])}” "
                                                        f"(słychać {ile_sl}×, w tekście {ile_ocz}×)"))
        for i in range(len(sl) - 1):
            if sl[i] == sl[i + 1] and len(sl[i]) >= 2 and not any(oczek[k] == oczek[k + 1] == sl[i] for k in range(len(oczek) - 1)):
                alarmy.append((slowa[i + 1][0], f"[{nazwa}] to samo słowo dwa razy: „{slowa[i][1]} {slowa[i + 1][1]}”"))

        # B. falstart: kawalek = poczatek nastepnego; urwane slowo poprawione od razu
        for k in range(len(kaw) - 1):
            w1 = [norm(w) for w in kaw[k][2].split() if norm(w)]
            for m in (1, 2):
                if k + m >= len(kaw):
                    break
                w2 = [norm(w) for w in kaw[k + m][2].split() if norm(w)]
                rowny = w1 and len(w2) > len(w1) and w2[:len(w1)] == w1 and any(len(w) >= 3 for w in w1)
                surowy = kaw[k][2].rstrip()
                urwany = not surowy.endswith((".", "!", "?")) or surowy.endswith(("...", "…"))
                krotki = urwany and 2 <= len(w1) <= 4 and len(w2) > len(w1) and w1[:2] == w2[:2]  # "tak jak to" -> "tak jak ta, ktora..."
                if rowny or krotki:
                    alarmy.append((kaw[k + m][0], f"[{nazwa}] falstart: „{kaw[k][2]}” → „{kaw[k + m][2]}”"))
            # restart slowa: krotki kawalek, a nastepny zaczyna sie od slowa o tym samym poczatku (min. 3 litery)
            w2n = [norm(w) for w in kaw[k + 1][2].split() if norm(w)]
            if w1 and w2n and kaw[k][1] - kaw[k][0] <= 0.6 and len(w1) <= 2 and w1[-1] != w2n[0]:
                pref = len(__import__("os").path.commonprefix([w1[-1], w2n[0]]))
                if pref >= 3:
                    alarmy.append((kaw[k + 1][0], f"[{nazwa}] restart słowa: „{kaw[k][2]}” → „{kaw[k + 1][2]}”"))
        pelne = [norm(w) for _, w in slowa]
        for k in range(len(pelne) - 1):
            a_, b_ = pelne[k], pelne[k + 1]
            if 2 <= len(a_) < len(b_) and b_.startswith(a_) and rdzen(a_) not in oczek:
                alarmy.append((slowa[k][0], f"[{nazwa}] urwane słowo poprawione: „{slowa[k][1]} {slowa[k + 1][1]}”"))

        # C. slowa spoza tekstu, ktore powtarzaja sasiednie
        sm = difflib.SequenceMatcher(a=oczek, b=sl, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op in ("insert", "replace") and j2 > j1:
                extra = sl[j1:j2]
                okolica = set(sl[max(0, j1 - 8):j1] + sl[j2:j2 + 8])
                if any(w in okolica and len(w) >= 3 for w in extra):
                    alarmy.append((slowa[j1][0], f"[{nazwa}] słowa spoza tekstu, powtórzone obok: „{' '.join(w for _, w in slowa[j1:j2])}”"))

    # D. akustyka: powtorzenie bez pauzy, ktorego whisper nie widzi
    def wyjasnione(t, L):
        """Czy oba fragmenty to ta sama fraza, ktora jest dwa razy w tekscie (np. "ktory jest wspomagany przez" Groka /
        Claude'a)? Wtedy to celowa budowa zdania, nie powtorka."""
        okno = lambda a_, b_: [rdzen(norm(w)) for tt, w in slowa_drobne if a_ - 0.15 <= tt <= b_ + 0.15]
        teraz, wczesniej = okno(t, t + 0.6), okno(t - L, t - L + 0.6)
        wspolne = [w for w in teraz if w in wczesniej and len(w) >= 3]
        if not wspolne:
            return False
        return all(sum(1 for o in oczek if o == w) >= 2 for w in wspolne)

    for t, L, v in akustyka(x):
        if v < 0.85 and wyjasnione(t, L):
            continue
        alarmy.append((t, f"[dźwięk] fragment od {t:.2f} s brzmi jak ten {L:.2f} s wcześniej (podobieństwo {v:.2f}): "
                          "możliwe powtórzenie bez pauzy"))

    # zbiorczo: jedno miejsce = jeden alarm (alarmy w odstepie < 1 s laczymy)
    alarmy.sort()
    wynik = []
    for t, opis in alarmy:
        if wynik and t - wynik[-1][0] < 1.0:
            if opis not in wynik[-1][1]:
                wynik[-1][1].append(opis)
        else:
            wynik.append([t, [opis]])
    kat = P / "analiza/powtorzenia"
    kat.mkdir(parents=True, exist_ok=True)
    for f in kat.glob("*.wav"):
        f.unlink()
    print(f"powtórzenia na całej rolce ({src.name}): {len(wynik)} miejsc do sprawdzenia")
    for n, (t, opisy) in enumerate(wynik):
        nr, t_src = gdzie(t, edl)
        klip = kat / f"{n:02d}_{t:06.2f}.wav"
        a, b = max(0, int((t - 1.2) * SR)), int((t + 1.2) * SR)
        with wave.open(str(klip), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(x[a:b], -1, 1) * 32767).astype(np.int16).tobytes())
        gdzie_txt = f"kwestia {nr}, nagranie {t_src:.2f} s" if nr is not None else "poza kwestiami"
        print(f"  {t:6.2f} s ({gdzie_txt}) -> {klip.name}")
        for o in opisy:
            print(f"      {o}")
    if wynik:
        print("Każde miejsce rozstrzygnij uchem (klip) i fonemy.py; prawdziwe powtórzenie wytnij (SEGS / wytnij) i puść kontrolę jeszcze raz.")
    sys.exit(1 if wynik else 0)


if __name__ == "__main__":
    main()

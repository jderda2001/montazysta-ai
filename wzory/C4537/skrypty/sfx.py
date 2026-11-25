#!/usr/bin/env python3
"""Subtelne efekty dzwiekowe pod animacje: miksuje probki z biblioteki pod glos, w momentach podanych w sfx.json.

Jakub 17.11.2026: "wyskakuje jakis napis, to jest taki bardzo delikatny, subtelny dzwiek... animowany wykres, zeby byl
taki shhh". Tylko prawdziwe probki z ~/Desktop/Montażysta AI/Muzyka/SFX (Kenney CC0, Mixkit Free License) - nigdy
dzwieki generowane z szumu (odrzucil je przy IMG_0361).

Uzycie: uv run --no-project --with numpy python3 -I sfx.py GLOS.wav SFX.json WYJSCIE.wav [--tylko-sfx SAME_SFX.wav]
SFX.json: [{"t": 6.20, "typ": "swoosh"}, {"t": 16.4, "typ": "pop", "db": -2}, ...]   (t = moment trafienia w obrazie)

Typy (kazdy ma kilka wariantow, brane po kolei, zeby ten sam dzwiek nie padal dwa razy pod rzad):
  pop     - wyskakujacy napis, kafelek, chip, liczba         (poczatek probki 1 klatke po obrazie)
  tik     - drobny ruch: ptaszek, podzialka, kropka          (jak wyzej, ciszej)
  swoosh  - wejscie/wyjscie planszy, przejscie               (SZCZYT probki na trafieniu, start wczesniej)
  shh     - rysowanie wykresu lub linii, dluzszy ruch        (t = START ruchu; pole "dl" = ile trwa ruch)
  powiad  - powiadomienie

Poziomy (szczyt probki w dBFS przy glosie -14 LUFS, szczyty glosu ok. -2 dBFS). To punkt wyjscia z rozpoznania,
do korekty po odsluchu Jakuba; calosc przesuwa stala GLOSNOSC.
"""
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

# Muzyka i SFX: najpierw wspolne repo zespolu (montazysta-ai/zasoby/Muzyka), a gdy go nie ma, folder na pulpicie.
_MUZYKA = next((b for b in (Path(os.environ.get("MONTAZ_REPO", Path.home() / "Montażysta AI/montazysta-ai")) / "zasoby/Muzyka",
                            Path.home() / "Desktop/Montażysta AI/Muzyka") if b.is_dir()),
               Path.home() / "Desktop/Montażysta AI/Muzyka")
LIB = _MUZYKA / "SFX"
K, U, M = "kenney-interface-sounds/Audio/", "kenney-ui-sfx-set/", "mixkit/"
GLOSNOSC = 0.0   # dB, wspolna korekta wszystkich efektow (np. -3 = jeszcze subtelniej)
SR = 48000
KLATKA = 1 / 30

# typ: (szczyt dBFS, filtr ffmpeg, wyrownanie, [warianty])
TYPY = {
    "pop": (-20.0, "highpass=f=180", "start", [K + "drop_002.ogg", K + "drop_003.ogg", K + "drop_004.ogg", M + "pop_2364_hard-pop-click.wav"]),
    "tik": (-25.0, "highpass=f=300", "start", [K + "click_001.ogg", K + "tick_002.ogg", K + "select_001.ogg", K + "tick_004.ogg"]),
    "swoosh": (-21.0, "highpass=f=220,lowpass=f=9000", "szczyt",
               [M + "swoosh_1461_short-wind-swoosh.wav", M + "swoosh_168_fast-air-sweep-transition.wav",
                M + "swoosh_1464_quick-swoosh-accent.wav", M + "swoosh_174_fast-sweep-transition.wav"]),
    "shh": (-24.0, "highpass=f=300,lowpass=f=9000", "ruch",
            [M + "swoosh_164_fast-sweeping-transition.wav", M + "swoosh_174_fast-sweep-transition.wav",
             M + "swoosh_167_long-sweeping-air-swoosh.wav"]),
    "powiad": (-20.0, "highpass=f=180", "start", [M + "pop_2356_dry-pop-up-notification-alert.wav", M + "pop_2357_bubble-pop-up-alert-notification.wav"]),
}


def dekoduj(plik, filtr, dl=None):
    """Probka -> mono 48 kHz float, przycieta do tresci (prog -45 dB od szczytu), z krotkim zanikiem na koncu."""
    af = filtr
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(plik), "-ac", "1", "-ar", str(SR), "-af", af, "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    env = np.abs(x)
    idx = np.where(env > env.max() * 10 ** (-45 / 20))[0]
    x = x[idx[0]:idx[-1] + 1]
    if dl and len(x) > int(dl * SR):   # dluzsza niz ruch: utnij i wycisz koncowke, zeby dzwiek nie przezyl ruchu
        x = x[:int(dl * SR)]
    n = min(len(x), int(0.03 * SR))
    x[-n:] *= np.linspace(1, 0, n)
    return x


def main():
    glos, cue, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sam = Path(sys.argv[sys.argv.index("--tylko-sfx") + 1]) if "--tylko-sfx" in sys.argv else None
    with wave.open(str(glos)) as w:
        assert w.getframerate() == SR, "glos ma byc 48 kHz"
        n, ch = w.getnframes(), w.getnchannels()
    bus = np.zeros(n)
    licznik = {}
    zd = sorted(json.loads(cue.read_text()), key=lambda e: e["t"])
    for e in zd:
        szczyt, filtr, tryb, warianty = TYPY[e["typ"]]
        k = licznik.get(e["typ"], 0)
        licznik[e["typ"]] = k + 1
        plik = LIB / warianty[k % len(warianty)]
        x = dekoduj(plik, filtr, e.get("dl") if tryb == "ruch" else None)
        cel = szczyt + GLOSNOSC + e.get("db", 0.0) + (-1.0 if k % 2 else 0.0)   # co drugi 1 dB ciszej: mniej mechanicznie
        x *= 10 ** (cel / 20) / (np.abs(x).max() + 1e-12)
        if tryb == "szczyt":      # swoosh: szczyt probki laduje na trafieniu obrazu
            start = e["t"] - np.argmax(np.abs(x)) / SR
        elif tryb == "ruch":      # shh: zaczyna sie z ruchem
            start = e["t"]
        else:                     # pop/tik: transjent klatke PO obrazie (dzwiek przed obrazem razi bardziej niz po)
            start = e["t"] + KLATKA
        a = max(0, int(round(start * SR)))
        b = min(n, a + len(x))
        if b > a:
            bus[a:b] += x[:b - a]
        print(f"  {e['t']:7.2f} {e['typ']:7s} {plik.name[:44]:44s} szczyt {cel:6.1f} dBFS, start {a / SR:7.2f}")
    tmp = out.with_suffix(".sfxbus.wav")
    with wave.open(str(tmp), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(bus, -1, 1) * 32767).astype(np.int16).tobytes())
    # glos bez zmiany poziomu (normalize=0) + efekty; limiter jak w kompozycja.py (-1,8 dBFS)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(glos), "-i", str(tmp), "-filter_complex",
                    "[1:a]aformat=channel_layouts=mono[s];[0:a][s]amix=inputs=2:normalize=0:duration=first:dropout_transition=0,"
                    "alimiter=limit=0.81:attack=1:release=40:level=false[o]", "-map", "[o]", "-ac", str(ch), "-c:a", "pcm_s16le", str(out)],
                   check=True)
    if sam:
        tmp.replace(sam)
    else:
        tmp.unlink()
    print(f"{out}: {len(zd)} efektow, {len(zd) / (n / SR) * 60:.1f} na minute, szczyt busa SFX {20 * np.log10(np.abs(bus).max() + 1e-12):.1f} dBFS")


if __name__ == "__main__":
    main()

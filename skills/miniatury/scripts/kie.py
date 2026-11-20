#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generowanie elementów graficznych przez kie.ai (tła, obiekty, ikony 3D). Tylko biblioteka standardowa.

  python3 kie.py kredyty
  python3 kie.py generuj --prompt "…" --wyj tlo.png [--rodzaj tlo|element|premium] [--proporcje 16:9]

Klucz: zmienna KIE_API_KEY albo plik ~/.config/kie/api_key (prawa 600). Klucza nie ma w skillu,
żeby nie wyciekł przy udostępnianiu skilla.

Do kie.ai idzie wyłącznie tekst promptu. Ten skrypt celowo nie wysyła żadnych obrazów, więc twarz
Jakuba nie opuszcza Maca. W promptach nie podawaj nazwisk, nazw firm klientów ani innych danych.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.kie.ai/api/v1"

# rodzaj -> (model, dodatkowe pola wejścia, orientacyjny koszt w kredytach)
RODZAJE = {
    # Tanie tło albo scena bez przezroczystości (PNG).
    "tlo": ("z-image", {}, 0.8),
    # Obiekt na przezroczystym tle (PNG z alfą): naklejki, ikony 3D, przedmioty.
    "element": ("gpt-image-2-6/economy-text-to-image", {"background": "transparent", "output_format": "png"}, None),
    # Najlepsza jakość sceny lub tła, do 4K.
    "premium": ("nano-banana-2-1", {"resolution": "2K", "output_format": "png", "image_input": []}, 5),
}
PROPORCJE = {
    "z-image": ("1:1", "4:3", "3:4", "16:9", "9:16"),
    "gpt-image-2-6/economy-text-to-image": ("auto", "1:1", "16:9", "9:16", "3:2", "2:3", "21:9", "4:3"),
    "nano-banana-2-1": ("1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "auto"),
}


def klucz():
    k = os.environ.get("KIE_API_KEY")
    if k:
        return k.strip()
    p = Path.home() / ".config" / "kie" / "api_key"
    if p.exists():
        return p.read_text().strip()
    sys.exit("BŁĄD: brak klucza kie.ai. Ustaw KIE_API_KEY albo zapisz klucz w ~/.config/kie/api_key (chmod 600).")


def zapytanie(metoda, sciezka, dane=None):
    req = urllib.request.Request(API + sciezka, method=metoda,
                                 data=json.dumps(dane).encode() if dane is not None else None,
                                 headers={"Authorization": "Bearer " + klucz(), "Content-Type": "application/json",
                                          "User-Agent": "miniatury-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            odp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit("BŁĄD kie.ai HTTP %s: %s" % (e.code, e.read().decode()[:300]))
    except urllib.error.URLError as e:
        sys.exit("BŁĄD połączenia z kie.ai: %s" % e.reason)
    # kie.ai zwraca błędy z HTTP 200, właściwy kod jest w polu "code".
    if odp.get("code") != 200:
        opisy = {401: "zły klucz", 402: "brak kredytów", 422: "złe parametry", 429: "za dużo zapytań, odczekaj chwilę"}
        sys.exit("BŁĄD kie.ai %s (%s): %s" % (odp.get("code"), opisy.get(odp.get("code"), "?"), odp.get("msg")))
    return odp.get("data")


def cmd_kredyty(a):
    print("Kredyty kie.ai: %s" % zapytanie("GET", "/chat/credit"))


def cmd_generuj(a):
    model, pola, _ = RODZAJE[a.rodzaj]
    if a.proporcje not in PROPORCJE[model]:
        sys.exit("BŁĄD: model %s nie obsługuje proporcji %s (dostępne: %s)" % (model, a.proporcje, ", ".join(PROPORCJE[model])))
    wej = dict(pola)
    wej["prompt"] = a.prompt
    wej["aspect_ratio"] = a.proporcje
    if a.rodzaj == "premium" and a.rozdzielczosc:
        wej["resolution"] = a.rozdzielczosc
    przed = zapytanie("GET", "/chat/credit")
    zad = zapytanie("POST", "/jobs/createTask", {"model": model, "input": wej})
    task = zad["taskId"]
    print("Zadanie %s (%s)…" % (task, model), file=sys.stderr)
    przerwa, start = 3.0, time.time()
    while True:
        time.sleep(przerwa)
        przerwa = min(przerwa * 1.3, 10)
        d = zapytanie("GET", "/jobs/recordInfo?taskId=" + task)
        stan = d.get("state")
        if stan == "success":
            break
        if stan == "fail":
            sys.exit("BŁĄD: generowanie nie powiodło się (%s): %s" % (d.get("failCode"), d.get("failMsg")))
        if time.time() - start > a.limit:
            sys.exit("BŁĄD: brak wyniku po %d s (zadanie %s nadal w stanie „%s”)" % (a.limit, task, stan))
    urls = json.loads(d.get("resultJson") or "{}").get("resultUrls") or []
    if not urls:
        sys.exit("BŁĄD: zadanie skończone, ale bez pliku wynikowego")
    wyj = Path(a.wyj)
    wyj.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(urls[0], headers={"User-Agent": "miniatury-skill/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        wyj.write_bytes(r.read())
    po = zapytanie("GET", "/chat/credit")
    # Zapis promptu obok pliku: wiadomo potem, skąd wziął się element i jak go powtórzyć.
    wyj.with_suffix(".prompt.json").write_text(json.dumps(
        {"model": model, "wejscie": wej, "zadanie": task, "kredyty": round(przed - po, 2), "czas_s": round(time.time() - start, 1)},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print("Zapisano %s (%d kB), koszt %.2f kredytu, zostało %s." % (wyj, wyj.stat().st_size / 1000, przed - po, po))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("kredyty", help="pokazuje stan konta")
    p.set_defaults(f=cmd_kredyty)
    p = sub.add_parser("generuj", help="generuje jeden obraz z promptu")
    p.add_argument("--prompt", required=True, help="opis po angielsku; bez napisów i bez ludzi")
    p.add_argument("--wyj", required=True)
    p.add_argument("--rodzaj", default="tlo", choices=sorted(RODZAJE),
                   help="tlo: tanie tło/scena; element: obiekt na przezroczystym tle; premium: najlepsza jakość")
    p.add_argument("--proporcje", default="16:9")
    p.add_argument("--rozdzielczosc", choices=["1K", "2K", "4K"], help="tylko dla rodzaju premium (domyślnie 2K)")
    p.add_argument("--limit", type=int, default=300, help="ile sekund czekać na wynik")
    p.set_defaults(f=cmd_generuj)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

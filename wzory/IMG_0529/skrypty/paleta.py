#!/usr/bin/env python3
"""Paleta grafik i napisow odcinka (wspolna dla kompozycja.py i napisy.py).

Dwie palety, ten sam uklad i ruch. MARKA wybiera, w ktorej jest caly film:
  "personal" - personal brand Jakuba (long-form, rolki): czern, biel, ciemny szary + akcent #00E5A0
  "adgen"    - stara paleta z pomaranczem #ff7018 (tak byl wyrenderowany ten odcinek 13.11.2026; reklamy adGen)
accent    - kolor akcentu; inny akcent pod temat filmu (tylko "personal") = zmiana tej jednej wartosci
on_accent - tekst i ikony NA akcencie (bialy na #00E5A0 ma kontrast 1,6:1, wiec tam ciemny; na pomaranczu bialy)
ok        - kolor "zrobione" (ptaszki, zielone ramki); None = akcent

Rolki promo maja wlasny przelacznik MARKA w rolka_szablon.py (kopia szablonu ze skilla montaz-rolek).
"""
PALETY = {
    "personal": {"accent": "#00E5A0", "on_accent": "#0f1012", "ok": None},
    "adgen": {"accent": "#ff7018", "on_accent": "#ffffff", "ok": "#3ddc84"},
}
MARKA = "personal"


def kolory(page, marka=None):
    """Wstawia palete do szablonu: {{ACCENT}}, {{ACCENT_RGB}} (pod rgba), {{ACCENT_HI}} (jasny koniec gradientu),
    {{ON_ACCENT}}, {{OK}} i {{OK_RGB}}. Reszta CSS korzysta tylko ze zmiennych, bez kolorow na sztywno."""
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

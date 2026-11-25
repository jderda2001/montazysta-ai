"""CTA i plansze koncowe "premium" w stylu Apple Liquid Glass (Jakub, 24.11.2026: "daj rozne wersje CTA (ale w podobnym
stylu)", "glass jest super, ale jeszcze troche bardziej jak Apple (liquid glass)", "daj jeszcze 5 wersji planszy
koncowej"). Wszystkie warianty sa w rotacji: kolejna rolka bierze inny wariant niz poprzednia (zapis w dzienniku).

TRYB (Jakub, 24.11.2026: "CTA ma byc cos w stylu zaobserwuj, bo nie chce miec automatyzacji na kazdej rolce"):
    tryb="obserwuj" (DOMYSLNY) - wezwanie do obserwowania, bez slow-kluczy i automatyzacji DM. `slowo` jest wtedy
        zwyklym tekstem: tresc komentarza (pole, arkusz), wiadomosc widza (dm), haslo/liczba na planszy (slowo, jasna,
        stos) albo dopisek pod karta (profil); pusty "" = bez dopisku.
    tryb="slowo" - stary wariant "Napisz SLOWO w komentarzu" pod automatyzacje. Tylko gdy Jakub wprost o to poprosi.

Uzycie w build() kompozycji:
    import cta
    h, j, d = cta.cta("pigulka", "cta", t_in, t_out, "", t_slowo, foto="avatar.jpg")       # Zaobserwuj @jakub.derda
    h2, j2, d2 = cta.plansza("profil", "pend", end_card_in, total, "", "Codziennie jedna automatyzacja", foto="avatar.jpg")
    # stary tryb pod automatyzacje: cta.cta("arkusz", ..., "ROLKA", t_slowo, tryb="slowo")
    el += [h, h2]; js += j + j2; dzw += d + d2
oraz cta.CTA_CSS w <style>. Zdjecie profilowe: foto = cta.przygotuj_avatar(P / "hf") (z Referencje i wytyczne/Zdjecie profilowe).

CTA (nad napisami, srodek na osi 540 px):
    pole     - pole komentarza, tekst wpisuje sie litera po literze, przycisk wyslij
    arkusz   - arkusz komentarzy jak w Instagramie, komentarz wjezdza na gore, serduszko sie wypelnia
    pigulka  - obserwuj: "Zaobserwuj @uchwyt"; slowo: "Napisz [SLOWO] w komentarzu"; palec stuka w chip
    profil   - karta profilu ze zdjeciem: Obserwuj -> Obserwujesz, pod spodem dopisek (slowo: "i napisz SLOWO")
    dm       - wiadomosc widza, kropki pisania, odpowiedz (obserwuj: "pokaze w nastepnej rolce"; slowo: karta linku)
Plansze koncowe (pelny ekran, A-roll rozmyty pod tafla):
    profil   - karta profilu: duze zdjecie z mietowym pierscieniem, imie, podpis, przycisk Obserwuj -> Obserwujesz
    slowo    - wielka szklana pigulka (haslo/liczba) z odblaskiem, pod nia "Zaobserwuj @uchwyt"
    telefon  - szklany telefon: obserwuj = ekran profilu z przyciskiem; slowo = komentarz i odpowiedz z linkiem
    jasna    - jasna plansza jak wstawki premium: zdjecie, haslo, "Zaobserwuj @uchwyt", podpis
    stos     - trzy szklane karty w wachlarzu (profil, haslo, Zaobserwuj) z powolna paralaksa
Ruch wedlug zasady 10: bez sprezyn, 0,5-0,9 s power3.out / expo.out, rozmycie schodzi do zera, powolny dryf.
"""
import html
import subprocess
from pathlib import Path

FOLDER_ZDJECIA = Path.home() / "Desktop/Montażysta AI/Referencje i wytyczne/Zdjęcie profilowe"


def przygotuj_avatar(hf_dir):
    """Bierze pierwsze zdjecie z Referencje i wytyczne/Zdjecie profilowe, przycina do kwadratu 512 px (srodek) i zapisuje
    jako hf/avatar.jpg. Zwraca "avatar.jpg" albo None (wtedy CTA i plansze pokaza inicjaly)."""
    pliki = sorted(p for p in FOLDER_ZDJECIA.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".heic"))
    if not pliki:
        print(f"UWAGA: brak zdjecia profilowego w {FOLDER_ZDJECIA} - CTA i plansze z inicjalami. Popros uzytkownika o zdjecie.")
        return None
    cel = Path(hf_dir) / "avatar.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pliki[0]), "-vf",
                    "crop='min(iw,ih)':'min(iw,ih)',scale=512:512:flags=lanczos", "-q:v", "2", str(cel)], check=True)
    return "avatar.jpg"

WARIANTY = ["pole", "arkusz", "pigulka", "profil", "dm"]
TRYBY = ["obserwuj", "slowo"]
PLANSZE = ["profil", "slowo", "telefon", "jasna", "stos"]

_IK = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "up": '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
}


def _ic(n, s, cls=""):
    return (f'<svg class="cic {cls}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_IK[n]}</svg>')


def _in(sel, t, y=22, dur=0.6):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{y},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{dur},ease:"power3.out"}},{t:.3f});'


def _av(foto, inicjaly, cls=""):
    if foto:
        return f'<span class="c-av {cls} ph"><img src="{html.escape(foto)}" alt=""></span>'
    return f'<span class="c-av {cls} mint">{html.escape(inicjaly)}</span>'


def cta(wariant, cid, t_in, t_out, slowo, t_slowo, uchwyt="jakub.derda", imie="Jakub Derda", inicjaly="JD", foto=None,
        odpowiedz=None, link="montaz-rolek · skill", tryb="obserwuj", wezwanie="Zaobserwuj"):
    """Zwraca (html, [js], [efekty dzwiekowe]). t_out = koniec (zwykle wejscie planszy koncowej).
    t_slowo = moment akcentu (wpisanie tekstu, klikniecie Obserwuj, stukniecie w chip)."""
    if tryb not in TRYBY:
        raise SystemExit(f"Nieznany tryb CTA: {tryb} (dostepne: {', '.join(TRYBY)})")
    obs = tryb == "obserwuj"
    if odpowiedz is None:
        odpowiedz = "Pokażę to w następnej rolce. Zaobserwuj!" if obs else "Trzymaj link do skilla"
    s = html.escape(slowo)
    js, dzw = [], []
    wrap = lambda inner, cls: (f'<div id="{cid}" class="ctaw {cls} clip" data-start="{t_in:.3f}" '
                               f'data-duration="{t_out - t_in:.3f}" data-track-index="6">{inner}</div>')
    js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:30,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{t_in:.3f});')
    js.append(f'tl.to("#{cid}",{{opacity:0,y:16,filter:"blur(8px)",duration:0.4,ease:"power2.inOut"}},{t_out - 0.4:.3f});')

    if wariant == "pole":
        inner = (f'<div class="lglass c-pole"><span class="c-av">{_ic("user", 34)}</span><span class="c-in">'
                 f'<span class="c-ph" id="{cid}ph">Dodaj komentarz…</span><span class="c-ty">'
                 + "".join(f'<i id="{cid}l{k}">{html.escape(c)}</i>' for k, c in enumerate(slowo))
                 + f'</span><span class="c-car" id="{cid}car"></span></span><span class="c-send" id="{cid}sd">{_ic("up", 34)}</span></div>')
        js.append(f'tl.set("#{cid}ph",{{opacity:0}},{t_slowo - 0.04:.3f});')
        for k in range(len(slowo)):
            js.append(f'tl.set("#{cid}l{k}",{{display:"inline"}},{t_slowo - 0.04 + 0.07 * k:.3f});')
        js.append(f'tl.fromTo("#{cid}car",{{opacity:1}},{{opacity:0,duration:0.4,ease:"steps(1)",repeat:{max(1, int((t_out - t_in) / 0.4))},yoyo:true}},{t_in + 0.3:.3f});')
        t_s = t_slowo + 0.07 * len(slowo) + 0.25
        js.append(f'tl.to("#{cid}sd",{{scale:0.9,duration:0.12,ease:"power2.out",yoyo:true,repeat:1}},{t_s:.3f});')
        dzw.append({"t": t_slowo - 0.04, "typ": "tik"})
        return wrap(inner, "c-dol"), js, dzw

    if wariant == "arkusz":
        stare = "".join(f'<div class="c-row c-old"><span class="c-av sm"></span><span class="c-sk"><i style="width:{w}px"></i><i style="width:{w2}px"></i></span></div>'
                        for w, w2 in ((160, 300),))
        inner = ('<div class="lglass c-ark"><div class="c-hd"><span class="c-grab"></span><b>Komentarze</b></div>'
                 f'<div class="c-list"><div class="c-row c-new" id="{cid}new"><span class="c-av sm mint">{_ic("user", 26)}</span>'
                 f'<span class="c-tx"><b>Ty</b><span class="{"c-km" if obs else "c-kw"}">{s}</span></span><span class="c-hrt" id="{cid}hr">{_ic("heart", 30)}</span></div>'
                 f'{stare}</div></div>')
        js.append(f'gsap.set("#{cid}new",{{height:0,opacity:0}});')
        js.append(f'tl.to("#{cid}new",{{height:84,opacity:1,duration:0.7,ease:"power3.inOut"}},{t_slowo - 0.1:.3f});')
        js.append(f'tl.to("#{cid}hr",{{color:"#ff3b5c",fill:"#ff3b5c",duration:0.35,ease:"power2.out"}},{t_slowo + 0.9:.3f});')
        dzw.append({"t": t_slowo - 0.1, "typ": "powiad"})
        return wrap(inner, "c-dol c-wys"), js, dzw  # wyzszy arkusz zaczyna sie wyzej, zeby nie wchodzic na napisy

    if wariant == "pigulka":
        if obs:
            chip = s or "@" + html.escape(uchwyt)
            srodek = f'<span>{html.escape(wezwanie)}</span><span class="c-chip c-low" id="{cid}ch">{chip}</span>'
        else:
            srodek = f'<span>Napisz</span><span class="c-chip" id="{cid}ch">{s}</span><span>w komentarzu</span>'
        inner = f'<div class="lglass c-pig">{srodek}<span class="c-tap" id="{cid}tp"></span></div>'
        js.append(f'gsap.set("#{cid}tp",{{opacity:0,scale:0.4}});')
        js.append(f'tl.to("#{cid}tp",{{opacity:1,scale:1,duration:0.35,ease:"power2.out"}},{t_slowo - 0.15:.3f});')
        js.append(f'tl.to("#{cid}tp",{{opacity:0,scale:1.8,duration:0.6,ease:"power2.out"}},{t_slowo + 0.25:.3f});')
        js.append(f'tl.to("#{cid}ch",{{scale:1.06,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:1}},{t_slowo - 0.05:.3f});')
        dzw.append({"t": t_slowo - 0.05, "typ": "tik"})
        return wrap(inner, "c-dol"), js, dzw

    if wariant == "profil":
        inner = (f'<div class="lglass c-prof">{_av(foto, inicjaly, "lg")}<span class="c-nm"><b>{html.escape(imie)}</b>'
                 f'<span>@{html.escape(uchwyt)}</span></span><span class="c-fol" id="{cid}fb"><span id="{cid}ft">Obserwuj</span></span></div>'
                 + (f'<div class="c-pod" id="{cid}pd">{s}</div>' if obs and s else '')
                 + ('' if obs else f'<div class="c-pod" id="{cid}pd">i napisz <span class="c-chip sm">{s}</span> w komentarzu</div>'))
        js.append(f'tl.to("#{cid}fb",{{backgroundColor:"rgba(255,255,255,.22)",duration:0.35,ease:"power2.inOut"}},{t_slowo:.3f});')
        js.append(f'tl.set("#{cid}ft",{{textContent:"Obserwujesz ✓"}},{t_slowo + 0.1:.3f});')
        if s or not obs:
            js.append(_in(f"#{cid}pd", t_slowo + 0.5))
        dzw.append({"t": t_slowo, "typ": "tik"})
        return wrap(inner, "c-dol"), js, dzw

    if wariant == "dm":
        inner = (f'<div class="lglass c-dm"><div class="c-dmh">{_av(foto, inicjaly, "sm")}<b>{html.escape(uchwyt)}</b></div>'
                 f'<div class="c-b me" id="{cid}b1">{s}</div>'
                 f'<div class="c-b them c-dots" id="{cid}b2"><i></i><i></i><i></i></div>'
                 f'<div class="c-b them" id="{cid}b3">{html.escape(odpowiedz)}'
                 + ('' if obs else f'<span class="c-lk">{_ic("link", 26)}{html.escape(link)}</span>') + '</div></div>')
        js.append(f'gsap.set(["#{cid}b1","#{cid}b2","#{cid}b3"],{{opacity:0}});')
        js.append(_in(f"#{cid}b1", t_slowo - 0.05, 16, 0.5))
        js.append(_in(f"#{cid}b2", t_slowo + 0.6, 12, 0.4))
        js.append(f'tl.to("#{cid}b2 i",{{opacity:0.25,duration:0.3,ease:"sine.inOut",stagger:0.12,yoyo:true,repeat:3}},{t_slowo + 0.7:.3f});')
        js.append(f'tl.to("#{cid}b2",{{opacity:0,height:0,margin:0,padding:0,duration:0.3,ease:"power2.inOut"}},{t_slowo + 1.9:.3f});')
        js.append(_in(f"#{cid}b3", t_slowo + 2.0, 16, 0.6))
        dzw.append({"t": t_slowo - 0.05, "typ": "tik"})
        dzw.append({"t": t_slowo + 2.0, "typ": "powiad"})
        return wrap(inner, "c-dol"), js, dzw

    raise SystemExit(f"Nieznany wariant CTA: {wariant} (dostepne: {', '.join(WARIANTY)})")


def plansza(wariant, pid, t_in, t_out, slowo, podpis, uchwyt="jakub.derda", imie="Jakub Derda", inicjaly="JD", foto=None,
            link="link do skilla", tryb="obserwuj", wezwanie="Zaobserwuj"):
    """Plansza koncowa na pelny ekran. A-roll zostaje pod spodem i jest rozmyty (backdrop-filter), wiec w kompozycji
    nie zaslaniaj wideo inna plansza. Zwraca (html, [js], [efekty]).
    tryb="obserwuj": slowo = krotkie haslo/liczba ("40 H", "1 czy 2?") albo "" (bez hasla)."""
    if tryb not in TRYBY:
        raise SystemExit(f"Nieznany tryb planszy: {tryb} (dostepne: {', '.join(TRYBY)})")
    obs = tryb == "obserwuj"
    s, p = html.escape(slowo), html.escape(podpis)
    uh, wz = "@" + html.escape(uchwyt), html.escape(wezwanie)
    obs_linia = f'{wz} <span class="c-chip sm c-low">{uh}</span>'  # "Zaobserwuj @jakub.derda"
    js, dzw = [], []
    d = t_out - t_in
    tlo = "e-tlo jasne" if wariant == "jasna" else "e-tlo"
    head = (f'<div id="{pid}" class="e-pl clip" data-start="{t_in:.3f}" data-duration="{d:.3f}" data-track-index="7">'
            f'<div class="{tlo}" id="{pid}bg"></div><div class="e-sc" id="{pid}sc">')
    tail = "</div></div>"
    js.append(f'tl.fromTo("#{pid}bg",{{opacity:0}},{{opacity:1,duration:0.6,ease:"power2.out"}},{t_in:.3f});')
    js.append(f'tl.fromTo("#{pid}sc",{{scale:1}},{{scale:1.035,duration:{d:.2f},ease:"none"}},{t_in:.3f});')  # powolny dryf
    dzw.append({"t": t_in, "typ": "swoosh"})
    t = t_in + 0.25

    if wariant == "profil":
        inner = (f'<div class="lglass e-prof" id="{pid}c"><span class="e-ring">{_av(foto, inicjaly, "xl")}</span>'
                 f'<b class="e-nm">{html.escape(imie)}</b><span class="e-uh">@{html.escape(uchwyt)}</span>'
                 + (f'<div class="e-l1">{s}</div>' if obs and s else '')
                 + ('' if obs else f'<div class="e-l1">Napisz <span class="c-chip">{s}</span> w komentarzu</div>')
                 + f'<div class="e-l2">{p}</div>'
                 f'<span class="e-btn" id="{pid}b"><span id="{pid}bt">Obserwuj</span></span></div>')
        js.append(_in(f"#{pid}c", t, 40, 0.8))
        js.append(_in(f"#{pid}b", t + 0.6, 12, 0.5))
        if obs:  # klikniecie: Obserwuj -> Obserwujesz
            js.append(f'tl.to("#{pid}b",{{scale:0.94,duration:0.12,ease:"power2.out",yoyo:true,repeat:1}},{t + 1.5:.3f});')
            js.append(f'tl.to("#{pid}b",{{backgroundColor:"rgba(255,255,255,.22)",color:"#fff",duration:0.35,ease:"power2.inOut"}},{t + 1.6:.3f});')
            js.append(f'tl.set("#{pid}bt",{{textContent:"Obserwujesz ✓"}},{t + 1.65:.3f});')
            dzw.append({"t": t + 1.5, "typ": "tik"})
        return head + inner + tail, js, dzw

    if wariant == "slowo":
        inner = (f'<div class="e-mid"><div class="lglass e-pill" id="{pid}w"><span>{s}</span><i class="e-sweep" id="{pid}sw"></i></div>'
                 f'<div class="e-l1 w" id="{pid}t1">{obs_linia if obs else "Napisz w komentarzu"}</div><div class="e-l2 w" id="{pid}t2">{p}</div></div>')
        js.append(_in(f"#{pid}w", t, 30, 0.8))
        js.append(f'tl.fromTo("#{pid}sw",{{xPercent:-160}},{{xPercent:260,duration:1.6,ease:"power2.inOut"}},{t + 0.6:.3f});')
        js.append(_in(f"#{pid}t1", t + 0.35))
        js.append(_in(f"#{pid}t2", t + 0.5))
        return head + inner + tail, js, dzw

    if wariant == "telefon" and obs:  # ekran profilu w szklanym telefonie
        inner = (f'<div class="lglass e-tel e-telp" id="{pid}ph"><span class="e-notch"></span>'
                 f'<span class="e-ring" id="{pid}a">{_av(foto, inicjaly, "lg2")}</span>'
                 f'<b class="e-nm" id="{pid}n">{html.escape(imie)}</b><span class="e-uh">{uh}</span>'
                 + (f'<span class="e-tsl">{s}</span>' if s else '')
                 + f'<span class="e-btn" id="{pid}b"><span id="{pid}bt">Obserwuj</span></span>'
                 f'</div><div class="e-cap" id="{pid}t1">{p}</div>')
        js.append(_in(f"#{pid}ph", t, 50, 0.9))
        js.append(_in(f"#{pid}b", t + 0.7, 12, 0.5))
        js.append(_in(f"#{pid}t1", t + 0.4))
        js.append(f'tl.to("#{pid}b",{{scale:0.94,duration:0.12,ease:"power2.out",yoyo:true,repeat:1}},{t + 1.5:.3f});')
        js.append(f'tl.to("#{pid}b",{{backgroundColor:"rgba(255,255,255,.22)",color:"#fff",duration:0.35,ease:"power2.inOut"}},{t + 1.6:.3f});')
        js.append(f'tl.set("#{pid}bt",{{textContent:"Obserwujesz ✓"}},{t + 1.65:.3f});')
        dzw.append({"t": t + 1.5, "typ": "tik"})
        return head + inner + tail, js, dzw

    if wariant == "telefon":
        inner = (f'<div class="lglass e-tel" id="{pid}ph"><span class="e-notch"></span><div class="e-tlh">Komentarze</div>'
                 f'<div class="e-tr" id="{pid}r1"><span class="c-av sm mint">{_ic("user", 24)}</span><span class="e-tx"><b>Ty</b><span class="c-kw">{s}</span></span></div>'
                 f'<div class="e-tr rep" id="{pid}r2">{_av(foto, inicjaly, "sm")}<span class="e-tx"><b>{html.escape(uchwyt)}</b><span>Wysłałem Ci {html.escape(link)} w DM</span></span></div>'
                 f'</div><div class="e-cap" id="{pid}t1">{p}</div>')
        js.append(_in(f"#{pid}ph", t, 50, 0.9))
        js.append(_in(f"#{pid}r1", t + 0.7, 14, 0.5))
        js.append(_in(f"#{pid}r2", t + 1.5, 14, 0.5))
        js.append(_in(f"#{pid}t1", t + 0.4))
        dzw.append({"t": t + 1.5, "typ": "powiad"})
        return head + inner + tail, js, dzw

    if wariant == "jasna":
        if obs:  # haslo (opcjonalne) nad wezwaniem
            srodek = ((f'<div class="e-kwl" id="{pid}k">{s}</div>' if s else f'<div id="{pid}k"></div>')
                      + f'<div class="e-l1" id="{pid}t1">{obs_linia}</div>')
        else:
            srodek = f'<div class="e-l1" id="{pid}t1">Napisz w komentarzu</div><div class="e-kwl" id="{pid}k">{s}</div>'
        inner = (f'<div class="e-mid dk"><span class="e-ring" id="{pid}a">{_av(foto, inicjaly, "xl")}</span>'
                 f'{srodek}<div class="e-l2" id="{pid}t2">{p}</div></div>')
        js.append(_in(f"#{pid}a", t, 20, 0.7))
        js.append(_in(f"#{pid}t1", t + 0.2))
        js.append(_in(f"#{pid}k", t + 0.35, 24, 0.8))
        js.append(_in(f"#{pid}t2", t + 0.55))
        return head + inner + tail, js, dzw

    if wariant == "stos":
        inner = (f'<div class="e-stos"><div class="lglass e-k k1" id="{pid}k1">{_av(foto, inicjaly, "lg")}<b>{html.escape(imie)}</b><span>@{html.escape(uchwyt)}</span></div>'
                 + (f'<div class="lglass e-k k3" id="{pid}k3">{_ic("heart", 52)}<b>{s}</b><span>{p}</span></div>'
                    f'<div class="lglass e-k k2" id="{pid}k2"><span class="e-l1 w">{wz}</span><span class="c-chip md c-low">{uh}</span></div></div>'
                    if obs else
                    f'<div class="lglass e-k k3" id="{pid}k3">{_ic("file", 52)}<b>{html.escape(link)}</b><span>{p}</span></div>'
                    f'<div class="lglass e-k k2" id="{pid}k2"><span class="e-l1 w">Napisz w komentarzu</span><span class="c-chip big">{s}</span></div></div>'))
        for kid, r, x, dl in (("k1", -8, -30, 0.0), ("k3", 7, 30, 0.12), ("k2", 0, 0, 0.24)):
            sel = f"#{pid}{kid}"
            js.append(f'tl.fromTo("{sel}",{{opacity:0,y:60,rotation:0,filter:"blur(12px)"}},{{opacity:1,y:0,rotation:{r},x:{x},filter:"blur(0px)",duration:0.9,ease:"expo.out"}},{t + dl:.3f});')
        js.append(f'tl.to("#{pid}k1",{{y:-14,duration:{d:.2f},ease:"sine.inOut"}},{t + 0.9:.3f});')
        js.append(f'tl.to("#{pid}k3",{{y:12,duration:{d:.2f},ease:"sine.inOut"}},{t + 0.9:.3f});')
        return head + inner + tail, js, dzw

    raise SystemExit(f"Nieznana plansza: {wariant} (dostepne: {', '.join(PLANSZE)})")


# Liquid Glass (Apple, ciemny tryb): przezroczysta tafla, mocne rozmycie i nasycenie tla, jasna krawedz (odblask
# u gory po lewej), wewnetrzna poswiata, cien. Tekst bialy. Akcent mietowy z ciemnym tekstem.
CTA_CSS = r"""
      .lglass { position: relative; color: #fff; isolation: isolate;
        background: linear-gradient(160deg, rgba(255,255,255,.26) 0%, rgba(255,255,255,.08) 42%, rgba(255,255,255,.14) 100%), rgba(20,22,26,.22);
        -webkit-backdrop-filter: blur(22px) saturate(190%) brightness(1.06); backdrop-filter: blur(22px) saturate(190%) brightness(1.06);
        border: 1px solid rgba(255,255,255,.38);
        box-shadow: inset 1.5px 1.5px 0 rgba(255,255,255,.75), inset -1px -1px 0 rgba(255,255,255,.22), inset 0 0 26px rgba(255,255,255,.14),
                    0 22px 60px rgba(0,0,0,.38); text-shadow: 0 1px 2px rgba(0,0,0,.25); }
      .lglass::before { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; z-index: -1;
        background: radial-gradient(90% 55% at 18% 0%, rgba(255,255,255,.42), rgba(255,255,255,0) 60%),
                    radial-gradient(60% 40% at 100% 100%, rgba(255,255,255,.16), rgba(255,255,255,0) 70%); }
      .ctaw { position: absolute; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px; z-index: 26; }
      .ctaw.c-dol { top: 900px; }
      .ctaw.c-dol.c-wys { top: 830px; }
      .cic { flex: none; }
      .c-av { width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.18); color: #fff; flex: none;
        font-size: 24px; font-weight: 800; overflow: hidden; }
      .c-av img { width: 100%; height: 100%; object-fit: cover; display: block; }
      .c-av.sm { width: 52px; height: 52px; font-size: 20px; }
      .c-av.lg { width: 96px; height: 96px; font-size: 34px; }
      .c-av.xl { width: 220px; height: 220px; font-size: 70px; }
      .c-av.mint { background: var(--accent); color: var(--on-accent); text-shadow: none; }
      .c-pole { width: 680px; display: flex; align-items: center; gap: 18px; padding: 14px 14px 14px 16px; border-radius: 100px; }
      .c-in { flex: 1; position: relative; display: flex; align-items: center; height: 64px; font-size: 38px; white-space: nowrap; }
      .c-ph { position: absolute; left: 0; color: rgba(255,255,255,.62); font-weight: 500; }
      .c-ty { font-weight: 800; letter-spacing: .02em; }
      .c-ty i { display: none; font-style: normal; }
      .c-car { width: 3px; height: 44px; background: #fff; margin-left: 4px; border-radius: 2px; }
      .c-send { width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; background: var(--accent); color: var(--on-accent); flex: none; }
      .c-ark { width: 690px; padding: 14px 26px 22px; border-radius: 34px; }
      .c-hd { display: flex; flex-direction: column; align-items: center; gap: 10px; font-size: 26px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,.18); }
      .c-grab { width: 60px; height: 6px; border-radius: 3px; background: rgba(255,255,255,.4); }
      .c-list { display: flex; flex-direction: column; }
      .c-row { display: flex; align-items: center; gap: 16px; height: 84px; overflow: hidden; }
      .c-tx { display: flex; align-items: center; gap: 12px; font-size: 30px; flex: 1; }
      .c-kw { font-weight: 800; padding: 4px 14px; border-radius: 10px; background: var(--accent); color: var(--on-accent); text-shadow: none; }
      .c-hrt { color: rgba(255,255,255,.7); }
      .c-sk { display: flex; flex-direction: column; gap: 10px; flex: 1; }
      .c-sk i { display: block; height: 14px; border-radius: 7px; background: rgba(255,255,255,.2); }
      .c-pig { display: flex; align-items: center; gap: 16px; padding: 18px 32px; border-radius: 100px; font-size: 40px; font-weight: 700; white-space: nowrap; }
      .c-chip { display: inline-block; padding: 6px 22px; border-radius: 100px; background: var(--accent); color: var(--on-accent); font-weight: 900; letter-spacing: .04em; text-shadow: none; }
      .c-chip.sm { padding: 2px 14px; font-size: .9em; }
      .c-chip.big { font-size: 96px; padding: 10px 44px; letter-spacing: .02em; }
      .c-chip.md { font-size: 50px; padding: 8px 34px; }
      .c-chip.c-low { letter-spacing: 0; }
      .c-km { font-weight: 700; }
      .c-av.lg2 { width: 170px; height: 170px; font-size: 56px; }
      .e-telp { display: flex; flex-direction: column; align-items: center; gap: 10px; top: 330px; height: auto; padding: 110px 34px 64px; text-align: center; }
      .e-telp + .e-cap { top: 1010px; }
      .e-telp .e-nm { font-size: 46px; }
      .e-tsl { margin-top: 10px; font-size: 34px; font-weight: 800; }
      .e-btn { transform-origin: 50% 50%; }
      .c-tap { position: absolute; left: 50%; top: 50%; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; border: 4px solid rgba(255,255,255,.8); }
      .c-prof { width: 690px; display: flex; align-items: center; gap: 20px; padding: 20px 22px; border-radius: 34px; }
      .c-nm { display: flex; flex-direction: column; gap: 2px; flex: 1; }
      .c-nm b { font-size: 36px; }
      .c-nm span { font-size: 28px; color: rgba(255,255,255,.7); }
      .c-fol { padding: 16px 30px; border-radius: 16px; background: #0095f6; color: #fff; font-size: 28px; font-weight: 700; white-space: nowrap; }
      .c-pod { font-size: 34px; font-weight: 700; color: #fff; text-shadow: 0 4px 16px rgba(0,0,0,.5); }
      .c-dm { width: 690px; display: flex; flex-direction: column; gap: 12px; padding: 16px 22px 22px; border-radius: 34px; }
      .c-dmh { display: flex; align-items: center; gap: 14px; font-size: 28px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,.18); }
      .c-b { max-width: 520px; padding: 16px 24px; border-radius: 26px; font-size: 30px; font-weight: 600; display: flex; flex-direction: column; gap: 10px; }
      .c-b.me { align-self: flex-end; background: var(--accent); color: var(--on-accent); font-weight: 800; border-bottom-right-radius: 8px; text-shadow: none; }
      .c-b.them { align-self: flex-start; background: rgba(255,255,255,.2); border-bottom-left-radius: 8px; }
      .c-dots { flex-direction: row; gap: 8px; }
      .c-dots i { width: 12px; height: 12px; border-radius: 50%; background: rgba(255,255,255,.75); }
      .c-lk { display: flex; align-items: center; gap: 10px; font-size: 26px; padding: 10px 14px; border-radius: 14px; background: rgba(255,255,255,.14); font-weight: 700; }

      /* plansze koncowe */
      .e-pl { position: absolute; inset: 0; z-index: 35; overflow: hidden; }
      .e-tlo { position: absolute; inset: 0; background: rgba(12,13,15,.35); -webkit-backdrop-filter: blur(46px) saturate(170%); backdrop-filter: blur(46px) saturate(170%); }
      .e-tlo.jasne { background: radial-gradient(110% 70% at 85% 0%, rgba(227,246,238,.92) 0%, rgba(245,245,242,.92) 48%, rgba(242,241,238,.94) 100%); }
      .e-sc { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .e-mid { position: absolute; left: 0; right: 0; top: 420px; display: flex; flex-direction: column; align-items: center; gap: 22px; color: #fff; text-align: center; }
      .e-mid.dk { color: #0f1012; top: 380px; }
      .e-ring { display: inline-block; padding: 8px; border-radius: 50%; background: conic-gradient(from 200deg, var(--accent), rgba(255,255,255,.9), var(--accent)); }
      .e-ring .c-av { border: 6px solid #0f1012; }
      .e-mid.dk .e-ring .c-av { border-color: #f5f5f2; }
      .e-prof { position: absolute; left: 210px; width: 660px; top: 330px; padding: 44px 40px 40px; border-radius: 56px; display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center; }
      .e-nm { font-size: 56px; margin-top: 14px; }
      .e-uh { font-size: 30px; color: rgba(255,255,255,.72); }
      .e-l1 { font-size: 46px; font-weight: 800; letter-spacing: -0.01em; margin-top: 22px; }
      .e-l1.w { margin-top: 0; }
      .e-prof .e-l1 { font-size: 40px; white-space: nowrap; }
      .e-l2 { font-size: 34px; font-weight: 500; opacity: .78; }
      .e-btn { margin-top: 18px; padding: 18px 64px; border-radius: 100px; background: #fff; color: #0f1012; font-size: 34px; font-weight: 800; text-shadow: none; }
      .e-pill { padding: 34px 90px; border-radius: 200px; overflow: hidden; }
      .e-pill span { font-size: 170px; font-weight: 900; letter-spacing: -0.02em; line-height: 1; }
      .e-sweep { position: absolute; top: -20%; bottom: -20%; left: 0; width: 30%; transform: skewX(-18deg);
        background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); mix-blend-mode: screen; }
      .e-tel { position: absolute; left: 260px; width: 560px; top: 300px; height: 700px; border-radius: 72px; padding: 70px 34px 30px; }
      .e-notch { position: absolute; left: 50%; top: 22px; width: 150px; height: 34px; margin-left: -75px; border-radius: 20px; background: rgba(0,0,0,.65); }
      .e-tlh { text-align: center; font-size: 28px; font-weight: 700; padding-bottom: 18px; border-bottom: 1px solid rgba(255,255,255,.2); }
      .e-tr { display: flex; align-items: center; gap: 14px; padding: 22px 0 0; }
      .e-tr.rep { padding-left: 46px; }
      .e-tx { display: flex; flex-direction: column; gap: 6px; font-size: 26px; }
      .e-tx b { font-size: 26px; }
      .e-tx span { color: rgba(255,255,255,.85); }
      .e-tx .c-kw { color: var(--on-accent); align-self: flex-start; }
      .e-cap { position: absolute; left: 0; right: 0; top: 1050px; text-align: center; font-size: 40px; font-weight: 800; color: #fff; text-shadow: 0 4px 18px rgba(0,0,0,.5); }
      .e-kwl { font-size: 150px; font-weight: 900; letter-spacing: -0.03em; line-height: 1; padding: 6px 40px 16px;
        background: linear-gradient(transparent 62%, rgba(var(--accent-rgb),.65) 62%, rgba(var(--accent-rgb),.65) 92%, transparent 92%); }
      .e-stos { position: absolute; left: 0; right: 0; top: 330px; height: 760px; }
      .e-k { position: absolute; left: 50%; width: 600px; margin-left: -300px; padding: 34px; border-radius: 44px; display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center; }
      .e-k b { font-size: 42px; }
      .e-k span { font-size: 28px; opacity: .78; }
      .e-k.k1 { top: 0; }
      .e-k.k3 { top: 230px; }
      .e-k.k2 { top: 450px; gap: 18px; }
"""

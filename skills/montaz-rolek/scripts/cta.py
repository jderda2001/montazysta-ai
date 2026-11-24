"""Warianty CTA "premium" (jasne szklo) do rolek. Jakub, 24.11.2026: "daj rozne wersje CTA (ale w podobnym stylu),
takie bardziej roznorodne". Kolejne rolki biora rozne warianty; uzyty wariant zapisz w dzienniku.

Uzycie w build() kompozycji:
    import cta
    h, j, d = cta.cta("arkusz", "cta", t_in, t_out, "ROLKA", t_slowo)
    el.append(h); js.extend(j); dzw.extend(d)
i dopisz cta.CTA_CSS do <style> (kompozycja.py robi to sama, jesli w TEMPLATE jest {{CTA_CSS}}).

Warianty (wszystkie w strefie bezpiecznej, srodek na osi 540 px):
    pole     - pole komentarza na szkle, slowo wpisuje sie litera po literze, przycisk wyslij
    arkusz   - arkusz komentarzy jak w Instagramie, Twoj komentarz ze slowem wjezdza na gore, serduszko sie wypelnia
    pigulka  - duza szklana pigulka "Napisz [SLOWO] w komentarzu", kursor stuka w slowo
    profil   - karta profilu: przycisk Obserwuj zmienia sie w Obserwujesz, pod spodem "i napisz SLOWO"
    dm       - rozmowa w wiadomosciach: Twoja wiadomosc ze slowem, kropki pisania, odpowiedz z karta linku
Ruch wedlug zasady 10: bez sprezyn, 0,5-0,8 s power3.out / expo.out, rozmycie schodzi do zera.
"""
import html

WARIANTY = ["pole", "arkusz", "pigulka", "profil", "dm"]

_IK = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "up": '<path d="M12 19V5"/><path d="M5 12l7-7 7 7"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "tap": '<circle cx="12" cy="12" r="3"/>',
}


def _ic(n, s, cls=""):
    return (f'<svg class="cic {cls}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_IK[n]}</svg>')


def _in(sel, t, y=22, dur=0.6):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{y},filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:{dur},ease:"power3.out"}},{t:.3f});'


def cta(wariant, cid, t_in, t_out, slowo, t_slowo, uchwyt="jakub.derda", imie="Jakub Derda", inicjaly="JD",
        odpowiedz="Trzymaj link do skilla", link="montaz-rolek · skill"):
    """Zwraca (html, [js], [efekty dzwiekowe]). t_out = koniec (zwykle wejscie planszy koncowej)."""
    s = html.escape(slowo)
    js, dzw = [], []
    wrap = lambda inner, cls: (f'<div id="{cid}" class="ctaw {cls} clip" data-start="{t_in:.3f}" '
                               f'data-duration="{t_out - t_in:.3f}" data-track-index="6">{inner}</div>')
    js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:30,filter:"blur(12px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.7,ease:"expo.out"}},{t_in:.3f});')
    js.append(f'tl.to("#{cid}",{{opacity:0,y:16,filter:"blur(8px)",duration:0.4,ease:"power2.inOut"}},{t_out - 0.4:.3f});')

    if wariant == "pole":
        inner = (f'<div class="glass c-pole"><span class="c-av">{_ic("user", 36)}</span><span class="c-in">'
                 '<span class="c-ph" id="{0}ph">Dodaj komentarz…</span><span class="c-ty">'.format(cid)
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
                        for w, w2 in ((160, 300), (120, 240)))
        inner = ('<div class="glass c-ark"><div class="c-hd"><span class="c-grab"></span><b>Komentarze</b></div>'
                 f'<div class="c-list"><div class="c-row c-new" id="{cid}new"><span class="c-av sm mint">{_ic("user", 26)}</span>'
                 f'<span class="c-tx"><b>Ty</b><span class="c-kw">{s}</span></span><span class="c-hrt" id="{cid}hr">{_ic("heart", 30)}</span></div>'
                 f'{stare}</div></div>')
        js.append(f'gsap.set("#{cid}new",{{height:0,opacity:0}});')
        js.append(f'tl.to("#{cid}new",{{height:84,opacity:1,duration:0.7,ease:"power3.inOut"}},{t_slowo - 0.1:.3f});')
        js.append(f'tl.to("#{cid}hr",{{color:"#ff3b5c",fill:"#ff3b5c",duration:0.35,ease:"power2.out"}},{t_slowo + 0.9:.3f});')
        dzw.append({"t": t_slowo - 0.1, "typ": "powiad"})
        return wrap(inner, "c-dol"), js, dzw

    if wariant == "pigulka":
        inner = (f'<div class="glass c-pig"><span>Napisz</span><span class="c-chip" id="{cid}ch">{s}</span><span>w komentarzu</span>'
                 f'<span class="c-tap" id="{cid}tp"></span></div>')
        js.append(f'gsap.set("#{cid}tp",{{opacity:0,scale:0.4}});')
        js.append(f'tl.to("#{cid}tp",{{opacity:1,scale:1,duration:0.35,ease:"power2.out"}},{t_slowo - 0.15:.3f});')
        js.append(f'tl.to("#{cid}tp",{{opacity:0,scale:1.8,duration:0.6,ease:"power2.out"}},{t_slowo + 0.25:.3f});')
        js.append(f'tl.to("#{cid}ch",{{scale:1.06,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:1}},{t_slowo - 0.05:.3f});')
        dzw.append({"t": t_slowo - 0.05, "typ": "tik"})
        return wrap(inner, "c-dol"), js, dzw

    if wariant == "profil":
        inner = (f'<div class="glass c-prof"><span class="c-av lg mint">{html.escape(inicjaly)}</span><span class="c-nm"><b>{html.escape(imie)}</b>'
                 f'<span>@{html.escape(uchwyt)}</span></span><span class="c-fol" id="{cid}fb"><span id="{cid}ft">Obserwuj</span></span></div>'
                 f'<div class="c-pod" id="{cid}pd">i napisz <span class="c-chip sm">{s}</span> w komentarzu</div>')
        js.append(f'tl.to("#{cid}fb",{{backgroundColor:"rgba(15,16,18,.08)",color:"#0f1012",duration:0.35,ease:"power2.inOut"}},{t_slowo:.3f});')
        js.append(f'tl.set("#{cid}ft",{{textContent:"Obserwujesz ✓"}},{t_slowo + 0.1:.3f});')
        js.append(_in(f"#{cid}pd", t_slowo + 0.5))
        dzw.append({"t": t_slowo, "typ": "tik"})
        return wrap(inner, "c-gora"), js, dzw

    if wariant == "dm":
        inner = (f'<div class="glass c-dm"><div class="c-dmh"><span class="c-av sm mint">{html.escape(inicjaly)}</span><b>{html.escape(uchwyt)}</b></div>'
                 f'<div class="c-b me" id="{cid}b1">{s}</div>'
                 f'<div class="c-b them c-dots" id="{cid}b2"><i></i><i></i><i></i></div>'
                 f'<div class="c-b them" id="{cid}b3">{html.escape(odpowiedz)}<span class="c-lk">{_ic("link", 26)}{html.escape(link)}</span></div></div>')
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


# Jasne szklo jak w Apple (backdrop-filter): wideo pod spodem prze swieca rozmyte. Tekst ciemny, akcent mietowy.
CTA_CSS = r"""
      .glass { background: linear-gradient(140deg, rgba(255,255,255,.72), rgba(255,255,255,.48)); -webkit-backdrop-filter: blur(30px) saturate(170%);
        backdrop-filter: blur(30px) saturate(170%); border: 1px solid rgba(255,255,255,.7); color: #0f1012;
        box-shadow: 0 24px 60px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.9), inset 0 -1px 0 rgba(255,255,255,.25); }
      .ctaw { position: absolute; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px; z-index: 26; }
      .ctaw.c-dol { top: 900px; }
      .ctaw.c-gora { top: 300px; }
      .cic { flex: none; }
      .c-av { width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; background: rgba(15,16,18,.08); color: #3a3d43; flex: none;
        font-size: 24px; font-weight: 800; }
      .c-av.sm { width: 52px; height: 52px; font-size: 20px; }
      .c-av.lg { width: 96px; height: 96px; font-size: 34px; }
      .c-av.mint { background: var(--accent); color: var(--on-accent); }
      .c-pole { width: 680px; display: flex; align-items: center; gap: 18px; padding: 14px 14px 14px 16px; border-radius: 100px; }
      .c-in { flex: 1; position: relative; display: flex; align-items: center; height: 64px; font-size: 38px; white-space: nowrap; }
      .c-ph { position: absolute; left: 0; color: rgba(15,16,18,.45); font-weight: 500; }
      .c-ty { font-weight: 800; letter-spacing: .02em; }
      .c-ty i { display: none; font-style: normal; }
      .c-car { width: 3px; height: 44px; background: #0f1012; margin-left: 4px; border-radius: 2px; }
      .c-send { width: 64px; height: 64px; border-radius: 50%; display: grid; place-items: center; background: #0f1012; color: #fff; flex: none; }
      .c-ark { width: 690px; padding: 14px 26px 22px; border-radius: 34px; }
      .c-hd { display: flex; flex-direction: column; align-items: center; gap: 10px; font-size: 26px; padding-bottom: 12px; border-bottom: 1px solid rgba(15,16,18,.1); }
      .c-grab { width: 60px; height: 6px; border-radius: 3px; background: rgba(15,16,18,.2); }
      .c-list { display: flex; flex-direction: column; }
      .c-row { display: flex; align-items: center; gap: 16px; height: 84px; overflow: hidden; }
      .c-tx { display: flex; align-items: center; gap: 12px; font-size: 30px; flex: 1; }
      .c-kw { font-weight: 800; padding: 4px 14px; border-radius: 10px; background: var(--accent); color: var(--on-accent); }
      .c-hrt { color: rgba(15,16,18,.45); }
      .c-sk { display: flex; flex-direction: column; gap: 10px; flex: 1; }
      .c-sk i { display: block; height: 14px; border-radius: 7px; background: rgba(15,16,18,.1); }
      .c-pig { position: relative; display: flex; align-items: center; gap: 16px; padding: 18px 32px; border-radius: 100px; font-size: 40px; font-weight: 700; white-space: nowrap; }
      .c-chip { display: inline-block; padding: 6px 22px; border-radius: 100px; background: var(--accent); color: var(--on-accent); font-weight: 900; letter-spacing: .04em; }
      .c-chip.sm { padding: 2px 14px; font-size: .9em; }
      .c-tap { position: absolute; left: 50%; top: 50%; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; border: 4px solid rgba(15,16,18,.55); }
      .c-prof { width: 690px; display: flex; align-items: center; gap: 20px; padding: 20px 22px; border-radius: 34px; }
      .c-nm { display: flex; flex-direction: column; gap: 2px; flex: 1; }
      .c-nm b { font-size: 36px; }
      .c-nm span { font-size: 28px; color: rgba(15,16,18,.55); }
      .c-fol { padding: 16px 30px; border-radius: 16px; background: #0095f6; color: #fff; font-size: 28px; font-weight: 700; white-space: nowrap; }
      .c-pod { font-size: 34px; font-weight: 700; color: #fff; text-shadow: 0 4px 16px rgba(0,0,0,.5); }
      .c-dm { width: 690px; display: flex; flex-direction: column; gap: 12px; padding: 16px 22px 22px; border-radius: 34px; }
      .c-dmh { display: flex; align-items: center; gap: 14px; font-size: 28px; padding-bottom: 12px; border-bottom: 1px solid rgba(15,16,18,.1); }
      .c-b { max-width: 520px; padding: 16px 24px; border-radius: 26px; font-size: 30px; font-weight: 600; display: flex; flex-direction: column; gap: 10px; }
      .c-b.me { align-self: flex-end; background: var(--accent); color: var(--on-accent); font-weight: 800; border-bottom-right-radius: 8px; }
      .c-b.them { align-self: flex-start; background: rgba(255,255,255,.8); border-bottom-left-radius: 8px; }
      .c-dots { flex-direction: row; gap: 8px; }
      .c-dots i { width: 12px; height: 12px; border-radius: 50%; background: rgba(15,16,18,.45); }
      .c-lk { display: flex; align-items: center; gap: 10px; font-size: 26px; padding: 10px 14px; border-radius: 14px; background: rgba(15,16,18,.06); font-weight: 700; }
"""

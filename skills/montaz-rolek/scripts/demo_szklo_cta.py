#!/usr/bin/env python3
"""Film demonstracyjny dla Jakuba (24.11.2026): wstawka w wariancie szkla + 5 wariantow CTA z cta.py,
na tle A-rollu z IMG_0717. Uzycie: python3 -I zbuduj.py  (potem render w hf/)."""
import importlib.util
from pathlib import Path

P = Path(__file__).resolve().parent
SK = Path.home() / ".claude/skills/montaz-rolek/scripts"
spec = importlib.util.spec_from_file_location("cta", SK / "cta.py")
cta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cta)

el, js = [], []
TOTAL = 28.0

# --- wstawka "szklo" (kurtyna z gory, A-roll rozmyty pod tafla)
t0, t1 = 0.8, 4.8
el.append(f'<div id="pg" class="panel light glass-p clip" data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" data-track-index="2">'
          '<div class="pbg"></div><div class="p-head" style="top:340px">AGENT DO MONTAŻU</div>'
          '<div class="lrow" style="top:440px"><div class="lcard" id="g1"><img src="logo/claude.png" alt=""><div><b>Claude</b><span>agent: montaż rolek</span></div></div></div>'
          '<div class="lrow" style="top:640px"><div class="lcard sm" id="g2">SUROWE NAGRANIE</div><div class="lcard sm" id="g3">GOTOWA ROLKA</div></div></div>')
js.append(f'tl.fromTo("#pg",{{y:-1920}},{{y:0,duration:0.55,ease:"power3.inOut"}},{t0:.2f});')
js.append(f'tl.to("#pg",{{y:-1920,duration:0.5,ease:"power3.inOut"}},{t1 - 0.5:.2f});')
for k, t in ((1, 1.4), (2, 2.1), (3, 2.4)):
    js.append(f'tl.fromTo("#g{k}",{{opacity:0,y:20,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:0.6,ease:"power3.out"}},{t:.2f});')

# --- 5 wariantow CTA
plan = [("pole", 5.2, 9.2, 6.2), ("arkusz", 9.6, 13.6, 10.4), ("pigulka", 14.0, 18.0, 15.0),
        ("profil", 18.4, 22.4, 19.4), ("dm", 22.8, 27.8, 23.6)]
for n, (w, a, b, ts) in enumerate(plan):
    h, j, _ = cta.cta(w, f"c{n}", a, b, "ROLKA", ts)
    el.append(h)
    js.extend(j)
etyk = [(0.8, 4.8, "WSTAWKA · SZKŁO")] + [(a, b, f"CTA {n + 1} · {w}") for n, (w, a, b, ts) in enumerate(plan)]
for n, (a, b, txt) in enumerate(etyk):
    el.append(f'<div id="e{n}" class="etyk clip" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="8"><span>{txt}</span></div>')
    js.append(f'tl.fromTo("#e{n}",{{opacity:0}},{{opacity:1,duration:0.4}},{a:.2f}); tl.to("#e{n}",{{opacity:0,duration:0.3}},{b - 0.3:.2f});')

page = f"""<!doctype html>
<html lang="pl" data-resolution="portrait"><head><meta charset="UTF-8" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
  @font-face {{ font-family: "Inter Tight"; src: url("fonts/InterTight.ttf") format("truetype"); font-weight: 100 900; }}
  :root {{ --accent: #00E5A0; --accent-rgb: 0,229,160; --on-accent: #0f1012; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0f1012; }}
  #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Inter Tight", sans-serif; color: #fff; }}
  #aroll {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
  .panel {{ position: absolute; inset: 0; z-index: 10; overflow: hidden; color: #0f1012; }}
  .pbg {{ position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.62), rgba(242,242,238,.42));
    -webkit-backdrop-filter: blur(54px) saturate(165%); backdrop-filter: blur(54px) saturate(165%); }}
  .p-head {{ position: absolute; left: 0; right: 0; text-align: center; font-size: 28px; font-weight: 800; letter-spacing: .18em; opacity: .5; }}
  .lrow {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; gap: 20px; }}
  .lcard {{ display: flex; align-items: center; gap: 22px; padding: 22px 34px 22px 22px; border-radius: 30px; background: rgba(255,255,255,.62);
    border: 1px solid rgba(255,255,255,.8); -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px);
    box-shadow: 0 18px 48px rgba(15,16,18,.10), inset 0 1px 0 rgba(255,255,255,.9); }}
  .lcard img {{ width: 96px; height: 96px; border-radius: 24px; }}
  .lcard div {{ display: flex; flex-direction: column; gap: 4px; }}
  .lcard b {{ font-size: 48px; }}
  .lcard span {{ font-size: 28px; font-weight: 700; color: #00a874; }}
  .lcard.sm {{ padding: 22px 30px; font-size: 28px; font-weight: 800; letter-spacing: .06em; }}
  .etyk {{ position: absolute; left: 0; right: 0; top: 1190px; display: flex; justify-content: center; z-index: 40; }}
  .etyk span {{ padding: 8px 20px; border-radius: 100px; background: rgba(0,0,0,.55); font-size: 26px; font-weight: 700; letter-spacing: .08em; }}
{cta.CTA_CSS}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" data-fps="60">
  <video id="aroll" class="clip" src="aroll.mp4" data-start="0" data-duration="{TOTAL}" data-track-index="0" muted playsinline></video>
  {chr(10).join(el)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join(js)}
  window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>"""
(P / "hf/index.html").write_text(page)
print("ok", len(el), "elementow")

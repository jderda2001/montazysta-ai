"""Okładka rolki w stałym systemie (wzór: C4537_v2/okladki/hf/A.html).
Uzycie: python3 okladka.py <tlo.jpg 1080x1920> <broda_y> "<linia 1 biała>" "<linia 2 w mięcie>" <wyjscie.jpg> [--nad <czubek_y>]
Karta pod brodą (top = broda + 34 px). Z --nad karta nad głową (dół karty = czubek - 30 px).
Jedna wielkość fontu na obie linie: 84 px, zmniejszana, aż najdłuższa linia zmieści się w 820 px.
Render: Chrome headless, potem JPG q=92. Wypisuje pozycję karty, żeby sprawdzić strefę."""
import json, subprocess, sys, shutil, tempfile
from pathlib import Path
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = Path(__file__).resolve().parents[2] / "miniatury/assets/InterTight.ttf"  # repo: skills/miniatury/assets

args = sys.argv[1:]
nad = None
if "--nad" in args:
    i = args.index("--nad"); nad = float(args[i + 1]); del args[i:i + 2]
tlo, broda, l1, l2, out = Path(args[0]), float(args[1]), args[2], args[3], Path(args[4])

pos = f"top:{broda + 34:.0f}px;" if nad is None else f"bottom:{1920 - (nad - 30):.0f}px;"
html = f"""<!doctype html><html lang="pl"><head><meta charset="UTF-8"><style>
@font-face {{ font-family:"Inter Tight"; src:url("InterTight.ttf") format("truetype"); font-weight:100 900; }}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0f1012}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Inter Tight",sans-serif}}
#tlo{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover}}
.karta{{position:absolute;left:0;right:0;{pos}margin:0 auto;width:max-content;max-width:900px;padding:26px 38px 30px;
 border-radius:30px;background:rgba(15,16,18,.92);box-shadow:0 24px 60px rgba(0,0,0,.35);text-align:center}}
.l{{font-size:84px;font-weight:800;letter-spacing:-0.035em;line-height:1.08;color:#fff;white-space:nowrap}}
.ac{{display:inline-block;margin-top:10px;padding:2px 18px 8px;border-radius:16px;background:#00E5A0;color:#0f1012}}
</style></head><body><div id="root">
<img id="tlo" src="tlo.jpg" alt="">
<div class="karta" id="karta"><div class="l" id="a">{l1}</div><div class="l"><span class="ac" id="b">{l2}</span></div></div>
</div><script>
document.fonts.ready.then(()=>{{
  let fs=84; const ls=[...document.querySelectorAll('.l')];
  const w=()=>Math.max(document.getElementById('a').scrollWidth, document.getElementById('b').getBoundingClientRect().width);
  while(w()>820 && fs>56){{ fs-=2; ls.forEach(e=>e.style.fontSize=fs+'px'); }}
  const r=document.getElementById('karta').getBoundingClientRect();
  document.title=JSON.stringify({{fs, x:Math.round(r.left), y:Math.round(r.top), w:Math.round(r.width), h:Math.round(r.height)}});
}});
</script></body></html>"""

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    shutil.copy(tlo, td / "tlo.jpg")
    shutil.copy(FONT, td / "InterTight.ttf")
    (td / "o.html").write_text(html, encoding="utf-8")
    png = td / "o.png"
    common = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
              "--window-size=1080,1920", "--virtual-time-budget=3000", "--allow-file-access-from-files"]
    subprocess.run(common + [f"--screenshot={png}", (td / "o.html").as_uri()], check=True, capture_output=True)
    dom = subprocess.run(common + ["--dump-dom", (td / "o.html").as_uri()], capture_output=True, text=True).stdout
    meta = dom.split("<title>")[1].split("</title>")[0] if "<title>" in dom else "{}"
    im = Image.open(png).convert("RGB")
    if im.size != (1080, 1920):
        sys.exit(f"zły rozmiar zrzutu {im.size}")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=92, subsampling=0)
    print(out.name, meta.replace("&quot;", '"'))

#!/usr/bin/env python3
"""Render 1200x630 social preview images into assets/img/og/ with headless Chrome.

Usage: python3 tools/og.py   (needs Google Chrome; run after build.py)
"""
import html
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import content as C  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(ROOT, "assets", "img", "og")
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&family=Newsreader:ital,opsz,wght@0,6..72,500;1,6..72,400&display=swap">'
CSS = """
*{box-sizing:border-box;margin:0}
body{width:1200px;height:630px;background:#faf9f6;color:#16161a;font-family:Inter,sans-serif;display:flex;overflow:hidden}
.l{flex:1;padding:64px 56px 56px 72px;display:flex;flex-direction:column}
.r{width:520px;background:#fff;border-left:1px solid #e4e1da;display:grid;place-items:center;padding:28px}
.r img{width:100%;height:auto;max-height:560px;object-fit:contain}
.chip{align-self:flex-start;font-family:'JetBrains Mono',monospace;font-size:20px;padding:6px 14px;border-radius:999px;background:#f2ebf8;color:#57068c}
.chip.ssrn{background:#e6f2f1;color:#0b5f5f}.chip.working{background:#f5efdd;color:#5a4a1a}
h1{font-family:Newsreader,serif;font-weight:500;font-size:54px;line-height:1.08;letter-spacing:-.015em;margin-top:26px}
p{font-size:25px;line-height:1.4;color:#45454f;margin-top:22px}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:end;font-size:22px;color:#676773}
.foot b{font-family:Newsreader,serif;font-weight:500;font-size:30px;color:#16161a}
.bar{position:absolute;left:0;top:0;bottom:0;width:10px;background:#57068c}
"""


def page(chip_html, title, text, right_html):
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head>
<body><div class="bar"></div><div class="l">{chip_html}<h1>{html.escape(title)}</h1><p>{html.escape(text)}</p>
<div class="foot"><b>Tanishk Yadav</b><span>tanishkyadav.me</span></div></div>{right_html}</body></html>"""


def shoot(html_text, name):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=ROOT) as f:
        f.write(html_text)
        tmp = f.name
    out = os.path.join(OUT, name + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                    "--virtual-time-budget=6000", f"--screenshot={out}", "file://" + tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)
    print("wrote", os.path.relpath(out, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    fig = lambda f: f'<div class="r"><img src="file://{ROOT}/assets/img/research/{f}.png"></div>'
    headshot = f'<div class="r" style="padding:0"><img src="file://{ROOT}/assets/img/headshot-720.jpg" style="width:100%;height:100%;max-height:none;object-fit:cover"></div>'
    shoot(page('<span class="chip">MS Financial Engineering, NYU Tandon, 2027</span>', C.HERO["tagline"],
               "Rates, equity factors, volatility and market structure. A journal submission, three SSRN preprints, and an MS thesis on the US sovereign debt doom loop.",
               headshot), "home")
    shoot(page('<span class="chip">MS thesis, in progress</span>', "The U.S. Sovereign Debt Doom Loop",
               "A point-in-time framework for identification, market pricing, and policy response. Advisor: Prof. David Shimko.",
               headshot), "thesis")
    for p in C.PAPERS:
        f0 = p["figures"][0][0]
        right = fig(f0) if not f0.startswith("svg:") else headshot
        kind = {"journal": "", "ssrn": " ssrn", "working": " working"}[p["chip_kind"]]
        shoot(page(f'<span class="chip{kind}">{html.escape(p["chip"])}</span>', p["short"], p["card_finding"], right), p["slug"])


if __name__ == "__main__":
    main()

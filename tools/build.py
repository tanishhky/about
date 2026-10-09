#!/usr/bin/env python3
"""Build the static site from tools/content.py.

Usage: python3 tools/build.py
Writes index.html, research.html, research/*.html, thesis.html, cv.html, writing.html,
404.html, sitemap.xml, robots.txt and vercel.json into the repository root.
No dependencies beyond the Python standard library.
"""
import hashlib
import html
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import content as C  # noqa: E402

VERSION = "20261009"
S = C.SITE
BASE = S["base"]


def e(text):
    """Escape text and keep short statistics on one line (t = -3.6, 0.51 to 0.89)."""
    out = html.escape(text, quote=True)
    out = re.sub(r"\b([tp]) = (-?\d)", r"\1&nbsp;=&nbsp;\2", out)
    out = re.sub(r"(\d) (to|vs) (-?\d)", r"\1&nbsp;\2&nbsp;\3", out)
    out = re.sub(r"(-?\d[\d.,]*%?) (pts|bp|pp)\b", r"\1&nbsp;\2", out)
    return out


# ------------------------------------------------------------------ icons
ICON = {
    "pdf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 11v6m0 0-2.5-2.5M12 17l2.5-2.5"/></svg>',
    "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m8 7-5 5 5 5M16 7l5 5-5 5"/></svg>',
    "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
}
MOON = '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
SUN = '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'

NAV = [("Research", "/research"), ("Thesis", "/thesis"), ("Projects", "/projects"), ("CV", "/cv"), ("Writing", "/writing")]


# ------------------------------------------------------------------ layout
def versioned(asset):
    """Append a short content hash so link-preview caches (LinkedIn, Slack, X) fetch a changed image."""
    path = os.path.join(ROOT, asset.lstrip("/"))
    if not os.path.exists(path):
        return asset
    with open(path, "rb") as fh:
        return f"{asset}?v={hashlib.sha256(fh.read()).hexdigest()[:10]}"


def layout(path, title, description, body, og_image="/assets/img/og/home.png", og_type="website", extra_head="", active=None):
    url = BASE + (path if path != "/" else "/")
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if active == label else ""}>{label}</a></li>' for label, href in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}">
<meta name="author" content="Tanishk Yadav">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Tanishk Yadav">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{versioned(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#faf9f6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0f0f13" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
<script>try{{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
{extra_head}<script>try{{var q=location.search;if(/[?&]notrack=1(&|$)/.test(q))localStorage.setItem("notrack","1");if(/[?&]notrack=0(&|$)/.test(q))localStorage.removeItem("notrack");if(localStorage.getItem("notrack")==="1")window["ga-disable-{S["ga"]}"]=true}}catch(e){{}}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={S["ga"]}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{S["ga"]}");</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav-wrap">
    <a class="brand" href="/">Tanishk Yadav</a>
    <nav class="primary-nav" aria-label="Primary"><ul>{nav}</ul></nav>
    <div class="nav-actions">
      <a class="btn btn-small" href="{S["resume"]}">Resume</a>
      <button class="theme-toggle" type="button" aria-label="Switch theme">{MOON}{SUN}</button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-row">
    <span>&copy; {date.today().year} Tanishk Yadav. New York, NY.</span>
    <nav aria-label="Footer">
      <a href="mailto:{S["email"]}">Email</a><a href="{S["linkedin"]}">LinkedIn</a><a href="{S["github"]}">GitHub</a><a href="{S["ssrn"]}">SSRN</a><a href="{S["scholar"]}">Google Scholar</a>
    </nav>
  </div>
</footer>
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ components
def picture(name, alt, cls="", sizes="100vw", loading="lazy"):
    return (
        f'<picture><source srcset="/assets/img/research/{name}.webp" type="image/webp">'
        f'<img src="/assets/img/research/{name}.png" alt="{e(alt)}" class="{cls}" loading="{loading}" decoding="async"></picture>'
    )


def chip(p):
    return f'<span class="chip chip-{p["chip_kind"]}">{e(p["chip"])}</span>'


def regime_svg():
    det = ["CUSUM on z-scored returns", "Cross-sector correlation", "Market breadth", "Return skewness"]
    rows = []
    for i, d in enumerate(det):
        y = 20 + i * 62
        rows.append(f'<rect class="box" x="10" y="{y}" width="240" height="46" rx="9"/><text class="label" x="130" y="{y + 28}" text-anchor="middle">{d}</text>')
        rows.append(f'<path class="arrow" d="M250 {y + 23} C 300 {y + 23}, 300 136, 330 136"/>')
    return f"""<svg class="schematic" viewBox="0 0 900 280" role="img" aria-label="Four stress detectors feed a max-of-top-2 consensus, which drives sector baskets and a de-risking overlay">
<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#676773"/></marker></defs>
{''.join(rows)}
<rect class="box-accent" x="330" y="96" width="230" height="80" rx="11"/>
<text class="label" x="445" y="128" text-anchor="middle">Max-of-top-2 consensus</text>
<text class="label-sm" x="445" y="151" text-anchor="middle">acts only when two detectors agree</text>
<path class="arrow" d="M560 136 H 610" marker-end="url(#ah)"/>
<rect class="box" x="612" y="40" width="278" height="76" rx="11"/>
<text class="label" x="751" y="72" text-anchor="middle">Sector baskets</text>
<text class="label-sm" x="751" y="95" text-anchor="middle">GARCH-t volatility terciles, OU half-life</text>
<rect class="box" x="612" y="156" width="278" height="76" rx="11"/>
<text class="label" x="751" y="188" text-anchor="middle">Capital-preservation overlay</text>
<text class="label-sm" x="751" y="211" text-anchor="middle">de-risk to implicit cash</text>
<path class="arrow" d="M751 116 V 154" marker-end="url(#ah)"/>
</svg>"""


def thesis_svg():
    return """<svg class="schematic" viewBox="0 0 980 350" role="img" aria-label="Thesis architecture: Treasury auctions and macro vintages feed a debt book and a real-time data layer, which drive two macro engines that answer three questions">
<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#676773"/></marker></defs>
<rect class="box" x="10" y="30" width="230" height="84" rx="11"/>
<text class="label" x="125" y="64" text-anchor="middle">11,000+ Treasury auctions</text>
<text class="label-sm" x="125" y="88" text-anchor="middle">since 1979, bond by bond</text>
<rect class="box" x="10" y="160" width="230" height="84" rx="11"/>
<text class="label" x="125" y="194" text-anchor="middle">39 macro series</text>
<text class="label-sm" x="125" y="218" text-anchor="middle">full revision histories (ALFRED)</text>
<path class="arrow" d="M240 72 H 272" marker-end="url(#ah2)"/>
<path class="arrow" d="M240 202 H 272" marker-end="url(#ah2)"/>
<rect class="box" x="274" y="30" width="216" height="84" rx="11"/>
<text class="label" x="382" y="64" text-anchor="middle">Debt book</text>
<text class="label-sm" x="382" y="88" text-anchor="middle">effective interest cost, rollover</text>
<rect class="box" x="274" y="160" width="216" height="84" rx="11"/>
<text class="label" x="382" y="194" text-anchor="middle">Real-time data layer</text>
<text class="label-sm" x="382" y="218" text-anchor="middle">as of every historical date</text>
<path class="arrow" d="M490 72 C 515 72, 515 137, 538 137" marker-end="url(#ah2)"/>
<path class="arrow" d="M490 202 C 515 202, 515 137, 538 137" marker-end="url(#ah2)"/>
<rect class="box-accent" x="540" y="84" width="236" height="106" rx="11"/>
<text class="label" x="658" y="118" text-anchor="middle">Two macro engines</text>
<text class="label-sm" x="658" y="142" text-anchor="middle">vector autoregression and</text>
<text class="label-sm" x="658" y="161" text-anchor="middle">regime-switching HMM, on</text>
<text class="label-sm" x="658" y="180" text-anchor="middle">common random numbers</text>
<path class="arrow" d="M776 137 C 794 137, 794 52, 812 52" marker-end="url(#ah2)"/>
<path class="arrow" d="M776 137 H 812" marker-end="url(#ah2)"/>
<path class="arrow" d="M776 137 C 794 137, 794 222, 812 222" marker-end="url(#ah2)"/>
<rect class="box" x="814" y="26" width="156" height="52" rx="9"/><text class="label" x="892" y="57" text-anchor="middle">Identification</text>
<rect class="box" x="814" y="111" width="156" height="52" rx="9"/><text class="label" x="892" y="142" text-anchor="middle">Market pricing</text>
<rect class="box" x="814" y="196" width="156" height="52" rx="9"/><text class="label" x="892" y="227" text-anchor="middle">Policy response</text>
<text class="label-sm" x="490" y="300" text-anchor="middle">Every assumption tested out of sample or stated as a literature range; invariance tests bar lookahead; infeasible paths are reported, never clipped.</text>
</svg>"""


def figure(fig_id, caption, n, loading="lazy"):
    if fig_id == "svg:regime":
        inner = regime_svg()
    else:
        inner = picture(fig_id, caption, loading=loading)
    return f'<figure class="figure">{inner}<figcaption><span class="fig-no">Figure {n}.</span> {e(caption)}</figcaption></figure>'


def thumb(p):
    fid = p["figures"][0][0]
    inner = regime_svg() if fid == "svg:regime" else picture(fid, p["figures"][0][1])
    return f'<div class="thumb">{inner}</div>'


def paper_card(p, thumbnail=True):
    links = [f'<a href="/research/{p["slug"]}">Read the paper</a>', f'<a href="{p["pdf"]}">PDF</a>']
    return f"""<article class="card">
  {f'<a href="/research/{p["slug"]}" tabindex="-1" aria-hidden="true">{thumb(p)}</a>' if thumbnail else ''}
  <div class="card-body">
    <div class="card-meta">{chip(p)}<span>{e(p["date"])}</span></div>
    <h3><a href="/research/{p["slug"]}">{e(p["short"])}</a></h3>
    <p>{e(p["card_finding"])}</p>
    <div class="card-links">{"".join(links)}</div>
  </div>
</article>"""


def project_card(pr):
    return f"""<article class="card">
  <div class="card-body">
    <div class="card-meta"><span class="chip chip-plain">{e(pr["tag"])}</span></div>
    <h3><a href="/projects/{pr["slug"]}">{e(pr["short"])}</a></h3>
    <p>{e(pr["card"])}</p>
    <div class="card-links"><a href="/projects/{pr["slug"]}">See the project</a></div>
  </div>
</article>"""


def any_card(slug):
    for p in C.PAPERS:
        if p["slug"] == slug:
            return paper_card(p, thumbnail=False)
    for pr in C.PROJECTS:
        if pr["slug"] == slug:
            return project_card(pr)
    raise KeyError(slug)


def contact_section():
    return f"""<section class="contact" id="contact">
  <div class="wrap contact-grid">
    <div>
      <p class="kicker">Contact</p>
      <h2>Hiring for quantitative research in 2027?</h2>
      <p class="muted" style="margin-top:14px">I am graduating in May 2027 and looking for full-time quantitative research roles. The fastest way to reach me is email.</p>
      <div class="actions" style="margin-top:22px">
        <a class="btn btn-primary" href="mailto:{S["email"]}">{ICON["mail"]} {S["email"]}</a>
        <a class="btn" href="{S["resume"]}">{ICON["pdf"]} Resume (PDF)</a>
      </div>
    </div>
    <ul class="link-list">
      <li><a href="{S["linkedin"]}">LinkedIn <span class="mono">in/tanishkyadav</span></a></li>
      <li><a href="{S["github"]}">GitHub <span class="mono">tanishhky</span></a></li>
      <li><a href="{S["ssrn"]}">SSRN author page <span class="mono">3 preprints</span></a></li>
      <li><a href="{S["scholar"]}">Google Scholar <span class="mono">profile</span></a></li>
    </ul>
  </div>
</section>"""


def person_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Tanishk Yadav",
        "url": BASE + "/",
        "image": BASE + "/assets/img/headshot-720.jpg",
        "email": "mailto:" + S["email"],
        "jobTitle": "MS Financial Engineering candidate",
        "affiliation": {"@type": "CollegeOrUniversity", "name": "New York University, Tandon School of Engineering"},
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "New York University"},
            {"@type": "CollegeOrUniversity", "name": "SRM University-AP"},
        ],
        "knowsAbout": ["Quantitative finance", "Time-series econometrics", "Fixed income", "Volatility", "Factor models", "Point-in-time data engineering"],
        "sameAs": [S["linkedin"], S["github"], S["ssrn"], S["scholar"]],
    }
    return '<script type="application/ld+json">' + json.dumps(data) + "</script>\n"


# ------------------------------------------------------------------ pages
def page_home():
    H = C.HERO
    feat = C.PAPERS[0]
    others = C.PAPERS[1:]
    stats = "".join(f'<div class="stat"><div class="stat-num">{e(n)}</div><div class="stat-label">{e(l)}</div></div>' for n, l in H["stats"])
    pillars = "".join(f'<div class="pillar"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in C.THESIS["pillars"])
    scale = "".join(f'<div class="stat"><div class="stat-num">{e(n)}</div><div class="stat-label">{e(l)}</div></div>' for n, l in C.THESIS["scale"])
    systems = "".join(project_card(pr) for pr in C.PROJECTS)
    principles = "".join(f'<div class="principle"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in C.PRINCIPLES)
    exp = C.EXPERIENCE[0]
    posts = "".join(
        f'<article class="card"><div class="card-body"><div class="card-meta"><span class="chip chip-plain">{e(p["venue"])}</span><span>{e(p["date"])}</span></div>'
        f'<h3><a href="{p["url"]}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in C.POSTS[:2]
    )
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">{e(H["kicker"])}</p>
      <h1>Tanishk Yadav</h1>
      <p class="tagline">{e(H["tagline"])}</p>
      <p class="lede">{H["lede_html"]}</p>
      <p class="seeking">{e(H["seeking"])}</p>
      <div class="actions">
        <a class="btn btn-primary" href="/research/{feat["slug"]}">Read the latest paper {ICON["arrow"]}</a>
        <a class="btn" href="{S["resume"]}">{ICON["pdf"]} Resume</a>
        <a class="btn" href="mailto:{S["email"]}">{ICON["mail"]} Email</a>
      </div>
    </div>
    <div class="portrait-wrap">
      <picture><source srcset="/assets/img/headshot-720.webp" type="image/webp"><img class="portrait" src="/assets/img/headshot-720.jpg" alt="Portrait of Tanishk Yadav" width="720" height="720" fetchpriority="high"></picture>
    </div>
  </div>
  <div class="wrap"><div class="stats" role="list">{stats.replace('class="stat"', 'class="stat" role="listitem"')}</div></div>
</section>

<section id="latest">
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Latest research</p><h2>The newest paper</h2></div></div>
    <article class="card feature">
      <a class="thumb" href="/research/{feat["slug"]}" tabindex="-1" aria-hidden="true">{picture(feat["figures"][0][0], feat["figures"][0][1], loading="eager")}</a>
      <div class="card-body">
        <div class="card-meta">{chip(feat)}<span>{e(feat["date"])}</span></div>
        <h3><a href="/research/{feat["slug"]}">{e(feat["short"])}</a></h3>
        <p class="question">{e(feat["question"])}</p>
        <p class="finding">{e(feat["card_finding"])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="/research/{feat["slug"]}">Read the paper {ICON["arrow"]}</a>
          <a class="btn" href="{feat["pdf"]}">{ICON["pdf"]} PDF</a>
        </div>
      </div>
    </article>
  </div>
</section>

<section id="research">
  <div class="wrap">
    <div class="section-head">
      <div><p class="kicker">Research</p><h2>Papers, each with its code</h2>
      <p>Two more SSRN preprints and two working papers, alongside the paper above. Every result is out of sample, and every paper reports what did not work.</p></div>
      <a class="section-link" href="/research">All research {ICON["arrow"].replace('<svg', '<svg style="width:15px;height:15px;display:inline;vertical-align:-2px"')}</a>
    </div>
    <div class="grid-2">{"".join(paper_card(p) for p in others)}</div>
  </div>
</section>

<section class="band" id="thesis">
  <div class="wrap">
    <p class="kicker">Master's thesis, in progress</p>
    <h2 class="thesis-title">{e(C.THESIS["title"])}</h2>
    <p>{e(C.THESIS["meta"])}</p>
    <div class="pillars">{pillars}</div>
    <div class="scale">{scale}</div>
    <div class="actions"><a class="btn btn-primary" href="/thesis">About the thesis {ICON["arrow"]}</a></div>
  </div>
</section>

<section id="projects">
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Projects</p><h2>The engineering underneath</h2>
    <p>Research is only as honest as its data pipeline. These are the engines and live systems behind the papers.</p></div>
    <a class="section-link" href="/projects">All projects {ICON["arrow"].replace('<svg', '<svg style="width:15px;height:15px;display:inline;vertical-align:-2px"')}</a></div>
    <div class="grid-2">{systems}</div>
  </div>
</section>

<section id="principles">
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">How I work</p><h2>Three rules every project follows</h2></div></div>
    <div class="grid-3 principles">{principles}</div>
  </div>
</section>

<section id="teaching">
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Teaching and experience</p><h2>{e(exp["org"])}</h2></div>
    <a class="section-link" href="/cv">Full CV {ICON["arrow"].replace('<svg', '<svg style="width:15px;height:15px;display:inline;vertical-align:-2px"')}</a></div>
    <div class="timeline">
      {"".join(f'<div class="tl-item"><div class="tl-when">{e(w)}</div><div><h3>{e(r)}</h3></div></div>' for r, w in exp["roles"])}
    </div>
    <ul class="prose" style="margin-top:22px">{"".join(f"<li>{e(pt)}</li>" for pt in exp["points"])}</ul>
  </div>
</section>

<section id="writing">
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Writing</p><h2>Notes and teardowns</h2></div>
    <a class="section-link" href="/writing">All writing {ICON["arrow"].replace('<svg', '<svg style="width:15px;height:15px;display:inline;vertical-align:-2px"')}</a></div>
    <div class="grid-2">{posts}</div>
  </div>
</section>

{contact_section()}
"""
    return layout(
        "/",
        "Tanishk Yadav: Quantitative Research",
        "MS Financial Engineering at NYU Tandon (May 2027). Point-in-time quantitative research across rates, equity factors, volatility and market structure: three SSRN preprints, two working papers, and an MS thesis on the US sovereign debt doom loop.",
        body,
        extra_head=person_jsonld(),
    )


def page_research_index():
    items = "".join(paper_card(p) for p in C.PAPERS)
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="kicker">Research</p>
    <h1>Research</h1>
    <p class="lede" style="margin-top:16px">Five papers across market structure, rates, factor investing, volatility, and risk overlays. Each links its full PDF and its code. Status words are exact: SSRN preprints and working papers are not peer reviewed.</p>
  </div>
</section>
<section style="padding-top:8px;border-top:0">
  <div class="wrap"><div class="grid-2">{items}</div></div>
</section>
<section class="band">
  <div class="wrap">
    <p class="kicker">In progress</p>
    <h2 class="thesis-title">{e(C.THESIS["title"])}</h2>
    <p>{e(C.THESIS["meta"])}</p>
    <div class="actions" style="margin-top:22px"><a class="btn btn-primary" href="/thesis">About the thesis {ICON["arrow"]}</a></div>
  </div>
</section>
"""
    return layout("/research", "Research: Tanishk Yadav",
                  "Papers by Tanishk Yadav on S&P 500 sector connectedness, Fed-decision forecasting, volatility-managed factors, the variance risk premium, and regime detection, each with PDF and code.",
                  body, active="Research")


def citation_meta(p):
    tags = [
        ("citation_title", p["title"]),
        ("citation_author", "Yadav, Tanishk"),
        ("citation_publication_date", p["pub_date"]),
        ("citation_pdf_url", BASE + p["pdf"]),
        ("citation_abstract_html_url", BASE + "/research/" + p["slug"]),
        ("citation_language", "en"),
    ]
    if p["chip_kind"] == "working":
        tags.append(("citation_technical_report_institution", "NYU Tandon School of Engineering"))
    for k in p["keywords"]:
        tags.append(("citation_keywords", k))
    meta = "".join(f'<meta name="{k}" content="{e(v)}">\n' for k, v in tags)
    ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": p["title"][:110],
        "name": p["title"],
        "author": {"@type": "Person", "name": "Tanishk Yadav", "url": BASE + "/"},
        "datePublished": p["pub_date"].replace("/", "-"),
        "abstract": p["abstract"],
        "keywords": ", ".join(p["keywords"]),
        "url": BASE + "/research/" + p["slug"],
        "encoding": {"@type": "MediaObject", "contentUrl": BASE + p["pdf"], "encodingFormat": "application/pdf"},
        "creativeWorkStatus": p["chip"],
    }
    return meta + '<script type="application/ld+json">' + json.dumps(ld) + "</script>\n"


def page_paper(p):
    others = [q for q in C.PAPERS if q["slug"] != p["slug"]]
    actions = [f'<a class="btn btn-primary" href="{p["pdf"]}">{ICON["pdf"]} Download PDF</a>']
    if p["ssrn"]:
        actions.append(f'<a class="btn" href="{p["ssrn"]}">{ICON["ext"]} SSRN</a>')
    actions.append(f'<a class="btn" href="{p["code"]}">{ICON["code"]} Code</a>')
    actions.append('<a class="btn" href="#cite">Cite</a>')
    results = "".join(f'<div class="result"><div class="result-num">{e(n)}</div><div class="result-label">{e(l)}</div></div>' for n, l in p["results"])
    figs = p["figures"]
    first_fig = figure(figs[0][0], figs[0][1], 1, loading="eager")
    rest_figs = "".join(f'<div style="margin-top:28px">{figure(f, c, i + 2)}</div>' for i, (f, c) in enumerate(figs[1:]))
    tags = "".join(f'<span class="chip chip-plain">{e(k)}</span>' for k in p["keywords"])
    jel = f'<p class="small" style="margin-top:12px">JEL: {e(p["jel"])}</p>' if p["jel"] else ""
    bib_id = "bib-" + p["slug"]
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="crumbs"><a href="/research">Research</a> / {e(p["short"])}</p>
    <div class="card-meta">{chip(p)}<span class="status-line">{e(p["status"])}</span></div>
    <h1>{e(p["title"])}</h1>
    <p class="byline"><a href="/">Tanishk Yadav</a>, NYU Tandon School of Engineering, {e(p["date"])}</p>
    <div class="actions">{"".join(actions)}</div>
  </div>
</section>
<section style="padding-top:0;border-top:0">
  <div class="wrap">
    <p class="question narrow">{e(p["question"])}</p>
    <div class="block"><h2>Key results</h2><div class="results n{len(p["results"])}">{results}</div></div>
    <div class="block">{first_fig}</div>
    <div class="block"><h2>Abstract</h2><p class="abstract">{e(p["abstract"])}</p></div>
    {f'<div class="block">{rest_figs}</div>' if rest_figs else ''}
    <div class="block prose"><h2>Methods</h2><ul>{"".join(f"<li>{e(m)}</li>" for m in p["methods"])}</ul></div>
    <div class="block prose"><h2>What it does not show</h2><ul>{"".join(f"<li>{e(l)}</li>" for l in p["limits"])}</ul></div>
    <div class="block"><div class="tags">{tags}</div>{jel}</div>
    <div class="block" id="cite">
      <h2>Cite</h2>
      <details class="cite" open><summary>BibTeX</summary><pre id="{bib_id}">{e(p["bibtex"])}</pre>
      <div class="copy-row"><button class="btn btn-small" type="button" data-copy="{bib_id}" hidden>Copy BibTeX</button></div></details>
    </div>
    <div class="block">
      <div class="author-box">
        <picture><source srcset="/assets/img/headshot-720.webp" type="image/webp"><img src="/assets/img/headshot-720.jpg" alt="" loading="lazy"></picture>
        <div>
          <h3>Tanishk Yadav</h3>
          <p>MS Financial Engineering at NYU Tandon, graduating May 2027, and looking for full-time quantitative research roles. My master's thesis measures, in real time, when US debt dynamics turn self-reinforcing.</p>
          <div class="actions"><a class="btn btn-small btn-primary" href="/">See all my work</a><a class="btn btn-small" href="/thesis">The thesis</a><a class="btn btn-small" href="{S["resume"]}">Resume</a></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">More research</p><h2>Other papers</h2></div></div>
    <div class="grid-2">{"".join(paper_card(q) for q in others)}</div>
  </div>
</section>
"""
    return layout(f"/research/{p['slug']}", f"{p['short']}: Tanishk Yadav", p["card_finding"], body,
                  og_image=f"/assets/img/og/{p['slug']}.png", og_type="article", extra_head=citation_meta(p), active="Research")


def page_projects_index():
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="kicker">Projects</p>
    <h1>Projects</h1>
    <p class="lede" style="margin-top:16px">The engines and live systems behind the research. Each page explains what the system does, how it is built, what it does not show, and links its code.</p>
  </div>
</section>
<section style="padding-top:8px;border-top:0">
  <div class="wrap"><div class="grid-2">{"".join(project_card(pr) for pr in C.PROJECTS)}</div></div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Research</p><h2>The papers these systems support</h2></div>
    <a class="section-link" href="/research">All research</a></div>
    <div class="grid-2">{"".join(paper_card(p) for p in C.PAPERS[:2])}</div>
  </div>
</section>
"""
    return layout("/projects", "Projects: Tanishk Yadav",
                  "Point-in-time data engines, backtests and live paper-trading systems by Tanishk Yadav, each with its code.",
                  body, active="Projects")


def page_project(pr):
    facts = "".join(f'<div class="result"><div class="result-num">{e(n)}</div><div class="result-label">{e(l)}</div></div>' for n, l in pr["facts"])
    extra = "".join(f'<a class="btn" href="{u}">{ICON["ext"]} {e(t)}</a>' for t, u in pr["extra_links"])
    related = "".join(any_card(r) for r in pr["related"])
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="crumbs"><a href="/projects">Projects</a> / {e(pr["short"])}</p>
    <div class="card-meta"><span class="chip chip-plain">{e(pr["tag"])}</span></div>
    <h1>{e(pr["name"])}</h1>
    <p class="byline"><a href="/">Tanishk Yadav</a>, NYU Tandon School of Engineering</p>
    <div class="actions"><a class="btn btn-primary" href="{pr["github"]}">{ICON["code"]} Code on GitHub</a>{extra}</div>
  </div>
</section>
<section style="padding-top:0;border-top:0">
  <div class="wrap">
    <p class="question narrow">{e(pr["lede"])}</p>
    <div class="block"><h2>Key facts</h2><div class="results n{len(pr["facts"])}">{facts}</div></div>
    <div class="block prose"><h2>How it works</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in pr["points"])}</ul></div>
    <div class="block prose"><h2>Built with</h2><p>{e(pr["stack"])}</p></div>
    <div class="block prose"><h2>What it does not show</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in pr["limits"])}</ul></div>
    <div class="block">
      <div class="author-box">
        <picture><source srcset="/assets/img/headshot-720.webp" type="image/webp"><img src="/assets/img/headshot-720.jpg" alt="" loading="lazy"></picture>
        <div>
          <h3>Tanishk Yadav</h3>
          <p>MS Financial Engineering at NYU Tandon, graduating May 2027, and looking for full-time quantitative research roles. My master's thesis measures, in real time, when US debt dynamics turn self-reinforcing.</p>
          <div class="actions"><a class="btn btn-small btn-primary" href="/">See all my work</a><a class="btn btn-small" href="/thesis">The thesis</a><a class="btn btn-small" href="{S["resume"]}">Resume</a></div>
        </div>
      </div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Related</p><h2>Related work</h2></div></div>
    <div class="grid-2">{related}</div>
  </div>
</section>
"""
    return layout(f"/projects/{pr['slug']}", f"{pr['short']}: Tanishk Yadav", pr["card"], body,
                  og_image=f"/assets/img/og/{pr['slug']}.png", active="Projects")


def page_thesis():
    T = C.THESIS
    pillars = "".join(f'<div class="pillar"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in T["pillars"])
    scale = "".join(f'<div class="result"><div class="result-num">{e(n)}</div><div class="result-label">{e(l)}</div></div>' for n, l in T["scale"])
    built_on = [C.PAPERS[1], C.PAPERS[0], C.PAPERS[3]]
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <div class="card-meta"><span class="chip chip-journal">MS thesis, in progress</span><span class="status-line">Expected May 2027</span></div>
    <h1>{e(T["title"])}</h1>
    <p class="byline"><a href="/">Tanishk Yadav</a>, NYU Tandon School of Engineering. Advisor: <a href="{S["shimko"]}">Prof. David Shimko</a>.</p>
  </div>
</section>
<section style="padding-top:0;border-top:0">
  <div class="wrap">
    <p class="question narrow">{e(T["question"])}</p>
    <p class="abstract" style="margin-top:18px">{e(T["framing"])}</p>
    <div class="block"><h2>Three questions, one framework</h2><div class="pillars pillars-light">{pillars}</div></div>
    <div class="block"><figure class="figure">{thesis_svg()}<figcaption><span class="fig-no">Architecture.</span> How the pieces connect. The figure describes the method; it reports no results.</figcaption></figure></div>
    <div class="block"><h2>Scale</h2><div class="results n4">{scale}</div></div>
    <div class="block prose"><h2>How the work is held to account</h2><ul>{"".join(f"<li>{e(r)}</li>" for r in T["rigor"])}</ul></div>
    <div class="block"><p class="note" style="border-left-color:var(--accent);background:var(--accent-soft)">{e(T["results_note"])}</p></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><p class="kicker">Built on</p><h2>The research that led here</h2>
    <p>The thesis combines methods developed in these papers: first-release macro data, time-varying econometrics, and the volatility risk premium.</p></div></div>
    <div class="grid-3">{"".join(paper_card(q) for q in built_on)}</div>
  </div>
</section>
"""
    return layout("/thesis", "Master's Thesis: The U.S. Sovereign Debt Doom Loop",
                  "An MS thesis by Tanishk Yadav (NYU Tandon, advisor Prof. David Shimko): a point-in-time framework for identifying, pricing, and responding to a self-reinforcing US debt loop.",
                  body, og_image="/assets/img/og/thesis.png", active="Thesis")


def page_cv():
    edu = ""
    for ed in C.EDUCATION:
        prog = f'<p class="small" style="margin:14px 0 0">In progress, Fall 2026</p><ul class="course-list progress">{"".join(f"<li>{e(c)}</li>" for c in ed["in_progress"])}</ul>' if ed["in_progress"] else ""
        edu += f"""<div class="tl-item"><div class="tl-when">{e(ed["dates"])}</div><div>
<h3>{e(ed["school"])}</h3><p class="tl-org">{e(ed["degree"])}, {e(ed["place"])}</p>
<ul>{"".join(f"<li>{e(n)}</li>" for n in ed["notes"])}</ul>
<p class="small" style="margin:14px 0 0">Selected coursework</p><ul class="course-list">{"".join(f"<li>{e(c)}</li>" for c in ed["coursework"])}</ul>{prog}
</div></div>"""
    exp = ""
    for x in C.EXPERIENCE:
        multi = len(x["roles"]) > 1
        roles = "".join(f'<h3>{e(r)}</h3>' + (f'<p class="small" style="margin:2px 0 8px">{e(w)}</p>' if multi else '') for r, w in x["roles"])
        exp += f"""<div class="tl-item"><div class="tl-when">{e(x["span"])}</div><div>
{roles}<p class="tl-org">{e(x["org"])}, {e(x["place"])}</p><ul>{"".join(f"<li>{e(pt)}</li>" for pt in x["points"])}</ul></div></div>"""
    pubs = "".join(
        f'<li><a class="pub-title" href="/research/{p["slug"]}">{e(p["title"])}</a><br><span class="small">{e(p["status"])}</span></li>'
        for p in C.PAPERS
    )
    skills = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in C.SKILLS)
    certs = "".join(
        f'<a class="cert" href="/{img}"><img src="/{img}" alt="" loading="lazy"><span>{e(n)}{f"<small>{e(d)}</small>" if d else ""}</span></a>'
        for n, d, img in C.CERTS
    )
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="kicker">Curriculum vitae</p>
    <h1>CV</h1>
    <p class="lede" style="margin-top:16px">The full record behind the one-page resume.</p>
    <div class="actions" style="margin-top:20px"><a class="btn btn-primary" href="{S["resume"]}">{ICON["pdf"]} Download the one-page resume</a></div>
  </div>
</section>
<div class="wrap">
  <div class="cv-section cv-grid"><h2>Education</h2><div class="timeline">{edu}</div></div>
  <div class="cv-section cv-grid"><h2>Thesis</h2><div><h3><a href="/thesis" style="color:var(--ink);text-decoration:none">{e(C.THESIS["title"])}</a></h3><p class="tl-org">{e(C.THESIS["meta"])}</p></div></div>
  <div class="cv-section cv-grid"><h2>Research</h2><ul class="pub-list">{pubs}</ul></div>
  <div class="cv-section cv-grid"><h2>Projects</h2><ul class="pub-list">{"".join(f'<li><a class="pub-title" href="/projects/{pr["slug"]}">{e(pr["name"])}</a><br><span class="small">{e(pr["tag"])}</span></li>' for pr in C.PROJECTS)}</ul></div>
  <div class="cv-section cv-grid"><h2>Experience</h2><div class="timeline">{exp}</div></div>
  <div class="cv-section cv-grid"><h2>Skills</h2><dl class="skills" style="margin:0">{skills}</dl></div>
  <div class="cv-section cv-grid"><h2>Certifications</h2><div class="certs">{certs}</div></div>
</div>
{contact_section()}
"""
    return layout("/cv", "CV: Tanishk Yadav",
                  "Education, research, experience, skills and certifications of Tanishk Yadav, MS Financial Engineering at NYU Tandon (May 2027).",
                  body, active="CV")


def page_writing():
    items = ""
    for p in C.POSTS:
        note = f'<p class="note">{e(p["note"])}</p>' if p["note"] else ""
        items += f"""<article class="post">
<a href="{p["url"]}" tabindex="-1" aria-hidden="true"><img src="/{p["image"]}" alt="" loading="lazy"></a>
<div><div class="card-meta"><span class="chip chip-plain">{e(p["venue"])}</span><span>{e(p["date"])}</span><span>{p["minutes"]} min read</span></div>
<h3><a href="{p["url"]}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p>{note}</div>
</article>"""
    body = f"""
<section class="paper-head">
  <div class="wrap">
    <p class="kicker">Writing</p>
    <h1>Writing</h1>
    <p class="lede" style="margin-top:16px">Teardowns of my own projects, including what is wrong with them, and plain-English explainers.</p>
  </div>
</section>
<section style="padding-top:8px;border-top:0"><div class="wrap narrow post-list">{items}</div></section>
"""
    return layout("/writing", "Writing: Tanishk Yadav", "Project teardowns and plain-English finance explainers by Tanishk Yadav.", body, active="Writing")


def page_404():
    body = """
<section class="paper-head" style="min-height:50vh">
  <div class="wrap narrow">
    <p class="kicker">404</p>
    <h1>That page does not exist.</h1>
    <p class="lede" style="margin-top:16px">The site was rebuilt in September 2026, so an old link may have moved.</p>
    <div class="actions" style="margin-top:22px"><a class="btn btn-primary" href="/">Home</a><a class="btn" href="/research">Research</a><a class="btn" href="/cv">CV</a></div>
  </div>
</section>"""
    return layout("/404", "Page not found: Tanishk Yadav", "This page does not exist.", body, extra_head='<meta name="robots" content="noindex">\n')


# ------------------------------------------------------------------ write
def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    pages = {
        "index.html": page_home(),
        "research.html": page_research_index(),
        "thesis.html": page_thesis(),
        "cv.html": page_cv(),
        "writing.html": page_writing(),
        "404.html": page_404(),
    }
    for p in C.PAPERS:
        pages[f"research/{p['slug']}.html"] = page_paper(p)
    pages["projects.html"] = page_projects_index()
    for pr in C.PROJECTS:
        pages[f"projects/{pr['slug']}.html"] = page_project(pr)
    for rel, text in pages.items():
        for bad in ("—", "–"):
            assert bad not in text, f"dash character in {rel}"
        write(rel, text)

    urls = (["/", "/research", "/projects", "/thesis", "/cv", "/writing"] + [f"/research/{p['slug']}" for p in C.PAPERS]
            + [f"/projects/{pr['slug']}" for pr in C.PROJECTS])
    today = date.today().isoformat()
    sm = "".join(f"<url><loc>{BASE}{u if u != '/' else '/'}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    vercel = {
        "cleanUrls": True,
        "trailingSlash": False,
        "redirects": [
            {"source": "/credentials", "destination": "/cv", "permanent": True},
            {"source": "/credentials.html", "destination": "/cv", "permanent": True},
            {"source": "/resumes/:file*", "destination": "/Tanishk_Yadav_Resume.pdf", "permanent": False},
            {"source": "/resume", "destination": "/Tanishk_Yadav_Resume.pdf", "permanent": False},
            {"source": "/papers", "destination": "/research", "permanent": False},
            {"source": "/systems", "destination": "/projects", "permanent": False},
        ] + [{"source": f"/{alias}", "destination": f"{dest}?via={alias}", "permanent": False} for alias, dest in C.SHORT_LINKS.items()]
        # LinkedIn text links (About, posts, contact info) show their URL, so they use these
        # short tracked forms: tanishkyadav.me/li and tanishkyadav.me/li/<alias>.
        + [{"source": "/li", "destination": "/?" + C.utm("linkedin", "social", "li-profile", "home"), "permanent": False}]
        + [{"source": f"/li/{alias}", "destination": f"{dest}?" + C.utm("linkedin", "social", "li-text", alias), "permanent": False}
           for alias, dest in C.LINKEDIN_TEXT_LINKS.items()],
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
            {"source": "/papers/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=3600"}]},
        ],
    }
    write("vercel.json", json.dumps(vercel, indent=2) + "\n")
    print(f"built {len(pages)} pages")


if __name__ == "__main__":
    main()

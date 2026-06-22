#!/usr/bin/env python3
"""
Generate the static city sheet page (city.html) from data/city.json.
Run from repo root:  python3 build_city.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://newportmaeve.com"
SERIES = "The Newport Maeve Chronicles"
AUTHOR = "Dean Jordanov"

city = json.load(open(os.path.join(ROOT, "data/city.json"), encoding="utf-8"))

# Shared Connect section (kept in sync across all pages)
CONNECT = open(os.path.join(ROOT, "partials/connect.html"), encoding="utf-8").read()

def esc(s):
    return html.escape(str(s), quote=True)

title = city["title"]
tagline = city.get("tagline", "")
general = city.get("general", "")
sheet_img = city.get("sheetImage", "")
districts = city.get("districts", [])
page_url = f"{SITE_URL}/city.html"
og_img = f"{SITE_URL}/{sheet_img}" if sheet_img else f"{SITE_URL}/assets/images/cover.webp"

# District cards: square image frame (with onerror fallback) + name + description
def district_html(d):
    name = esc(d["name"])
    slug = esc(d.get("slug", ""))
    img = d.get("image", "").strip()
    desc = esc(d.get("description", ""))
    if img:
        frame_inner = (
            f'<img src="{esc(img)}" alt="{name}, a district of {esc(title)}" loading="lazy" '
            f'onerror="this.style.display=\'none\';'
            f'this.parentNode.classList.add(\'is-empty\');'
            f'this.parentNode.insertAdjacentHTML(\'beforeend\',\'<span class=&quot;frame-empty&quot;>Coming soon</span>\')">'
        )
    else:
        frame_inner = '<span class="frame-empty">Coming soon</span>'
    return (
        f'<article class="district-card" id="{slug}">\n'
        f'      <div class="district-frame">{frame_inner}</div>\n'
        f'      <div class="district-info">\n'
        f'        <h3 class="district-name">{name}</h3>\n'
        f'        <p class="district-desc">{desc}</p>\n'
        f'      </div>\n'
        f'    </article>'
    )

districts_html = "\n    ".join(district_html(d) for d in districts)

# Place JSON-LD describing the city as a fictional Place within the series
place_ld = {
    "@context": "https://schema.org",
    "@type": "Place",
    "name": title,
    "description": general[:300],
    "url": page_url,
    "image": og_img,
    "subjectOf": {
        "@type": "BookSeries",
        "name": SERIES,
        "author": {"@type": "Person", "name": AUTHOR}
    }
}
ld_json = json.dumps(place_ld, indent=2, ensure_ascii=False)

full_link = ""
if sheet_img:
    full_link = (
        '<div class="city-fulllink">\n'
        f'  <a id="viewMap" data-full="{esc(sheet_img)}" data-alt="{esc(title)} — full city map">'
        'View the full city map &rarr;</a>\n'
        '</div>'
    )

general_paras = "".join(f"<p>{esc(p.strip())}</p>\n      " for p in general.split("\n") if p.strip()) \
    if "\n" in general else f"<p>{esc(general)}</p>"

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="author" content="{esc(AUTHOR)}">
<meta name="description" content="{esc(title)} — the industrial metropolis at the heart of {esc(SERIES)}. Explore its districts: Market, Industrial, NorthPort, Living, Luxury, and the Military Base.">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(SERIES)}">
<meta property="og:title" content="{esc(title)} | {esc(SERIES)}">
<meta property="og:description" content="The industrial metropolis at the heart of {esc(SERIES)} — explore its districts.">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{page_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)} | {esc(SERIES)}">
<meta name="twitter:description" content="The industrial metropolis at the heart of {esc(SERIES)} — explore its districts.">
<meta name="twitter:image" content="{og_img}">
<title>{esc(title)} | {esc(SERIES)}</title>
<link rel="icon" type="image/png" href="/assets/favicon/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/assets/favicon/favicon.svg" />
<link rel="shortcut icon" href="/assets/favicon/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png" />
<script type="application/ld+json">
{ld_json}
</script>
<link rel="stylesheet" href="css/reset.css">
<link rel="stylesheet" href="css/general.css">
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/components/lightbox.css">
<link rel="stylesheet" href="css/components/connect.css">
<link rel="stylesheet" href="css/components/footer.css">
<link rel="stylesheet" href="css/components/city-sheet.css">
<noscript><style>.district-card{{opacity:1 !important;transform:none !important;}}</style></noscript>
</head>
<body>

<nav class="city-nav">
  <a href="index.html" class="nav-logo">NM Chronicles</a>
  <a href="index.html#map" class="nav-back">&larr; Back to Home</a>
</nav>

<header class="city-hero">
  <div class="city-hero-inner">
    <p class="city-eyebrow">{esc(SERIES)} &middot; The World</p>
    <h1 class="city-name">{esc(title)}</h1>
    <p class="city-tagline">{esc(tagline)}</p>
  </div>
</header>

<section class="city-body">
  <p class="section-label">General Information</p>
  <div class="divider"></div>
  <div class="city-general">
    {general_paras}
  </div>
</section>

{full_link}

<section class="districts">
  <p class="districts-label">The City</p>
  <h2 class="districts-title">Districts of {esc(title)}</h2>
  <div class="district-grid">
    {districts_html}
  </div>
</section>

<nav class="city-crosslinks">
  <a href="index.html#map">&larr; Back to home</a>
  <a href="index.html#characters">Characters &rarr;</a>
  <a href="https://newport-maeve.fandom.com/wiki/Newport_Maeve_Chronicles_Wiki" target="_blank" rel="noopener">Fandom Wiki &rarr;</a>
</nav>

{CONNECT}

<div class="lightbox" id="lightbox" aria-hidden="true">
  <button class="lightbox-close" id="lightboxClose" aria-label="Close">&times;</button>
  <img id="lightboxImg" src="" alt="">
  <span class="lightbox-hint">Click outside or &times; to close</span>
</div>

<footer>
  <div>
    <div class="footer-logo">Newport Maeve Chronicles</div>
    <div class="footer-sub">World of Shadows &amp; Power</div>
  </div>
  <div class="footer-credit">Created by {esc(AUTHOR)}<br><span class="footer-copy">&copy; All rights reserved</span></div>
</footer>

<script type="module" src="js/city.js"></script>
</body>
</html>
"""

with open(os.path.join(ROOT, "city.html"), "w", encoding="utf-8") as f:
    f.write(page)
print("wrote city.html with", len(districts), "districts")

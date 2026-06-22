#!/usr/bin/env python3
"""
Generate static character-sheet HTML pages from data/characters.json.
Output: characters/<slug>.html  (one crawlable page per character)
Run from repo root:  python3 build_character_sheets.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://newportmaeve.com"
SERIES = "The Newport Maeve Chronicles"
AUTHOR = "Dean Jordanov"

chars = json.load(open(os.path.join(ROOT, "data/characters.json"), encoding="utf-8"))
os.makedirs(os.path.join(ROOT, "characters"), exist_ok=True)

# Shared Connect section (kept in sync across all pages)
CONNECT = open(os.path.join(ROOT, "partials/connect.html"), encoding="utf-8").read()

def esc(s):
    return html.escape(str(s), quote=True)

def profile_value_html(val):
    if isinstance(val, list):
        items = "".join(f"<li>{esc(v)}</li>" for v in val)
        return f"<ul>{items}</ul>"
    return esc(val)

# Fixed field order per Dean's spec
FIELD_ORDER = ["Name", "Race", "Abilities", "Role", "Age", "Hair", "Eyes", "Affiliations", "Traits"]

def gallery_slot_html(slot):
    label = esc(slot.get("label", ""))
    img = slot.get("image", "").strip()
    if img:
        # Image path is baked in; if the file isn't uploaded yet, onerror swaps
        # to the "Coming soon" frame so visitors never see a broken-image icon.
        inner = (
            f'<img src="../{esc(img)}" alt="{label} of {{name}}" loading="lazy" '
            f'onerror="this.style.display=\'none\';'
            f'this.parentNode.classList.add(\'is-empty\');'
            f'this.parentNode.insertAdjacentHTML(\'beforeend\',\'<span class=&quot;frame-empty&quot;>Coming soon</span>\')">'
        )
        frame_cls = "gallery-frame"
    else:
        inner = '<span class="frame-empty">Coming soon</span>'
        frame_cls = "gallery-frame"
    return label, inner, frame_cls

def build_page(c):
    name = c["name"]
    slug = c["slug"]
    role = c.get("role", "")
    tagline = c.get("tagline") or role
    quote = c.get("quote", "")
    bio = c.get("bio", "")
    profile = c.get("profile", {})
    gallery = c.get("gallery", {})
    sheet_img = c.get("sheetImage") or c.get("image", "")
    page_url = f"{SITE_URL}/characters/{slug}.html"
    og_img = f"{SITE_URL}/{sheet_img}" if sheet_img else f"{SITE_URL}/assets/images/cover.webp"

    # Profile rows
    rows = ""
    for key in FIELD_ORDER:
        if key not in profile:
            continue
        rows += (
            '<div class="profile-row">'
            f'<div class="profile-key">{esc(key)}</div>'
            f'<div class="profile-val">{profile_value_html(profile[key])}</div>'
            '</div>\n        '
        )

    # Gallery: portrait + extra side by side (left-aligned row), turnaround wide below
    def slot_markup(slot_key, wide=False):
        slot = gallery.get(slot_key, {})
        label, inner, frame_cls = gallery_slot_html(slot)
        inner = inner.replace("{name}", esc(name))
        wide_cls = " gallery-slot--wide" if wide else ""
        return (
            f'<div class="gallery-slot{wide_cls}">'
            f'<div class="{frame_cls}">{inner}</div>'
            f'<div class="gallery-label">{label}</div>'
            '</div>'
        )

    row_slots = slot_markup("portrait") + "\n            " + slot_markup("extra")
    turnaround = slot_markup("turnaround", wide=True)
    slots_html = (
        f'<div class="gallery-row">\n            {row_slots}\n          </div>\n          '
        f'{turnaround}'
    )

    # Bio (fallback if empty)
    bio_html = f"<p>{esc(bio)}</p>" if bio else (
        '<p style="color:var(--text-dim); font-style:italic;">Profile in progress. '
        'More on this character will be revealed as the Chronicles unfold.</p>'
    )

    quote_html = f'<div class="sheet-quote">&ldquo;{esc(quote)}&rdquo;</div>' if quote else ""

    # Person JSON-LD, linked to the series
    person_ld = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "description": (bio or f"{name} — {role}, a character from {SERIES}."),
        "url": page_url,
        "image": og_img,
        "subjectOf": {
            "@type": "BookSeries",
            "name": SERIES,
            "author": {"@type": "Person", "name": AUTHOR}
        }
    }
    ld_json = json.dumps(person_ld, indent=2, ensure_ascii=False)

    full_link_html = ""
    if sheet_img:
        full_link_html = (
            '<div class="sheet-fulllink">'
            f'<a id="viewSheet" data-full="../{esc(sheet_img)}" data-alt="{esc(name)} full character sheet">'
            'View the full character sheet &rarr;</a>'
            '</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="author" content="{esc(AUTHOR)}">
<meta name="description" content="{esc(name)} — {esc(role)}. A character from {esc(SERIES)}, a gothic noir fantasy by {esc(AUTHOR)}.">
<link rel="canonical" href="{page_url}">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{esc(SERIES)}">
<meta property="og:title" content="{esc(name)} | {esc(SERIES)}">
<meta property="og:description" content="{esc(name)} — {esc(role)}. A character from {esc(SERIES)}.">
<meta property="og:image" content="{og_img}">
<meta property="og:url" content="{page_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(name)} | {esc(SERIES)}">
<meta name="twitter:description" content="{esc(name)} — {esc(role)}. A character from {esc(SERIES)}.">
<meta name="twitter:image" content="{og_img}">
<title>{esc(name)} | {esc(SERIES)}</title>
<link rel="icon" type="image/png" href="/assets/favicon/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/assets/favicon/favicon.svg" />
<link rel="shortcut icon" href="/assets/favicon/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png" />
<script type="application/ld+json">
{ld_json}
</script>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" href="../css/general.css">
<link rel="stylesheet" href="../css/typography.css">
<link rel="stylesheet" href="../css/components/lightbox.css">
<link rel="stylesheet" href="../css/components/connect.css">
<link rel="stylesheet" href="../css/components/footer.css">
<link rel="stylesheet" href="../css/components/character-sheet.css">
</head>
<body>

<nav class="sheet-nav">
  <a href="../index.html" class="nav-logo">NM Chronicles</a>
  <a href="../index.html#characters" class="nav-back">&larr; All Characters</a>
</nav>

<header class="sheet-hero">
  <div class="sheet-hero-inner">
    <p class="sheet-eyebrow">{esc(SERIES)}</p>
    <h1 class="sheet-name">{esc(name)}</h1>
    <p class="sheet-tagline">{esc(tagline)}</p>
    {quote_html}
  </div>
</header>

<div class="sheet-body">
  <aside class="profile-block">
    <h2>Profile</h2>
    {rows}
  </aside>

  <main class="sheet-main">
    <p class="section-label">Character Info</p>
    <h2 class="section-title">{esc(name)}</h2>
    <div class="divider"></div>
    <div class="sheet-bio">
      {bio_html}
    </div>

    <div class="sheet-gallery">
      {slots_html}
    </div>

    {full_link_html}
  </main>
</div>

<nav class="sheet-crosslinks">
  <a href="../index.html#characters">&larr; Back to all characters</a>
  <a href="https://newport-maeve.fandom.com/wiki/Newport_Maeve_Chronicles_Wiki" target="_blank" rel="noopener">Fandom Wiki &rarr;</a>
  <a href="../index.html#listen">Listen to the Prequel &rarr;</a>
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

<script type="module" src="../js/character-sheet.js"></script>
</body>
</html>
"""

count = 0
for c in chars:
    page = build_page(c)
    out = os.path.join(ROOT, "characters", f"{c['slug']}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    count += 1
    print("wrote characters/%s.html" % c["slug"])

print("Done. %d sheets generated." % count)

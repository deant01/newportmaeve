# The Newport Maeve Chronicles

Official landing page for *The Newport Maeve Chronicles* — a gothic noir fantasy series by Dean Jordanov.

Live site: [newportmaeve.com](https://newportmaeve.com)

## Project structure

```
newportmaeve/
├── index.html              # Main page
├── data/
│   ├── schema.json         # JSON-LD structured data (BookSeries)
│   ├── site.json           # Site URL, prequel links, social links
│   └── characters.json     # Character cards (name, role, quote, image)
├── CNAME                   # Custom domain for GitHub Pages
├── robots.txt
├── sitemap.xml
├── css/
│   ├── reset.css
│   ├── general.css
│   ├── typography.css
│   └── components/         # One file per page section (linked from index.html)
├── js/
│   ├── main.js             # Entry point (DOMContentLoaded)
│   └── components/
│       ├── characters.js
│       ├── site-links.js
│       ├── lightbox.js
│       └── scroll-reveal.js
├── assets/                 # WebP images
└── archive/                # Legacy HTML and source images (not linked from the live page)
```

## Local preview

No build step required. Serve the repo root with any static file server, for example:

```bash
npx serve .
```

Then open `http://localhost:3000` (or the port shown).

## Deployment

Hosted on **GitHub Pages** with a custom domain via `CNAME`.

1. Push changes to the branch configured for Pages (usually `main`).
2. GitHub serves files from the repository root.
3. The custom domain `newportmaeve.com` is set in repository Settings → Pages.

Verification files at the repo root (`25e1fa98….txt`, `yandex_….html`) must stay there for search-engine ownership checks.

## Editing

| What to change | Where |
|----------------|-------|
| Page content | `index.html`, `data/characters.json` |
| SEO / schema | `data/schema.json`, `<head>` in `index.html` |
| Shared URLs | `data/site.json` (applied via `data-site-link` attributes) |
| Section styling | `css/components/<section>.css` (linked in `index.html` `<head>`) |
| Shared tokens & layout | `css/general.css`, `css/typography.css` |
| Images | `assets/images/*.webp` |
| Lightbox / scroll animations | `js/components/lightbox.js`, `js/components/scroll-reveal.js` |
| Character cards / external links | `js/components/characters.js`, `js/components/site-links.js` |

## Archive folder

`archive/` holds superseded HTML and original JPG/PNG assets from earlier versions. These files are **not** linked from the live site, but GitHub Pages will still publish them at `/archive/…` unless you remove them from the repo or change the deploy setup.

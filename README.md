# Pranav Gadekar — Portfolio Website

Source for my UI/UX and product design portfolio: a clean white, Lusion-inspired site with WebGL effects, case studies, explorations and a toolkit.

**Live:** https://claude.ai/artifact/6Y6NJ6si53RupGkyPMLp59

## Deploy

The site is plain static files: **`index.html` at the repo root** plus the other pages, `dc-lite.js` and `assets/`. There's no build step.

- **Vercel:** import the repo and keep the defaults: Framework Preset *Other*, no build command, output directory = repo root.
- **GitHub Pages / Netlify / any static host:** serve the repo root.
- **Locally:** `python3 -m http.server` in the repo root, then open http://localhost:8000.

After editing anything in `pages/`, regenerate the deployable files with `python3 build/build.py` and commit the result.

## What's inside

```
index.html, *.html  Deployable site (generated from pages/ by build/build.py)
dc-lite.js          Small runtime that renders the pages in any browser
build/              build.py and the runtime source
pages/            Source pages, one per page, as made in the design canvas
  Main.dc.html        Home: hero carousel, work grid, capabilities, toolkit, approach, contact, footer
  About.dc.html       About me, "at a glance" bento
  Explorations.dc.html  Graphic design, 3D and games
  Case-Augle.dc.html  Case study 01 — Augle AI interactive website
  Case-Hotel.dc.html  Case study — Q100 Room Inspection App (13 image panels)
  CaseStudy.dc.html   Shared template for Nom Nom, Parallel, StudyPal, Ainaa, Pawssible
  Case-*.dc.html      Small entry pages that load the shared template
  canvas.json         Page index and layout
assets/           Every image and video the pages use, grouped by project
  asset-map.json      Original upload id → file in this repo
source/
  templates/        Page templates with @@key@@ placeholders, plus media-map.json (key → asset)
  scripts/          build2.py (generates the Augle case study) and its base CSS
  q100-panels/      HTML source of the Q100 case-study panels and its images
```

## How the pages work

The source pages are **Design Component** files (`.dc.html`) made in a Claude design canvas. `build/build.py` turns each one
into a normal HTML page and `dc-lite.js` renders it in any browser: templates, loops, conditionals, state and the shared case-study
component. Every asset path points to a file under `assets/`, so nothing depends on private links.

## Projects

- **Augle AI** — interactive 3D factory website · [live site](https://augle-ai-website-working-automation.vercel.app/)
- **Q100** — AI-assisted room inspections for hotel housekeeping (iOS)
- **Nom Nom** — food ordering and delivery app
- **Parallel**, **StudyPal**, **Ainaa**, **Pawssible**
- **Explorations** — graphic design, 3D modelling and animation, Unity games

## Credits

- Overview photo in the Q100 case study: Ashwini Chaudhary (Monty) on [Unsplash](https://unsplash.com) (Unsplash License).
- Tool logos: [Simple Icons](https://simpleicons.org) (CC0).

# Pranav Gadekar — Portfolio Website

Source for my UI/UX and product design portfolio: a clean white, Lusion-inspired site with WebGL effects, case studies, explorations and a toolkit.

**Live:** https://claude.ai/artifact/6Y6NJ6si53RupGkyPMLp59

## What's inside

```
pages/            The site, one file per page (exactly what is live)
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

The pages are **Design Component** files (`.dc.html`) made in a Claude design canvas. They rely on a runtime
(`support.js`) that the canvas provides, so opening them straight from disk shows only the raw markup, not the finished site.
The live link above is the working version.

In this repo every asset path points to a file under `assets/`, so all the media is here and nothing depends on private links.

## Projects

- **Augle AI** — interactive 3D factory website · [live site](https://augle-ai-website-working-automation.vercel.app/)
- **Q100** — AI-assisted room inspections for hotel housekeeping (iOS)
- **Nom Nom** — food ordering and delivery app
- **Parallel**, **StudyPal**, **Ainaa**, **Pawssible**
- **Explorations** — graphic design, 3D modelling and animation, Unity games

## Credits

- Overview photo in the Q100 case study: Ashwini Chaudhary (Monty) on [Unsplash](https://unsplash.com) (Unsplash License).
- Tool logos: [Simple Icons](https://simpleicons.org) (CC0).

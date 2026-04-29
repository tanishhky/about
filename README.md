# Tanishk Yadav — Portfolio

Personal portfolio website for **Tanishk Yadav**, M.S. Financial Engineering at NYU Tandon (May 2027).

**Live:** [about-silk-one.vercel.app](https://about-silk-one.vercel.app)

---

## About

Single-page portfolio showcasing quantitative finance and machine learning projects, selected work experience, and credentials. Actively updated for Summer 2026 quant internship recruiting.

### Pages

| Page | Description |
|------|-------------|
| `index.html` | Main portfolio — hero, about, 9 project cards, experience, skills, contact |
| `credentials.html` | Research publications, graduate coursework, certifications, dual resume downloads |
| `writing.html` | Writing & Notes — coming soon (LinkedIn series scaffold) |

## Tech Stack

- **HTML/CSS/JS** — no build step, no framework
- All CSS is inline `<style>` in each HTML file
- Fonts: Instrument Serif, DM Sans, JetBrains Mono (Google Fonts CDN)
- Palette: `#0a0a0b` background, `#c9a96e` warm gold accent
- Grain overlay via inline SVG filter

## Local Development

```bash
# Option 1: Python
python -m http.server 8080

# Option 2: Node
npx serve .

# Then open http://localhost:8080
```

No build step required — just open `index.html` directly or serve via any static file server.

## Deployment

Deployed on **Vercel** via auto-deploy from the `main` branch. Push to main → live in ~10 seconds.

## Structure

```
about/
├── index.html                    # Main portfolio page
├── credentials.html              # Credentials & resume sub-page
├── writing.html                  # Writing page (multi-series support)
├── resumes/                      # PDF resumes
│   ├── Tanishk_Yadav_Resume_Research.pdf
│   └── Tanishk_Yadav_Resume_QuantDev.pdf
├── scripts/                      # Utility scripts
│   └── new_project.py            # Generates new project SVGs and JS
├── assets/
│   ├── favicon.svg
│   └── img/
│       ├── headshot.jpg          # (user-provided)
│       ├── og-card.png           # OpenGraph share card
│       └── projects/             # Custom SVG project thumbnails
│           ├── chronofund.svg
│           ├── regime-aware-factor.svg
│           └── ...
└── README.md
```

## License

© 2026 Tanishk Yadav. All rights reserved.

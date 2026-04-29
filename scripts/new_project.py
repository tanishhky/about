#!/usr/bin/env python3
import os
import textwrap

def main():
    print("=== Portfolio Project Generator ===")
    print("This script generates a new SVG thumbnail and the JSON block for index.html.\n")

    # Gather inputs
    slug = input("Project Slug (e.g. 'new-strategy', used for SVG filename): ").strip().lower().replace(" ", "-")
    title = input("Project Title (e.g. 'Volatility Trading System'): ").strip()
    repo = input("GitHub Repo (e.g. 'tanishhky/voledge' or leave blank): ").strip()
    tag = input("Category Tag (e.g. 'Quantitative Trading'): ").strip()
    category = input("Filter Category ('quant-research', 'quant-dev', 'ml'): ").strip()
    tech_str = input("Tech Stack (comma separated, e.g. 'Python, HMM, Pandas'): ").strip()
    summary = input("Brief Summary (1-2 sentences for card): ").strip()
    
    print("\nDetailed Description (press Enter twice to finish):")
    detail_lines = []
    while True:
        line = input()
        if not line:
            if detail_lines and detail_lines[-1] == "":
                break
            elif not detail_lines:
                break
        detail_lines.append(line)
    
    # Process inputs
    tech_list = [t.strip() for t in tech_str.split(",") if t.strip()]
    tech_js = "[" + ", ".join(f'"{t}"' for t in tech_list) + "]"
    
    # Clean up detail string for JS (replace newlines with \n)
    # Remove trailing empty lines
    while detail_lines and detail_lines[-1] == "":
        detail_lines.pop()
    detail_js = "\\n".join(detail_lines).replace('"', '\\"')

    # Generate Motif (a simple dot pattern as fallback, but users can edit later)
    # We will use a generic grid motif for new projects
    motif = '<g opacity="0.15" stroke="#8b7444" stroke-width="1" fill="none"><rect x="1040" y="50" width="60" height="60" rx="4"/><line x1="1070" y1="50" x2="1070" y2="110"/><line x1="1040" y1="80" x2="1100" y2="80"/></g>'
    
    svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0a0a0b"/>
      <stop offset="100%" stop-color="#111113"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c9a96e"/>
      <stop offset="100%" stop-color="#8b7444"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="0" y="0" width="1200" height="630" fill="none" stroke="#222226" stroke-width="1"/>
  <!-- Geometric motif -->
  {motif}
  <!-- Accent line -->
  <rect x="60" y="280" width="120" height="3" rx="1.5" fill="url(#accent)"/>
  <!-- Title -->
  <text x="60" y="340" font-family="Georgia, 'Times New Roman', serif" font-size="48" font-weight="400" fill="#e8e6e3" letter-spacing="-1">{title.replace("&", "&amp;")}</text>
  <!-- Subtitle -->
  <text x="60" y="385" font-family="Georgia, 'Times New Roman', serif" font-size="22" font-weight="400" font-style="italic" fill="#8a8a8e">{tag.replace("&", "&amp;")}</text>
  <!-- Tech stack -->
  <text x="60" y="440" font-family="monospace" font-size="14" fill="#55555a" letter-spacing="1">{" · ".join(tech_list).replace("&", "&amp;")}</text>
  <!-- Bottom border -->
  <rect x="0" y="626" width="1200" height="4" fill="url(#accent)" opacity="0.5"/>
</svg>'''

    # Write SVG
    outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "projects")
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    svg_path = os.path.join(outdir, f"{slug}.svg")
    with open(svg_path, 'w') as f:
        f.write(svg_template)

    # Generate JSON block
    json_block = f'''
      {{
        name: "{title}",
        repo: "{repo}",
        tag: "{tag}",
        category: "{category}",
        tech: {tech_js},
        image: "assets/img/projects/{slug}.svg",
        summary: "{summary}",
        detail: "{detail_js}"
      }},'''

    print("\n" + "="*50)
    print(f"✓ Created SVG thumbnail at: assets/img/projects/{slug}.svg")
    print("="*50)
    print("\nCopy and paste this block into the 'const projects = [...]' array in index.html:\n")
    print(json_block)
    print("="*50)

if __name__ == "__main__":
    main()

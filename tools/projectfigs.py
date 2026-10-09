#!/usr/bin/env python3
"""Result figures for project pages, drawn from each project's own output.

  regime-aware   ra-growth, ra-drawdown, ra-relative: the strategy against SPY, 2008 to 2026,
                 from the backtest's daily history (net of the 2/15 fee structure)

Usage:
  python3 tools/projectfigs.py            render assets/img/research/ra-*.png and .webp from tools/carddata/
  python3 tools/projectfigs.py --refresh  rebuild tools/carddata/regime_aware_daily.csv from the sibling repo first

Needs numpy and matplotlib (not the standard library, unlike build.py) and cwebp for the WebP copies.
Run order when charts change: projectfigs.py, then build.py. Every figure prints the numbers its caption
quotes, so a caption can be checked against the data it describes.
"""
import csv
import os
import shutil
import subprocess
import sys

import numpy as np
import matplotlib

matplotlib.use("agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.dates as mdates  # noqa: E402
from matplotlib import font_manager  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(ROOT)))) if ".claude" in ROOT else os.path.dirname(ROOT)
DATA = os.path.join(ROOT, "tools", "carddata", "regime_aware_daily.csv")
OUT = os.path.join(ROOT, "assets", "img", "research")

# Site tokens (see cardfigs.py): the two series colors pass the dataviz validator on white, and every
# chart labels its series directly.
INK, SECOND, MUTED, GRID = "#16161a", "#45454f", "#676773", "#e4e1da"
MINE, OTHER = "#6d28a8", "#2a9d8f"

available = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ("Inter", "Helvetica Neue", "Arial") if f in available), "DejaVu Sans")
plt.rcParams.update({
    "font.family": FONT, "font.size": 12.5, "text.color": SECOND, "axes.edgecolor": GRID, "axes.linewidth": 1,
    "axes.labelcolor": MUTED, "axes.labelsize": 12.5, "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "xtick.major.size": 0, "ytick.major.size": 0,
    "xtick.major.pad": 7, "ytick.major.pad": 7, "axes.unicode_minus": False, "savefig.facecolor": "white",
})


def refresh():
    src = os.path.join(GH, "Regime-Aware-Factor-Backtest", "results", "daily_history.csv")
    with open(src, newline="") as f, open(DATA, "w", newline="") as g:
        w = csv.writer(g)
        w.writerow(["date", "strategy", "spy"])
        for r in csv.DictReader(f):
            w.writerow([r["date"], f"{float(r['portfolio_value']):.2f}", f"{float(r['spy_value']):.2f}"])
    print("wrote", os.path.relpath(DATA, ROOT))


def load():
    with open(DATA, newline="") as f:
        rows = list(csv.DictReader(f))
    d = np.array([r["date"] for r in rows], dtype="datetime64[D]")
    return d, np.array([float(r["strategy"]) for r in rows]), np.array([float(r["spy"]) for r in rows])


def base():
    fig = plt.figure(figsize=(9, 4.5), dpi=200)
    ax = fig.add_axes([0.115, 0.11, 0.70, 0.84])
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    return fig, ax


def label_end(ax, x, y, text, color, dy=0):
    ax.annotate(text, (x, y), xytext=(8, dy), textcoords="offset points", color=color, fontsize=12.5,
                fontweight="bold", va="center", annotation_clip=False)


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    png = os.path.join(OUT, name + ".png")
    fig.savefig(png)
    plt.close(fig)
    if shutil.which("cwebp"):
        subprocess.run(["cwebp", "-quiet", "-q", "88", png, "-o", os.path.join(OUT, name + ".webp")], check=True)
    print("wrote", os.path.relpath(png, ROOT), f"({os.path.getsize(png) // 1024} KB)")


def stamp(d, i):
    return str(d[i].astype("datetime64[M]"))


def main():
    if "--refresh" in sys.argv:
        refresh()
    d, s, b = load()
    x = d.astype("datetime64[ms]").astype(object)
    gs, gb = s / s[0] * 100, b / b[0] * 100
    print(f"period {d[0]} to {d[-1]}, {len(d)} days; growth of 100: strategy {gs[-1]:.0f}, SPY {gb[-1]:.0f}")

    # 1. Growth of 100
    fig, ax = base()
    ax.plot(x, gb, color=OTHER, lw=1.8)
    ax.plot(x, gs, color=MINE, lw=1.8)
    ax.set_ylim(0, 1000)
    ax.set_yticks(range(0, 1001, 200))
    ax.set_ylabel("Value of 100 invested in Feb 2008")
    label_end(ax, x[-1], gs[-1], f"Regime-Aware {gs[-1]:.0f}", MINE, 14)
    label_end(ax, x[-1], gb[-1], f"SPY {gb[-1]:.0f}", OTHER, -14)
    save(fig, "ra-growth")

    # 2. Drawdowns
    ddS = s / np.maximum.accumulate(s) - 1
    ddB = b / np.maximum.accumulate(b) - 1
    iS, iB = int(ddS.argmin()), int(ddB.argmin())
    print(f"max drawdown strategy {ddS[iS]:.4f} on {d[iS]} ({stamp(d, iS)}), SPY {ddB[iB]:.4f} on {d[iB]} ({stamp(d, iB)})")
    fig, ax = base()
    ax.fill_between(x, ddB * 100, 0, color=OTHER, alpha=0.10, lw=0)
    ax.fill_between(x, ddS * 100, 0, color=MINE, alpha=0.10, lw=0)
    ax.plot(x, ddB * 100, color=OTHER, lw=1.0)
    ax.plot(x, ddS * 100, color=MINE, lw=1.0)
    ax.set_ylim(-58, 2)
    ax.set_yticks(range(-50, 1, 10))
    ax.set_yticklabels([f"{v}%" for v in range(-50, 1, 10)])
    ax.set_ylabel("Drawdown from previous peak")
    ax.annotate(f"SPY {ddB[iB] * 100:.1f}%\n{d[iB].astype('datetime64[M]').astype(object):%b %Y}", (x[iB], ddB[iB] * 100),
                xytext=(18, -2), textcoords="offset points", color=OTHER, fontsize=12, fontweight="bold", va="center")
    ax.annotate(f"Regime-Aware {ddS[iS] * 100:.1f}%\n{d[iS].astype('datetime64[M]').astype(object):%b %Y}", (x[iS], ddS[iS] * 100),
                xytext=(-12, -2), textcoords="offset points", color=MINE, fontsize=12, fontweight="bold", va="center", ha="right")
    save(fig, "ra-drawdown")

    # 3. Relative wealth
    rel = (s / b - 1) * 100
    iP = int(rel.argmax())
    print(f"relative wealth peak {rel[iP]:.1f}% on {d[iP]} ({stamp(d, iP)}), final {rel[-1]:.1f}% on {d[-1]}")
    fig, ax = base()
    ax.axhline(0, color=MUTED, lw=1, ls=(0, (4, 4)))
    ax.fill_between(x, rel, 0, color=MINE, alpha=0.16, lw=0)
    ax.plot(x, rel, color=MINE, lw=1.8)
    ax.set_ylim(-10, 150)
    ax.set_yticks(range(0, 121, 20))
    ax.set_yticklabels([f"+{v}%" if v else "0%" for v in range(0, 121, 20)])
    ax.set_ylabel("Wealth relative to SPY")
    ax.annotate(f"Peak +{rel[iP]:.0f}%\n{d[iP].astype('datetime64[M]').astype(object):%b %Y}", (x[iP], rel[iP]), xytext=(0, 10),
                textcoords="offset points", color=MINE, fontsize=12, fontweight="bold", ha="center", va="bottom")
    label_end(ax, x[-1], rel[-1], f"+{rel[-1]:.0f}%", MINE)
    save(fig, "ra-relative")


if __name__ == "__main__":
    main()

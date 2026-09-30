#!/usr/bin/env python3
"""Charts for the social preview cards of pages that have no paper figure.

Each card shows real output from its own project, never the headshot:

  chronofund          10-K filing lags from ChronoFund's filings table
  regime-aware        strategy vs SPY drawdowns from the backtest's daily history
  pinsight            a live SPY risk-neutral density fitted by PinSight's own pipeline
  driftedge           DriftEdge's own empirical-Bayes estimate and Kelly sizer as trades accumulate
  regime-detection    the paper's cross-asset drawdown table (paper.tex, tab:crossasset)
  thesis              public OMB data via FRED (context only, never a thesis result)

Usage:
  python3 tools/cardfigs.py            render assets/img/cards/*.svg from tools/carddata/
  python3 tools/cardfigs.py --refresh  rebuild tools/carddata/ from the sibling repos and the network first

Needs pandas, numpy and matplotlib (not the standard library, unlike build.py). --refresh also needs
pyarrow, the sibling repos next to this one, and PinSight's dependencies (yfinance, scipy, rich; numpy
below 2.4 until PinSight stops calling np.trapz). Run order: cardfigs.py, then og.py, then build.py.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = os.path.dirname(ROOT)
DATA = os.path.join(ROOT, "tools", "carddata")
OUT = os.path.join(ROOT, "assets", "img", "cards")

# Site tokens. The two series colors pass the dataviz validator on white (lightness band, chroma,
# CVD separation, contrast); every chart also labels its series directly.
INK, SECOND, MUTED, GRID = "#16161a", "#45454f", "#676773", "#e4e1da"
MINE, OTHER = "#6d28a8", "#2a9d8f"
W, H = 468, 470  # the card's right panel under its caption, in px (1 pt = 1 px at this size)

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Inter", "font.size": 17, "text.color": SECOND,
    "axes.edgecolor": GRID, "axes.linewidth": 1, "axes.labelcolor": MUTED, "axes.labelsize": 17,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelsize": 16, "ytick.labelsize": 16,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 8, "ytick.major.pad": 8,
    "axes.unicode_minus": False, "svg.hashsalt": "tanishkyadav",
})


def fig_ax():
    fig = plt.figure(figsize=(W / 72, H / 72), dpi=72)
    ax = fig.add_axes([0.17, 0.12, 0.79, 0.84])
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    return fig, ax


def save(fig, slug):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, slug + ".svg")
    fig.savefig(path, format="svg", metadata={"Date": None})
    plt.close(fig)
    print("wrote", os.path.relpath(path, ROOT))


def pct(ax, axis="y", digits=0):
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.{digits}f}%")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


# ---------------------------------------------------------------- refresh (sibling repos + network)
def refresh():
    os.makedirs(DATA, exist_ok=True)
    rab = os.path.join(GH, "Regime-Aware-Factor-Backtest")

    # ChronoFund: days from fiscal year end to the SEC acceptance timestamp, original 10-K filings.
    f = pd.read_parquet(os.path.join(rab, "historical_data", "filings.parquet"))
    f = f[f.form_type == "10-K"].copy()
    f["lag"] = (f.acceptance_datetime.dt.normalize() - pd.to_datetime(f.period_of_report)).dt.days
    f = f.dropna(subset=["lag"])
    f[["ticker", "lag"]].assign(year=f.acceptance_datetime.dt.year).to_csv(
        os.path.join(DATA, "chronofund_10k_lags.csv"), index=False)

    # Regime-Aware: weekly drawdown from peak, strategy (net of 2/15 fees) and SPY.
    d = pd.read_csv(os.path.join(rab, "results", "daily_history.csv"), parse_dates=["date"]).set_index("date")
    dd = pd.DataFrame({c: d[c] / d[c].cummax() - 1 for c in ("portfolio_value", "spy_value")})
    wk = dd.resample("W-FRI").min()
    wk.columns = ["strategy", "spy"]
    wk.round(5).to_csv(os.path.join(DATA, "regime_aware_drawdown.csv"))

    # PinSight: SPY chain from Yahoo, fitted by PinSight's own filter, SVI smile and Breeden-Litzenberger.
    sys.path.insert(0, os.path.join(GH, "PinSight", "src"))
    from datetime import date, datetime, timezone
    from pinsight.data import yahoo
    from pinsight.rnd.density import extract
    expiry = sorted(yahoo.list_expiries("SPY"))[2]
    chain = yahoo.fetch_chain("SPY", date.fromisoformat(expiry))
    spot = float(chain.underlying_price.iloc[0])
    as_of = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    fit = extract(chain, spot=spot, as_of_ts=as_of, expiry_iso=expiry)
    if fit is None:
        raise SystemExit("PinSight rejected the chain; keep the previous snapshot")
    pd.DataFrame({"strike": fit.strikes, "density": fit.density}).iloc[::4].to_csv(
        os.path.join(DATA, "pinsight_rnd.csv"), index=False)
    meta = {"as_of": as_of, "last_quote": str(chain.quote_ts.max()), "expiry": expiry, "spot": spot,
            "T_years": fit.T, "smile_r2": fit.smile_r_squared, "clean_strikes": fit.n_clean_strikes,
            "mean": fit.rnd_mean, "std": fit.rnd_std, "skew": fit.rnd_skew,
            "excess_kurtosis": fit.rnd_kurtosis_excess}
    with open(os.path.join(DATA, "pinsight_rnd.json"), "w") as fh:
        json.dump(meta, fh, indent=1)

    # DriftEdge: the stake its own sizer allows as settled trades accumulate at two hypothetical hit rates.
    sys.path.insert(0, os.path.join(GH, "DriftEdge", "src"))
    from driftedge import calibration, sizing
    c, target, stop, bank = 0.35, 0.60, 0.20, 10_000.0
    p0, a0, b0 = calibration.design_priors(c=c, target=target, stop=stop)
    rows = []
    for hit in (0.45, 0.30):
        for n in range(0, 301, 20):  # multiples of 20, so wins are exact at both hit rates
            wins = int(round(hit * n))
            trades = [{"status": "closed", "trader": "equal", "category": "politics", "entry_price": c,
                       "entry_size_usd": 100.0, "pnl_usd": (100 * a0 if i < wins else -100 * b0),
                       "exit_ts": "2026-01-01T00:00:00+00:00"} for i in range(n)]
            calib = calibration.bet_stats(trades, c=c, target=target, stop=stop, category="politics",
                                          as_of_ts="2026-06-01T00:00:00+00:00")
            state = sizing.TraderState(trader="kelly", bankroll_init=bank, cash_usd=bank, open_exposure=0.0,
                                        closed_pnl=0.0)
            stake = sizing.kelly_size(state, c=c, target=target, stop=stop, calib=calib)
            rows.append({"hit_rate": hit, "trades": n, "p_hat": calib.p_hat, "stake_pct": 100 * stake / bank})
    pd.DataFrame(rows).round(5).to_csv(os.path.join(DATA, "driftedge_sizer.csv"), index=False)
    with open(os.path.join(DATA, "driftedge_sizer.json"), "w") as fh:
        json.dump({"entry": c, "target": target, "stop": stop, "prior_p0": p0,
                   "kelly_fraction": sizing.KELLY_KAPPA, "cap": sizing.MAX_SINGLE_EXPOSURE}, fh, indent=1)

    # Thesis: federal interest outlays over receipts, fiscal years (OMB via FRED).
    fred = pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=FYOINT,FYFR", parse_dates=["observation_date"])
    fred = fred.dropna()
    fred["fy"] = fred.observation_date.dt.year
    fred = fred[fred.fy >= 1979]
    fred["interest_share"] = 100 * fred.FYOINT / fred.FYFR
    fred[["fy", "FYOINT", "FYFR", "interest_share"]].round(3).to_csv(
        os.path.join(DATA, "fred_interest_receipts.csv"), index=False)
    print("refreshed", os.path.relpath(DATA, ROOT))


# ---------------------------------------------------------------- charts
def chronofund():
    f = pd.read_csv(os.path.join(DATA, "chronofund_10k_lags.csv"))
    lag = f.lag.clip(upper=121)
    edges = np.arange(0, 124, 4)
    counts, _ = np.histogram(lag, bins=edges)
    share = 100 * counts / len(lag)
    fig, ax = fig_ax()
    ax.bar(edges[:-1] + 2, share, width=3.2, color=MINE, linewidth=0)
    med = float(f.lag.median())
    ax.axvline(med, color=INK, linewidth=1.5)
    ax.text(med - 4, share.max() * 0.97, f"median {med:.0f} days", color=INK, fontsize=17, va="top", ha="right")
    ax.text(med - 4, share.max() * 0.88, "until then the report\nis invisible to a\nbacktest", color=MUTED,
            fontsize=15, va="top", ha="right")
    ax.set_xlim(0, 124)
    ax.set_xticks([0, 30, 60, 90, 120])
    ax.set_xticklabels(["0", "30", "60", "90", "120+"])
    ax.set_xlabel("Days from fiscal year end to SEC acceptance")
    pct(ax)
    save(fig, "chronofund")
    return {"n": len(f), "companies": int(f.ticker.nunique()), "first": int(f.year.min()),
            "last": int(f.year.max()), "median": med}


def regime_aware():
    d = pd.read_csv(os.path.join(DATA, "regime_aware_drawdown.csv"), parse_dates=["date"]).set_index("date")
    fig, ax = fig_ax()
    ax.fill_between(d.index, 100 * d.spy, 0, color=OTHER, alpha=0.10, linewidth=0)
    ax.plot(d.index, 100 * d.spy, color=OTHER, linewidth=2)
    ax.fill_between(d.index, 100 * d.strategy, 0, color=MINE, alpha=0.10, linewidth=0)
    ax.plot(d.index, 100 * d.strategy, color=MINE, linewidth=2)
    for col, color, name, dx, ha in (("spy", OTHER, "SPY", 12, "left"), ("strategy", MINE, "Strategy", -12, "right")):
        t, v = d[col].idxmin(), 100 * d[col].min()
        ax.plot([t], [v], "o", color=color, markersize=8, markeredgecolor="white", markeredgewidth=2)
        ax.annotate(f"{name} {v:.1f}%", (t, v), xytext=(dx, -4), textcoords="offset points",
                    color=INK, fontsize=17, va="center", ha=ha)
    ax.set_ylim(-58, 2)
    ax.set_xlim(d.index.min(), d.index.max())
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(6))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    pct(ax)
    save(fig, "regime-aware")


def pinsight():
    d = pd.read_csv(os.path.join(DATA, "pinsight_rnd.csv"))
    with open(os.path.join(DATA, "pinsight_rnd.json")) as fh:
        m = json.load(fh)
    # Lognormal with the fitted density's mean and standard deviation, for shape comparison.
    s2 = np.log(1 + (m["std"] / m["mean"]) ** 2)
    mu = np.log(m["mean"]) - s2 / 2
    k = d.strike.to_numpy()
    logn = np.exp(-(np.log(k) - mu) ** 2 / (2 * s2)) / (k * np.sqrt(2 * np.pi * s2))
    dk = np.gradient(k)
    cut = m["mean"] - 3 * m["std"]
    m["p_below_3sd"] = float((d.density[k < cut] * dk[k < cut]).sum())
    m["p_below_3sd_lognormal"] = float((logn[k < cut] * dk[k < cut]).sum())
    fig, ax = fig_ax()
    ax.plot(k, 100 * logn, color=OTHER, linewidth=2)
    ax.fill_between(k, 100 * d.density, 0, color=MINE, alpha=0.10, linewidth=0)
    ax.plot(k, 100 * d.density, color=MINE, linewidth=2)
    ax.axvline(m["spot"], color=INK, linewidth=1)
    top = 100 * d.density.max()
    ax.text(m["spot"] + 1.2, top * 1.33, f"spot {m['spot']:.2f}", color=INK, fontsize=15, ha="left", va="top")
    ax.annotate("implied by\noptions", (m["spot"] + 2, top * 0.97), xytext=(m["spot"] + 9, top * 1.12),
                color=INK, fontsize=16, va="center", arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 1})
    j = int(np.argmin(np.abs(k - (m["mean"] + 1.5 * m["std"]))))
    ax.annotate("lognormal,\nsame mean\nand s.d.", (k[j], 100 * logn[j]), xytext=(m["mean"] + 2.4 * m["std"], top * 0.62),
                color=INK, fontsize=16, ha="center", va="bottom",
                arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 1})
    i = int(np.argmin(np.abs(k - (m["mean"] - 3 * m["std"]))))
    ax.annotate(f"3+ s.d. drop priced\nat {100 * m['p_below_3sd']:.2f}%, vs {100 * m['p_below_3sd_lognormal']:.2f}%\nunder a lognormal",
                (k[i], 100 * d.density.iloc[i]), xytext=(m["mean"] - 4.05 * m["std"], top * 0.98), color=INK,
                fontsize=15, ha="left", va="bottom", arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 1,
                                                                   "relpos": (0.3, 0)})
    ax.set_xlim(m["mean"] - 4.2 * m["std"], m["mean"] + 3.6 * m["std"])
    ax.set_ylim(0, top * 1.35)
    ax.set_xlabel("SPY at expiry")
    pct(ax, digits=1)
    ax.set_ylabel("Probability per $1")
    save(fig, "pinsight")
    return m


def driftedge():
    d = pd.read_csv(os.path.join(DATA, "driftedge_sizer.csv"))
    with open(os.path.join(DATA, "driftedge_sizer.json")) as fh:
        m = json.load(fh)
    p0 = 100 * m["prior_p0"]
    fig, ax = fig_ax()
    ax.axhspan(24, p0, color=GRID, alpha=0.45, linewidth=0)
    ax.axhline(p0, color=INK, linewidth=1.2)
    ax.text(298, p0 - 0.5, f"break-even prior {p0:.1f}%\nat or below: stake is zero", ha="right", va="top",
            color=MUTED, fontsize=15)
    for hit, color, label in ((0.45, MINE, "45% realized:\nbets, at the 2% cap"), (0.30, OTHER, "30% realized:\nnever bets")):
        s = d[d.hit_rate == hit]
        ax.plot(s.trades, 100 * s.p_hat, color=color, linewidth=2.5, solid_capstyle="round")
        ax.plot([s.trades.iloc[-1]], [100 * s.p_hat.iloc[-1]], "o", color=color, markersize=9,
                markeredgecolor="white", markeredgewidth=2)
        ax.text(s.trades.iloc[-1] - 4, 100 * s.p_hat.iloc[-1] + (1.2 if hit > 0.4 else -1.6), label,
                ha="right", va="bottom" if hit > 0.4 else "top", color=INK, fontsize=16)
    ax.set_xlim(0, 300)
    ax.set_ylim(24, 47)
    ax.set_xticks([0, 100, 200, 300])
    pct(ax)
    ax.set_xlabel("Settled trades observed")
    ax.set_ylabel("Estimated win probability")
    save(fig, "driftedge")
    return m


def regime_detection():
    # paper.tex, table tab:crossasset (walk-forward, calibration unchanged from the SPY universe).
    rows = [("Factor", -6.1, -44.4), ("International", -7.3, -58.3), ("Multi-asset", -14.3, -25.1)]
    fig, ax = fig_ax()
    x = np.arange(len(rows))
    for j, (color, off) in enumerate(((MINE, -0.2), (OTHER, 0.2))):
        vals = [r[1 + j] for r in rows]
        ax.bar(x + off, vals, width=0.36, color=color, linewidth=0)
        for xi, v in zip(x + off, vals):
            ax.text(xi, v - 1.2, f"{v:.1f}%", ha="center", va="top", color=INK, fontsize=15)
    ax.axhline(0, color=MUTED, linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_ylim(-68, 1)
    pct(ax)
    for y, color, name in ((0.30, MINE, "Regime-adaptive"), (0.22, OTHER, "Equal weight")):
        ax.plot([0.58, 0.63], [y + 0.012, y + 0.012], transform=ax.transAxes, color=color, linewidth=8)
        ax.text(0.66, y, name, transform=ax.transAxes, ha="left", color=INK, fontsize=16)
    save(fig, "regime-detection")


def thesis():
    d = pd.read_csv(os.path.join(DATA, "fred_interest_receipts.csv"))
    fig, ax = fig_ax()
    ax.fill_between(d.fy, d.interest_share, 0, color=MINE, alpha=0.10, linewidth=0)
    ax.plot(d.fy, d.interest_share, color=MINE, linewidth=2.5)
    old = d[d.fy < 2000].loc[lambda t: t.interest_share.idxmax()]
    last = d.iloc[-1]
    for row, dx, ha in ((old, 0, "center"), (last, -4, "right")):
        ax.plot([row.fy], [row.interest_share], "o", color=MINE, markersize=9, markeredgecolor="white", markeredgewidth=2)
        ax.annotate(f"FY{int(row.fy)}: {row.interest_share:.1f}%", (row.fy, row.interest_share), xytext=(dx, 14),
                    textcoords="offset points", ha=ha, color=INK, fontsize=17)
    ax.set_xlim(d.fy.min(), d.fy.max() + 0.5)
    ax.set_ylim(0, 23)
    ax.set_xticks([1980, 1990, 2000, 2010, 2020])
    pct(ax)
    ax.set_ylabel("Interest outlays / receipts")
    save(fig, "thesis")
    return {"first": int(d.fy.min()), "last": int(last.fy), "last_share": float(last.interest_share),
            "peak_before_2000": (int(old.fy), float(old.interest_share))}


def main():
    if "--refresh" in sys.argv:
        refresh()
    facts = {"chronofund": chronofund(), "pinsight": pinsight(), "driftedge": driftedge(), "thesis": thesis()}
    regime_aware()
    regime_detection()
    with open(os.path.join(DATA, "facts.json"), "w") as fh:
        json.dump(facts, fh, indent=1, default=float)


if __name__ == "__main__":
    main()

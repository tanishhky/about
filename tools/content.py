"""Site content. Every fact here is sourced from SecondBrain/profile.md (verified 2026-09-27).

Rules carried over from the profile:
- Status words are exact: "Journal submission", "SSRN preprint", "Working paper". Nothing is "published".
- Thesis: description only. No results until they are public claims in the thesis claims register.
- No GPA, no GRE. Official titles only. Wiley is "in preparation".
- No em or en dashes anywhere.
Fields ending in _html may contain inline HTML; everything else is escaped by build.py.
"""

SITE = {
    "base": "https://www.tanishkyadav.me",
    "name": "Tanishk Yadav",
    "email": "tanishkyadav@nyu.edu",
    "linkedin": "https://www.linkedin.com/in/tanishkyadav",
    "github": "https://github.com/tanishhky",
    "ssrn": "https://ssrn.com/author=8715020",
    "scholar": "https://scholar.google.com/citations?user=XKyUOj0AAAAJ",
    "resume": "/Tanishk_Yadav_Resume.pdf",
    "ga": "G-87P07T86WH",
    "shimko": "https://www.linkedin.com/in/davidcshimko/",
}

HERO = {
    "kicker": "MS Financial Engineering, NYU Tandon, May 2027",
    "tagline": "Quantitative research that only uses what was knowable at the time.",
    "lede_html": (
        "I work on rates, equity factors, volatility, and market structure, and I build the point-in-time "
        "data engines underneath them. Every result on this site is judged out of sample, and the ones that "
        "did not survive are reported next to the ones that did."
    ),
    "seeking": "Seeking full-time quantitative research roles from summer 2027.",
    "stats": [
        ("1", "journal submission"),
        ("3", "SSRN preprints"),
        ("5", "papers, all with code"),
        ("11,000+", "Treasury auctions in my thesis data"),
    ],
}

PRINCIPLES = [
    ("Point-in-time by construction",
     "Every data read is stamped with the moment it became knowable. Filings are dated to the second the SEC "
     "accepted them, and macro series are read from their full revision histories, so a backtest cannot see "
     "a number before the market did."),
    ("Tests that are allowed to fail",
     "Out-of-sample splits, heteroskedasticity-robust inference, and multiple-testing control. When a better "
     "test kills a result, the result goes, and the correction is published next to the finding."),
    ("Research that ships",
     "Tested code behind every paper, full-stack research platforms, and scheduled live systems, built by one "
     "person who can explain every line."),
]

# ---------------------------------------------------------------- research
PAPERS = [
    {
        "slug": "concentrated-sectors",
        "title": "Concentrated Sectors Transmit Less: Within-Sector Concentration and Time-Varying Connectedness in the S&P 500, 2018 to 2026",
        "short": "Concentrated Sectors Transmit Less",
        "chip": "Journal submission",
        "chip_kind": "journal",
        "status": "Submitted to Studies in Nonlinear Dynamics & Econometrics, September 2026. Not yet peer reviewed.",
        "date": "September 2026",
        "pub_date": "2026/09/23",
        "pdf": "/papers/yadav-2026-concentrated-sectors-transmit-less.pdf",
        "code": "https://github.com/tanishhky/sp500-sector-analysis",
        "ssrn": None,
        "card_finding": "A one-point rise in a sector's top-three share lowers its net shock transmission by 0.47 points (t = -3.6), and none of 110 apparent Granger lead-lag links survives robust tests.",
        "question": "The ten largest firms rose from 24% to 41% of S&P 500 market capitalization between 2018 and 2025. Did that concentration change the way shocks travel between the eleven sectors?",
        "abstract": (
            "The ten largest firms rose from 24% to 41% of S&P 500 market capitalization between 2018 and 2025. "
            "This paper asks how that concentration changed the way shocks travel between the eleven GICS sectors, "
            "using daily returns and range volatilities of the Select Sector SPDR funds from October 2018 to August "
            "2026, a point-in-time constituent panel, and a filtered TVP-VAR connectedness model. Sector "
            "connectedness is contemporaneous: classical Granger tests appear to find 90 of 110 significant links, "
            "but they are oversized under GARCH errors, heteroskedasticity-robust tests leave none, and lagged "
            "cross-sector returns have negative out-of-sample R² for every sector. Total connectedness peaked "
            "at 88.9% in March 2020 and fell to a sample low of 53.7% in August 2026. With sector and month fixed "
            "effects, a one-point rise in a sector's top-three share lowers its net directional connectedness by "
            "0.47 points (t = -3.6), and by 0.66 points on uncapped constituent returns. Concentrated sectors also "
            "co-move less with the rest of the market, consistent with granular firm-level shocks dominating their "
            "returns."
        ),
        "results": [
            ("-0.47 pts", "net shock transmission per one-point rise in a sector's top-three share (t = -3.6), sector and month fixed effects"),
            ("-0.66 pts", "the same effect on uncapped constituent-built returns (t = -4.8)"),
            ("88.9%", "peak total connectedness (16 March 2020); sample low 53.7% (August 2026)"),
            ("0 of 110", "Granger lead-lag links surviving heteroskedasticity-robust tests; classical tests appear to find 90"),
            ("21-31%", "false-rejection rate of the classical Granger test at a nominal 5% under GARCH errors, from a data-calibrated Monte Carlo"),
            ("78", "since-removed firms recovered for the point-in-time constituent panel"),
        ],
        "figures": [
            ("cs-tci", "Total connectedness of S&P 500 sector returns (a) and range volatility (b). The filtered TVP-VAR uses only data available on each date; the 200-day rolling window invents a drop when the April 2025 tariff shock leaves the window."),
            ("cs-concentration-link", "Within-sector concentration and net shock transmission, between sectors (a) and within sectors after two-way fixed effects (b)."),
            ("cs-net-heatmap", "Net directional connectedness by sector, monthly means of daily TVP-VAR estimates. Red sectors transmit shocks; blue sectors receive them."),
        ],
        "methods": [
            "Filtered TVP-VAR connectedness with forgetting factors (Antonakakis, Chatziantoniou and Gabauer 2020), so every date uses only data available on that date",
            "Point-in-time S&P 500 constituent panel: historical membership, split-consistent share counts, the 2023 GICS reclassification, dual-class deduplication",
            "Panel regressions with sector and month fixed effects and Driscoll-Kraay standard errors",
            "Granger tests with heteroskedasticity-robust Wald statistics and Benjamini-Hochberg control, plus a Monte Carlo that measures the classical test's size",
        ],
        "limits": [
            "The concentration effect is a relationship in levels; it does not appear in first differences.",
            "An earlier version of this project, circulated on SSRN, reported Granger results that did not survive robust tests. This manuscript supersedes it, and the repository lists each retracted claim.",
        ],
        "keywords": ["connectedness", "market concentration", "TVP-VAR", "Granger causality", "heteroskedasticity-robust inference", "granularity"],
        "jel": "C12, C23, C32, G12, L11",
        "bibtex": "@unpublished{yadav2026concentrated,\n  title  = {Concentrated Sectors Transmit Less: Within-Sector Concentration and Time-Varying Connectedness in the {S\\&P} 500, 2018 to 2026},\n  author = {Yadav, Tanishk},\n  year   = {2026},\n  note   = {Manuscript submitted to Studies in Nonlinear Dynamics \\& Econometrics}\n}",
    },
    {
        "slug": "ratewalk",
        "title": "RateWalk: Forecasting Fed Rate Decisions with a Shrunk Markov Chain",
        "short": "RateWalk: Forecasting Fed Decisions",
        "chip": "Working paper",
        "chip_kind": "working",
        "status": "Working paper, July 2026. Not peer reviewed.",
        "date": "July 2026",
        "pub_date": "2026/07/04",
        "pdf": "/papers/yadav-2026-ratewalk.pdf",
        "code": "https://github.com/tanishhky/RateWalk",
        "ssrn": None,
        "card_finding": "Naive inflation-regime conditioning overfits; empirical-Bayes shrinkage fixes it in the US, UK and Germany, and a blend with a market proxy reaches log-loss 1.056 and a 72.7% hit rate.",
        "question": "Can a memoryless Markov chain on the Fed's policy moves forecast the next decision out of sample, and does conditioning on the inflation regime help?",
        "abstract": (
            "I ask whether a memoryless Markov chain on the Federal Reserve's policy moves can forecast the next "
            "rate decision out of sample, and whether conditioning the chain on the inflation regime improves it. "
            "Under strict no-look-ahead discipline, with CPI read at its real ALFRED release date so revisions "
            "never leak, the answer is a clean bias-variance story. A first-order chain beats a climatology "
            "baseline. Naive conditioning on the CPI regime overfits and hurts, because it splits sparse transition "
            "data across regimes. Shrinking each regime row toward the pooled chain (an empirical-Bayes Dirichlet "
            "prior) recovers a small but consistent edge that replicates across the United States, the United "
            "Kingdom, and Germany, survives a data-driven shrinkage strength, and sits on a broad parameter plateau "
            "rather than a tuned point. Against the market's own pricing, proxied by a walk-forward-calibrated "
            "Treasury-curve signal, the chain wins overall (log-loss 1.06 vs. 1.20) but the decomposition is "
            "sharper: the market is better on 82% of actual move months, the chain on 85% of holds, and a "
            "no-look-ahead adaptive blend beats both. The edge lives in probabilistic calibration: a duration-timing "
            "strategy built on the signal does not beat a constant-duration benchmark risk-adjusted. I report the "
            "negatives as part of the result."
        ),
        "results": [
            ("3 of 3", "countries where empirical-Bayes shrinkage beats both the unconditional and the naively conditioned chain out of sample (US, UK, Germany, 1990-2026)"),
            ("1.059", "US out-of-sample log-loss of the shrunk chain, vs 1.071 unconditional and 1.136 naively conditioned"),
            ("1.056", "log-loss of the adaptive blend with a Treasury-curve market proxy (proxy alone 1.199) over 319 decisions"),
            ("72.7%", "hit rate of the blend, vs 68.7% for the chain and 54.6% for the market proxy"),
            ("82% / 85%", "share of move months the market proxy wins, and of hold months the chain wins"),
            ("Null", "a duration-timing strategy on the signal does not beat a constant-duration bond risk-adjusted"),
        ],
        "figures": [
            ("rw-replication", "Out-of-sample log-loss by country. Conditioning on the inflation regime raises it; empirical-Bayes shrinkage lowers it, in all three."),
            ("rw-market-decomp", "Against a Treasury-curve proxy for market pricing, the market wins months with a move and the chain wins holds."),
        ],
        "methods": [
            "Markov chains on policy-rate increments and CPI regimes, estimated walk-forward",
            "CPI read at its first ALFRED release, so later revisions never leak into a past forecast",
            "Empirical-Bayes Dirichlet shrinkage toward the pooled chain, with a data-driven strength",
            "A fixed-income Monte Carlo behind the forecaster: yield-curve mapping, 5,000 paths, replayed GFC, Covid and SVB shocks, VaR and CVaR",
        ],
        "limits": [
            "The market benchmark is a Treasury-curve proxy, not fed funds futures.",
            "The value is calibrated probabilities, not a tradeable duration signal.",
        ],
        "keywords": ["Federal Reserve", "Markov chain", "empirical Bayes", "forecast evaluation", "point-in-time data"],
        "jel": None,
        "bibtex": "@techreport{yadav2026ratewalk,\n  title       = {RateWalk: Forecasting Fed Rate Decisions with a Shrunk Markov Chain},\n  author      = {Yadav, Tanishk},\n  year        = {2026},\n  institution = {NYU Tandon School of Engineering},\n  type        = {Working paper}\n}",
    },
    {
        "slug": "volatility-managed-factors",
        "title": "Volatility-Managed Factor Portfolios: A Replication and Extension on the Fama-French Five Factors and Momentum",
        "short": "Volatility-Managed Factor Portfolios",
        "chip": "SSRN preprint",
        "chip_kind": "ssrn",
        "status": "SSRN preprint 7113079, July 2026. Not peer reviewed.",
        "date": "July 2026",
        "pub_date": "2026/07/29",
        "pdf": "/papers/yadav-2026-volatility-managed-factor-portfolios.pdf",
        "code": "https://github.com/tanishhky/Equity-Factor-Volatility-Analysis",
        "ssrn": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7113079",
        "card_finding": "Volatility timing pays only on crash-prone factors: momentum earns 8.9% a year of alpha (t = 5.0) and its Sharpe rises from 0.51 to 0.89; size, value and investment gain nothing.",
        "question": "Moreira and Muir (2017) showed that scaling factor exposure by inverse recent variance raises Sharpe ratios. Does it hold across the Fama-French five factors and momentum, and after costs?",
        "abstract": (
            "We replicate and extend Moreira and Muir (2017) by volatility-managing the Fama-French five factors "
            "plus the momentum factor over 1963 to 2026, using daily data from the Kenneth French Data Library. "
            "Each factor's exposure is scaled by the inverse of its prior-month realized variance, so the leverage "
            "decision uses only past information. Regressing the managed factor on the original (the Moreira-Muir "
            "spanning test, with Newey-West standard errors) gives an honest, factor-dependent answer: volatility "
            "timing earns large and statistically significant alpha on the crash-prone factors, momentum (8.9% per "
            "year, t = 5.0) and profitability (RMW, 2.3% per year, t = 2.9), while it adds nothing for size, value, "
            "or investment, and the market factor's managed alpha is positive but insignificant over the full "
            "sample. Volatility-managed momentum raises the annualized Sharpe ratio from 0.51 to 0.89 (0.81 net of "
            "a 14 basis point per turn transaction cost). The results are consistent with Barroso and Santa-Clara "
            "(2015): the factors that benefit are those whose left-tail crashes cluster in high-volatility states. "
            "We treat the study as performance attribution rather than a live strategy, reporting turnover and "
            "net-of-cost Sharpe throughout."
        ),
        "results": [
            ("8.9% / yr", "managed momentum alpha (t = 5.0)"),
            ("0.51 to 0.89", "momentum Sharpe ratio; 0.81 after 14 bp per-turn costs"),
            ("2.3% / yr", "managed profitability (RMW) alpha (t = 2.9)"),
            ("Nothing", "for size, value, or investment; market alpha positive but insignificant"),
        ],
        "figures": [
            ("vm-sharpe-bars", "Annualized Sharpe ratio of each factor, original vs volatility-managed, 1963 to 2026."),
        ],
        "methods": [
            "Daily Kenneth French data, 1963 to 2026",
            "Exposure scaled by inverse prior-month realized variance, so leverage uses only past data",
            "Moreira-Muir spanning regressions with Newey-West standard errors",
            "Turnover and 14 bp per-turn transaction costs reported throughout",
        ],
        "limits": [
            "This is performance attribution, not a live strategy; as in Moreira and Muir, the scaling constant is set over the full sample.",
        ],
        "keywords": ["volatility-managed portfolios", "factor timing", "momentum", "Fama-French", "Newey-West"],
        "jel": None,
        "bibtex": "@article{yadav2026volmanaged,\n  title   = {Volatility-Managed Factor Portfolios: A Replication and Extension on the {Fama-French} Five Factors and Momentum},\n  author  = {Yadav, Tanishk},\n  year    = {2026},\n  journal = {SSRN Electronic Journal},\n  note    = {Preprint, abstract 7113079}\n}",
    },
    {
        "slug": "voledge",
        "title": "VolEdge: Measuring and Trading the Variance Risk Premium with Model-Free Risk-Neutral Moments",
        "short": "VolEdge: The Variance Risk Premium",
        "chip": "Working paper",
        "chip_kind": "working",
        "status": "Working paper, July 2026. Not peer reviewed.",
        "date": "July 2026",
        "pub_date": "2026/07/07",
        "pdf": "/papers/yadav-2026-voledge.pdf",
        "code": "https://github.com/tanishhky/voledge",
        "ssrn": None,
        "card_finding": "A full-stack platform that extracts risk-neutral moments from live option chains without a pricing model; a GARCH vol-targeted sleeve beat SPY on risk (Sharpe 0.85 vs 0.68) while naive short-variance harvesting lost money.",
        "question": "The gap between what options price and what the underlying realizes is the variance risk premium. Can it be measured model-free, and does it pay to trade?",
        "abstract": (
            "VolEdge is a full-stack research platform built around a single thesis: the gap between what options "
            "price and what the underlying realizes is the risk premium, and that gap can be measured and traded. "
            "The platform extracts the risk-neutral distribution model-free via Bakshi-Kapadia-Madan (BKM) moments "
            "and compares it, horizon-matched, against the physical distribution estimated from realized returns; "
            "the spread Q minus P is surfaced for variance, skew, and kurtosis. A no-look-ahead walk-forward engine "
            "then backtests premium-driven strategies. We report two honest results on free data (2019 to 2024, net "
            "of modeled costs): a GARCH(1,1) volatility-targeted strategy beat SPY buy-and-hold on a risk-adjusted "
            "basis (Sharpe 0.85 vs. 0.68) with 41% lower maximum drawdown, while a naive long-only variance-premium "
            "harvest lost money (Sharpe -0.16), empirically confirming the premium as compensation for crash risk "
            "rather than harvestable alpha. The BKM extractor is validated against Black-Scholes chains of known "
            "volatility, and the backtest engine reproduces buy-and-hold to 0.000 pp at any rebalance frequency."
        ),
        "results": [
            ("0.85 vs 0.68", "Sharpe of the GARCH volatility-targeted SPY/BIL sleeve vs SPY, net of costs (evaluation 2020 to 2024, including Covid)"),
            ("-19.7% vs -33.7%", "maximum drawdown, a 41% reduction"),
            ("-0.16", "Sharpe of naive short-variance harvesting: the premium pays for crash risk, it is not free yield"),
            ("0.000 pp", "difference between the backtest engine and buy-and-hold at any rebalance frequency"),
        ],
        "figures": [
            ("ve-garch-volmanaged", "Growth of $1: the GARCH volatility-targeted sleeve earns less than buy-and-hold but with a far smaller drawdown. Walk-forward, net of costs."),
        ],
        "methods": [
            "Bakshi-Kapadia-Madan model-free risk-neutral variance, skew and kurtosis from live option chains",
            "Implied volatility and Greeks computed locally (Black-Scholes with Brent root-finding); runs on free data with no API key",
            "Walk-forward engine with strict t-1 data boundaries, sandboxed user strategies, and a parameter-sensitivity surface",
            "FastAPI backend and a React front end with 18+ panels, including a 3D implied-volatility surface",
        ],
        "limits": [
            "Free data and a five-year evaluation window; the Sharpe comparison depends on including 2020.",
        ],
        "keywords": ["variance risk premium", "risk-neutral moments", "BKM", "volatility targeting", "walk-forward backtesting"],
        "jel": None,
        "bibtex": "@techreport{yadav2026voledge,\n  title       = {VolEdge: Measuring and Trading the Variance Risk Premium with Model-Free Risk-Neutral Moments},\n  author      = {Yadav, Tanishk},\n  year        = {2026},\n  institution = {NYU Tandon School of Engineering},\n  type        = {Working paper}\n}",
    },
    {
        "slug": "regime-detection",
        "title": "Multi-Scale Regime Detection with Fuzzy Aggregation for Adaptive Sector Portfolio Management",
        "short": "Multi-Scale Regime Detection",
        "chip": "SSRN preprint",
        "chip_kind": "ssrn",
        "status": "SSRN preprint 6484679, July 2026. Not peer reviewed.",
        "date": "July 2026",
        "pub_date": "2026/07/13",
        "pdf": "/papers/yadav-2026-multi-scale-regime-detection.pdf",
        "code": "https://github.com/tanishhky/regime-adaptive-portfolio",
        "ssrn": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6484679",
        "card_finding": "Four independent stress signals that must agree before de-risking: maximum drawdown -6.2% vs -41.7% for SPY, and the same calibration transfers to factor and international portfolios.",
        "question": "Can a crash-avoidance overlay suppress false alarms by requiring independent stress signals to agree, and does one calibration transfer across asset classes?",
        "abstract": (
            "We propose a multi-scale regime detection framework that fuses four orthogonal stress detectors (CUSUM "
            "sequential analysis on z-score returns, rolling cross-sector correlation, market breadth, and rolling "
            "return skewness) into a unified stress probability via sigmoid-membership fuzzy inference. The "
            "aggregator uses a max-of-top-2 rule: it returns the second-largest membership, so at least two "
            "orthogonal detectors must agree before the system acts, structurally suppressing single-detector false "
            "alarms. The composite signal drives an adaptive sector portfolio that classifies eleven S&P 500 sector "
            "ETFs into three baskets by GARCH(1,1)-t conditional-volatility terciles and Ornstein-Uhlenbeck recovery "
            "half-life, with implicit cash allocation as the primary risk-reduction mechanism. In a walk-forward "
            "backtest (2009 to 2025, quarterly recalibration, 10 bps per trade, zero look-ahead), the framework is "
            "best understood as a capital-preservation overlay: it holds maximum drawdown to -6.2% (versus -41.7% "
            "for SPY) at 4.6% annualized volatility, for a Sharpe of 0.97 (versus SPY's 0.58) and Calmar 0.94. "
            "Benchmarked honestly, simple trend rules achieve higher raw Sharpe on the SPY universe; the "
            "architecture's distinctive value is generalization: applied unchanged to factor portfolios and "
            "international equities it scores Sharpe 1.21 and 1.04 against 0.51 and 0.11 for equal-weight."
        ),
        "results": [
            ("-6.2% vs -41.7%", "maximum drawdown vs SPY, walk-forward 2009 to 2025, net of 10 bp per trade"),
            ("0.97 vs 0.58", "Sharpe ratio vs SPY, at 4.6% annualized volatility (Calmar 0.94)"),
            ("1.21 vs 0.51", "Sharpe on factor portfolios with the calibration unchanged, vs equal weight"),
            ("1.04 vs 0.11", "Sharpe on international equities, unchanged, vs equal weight"),
        ],
        "figures": [
            ("svg:regime", "Four orthogonal detectors feed a max-of-top-2 fuzzy consensus: the system de-risks only when at least two agree. Every threshold is estimated walk-forward."),
        ],
        "methods": [
            "Detectors: Page CUSUM on z-scored returns, rolling cross-sector correlation, market breadth, rolling skewness",
            "Sigmoid-membership fuzzy inference with a max-of-top-2 rule",
            "Baskets from GARCH(1,1)-t volatility terciles and Ornstein-Uhlenbeck recovery half-life; implicit cash",
            "Walk-forward: 504-day training window, 63-day out-of-sample steps, quarterly recalibration",
        ],
        "limits": [
            "Simple trend rules post a higher raw Sharpe on the SPY universe; the case for this design is false-alarm suppression and cross-asset transfer.",
            "Annual return is 5.8% vs 11.8% for SPY: a capital-preservation overlay, not a return maximizer.",
        ],
        "keywords": ["regime detection", "fuzzy consensus", "capital preservation", "CUSUM", "walk-forward validation"],
        "jel": None,
        "bibtex": "@article{yadav2026regime,\n  title   = {Multi-Scale Regime Detection with Fuzzy Aggregation for Adaptive Sector Portfolio Management},\n  author  = {Yadav, Tanishk},\n  year    = {2026},\n  journal = {SSRN Electronic Journal},\n  note    = {Preprint, abstract 6484679}\n}",
    },
]

# ---------------------------------------------------------------- thesis (description only)
THESIS = {
    "title": "The U.S. Sovereign Debt Doom Loop: A Point-in-Time Framework for Identification, Market Pricing, and Policy Response",
    "meta": "MS thesis, NYU Tandon School of Engineering. Advisor: Prof. David Shimko. In progress, expected May 2027.",
    "question": "When do US debt dynamics turn self-reinforcing, and what does each way out cost?",
    "framing": (
        "Higher debt can push rates up, and higher rates push debt service and future debt up further. The thesis "
        "does not forecast a crisis. It measures, in real time, when the dynamics become explosive, how markets "
        "price that risk, and what each policy response costs, using only information that was available at each "
        "historical date."
    ),
    "pillars": [
        ("Identification",
         "Tests in real time when debt dynamics turn self-reinforcing. The marketable Treasury debt is rebuilt bond "
         "by bond from 11,000+ auctions since 1979, and 39 macro series are read from their full revision "
         "histories, so no historical judgment sees data that had not yet been released."),
        ("Market pricing",
         "Reads fiscal stress through the rates market: the Treasury volatility risk premium (implied versus "
         "realized) and a regime-switching stress state, each tested as a leading signal of the fiscal gap under "
         "multiple-testing control."),
        ("Policy response",
         "Simulates 30-year debt paths under two independently estimated macro engines, a vector autoregression "
         "and a regime-switching hidden Markov model, on common random numbers, pricing five policy responses "
         "against four shocks, down to sector employment and recovery times."),
    ],
    "rigor": [
        "Every assumption is either tested out of sample and corrected for multiple testing, or stated as a range from the literature.",
        "Design choices are challenged by an LLM agent over a purpose-built 147-paper retrieval corpus (hybrid vector and keyword search with an in-corpus citation graph).",
        "No-lookahead invariance tests guard the data layer; the engine carries 48 passing tests and stamps a configuration hash on every result.",
        "Paths that break hard feasibility are rejected and reported with their reasons, never clipped.",
    ],
    "scale": [
        ("11,000+", "Treasury auctions since 1979, rebuilt bond by bond"),
        ("39", "macro series with full revision histories"),
        ("2", "independently estimated macro engines"),
        ("5 x 4", "policy responses by shocks, on common random numbers"),
    ],
    "results_note": "Results will appear here once they pass the thesis quality gate: every claim is tested, stated conditionally, and reviewed by my advisor before it is published anywhere.",
}

# ---------------------------------------------------------------- systems
SYSTEMS = [
    {
        "name": "ChronoFund",
        "tag": "Point-in-time data engine",
        "text": "SEC EDGAR, XBRL and Bloomberg fundamentals dated to the second the SEC accepted each filing. Four independent layers enforce the cutoff, and any violation fails at parse time rather than months later inside an inflated backtest. Survivorship-free, 65 tests.",
        "link": "https://github.com/tanishhky/chronofund-fundamental-engine",
    },
    {
        "name": "Regime-Aware Factor Strategy",
        "tag": "Fundamental equity backtest",
        "text": "A walk-forward regime-switching fundamental strategy on ChronoFund data, 2008 to 2026, net of 2/15 fees. Fama-French five-factor attribution reports alpha decay rather than hiding it: 8.37% (t = 2.73) in 2008 to 2017, fading to an insignificant 2.42% over the full period.",
        "link": "https://github.com/tanishhky/Regime-Aware-Factor-Backtest",
    },
    {
        "name": "PinSight",
        "tag": "0DTE options engine",
        "text": "Infers the risk-neutral density of SPY same-day options and runs a scheduled live paper-trading loop. Every decision is a pure function of an as-of timestamp, and a test proves past decisions cannot change when future data is appended.",
        "link": "https://github.com/tanishhky/PinSight",
    },
    {
        "name": "DriftEdge",
        "tag": "Prediction-market engine",
        "text": "Sizes Polymarket and Kalshi binary contracts with Kelly on an empirical-Bayes win probability whose prior is a zero-edge bet, so no evidence means no position. Deterministic replay audits every strategy change; 64 tests with CI.",
        "link": "https://github.com/tanishhky/DriftEdge",
    },
]

# ---------------------------------------------------------------- experience and education
EXPERIENCE = [
    {
        "org": "New York University, Tandon School of Engineering",
        "place": "New York, NY",
        "span": "Jun 2026 to present",
        "roles": [
            ("Course Assistant, FRE-GY 6103 Valuation for Financial Engineering (Prof. David Shimko)", "Sep 2026 to present"),
            ("Contributor, Valuation Principles, Prof. Shimko's graduate valuation textbook (Wiley, in preparation)", "Jun 2026 to present"),
        ],
        "points": [
            "Designated lead of the course's four assistants across two sections; resolve modeling questions on mortgage-pool prepayment and default, level-payment amortization, and Treasury curve bootstrapping, and fix ambiguous project specifications.",
            "Restructured the textbook's Monte Carlo and variance-reduction material and built its figures, companion Python notebooks, Excel models, and a 164-page solutions manual; the chapters serve as the course text.",
        ],
    },
    {
        "org": "IUDX (India Urban Data Exchange)",
        "place": "Bengaluru, India",
        "span": "Jun 2023 to Aug 2023",
        "roles": [("Summer Intern, Framework Development", "Jun 2023 to Aug 2023")],
        "points": [
            "Built a consent-capture tool for the Agricultural Data Exchange (ADeX) in a four-person team, used to build 38 government datasets: purpose-coded, expiring consent records with RSA/SHA-256 digital-signature support for regulated data sharing.",
        ],
    },
    {
        "org": "SRM University-AP",
        "place": "Amaravati, India",
        "span": "2022 to 2023",
        "roles": [("Student Council, PR Convener", "2022 to 2023")],
        "points": [
            "Primary student liaison to the administration; directed cross-functional teams running the university's cultural festivals.",
        ],
    },
]

EDUCATION = [
    {
        "school": "New York University, Tandon School of Engineering",
        "place": "Brooklyn, NY",
        "degree": "Master of Science in Financial Engineering",
        "dates": "Sep 2025 to May 2027",
        "notes": ["MS thesis in progress (see Thesis), advised by Prof. David Shimko"],
        "coursework": [
            "Econometrics and Time Series Analysis", "Derivative Securities", "Algorithmic Trading and High-Frequency Finance",
            "Credit Risk and Financial Risk Management", "Model Risk Management", "Valuation for Financial Engineering",
            "Corporate Valuation", "Quantitative Methods in Finance",
        ],
        "in_progress": [
            "Volatility Models", "Fixed Income Quantitative Trading", "Financial Risk Management",
            "Real-Time Risk Management", "Financial Economics", "Advanced Topics in Financial Technology",
        ],
    },
    {
        "school": "SRM University-AP",
        "place": "Amaravati, India",
        "degree": "Bachelor of Technology, Computer Science and Engineering (Artificial Intelligence and Machine Learning)",
        "dates": "2021 to 2025",
        "notes": ["100% merit scholarship"],
        "coursework": [
            "Linear Algebra", "Multivariable Calculus", "Differential Equations", "Probability and Statistics",
            "Design and Analysis of Algorithms", "Machine Learning", "Operating Systems", "Compiler Design",
        ],
        "in_progress": [],
    },
]

SKILLS = [
    ("Programming", "Python (pandas, NumPy, SciPy, statsmodels, scikit-learn, arch, hmmlearn), SQL, R, C++ (coursework); FastAPI, React, pytest, Git, LaTeX"),
    ("Econometrics", "VAR and TVP-VAR, Diebold-Yilmaz connectedness, Granger causality with FDR control, robust inference, panel fixed effects, Newey-West and Driscoll-Kraay errors, GARCH"),
    ("Probability and ML", "Markov chains, hidden Markov models, empirical Bayes and Dirichlet shrinkage, Kalman filtering, Monte Carlo and variance reduction, Gaussian mixtures"),
    ("Derivatives and risk", "Black-Scholes and Greeks, model-free risk-neutral moments, risk-neutral densities, variance risk premium, factor models, VaR and CVaR, stress testing"),
    ("Data", "SEC EDGAR and XBRL, FRED and ALFRED vintages, Treasury Fiscal Data, Kenneth French library, Bloomberg Terminal, WRDS"),
]

CERTS = [
    ("ARPM Quant Bootcamp (Advanced Risk and Portfolio Management)", "2026", "assets/certs/arpm-quant-bootcamp.png"),
    ("Akuna Capital Options 101", "2026", "assets/certs/akuna-options-101.png"),
    ("AI for Investments, NPTEL online certification", "Credited toward the B.Tech", "assets/certs/iit-ai-for-investments.png"),
    ("Bloomberg Market Concepts", "", "assets/certs/bloomberg-market-concepts.png"),
    ("Bloomberg Finance Fundamentals", "", "assets/certs/bloomberg-finance-fundamentals.png"),
    ("Financial Markets, Yale University (with honors)", "", "assets/certs/yale-financial-markets.png"),
    ("IBM Machine Learning Professional Certificate", "", "assets/certs/ibm-machine-learning-professional.png"),
]

# ---------------------------------------------------------------- writing
POSTS = [
    {
        "title": "RateWalk: Does a Fed-Rate Forecaster Actually Beat the Market?",
        "date": "July 2026", "venue": "LinkedIn", "minutes": 5,
        "url": "https://www.linkedin.com/feed/update/urn:li:activity:7481746164057464832/",
        "image": "assets/img/writing/ratewalk-post.png",
        "summary": "A Markov chain over Fed policy moves and CPI regimes, walk-forward validated on first-release inflation data. Naive regime conditioning overfits; shrinkage recovers a small edge that replicates across the US, UK and Germany.",
        "note": None,
    },
    {
        "title": "The Big Short didn't really explain derivatives. Let me try.",
        "date": "May 2026", "venue": "Medium", "minutes": 8,
        "url": "https://medium.com/@tanishhky/what-actually-are-financial-derivatives-f486fa3c8971",
        "image": "assets/img/writing/big-short-cover.png",
        "summary": "A plain-English primer on forwards, futures, options and swaps, with the everyday deals they come from.",
        "note": None,
    },
    {
        "title": "What Actually Drives Sector Returns? A Factor-Model Teardown",
        "date": "April 2026", "venue": "LinkedIn", "minutes": 6,
        "url": "https://www.linkedin.com/feed/update/urn:li:activity:7451289420227477504/",
        "image": "assets/img/writing/factor-teardown-post.png",
        "summary": "The 11 sector ETFs run through Fama-French three-factor, Carhart and five-factor models: technology's returns are 92-93% explained by factors, and a simple sector-momentum rule does not beat SPY risk-adjusted.",
        "note": None,
    },
    {
        "title": "Sector-Level Analysis and Clustering of S&P 500 Companies",
        "date": "April 2026", "venue": "LinkedIn", "minutes": 8,
        "url": "https://www.linkedin.com/posts/tanishkyadav_sector-level-analysis-and-clustering-of-s-ugcPost-7447846466427162624-z4sa",
        "image": "assets/img/writing/sp500-clustering-post.png",
        "summary": "The first version of the S&P 500 sector project: concentration measures, clustering, and lead-lag tests across 68 sub-sectors.",
        "note": "Correction: this post's Granger and clustering results did not survive later testing. The project was rebuilt as Concentrated Sectors Transmit Less, which lists every retracted claim.",
    },
]

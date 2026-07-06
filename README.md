# German Auto Industry Analysis
**Python-based equity research toolkit for the German automotive sector**

`BMW.DE` · `MBG.DE` · `VOW3.DE` · `P911.DE` · benchmarked vs `TSLA`

---

## What This Is

A four-module Python project that analyses the German automotive sector through the lens of a buy-side equity analyst. The core thesis: **German OEMs are being squeezed from two sides — EV transition costs compressing margins, and China market share eroding permanently.** The project quantifies both pressures and identifies which OEM is best positioned.

---

## Four Charts, Four Lenses

| Chart | File | What It Shows |
|---|---|---|
| Valuation Comps | `01_valuation_comps.html` | EV/EBITDA vs P/E — who's cheap, who's expensive |
| Margin Trends | `02_margin_trends.html` | EBIT margin 2021–2024 — VW collapse vs BMW stability |
| EV Transition | `03_ev_transition.html` | BEV mix % per OEM vs EU 2035 mandate trajectory |
| China Exposure | `04_china_exposure.html` | China revenue % and units sold — the liability story |

All charts are interactive (Plotly HTML) — hover for data, click legend to toggle series.

---

## Key Findings (last refreshed 06 July 2026 — updates automatically, see below)

**Valuation:** BMW is the cheapest OEM on both EV/EBITDA and P/E among the German cluster as of the latest refresh. These multiples are TTM as of the refresh date (not FY2025A) since they move with the live share price — check `charts/01_valuation_comps.html` for the current snapshot rather than quoting a fixed number.

**Margins:** Porsche remains the highest-margin German OEM in the latest run, though well off its earlier peak — see `charts/02_margin_trends.html` for the current cross-OEM comparison.

**EV Transition:** BMW leads the German OEM cluster on BEV mix of 2025 deliveries (using annual-report-sourced figures, not an unlabeled estimate). VW lags despite being an early mover.

**China:** VW carries the highest China revenue exposure (24.2%) of the four OEMs tracked, followed by Porsche and Mercedes; BMW has the lowest at 18.6%.

**Bottom line:** BMW is the highest-quality way to express a German auto recovery within this OEM cluster — cheapest multiples, strongest EV progress, and the lowest China concentration of the four.

---

## Project Structure

```
german-auto-analysis/
├── analysis.py        # Main runner — executes all modules
├── auto_data.py       # Data layer — yfinance live data + static CSV loaders
├── charts.py          # Four Plotly visualisations
├── requirements.txt
├── data/
│   ├── ev_mix.csv         # BEV delivery mix 2020–2025 per OEM
│   └── china_exposure.csv # China revenue and units 2020–2025 per OEM
└── charts/            # Output folder — HTML + PNG charts
```

---

## Setup & Run

```bash
git clone https://github.com/SharDXL/german-auto-analysis
cd german-auto-analysis
pip install -r requirements.txt
python analysis.py
```

Opens interactive HTML charts in `/charts/`. Live data pulled from Yahoo Finance on each run.

**Dependencies:** `yfinance`, `pandas`, `plotly`, `kaleido==0.2.1`

---

## Key Concepts

**EV/EBITDA** — Enterprise value divided by EBITDA. The primary valuation multiple for capital-intensive businesses like autos. Lower = cheaper. German OEMs cluster at 9–12x vs Tesla's 134x.

**EBIT Margin** — Earnings before interest and tax as % of revenue. The core profitability metric for the automotive segment (excludes financial services). VW at ~3% vs BMW at ~6.6% is the clearest signal of which OEM has the structural problem.

**BEV Mix** — Battery electric vehicles as % of total deliveries. The EU 2035 mandate requires 100% ZEV sales. Any OEM below the trajectory line is at regulatory fine risk.

**China Revenue %** — China's share of group revenue. Was the sector's primary growth and margin engine 2015–2022. Now the primary risk. VW's 24% exposure is the highest; all four OEMs have been declining since 2022.

---

*Data sources: Yahoo Finance (live), company annual reports (static datasets). For educational purposes.*

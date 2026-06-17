# German Auto Industry Analysis
**Python-based equity research toolkit for the German automotive sector**

`BMW.DE` · `MBG.DE` · `VOW3.DE` · `P911.DE` · benchmarked vs `TSLA`

---

## What This Is

A four-module Python project that analyses the German automotive sector through the lens of a buy-side equity analyst. The core thesis: **German OEMs are being squeezed from two sides — EV transition costs compressing margins, and China market share eroding permanently.** The project quantifies both pressures and identifies which OEM is best positioned.

Built as part of a structured project roadmap: DAX40 Trading Comps → Mittelstand M&A → ECB Fixed Income → **German Auto Deep-Dive (this)** → BMW Business Analysis → BMW DCF → Full Equity Research Report.

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

## Key Findings (June 2026)

**Valuation:** BMW is the cheapest on both EV/EBITDA (9.5x) and P/E (6.1x) among German OEMs. Porsche trades at a significant premium (EV/EBITDA 20x) despite margin compression. Tesla's multiples (EV/EBITDA 134x, P/E 371x) reflect pure growth pricing vs. the German value cluster.

**Margins:** VW's operating margin has compressed to ~3%, reflecting restructuring costs and China headwinds. BMW and Mercedes have held 6%+ despite headwinds. Porsche remains the highest-margin OEM but dropped sharply from its 20%+ peak.

**EV Transition:** BMW leads German OEMs at 20.6% BEV mix (2025), ahead of the EU mandate trajectory. VW lags at 10.1% despite being the earliest mover, reflecting consumer adoption headwinds post-subsidy removal.

**China:** VW has the highest China dependency (24.2% of revenue) and the most acute exposure. All four OEMs have seen China % decline since 2022 peak. What was once Germany's most profitable export market is now the sector's primary risk.

**Bottom line:** BMW is the highest-quality way to express a German auto recovery — cheapest multiples, best EV progress among German OEMs, strong net cash position, and the Neue Klasse platform as a credible 2026-2027 catalyst.

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

## Context & Next Steps

This project is the industry layer of a full equity research workflow:
- **P4 (next):** BMW business analysis — revenue model, competitive moat, segment breakdown
- **P5:** BMW 3-statement financial model
- **P7:** BMW DCF valuation
- **P9:** Full equity research report with price target

---

*Data sources: Yahoo Finance (live), company annual reports (static datasets). For educational purposes.*

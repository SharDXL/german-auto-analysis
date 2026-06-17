# German Auto Industry Analysis — Explained in Plain English

This document is for me (Shardul). It covers what this project actually does, why I built it, the real-world situation it's analysing, the key concepts behind each part, how every piece of Python code works, and what to say when someone asks about it. Written to be studied, not skimmed.

---

## Part 1: What Is Actually Happening in the German Auto Industry?

Before anything else, understand the situation this project is analysing. This is not abstract — it's one of the most consequential industrial stories in Europe right now.

### Germany's car industry is its economy

Germany's automotive sector generates about €243 billion in annual revenue, accounts for over 5% of GDP, and employs roughly 800,000 people directly. Indirectly (through the supplier base, dealerships, logistics), the number is several million. The "Big Three" — BMW, Mercedes-Benz, and Volkswagen Group — are among the most recognised brands in the world. Porsche AG (majority owned by VW Group, separately listed) sits at the ultra-premium end.

For decades, the formula was simple: German engineering quality commanded price premiums globally, with China as the single biggest profit engine. In 2022, German OEMs collectively earned roughly 35% of their global profits from China. That's an extraordinary concentration.

### The two-sided squeeze — what this project quantifies

**Squeeze 1: The EV transition is expensive**

The world is moving from internal combustion engines (ICE) to battery electric vehicles (BEV). The EU has mandated 100% zero-emission vehicle sales by 2035 — meaning from 2035, you cannot sell a new petrol or diesel car in the EU. German OEMs must completely retool their manufacturing lines, retrain their workforce, develop battery technology, build software capability, and launch competitive EV products — all simultaneously.

This costs tens of billions of euros upfront, before you've sold a single electric car. In the meantime, you're still selling ICE cars (which are profitable) to fund the transition. This is why you see margin compression across the sector — BMW, Mercedes, and especially VW are in the expensive middle phase where investment is high but EV revenue hasn't scaled to compensate.

**Squeeze 2: China is no longer a profit engine — it's a threat**

Chinese EV manufacturers — principally BYD, but also NIO, Li Auto, Xpeng, and others backed by the Chinese government — have become genuinely world-class in a very short time. In China, which is the world's largest car market, they have displaced German OEMs in large portions of the market. VW was overtaken by BYD in 2024 and by Geely in 2025. German auto exports to China fell 33% in 2025 alone.

Worse: Chinese OEMs are now entering Europe. BYD outsold Tesla in Germany in 2025. They're selling at €32,000 on average — far cheaper than German equivalents. The EU has imposed tariffs (BYD faces 27% total duties), but analysts say 40-50% would be needed to make Europe unattractive for Chinese exporters.

So simultaneously: German OEMs are losing China (where they made their profits) AND facing Chinese competition at home (where they need to rebuild margins).

### What this project tries to answer

Three questions:
1. **Who is cheapest right now?** — Valuation comps chart. Are German OEM stocks cheap because the market is pricing in too much pain? Or are they fairly valued for the headwinds?
2. **Who has held their profitability?** — Margin trends chart. Which OEM has executed better through the transition?
3. **Who is most at risk?** — EV transition and China exposure charts. Who is behind on EVs? Who is most China-dependent?

The ultimate answer this project builds toward (in P9, the full equity research report): **Should you buy BMW, Mercedes, VW, or Porsche stock today — and at what price?**

---

## Part 2: The File Structure — What Each File Does

### `auto_data.py` — The Data Layer

This file is responsible for one thing only: **getting data**. It doesn't analyse, it doesn't chart. It just fetches and returns clean data for everything else to use.

Think of it like the research department at a bank — their job is to find the numbers. Other teams (strategy, trading) then use those numbers.

#### `fetch_oem_info()` — The Snapshot Function

```python
def fetch_oem_info() -> pd.DataFrame:
```

This pulls a "snapshot" of where each OEM stands right now — market cap, revenue, EBITDA, margins, valuation multiples. Every metric is pulled from Yahoo Finance's database.

**What `yf.Ticker(ticker)` does:** Creates a connection to a specific stock. `yf.Ticker("BMW.DE")` connects to BMW's Frankfurt listing (`.DE` suffix = Deutsche Boerse). Then `.info` fetches a dictionary of ~100 data points about that stock — everything from the CEO's name to yesterday's closing price to trailing EBITDA.

**The metrics being pulled and why:**

`marketCap` — The total market value of all shares outstanding. BMW at €41bn means the stock market thinks the entire BMW company is worth €41 billion right now.

`totalRevenue` — Annual sales (not profit). BMW's is ~€138bn. Revenue tells you the scale of the business.

`ebitda` — Earnings Before Interest, Tax, Depreciation, and Amortisation. This is the closest thing to "how much cash does the business actually generate from operations?" It strips out financing costs (interest), tax (varies by country), and non-cash charges (depreciation, amortisation). For comparing companies across countries with different tax regimes, EBITDA is cleaner than net income.

`totalDebt` and `totalCash` — Together these tell you the net debt position. If you have €10bn debt and €8bn cash, your net debt is €2bn — and you're vulnerable if cash flows drop. If you have more cash than debt (net cash position), you have financial flexibility to invest through a downturn. BMW and Mercedes have strong net cash; VW is under pressure.

`enterpriseToEbitda` — This is the EV/EBITDA multiple. Enterprise Value (EV) = Market Cap + Net Debt. EV/EBITDA = EV divided by EBITDA. At 9.5x, BMW means: investors are paying 9.5 years' worth of EBITDA for the whole business. Lower = cheaper. This is the most important valuation multiple for capital-intensive businesses like autos.

`trailingPE` — Price divided by earnings per share (last 12 months). Simpler and more widely known than EV/EBITDA, but less reliable for comparing companies with different debt levels. BMW at 6.1x P/E is historically very cheap — the average S&P 500 P/E is ~22x.

`operatingMargins` — Operating profit as % of revenue. This is the EBIT margin (essentially). BMW at 6.6% vs VW at 4.4% shows who has managed costs better through the transition.

`returnOnEquity` — Net income divided by shareholders' equity. How efficiently is the company generating profit from what shareholders have invested? Low RoE (BMW 7.1%, Porsche 0.8%) reflects the current investment phase — profits are being reinvested into EV capex rather than returned to shareholders.

**Why divide by 1e9?**
Yahoo Finance returns numbers in absolute terms (e.g., 138,000,000,000 for BMW revenue). Dividing by 1e9 (one billion) gives you €138bn — the format analysts actually use. Otherwise you're reading 12-digit numbers.

**Why `round(...)`?**
Precision theatre. Saying BMW's market cap is "€41,234,567,890" is false precision — the number changes every second as stock price moves. Rounding to 1 decimal place (€41.2bn) is the convention in finance.

---

#### `fetch_price_history()` — The Price Tracker

```python
def fetch_price_history(period: str = "5y") -> pd.DataFrame:
```

This pulls 5 years of daily adjusted closing prices for all five OEMs, then normalises them to 100 at the start date.

**Why adjusted close (auto_adjust=True)?** Stock prices are adjusted for dividends and stock splits. If BMW pays a €3 dividend, the raw share price drops by roughly €3 on the ex-dividend date. This looks like a loss but it wasn't — the shareholder received the €3 in cash. Adjusted prices remove these mechanical adjustments so you're seeing true economic return.

**Why normalise to 100?** BMW trades in euros, Tesla in dollars. If BMW is at €75 and Tesla is at $245, you can't just compare — you don't know which has performed better. Normalising both to 100 at the same start date lets you compare percentage performance: if BMW is at 95 and Tesla is at 130, Tesla is up 30% and BMW is down 5%, regardless of currency or absolute price.

---

#### `fetch_annual_financials()` — The Trend Data

```python
def fetch_annual_financials() -> dict:
```

This pulls the last 4 years of annual income statements for each OEM and computes EBIT margin for each year.

**Why `t.financials`?** yfinance's `.financials` attribute returns a full income statement as a pandas DataFrame — rows are line items (Revenue, EBIT, Tax, etc.), columns are fiscal year end dates. It's the same data you'd find in the company's annual report, pulled automatically.

**Why compute EBIT margin from the raw numbers?**
EBIT margin = EBIT / Revenue × 100. This tells you what percentage of every euro of revenue becomes operating profit. The trend matters more than the absolute number — a margin declining from 8% to 4% over three years is a warning signal; a margin recovering from 4% to 7% is a bullish signal. Chart 2 visualises this trend for all four OEMs.

---

#### `load_ev_data()` and `load_china_data()` — Static CSV Loaders

```python
def load_ev_data() -> pd.DataFrame:
def load_china_data() -> pd.DataFrame:
```

These are simple — just `pd.read_csv()` on two files in `/data/`. The reason these are static CSVs rather than live API calls: Yahoo Finance doesn't have per-OEM BEV delivery mix data or China revenue breakdowns. That data lives in company press releases, annual reports, and industry databases. I compiled it manually from primary sources (BMW Group Annual Reports 2020–2025, VW Group Annual Reports, China Passenger Car Association data).

This is actually how real analysts work — some data is pulled programmatically (prices, financial statements), some is manually researched and stored in a model.

---

### `charts.py` — The Visualisation Layer

Four functions, one chart each. Each chart tells one part of the story.

---

#### Chart 1: `plot_valuation_comps()` — Who Is Cheap?

**The question it answers:** Relative to each other, which German OEM is the most attractively valued right now?

**The chart:** A scatter plot. X-axis = P/E ratio. Y-axis = EV/EBITDA. Each OEM is a bubble, sized by market cap. Tesla is included as a benchmark.

**How to read it:**
- **Bottom-left** = cheap on both multiples = best value
- **Top-right** = expensive on both = growth/quality premium
- **Bottom-right** = cheap EV/EBITDA but expensive P/E = unusual (suggests EBITDA is depressed relative to earnings — e.g. high D&A)
- **Top-left** = expensive EV/EBITDA but cheap P/E = also unusual (suggests high D&A making earnings look cheap)

The German OEMs all cluster in the bottom-left relative to Tesla — structurally cheaper by every metric. Within the German cluster, BMW is cheapest. Tesla is off in the top-right at 371x P/E and 134x EV/EBITDA — investors are paying a massive premium for Tesla's growth story and software narrative.

**Key Plotly concepts used:**

`go.Scatter` with `mode="markers+text"` — Creates a scatter plot where each point also shows a text label (the OEM name). The `marker` dict controls size, colour, and border. Bubble size is set to `Market_Cap_Bn ** 0.45` — this maps market cap to bubble area in a visually proportional way (without square root, large numbers would dominate too much).

`hovertemplate` — Controls what you see when you hover over a bubble. The `<b>` tags make text bold. `<extra></extra>` removes the default trace name that Plotly appends. This makes the tooltip clean and informative.

`fig.add_annotation` — Adds text labels directly onto the chart at specific positions. Used here to label the quadrants ("Best value zone", "Cheap on earnings").

`xref="paper", yref="paper"` — Positions annotations as fractions of the chart area (0–1) rather than in data coordinates. So `x=0.02, y=0.02` means bottom-left corner of the chart regardless of what values are on the axes.

---

#### Chart 2: `plot_margin_trends()` — Who Has Held Profitability?

**The question it answers:** Over the last 4 fiscal years, which OEM has best protected its margins through the EV transition?

**The chart:** Line chart. X-axis = fiscal year. Y-axis = EBIT margin %. One line per OEM.

**What you should see:** VW's line declining sharply toward 3%. BMW and Mercedes holding relatively flat at 6%+. Porsche dropping from its 20%+ peak but remaining the highest-margin OEM. This tells the story visually: VW has a structural problem; BMW has managed the transition better.

**Why EBIT margin and not net margin?**
Net margin (profit after tax and interest) is affected by how much debt a company has and the local tax rate. BMW and Mercedes both have large financial services divisions (they lend money to car buyers) which distort net income. EBIT margin isolates the performance of the core car business.

**Key Plotly concepts used:**

`go.Scatter` with `mode="lines+markers"` — A line chart where each data point also shows a dot. The dot makes it easy to see exactly where each year's data point is on the line.

`fig.add_hline(y=5)` — Adds a horizontal reference line across the entire chart at y=5%. This represents a rough industry floor — going below 5% consistently signals serious operational problems. It gives context to each OEM's actual margin position.

`line_dash="dot"` — Makes the reference line dotted so it's visually distinct from the OEM lines.

---

#### Chart 3: `plot_ev_transition()` — Who Is Ready for 2035?

**The question it answers:** How fast is each OEM converting its sales to battery electric? Are they on track for the EU mandate, or at risk of regulatory fines?

**The chart:** Line chart. X-axis = year (2020–2025). Y-axis = BEV as % of total deliveries. One line per OEM, plus a dashed grey "EU mandate trajectory" line.

**Why the mandate trajectory matters:** The EU's 2035 100% ZEV mandate means OEMs need to be selling a rapidly growing share of EVs now to build production capacity, consumer adoption, and charging infrastructure. If an OEM is consistently below the trajectory line, they face: (a) EU CO₂ fines per vehicle sold (these can be enormous), and (b) a structural catch-up problem when 2035 approaches.

**What you should see:** Tesla at 100% (naturally, they only make EVs). BMW the strongest German OEM at 20.6%. VW at just 10.1% despite being the earliest German EV mover — reflecting how difficult consumer adoption has been after Germany ended EV subsidies in December 2023 (this caused a 30%+ drop in EV demand overnight).

**Key Plotly concepts used:**

`line=dict(dash="dot" if oem == "Tesla" else "solid")` — Conditional styling. Tesla's line is dotted because it's a benchmark, not a comparable — it makes sense for them to be at 100%, so you don't want it visually competing with the German OEM lines.

`range=[0, 105]` on the y-axis — Forces the axis to show 0–105% even if no data point is at 0 or 100. Without this, Plotly auto-scales and the chart looks cluttered at the extremes.

The EU mandate trajectory points are hardcoded (I estimated an indicative ramp — 2.5% in 2020 to 17% in 2025 heading toward 100% by 2035). This is a judgment call, not an official EU number — the mandate specifies 2035, not the ramp. In a real analyst presentation you'd use industry consultants' (like BNEF or Wood Mackenzie) EV adoption forecasts as the trajectory.

---

#### Chart 4: `plot_china_exposure()` — The Liability Story

**The question it answers:** How dependent is each OEM on China, and how fast is that dependency growing or shrinking?

**The chart:** Two-panel chart. Top panel = China revenue as % of group. Bottom panel = China units sold (thousands). Shared X-axis (year).

**Why two panels?** Revenue % tells you the relative importance of China. Units sold tells you the absolute volume. You need both: an OEM might maintain China revenue % by raising prices even as volume falls — the unit data exposes that. Together they tell you whether China is a growing or shrinking priority.

**What you should see in both panels:** A peak around 2022–2023, then declining sharply through 2025 for all four OEMs. VW has the highest China dependency at 24.2% — the most exposed to continued market share erosion. This chart is essentially a risk heatmap: the higher the China %, the bigger the problem if Chinese OEMs keep displacing German brands.

**Key Plotly concept — `make_subplots`:**

```python
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
```

This creates a figure with two separate chart panels stacked vertically. `rows=2, cols=1` means 2 rows and 1 column of panels. `shared_xaxes=True` means both panels share the same X-axis — so when you zoom in on one, the other zooms with it.

`fig.add_trace(..., row=1, col=1)` and `fig.add_trace(..., row=2, col=1)` — Adds traces to specific panels. Every trace needs to know which panel it belongs to.

`legendgroup=display` — Groups the legend entries for each OEM together. Without this, you'd have 8 legend entries (4 OEMs × 2 panels). With `legendgroup`, clicking "BMW" in the legend shows/hides BMW's lines in both panels simultaneously.

---

### `analysis.py` — The Main Runner

This file ties everything together. When you run `python analysis.py`, it:

1. Calls `auto_data.fetch_oem_info()` → gets the live snapshot
2. Calls `auto_data.fetch_annual_financials()` → gets the margin trend data
3. Calls `auto_data.load_ev_data()` and `load_china_data()` → loads the CSVs
4. Calls all four chart functions → generates and saves the HTML files
5. Prints an "Investment Snapshot" to the terminal — a text summary of key findings

**The Investment Snapshot in the terminal:**

```
Cheapest on EV/EBITDA : BMW
Cheapest on P/E        : BMW
Highest op. margin     : Porsche

China Revenue Exposure (2025):
  VW_Group      24.2%  ████████████
  BMW           19.2%  █████████
```

This bar chart in text form (using the `█` character) is a quick visual in a terminal that has no graphics. It's a common pattern in Python CLI tools — it lets you see relative magnitudes at a glance without opening a browser.

**How the cheapest OEM is computed:**

```python
valid = oem_df[oem_df["EV_EBITDA"] > 0]
cheapest_ev_ebitda = valid.loc[valid["EV_EBITDA"].idxmin(), "OEM"]
```

`oem_df["EV_EBITDA"] > 0` filters to rows where EV/EBITDA is positive (yfinance sometimes returns 0 or negative for loss-making companies where the metric isn't meaningful). `.idxmin()` finds the index of the minimum value. `.loc[..., "OEM"]` retrieves the OEM name at that index.

---

### `data/ev_mix.csv` and `data/china_exposure.csv`

These are static datasets compiled from primary sources:
- BMW Group Annual Reports 2020–2025 (investor.bmwgroup.com)
- Mercedes-Benz Annual Reports
- Volkswagen Group Annual Reports
- China Passenger Car Association (CPCA) monthly data
- Porsche AG Annual Reports

Each row is one OEM-year combination. This is called a "long format" DataFrame — each observation is one row. The alternative is "wide format" where each year is a column. Long format is better for Plotly because you can group by OEM and filter by year easily.

---

## Part 3: The Concepts You Need to Own

### Enterprise Value (EV) — The Real Price Tag

Market cap is what equity investors have paid for the shares. But if you're buying the whole company, you'd also inherit its debt — and you'd get its cash. Enterprise Value accounts for this:

**EV = Market Cap + Total Debt − Cash**

If BMW has a market cap of €41bn, net debt of €5bn, then EV = €46bn. That's the actual price you'd pay to buy the whole business. EV is almost always used in the denominator of valuation multiples (EV/EBITDA, EV/Revenue) for this reason — it's a more complete measure of what you're paying.

### Valuation Multiples — What Are You Paying Per Unit of Something?

A multiple answers: "For every €1 of [metric], how much am I paying?" Lower = cheaper.

**EV/EBITDA:** For every €1 of EBITDA, you're paying EV/EBITDA euros. BMW at 9.5x means you pay €9.50 for each €1 of EBITDA. This is the primary multiple in auto analysis because it eliminates distortions from debt, tax, and non-cash charges.

**P/E:** For every €1 of earnings per share, you're paying the share price. BMW at 6.1x P/E means the stock costs 6.1× annual earnings. Historically cheap. The average for European equities is ~15x; the S&P 500 is ~22x. BMW at 6.1x reflects the market pricing in significant downside risk — is that too pessimistic? That's the investment question.

**EV/Revenue:** For every €1 of revenue, how much EV are you paying? Useful for companies that aren't yet profitable (no EBITDA or earnings to use). Less relevant for German OEMs which are profitable, but useful for comparing to Tesla.

### Why BMW Looks Cheap — The Value Trap Risk

BMW trades at 6.1x P/E. The average company trades at 15-22x. So BMW is 60-70% cheaper than the market average on earnings. This sounds like an obvious buy — but this is where value investing gets hard.

A stock is "cheap" for a reason. The market is pricing in: continued China headwinds, EV transition costs, potential US tariff escalation, and software capability risk. The question is whether the market is over-discounting these risks. If BMW's earnings normalise to €6-7bn (from current depressed levels) and the stock still trades at €55-60, then at a "normal" 12x P/E it should be worth €72-84 — significant upside. But if China keeps deteriorating and margins don't recover, current earnings are the new normal and the stock is fairly priced.

This is the exact analysis you'll do in P7 (the DCF) — where you build explicit scenarios and put a price target on it.

### EBIT vs EBITDA vs Net Income — Which One to Use?

All three measure profit, but strip out different things:

**Net Income** — The bottom line after everything: revenue minus costs minus interest minus tax. Affected by how much debt the company has (interest) and the country's tax rate. Hard to compare across companies.

**EBIT** (Earnings Before Interest and Tax) — Strips out financing decisions (debt) and tax. The best measure of operating performance of the business itself. Used as "operating profit."

**EBITDA** — Strips out depreciation and amortisation (D&A) on top of EBIT. D&A is a non-cash charge — it's the accounting write-down of assets over time (a car factory depreciates over 20 years). Adding it back gives you a cleaner picture of cash generation. The issue: some businesses genuinely consume a lot of capex (they need to constantly replace machinery). EBITDA ignores this. For autos, which are capex-heavy, EBIT is actually more honest — but EV/EBITDA is the market convention.

---

## Part 4: Reading Resources — Go Deeper

### On Valuation (Essential)
- **Damodaran's free NYU Valuation course** — youtube.com/c/AswathDamodaran — Lecture 1-4 cover everything on multiples. Damodaran literally invented the modern approach to EV/EBITDA sector analysis. Free, best in the world.
- **Damodaran's auto industry data page** — pages.stern.nyu.edu/~adamodar — He publishes sector-level EV/EBITDA and margin data for every industry annually. Go to "Data" → "Valuation Multiples by Sector." Compare our live BMW numbers to the sector average.

### On the German Auto Industry (Directly Relevant)
- **Rhodium Group — "Germany's China Shock Revisited"** (2025) — rhg.com — The single best analysis of how Germany's auto sector lost China. Read the executive summary at minimum.
- **Clean Energy Wire — German auto supplier technology gap** — cleanenergywire.org — On the 35% cost disadvantage vs Chinese competitors. Sobering read.
- **IAA Mobility 2025 coverage** — electrive.com — IAA is the global auto show in Munich. The 2025 edition reporting shows exactly where each OEM stands on their EV lineup.
- **BMW Group Annual Report 2025** — bmwgroup.com/en/report/2025 — 200 pages but the first 30 (management overview + segment financials) are all you need. This is primary source data.

### On Equity Research Technique
- **Mergers & Inquisitions — Equity Research free guides** — mergersandinquisitions.com/equity-research — Covers how to structure an initiation-of-coverage report (what you'll build in P9).
- **Kenji Explains (YouTube)** — His "How to Read a 10-K" and "Comps Table from Scratch" videos are directly relevant to what this project does.
- **CFA Institute — Equity Research and Valuation** — You've cleared CFA Level I, so you already have the foundation. Level II deepens equity valuation significantly — even reading the curriculum outline on equity analysis is useful for framing.

### Python / Code
- **Plotly Express vs Graph Objects** — plotly.com/python — We use `go.Figure()` (Graph Objects) rather than `px.` (Plotly Express) because GO gives you full control over multi-trace figures, subplots, and custom hover templates. Express is faster for simple charts but less flexible.
- **yfinance documentation** — pypi.org/project/yfinance — The `.info` dictionary keys are not documented officially but the GitHub wiki lists them. When a key returns 0 or None, it means Yahoo Finance doesn't have that data for that ticker.

---

## Part 5: What to Say When Someone Asks About This Project

**Short version (for a LinkedIn comment or introduction):**
"I built a Python equity research toolkit analysing the German auto sector — pulls live financials for BMW, Mercedes, VW, and Porsche, generates four interactive charts covering valuation multiples, EBIT margin trends, EV transition progress, and China exposure, and synthesises them into an investment thesis."

**Longer version (for an interview):**
"The German auto sector is arguably the most interesting equity story in Europe right now — two structural headwinds converging simultaneously. I built a Python project that quantifies both: on the valuation side, BMW trades at 6.1x P/E, which is 60-70% below market averages, reflecting the market pricing in significant downside from China share loss and EV transition costs. On the fundamental side, VW's EBIT margin has compressed to ~3% while BMW has held ~6.6% — you can see the operational divergence clearly in the margin trend chart. My thesis is that BMW is the highest-quality expression of a German auto recovery: cheapest multiples, strongest EV progress among German OEMs at 20.6% BEV mix, net cash balance sheet, and the Neue Klasse platform as a 2026-2027 catalyst. The risk is that China doesn't stabilise — VW has 24.2% China revenue exposure, BMW around 19%, and if Chinese OEMs continue gaining European share, margin recovery gets pushed out further."

---

*Last updated: June 2026. Part of the Shardul Pundir WHU Finance Prep project series.*
*Next: P4 — BMW Business Analysis (business model, competitive moat, segment deep-dive)*

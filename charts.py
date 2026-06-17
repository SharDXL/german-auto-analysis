"""
charts.py
---------
Four Plotly visualisations for the German Auto Industry Analysis.

Chart 1 — Valuation Comps:     EV/EBITDA vs P/E scatter (live data)
Chart 2 — Margin Trends:       EBIT margin over 5 years per OEM (live data)
Chart 3 — EV Transition:       BEV mix % per OEM over time vs EU 2035 mandate
Chart 4 — China Exposure:      China revenue % per OEM declining over time
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import os

CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Colour palette — one colour per OEM, consistent across all charts
OEM_COLOURS = {
    "BMW":      "#1A56DB",   # blue
    "Mercedes": "#111827",   # near-black
    "VW":       "#059669",   # green
    "Porsche":  "#D97706",   # amber
    "Tesla":    "#DC2626",   # red
}


# ── Chart 1: Valuation Comps ──────────────────────────────────────────────────

def plot_valuation_comps(df: pd.DataFrame) -> str:
    """
    Scatter: EV/EBITDA (Y) vs P/E (X).
    Each bubble sized by Market Cap.
    Bottom-left = cheap on both = value.
    """
    df = df[df["PE_Ratio"] > 0].copy()

    fig = go.Figure()

    for _, row in df.iterrows():
        oem = row["OEM"]
        colour = OEM_COLOURS.get(oem, "#6B7280")
        fig.add_trace(go.Scatter(
            x=[row["PE_Ratio"]],
            y=[row["EV_EBITDA"]],
            mode="markers+text",
            marker=dict(
                size=max(row["Market_Cap_Bn"] ** 0.45, 15),
                color=colour,
                line=dict(width=1.5, color="white"),
                opacity=0.88,
            ),
            text=[oem],
            textposition="top center",
            textfont=dict(size=12, color=colour),
            name=oem,
            hovertemplate=(
                f"<b>{oem}</b><br>"
                f"P/E: {row['PE_Ratio']}x<br>"
                f"EV/EBITDA: {row['EV_EBITDA']}x<br>"
                f"Market Cap: €{row['Market_Cap_Bn']}bn<br>"
                f"Op. Margin: {row['Operating_Margin_Pct']}%<extra></extra>"
            ),
        ))

    # Quadrant annotation
    fig.add_annotation(x=0.02, y=0.98, xref="paper", yref="paper",
        text="◀ Cheap on earnings | Expensive on EBITDA ▲",
        showarrow=False, font=dict(size=9, color="#9CA3AF"), align="left")
    fig.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper",
        text="◀ Best value zone (low on both multiples)",
        showarrow=False, font=dict(size=9, color="#059669"), align="left")

    fig.update_layout(
        title=dict(text="<b>German Auto OEMs — Valuation Comps</b><br>"
                        "<sup>EV/EBITDA vs P/E | bubble size = market cap | bottom-left = cheapest</sup>",
                   x=0.5, font=dict(size=16)),
        xaxis=dict(title="P/E Ratio (x)", showgrid=True, gridcolor="#F3F4F6", zeroline=False),
        yaxis=dict(title="EV/EBITDA (x)", showgrid=True, gridcolor="#F3F4F6", zeroline=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=520,
        margin=dict(l=60, r=40, t=90, b=60),
    )

    path = os.path.join(CHARTS_DIR, "01_valuation_comps.html")
    fig.write_html(path)
    try:
        fig.write_image(path.replace(".html", ".png"), scale=2)
    except Exception:
        pass  # PNG export requires Chrome/kaleido — HTML always works
    print(f"  ✓ Chart 1 saved → {path}")
    return path


# ── Chart 2: EBIT Margin Trends ───────────────────────────────────────────────

def plot_margin_trends(financials: dict) -> str:
    """
    Line chart: EBIT margin % per OEM, last 4 fiscal years.
    Shows the VW deterioration vs BMW/Mercedes stability story.
    """
    fig = go.Figure()

    for oem, df in financials.items():
        df = df.dropna(subset=["EBIT_Margin_Pct"])
        colour = OEM_COLOURS.get(oem, "#6B7280")
        fig.add_trace(go.Scatter(
            x=df.index.tolist(),
            y=df["EBIT_Margin_Pct"].tolist(),
            mode="lines+markers",
            name=oem,
            line=dict(color=colour, width=2.5),
            marker=dict(size=8, color=colour),
            hovertemplate=f"<b>{oem}</b><br>Year: %{{x}}<br>EBIT Margin: %{{y:.1f}}%<extra></extra>",
        ))

    # Add industry average reference line at ~5%
    fig.add_hline(y=5, line_dash="dot", line_color="#D1D5DB",
                  annotation_text="~5% industry floor", annotation_position="bottom right",
                  annotation_font=dict(size=9, color="#9CA3AF"))

    fig.update_layout(
        title=dict(text="<b>EBIT Margin Trends — German OEMs</b><br>"
                        "<sup>Automotive segment | VW margin collapse vs BMW/Mercedes resilience</sup>",
                   x=0.5, font=dict(size=16)),
        xaxis=dict(title="Fiscal Year", showgrid=False, dtick=1),
        yaxis=dict(title="EBIT Margin (%)", showgrid=True, gridcolor="#F3F4F6",
                   ticksuffix="%"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=480,
        margin=dict(l=60, r=40, t=90, b=60),
    )

    path = os.path.join(CHARTS_DIR, "02_margin_trends.html")
    fig.write_html(path)
    try:
        fig.write_image(path.replace(".html", ".png"), scale=2)
    except Exception:
        pass
    print(f"  ✓ Chart 2 saved → {path}")
    return path


# ── Chart 3: EV Transition Scorecard ─────────────────────────────────────────

def plot_ev_transition(ev_df: pd.DataFrame) -> str:
    """
    Line chart: BEV mix % per OEM over 2020–2025.
    Overlays EU 2035 mandate trajectory as a dashed target line.
    """
    fig = go.Figure()

    oems_to_plot = ["BMW", "Mercedes", "VW_Group", "Porsche", "Tesla"]

    for oem in oems_to_plot:
        subset = ev_df[ev_df["OEM"] == oem].sort_values("Year")
        display = oem.replace("_Group", "")
        colour = OEM_COLOURS.get(display, "#6B7280")
        fig.add_trace(go.Scatter(
            x=subset["Year"].tolist(),
            y=subset["BEV_Mix_Pct"].tolist(),
            mode="lines+markers",
            name=display,
            line=dict(color=colour, width=2.5,
                      dash="dot" if oem == "Tesla" else "solid"),
            marker=dict(size=7),
            hovertemplate=f"<b>{display}</b><br>Year: %{{x}}<br>BEV Mix: %{{y:.1f}}%<extra></extra>",
        ))

    # EU mandate trajectory: ~15% by 2025, 100% by 2035 (indicative)
    mandate_years = [2020, 2021, 2022, 2023, 2024, 2025]
    mandate_pct   = [2.5,  5.0,  8.0, 11.0, 14.0, 17.0]
    fig.add_trace(go.Scatter(
        x=mandate_years, y=mandate_pct,
        mode="lines",
        name="EU Mandate Trajectory",
        line=dict(color="#6B7280", width=1.5, dash="dash"),
        hovertemplate="EU Target: %{y:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        title=dict(text="<b>EV Transition Scorecard — OEM BEV Mix %</b><br>"
                        "<sup>Battery electric vehicles as % of total deliveries | dashed = EU mandate trajectory</sup>",
                   x=0.5, font=dict(size=16)),
        xaxis=dict(title="Year", showgrid=False, dtick=1),
        yaxis=dict(title="BEV Mix (%)", showgrid=True, gridcolor="#F3F4F6",
                   ticksuffix="%", range=[0, 105]),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=480,
        margin=dict(l=60, r=40, t=90, b=60),
    )

    path = os.path.join(CHARTS_DIR, "03_ev_transition.html")
    fig.write_html(path)
    try:
        fig.write_image(path.replace(".html", ".png"), scale=2)
    except Exception:
        pass
    print(f"  ✓ Chart 3 saved → {path}")
    return path


# ── Chart 4: China Revenue Exposure ──────────────────────────────────────────

def plot_china_exposure(china_df: pd.DataFrame) -> str:
    """
    Two-panel chart:
    Top: China revenue % per OEM per year (line)
    Bottom: China units sold (area — shows volume erosion)
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("China Revenue as % of Group Revenue",
                        "China Units Sold (thousands)"),
    )

    oems = ["BMW", "Mercedes", "VW_Group", "Porsche"]
    display_names = {"VW_Group": "VW Group"}

    for oem in oems:
        subset = china_df[china_df["OEM"] == oem].sort_values("Year")
        display = display_names.get(oem, oem)
        colour = OEM_COLOURS.get(display.replace(" Group", ""), "#6B7280")

        # Top panel: China %
        fig.add_trace(go.Scatter(
            x=subset["Year"].tolist(),
            y=subset["China_Pct"].tolist(),
            mode="lines+markers",
            name=display,
            line=dict(color=colour, width=2.5),
            marker=dict(size=7),
            hovertemplate=f"<b>{display}</b><br>Year: %{{x}}<br>China %: %{{y:.1f}}%<extra></extra>",
            legendgroup=display,
        ), row=1, col=1)

        # Bottom panel: China units (thousands)
        fig.add_trace(go.Scatter(
            x=subset["Year"].tolist(),
            y=(subset["China_Units_Sold"] / 1000).round(1).tolist(),
            mode="lines+markers",
            name=display,
            line=dict(color=colour, width=2, dash="dot"),
            marker=dict(size=6),
            showlegend=False,
            hovertemplate=f"<b>{display}</b><br>Year: %{{x}}<br>China units: %{{y:.0f}}k<extra></extra>",
            legendgroup=display,
        ), row=2, col=1)

    fig.update_yaxes(title_text="China Revenue %", ticksuffix="%",
                     showgrid=True, gridcolor="#F3F4F6", row=1, col=1)
    fig.update_yaxes(title_text="Units (thousands)",
                     showgrid=True, gridcolor="#F3F4F6", row=2, col=1)
    fig.update_xaxes(showgrid=False, dtick=1, row=2, col=1)

    fig.update_layout(
        title=dict(text="<b>China Exposure — From Profit Engine to Liability</b><br>"
                        "<sup>Revenue % and unit volume 2020–2025 | all OEMs losing ground</sup>",
                   x=0.5, font=dict(size=16)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=620,
        margin=dict(l=60, r=40, t=100, b=60),
    )

    path = os.path.join(CHARTS_DIR, "04_china_exposure.html")
    fig.write_html(path)
    try:
        fig.write_image(path.replace(".html", ".png"), scale=2)
    except Exception:
        pass
    print(f"  ✓ Chart 4 saved → {path}")
    return path

"""
analysis.py
-----------
Main runner for the German Auto Industry Analysis project.

Usage:
    python analysis.py

Runs all modules in sequence:
  1. Fetches live OEM data via yfinance
  2. Runs data vintage check (consistency across sources)
  3. Generates four Plotly charts (saved to /charts/)
  4. Prints a summary investment snapshot to the terminal
"""

import auto_data as ad
import charts as ch
import pandas as pd

SEPARATOR = "-" * 60


def print_header(text: str):
    print(f"\n{SEPARATOR}")
    print(f"  {text}")
    print(SEPARATOR)


def run():
    print("\n" + "=" * 60)
    print("  GERMAN AUTO INDUSTRY ANALYSIS -- Shardul Pundir")
    print("  github.com/SharDXL/german-auto-analysis")
    print("=" * 60)

    # -- 1. Live OEM Snapshot --------------------------------------------------
    print_header("1/4 -- Fetching live OEM data")
    oem_df = ad.fetch_oem_info()

    print("\n  Valuation Snapshot:")
    snap = oem_df[["OEM", "Market_Cap_Bn", "EV_EBITDA", "PE_Ratio",
                    "Operating_Margin_Pct", "ROE_Pct"]].copy()
    snap.columns = ["OEM", "Mkt Cap (Ebn)", "EV/EBITDA", "P/E", "Op Margin %", "RoE %"]
    print(snap.to_string(index=False))

    # -- 2. Annual Financials --------------------------------------------------
    print_header("2/4 -- Fetching annual financials")
    financials = ad.fetch_annual_financials()

    # -- 3. Static Data --------------------------------------------------------
    print_header("3/4 -- Loading static datasets")
    ev_df    = ad.load_ev_data()
    china_df = ad.load_china_data()
    print(f"  EV mix data:    {ev_df.shape[0]} rows")
    print(f"  China exposure: {china_df.shape[0]} rows")

    # -- Data Vintage Check ----------------------------------------------------
    print_header("Data Vintage Check")
    ad.check_data_vintage(financials, ev_df, china_df)

    # -- 4. Generate Charts ----------------------------------------------------
    print_header("4/4 -- Generating charts")

    ch.plot_valuation_comps(oem_df)
    ch.plot_margin_trends(financials)
    ch.plot_ev_transition(ev_df)
    ch.plot_china_exposure(china_df)

    # -- 5. Investment Snapshot ------------------------------------------------
    print_header("Investment Snapshot")

    valid = oem_df[oem_df["EV_EBITDA"] > 0]
    if not valid.empty:
        cheapest_ev_ebitda = valid.loc[valid["EV_EBITDA"].idxmin(), "OEM"]
        cheapest_pe        = valid.loc[valid["PE_Ratio"].idxmin(), "OEM"]
        highest_margin     = oem_df.loc[oem_df["Operating_Margin_Pct"].idxmax(), "OEM"]
        print(f"\n  Cheapest on EV/EBITDA : {cheapest_ev_ebitda}")
        print(f"  Cheapest on P/E        : {cheapest_pe}")
        print(f"  Highest op. margin     : {highest_margin}")

    print("\n  China Revenue Exposure (2025):")
    china_2025 = china_df[china_df["Year"] == 2025][["OEM", "China_Pct"]]
    china_2025 = china_2025.sort_values("China_Pct", ascending=False)
    for _, row in china_2025.iterrows():
        bar = "#" * int(row["China_Pct"] / 2)
        print(f"    {row['OEM']:<12} {row['China_Pct']:>5.1f}%  {bar}")

    print("\n  BEV Mix -- 2025 Deliveries:")
    ev_2025 = ev_df[ev_df["Year"] == 2025][["OEM", "BEV_Mix_Pct"]]
    for _, row in ev_2025.iterrows():
        bar = "#" * int(row["BEV_Mix_Pct"] / 5)
        print(f"    {row['OEM']:<12} {row['BEV_Mix_Pct']:>5.1f}%  {bar}")

    print(f"\n{SEPARATOR}")
    print("  All charts saved to /charts/")
    print("  Open .html files for interactive versions")
    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    run()

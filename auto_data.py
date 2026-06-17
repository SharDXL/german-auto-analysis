"""
auto_data.py
------------
Data fetching layer for the German Auto Analysis project.
Pulls live financials and price data via yfinance.
Static EV mix and China exposure data loaded from /data/ CSVs.
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Base Year - all analysis anchored to this
# FY2025 is the most recent complete fiscal year for all German OEMs.
# Live market data (prices, TTM multiples) is stamped with today's date.
# When building the equity research report, clearly label:
#   - Historicals  -> FY2021-FY2025
#   - Forecasts    -> FY2026E-FY2028E
#   - Market data  -> as of DATA_AS_OF_DATE
BASE_YEAR       = 2025
DATA_AS_OF_DATE = datetime.today().strftime("%d %b %Y")

# OEM Universe
OEMS = {
    "BMW":      "BMW.DE",
    "Mercedes": "MBG.DE",
    "VW":       "VOW3.DE",
    "Porsche":  "P911.DE",
    "Tesla":    "TSLA",
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def fetch_oem_info() -> pd.DataFrame:
    """Pull key financial metrics for each OEM via yfinance."""
    rows = []
    for name, ticker in OEMS.items():
        try:
            t = yf.Ticker(ticker)
            info = t.info
            rows.append({
                "OEM":                  name,
                "Ticker":               ticker,
                "Market_Cap_Bn":        round(info.get("marketCap", 0) / 1e9, 1),
                "Revenue_Bn":           round(info.get("totalRevenue", 0) / 1e9, 1),
                "EBITDA_Bn":            round(info.get("ebitda", 0) / 1e9, 1),
                "Net_Income_Bn":        round(info.get("netIncomeToCommon", 0) / 1e9, 1),
                "Total_Debt_Bn":        round(info.get("totalDebt", 0) / 1e9, 1),
                "Cash_Bn":              round(info.get("totalCash", 0) / 1e9, 1),
                "PE_Ratio":             round(info.get("trailingPE", 0), 1),
                "EV_EBITDA":            round(info.get("enterpriseToEbitda", 0), 1),
                "EV_Revenue":           round(info.get("enterpriseToRevenue", 0), 1),
                "Gross_Margin_Pct":     round((info.get("grossMargins", 0) or 0) * 100, 1),
                "Operating_Margin_Pct": round((info.get("operatingMargins", 0) or 0) * 100, 1),
                "ROE_Pct":              round((info.get("returnOnEquity", 0) or 0) * 100, 1),
                "52W_High":             round(info.get("fiftyTwoWeekHigh", 0), 2),
                "52W_Low":              round(info.get("fiftyTwoWeekLow", 0), 2),
                "Current_Price":        round(info.get("currentPrice", 0), 2),
            })
            print(f"  OK {name} ({ticker})")
        except Exception as e:
            print(f"  FAIL {name} ({ticker}): {e}")
    return pd.DataFrame(rows)


def fetch_price_history(period: str = "5y") -> pd.DataFrame:
    """Pull adjusted close prices for all OEMs. Returns wide DataFrame indexed by Date."""
    tickers = list(OEMS.values())
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)["Close"]
    reverse = {v: k for k, v in OEMS.items()}
    raw.rename(columns=reverse, inplace=True)
    normalised = raw.div(raw.iloc[0]) * 100
    return normalised


def fetch_annual_financials() -> dict:
    """Pull annual income statement data. Returns {OEM: DataFrame}."""
    result = {}
    for name, ticker in OEMS.items():
        if name == "Tesla":
            continue
        try:
            t = yf.Ticker(ticker)
            inc = t.financials
            if inc is None or inc.empty:
                continue
            df = pd.DataFrame()
            df["Revenue_Bn"] = (inc.loc["Total Revenue"] / 1e9).round(1) if "Total Revenue" in inc.index else None
            df["EBIT_Bn"]    = (inc.loc["EBIT"] / 1e9).round(1) if "EBIT" in inc.index else None
            df["EBIT_Margin_Pct"] = ((df["EBIT_Bn"] / df["Revenue_Bn"]) * 100).round(1)
            df.index = pd.to_datetime(df.index).year
            df = df.sort_index()
            result[name] = df
            print(f"  OK {name} financials")
        except Exception as e:
            print(f"  FAIL {name} financials: {e}")
    return result


def load_ev_data() -> pd.DataFrame:
    """Load EV mix data from data/ev_mix.csv"""
    return pd.read_csv(os.path.join(DATA_DIR, "ev_mix.csv"))


def load_china_data() -> pd.DataFrame:
    """Load China revenue exposure data from data/china_exposure.csv"""
    return pd.read_csv(os.path.join(DATA_DIR, "china_exposure.csv"))


def check_data_vintage(financials: dict, ev_df: pd.DataFrame, china_df: pd.DataFrame):
    """
    Prints a data consistency report to the terminal.

    Why this matters: the equity research report (P9) combines live yfinance
    data (TTM) with static CSVs (FY2020-FY2025). If any source is missing
    FY2025, the conclusions will be inconsistent. This flags mismatches on
    every run so nothing slips through.
    """
    SEP = "-" * 55
    print(f"\n{SEP}")
    print("  DATA VINTAGE CHECK")
    print(f"  Base year   : FY{BASE_YEAR}")
    print(f"  Market data : TTM as of {DATA_AS_OF_DATE}")
    print(SEP)

    print("\n  Annual Financials (yfinance):")
    for oem, df in financials.items():
        years = sorted(df.index.tolist())
        status = "OK" if BASE_YEAR in years else "WARNING: FY2025 MISSING"
        print(f"    {oem:<12} FY{years[0]}-FY{years[-1]}  {status}")

    print("\n  EV Mix CSV:")
    for oem in ev_df["OEM"].unique():
        years = sorted(ev_df[ev_df["OEM"] == oem]["Year"].tolist())
        status = "OK" if BASE_YEAR in years else f"WARNING: {BASE_YEAR} MISSING"
        print(f"    {oem:<12} {years[0]}-{years[-1]}  {status}")

    print("\n  China Exposure CSV:")
    for oem in china_df["OEM"].unique():
        years = sorted(china_df[china_df["OEM"] == oem]["Year"].tolist())
        status = "OK" if BASE_YEAR in years else f"WARNING: {BASE_YEAR} MISSING"
        print(f"    {oem:<12} {years[0]}-{years[-1]}  {status}")

    print(f"\n  NOTE: Valuation multiples (EV/EBITDA, P/E) in Chart 1 are")
    print(f"  TTM as of {DATA_AS_OF_DATE}, NOT FY{BASE_YEAR}.")
    print(f"  Label them accordingly in any report.")
    print(f"{SEP}\n")

# app/data.py
from __future__ import annotations
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests
import streamlit as st


# --- Public helpers (same names you already import) ---
@st.cache_data(ttl=60 * 10, show_spinner=False)
def generate_ohlc_data(symbol: str, n_days: int) -> pd.DataFrame:
    """
    Fetch OHLC from Kraken and keep extra lookback data for indicators.
    """
    pair = _symbol_to_kraken_pair(symbol)
    # Add 100-day buffer for indicators like RSI(14), SMA(20)
    buffer_days = 100
    end_dt = datetime.now(timezone.utc).date()
    start_dt = end_dt - timedelta(days=max(n_days + buffer_days, 120))
    since = int(datetime.combine(start_dt, datetime.min.time(), tzinfo=timezone.utc).timestamp())

    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": pair, "interval": 1440, "since": since}
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    payload = resp.json()

    if payload.get("error"):
        raise RuntimeError(f"Kraken API error: {payload['error']}")

    result = payload.get("result", {})
    keys = [k for k in result.keys() if k != "last"]
    if not keys:
        raise RuntimeError("Kraken response missing OHLC data")
    pair_key = keys[0]
    rows = result[pair_key]

    df = pd.DataFrame(
        rows,
        columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"],
    )

    df["time"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert(None)
    for col in ["open", "high", "low", "close", "vwap", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["open", "high", "low", "close", "volume"]).sort_values("time")
    df = df.rename(columns={"time": "date"})[["date", "open", "high", "low", "close", "volume"]]

    # Keep last n_days + RSI warmup
    df = df.tail(n_days + 14).reset_index(drop=True)
    return df


def sma(series: pd.Series, w: int) -> pd.Series:
    return series.rolling(w, min_periods=w).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """
    Compute RSI with extra smoothing and warm-up handling.
    """
    ret = close.diff()
    gain = ret.clip(lower=0)
    loss = -ret.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


# --- Internal: map UI symbols to Kraken pairs robustly ---
def _symbol_to_kraken_pair(symbol: str) -> str:
    s = symbol.upper()
    # Kraken uses XBT for BTC; others generally standard
    mapping = {
        "BTC": "XBTUSD",
        "XBT": "XBTUSD",
        "ETH": "ETHUSD",
        "SOL": "SOLUSD",
        "XRP": "XRPUSD",
    }
    return mapping.get(s, f"{s}USD")

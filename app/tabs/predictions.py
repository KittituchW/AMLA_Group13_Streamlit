import importlib
import requests
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests.exceptions as req_exc


# --- ensure repo root is importable (students/ is outside app/) ---
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Choose the import style that matches your project
try:
    from app.data import generate_ohlc_data
except ModuleNotFoundError:
    from data import generate_ohlc_data

# Map sidebar coin -> students module path
COIN_TO_MODULE = {
    "BTC": "students.Dylan",
    "ETH": "students.Kittituch",
    "SOL": "students.Shawya",
    "XRP": "students.Ratticha",
}

# Map coin -> exact endpoint suffix (case-sensitive as per your APIs)
COIN_TO_ENDPOINT = {
    "BTC": "bitcoin",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "XRP": "xrp",
}

# A tiny cache for the HTTP session so we reuse connections
@st.cache_resource
def _http_session():
    s = requests.Session()
    s.headers.update({"User-Agent": "CryptoInsight/1.0"})

    retry = Retry(
        total=2,                 # small retry count to keep UX snappy
        backoff_factor=0.6,     # 0.6s, 1.2s ...
        status_forcelist=[408, 429, 500, 502, 503, 504, 522, 524],
        allowed_methods=["GET", "POST"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

@st.cache_data(ttl=60)
def _check_health_url(api_url: str) -> bool:
    """Try /health if it exists, else do a tiny predict probe."""
    base = api_url.rstrip("/")
    # Prefer /health if available
    try:
        r = _http_session().get(f"{base}/health", timeout=3)
        if r.ok:
            return True
    except Exception:
        pass

    # Fallback: tiny predict (works for your /predict/<coin>?price=)
    try:
        # Pick a default coin endpoint that exists in your mapping
        # We call a *very cheap* predict to force cold-start load.
        fallback_coin = next(iter(COIN_TO_ENDPOINT.values()))
        url = f"{base}/predict/{fallback_coin}"
        r = _http_session().get(url, params={"price": 1.0}, timeout=5)
        return r.ok
    except Exception:
        return False

def prewarm_prediction_for_coin(coin: str) -> bool:
    """Pre-warm the specific student's API behind the chosen coin."""
    # Avoid repeated work in one session
    ready_key = f"pred_ready_{coin}"
    if st.session_state.get(ready_key):
        return True

    module = _get_student_module(coin)
    api_url = getattr(module, "API_URL", None)
    if not api_url:
        # No API to warm, consider it ready (prevents tab errors)
        st.session_state[ready_key] = True
        return True

    ok = _check_health_url(api_url)
    st.session_state[ready_key] = bool(ok)
    return bool(ok)


def _get_student_module(coin: str):
    mod_path = COIN_TO_MODULE.get(coin)
    if not mod_path:
        st.error(f"No student module mapped for coin '{coin}'.")
        st.stop()
    try:
        return importlib.import_module(mod_path)
    except Exception as e:
        st.error(f"Failed to import {mod_path}: {e}")
        st.stop()

def _fetch_api_prediction(module, endpoint_suffix: str, price: float) -> dict:
    api_url = getattr(module, "API_URL", None)
    if not api_url:
        st.error(f"{module.__name__} has no API_URL defined.")
        st.stop()

    base = api_url.rstrip("/")
    if base.lower().endswith("/predict"):
        base = base[: -len("/predict")]

    url = f"{base}/predict/{endpoint_suffix}"

    try:
        res = _http_session().get(url, params={"price": float(price)}, timeout=10)
        res.raise_for_status()
    except Exception as e:
        st.error(f"Error calling API {url}: {e}")
        st.stop()

    try:
        raw = res.json()
    except Exception:
        st.error(f"API {url} did not return valid JSON. Got: {res.text[:300]}")
        st.stop()

    # handle nested prediction key
    data = raw.get("prediction", raw)

    # try to extract only from these keys
    pred_val = None
    for key in ["bitcoin_predicted_next_day_high", "predicted_next_day_high"]:
        if key in data:
            pred_val = data[key]
            break

    if pred_val is None:
        st.error(f"Expected keys not found. Got: {data}")
        st.stop()

    try:
        predicted_high = float(pred_val)
    except Exception:
        st.error(f"Value under key is not numeric: {pred_val}")
        st.stop()

    # optional model name
    model_name = getattr(module, "MODEL_NAME", "Unknown")

    return {"predictedHigh": predicted_high, "modelName": model_name}



def render(coin: str, days: int):
    # ---------- HEADER ----------
    col_title, col_btn = st.columns([6, 1])
    with col_title:
        st.subheader(f"Tomorrow's Predicted HIGH — {coin}")
    with col_btn:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        refresh_clicked = st.button("↻ Refresh", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if refresh_clicked:
        st.cache_data.clear()

    # ---------- PREWARM GUARD ----------
    ready_key = f"pred_ready_{coin}"
    if not st.session_state.get(ready_key, False):
        ok = prewarm_prediction_for_coin(coin)
        if not ok:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.info("Warming up the model service… If this is the first run or a cold start, it can take a moment.")
            with c2:
                if st.button("Warm up now", use_container_width=True):
                    if prewarm_prediction_for_coin(coin):
                        st.success("Ready!")
                        st.rerun()
                    else:
                        st.error("Still not ready. Check your API is up and reachable.")
            st.stop()  # avoid calling the predict endpoint until ready

    # ---------- DATA ----------
    ohlc = generate_ohlc_data(coin, max(days, 30))
    current_price = float(ohlc.iloc[-1]["close"])

    # ---------- Route to the correct student + endpoint ----------
    module = _get_student_module(coin)
    endpoint_suffix = COIN_TO_ENDPOINT.get(coin)
    if not endpoint_suffix:
        st.error(f"No endpoint suffix mapped for coin '{coin}'.")
        st.stop()

    pred = _fetch_api_prediction(module, endpoint_suffix, current_price)

    delta_pct = (pred["predictedHigh"] - current_price) / max(current_price, 1e-6) * 100

    with st.container():
        st.caption(f"Based on {pred['modelName']}")

        cols = st.columns([2, 1, 7])
        with cols[0]:
            st.markdown(
                f"<div style='font-size:40px;font-weight:800;'>${pred['predictedHigh']:,.2f}</div>",
                unsafe_allow_html=True,
            )
        with cols[0]:
            pill_color = "#22c55e" if delta_pct >= 0 else "#ef4444"
            st.markdown(
                f"<div style='display:inline-block;padding:6px 10px;border-radius:999px;background:{pill_color};"
                f"color:white;font-weight:600;'>{delta_pct:+.2f}%</div>",
                unsafe_allow_html=True,
            )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                "<div style='margin-top:20px; color:rgba(255,255,255,.6); font-size:0.8rem;'>Current Price</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:23px; font-weight:800; color:white;'>${current_price:,.2f}</div>",
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                "<div style='margin-top:20px; color:rgba(255,255,255,.6); font-size:0.8rem;'>Model Used</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='font-size:23px; font-weight:800; color:white;'>{pred['modelName']}</div>",
                unsafe_allow_html=True
            )



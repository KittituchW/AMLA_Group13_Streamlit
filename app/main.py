import pkgutil
from pathlib import Path
import streamlit as st

from tabs.ui import style_sidebar
from tabs.overview import render as render_overview
from tabs.ohlc import render as render_ohlc
from tabs.predictions import render as render_predictions
from tabs.team import render as render_team
from tabs.predictions import prewarm_prediction_for_coin

# ---------- Page config ----------
st.set_page_config(
    page_title="Crypto Insight",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Sidebar ----------
style_sidebar()
with st.sidebar:
    st.markdown("<div class='brand'>🚀 Crypto Insight</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AT3 - UTS Project</div>", unsafe_allow_html=True)

    # Card: coin
    with st.container():
        st.markdown("<div class='card-title'>☰&nbsp;&nbsp;Select Cryptocurrency</div>", unsafe_allow_html=True)
        coin = st.selectbox(
            "coin",
            ["BTC", "ETH", "SOL", "XRP"],
            index=1,
            label_visibility="collapsed",
            key="coin_select",
        )

    # Card: date range
    with st.container():
        st.markdown("<div class='card-title'>&nbsp;&nbsp;Date Range</div>", unsafe_allow_html=True)
        days_label = st.selectbox(
            "range",
            ["Last 30 Days", "Last 60 Days", "Last 90 Days", "Last 180 Days"],
            index=3,
            label_visibility="collapsed",
            key="date_range_select",
        )
        days = {"Last 30 Days": 30, "Last 60 Days": 60, "Last 90 Days": 90, "Last 180 Days": 180}[days_label]

    # Card: toggle
    with st.container():
        st.markdown("<div class='card-title toggle-row'>Show Indicators <span></span></div>", unsafe_allow_html=True)
        show_ind = st.toggle(" ", value=True, label_visibility="collapsed", key="show_ind_toggle")
    
    with st.container():
        st.markdown(
            """
            <div class="disclaimer-text">
            <strong>Disclaimer:</strong><br>
            This service is for informational purposes only and not financial advice. 
            No guarantee is made on model accuracy. Always do your own research or consult 
            a licensed professional before making investment decisions.
            </div>
            """,
            unsafe_allow_html=True
        )

    prewarm_prediction_for_coin(coin)


# ---------- Tabs ----------
tab_overview, tab_ohlc, tab_pred, tab_students = st.tabs(
    ["Overview", "OHLC + Indicators", "Predictions", "Team"]
)

with tab_overview:
    render_overview(coin=coin, days=days)

with tab_ohlc:
    render_ohlc(coin=coin, days=days, show_ind=show_ind)

with tab_pred:
    render_predictions(coin=coin, days=days)

with tab_students:
    render_team()

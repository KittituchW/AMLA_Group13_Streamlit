import plotly.express as px
import streamlit as st
from data import generate_ohlc_data   # use from app.data if you kept package imports

def render(coin: str, days: int):
    st.subheader(f"Overview — {coin}")
    
    df = generate_ohlc_data(coin, days)
    latest, prev = df.iloc[-1], df.iloc[-2]
    change24 = (latest.close - prev.close) / max(prev.close, 1e-6) * 100

    # ===== KPI ROW wrapped by BIG CARD =====
    with st.container():
        st.markdown("<div class='as-card'></div>", unsafe_allow_html=True)  # outer big card

        c1, c2, c3, c4 = st.columns(4)

        # ---- KPI 1 (mini card) ----
        with c1:
            with st.container():
                st.markdown("<div class='as-mini'></div>", unsafe_allow_html=True)
                st.markdown("<div class='kpi-header'>Last Close</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='kpi-value'>${latest.close:,.2f}</div>", unsafe_allow_html=True)
                cls = "kpi-delta-pos" if change24 >= 0 else "kpi-delta-neg"
                st.markdown(f"<span class='{cls}'>{change24:+.2f}%</span>", unsafe_allow_html=True)

        # ---- KPI 2 (mini card) ----
        with c2:
            with st.container():
                st.markdown("<div class='as-mini'></div>", unsafe_allow_html=True)
                st.markdown("<div class='kpi-header'>24h High</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='kpi-value'>${latest.high:,.2f}</div>", unsafe_allow_html=True)

        # ---- KPI 3 (mini card) ----
        with c3:
            with st.container():
                st.markdown("<div class='as-mini'></div>", unsafe_allow_html=True)
                st.markdown("<div class='kpi-header'>24h Low</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='kpi-value'>${latest.low:,.2f}</div>", unsafe_allow_html=True)

        # ---- KPI 4 (mini card) ----
        with c4:
            with st.container():
                st.markdown("<div class='as-mini'></div>", unsafe_allow_html=True)
                st.markdown("<div class='kpi-header'>Volume</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='kpi-value'>{latest.volume/1000:.2f}k</div>", unsafe_allow_html=True)

    # ===== Chart (still in its own big card) =====
    with st.container():
        # st.markdown("<div class='as-card'></div>", unsafe_allow_html=True)
        st.markdown(f"### Price History – {coin}")
        fig = px.line(df, x="date", y="close", title=None)
        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(t=30, b=30, l=30, r=30),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

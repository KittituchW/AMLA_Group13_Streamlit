# # app/tabs/ohlc.py
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# import streamlit as st
# from datetime import datetime

# from app.data import generate_ohlc_data, sma, rsi

# def render(coin: str, days: int, show_ind: bool):
#     st.subheader(f"🕯️ OHLC + Indicators — {coin}")

#     # 1) Pull data WITH warm-up (generate_ohlc_data already fetches extra history)
#     df_full = generate_ohlc_data(coin, max(days, 60))   # function internally adds buffer for indicators

#     # 2) Drop a possibly-partial "today" candle (Kraken sometimes returns it)
#     if not df_full.empty and df_full["date"].iloc[-1].date() >= datetime.utcnow().date():
#         df_full = df_full.iloc[:-1]

#     # 3) Compute indicators on the FULL series (uses warm-up), then slice to last N for display
#     df_full = df_full.sort_values("date").reset_index(drop=True)

#     # SMAs (compute on full, then cut)
#     sma7_full  = sma(df_full["close"], 7)
#     sma20_full = sma(df_full["close"], 20)

#     # RSI (compute on full, EMA-style from data.py)
#     rsi_full = rsi(df_full["close"], 14)

#     # 4) Visible window (last N days) — no NaNs since we computed using warm-up
#     df = df_full.tail(days).reset_index(drop=True)
#     sma7  = sma7_full.tail(days).reset_index(drop=True)
#     sma20 = sma20_full.tail(days).reset_index(drop=True)
#     rsi_vis = rsi_full.tail(days).reset_index(drop=True)

#     # =======================
#     # TOP: Candles + Volume + SMAs
#     # =======================
#     with st.container(border=True):
#         st.markdown("### 📈 Candlestick Chart + Moving Averages")

#         fig = go.Figure()

#         # Candles
#         fig.add_trace(go.Candlestick(
#             x=df["date"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
#             name="OHLC",
#             increasing_line_color="#00FFAA",
#             decreasing_line_color="#FF5C5C",
#         ))

#         # Volume (secondary axis)
#         fig.add_trace(go.Bar(
#             x=df["date"],
#             y=(df["volume"] / 1_000_000),
#             name="Volume (M)",
#             marker_color="#1E90FF",
#             opacity=0.3,
#             yaxis="y2",
#         ))

#         # SMAs
#         if show_ind:
#             fig.add_trace(go.Scatter(
#                 x=df["date"], y=sma7, mode="lines", name="SMA(7)",
#                 line=dict(width=2, color="#00BFFF")
#             ))
#             fig.add_trace(go.Scatter(
#                 x=df["date"], y=sma20, mode="lines", name="SMA(20)",
#                 line=dict(width=2, color="#00FFAA")
#             ))

#         fig.update_layout(
#             template="plotly_dark",
#             height=500,
#             margin=dict(t=50, b=30, l=30, r=30),
#             xaxis_rangeslider_visible=False,
#             xaxis=dict(title=None),
#             yaxis=dict(title="Price", side="right"),
#             yaxis2=dict(overlaying="y", side="left", showgrid=False, title="Volume (M)",
#                         range=[0, max(1.0, (df["volume"].max() / 1_000_000) * 3)]),
#             legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
#             plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
#         )
#         st.plotly_chart(fig, use_container_width=True)

#     # =======================
#     # BOTTOM: RSI with bands
#     # =======================
#     if show_ind:
#         with st.container(border=True):
#             st.markdown("### 💹 RSI (14)")

#             rsi_df = pd.DataFrame({"date": df["date"], "rsi": rsi_vis})

#             fig2 = go.Figure()

#             # RSI line
#             fig2.add_trace(go.Scatter(
#                 x=rsi_df["date"], y=rsi_df["rsi"],
#                 mode="lines", name="RSI(14)"
#             ))

#             # Overbought/Oversold shaded regions
#             fig2.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.10)", line_width=0, layer="below")
#             fig2.add_hrect(y0=0,  y1=30,  fillcolor="rgba(34,197,94,0.10)", line_width=0, layer="below")

#             # Reference lines
#             for lvl in (30, 50, 70):
#                 fig2.add_hline(y=lvl, line=dict(width=1, dash="dot", color="rgba(255,255,255,0.35)"))

#             fig2.update_yaxes(range=[0, 100], title="RSI")
#             fig2.update_layout(
#                 template="plotly_dark",
#                 height=250,
#                 margin=dict(t=30, b=30, l=30, r=30),
#                 showlegend=False,
#                 plot_bgcolor="#0E1117",
#                 paper_bgcolor="#0E1117",
#             )
#             st.plotly_chart(fig2, use_container_width=True)

#         st.caption("Guide: Oversold < 30, Neutral ≈ 50, Overbought > 70")
# app/tabs/ohlc.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from datetime import datetime

from data import generate_ohlc_data, sma, rsi

def render(coin: str, days: int, show_ind: bool):
    st.subheader(f"🕯️ OHLC + Indicators — {coin}")

    # 1) Pull data WITH warm-up (generate_ohlc_data already fetches extra history)
    df_full = generate_ohlc_data(coin, max(days, 60))   # function internally adds buffer for indicators

    # 2) Drop a possibly-partial "today" candle (Kraken sometimes returns it)
    if not df_full.empty and df_full["date"].iloc[-1].date() >= datetime.utcnow().date():
        df_full = df_full.iloc[:-1]

    # 3) Compute indicators on the FULL series (uses warm-up), then slice to last N for display
    df_full = df_full.sort_values("date").reset_index(drop=True)

    # SMAs (compute on full, then cut)
    sma7_full  = sma(df_full["close"], 7)
    sma20_full = sma(df_full["close"], 20)

    # RSI (compute on full, EMA-style from data.py)
    rsi_full = rsi(df_full["close"], 14)

    # 4) Visible window (last N days) — no NaNs since we computed using warm-up
    df = df_full.tail(days).reset_index(drop=True)
    sma7  = sma7_full.tail(days).reset_index(drop=True)
    sma20 = sma20_full.tail(days).reset_index(drop=True)
    rsi_vis = rsi_full.tail(days).reset_index(drop=True)

    # =======================
    # TOP: Candles + Volume + SMAs
    # =======================
    with st.container(border=True):
        st.markdown("### 📈 Candlestick Chart + Moving Averages")

        fig = go.Figure()

        # Candles
        fig.add_trace(go.Candlestick(
            x=df["date"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
            name="OHLC",
            increasing_line_color="#00FFAA",
            decreasing_line_color="#FF5C5C",
        ))

        # Volume (secondary axis)
        fig.add_trace(go.Bar(
            x=df["date"],
            y=(df["volume"] / 1_000_000),
            name="Volume (M)",
            marker_color="#1E90FF",
            opacity=0.3,
            yaxis="y2",
        ))

        # SMAs
        if show_ind:
            fig.add_trace(go.Scatter(
                x=df["date"], y=sma7, mode="lines", name="SMA(7)",
                line=dict(width=2, color="#00BFFF")
            ))
            fig.add_trace(go.Scatter(
                x=df["date"], y=sma20, mode="lines", name="SMA(20)",
                line=dict(width=2, color="#00FFAA")
            ))

        fig.update_layout(
            template="plotly_dark",
            height=500,
            margin=dict(t=50, b=30, l=30, r=30),
            xaxis_rangeslider_visible=False,
            xaxis=dict(title=None),
            yaxis=dict(title="Price", side="right"),
            yaxis2=dict(overlaying="y", side="left", showgrid=False, title="Volume (M)",
                        range=[0, max(1.0, (df["volume"].max() / 1_000_000) * 3)]),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
        )
        st.plotly_chart(fig, use_container_width=True)

    # =======================
    # BOTTOM: RSI with bands
    # =======================
    if show_ind:
        with st.container(border=True):
            st.markdown("### 💹 RSI (14)")

            rsi_df = pd.DataFrame({"date": df["date"], "rsi": rsi_vis})

            fig2 = go.Figure()

            # RSI line
            fig2.add_trace(go.Scatter(
                x=rsi_df["date"], y=rsi_df["rsi"],
                mode="lines", name="RSI(14)",
                line=dict(color="rgb(255,170,50)", width=2.5)
            ))

            # Overbought/Oversold shaded regions
            fig2.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.10)", line_width=0, layer="below")
            fig2.add_hrect(y0=0,  y1=30,  fillcolor="rgba(34,197,94,0.10)", line_width=0, layer="below")

            # Reference lines
            for lvl in (30, 50, 70):
                fig2.add_hline(y=lvl, line=dict(width=1, dash="dot", color="rgba(255,255,255,0.35)"))

            fig2.update_yaxes(range=[0, 100], title="RSI")
            fig2.update_layout(
                template="plotly_dark",
                height=250,
                margin=dict(t=30, b=30, l=30, r=30),
                showlegend=False,
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.caption("Guide: Oversold < 30, Neutral ≈ 50, Overbought > 70")

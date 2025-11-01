import streamlit as st

def render():
    # ===== PROJECT TEAM HEADER =====
    st.markdown("<h2 style='color:#fff; margin:0;'>Project Team</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:rgba(255,255,255,0.7);'>"
        "Meet the team behind AMLA AT3 — Crypto Price Prediction Dashboard</p>",
        unsafe_allow_html=True
    )

    # ===== TEAM MEMBER CARDS =====
    team_members = [
        {
            "emoji": "🐱",
            "name": "Kittituch Wongwatcharapaiboon",
            "Student ID": "25544646",
            "role": "Linear Regression",
            "metrics": {"RMSE": "126.09", "MAE": "92.26", "MAPE": "2.88%", "R²": "0.94"},
            "university": "UTS - University of Technology Sydney",
        },
        {
            "emoji": "🦊",
            "name": "Ratticha Ratanawarocha",
            "Student ID": "24996427",
            "role": "LightGBM",
            "metrics": {"RMSE": "0.09", "MAE": "0.04", "MAPE": "4.01%", "R²": "0.97"},
            "university": "UTS - University of Technology Sydney",
        },
        {
            "emoji": "🐼",
            "name": "Shawya Saito",
            "Student ID": "25552249",
            "role": "XGBoost",
            "metrics": {"RMSE": "8.65", "MAE": "6.50", "MAPE": "3.58%", "R²": "0.95"},
            "university": "UTS - University of Technology Sydney",
        },
        {
            "emoji": "🦁",
            "name": "Dylan Jun Jie Leong",
            "Student ID": "25400603",
            "role": "CatBoost",
            "metrics": {"RMSE": "159.76", "MAE": "126.45", "MAPE": "2.74%", "R²": "0.960"},
            "university": "UTS - University of Technology Sydney",
        },
    ]

    # Two-column layout
    for i in range(0, len(team_members), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(team_members):
                member = team_members[i + j]
                metrics_html = "".join(
                    f"<div style='display:flex; justify-content:space-between;'>"
                    f"<span>{k}</span><span><b>{v}</b></span></div>"
                    for k, v in member["metrics"].items()
                )
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            background:rgba(255,255,255,0.05);
                            border:1px solid rgba(255,255,255,0.08);
                            border-radius:16px;
                            padding:20px 22px;
                            margin-bottom:20px;
                            box-shadow:0 0 20px rgba(0,0,0,0.35);
                        ">
                            <div style="font-size:1.2rem; font-weight:700; color:#fff;">
                                {member['emoji']} {member['name']}
                            </div>
                            <div style="color:rgba(255,255,255,0.8); font-size:0.95rem; margin-bottom:12px;">
                                {member['role']}
                            </div>
                            <div style="font-weight:600; margin-top:6px; font-size:0.9rem; color:#fff;">
                                Model Metrics
                            </div>
                            <div style="color:rgba(255,255,255,0.85); font-size:0.9rem; margin-bottom:14px;">
                                {metrics_html}
                            </div>
                            <div style="
                                border-top:1px solid rgba(255,255,255,0.1);
                                padding-top:10px;
                                color:rgba(255,255,255,0.6);
                                font-size:0.85rem;
                                text-align:center;
                            ">
                                {member['university']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ===== ABOUT THIS PROJECT =====
    st.markdown("<h2 style='color:#fff; margin-top:6px;'>About This Project</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background:rgba(255,255,255,0.05);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:16px;
            padding:22px 24px;
            margin-top:10px;
            box-shadow:0 0 20px rgba(0,0,0,0.35);
        ">
        <p style="color:rgba(255,255,255,0.85); font-size:0.95rem; line-height:1.6;">
        <b>AMLA AT3 - Advanced Machine Learning Application</b> focuses on predicting cryptocurrency price movements 
        using different regression algorithms. The project integrates <b>machine learning</b> models such as 
        Linear Regression, LightGBM, XGBoost, and CatBoost to forecast the next-day <b>high price</b> of Ethereum (ETH).
        </p>
        <ul style="color:rgba(255,255,255,0.85); font-size:0.95rem; line-height:1.6;">
            <li>Model performance comparison using RMSE, MAE, MAPE, and R² metrics</li>
            <li>Data preprocessing and feature engineering on OHLCV and technical indicators</li>
            <li>Integration of Streamlit dashboard with FastAPI model endpoints</li>
            <li>Interactive visualizations for price trends and prediction insights</li>
            <li>Collaborative work aligned with AMLA learning outcomes at UTS</li>
        </ul>
        <p style="color:rgba(255,255,255,0.7); font-size:0.9rem;">
        All displayed metrics are based on test set evaluation within the AT3 project scope.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

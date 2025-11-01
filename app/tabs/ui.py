import streamlit as st

def style_sidebar():
    st.markdown(
        """
        <style>
        @media (prefers-color-scheme: light) {
        body, [data-testid="stSidebar"] {
            color: #0b0e1b !important; /* dark text for light mode */
        }
        .faded, .subtitle {
            color: rgba(0,0,0,.6) !important;
        }
        }

        @media (prefers-color-scheme: dark) {
        body, [data-testid="stSidebar"] {
            color: #fff !important; /* white text for dark mode */
        }
        }
        /* Sidebar background */
        [data-testid="stSidebar"]{
            background: radial-gradient(1100px 680px at 28% 18%, #1a1f3b 0%, #0f142a 55%, #0b0e1b 100%);
            border-right: 1px solid rgba(255,255,255,.06);
        }
        [data-testid="stSidebar"] .block-container{
            padding: 1rem .6rem 1.4rem .6rem;
        }
        [data-testid="stSidebar"] .subtitle,
        [data-testid="stSidebar"] .card-title,
        [data-testid="stSidebar"] .subtitle,
        [data-testid="stSidebar"] .card-title,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption {
            color: white !important;
        }
        /* Force selectbox text (selected value + dropdown items) to white */
        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: white !important;
        }
        [data-baseweb="tab-list"] button p {
            color: white !important;
            transition: color 0.2s ease;
        }

        [data-baseweb="tab-list"] button[aria-selected="true"] p {
            color: #ff4b4b !important; /* bright red */
            font-weight: 700;
        }
        /* Card container */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]:has(.card-title){
            background: rgba(255,255,255,.045);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 18px;
            padding: 16px 14px 18px 14px;
            margin: 14px 0;
            box-shadow: 0 8px 30px rgba(2,8,23,.35);
        }

        .card-title{
            font-size: .95rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: .5rem;
            margin-bottom: 8px;
        }

        /* Selectbox smaller and fully inside card */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"]:has(.card-title)
          [data-testid="stSelectbox"] > div > div{
            width: calc(100% - 30px) !important;
            margin-right: 7px !important;
            padding: 6px 10px !important;
            min-height: 45px !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,.15);
            background: rgba(0,0,0,.3);
            font-size: .85rem !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            line-height: 1 !important;
        }

        /* Hide BaseWeb right blob overflow completely */
        [data-baseweb="select"] > div{
            box-shadow: none !important;
            overflow: hidden !important;
        }

        /* Resize right arrow icon */
        [data-baseweb="select"] svg{
            transform: scale(.7);
            margin-right: 2px;
        }

        /* Text label clamp */
        [data-baseweb="select"] [class*="singleValue"]{
            font-size: .85rem !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* Dropdown menu: same width and compact font */
        [data-baseweb="popover"]{
            width: 85% !important;
            max-width: 240px !important;
            font-size: .85rem !important;
            border-radius: 10px !important;
        }

        /* Toggle row and pills */
        .toggle-row{ display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; }
        [data-testid="stToggle"] label div{ border-radius:20px !important; transform: scale(.9); }

        .pill{ display:inline-block; padding:6px 12px; border-radius:999px; font-weight:700; font-size:.8rem; }
        .pill.active{ background:#34d399; color:#0b0e1b; }
        .pill.limited{ background:#7c3aed; color:#fff; box-shadow:0 0 20px rgba(124,58,237,.35); }

        /* Brand + subtitle */
        .brand{
            font-size:1.7rem;
            font-weight:900;
            background: linear-gradient(90deg,#5ad2ff,#6ee7b7);
            -webkit-background-clip:text;
            color:transparent;
            display:flex; align-items:center; gap:.5rem;
            margin:.2rem 0 .15rem 0;
        }
        .subtitle{ color:rgba(255,255,255,.7); margin-bottom:.35rem; }

        /* Footer line */
        hr.side{
            border:none; height:1px;
            background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);
            margin:14px 0 10px 0;
        }
        .faded{ color:rgba(255,255,255,.46); text-align:center; }

        /* Invisible anchor used to "cardify" Streamlit containers */
        .as-card{ display:none; }

        /* Style ANY main-area Streamlit block that contains the anchor */
        [data-testid="stVerticalBlock"]:has(.as-card){
        background: radial-gradient(900px at 30% 15%, #1b103f 0%, #0f0824 65%, #090516 100%);
        border: 1px solid rgba(180,150,255,0.18);
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(120,70,255,0.18);
        padding: 18px 20px 22px 20px;
        margin: 10px 0 18px 0;
        }

        /* KPI text tweaks */
        .kpi-header{ color:rgba(255,255,255,.8); font-weight:700; font-size:.95rem; margin-bottom:4px; }
        .kpi-value{ font-size:1.8rem; font-weight:800; line-height:1.1; }
        .kpi-delta-pos{ color:#22c55e; font-weight:600; }
        .kpi-delta-neg{ color:#ef4444; font-weight:600; }

        /* Mini KPI cards (used inside Overview big card) */
        .as-mini{ display:none; }  /* invisible anchor */

        </style>
        """,
        unsafe_allow_html=True,
    )

def status_pill(text: str) -> str:
    cls = "active" if text.lower() == "active" else "limited"
    return f"<span class='pill {cls}'>{text}</span>"

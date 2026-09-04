import streamlit as st

GLOBAL_CSS = """
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* App background — deep blue like the reference design */
    .stApp {
        background: radial-gradient(circle at 30% 20%, #1e3a9c 0%, #14237a 45%, #0d1a5c 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14237a 0%, #0d1a5c 100%);
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    /* White content cards */
    .gym-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem 2.2rem;
        box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    }

    h1, h2, h3 { color: #4a4a4a; }

    /* Gradient buttons like LOG IN button in the reference image */
    div.stButton > button, .stDownloadButton > button {
        background: linear-gradient(90deg, #f0955a 0%, #e0646a 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.6rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: transform 0.15s ease;
    }
    div.stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        opacity: 0.92;
        color: white;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #f7f7fb;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #eee;
    }

    /* Inputs — pill shaped like the reference design */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] > div {
        border-radius: 30px !important;
    }
</style>
"""


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

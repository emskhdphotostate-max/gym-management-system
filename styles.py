import streamlit as st

# ---------- Login page theme (dark blue, matches the reference design) ----------
LOGIN_CSS = """
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .stApp {
        background: radial-gradient(circle at 30% 20%, #1e3a9c 0%, #14237a 45%, #0d1a5c 100%);
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border-radius: 24px;
        padding: 2.5rem 2.5rem 1.5rem 2.5rem;
        box-shadow: 0 25px 60px rgba(0,0,0,0.35);
        max-width: 420px;
        margin: 3rem auto 0 auto;
    }
    .login-title { text-align: center; font-size: 2.2rem; font-weight: 800; color: #4a4a4a; margin-bottom: 0.2rem;}
    .login-sub { text-align: center; color: #9a9a9a; margin-bottom: 1.8rem; font-size: 0.95rem;}

    div.stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #f0955a 0%, #e0646a 100%);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.6rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 30px !important;
    }
</style>
"""

# ---------- Internal app theme (light, readable, dark sidebar) ----------
APP_CSS = """
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* Light, clean main background */
    .stApp {
        background: #f4f5fa;
    }

    /* Dark navy sidebar with white text */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14237a 0%, #0d1a5c 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] a {
        color: #ffffff !important;
    }

    /* Readable dark text everywhere in main content */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {
        color: #1f2430 !important;
    }
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] li {
        color: #3a3f4b !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Card-style bordered containers (st.container(border=True)) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-radius: 18px;
        box-shadow: 0 6px 24px rgba(20,35,122,0.08);
    }

    /* Gradient buttons */
    div.stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #f0955a 0%, #e0646a 100%);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.55rem 1.5rem;
        font-weight: 700;
    }
    div.stButton > button:hover, .stDownloadButton > button:hover {
        opacity: 0.92;
        color: white !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid #eceef5;
        box-shadow: 0 2px 10px rgba(20,35,122,0.05);
    }
    div[data-testid="stMetric"] label { color: #6b7280 !important; }
    div[data-testid="stMetric"] div { color: #1f2430 !important; }

    /* Inputs — light, pill shaped, readable */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-baseweb="select"] > div,
    div[data-testid="stTextArea"] textarea {
        border-radius: 10px !important;
        background: #ffffff !important;
        color: #1f2430 !important;
        border: 1px solid #dfe2ee !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] { color: #3a3f4b !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #e0646a !important; }

    /* Dataframes / tables */
    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 12px;
    }
</style>
"""


def inject_login_css():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)


def inject_app_css():
    st.markdown(APP_CSS, unsafe_allow_html=True)


# Backward-compatible alias (older pages may still import this name)
def inject_global_css():
    inject_app_css()

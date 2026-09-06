import streamlit as st

# ---------- Login page theme (premium gradient) ----------
LOGIN_CSS = """
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Hide Streamlit's default nav completely on login */
    div[data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    ul[data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    /* Premium gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        min-height: 100vh;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Premium glassmorphism card */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem 2.5rem 2rem 2.5rem;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.3),
                    0 10px 30px rgba(102, 126, 234, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
        max-width: 440px;
        margin: 3rem auto 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Logo container styling */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Login title */
    .login-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }

    /* Subtitle */
    .login-sub {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1rem;
        font-weight: 500;
    }

    /* Premium gradient button */
    div.stButton > button,
    .stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }

    /* Premium input fields */
    div[data-testid="stTextInput"] input {
        border-radius: 15px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        background: #ffffff !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* Checkbox styling */
    div[data-testid="stCheckbox"] {
        margin: 0.5rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# ---------- Internal app theme ----------
APP_CSS = """
<style>
    /* CRITICAL: Hide default Streamlit nav */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    .stApp {
        background: #f4f5fa;
    }

    /* Dark navy sidebar */
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

    /* Card-style containers */
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

    /* Inputs */
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

    /* Dataframes */
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


# Backward-compatible alias
def inject_global_css():
    inject_app_css()

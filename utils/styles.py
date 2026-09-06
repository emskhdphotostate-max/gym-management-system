import streamlit as st

# ---------- Login page theme (premium dark blue gradient) ----------
LOGIN_CSS = """
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
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

# ---------- Internal app theme (light, readable, dark sidebar) ----------
APP_CSS = """
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* CRITICAL: Completely hide Streamlit's default auto-generated multipage nav */
    div[data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    div[data-testid="stSidebarNavSeparator"],
    ul[data-testid="stSidebarNavItems"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Light, clean main background */
    .stApp {
        background: #f8fafc;
    }

    /* Dark navy sidebar with sleek gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Custom Sidebar Navigation Links */
    [data-testid="stPageLink-NavLink"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        margin-bottom: 0.4rem !important;
        transition: all 0.25s ease !important;
    }

    [data-testid="stPageLink-NavLink"]:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(129, 140, 248, 0.4) !important;
        transform: translateX(4px);
    }

    /* Readable dark text everywhere in main content */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] li {
        color: #334155 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }

    /* Card-style bordered containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04) !important;
        padding: 1.5rem !important;
    }

    /* Gradient buttons */
    div.stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.6rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover, .stDownloadButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
        opacity: 0.95 !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06) !important;
        border-color: #cbd5e1 !important;
    }

    div[data-testid="stMetric"] label { color: #64748b !important; font-weight: 600 !important; }
    div[data-testid="stMetric"] div { color: #0f172a !important; font-weight: 800 !important; }

    /* Inputs — modern, crisp borders */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-baseweb="select"] > div,
    div[data-testid="stTextArea"] textarea {
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1.5px solid #cbd5e1 !important;
        padding: 0.6rem 0.9rem !important;
    }

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4f46e5 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #4f46e5 !important;
    }

    /* Dataframes / tables */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        overflow: hidden !important;
    }

    /* Clean divider */
    hr {
        margin: 1.5rem 0 !important;
        border-color: #e2e8f0 !important;
    }
</style>
"""
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

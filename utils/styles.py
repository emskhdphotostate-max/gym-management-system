import streamlit as st

# ---------- Login page theme (VIP Crystal Luxury with Animated Gym Background) ----------
LOGIN_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Hide Streamlit default navigation and chrome */
    div[data-testid="stSidebarNav"],
    section[data-testid="stSidebar"],
    [data-testid="stSidebarNavItems"],
    [data-testid="collapsedControl"],
    #MainMenu, footer, header {
        display: none !important;
        visibility: hidden !important;
    }

    /* Animated VIP Gym Dynamic Background */
    .stApp {
        background:
            radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.22) 0%, transparent 40%),
            radial-gradient(circle at 85% 20%, rgba(236, 72, 153, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 50% 85%, rgba(14, 165, 233, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #0b0f19 0%, #111827 50%, #030712 100%) !important;
        background-size: 200% 200% !important;
        animation: gymAmbientMove 18s ease infinite alternate !important;
        min-height: 100vh;
    }

    @keyframes gymAmbientMove {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* Subtle gym fitness background grid/pattern */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
        background-size: 28px 28px;
        pointer-events: none;
        z-index: 0;
    }

    /* Main container alignment */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 520px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
    }

    /* Ultra VIP Crystal Glass Card */
    div[data-testid="stForm"] {
        background: rgba(17, 24, 39, 0.75) !important;
        backdrop-filter: blur(30px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(190%) !important;
        border-radius: 28px !important;
        padding: 2.5rem 2.2rem 1.8rem 2.2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow:
            0 25px 50px -12px rgba(0, 0, 0, 0.65),
            0 0 40px rgba(99, 102, 241, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        margin: 1.5rem auto 0 auto !important;
    }

    /* Centered Header Box */
    .vip-header {
        text-align: center;
        margin-bottom: 1.8rem;
    }

    .vip-logo-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 88px;
        height: 88px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(236, 72, 153, 0.2) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        margin: 0 auto 1.2rem auto;
        padding: 10px;
        animation: pulseGlow 4s ease-in-out infinite alternate;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 25px rgba(99, 102, 241, 0.3); transform: scale(1); }
        100% { box-shadow: 0 0 35px rgba(236, 72, 153, 0.45); transform: scale(1.03); }
    }

    .vip-logo-badge img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    .vip-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem;
    }

    .vip-subtitle {
        font-size: 0.95rem;
        font-weight: 500;
        color: #94a3b8;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .vip-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        border: 1px solid rgba(165, 180, 252, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Premium Input Styling */
    div[data-testid="stTextInput"] input {
        border-radius: 14px !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        background: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        padding: 0.85rem 1.1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #818cf8 !important;
        background: rgba(15, 23, 42, 0.9) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.25) !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }

    /* Checkbox */
    div[data-testid="stCheckbox"] label span {
        color: #cbd5e1 !important;
        font-size: 0.9rem !important;
    }

    /* VIP Submit Button */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.85rem 1.8rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-transform: uppercase !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 15px 35px rgba(236, 72, 153, 0.45) !important;
    }

    /* Demo credentials glass badge */
    .vip-demo-badge {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 0.9rem 1.2rem;
        margin-top: 1.5rem;
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
    }

    .vip-demo-badge strong {
        color: #f1f5f9;
    }
</style>
"""

# ---------- Internal app theme (VIP Crystal Luxury Dashboard & Sidebar) ----------
APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* CRITICAL: Completely hide Streamlit default multipage navigation */
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

    /* App Background */
    .stApp {
        background: #f1f5f9;
    }

    /* VIP Dark Obsidian Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090d16 0%, #0f172a 40%, #090d16 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 25px rgba(0, 0, 0, 0.3) !important;
    }

    /* Sidebar Logo Header */
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }

    .sidebar-brand-name {
        font-size: 1.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 0.4rem;
        letter-spacing: -0.3px;
    }

    /* CRITICAL FIX: Bright White Text on Dark Sidebar Navigation Links */
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] *,
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span,
    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] div,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a * {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        margin-bottom: 0.45rem !important;
        transition: all 0.22s ease !important;
    }

    section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.45) 0%, rgba(236, 72, 153, 0.35) 100%) !important;
        border-color: rgba(165, 180, 252, 0.5) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
    }

    /* VIP Sidebar Logout Button */
    section[data-testid="stSidebar"] div.stButton > button,
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.35) !important;
    }

    section[data-testid="stSidebar"] div.stButton > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* VIP Main Container Header */
    [data-testid="stAppViewContainer"] h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.8px;
        font-size: 2.1rem !important;
    }

    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span {
        color: #475569 !important;
    }

    /* VIP Crystal Bordered Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05) !important;
        padding: 1.6rem !important;
    }

    /* VIP Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04) !important;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08) !important;
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetric"] div {
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 1.65rem !important;
    }

    /* Main Area Buttons */
    div[data-testid="stAppViewContainer"] div.stButton > button,
    div[data-testid="stAppViewContainer"] .stDownloadButton > button,
    div[data-testid="stAppViewContainer"] div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.6rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.28) !important;
        transition: all 0.2s ease !important;
    }

    /* CRITICAL FIX: Force white text on all buttons */
    div[data-testid="stAppViewContainer"] div.stButton > button *,
    div[data-testid="stAppViewContainer"] .stDownloadButton > button *,
    div[data-testid="stAppViewContainer"] div[data-testid="stFormSubmitButton"] > button *,
    div[data-testid="stAppViewContainer"] div.stButton > button p,
    div[data-testid="stAppViewContainer"] .stDownloadButton > button p,
    div[data-testid="stAppViewContainer"] div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stAppViewContainer"] div.stButton > button span,
    div[data-testid="stAppViewContainer"] .stDownloadButton > button span,
    div[data-testid="stAppViewContainer"] div[data-testid="stFormSubmitButton"] > button span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    div[data-testid="stAppViewContainer"] div.stButton > button:hover,
    div[data-testid="stAppViewContainer"] .stDownloadButton > button:hover,
    div[data-testid="stAppViewContainer"] div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.4) !important;
        opacity: 0.95 !important;
    }

    /* Form Inputs */
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
        padding: 0.6rem 1.2rem !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4f46e5 !important;
        font-weight: 700 !important;
        background: rgba(99, 102, 241, 0.08) !important;
        border-bottom: 2px solid #4f46e5 !important;
    }

    /* Dataframe tables */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Badges */
    .status-active {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        background: #dcfce7;
        color: #15803d;
    }

    .status-inactive {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        background: #fee2e2;
        color: #b91c1c;
    }

    /* Member photo card preview */
    .member-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #6366f1;
    }
</style>
"""


def inject_login_css():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)


def inject_app_css():
    st.markdown(APP_CSS, unsafe_allow_html=True)


def inject_global_css():
    inject_app_css()

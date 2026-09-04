import streamlit as st
from utils.db import init_db
from utils.auth import check_password

# Page configuration
st.set_page_config(
    page_title="Iron Pulse Gym",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit top sidebar nav using CSS
st.markdown(
    """
    <style>
        /* Yeh default Streamlit pages menu ko sidebar se chupa dega */
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Database
init_db()

# Check authentication
if not check_password():
    st.stop()

# Main App Navigation & Pages Setup (Aap ka original code)
st.sidebar.title("IRON PULSE GYM")
st.sidebar.write(f"Logged in as **{st.session_state.get('username', 'admin')}**")

st.sidebar.markdown("---")
st.sidebar.page_link("app.py", label="Dashboard", icon="📊")
st.sidebar.page_link("pages/2_Members.py", label="Members", icon="👥")
st.sidebar.page_link("pages/3_Fee_Chalan.py", label="Fee / Chalan", icon="💳")
st.sidebar.page_link("pages/4_Timing.py", label="Gym Timing", icon="⏰")
st.sidebar.page_link("pages/5_Reports.py", label="Reports / PDF Export", icon="📄")

st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state["password_correct"] = False
    st.rerun()

# Dashboard Content
st.title("📊 Dashboard")
st.write("Quick overview of your gym's performance")

# Baqi ka dashboard content agar aap ka mazeed hai toh woh yahan aayega

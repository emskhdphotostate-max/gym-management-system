import streamlit as st
from utils.auth import check_auth, render_sidebar_auth, init_auth_state
from utils.db import init_db
from utils.styles import load_custom_styles

# Page configuration
st.set_page_config(
    page_title="Iron Pulse Gym",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom styles & hide default Streamlit top sidebar nav
load_custom_styles()
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

# Initialize Database & Auth State
init_db()
init_auth_state()

# Check authentication
if not check_auth():
    render_sidebar_auth()
    st.stop()

# Render Custom Sidebar for Authenticated Users
render_sidebar_auth()

# Main Dashboard Content Redirect / Display
# (Aap ka jo bhi baki code ya redirection yahan pehle se thi, wohi rahe gi)
st.title("🏋️‍♂️ Iron Pulse Gym Management System")
st.write("Welcome to the dashboard. Use the custom sidebar navigation on the left to switch between pages.")

# Agar aap yahan koi aur default view dikhana chahtay hain toh woh add kar saktay hain.

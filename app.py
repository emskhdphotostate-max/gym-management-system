import streamlit as st
from utils.db import init_db
from utils.auth import ensure_default_admin, login
from utils.styles import inject_global_css

st.set_page_config(
    page_title="Gym Admin Panel",
    page_icon="assets/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_global_css()

GYM_NAME = st.secrets.get("GYM_NAME", "IRON PULSE GYM")

# --- DB setup (runs once, cheap after that thanks to cache_resource) ---
try:
    init_db()
    ensure_default_admin()
    db_ready = True
except Exception as e:
    db_ready = False
    db_error = str(e)

st.markdown("""
<style>
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
    .logo-wrap { display: flex; justify-content: center; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("logged_in"):
    st.switch_page("pages/1_Dashboard.py")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("assets/logo.png", width=90)

st.markdown(f'<div class="login-title">Login</div>', unsafe_allow_html=True)
st.markdown(f'<div class="login-sub">{GYM_NAME} — Admin Panel</div>', unsafe_allow_html=True)

if not db_ready:
    st.error(
        "⚠️ Database not connected. Add your Neon connection string to "
        "`.streamlit/secrets.toml` as `NEON_DB_URL`.\n\nDetails: " + db_error
    )
else:
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("Password", placeholder="Password", type="password", label_visibility="collapsed")
        remember = st.checkbox("Remember me", value=True)
        submitted = st.form_submit_button("LOG IN", use_container_width=True)

        if submitted:
            if login(username, password):
                st.success("Login successful — redirecting...")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("❌ Invalid username or password.")

    st.markdown(
        "<p style='text-align:center; color:#9a9a9a; font-size:0.85rem; margin-top:0.5rem;'>"
        "Default demo login: <b>admin</b> / <b>Admin@123</b><br>"
        "(change this in .streamlit/secrets.toml)</p>",
        unsafe_allow_html=True,
    )

"""
Simple bcrypt-based auth for the admin panel.
"""

import bcrypt
import streamlit as st
from utils.db import get_admin_by_username, seed_default_admin


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except Exception:
        return False


def ensure_default_admin():
    """Creates the default admin account (from secrets.toml) the very first time the app runs."""
    username = st.secrets.get("DEFAULT_ADMIN_USERNAME", "admin")
    password = st.secrets.get("DEFAULT_ADMIN_PASSWORD", "Admin@123")
    seed_default_admin(username, hash_password(password))


def login(username: str, password: str) -> bool:
    row = get_admin_by_username(username)
    if row is None:
        return False
    _, db_username, password_hash = row
    if verify_password(password, password_hash):
        st.session_state["logged_in"] = True
        st.session_state["admin_username"] = db_username
        return True
    return False


def logout():
    for key in ["logged_in", "admin_username"]:
        if key in st.session_state:
            del st.session_state[key]


def require_login():
    """Call this at the top of every internal page. Redirects to login if not authenticated."""
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first.")
        st.stop()

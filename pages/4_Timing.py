import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_global_css
from utils.db import get_setting, set_setting, get_all_members

st.set_page_config(page_title="Timing | Gym Admin", page_icon="assets/logo.png", layout="wide")
inject_global_css()
require_login()

GYM_NAME = st.secrets.get("GYM_NAME", "IRON PULSE GYM")

with st.sidebar:
    st.image("assets/logo.png", width=70)
    st.markdown(f"### {GYM_NAME}")
    st.caption(f"Logged in as **{st.session_state.get('admin_username')}**")
    st.divider()
    st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.page_link("pages/2_Members.py", label="🧑‍🤝‍🧑 Members")
    st.page_link("pages/3_Fee_Chalan.py", label="🧾 Fee / Chalan")
    st.page_link("pages/4_Timing.py", label="⏰ Gym Timing")
    st.page_link("pages/5_Reports.py", label="📄 Reports / PDF Export")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("app.py")

st.markdown('<div class="gym-card">', unsafe_allow_html=True)
st.title("⏰ Gym Timing")

st.subheader("Gym Operating Hours")
with st.form("timing_form"):
    c1, c2 = st.columns(2)
    opening = c1.text_input("Opening Time", value=get_setting("opening_time", "06:00 AM"))
    closing = c2.text_input("Closing Time", value=get_setting("closing_time", "11:00 PM"))
    weekly_off = st.selectbox(
        "Weekly Off Day",
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        index=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(
            get_setting("weekly_off", "Sunday")
        ) if get_setting("weekly_off", "Sunday") in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] else 6,
    )
    if st.form_submit_button("💾 Save Timing", use_container_width=True):
        set_setting("opening_time", opening)
        set_setting("closing_time", closing)
        set_setting("weekly_off", weekly_off)
        st.success("✅ Gym timing updated.")
        st.rerun()

st.divider()
st.subheader("👥 Members by Preferred Slot")
df = get_all_members()
if df.empty:
    st.info("No members yet.")
else:
    for slot in ["Morning", "Evening", "Both"]:
        slot_df = df[df["time_slot"] == slot]
        with st.expander(f"{slot} ({len(slot_df)} members)"):
            if slot_df.empty:
                st.caption("No members in this slot.")
            else:
                st.dataframe(
                    slot_df[["full_name", "phone", "membership_type", "status"]],
                    use_container_width=True, hide_index=True,
                )

st.markdown('</div>', unsafe_allow_html=True)

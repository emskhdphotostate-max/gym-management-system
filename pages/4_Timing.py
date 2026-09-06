import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import get_setting, set_setting, get_all_members

st.set_page_config(page_title="Timing | Gym Admin", page_icon="assets/logo.png", layout="wide")
inject_app_css()
require_login()

GYM_NAME = st.secrets.get("GYM_NAME", "IRON PULSE GYM")

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <img src="https://raw.githubusercontent.com/emskhdphotostate-max/gym-management-system/main/assets/logo.png" width="55" style="border-radius:12px; margin-bottom:4px;">
        <div class="sidebar-brand-name">{GYM_NAME}</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Logged in: <strong style="color:#e2e8f0;">{st.session_state.get('admin_username')}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
    st.page_link("pages/2_Members.py", label="👥 Members Management")
    st.page_link("pages/3_Fee_Chalan.py", label="🧾 Fee & Chalan")
    st.page_link("pages/4_Timing.py", label="⏰ Gym Timing")
    st.page_link("pages/5_Reports.py", label="📄 Reports & Export")
    st.page_link("pages/6_Attendance.py", label="📋 Daily Attendance")
    st.page_link("pages/7_Expenses.py", label="💰 Expense & Profit")
    st.page_link("pages/8_Trainers.py", label="🏋️ Staff & Trainers")

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("app.py")

with st.container(border=True):
    st.title("⏰ Gym Operating Hours & Shifts")
    st.caption("Configure gym opening times, shifts, and member slot distribution")

    st.markdown("### 🕐 Gym Operating Hours")
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
        if st.form_submit_button("💾 Save Gym Timing", use_container_width=True):
            set_setting("opening_time", opening)
            set_setting("closing_time", closing)
            set_setting("weekly_off", weekly_off)
            st.success("✅ Gym operating hours updated successfully!")
            st.rerun()

    st.divider()
    st.markdown("### 👥 Members by Preferred Workout Slot")
    df = get_all_members()

    if df.empty:
        st.info("No members registered yet.")
    else:
        for slot in ["Morning", "Evening", "Both"]:
            slot_df = df[df["time_slot"] == slot]
            emoji = "🌅" if slot == "Morning" else ("🌆" if slot == "Evening" else "🔄")
            with st.expander(f"{emoji} {slot} Shift ({len(slot_df)} members)"):
                if slot_df.empty:
                    st.caption("No members prefer this time slot.")
                else:
                    st.dataframe(
                        slot_df[["full_name", "phone", "membership_type", "status"]],
                        use_container_width=True,
                        hide_index=True,
                    )

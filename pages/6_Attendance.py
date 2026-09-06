import streamlit as st
from datetime import date
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import get_all_members, mark_attendance, get_today_attendance, get_attendance_history

st.set_page_config(page_title="Attendance | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
    st.title("📋 Daily Member Attendance")
    st.caption(f"Track daily member check-ins and workout timings — **{date.today().strftime('%A, %d %B %Y')}**")

    tab1, tab2 = st.tabs(["⚡ Quick Check-in", "📜 Attendance Log"])

    with tab1:
        st.markdown("### 🏃 Quick Member Check-in")

        members_df = get_all_members()
        if members_df.empty:
            st.info("No members available. Please add members first.")
        else:
            active_members = members_df[members_df["status"] == "Active"]

            if active_members.empty:
                st.warning("No active members found.")
            else:
                col_sel, col_note = st.columns([2, 2])
                with col_sel:
                    member_id = st.selectbox(
                        "Select Member for Check-in",
                        active_members["id"].tolist(),
                        format_func=lambda x: f"{active_members[active_members['id'] == x]['full_name'].values[0]} ({active_members[active_members['id'] == x]['phone'].values[0]}) - {active_members[active_members['id'] == x]['time_slot'].values[0]}"
                    )

                with col_note:
                    notes = st.text_input("Notes (Optional)", placeholder="e.g. Cardio Day, Leg Workout")

                if st.button("✅ Mark Check-in Now", use_container_width=True):
                    mark_attendance(member_id, notes)
                    st.success("🎉 Check-in marked successfully!")
                    st.rerun()

        st.divider()
        st.markdown("### 📌 Today's Check-ins")
        today_df = get_today_attendance()

        if today_df.empty:
            st.info("No members checked in yet today.")
        else:
            st.caption(f"Total check-ins today: **{len(today_df)}**")
            st.dataframe(
                today_df[["time_in", "full_name", "phone", "membership_type", "time_slot", "notes"]],
                use_container_width=True,
                hide_index=True
            )

    with tab2:
        st.markdown("### 📜 Attendance History")
        history_df = get_attendance_history(200)

        if history_df.empty:
            st.info("No attendance history found.")
        else:
            st.dataframe(history_df, use_container_width=True, hide_index=True)

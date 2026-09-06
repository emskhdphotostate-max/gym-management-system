import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import get_all_members, get_all_fees
from utils.pdf_generator import generate_members_report_pdf, generate_fee_history_pdf
from datetime import date

st.set_page_config(page_title="Reports | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
    st.title("📄 Reports & Data Export")
    st.caption("Generate comprehensive reports and export data in PDF format for records & auditing")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Members Master Report")
        members_df = get_all_members()
        st.caption(f"Total Members: **{len(members_df)}**")

        if not members_df.empty:
            pdf_bytes = generate_members_report_pdf(GYM_NAME, members_df)
            st.download_button(
                "⬇️ Download Members List (PDF)",
                data=pdf_bytes,
                file_name=f"members_report_{date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("No members to export yet.")

    with col2:
        st.markdown("### 🧾 Fee Collection Report")
        fees_df = get_all_fees()
        st.caption(f"Total Fee Records: **{len(fees_df)}**")

        if not fees_df.empty:
            pdf_bytes2 = generate_fee_history_pdf(GYM_NAME, fees_df)
            st.download_button(
                "⬇️ Download Fee History (PDF)",
                data=pdf_bytes2,
                file_name=f"fee_history_{date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.info("No fee records to export yet.")

    st.divider()
    st.markdown("### 📊 Live Data Preview")

    tab1, tab2 = st.tabs(["👥 Members Data", "🧾 Fee Records"])

    with tab1:
        if members_df.empty:
            st.info("No member data available.")
        else:
            st.dataframe(members_df, use_container_width=True, hide_index=True)

    with tab2:
        if fees_df.empty:
            st.info("No fee data available.")
        else:
            st.dataframe(fees_df, use_container_width=True, hide_index=True)

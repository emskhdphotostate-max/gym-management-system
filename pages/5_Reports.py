import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_global_css
from utils.db import get_all_members, get_all_fees
from utils.pdf_generator import generate_members_report_pdf, generate_fee_history_pdf
from datetime import date

st.set_page_config(page_title="Reports | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
st.title("📄 Reports & PDF Export")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Members Report")
    members_df = get_all_members()
    st.caption(f"{len(members_df)} total members")
    if not members_df.empty:
        pdf_bytes = generate_members_report_pdf(GYM_NAME, members_df)
        st.download_button(
            "⬇️ Export Members List (PDF)", data=pdf_bytes,
            file_name=f"members_report_{date.today()}.pdf", mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.info("No members to export yet.")

with col2:
    st.subheader("🧾 Fee History Report")
    fees_df = get_all_fees()
    st.caption(f"{len(fees_df)} total fee records")
    if not fees_df.empty:
        pdf_bytes2 = generate_fee_history_pdf(GYM_NAME, fees_df)
        st.download_button(
            "⬇️ Export Fee History (PDF)", data=pdf_bytes2,
            file_name=f"fee_history_{date.today()}.pdf", mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.info("No fee records to export yet.")

st.divider()
st.subheader("📊 Raw Data Preview")
tab1, tab2 = st.tabs(["Members", "Fees"])
with tab1:
    st.dataframe(members_df, use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(fees_df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

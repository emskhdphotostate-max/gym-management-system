import streamlit as st
from datetime import date
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import (
    get_all_members, add_fee, generate_chalan_no,
    get_fees_for_member, get_fee_by_chalan, get_all_fees,
)
from utils.pdf_generator import generate_chalan_pdf

st.set_page_config(page_title="Fee / Chalan | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
    st.title("🧾 Fee & Chalan Management")
    st.caption("Collect monthly membership fees and generate payment receipts")

    members_df = get_all_members()

    tab1, tab2 = st.tabs(["💳 Collect Fee Payment", "📜 Fee Payment History"])

    with tab1:
        if members_df.empty:
            st.info("Add members first from the **Members** page.")
        else:
            st.markdown("### 💰 Record Fee Payment")
            member_id = st.selectbox(
                "Select Member",
                members_df["id"].tolist(),
                format_func=lambda x: f"{members_df[members_df['id']==x]['full_name'].values[0]} - {members_df[members_df['id']==x]['membership_type'].values[0]} (Rs. {float(members_df[members_df['id']==x]['monthly_fee'].values[0]):,.0f})"
            )
            selected = members_df[members_df["id"] == member_id].iloc[0]

            with st.form("fee_form"):
                c1, c2 = st.columns(2)
                amount = c1.number_input("Fee Amount (Rs.)", min_value=0.0, step=500.0, value=float(selected["monthly_fee"]))
                payment_method = c2.selectbox("Payment Method", ["Cash", "Bank Transfer", "Card", "JazzCash", "EasyPaisa", "NayaPay"])

                c3, c4 = st.columns(2)
                months = ["January","February","March","April","May","June","July",
                          "August","September","October","November","December"]
                month = c3.selectbox("Month", months, index=date.today().month - 1)
                year = c4.number_input("Year", min_value=2020, max_value=2100, value=date.today().year, step=1)

                paid_date = st.date_input("Payment Date", value=date.today())

                submitted = st.form_submit_button("💳 Collect Fee & Generate Chalan", use_container_width=True)

                if submitted:
                    chalan_no = generate_chalan_no()
                    add_fee({
                        "member_id": int(member_id),
                        "chalan_no": chalan_no,
                        "amount": amount,
                        "month": month,
                        "year": int(year),
                        "payment_method": payment_method,
                        "status": "Paid",
                        "paid_date": paid_date,
                    })
                    st.success(f"✅ Fee collected successfully! Chalan No: **{chalan_no}**")

                    fee_row = get_fee_by_chalan(chalan_no)
                    pdf_bytes = generate_chalan_pdf(GYM_NAME, fee_row)
                    st.download_button(
                        "⬇️ Download Payment Receipt (PDF)",
                        data=pdf_bytes,
                        file_name=f"{chalan_no}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

    with tab2:
        st.markdown("### 📜 All Fee Records")
        all_fees = get_all_fees()

        if all_fees.empty:
            st.info("No fee records yet.")
        else:
            search = st.text_input("🔍 Search by member name or chalan number")
            display_df = all_fees

            if search:
                display_df = all_fees[
                    all_fees["full_name"].str.contains(search, case=False, na=False) |
                    all_fees["chalan_no"].str.contains(search, case=False, na=False)
                ]

            st.dataframe(
                display_df[["chalan_no", "full_name", "phone", "amount", "month", "year",
                            "payment_method", "status", "paid_date"]],
                use_container_width=True,
                hide_index=True,
            )

            st.divider()
            st.markdown("### ⬇️ Download Receipt")
            chalan_choice = st.selectbox("Select Chalan No", display_df["chalan_no"].tolist())
            if st.button("📄 Generate PDF Receipt"):
                fee_row = get_fee_by_chalan(chalan_choice)
                pdf_bytes = generate_chalan_pdf(GYM_NAME, fee_row)
                st.download_button(
                    "⬇️ Download Chalan PDF",
                    data=pdf_bytes,
                    file_name=f"{chalan_choice}.pdf",
                    mime="application/pdf",
                )

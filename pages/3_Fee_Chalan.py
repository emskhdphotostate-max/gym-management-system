import streamlit as st
from datetime import date
from utils.auth import require_login, logout
from utils.styles import inject_global_css
from utils.db import (
    get_all_members, add_fee, generate_chalan_no,
    get_fees_for_member, get_fee_by_chalan, get_all_fees,
)
from utils.pdf_generator import generate_chalan_pdf

st.set_page_config(page_title="Fee / Chalan | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
st.title("🧾 Fee / Chalan Management")

members_df = get_all_members()

tab1, tab2 = st.tabs(["➕ Collect Fee", "📜 Fee History"])

with tab1:
    if members_df.empty:
        st.info("Add a member first from the **Members** page.")
    else:
        member_id = st.selectbox(
            "Select Member", members_df["id"].tolist(),
            format_func=lambda x: f"{members_df[members_df['id']==x]['full_name'].values[0]} "
                                   f"({members_df[members_df['id']==x]['phone'].values[0]})"
        )
        selected = members_df[members_df["id"] == member_id].iloc[0]

        with st.form("fee_form"):
            c1, c2 = st.columns(2)
            amount = c1.number_input("Amount (Rs.)", min_value=0.0, step=500.0, value=float(selected["monthly_fee"]))
            payment_method = c2.selectbox("Payment Method", ["Cash", "Bank Transfer", "Card", "JazzCash", "EasyPaisa"])
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
                    "member_id": int(member_id), "chalan_no": chalan_no, "amount": amount,
                    "month": month, "year": int(year), "payment_method": payment_method,
                    "status": "Paid", "paid_date": paid_date,
                })
                st.success(f"✅ Fee collected! Chalan No: **{chalan_no}**")

                fee_row = get_fee_by_chalan(chalan_no)
                pdf_bytes = generate_chalan_pdf(GYM_NAME, fee_row)
                st.download_button(
                    "⬇️ Download Chalan PDF", data=pdf_bytes,
                    file_name=f"{chalan_no}.pdf", mime="application/pdf",
                    use_container_width=True,
                )

with tab2:
    all_fees = get_all_fees()
    if all_fees.empty:
        st.info("No fee records yet.")
    else:
        search = st.text_input("🔍 Search by member name or chalan no")
        display_df = all_fees
        if search:
            display_df = all_fees[
                all_fees["full_name"].str.contains(search, case=False, na=False) |
                all_fees["chalan_no"].str.contains(search, case=False, na=False)
            ]
        st.dataframe(
            display_df[["chalan_no", "full_name", "phone", "amount", "month", "year",
                        "payment_method", "status", "paid_date"]],
            use_container_width=True, hide_index=True,
        )

        st.divider()
        st.subheader("⬇️ Download a specific chalan")
        chalan_choice = st.selectbox("Select Chalan No", display_df["chalan_no"].tolist())
        if st.button("Generate PDF for selected chalan"):
            fee_row = get_fee_by_chalan(chalan_choice)
            pdf_bytes = generate_chalan_pdf(GYM_NAME, fee_row)
            st.download_button(
                "⬇️ Download Chalan PDF", data=pdf_bytes,
                file_name=f"{chalan_choice}.pdf", mime="application/pdf",
            )

st.markdown('</div>', unsafe_allow_html=True)

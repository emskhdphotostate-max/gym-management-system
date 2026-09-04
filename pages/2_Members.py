import streamlit as st
from datetime import date
from utils.auth import require_login, logout
from utils.styles import inject_global_css
from utils.db import add_member, get_all_members, update_member, delete_member, get_member

st.set_page_config(page_title="Members | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
st.title("🧑‍🤝‍🧑 Members")

tab1, tab2 = st.tabs(["➕ Add New Member", "📋 All Members"])

with tab1:
    with st.form("add_member_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        full_name = c1.text_input("Full Name *")
        phone = c2.text_input("Phone Number")
        c3, c4 = st.columns(2)
        email = c3.text_input("Email")
        gender = c4.selectbox("Gender", ["Male", "Female", "Other"])
        address = st.text_area("Address", height=70)
        c5, c6, c7 = st.columns(3)
        membership_type = c5.selectbox("Membership Type", ["Standard", "Premium", "VIP", "Student"])
        monthly_fee = c6.number_input("Monthly Fee (Rs.)", min_value=0.0, step=500.0)
        time_slot = c7.selectbox("Preferred Timing", ["Morning", "Evening", "Both"])
        join_date = st.date_input("Join Date", value=date.today())

        submitted = st.form_submit_button("Add Member", use_container_width=True)
        if submitted:
            if not full_name:
                st.error("Full Name is required.")
            else:
                add_member({
                    "full_name": full_name, "phone": phone, "email": email,
                    "address": address, "gender": gender,
                    "membership_type": membership_type, "monthly_fee": monthly_fee,
                    "time_slot": time_slot, "join_date": join_date, "status": "Active",
                })
                st.success(f"✅ {full_name} added successfully!")
                st.rerun()

with tab2:
    df = get_all_members()
    if df.empty:
        st.info("No members added yet.")
    else:
        search = st.text_input("🔍 Search by name or phone")
        if search:
            df = df[df["full_name"].str.contains(search, case=False, na=False) |
                     df["phone"].astype(str).str.contains(search, case=False, na=False)]

        st.dataframe(
            df[["id", "full_name", "phone", "email", "membership_type", "monthly_fee",
                "time_slot", "status", "join_date"]],
            use_container_width=True, hide_index=True,
        )

        st.divider()
        st.subheader("✏️ Edit / ❌ Remove Member")
        if not df.empty:
            member_id = st.selectbox("Select Member", df["id"].tolist(),
                                      format_func=lambda x: df[df["id"] == x]["full_name"].values[0])
            m = get_member(member_id)
            if m:
                with st.form("edit_member_form"):
                    c1, c2 = st.columns(2)
                    e_name = c1.text_input("Full Name", value=m.full_name)
                    e_phone = c2.text_input("Phone", value=m.phone or "")
                    c3, c4 = st.columns(2)
                    e_email = c3.text_input("Email", value=m.email or "")
                    e_gender = c4.selectbox("Gender", ["Male", "Female", "Other"],
                                             index=["Male", "Female", "Other"].index(m.gender) if m.gender in ["Male","Female","Other"] else 0)
                    e_address = st.text_area("Address", value=m.address or "")
                    c5, c6, c7 = st.columns(3)
                    e_type = c5.selectbox("Membership Type", ["Standard", "Premium", "VIP", "Student"],
                                           index=["Standard","Premium","VIP","Student"].index(m.membership_type) if m.membership_type in ["Standard","Premium","VIP","Student"] else 0)
                    e_fee = c6.number_input("Monthly Fee", min_value=0.0, step=500.0, value=float(m.monthly_fee))
                    e_slot = c7.selectbox("Timing", ["Morning", "Evening", "Both"],
                                           index=["Morning","Evening","Both"].index(m.time_slot) if m.time_slot in ["Morning","Evening","Both"] else 0)
                    e_status = st.selectbox("Status", ["Active", "Inactive"],
                                             index=0 if m.status == "Active" else 1)

                    b1, b2 = st.columns(2)
                    update_btn = b1.form_submit_button("💾 Save Changes", use_container_width=True)
                    delete_btn = b2.form_submit_button("🗑️ Delete Member", use_container_width=True)

                    if update_btn:
                        update_member(member_id, {
                            "full_name": e_name, "phone": e_phone, "email": e_email,
                            "address": e_address, "gender": e_gender,
                            "membership_type": e_type, "monthly_fee": e_fee,
                            "time_slot": e_slot, "status": e_status,
                        })
                        st.success("✅ Member updated.")
                        st.rerun()

                    if delete_btn:
                        delete_member(member_id)
                        st.warning("🗑️ Member deleted.")
                        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from datetime import date
import base64
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import add_member, get_all_members, update_member, delete_member, get_member

st.set_page_config(page_title="Members | Gym Admin", page_icon="assets/logo.png", layout="wide")
inject_app_css()
require_login()

GYM_NAME = st.secrets.get("GYM_NAME", "IRON PULSE GYM")

# Fee presets
FEE_MAP = {
    "Standard": 2000.0,
    "Premium": 3000.0,
    "VIP": 5000.0,
}

# Helper to convert uploaded photo to base64
def encode_photo(file):
    if file is not None:
        b64 = base64.b64encode(file.getvalue()).decode()
        return f"data:{file.type};base64,{b64}"
    return None

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
    st.title("👥 Members Management")
    st.caption("Manage gym members, registrations, profiles, and memberships")

    tab1, tab2, tab3 = st.tabs(["➕ Add New Member", "📋 Member Directory", "✏️ Edit / Manage Member"])

    # ---------------- TAB 1: ADD NEW MEMBER ----------------
    with tab1:
        st.markdown("### 📝 Register New Member")

        c_type, c_fee = st.columns([1, 1])
        with c_type:
            selected_type = st.selectbox("Membership Type *", ["Standard", "Premium", "VIP"], key="add_mem_type")
        with c_fee:
            auto_fee = FEE_MAP.get(selected_type, 2000.0)
            monthly_fee = st.number_input("Monthly Fee (Rs.)", min_value=0.0, step=500.0, value=auto_fee, key="add_mem_fee")

        with st.form("add_member_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            full_name = c1.text_input("Full Name *", placeholder="e.g. Ali Ahmed")
            phone = c2.text_input("Phone Number *", placeholder="e.g. 0300-1234567")

            c3, c4 = st.columns(2)
            email = c3.text_input("Email Address", placeholder="e.g. ali@example.com")
            gender = c4.selectbox("Gender", ["Male", "Female", "Other"])

            c5, c6 = st.columns(2)
            time_slot = c5.selectbox("Preferred Workout Timing", ["Morning", "Evening", "Both"])
            join_date = c6.date_input("Registration / Join Date", value=date.today())

            address = st.text_area("Home / Office Address", height=70, placeholder="Address details...")

            uploaded_photo = st.file_uploader("📸 Upload Member Photo (Optional)", type=["png", "jpg", "jpeg"])

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✨ Register Member", use_container_width=True)

            if submitted:
                if not full_name.strip():
                    st.error("❌ Full Name is required.")
                elif not phone.strip():
                    st.error("❌ Phone Number is required.")
                else:
                    photo_b64 = encode_photo(uploaded_photo)
                    add_member({
                        "full_name": full_name.strip(),
                        "phone": phone.strip(),
                        "email": email.strip() if email else "",
                        "address": address.strip() if address else "",
                        "gender": gender,
                        "membership_type": selected_type,
                        "monthly_fee": monthly_fee,
                        "time_slot": time_slot,
                        "join_date": join_date,
                        "status": "Active",
                        "photo": photo_b64,
                    })
                    st.success(f"🎉 **{full_name}** successfully registered as **{selected_type}** member (Fee: Rs. {monthly_fee:,.0f})!")
                    st.rerun()

    # ---------------- TAB 2: MEMBER DIRECTORY ----------------
    with tab2:
        df = get_all_members()
        if df.empty:
            st.info("No members registered yet. Add your first member using the 'Add New Member' tab.")
        else:
            col_s, col_f1, col_f2 = st.columns([2, 1, 1])
            search = col_s.text_input("🔍 Search member by Name or Phone")
            type_filter = col_f1.selectbox("Filter Type", ["All", "Standard", "Premium", "VIP"])
            status_filter = col_f2.selectbox("Filter Status", ["All", "Active", "Inactive"])

            filtered_df = df
            if search:
                filtered_df = filtered_df[
                    filtered_df["full_name"].str.contains(search, case=False, na=False) |
                    filtered_df["phone"].astype(str).str.contains(search, case=False, na=False)
                ]
            if type_filter != "All":
                filtered_df = filtered_df[filtered_df["membership_type"] == type_filter]
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df["status"] == status_filter]

            st.caption(f"Showing **{len(filtered_df)}** members")

            # Grid card view of members with photos
            for idx, r in filtered_df.iterrows():
                with st.container():
                    col_p, col_info, col_fee_info = st.columns([1, 3, 2])
                    with col_p:
                        if r.get("photo") and str(r["photo"]).startswith("data:image"):
                            st.markdown(f'<img src="{r["photo"]}" class="member-avatar" style="width:75px; height:75px; border-radius:50%; object-fit:cover; border:2px solid #6366f1;">', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="width:75px; height:75px; border-radius:50%; background:#e2e8f0; display:flex; align-items:center; justify-content:center; font-size:1.8rem;">👤</div>', unsafe_allow_html=True)

                    with col_info:
                        status_badge = '<span class="status-active">🟢 Active</span>' if r["status"] == "Active" else '<span class="status-inactive">🔴 Inactive</span>'
                        st.markdown(f"### {r['full_name']} {status_badge}", unsafe_allow_html=True)
                        st.write(f"📞 **Phone:** {r['phone']} | ✉️ **Email:** {r['email'] or 'N/A'}")
                        st.caption(f"🗓️ Joined: {r['join_date']} | ⏰ Slot: **{r['time_slot']}**")

                    with col_fee_info:
                        type_color = "#6366f1" if r["membership_type"] == "VIP" else ("#ec4899" if r["membership_type"] == "Premium" else "#0ea5e9")
                        st.markdown(f"""
                        <div style="background:rgba(241,245,249,0.8); padding:10px 15px; border-radius:12px; border-left:4px solid {type_color};">
                            <div style="font-size:0.8rem; color:#64748b; font-weight:700;">MEMBERSHIP</div>
                            <div style="font-size:1.1rem; font-weight:800; color:#0f172a;">{r['membership_type']}</div>
                            <div style="font-size:0.95rem; font-weight:700; color:#10b981;">Rs. {float(r['monthly_fee']):,.0f} / mo</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.divider()

    # ---------------- TAB 3: EDIT / MANAGE MEMBER ----------------
    with tab3:
        all_m = get_all_members()
        if all_m.empty:
            st.info("No members available to edit.")
        else:
            member_id = st.selectbox(
                "Select Member to Edit",
                all_m["id"].tolist(),
                format_func=lambda x: f"{all_m[all_m['id'] == x]['full_name'].values[0]} ({all_m[all_m['id'] == x]['phone'].values[0]})"
            )
            m = get_member(member_id)

            if m:
                # Type and Fee selection with auto update
                edit_type = st.selectbox(
                    "Membership Type",
                    ["Standard", "Premium", "VIP"],
                    index=["Standard", "Premium", "VIP"].index(m.membership_type) if m.membership_type in ["Standard", "Premium", "VIP"] else 0,
                    key="edit_mem_type"
                )
                default_edit_fee = float(m.monthly_fee) if m.monthly_fee else FEE_MAP.get(edit_type, 2000.0)

                with st.form("edit_member_form"):
                    c1, c2 = st.columns(2)
                    e_name = c1.text_input("Full Name", value=m.full_name)
                    e_phone = c2.text_input("Phone Number", value=m.phone or "")

                    c3, c4 = st.columns(2)
                    e_email = c3.text_input("Email", value=m.email or "")
                    e_gender = c4.selectbox(
                        "Gender",
                        ["Male", "Female", "Other"],
                        index=["Male", "Female", "Other"].index(m.gender) if m.gender in ["Male", "Female", "Other"] else 0
                    )

                    c5, c6 = st.columns(2)
                    e_fee = c5.number_input("Monthly Fee (Rs.)", min_value=0.0, step=500.0, value=default_edit_fee)
                    e_slot = c6.selectbox(
                        "Timing Slot",
                        ["Morning", "Evening", "Both"],
                        index=["Morning", "Evening", "Both"].index(m.time_slot) if m.time_slot in ["Morning", "Evening", "Both"] else 0
                    )

                    c7, c8 = st.columns(2)
                    e_status = c7.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                        index=0 if m.status == "Active" else 1
                    )
                    edit_photo = c8.file_uploader("Update Photo (Optional)", type=["png", "jpg", "jpeg"])

                    e_address = st.text_area("Address", value=m.address or "")

                    b1, b2 = st.columns(2)
                    save_btn = b1.form_submit_button("💾 Save Member Changes", use_container_width=True)
                    del_btn = b2.form_submit_button("🗑️ Delete Member", use_container_width=True)

                    if save_btn:
                        new_photo = encode_photo(edit_photo) if edit_photo else m.photo
                        update_member(member_id, {
                            "full_name": e_name.strip(),
                            "phone": e_phone.strip(),
                            "email": e_email.strip(),
                            "address": e_address.strip(),
                            "gender": e_gender,
                            "membership_type": edit_type,
                            "monthly_fee": e_fee,
                            "time_slot": e_slot,
                            "status": e_status,
                            "photo": new_photo,
                        })
                        st.success("✅ Member details successfully updated!")
                        st.rerun()

                    if del_btn:
                        delete_member(member_id)
                        st.warning("🗑️ Member removed from system.")
                        st.rerun()

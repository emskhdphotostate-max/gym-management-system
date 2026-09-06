import streamlit as st
import base64
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import add_trainer, get_all_trainers, update_trainer, delete_trainer, get_trainer

st.set_page_config(page_title="Trainers | Gym Admin", page_icon="assets/logo.png", layout="wide")
inject_app_css()
require_login()

GYM_NAME = st.secrets.get("GYM_NAME", "IRON PULSE GYM")

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
    st.title("🏋️ Staff & Gym Trainers")
    st.caption("Manage certified fitness coaches, personal trainers, shifts, and salaries")

    tab1, tab2, tab3 = st.tabs(["➕ Add New Trainer", "📋 Trainer Directory", "✏️ Edit / Manage Trainer"])

    with tab1:
        st.markdown("### 📝 Register New Fitness Coach")
        with st.form("add_trainer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            full_name = col1.text_input("Coach Full Name *", placeholder="e.g. Captain Salman")
            phone = col2.text_input("Phone Number *", placeholder="e.g. 0312-3456789")

            col3, col4 = st.columns(2)
            specialization = col3.selectbox("Specialization", [
                "Bodybuilding & Hypertrophy",
                "Weight Loss & Cardio",
                "Strength & Conditioning",
                "CrossFit & HIIT",
                "Yoga & Flexibility",
                "Diet & Nutrition Coach",
                "General Fitness Coach"
            ])
            shift = col4.selectbox("Working Shift", ["Morning Shift", "Evening Shift", "Full Day"])

            col5, col6 = st.columns(2)
            salary = col5.number_input("Monthly Salary (Rs.)", min_value=0.0, step=1000.0, value=25000.0)
            uploaded_photo = col6.file_uploader("Trainer Photo (Optional)", type=["png", "jpg", "jpeg"])

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("✨ Register Trainer", use_container_width=True)

            if submitted:
                if not full_name.strip():
                    st.error("Coach Name is required.")
                elif not phone.strip():
                    st.error("Phone Number is required.")
                else:
                    photo_b64 = encode_photo(uploaded_photo)
                    add_trainer({
                        "full_name": full_name.strip(),
                        "phone": phone.strip(),
                        "specialization": specialization,
                        "salary": salary,
                        "shift": shift,
                        "status": "Active",
                        "photo": photo_b64,
                    })
                    st.success(f"🎉 Coach **{full_name}** successfully registered!")
                    st.rerun()

    with tab2:
        st.markdown("### 📋 Active Coaching Staff")
        trainers_df = get_all_trainers()

        if trainers_df.empty:
            st.info("No trainers added yet. Add your coaching staff in the 'Add New Trainer' tab.")
        else:
            for _, r in trainers_df.iterrows():
                with st.container():
                    col_p, col_info, col_extra = st.columns([1, 3, 2])
                    with col_p:
                        if r.get("photo") and str(r["photo"]).startswith("data:image"):
                            st.markdown(f'<img src="{r["photo"]}" style="width:75px; height:75px; border-radius:50%; object-fit:cover; border:2px solid #8b5cf6;">', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="width:75px; height:75px; border-radius:50%; background:#e2e8f0; display:flex; align-items:center; justify-content:center; font-size:1.8rem;">🏋️</div>', unsafe_allow_html=True)

                    with col_info:
                        status_badge = '<span class="status-active">🟢 Active</span>' if r["status"] == "Active" else '<span class="status-inactive">🔴 Inactive</span>'
                        st.markdown(f"### Coach {r['full_name']} {status_badge}", unsafe_allow_html=True)
                        st.write(f"🎯 **Specialty:** {r['specialization']} | 📞 **Phone:** {r['phone']}")
                        st.caption(f"⏰ Shift: **{r['shift']}**")

                    with col_extra:
                        st.markdown(f"""
                        <div style="background:rgba(241,245,249,0.8); padding:10px 15px; border-radius:12px; border-left:4px solid #8b5cf6;">
                            <div style="font-size:0.8rem; color:#64748b; font-weight:700;">SALARY PACKAGE</div>
                            <div style="font-size:1.1rem; font-weight:800; color:#0f172a;">Rs. {float(r['salary']):,.0f} / mo</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.divider()

    with tab3:
        all_t = get_all_trainers()
        if all_t.empty:
            st.info("No trainers to edit.")
        else:
            t_id = st.selectbox(
                "Select Trainer to Edit",
                all_t["id"].tolist(),
                format_func=lambda x: f"{all_t[all_t['id']==x]['full_name'].values[0]} ({all_t[all_t['id']==x]['specialization'].values[0]})"
            )
            t = get_trainer(t_id)

            if t:
                with st.form("edit_trainer_form"):
                    col1, col2 = st.columns(2)
                    e_name = col1.text_input("Full Name", value=t.full_name)
                    e_phone = col2.text_input("Phone Number", value=t.phone or "")

                    col3, col4 = st.columns(2)
                    specs = [
                        "Bodybuilding & Hypertrophy", "Weight Loss & Cardio",
                        "Strength & Conditioning", "CrossFit & HIIT",
                        "Yoga & Flexibility", "Diet & Nutrition Coach", "General Fitness Coach"
                    ]
                    e_spec = col3.selectbox("Specialization", specs, index=specs.index(t.specialization) if t.specialization in specs else 0)
                    shifts = ["Morning Shift", "Evening Shift", "Full Day"]
                    e_shift = col4.selectbox("Working Shift", shifts, index=shifts.index(t.shift) if t.shift in shifts else 0)

                    col5, col6 = st.columns(2)
                    e_salary = col5.number_input("Monthly Salary", min_value=0.0, step=1000.0, value=float(t.salary))
                    e_status = col6.selectbox("Status", ["Active", "Inactive"], index=0 if t.status == "Active" else 1)

                    e_photo = st.file_uploader("Update Photo (Optional)", type=["png", "jpg", "jpeg"])

                    b1, b2 = st.columns(2)
                    save_btn = b1.form_submit_button("💾 Save Coach Details", use_container_width=True)
                    del_btn = b2.form_submit_button("🗑️ Remove Coach", use_container_width=True)

                    if save_btn:
                        new_photo = encode_photo(e_photo) if e_photo else t.photo
                        update_trainer(t_id, {
                            "full_name": e_name.strip(),
                            "phone": e_phone.strip(),
                            "specialization": e_spec,
                            "salary": e_salary,
                            "shift": e_shift,
                            "status": e_status,
                            "photo": new_photo,
                        })
                        st.success("✅ Coach profile updated!")
                        st.rerun()

                    if del_btn:
                        delete_trainer(t_id)
                        st.warning("🗑️ Coach removed.")
                        st.rerun()

import streamlit as st
from datetime import date
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import add_expense, get_all_expenses, delete_expense, get_dashboard_stats

st.set_page_config(page_title="Expenses | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
    st.title("💰 Expenses & Financial Health")
    st.caption("Track gym operating costs, bills, equipment maintenance, and net profitability")

    stats = get_dashboard_stats()

    # Financial Summary Tiles
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Fee Collections", f"Rs. {stats['total_income']:,.0f}")
    with c2:
        st.metric("Total Expenses Logged", f"Rs. {stats['total_expenses']:,.0f}")
    with c3:
        st.metric("Net Gym Profit", f"Rs. {stats['net_profit']:,.0f}", delta="Healthy" if stats['net_profit'] >= 0 else "Loss")

    st.divider()

    tab1, tab2 = st.tabs(["➕ Add New Expense", "📜 Expense History & Management"])

    with tab1:
        st.markdown("### 💸 Log New Expense")
        with st.form("expense_form", clear_on_submit=True):
            col_t, col_c = st.columns(2)
            title = col_t.text_input("Expense Title *", placeholder="e.g. Electricity Bill, Dumbbells Repair")
            category = col_c.selectbox("Expense Category", [
                "Utilities (Electricity/Water/Gas)",
                "Rent",
                "Equipment Maintenance",
                "Staff / Trainer Salaries",
                "Supplements & Stock",
                "Cleaning & Hygiene",
                "Marketing & Ads",
                "Miscellaneous"
            ])

            col_a, col_d = st.columns(2)
            amount = col_a.number_input("Amount (Rs.) *", min_value=0.0, step=500.0)
            expense_date = col_d.date_input("Expense Date", value=date.today())

            notes = st.text_area("Additional Notes (Optional)", height=60)

            submitted = st.form_submit_button("💳 Log Expense", use_container_width=True)
            if submitted:
                if not title.strip():
                    st.error("Expense Title is required.")
                elif amount <= 0:
                    st.error("Expense Amount must be greater than 0.")
                else:
                    add_expense({
                        "title": title.strip(),
                        "category": category,
                        "amount": amount,
                        "expense_date": expense_date,
                        "notes": notes.strip() if notes else "",
                    })
                    st.success(f"✅ Expense of **Rs. {amount:,.0f}** for **{title}** logged successfully!")
                    st.rerun()

    with tab2:
        st.markdown("### 📜 Expense Records")
        exp_df = get_all_expenses()

        if exp_df.empty:
            st.info("No expenses logged yet.")
        else:
            st.dataframe(
                exp_df[["id", "title", "category", "amount", "expense_date", "notes"]],
                use_container_width=True,
                hide_index=True
            )

            st.divider()
            st.markdown("### 🗑️ Delete Expense Entry")
            del_id = st.selectbox(
                "Select Expense to Delete",
                exp_df["id"].tolist(),
                format_func=lambda x: f"ID {x}: {exp_df[exp_df['id']==x]['title'].values[0]} (Rs. {float(exp_df[exp_df['id']==x]['amount'].values[0]):,.0f})"
            )
            if st.button("🗑️ Delete Selected Expense", use_container_width=True):
                delete_expense(del_id)
                st.warning("Expense deleted.")
                st.rerun()

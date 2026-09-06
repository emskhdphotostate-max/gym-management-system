import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_app_css
from utils.db import get_dashboard_stats, get_all_members

st.set_page_config(page_title="Dashboard | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.title("📊 Dashboard Overview")
    st.caption(f"Real-time analytics and insights for **{GYM_NAME}**")

    stats = get_dashboard_stats()

    # Premium KPI Cards Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Total Members",
            value=stats["total_members"],
            delta=f"{stats['active_members']} Active"
        )

    with col2:
        st.metric(
            label="💰 This Month Income",
            value=f"Rs. {stats['this_month_income']:,.0f}",
            delta=f"Total: Rs. {stats['total_income']:,.0f}"
        )

    with col3:
        st.metric(
            label="📋 Today's Attendance",
            value=stats["today_attendance"],
            delta=f"{stats['active_members']} Total Active"
        )

    with col4:
        net_color = "normal" if stats['net_profit'] >= 0 else "inverse"
        st.metric(
            label="💵 Net Profit",
            value=f"Rs. {stats['net_profit']:,.0f}",
            delta=f"Expenses: Rs. {stats['total_expenses']:,.0f}",
            delta_color=net_color
        )

    st.divider()

    # Row 2: More Stats
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="🏋️ Active Trainers",
            value=stats["active_trainers"],
            delta="Staff Members"
        )

    with col6:
        st.metric(
            label="💸 Monthly Expenses",
            value=f"Rs. {stats['this_month_expenses']:,.0f}",
            delta=f"Total: Rs. {stats['total_expenses']:,.0f}"
        )

    with col7:
        active_rate = (stats['active_members'] / stats['total_members'] * 100) if stats['total_members'] > 0 else 0
        st.metric(
            label="📈 Active Rate",
            value=f"{active_rate:.1f}%",
            delta="Retention"
        )

    with col8:
        avg_income = (stats['total_income'] / stats['total_members']) if stats['total_members'] > 0 else 0
        st.metric(
            label="💎 Avg Revenue/Member",
            value=f"Rs. {avg_income:,.0f}",
            delta="Lifetime Value"
        )

    st.divider()

    # Recent Members Section
    st.markdown("### 🆕 Recently Registered Members")
    df = get_all_members()

    if df.empty:
        st.info("🚀 No members yet — Add your first member from the **Members** tab to get started!")
    else:
        # Show top 8 recent members in card format
        recent = df.head(8)

        cols = st.columns(4)
        for idx, (_, r) in enumerate(recent.iterrows()):
            with cols[idx % 4]:
                type_emoji = "👑" if r["membership_type"] == "VIP" else ("💎" if r["membership_type"] == "Premium" else "⭐")
                status_dot = "🟢" if r["status"] == "Active" else "🔴"

                st.markdown(f"""
                <div style="background:#ffffff; border-radius:14px; padding:12px; border:1px solid #e2e8f0; margin-bottom:10px;">
                    <div style="font-size:1.1rem; font-weight:700; color:#0f172a;">{type_emoji} {r['full_name'][:18]}</div>
                    <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">📞 {r['phone']}</div>
                    <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">{r['membership_type']} | Rs. {float(r['monthly_fee']):,.0f}</div>
                    <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">{status_dot} {r['status']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"<div style='text-align:center; margin-top:1rem;'><a href='/Members' style='color:#6366f1; font-weight:600;'>View All {len(df)} Members →</a></div>", unsafe_allow_html=True)

    st.divider()

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("➕ Add New Member", use_container_width=True):
            st.switch_page("pages/2_Members.py")

    with q2:
        if st.button("💳 Collect Fee Payment", use_container_width=True):
            st.switch_page("pages/3_Fee_Chalan.py")

    with q3:
        if st.button("📋 Mark Attendance", use_container_width=True):
            st.switch_page("pages/6_Attendance.py")

    with q4:
        if st.button("💰 Add Expense Entry", use_container_width=True):
            st.switch_page("pages/7_Expenses.py")

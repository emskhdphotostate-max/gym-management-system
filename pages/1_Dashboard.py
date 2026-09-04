import streamlit as st
from utils.auth import require_login, logout
from utils.styles import inject_global_css
from utils.db import get_dashboard_stats, get_all_members, get_setting

st.set_page_config(page_title="Dashboard | Gym Admin", page_icon="assets/logo.png", layout="wide")
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
st.title("📊 Dashboard")
st.caption("Quick overview of your gym's performance")

stats = get_dashboard_stats()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Members", stats["total_members"])
c2.metric("Active Members", stats["active_members"])
c3.metric("This Month Income", f"Rs. {stats['this_month_income']:,.0f}")
c4.metric("Total Income (All Time)", f"Rs. {stats['total_income']:,.0f}")

st.divider()
st.subheader("Recent Members")
df = get_all_members()
if df.empty:
    st.info("No members yet — add your first member from the **Members** page.")
else:
    st.dataframe(
        df[["id", "full_name", "phone", "membership_type", "time_slot", "status", "join_date"]].head(10),
        use_container_width=True, hide_index=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

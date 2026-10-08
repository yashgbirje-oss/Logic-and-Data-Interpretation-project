import streamlit as st
st.set_page_config(page_title="Logic & Data Interpretation", layout="wide", initial_sidebar_state="expanded")

from utils import auth
from utils.scoring import init_session_state, load_user_progress
from utils.styles import inject_css
from modules import (
    home, clock, calendar_module, patterns, tabular_di,
    bar_graph, pie_chart, line_graph, scatter, summary, admin
)

inject_css()


@st.cache_resource
def _setup():
    auth.init_db()
    return True


_setup()

# ---------------- LOGIN GATE ----------------
if "user" not in st.session_state:
    st.markdown('<h1 class="gradient-header">🧠 Logic & Data Interpretation</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Please log in. Accounts are created by your administrator.</p>', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Log in", width="stretch"):
                found = auth.verify(u, p)
                if found:
                    st.session_state.user = found
                    st.rerun()
                else:
                    st.error("Wrong username or password.")
    st.stop()

user = st.session_state.user
init_session_state()
load_user_progress(user["username"])

PAGES = {
    "🏠 Home": home.render,
    "⏱️ Clock": clock.render,
    "📅 Calendar": calendar_module.render,
    "🧩 Patterns": patterns.render,
    "📊 Tabular": tabular_di.render,
    "📶 Bar Graph": bar_graph.render,
    "🥧 Pie Chart": pie_chart.render,
    "📈 Line Graph": line_graph.render,
    "📉 Scatter": scatter.render,
    "🏆 Summary": summary.render,
}
if user["role"] == "admin":
    PAGES["🛠️ Admin"] = admin.render

st.sidebar.markdown("### 🧠 Logic & DI")
st.sidebar.markdown(f"👤 **{user['full_name'] or user['username']}** · `{user['role']}`")
selection = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
attempted = sum(s['attempted'] for s in st.session_state.scores.values())
correct = sum(s['correct'] for s in st.session_state.scores.values())
acc = (correct / attempted * 100) if attempted > 0 else 0
st.sidebar.markdown(f"""
<div class="custom-card" style="padding:15px; text-align:center;">
    <strong>Your Progress</strong><br/>
    Attempted: {attempted}<br/>
    Accuracy: {acc:.1f}%
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("🔑 Account"):
    with st.form("chpw", clear_on_submit=True):
        old = st.text_input("Current password", type="password")
        new = st.text_input("New password", type="password")
        if st.form_submit_button("Change password"):
            if auth.verify(user["username"], old):
                ok, msg = auth.set_password(user["username"], new)
                (st.success if ok else st.error)(msg)
            else:
                st.error("Current password is wrong.")

if st.sidebar.button("🚪 Log out", width="stretch"):
    st.session_state.clear()
    st.rerun()

PAGES[selection]()

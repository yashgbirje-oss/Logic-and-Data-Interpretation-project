import streamlit as st
st.set_page_config(page_title="Logic & Data Interpretation", layout="wide", initial_sidebar_state="expanded")

from utils.scoring import init_session_state
from utils.styles import inject_css
from modules import (
    home, clock, calendar_module, patterns, tabular_di,
    bar_graph, pie_chart, line_graph, scatter, summary
)

inject_css()
init_session_state()

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
    "🏆 Summary": summary.render
}

st.sidebar.markdown("### 🧠 Logic & DI")
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

PAGES[selection]()

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.scoring import get_summary_df, get_mistakes
from utils.errors import safe_run
from utils.charts import COLORWAY

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">🏆 Result Summary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Track your weakest modules, view performance charts, and download CSVs.</p>', unsafe_allow_html=True)
    
    df = get_summary_df()
    total_attempted = df['Attempted'].sum()
    total_correct = df['Correct'].sum()
    overall_accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Total Questions Attempted", total_attempted)
    with col2:
        with st.container(border=True):
            st.metric("Total Correct Answers", total_correct)
    with col3:
        with st.container(border=True):
            st.metric("Overall Accuracy", f"{overall_accuracy:.1f}%")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        with st.container(border=True):
            st.markdown("### Accuracy by Module")
            if total_attempted > 0:
                fig = px.bar(df, x='Module', y='Accuracy', text_auto='.1f', color_discrete_sequence=[COLORWAY[0]])
                fig.update_layout(height=300, margin=dict(l=20,r=20,t=30,b=20), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, width="stretch", key="summary_bar_chart")
            else:
                st.info("No data yet. Go practice some modules!")
                
    with c2:
        with st.container(border=True):
            st.markdown("### Overall Status")
            if total_attempted > 0:
                pie_data = pd.DataFrame({'Status': ['Correct', 'Wrong'], 'Count': [total_correct, total_attempted - total_correct]})
                fig2 = px.pie(pie_data, values='Count', names='Status', hole=0.5, color='Status', color_discrete_map={'Correct': COLORWAY[2], 'Wrong': COLORWAY[4]})
                fig2.update_traces(textinfo='percent+label', showlegend=False)
                fig2.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True, width="stretch", key="summary_pie_chart")
            else:
                st.info("No data yet.")
                
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mistake Analyzer Feature
    with st.container(border=True):
        st.markdown("### 🧠 Mistake Analyzer")
        mistakes = get_mistakes()
        
        if not mistakes:
            st.success("You haven't made any mistakes yet! Keep up the great work.")
        else:
            # Group mistakes by module to find the weakest
            weak_counts = {}
            for m in mistakes:
                weak_counts[m["module"]] = weak_counts.get(m["module"], 0) + 1
                
            weakest_module = max(weak_counts, key=weak_counts.get)
            st.warning(f"**Your Weakest Topic:** {weakest_module} ({weak_counts[weakest_module]} mistakes)")
            st.write(f"Recommendation: Go back to the **{weakest_module}** module and review the Concept tab. Then try some Easy questions.")
            
            st.markdown("#### Recent Errors:")
            for m in reversed(mistakes[-5:]): # Show last 5
                st.write(f"- <span class='badge-{m['difficulty'].lower()}'>{m['difficulty']}</span> **{m['module']}**: {m['reason']}", unsafe_allow_html=True)
                
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Report (CSV)", data=csv, file_name="logic_app_report.csv", mime="text/csv", key="summary_dl_btn")

import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
from scipy.stats import pearsonr, linregress
from utils.scoring import record_attempt
from utils.errors import safe_run

def generate_scatter_data(correlation_type="Positive"):
    x = np.random.rand(50) * 100
    if correlation_type == "Positive":
        y = 2 * x + np.random.randn(50) * 20
    elif correlation_type == "Negative":
        y = -2 * x + np.random.randn(50) * 20 + 200
    else:
        y = np.random.rand(50) * 100
    return pd.DataFrame({'X': x, 'Y': y})

def interpret_r(r):
    strength = "Strong" if abs(r) > 0.7 else ("Moderate" if abs(r) > 0.3 else "Weak")
    direction = "Positive" if r > 0 else "Negative"
    if abs(r) < 0.1: return "No meaningful correlation"
    return f"{strength} {direction} correlation"

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">📉 Scatter Diagram</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understand correlation and regression.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1: 
        with st.container(border=True):
            st.markdown("### 📉 Scatter Diagrams & Correlation")
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("A scatter plot places individual data points on a 2D grid based on two variables. It helps us figure out if the two variables are connected (correlated). For example, studying hours vs test scores.")
            with st.expander("2. Correlation Coefficient (r)"):
                st.write("The Pearson correlation coefficient 'r' measures how closely the points form a straight line. It ranges from **-1 to +1**.")
                st.markdown("- **Positive (r > 0):** As X goes up, Y goes up (e.g., studying hours vs. test scores).")
                st.markdown("- **Negative (r < 0):** As X goes up, Y goes down (e.g., car weight vs. fuel efficiency).")
                st.markdown("- **No Correlation (r = 0):** The points look like a random cloud.")
                st.markdown("- **Strength Scale:** $|r| > 0.7$ is Strong. $0.3 - 0.7$ is Moderate. $< 0.3$ is Weak.")
            with st.expander("3. Linear Regression (Line of Best Fit)"):
                st.write("Regression tries to draw the perfect line through the points to predict future values. The equation is:")
                st.latex(r"Y = mX + c")
                st.write("Where **m** is the slope and **c** is the y-intercept.")
            with st.expander("4. Common Traps"):
                st.info("💡 **Pro Tip:** Remember that **correlation does not equal causation!** Just because ice cream sales and shark attacks both increase in summer (strong positive correlation), it doesn't mean eating ice cream attracts sharks. They are both caused by heat.")
            
    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Data Generator")
                c_type = st.selectbox("Generate data with correlation:", ["Positive", "Negative", "Random"], key="scat_calc_type")
                
                df = generate_scatter_data(c_type)
                
                # Math
                r, p = pearsonr(df['X'], df['Y'])
                slope, intercept, r_value, p_value, std_err = linregress(df['X'], df['Y'])
                
                st.markdown("### Statistical Analysis")
                st.write(f"**Pearson r:** {r:.3f}")
                st.success(f"**Interpretation:** {interpret_r(r)}")
                
                st.markdown("### Regression Equation")
                st.latex(f"Y = {slope:.2f}X + {intercept:.2f}")
                
            with col2:
                st.markdown("### Visualization")
                # Using px.scatter for automatic trendline
                fig = px.scatter(df, x='X', y='Y', trendline="ols", trendline_color_override="red")
                fig.update_layout(height=400, margin=dict(l=20,r=20,t=30,b=20))
                st.plotly_chart(fig, use_container_width=True, width="stretch", key="scat_calc_chart")

    with tab3:
        if "scat_df" not in st.session_state: st.session_state.scat_df = generate_scatter_data("Positive")
        if "scat_q" not in st.session_state: st.session_state.scat_q = None
        if "scat_streak" not in st.session_state: st.session_state.scat_streak = 0
        if "scat_total" not in st.session_state: st.session_state.scat_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="scat_prac_diff")
                st.metric("Streak", f"🔥 {st.session_state.scat_streak}")
                st.write(f"Question {st.session_state.scat_total + 1} of 10")
                
                if st.button("Generate Question", key="scat_prac_gen"):
                    ctype = random.choice(["Positive", "Negative", "Random"])
                    df = generate_scatter_data(ctype)
                    st.session_state.scat_df = df
                    
                    r, _ = pearsonr(df['X'], df['Y'])
                    slope, inter, _, _, _ = linregress(df['X'], df['Y'])
                    
                    if diff == "Easy":
                        ans = "Positive" if r > 0.3 else ("Negative" if r < -0.3 else "None")
                        q_text = "What is the direction of correlation?"
                        opts = ["Positive", "Negative", "None"]
                    elif diff == "Medium":
                        ans = "Strong" if abs(r) > 0.7 else ("Moderate" if abs(r) > 0.3 else "Weak")
                        q_text = "What is the strength of the correlation?"
                        opts = ["Strong", "Moderate", "Weak"]
                    else:
                        x_val = 50
                        ans = round(slope * x_val + inter, 1)
                        q_text = f"Using linear regression, predict Y when X = {x_val}."
                        opts_set = set([ans])
                        while len(opts_set) < 4:
                            offset = ans * random.uniform(0.1, 0.3) * random.choice([-1, 1])
                            if offset == 0: offset = random.choice([-5, 5])
                            opts_set.add(round(ans + offset, 1))
                        opts = list(opts_set)
                        
                    random.shuffle(opts)
                    
                    st.session_state.scat_q = {"text": q_text, "correct": ans, "options": opts, "answered": False, "diff": diff}
        with col2:
            with st.container(border=True):
                fig = px.scatter(st.session_state.scat_df, x='X', y='Y')
                st.plotly_chart(fig, use_container_width=True, width="stretch", key="scat_prac_chart")
                
                if st.session_state.scat_q:
                    q = st.session_state.scat_q
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    ans = st.radio("Options:", q["options"], index=None, horizontal=True, key="scat_prac_radio")
                    
                    if st.button("Submit Answer", key="scat_prac_submit") and not q["answered"] and ans is not None:
                        st.session_state.scat_q["answered"] = True
                        st.session_state.scat_total += 1
                        is_correct = (str(ans) == str(q["correct"]))
                        if is_correct:
                            st.session_state.scat_streak += 1
                            record_attempt("Scatter Diagram Analysis", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.scat_streak = 0
                            record_attempt("Scatter Diagram Analysis", False, q["diff"], f"Failed scatter interpretation")
                            st.error(f"❌ Wrong! Answer is {q['correct']}.")

import streamlit as st
import pandas as pd
import random
from utils.charts import create_line_chart
from utils.scoring import record_attempt
from utils.errors import safe_run

def generate_line_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    val_a = [random.randint(100, 200)]
    val_b = [random.randint(50, 150)]
    for i in range(1, 8):
        val_a.append(val_a[-1] + random.randint(-20, 40))
        val_b.append(val_b[-1] + random.randint(-15, 30))
    return pd.DataFrame({'Month': months, 'Company A': val_a, 'Company B': val_b})

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">📈 Line Graph Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Detect trends and compute growth over time.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1: 
        with st.container(border=True):
            st.markdown("### 📈 Tracking Trends with Line Graphs")
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("Line graphs connect individual data points with straight lines. They are almost exclusively used to show how a variable changes **over time** (like stock prices, or company profits over months).")
            with st.expander("2. What to look for"):
                st.markdown("- **Steepness (Slope):** A steeper line means a faster rate of change (rapid growth or rapid decline).")
                st.markdown("- **Peaks and Valleys:** The highest and lowest points on the graph show the maximum and minimum values during that time period.")
                st.markdown("- **Highest Value vs. Highest Growth:** The highest point on the graph is NOT always where the most growth happened. Growth is about the *change* from the previous point.")
            with st.expander("3. Moving Averages"):
                st.write("Sometimes data is so spiky it's hard to read. A moving average smooths out the line by averaging the last few data points.")
                st.latex(r"\\text{3-Point MA} = \\frac{X_{t} + X_{t-1} + X_{t-2}}{3}")
            with st.expander("4. Growth Formula"):
                st.latex(r"\\text{Growth \%} = \\left( \\frac{\\text{Final} - \\text{Initial}}{\\text{Initial}} \\right) \\times 100")
            with st.expander("5. Worked Example"):
                st.write("**Q: Stock was $100 in Jan, $120 in Feb, and $90 in Mar. What was the growth from Feb to Mar?**")
                st.write("Initial = $120, Final = $90")
                st.latex(r"\\frac{90 - 120}{120} \\times 100 = \\frac{-30}{120} \\times 100 = -25\\%")
                st.write("The stock dropped by 25%.")
            with st.expander("6. Common Mistakes"):
                st.info("💡 **Pro Tip:** Don't confuse percentage points with percentage change. If a margin goes from 10% to 15%, the absolute change is 5 percentage points, but the percentage growth is 50%!")
            
    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Data Settings")
                df = generate_line_data()
                
                show_ma = st.checkbox("Show 3-Period Moving Average", key="line_calc_ma")
                if show_ma:
                    df['A (MA)'] = df['Company A'].rolling(window=3).mean()
                    df['B (MA)'] = df['Company B'].rolling(window=3).mean()
                    
                st.markdown("### Trend Calculator")
                st.write("Calculate growth between any two points:")
                c_opts = ['Company A', 'Company B']
                comp = st.selectbox("Company", c_opts, key="line_calc_comp")
                m1 = st.selectbox("From", df['Month'].tolist(), key="line_calc_m1", index=0)
                m2 = st.selectbox("To", df['Month'].tolist(), key="line_calc_m2", index=2)
                
                if m1 != m2:
                    v1 = df.loc[df['Month'] == m1, comp].values[0]
                    v2 = df.loc[df['Month'] == m2, comp].values[0]
                    growth = ((v2 - v1) / v1) * 100
                    st.write(f"Value at {m1}: **{v1:.1f}**")
                    st.write(f"Value at {m2}: **{v2:.1f}**")
                    st.success(f"**Growth:** {growth:,.2f}%")
                
                # Auto detect highest growth period
                df['Growth'] = df[comp].pct_change() * 100
                max_g_idx = df['Growth'].idxmax()
                if pd.notna(max_g_idx):
                    st.info(f"**Highest Growth Period for {comp}:** {df.loc[max_g_idx-1, 'Month']} to {df.loc[max_g_idx, 'Month']} ({df.loc[max_g_idx, 'Growth']:.1f}%)")

            with col2:
                st.markdown("### Visualization")
                cols_to_plot = ['Company A', 'Company B']
                if show_ma: cols_to_plot += ['A (MA)', 'B (MA)']
                st.plotly_chart(create_line_chart(df, 'Month', cols_to_plot), use_container_width=True, width="stretch", key="line_calc_chart")

    with tab3:
        if "line_df" not in st.session_state: st.session_state.line_df = generate_line_data()
        if "line_q" not in st.session_state: st.session_state.line_q = None
        if "line_streak" not in st.session_state: st.session_state.line_streak = 0
        if "line_total" not in st.session_state: st.session_state.line_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="line_prac_diff")
                st.metric("Streak", f"🔥 {st.session_state.line_streak}")
                st.write(f"Question {st.session_state.line_total + 1} of 10")
                
                if st.button("Generate Question", key="line_prac_gen"):
                    df = st.session_state.line_df
                    c = random.choice(['Company A', 'Company B'])
                    
                    if diff == "Easy":
                        idx = random.randint(0, len(df)-1)
                        m = df.loc[idx, 'Month']
                        ans = float(df.loc[idx, c])
                        q_text = f"What is the value for {c} in {m}?"
                    elif diff == "Medium":
                        idx = random.randint(1, len(df)-1)
                        m1 = df.loc[idx-1, 'Month']
                        m2 = df.loc[idx, 'Month']
                        v1 = df.loc[idx-1, c]
                        v2 = df.loc[idx, c]
                        ans = round(((v2 - v1)/v1)*100, 2)
                        q_text = f"What is the percentage growth for {c} from {m1} to {m2}?"
                    else:
                        m1 = df.loc[0, 'Month']
                        m2 = df.loc[len(df)-1, 'Month']
                        v1 = df.loc[0, c]
                        v2 = df.loc[len(df)-1, c]
                        cagr = (((v2/v1)**(1/7)) - 1) * 100
                        ans = round(cagr, 2)
                        q_text = f"What is the average monthly compound growth rate (CAGR) for {c} from {m1} to {m2}?"
                        
                    opts_set = set([ans])
                    while len(opts_set) < 4:
                        if ans == 0: offset = random.choice([-2, 2])
                        else: offset = ans * random.uniform(0.1, 0.3) * random.choice([-1, 1])
                        opts_set.add(round(ans + offset, 2))
                        
                    opts = list(opts_set)
                    random.shuffle(opts)
                    
                    st.session_state.line_q = {"text": q_text, "correct": ans, "options": opts, "answered": False, "diff": diff}
        with col2:
            with st.container(border=True):
                st.plotly_chart(create_line_chart(st.session_state.line_df, 'Month', ['Company A', 'Company B']), use_container_width=True, width="stretch", key="line_prac_chart")
                if st.session_state.line_q:
                    q = st.session_state.line_q
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    ans = st.radio("Options:", q["options"], index=None, horizontal=True, key="line_prac_radio")
                    
                    if st.button("Submit Answer", key="line_prac_submit") and not q["answered"] and ans is not None:
                        st.session_state.line_q["answered"] = True
                        st.session_state.line_total += 1
                        is_correct = abs(ans - q["correct"]) < 0.01
                        if is_correct:
                            st.session_state.line_streak += 1
                            record_attempt("Line Graph Analysis", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.line_streak = 0
                            record_attempt("Line Graph Analysis", False, q["diff"], f"Failed line graph calc")
                            st.error(f"❌ Wrong! Answer is {q['correct']}.")

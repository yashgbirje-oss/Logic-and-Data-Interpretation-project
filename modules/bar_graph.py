import streamlit as st
import pandas as pd
import random
from utils.charts import create_bar_chart
from utils.scoring import record_attempt
from utils.errors import safe_run

def generate_bar_data():
    return pd.DataFrame({
        'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'], 
        'Product A': [random.randint(20, 80) for _ in range(4)], 
        'Product B': [random.randint(15, 60) for _ in range(4)]
    })

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">📶 Bar Graph Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze datasets and visualize grouped/stacked concepts.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1:
        with st.container(border=True):
            st.markdown("### 📶 Understanding Bar Graphs")
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("Bar graphs represent categorical data using rectangular bars. The height (or length) of the bar is directly proportional to the value it represents. They are excellent for comparing discrete groups.")
            with st.expander("2. Types of Bar Graphs"):
                st.markdown("- **Grouped (Side-by-Side):** Places bars from different categories next to each other. Great for comparing two different products in the same year.")
                st.markdown("- **Stacked:** Places bars on top of each other. Great for seeing the **total** combined value while still seeing how much each category contributed.")
            with st.expander("3. Key Calculations"):
                st.write("Calculations on bar charts are identical to tabular DI, just presented visually. You must read the Y-axis carefully to extract the numbers.")
                st.latex(r"\\text{Total} = \\text{Bar 1} + \\text{Bar 2} + \\dots")
            with st.expander("4. Worked Example"):
                st.write("**Q: In a stacked bar chart, the bottom segment is 40 and the top of the bar reaches 100. What is the value of the top segment?**")
                st.write("The top segment is the total height minus the bottom segment height.")
                st.write("Value = $100 - 40 = 60$")
            with st.expander("5. Common Mistakes & Traps"):
                st.info("💡 **Pro Tip:** Always check the Y-axis scale! Sometimes the axis doesn't start at zero, which can make a small 2% difference look like a massive 50% drop visually.")
            
    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Calculator Inputs")
                data_mode = st.radio("Choose data source:", ["Generate Random", "Upload CSV"], key="bar_calc_mode")
                if data_mode == "Upload CSV":
                    uploaded = st.file_uploader("Upload CSV", type=['csv'], key="bar_calc_upload")
                    if uploaded:
                        try: df = pd.read_csv(uploaded)
                        except: df = generate_bar_data()
                    else: df = generate_bar_data()
                else: df = generate_bar_data()
                
                barmode = st.radio("Bar Mode", ["group", "stack"], horizontal=True, key="bar_calc_barmode")
                
                # Auto Insights
                st.markdown("### Auto-Insights")
                y_cols = df.select_dtypes(include=['number']).columns.tolist()
                x_col = df.columns[0]
                if y_cols:
                    df['Total'] = df[y_cols].sum(axis=1)
                    max_idx = df['Total'].idxmax()
                    min_idx = df['Total'].idxmin()
                    st.write(f"- **Highest Total:** {df.loc[max_idx, x_col]} ({df.loc[max_idx, 'Total']})")
                    st.write(f"- **Lowest Total:** {df.loc[min_idx, x_col]} ({df.loc[min_idx, 'Total']})")
                
            with col2:
                st.markdown("### Visualization")
                if y_cols:
                    st.plotly_chart(create_bar_chart(df, x_col, y_cols, barmode), use_container_width=True, width="stretch", key="bar_calc_chart")
                    with st.expander("View Raw Data"): st.dataframe(df)

    with tab3:
        if "bar_df" not in st.session_state: st.session_state.bar_df = generate_bar_data()
        if "bar_q" not in st.session_state: st.session_state.bar_q = None
        if "bar_streak" not in st.session_state: st.session_state.bar_streak = 0
        if "bar_total" not in st.session_state: st.session_state.bar_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="bar_prac_diff")
                st.metric("Streak", f"🔥 {st.session_state.bar_streak}")
                st.write(f"Question {st.session_state.bar_total + 1} of 10")
                
                if st.button("Generate Question", key="bar_prac_gen"):
                    df = st.session_state.bar_df
                    idx = random.randint(0, len(df)-1)
                    q_col = df.columns[0]
                    cat = df.loc[idx, q_col]
                    
                    if diff == "Easy":
                        ans = df.loc[idx, 'Product A'] + df.loc[idx, 'Product B']
                        q_text = f"What is the total sum of products in {cat}?"
                    elif diff == "Medium":
                        ans = df.loc[idx, 'Product A'] - df.loc[idx, 'Product B']
                        ans = abs(ans)
                        q_text = f"What is the absolute difference between Product A and B in {cat}?"
                    else:
                        ans = round(df.loc[idx, 'Product A'] / df.loc[idx, 'Product B'], 2)
                        q_text = f"What is the ratio of Product A to Product B in {cat}?"
                        
                    opts_set = set([ans])
                    while len(opts_set) < 4:
                        offset = ans * random.uniform(0.1, 0.3) * random.choice([-1, 1])
                        if offset == 0: offset = random.choice([-1, 1])
                        opts_set.add(round(ans + offset, 2))
                        
                    opts = list(opts_set)
                    random.shuffle(opts)
                    
                    st.session_state.bar_q = {"text": q_text, "correct": ans, "options": opts, "answered": False, "diff": diff}
        with col2:
            with st.container(border=True):
                st.plotly_chart(create_bar_chart(st.session_state.bar_df, 'Quarter', ['Product A', 'Product B']), use_container_width=True, width="stretch", key="bar_prac_chart")
                if st.session_state.bar_q:
                    q = st.session_state.bar_q
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    ans = st.radio("Options:", q["options"], index=None, horizontal=True, key="bar_prac_radio")
                    
                    if st.button("Submit Answer", key="bar_prac_submit") and not q["answered"] and ans is not None:
                        st.session_state.bar_q["answered"] = True
                        st.session_state.bar_total += 1
                        is_correct = abs(ans - q["correct"]) < 0.01
                        if is_correct:
                            st.session_state.bar_streak += 1
                            record_attempt("Bar Graph Analysis", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.bar_streak = 0
                            record_attempt("Bar Graph Analysis", False, q["diff"], f"Failed bar interpretation")
                            st.error(f"❌ Wrong! Answer is {q['correct']}.")

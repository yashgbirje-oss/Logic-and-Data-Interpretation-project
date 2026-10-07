import streamlit as st
import pandas as pd
import numpy as np
import random
from utils.scoring import record_attempt
from utils.errors import safe_run

def generate_table_data():
    years = [2020, 2021, 2022, 2023, 2024]
    return pd.DataFrame({
        'Year': years,
        'North Sales': [random.randint(100,500) for _ in range(5)],
        'South Sales': [random.randint(100,500) for _ in range(5)],
        'East Sales': [random.randint(100,500) for _ in range(5)],
        'West Sales': [random.randint(100,500) for _ in range(5)]
    })

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">📊 Tabular DI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze complex data tables and extract insights.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1:
        with st.container(border=True):
            st.markdown("### 📊 Tabular Data Interpretation")
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("Tabular DI questions test your ability to quickly scan rows and columns to find the right data, and then perform basic math on it. It mimics real-world corporate financial reporting.")
            with st.expander("2. Key Calculations to Master"):
                st.markdown("- **Averages:** Add up all the values in a column or row, and divide by the count.")
                st.markdown("- **Percentage Change:** Used to find how much a value grew or shrank.")
                st.latex(r"\\text{Growth \\%} = \\left( \\frac{\\text{New} - \\text{Old}}{\\text{Old}} \\right) \\times 100")
                st.markdown("- **Ratios:** Comparing two columns (e.g., North Sales : South Sales).")
                st.markdown("- **Ranking:** Finding the highest or lowest performer in a specific year.")
            with st.expander("3. Worked Example"):
                st.write("**Q: If Sales went from 200 in 2020 to 250 in 2021, what is the growth percentage?**")
                st.write("New = 250, Old = 200.")
                st.latex(r"\\text{Growth} = \\frac{250 - 200}{200} \\times 100 = \\frac{50}{200} \\times 100 = 25\\%")
            with st.expander("4. Common Mistakes & Tricks"):
                st.info("💡 **Pro Tip:** Don't calculate everything perfectly! Round large numbers to the nearest hundred or thousand to estimate the answer much faster.")

    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Data Source")
                data_mode = st.radio("Choose data source:", ["Generate Random", "Upload CSV"], key="tab_calc_mode")
                if data_mode == "Upload CSV":
                    uploaded = st.file_uploader("Upload CSV", type=['csv'], key="tab_calc_upload")
                    if uploaded:
                        try:
                            df = pd.read_csv(uploaded)
                        except Exception as e:
                            st.error(f"Error reading CSV: {e}")
                            df = generate_table_data()
                    else:
                        df = generate_table_data()
                else:
                    df = generate_table_data()
                    
                st.markdown("### Analysis")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) > 0:
                    sel_col = st.selectbox("Select column to analyze:", numeric_cols, key="tab_calc_col")
                    
                    total = df[sel_col].sum()
                    avg = df[sel_col].mean()
                    mx = df[sel_col].max()
                    mn = df[sel_col].min()
                    
                    st.write(f"**Total Sum:** {total:,.2f}")
                    st.write(f"**Average:** {avg:,.2f}")
                    st.write(f"**Maximum:** {mx:,.2f}")
                    st.write(f"**Minimum:** {mn:,.2f}")
                    
                    if len(df) >= 2:
                        first_val = df[sel_col].iloc[0]
                        last_val = df[sel_col].iloc[-1]
                        if first_val != 0:
                            growth = ((last_val - first_val) / first_val) * 100
                            st.write(f"**Overall Growth:** {growth:,.2f}%")
            
            with col2:
                st.markdown("### Dataset View")
                st.dataframe(df.style.highlight_max(axis=0, color='rgba(42, 157, 143, 0.3)').highlight_min(axis=0, color='rgba(230, 57, 70, 0.3)'), use_container_width=True, width="stretch")

    with tab3:
        if "tab_df" not in st.session_state: st.session_state.tab_df = generate_table_data()
        if "tab_q" not in st.session_state: st.session_state.tab_q = None
        if "tab_streak" not in st.session_state: st.session_state.tab_streak = 0
        if "tab_total" not in st.session_state: st.session_state.tab_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="tab_prac_diff")
                
                st.metric("Streak", f"🔥 {st.session_state.tab_streak}")
                st.write(f"Question {st.session_state.tab_total + 1} of 10")
                
                if st.button("Generate Question", key="tab_prac_gen"):
                    df = st.session_state.tab_df
                    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if 'Year' in num_cols: num_cols.remove('Year')
                    
                    col_choice = random.choice(num_cols)
                    
                    if diff == "Easy":
                        # Simple Sum or Average
                        if random.choice([True, False]):
                            correct = round(df[col_choice].sum(), 2)
                            q_text = f"What is the total sum of {col_choice}?"
                        else:
                            correct = round(df[col_choice].mean(), 2)
                            q_text = f"What is the average of {col_choice}?"
                    elif diff == "Medium":
                        # Percentage growth between years
                        idx1 = 0
                        idx2 = random.randint(1, len(df)-1)
                        val1 = df[col_choice].iloc[idx1]
                        val2 = df[col_choice].iloc[idx2]
                        correct = round(((val2 - val1) / val1) * 100, 2) if val1 != 0 else 0
                        yr1 = df['Year'].iloc[idx1] if 'Year' in df.columns else f"Row {idx1}"
                        yr2 = df['Year'].iloc[idx2] if 'Year' in df.columns else f"Row {idx2}"
                        q_text = f"What is the percentage growth of {col_choice} from {yr1} to {yr2}?"
                    else:
                        # Ratios
                        c1, c2 = random.sample(num_cols, 2)
                        idx = random.randint(0, len(df)-1)
                        val1 = df[c1].iloc[idx]
                        val2 = df[c2].iloc[idx]
                        correct = round(val1 / val2, 2) if val2 != 0 else 0
                        yr = df['Year'].iloc[idx] if 'Year' in df.columns else f"Row {idx}"
                        q_text = f"In {yr}, what is the ratio of {c1} to {c2}?"
                        
                    opts_set = set([correct])
                    while len(opts_set) < 4:
                        offset = correct * random.uniform(0.05, 0.2) * random.choice([-1, 1])
                        if offset == 0: offset = random.choice([-1, 1])
                        opts_set.add(round(correct + offset, 2))
                        
                    opts = list(opts_set)
                    random.shuffle(opts)
                    
                    st.session_state.tab_q = {
                        "text": q_text, "correct": correct, "options": opts, 
                        "answered": False, "diff": diff
                    }
        with col2:
            with st.container(border=True):
                st.dataframe(st.session_state.tab_df, use_container_width=True, width="stretch")
                if st.session_state.tab_q:
                    q = st.session_state.tab_q
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    ans = st.radio("Options:", q["options"], index=None, horizontal=True, key="tab_prac_radio")
                    
                    if st.button("Submit Answer", key="tab_prac_submit") and not q["answered"] and ans is not None:
                        st.session_state.tab_q["answered"] = True
                        st.session_state.tab_total += 1
                        is_correct = abs(ans - q["correct"]) < 0.01
                        
                        if is_correct:
                            st.session_state.tab_streak += 1
                            record_attempt("Tabular Data Interpretation", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.tab_streak = 0
                            record_attempt("Tabular Data Interpretation", False, q["diff"], f"Failed {q['diff']} table calc")
                            st.error(f"❌ Wrong! Answer is {q['correct']}.")

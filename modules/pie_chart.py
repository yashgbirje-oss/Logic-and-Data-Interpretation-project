import streamlit as st
import pandas as pd
import random
from utils.charts import create_pie_chart
from utils.scoring import record_attempt
from utils.errors import safe_run

def generate_pie_data():
    return pd.DataFrame({'Category': ['Rent', 'Food', 'Transport', 'Utilities'], 'Value': [random.randint(20, 50), random.randint(15, 40), random.randint(10, 25), random.randint(5, 15)]})

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">🥧 Pie Chart Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Compute percentage share and slice degrees.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1: 
        with st.container(border=True):
            st.markdown("### 🥧 Slicing up Pie Charts")
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("A pie chart is a circle divided into slices. The entire circle represents 100% of the data (the total), and each slice represents a portion (percentage or fraction) of that total. It is the best chart for showing part-to-whole relationships.")
            with st.expander("2. The Math Behind the Slices"):
                st.write("Since a full circle is $360^\circ$ and also represents 100%, we can convert between raw values, percentages, and angles using simple ratios:")
                st.latex(r"\\text{Angle in Degrees} = \\left( \\frac{\\text{Slice Value}}{\\text{Total Value}} \\right) \\times 360^\circ")
                st.latex(r"\\text{Percentage} = \\left( \\frac{\\text{Slice Value}}{\\text{Total Value}} \\right) \\times 100\\%")
            with st.expander("3. Worked Example"):
                st.write("**Q: If total sales are $2000, and the 'Electronics' slice is $120^\circ$, what is the sales value of Electronics?**")
                st.write("First, find the fraction of the circle it takes up:")
                st.latex(r"\\text{Fraction} = \\frac{120}{360} = \\frac{1}{3}")
                st.write("Multiply the fraction by the total value:")
                st.latex(r"\\text{Value} = \\frac{1}{3} \\times 2000 = \$666.67")
            with st.expander("4. Common Mistakes & Tricks"):
                st.info("💡 **Pro Tip:** Memorize common fractions! $25\%$ is exactly $90^\circ$. $50\%$ is $180^\circ$. $33.3\%$ is $120^\circ$. $10\%$ is $36^\circ$. This saves a ton of calculation time.")
            
    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Data Builder")
                categories = st.text_input("Categories (comma separated)", value="Rent, Food, Transport", key="pie_calc_cats")
                values = st.text_input("Values (comma separated)", value="1000, 500, 300", key="pie_calc_vals")
                
                cat_list = [c.strip() for c in categories.split(",")]
                val_list = []
                for v in values.split(","):
                    try: val_list.append(float(v.strip()))
                    except: val_list.append(0)
                    
                if len(cat_list) != len(val_list):
                    st.warning("Number of categories must match number of values.")
                    df = generate_pie_data()
                else:
                    df = pd.DataFrame({'Category': cat_list, 'Value': val_list})
                    
                total = df['Value'].sum()
                st.write(f"**Total Sum:** {total}")
                
                df['Percentage'] = (df['Value'] / total) * 100
                df['Angle (Degrees)'] = (df['Value'] / total) * 360
                
                st.markdown("### Slice Breakdown")
                st.dataframe(df.style.format({"Percentage": "{:.1f}%", "Angle (Degrees)": "{:.1f}°"}), use_container_width=True, width="stretch")
                
            with col2:
                st.markdown("### Visualization")
                st.plotly_chart(create_pie_chart(df, 'Category', 'Value'), use_container_width=True, width="stretch", key="pie_calc_chart")
            
    with tab3:
        if "pie_df" not in st.session_state: st.session_state.pie_df = generate_pie_data()
        if "pie_q" not in st.session_state: st.session_state.pie_q = None
        if "pie_streak" not in st.session_state: st.session_state.pie_streak = 0
        if "pie_total" not in st.session_state: st.session_state.pie_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="pie_prac_diff")
                st.metric("Streak", f"🔥 {st.session_state.pie_streak}")
                st.write(f"Question {st.session_state.pie_total + 1} of 10")
                
                if st.button("Generate Question", key="pie_prac_gen"):
                    df = st.session_state.pie_df
                    total = df['Value'].sum()
                    idx = random.randint(0, len(df)-1)
                    cat = df.loc[idx, 'Category']
                    
                    if diff == "Easy":
                        ans = round((df.loc[idx, 'Value'] / total) * 100, 1)
                        q_text = f"What is the percentage share of {cat}?"
                    elif diff == "Medium":
                        ans = round((df.loc[idx, 'Value'] / total) * 360, 1)
                        q_text = f"What is the central angle (in degrees) for {cat}?"
                    else:
                        cat2 = df.loc[(idx+1)%len(df), 'Category']
                        val2 = df.loc[(idx+1)%len(df), 'Value']
                        ans = round(((df.loc[idx, 'Value'] - val2) / total) * 360, 1)
                        ans = abs(ans)
                        q_text = f"What is the difference in central angles between {cat} and {cat2}?"
                        
                    opts_set = set([ans])
                    while len(opts_set) < 4:
                        offset = ans * random.uniform(0.1, 0.3) * random.choice([-1, 1])
                        if offset == 0: offset = random.choice([-5, 5])
                        opts_set.add(round(ans + offset, 1))
                        
                    opts = list(opts_set)
                    random.shuffle(opts)
                    
                    st.session_state.pie_q = {"text": q_text, "correct": ans, "options": opts, "answered": False, "diff": diff}
        with col2:
            with st.container(border=True):
                st.plotly_chart(create_pie_chart(st.session_state.pie_df, 'Category', 'Value'), use_container_width=True, width="stretch", key="pie_prac_chart")
                if st.session_state.pie_q:
                    q = st.session_state.pie_q
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    ans = st.radio("Options:", q["options"], index=None, horizontal=True, key="pie_prac_radio")
                    
                    if st.button("Submit Answer", key="pie_prac_submit") and not q["answered"] and ans is not None:
                        st.session_state.pie_q["answered"] = True
                        st.session_state.pie_total += 1
                        is_correct = abs(ans - q["correct"]) < 0.1
                        if is_correct:
                            st.session_state.pie_streak += 1
                            record_attempt("Pie Chart Analysis", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.pie_streak = 0
                            record_attempt("Pie Chart Analysis", False, q["diff"], f"Failed pie math")
                            st.error(f"❌ Wrong! Answer is {q['correct']}.")

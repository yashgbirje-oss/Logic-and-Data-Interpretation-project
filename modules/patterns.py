import streamlit as st
import random
import plotly.graph_objects as go
from utils.scoring import record_attempt
from utils.errors import safe_run
from utils.charts import COLORWAY

def generate_series(stype, start, param, length=6):
    series = []
    if stype == "AP":
        series = [start + i*param for i in range(length)]
        rule = f"Add {param}"
    elif stype == "GP":
        series = [start * (param**i) for i in range(length)]
        rule = f"Multiply by {param}"
    elif stype == "Squares":
        series = [(start+i)**2 for i in range(length)]
        rule = "Square of consecutive numbers"
    elif stype == "Fibonacci":
        series = [start, param]
        for _ in range(length-2): series.append(series[-1] + series[-2])
        rule = "Sum of previous two terms"
    elif stype == "Alternating":
        series = [start + (param if i%2==0 else -param) for i in range(length)]
        rule = f"Alternate adding and subtracting {param}"
    return series, rule

def draw_shape_pattern(n_shapes):
    fig = go.Figure()
    for i in range(n_shapes):
        fig.add_shape(type="circle", xref="x", yref="y", x0=i*3, y0=0, x1=i*3+1+i*0.5, y1=1+i*0.5, fillcolor=COLORWAY[i%len(COLORWAY)], line_color="rgba(0,0,0,0)")
    fig.update_layout(xaxis=dict(visible=False, range=[-1, n_shapes*3+2]), yaxis=dict(visible=False, range=[-1, 5]), height=200, margin=dict(l=0,r=0,t=0,b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    return fig

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">🧩 Patterns & Figures</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Identify the underlying rule in number series and shapes.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1:
        with st.container(border=True):
            st.markdown("### 🧩 Breaking Down Patterns")
            
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("Pattern recognition is the foundation of logical reasoning. It trains your brain to find the hidden rule generating a sequence of numbers or shapes.")
            
            with st.expander("2. Common Number Series Rules"):
                st.markdown("- **Arithmetic Progression (AP):** Add/subtract a constant. $a_n = a + (n-1)d$")
                st.markdown("- **Geometric Progression (GP):** Multiply/divide by a constant. $a_n = a r^{n-1}$")
                st.markdown("- **Squares & Cubes:** Look out for numbers near $n^2$ or $n^3$.")
                st.markdown("- **Fibonacci Series:** Every number is the sum of the two before it.")
            
            with st.expander("3. Difference-of-Differences Method"):
                st.write("If you're stuck, always calculate the difference between consecutive numbers:")
                st.write("Series: 2, 5, 10, 17, 26")
                st.write("1st Diff: 3, 5, 7, 9 (This is an AP!)")
                st.write("2nd Diff: 2, 2, 2 (Constant)")
            
            with st.expander("4. Figure & Shape Patterns"):
                st.markdown("- **Rotation:** Shapes rotate by 45° or 90° clockwise/anticlockwise.")
                st.markdown("- **Addition/Deletion:** Lines or dots are added or removed sequentially.")
                st.markdown("- **Movement:** An element moves along the corners of a square.")
            
            with st.expander("5. Worked Example"):
                st.write("**Q: What comes next? 3, 6, 18, 72, ?**")
                st.write("- 3 × 2 = 6")
                st.write("- 6 × 3 = 18")
                st.write("- 18 × 4 = 72")
                st.write("Rule is multiplying by consecutive integers. Next is 72 × 5 = **360**.")
                
            with st.expander("6. Common Mistakes"):
                st.info("💡 **Pro Tip:** Don't assume a series is an AP just because the first two differences match. Always check at least 3 terms before locking in the rule.")

    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("### Series Generator")
                stype = st.selectbox("Pattern Type", ["AP", "GP", "Squares", "Fibonacci", "Alternating"], key="pattern_calc_type")
                start = st.number_input("Start Value", value=2, key="pattern_calc_start")
                param = st.number_input("Parameter (Difference/Ratio/2nd Start)", value=3, key="pattern_calc_param")
                
                series, rule = generate_series(stype, start, param, length=8)
                
                st.markdown("### Generated Series")
                st.write(f"**Rule:** {rule}")
                
                # Display terms in a nice row
                html = "<div style='display:flex; gap:10px; font-size:1.2rem;'>"
                for num in series[:5]:
                    html += f"<div style='background:rgba(128,128,128,0.1); padding:10px 15px; border-radius:8px;'>{num}</div>"
                html += f"<div style='padding:10px 15px; border-radius:8px; color:var(--text-color); opacity:0.5;'>...</div>"
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
                
                st.markdown("<br>### Next 3 Terms Predicted:", unsafe_allow_html=True)
                st.success(f"{series[5]}, {series[6]}, {series[7]}")
                
            with col2:
                st.markdown("### Visual Plot")
                fig = go.Figure(data=go.Scatter(y=series, mode='lines+markers', line=dict(color=COLORWAY[0], width=3), marker=dict(size=10)))
                fig.update_layout(height=250, margin=dict(l=20,r=20,t=30,b=20))
                st.plotly_chart(fig, use_container_width=True, width="stretch", key="pattern_calc_chart")
                
                st.markdown("### Shape Pattern Example")
                st.write("Growth Pattern:")
                st.plotly_chart(draw_shape_pattern(4), use_container_width=True, width="stretch", key="pattern_calc_shape")

    with tab3:
        if "pat_q" not in st.session_state: st.session_state.pat_q = None
        if "pat_streak" not in st.session_state: st.session_state.pat_streak = 0
        if "pat_total" not in st.session_state: st.session_state.pat_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="pattern_prac_diff")
                
                st.metric("Streak", f"🔥 {st.session_state.pat_streak}")
                st.write(f"Question {st.session_state.pat_total + 1} of 10")
                
                if st.button("Generate Question", key="pattern_prac_gen"):
                    stypes = ["AP", "GP", "Squares", "Fibonacci", "Alternating"]
                    if diff == "Easy":
                        stype = random.choice(["AP", "Squares"])
                    elif diff == "Medium":
                        stype = random.choice(["GP", "Alternating", "Fibonacci"])
                    else:
                        stype = random.choice(["GP", "Fibonacci", "Alternating"])
                        
                    start = random.randint(1, 10)
                    param = random.randint(2, 5)
                    series, _ = generate_series(stype, start, param, length=6)
                    
                    correct = series[5]
                    q_text = f"Find the next term in the series: {series[0]}, {series[1]}, {series[2]}, {series[3]}, {series[4]}, ?"
                    
                    opts_set = set([correct])
                    while len(opts_set) < 4:
                        if correct == 0: offset = random.randint(1, 5)
                        else: offset = int(correct * random.uniform(-0.5, 0.5))
                        if offset == 0: offset = random.choice([-2, 2])
                        opts_set.add(correct + offset)
                        
                    opts = list(opts_set)
                    random.shuffle(opts)
                    
                    st.session_state.pat_q = {
                        "series": series, "text": q_text, "correct": correct,
                        "options": opts, "answered": False, "diff": diff
                    }
        
        with col2:
            with st.container(border=True):
                if st.session_state.pat_q:
                    q = st.session_state.pat_q
                    
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    
                    ans = st.radio("Select Answer:", q["options"], index=None, key="pattern_prac_radio")
                    
                    if st.button("Submit Answer", key="pattern_prac_submit") and not q["answered"] and ans is not None:
                        q["answered"] = True
                        st.session_state.pat_total += 1
                        
                        is_correct = (ans == q["correct"])
                        
                        if is_correct:
                            st.session_state.pat_streak += 1
                            record_attempt("Patterns & Figures", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.pat_streak = 0
                            record_attempt("Patterns & Figures", False, q["diff"], f"Failed to predict pattern {q['series'][:3]}...")
                            st.error(f"❌ Wrong! The correct answer is {q['correct']}.")
                            
                        fig = go.Figure(data=go.Scatter(y=q["series"], mode='lines+markers', line=dict(color=COLORWAY[1], width=3)))
                        fig.update_layout(height=200, margin=dict(l=20,r=20,t=10,b=20))
                        st.plotly_chart(fig, use_container_width=True, width="stretch", key="pattern_prac_chart")

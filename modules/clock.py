import streamlit as st
import random
from utils.charts import draw_clock
from utils.scoring import record_attempt
from utils.errors import safe_run
import math

def calculate_angle(h, m):
    h = h % 12
    # The absolute angle formula
    angle = abs(30 * h - 5.5 * m)
    angle = min(angle, 360 - angle)
    reflex = 360 - angle
    return angle, reflex

def get_overlap_time(h):
    # Hands overlap at (60/11) * H minutes past H
    m = (60/11) * h
    return m

def get_perpendicular_times(h):
    # Perpendicular at (60/11)*(H - 3) and (60/11)*(H + 3)
    times = []
    t1 = (5 * h - 15) * 12/11
    t2 = (5 * h + 15) * 12/11
    if 0 <= t1 < 60: times.append(t1)
    if 0 <= t2 < 60: times.append(t2)
    # Wrap around cases
    if t1 < 0:
        t1_wrap = (5 * h + 45) * 12/11
        if 0 <= t1_wrap < 60: times.append(t1_wrap)
    if t2 >= 60:
        t2_wrap = (5 * h - 45) * 12/11
        if 0 <= t2_wrap < 60: times.append(t2_wrap)
    return sorted(times)

def format_time(m):
    minutes = int(m)
    seconds = int((m - minutes) * 60)
    return f"{minutes:02d}m {seconds:02d}s"

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">⏱️ Clock Problems</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Calculate angles between hands and solve time logic.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1:
        with st.container(border=True):
            st.markdown("### ⏱️ Understanding Clock Angles")
            st.write("A clock face is a complete circle of 360°. Questions usually involve calculating the angle between hands or finding when hands align.")
            
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("Clock logic is a fundamental part of quantitative aptitude. It tests your ability to track two moving objects (the hour and minute hands) traveling at different speeds around a circular track.")
            
            with st.expander("2. Key Terms & Speeds"):
                st.markdown("- **Minute Hand Speed:** Covers 360° in 60 minutes = **6° per minute**.")
                st.markdown("- **Hour Hand Speed:** Covers 360° in 12 hours (720 minutes) = **0.5° per minute**.")
                st.markdown("- **Relative Speed:** The minute hand gains $5.5^\\circ$ ($6 - 0.5$) over the hour hand every minute.")
            
            with st.expander("3. Master Formulas"):
                st.write("**The Angle Formula:**")
                st.latex(r"\\theta = |30H - 5.5M|")
                st.write("**Hands Overlap (0°):**")
                st.latex(r"M = \\frac{60}{11} \times H")
                st.write("Hands overlap exactly every $65 \\frac{5}{11}$ minutes.")
            
            with st.expander("4. Daily Frequencies & Mirror Images"):
                st.markdown("- **Overlap (0°):** 22 times a day (11 times in 12 hours).")
                st.markdown("- **Opposite (180°):** 22 times a day.")
                st.markdown("- **Perpendicular (90°):** 44 times a day (22 times in 12 hours).")
                st.markdown("- **Mirror Image Time:** $11:60 - \text{Given Time}$ (or $23:60$ for 24hr format).")
            
            with st.expander("5. Worked Examples"):
                st.markdown("**Example 1: Angle at 3:40**")
                st.write("$H = 3, M = 40$")
                st.latex(r"\\theta = |30(3) - 5.5(40)| = |90 - 220| = |-130| = 130^\circ")
                st.markdown("**Example 2: When do hands overlap between 4 and 5 o'clock?**")
                st.write("$H = 4$. Using the overlap formula:")
                st.latex(r"M = \\frac{60}{11} \times 4 = \\frac{240}{11} = 21 \\frac{9}{11} \text{ minutes}")
                st.write("So they overlap at exactly 4:21:49.")
            
            with st.expander("6. Common Mistakes & Tricks"):
                st.info("💡 **Pro Tip:** The angle formula can give a result $> 180^\circ$. This is the reflex angle. Subtract from $360^\circ$ to get the interior angle.")
    
    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("### Calculator Inputs")
                h = st.number_input("Hour (1-12)", min_value=1, max_value=12, value=3, key="clock_calc_h")
                m = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=40, key="clock_calc_m")
                
                angle, reflex = calculate_angle(h, m)
                overlap_m = get_overlap_time(h)
                perp_times = get_perpendicular_times(h)
                
                st.markdown("### Results & Working")
                st.write(f"**Step 1:** Plug $H={h}$ and $M={m}$ into formula $|30H - 5.5M|$")
                raw_angle = abs(30 * h - 5.5 * m)
                st.write(f"**Step 2:** $|30({h}) - 5.5({m})| = |{30*h} - {5.5*m}| = {raw_angle}^\circ$")
                
                if raw_angle > 180:
                    st.write(f"**Step 3:** Since {raw_angle}° > 180°, the interior angle is $360^\circ - {raw_angle}^\circ = {angle}^\circ$")
                
                st.success(f"**Interior Angle:** {angle}°")
                st.warning(f"**Reflex Angle:** {reflex}°")
                
                st.markdown("---")
                st.write(f"**Between {h}:00 and {(h%12)+1}:00:**")
                st.write(f"- Hands overlap at **{h}:{format_time(overlap_m)}**")
                perp_str = " and ".join([f"**{h}:{format_time(pt)}**" for pt in perp_times])
                st.write(f"- Hands are perpendicular at {perp_str}")
                
            with col2:
                fig = draw_clock(h, m)
                st.plotly_chart(fig, use_container_width=True, width="stretch", key="clock_calc_chart")

    with tab3:
        if "clock_q" not in st.session_state: st.session_state.clock_q = None
        if "clock_streak" not in st.session_state: st.session_state.clock_streak = 0
        if "clock_total" not in st.session_state: st.session_state.clock_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="clock_prac_diff")
                
                st.metric("Streak", f"🔥 {st.session_state.clock_streak}")
                st.write(f"Question {st.session_state.clock_total + 1} of 10")
                
                if st.button("Generate Question", key="clock_prac_gen"):
                    h = random.randint(1, 12)
                    if diff == "Easy":
                        m = random.choice([0, 15, 30, 45])
                    elif diff == "Medium":
                        m = random.randint(0, 59)
                    else: # Hard
                        m = random.randint(0, 59)
                    
                    ans, reflex = calculate_angle(h, m)
                    
                    # Hard might ask for reflex angle
                    ask_reflex = diff == "Hard" and random.choice([True, False])
                    correct = reflex if ask_reflex else ans
                    q_text = f"What is the {'reflex ' if ask_reflex else 'interior '}angle at {h:02d}:{m:02d}?"
                    
                    opts = set([correct])
                    while len(opts) < 4:
                        opts.add(correct + random.choice([-15, -10, -5, 5, 10, 15, 30, -30, 0.5, -0.5]))
                    
                    opts = list(opts)
                    random.shuffle(opts)
                    
                    st.session_state.clock_q = {
                        "h": h, "m": m, "text": q_text, "correct": correct,
                        "options": opts, "answered": False, "diff": diff
                    }
        
        with col2:
            with st.container(border=True):
                if st.session_state.clock_q:
                    q = st.session_state.clock_q
                    
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    
                    ans = st.radio("Select Answer:", q["options"], index=None, key="clock_prac_radio")
                    
                    if st.button("Submit Answer", key="clock_prac_submit") and not q["answered"] and ans is not None:
                        q["answered"] = True
                        st.session_state.clock_total += 1
                        
                        is_correct = abs(ans - q["correct"]) < 0.01
                        
                        if is_correct:
                            st.session_state.clock_streak += 1
                            record_attempt("Clock Problems", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.clock_streak = 0
                            record_attempt("Clock Problems", False, q["diff"], f"Failed angle at {q['h']}:{q['m']}")
                            st.error(f"❌ Wrong! The correct answer is {q['correct']}°.")
                            
                        # Show explanation
                        st.write("---")
                        st.write("**Explanation:**")
                        raw_a = abs(30 * q['h'] - 5.5 * q['m'])
                        st.write(f"Formula: $|30({q['h']}) - 5.5({q['m']})| = {raw_a}^\circ$")
                        st.write(f"Interior angle: $\min({raw_a}, 360-{raw_a}) = {min(raw_a, 360-raw_a)}^\circ$")
                        
                    if q["answered"]:
                        fig = draw_clock(q["h"], q["m"])
                        st.plotly_chart(fig, use_container_width=True, width="stretch", key="clock_prac_chart")

import streamlit as st
import datetime
import calendar
import random
from utils.scoring import record_attempt
from utils.errors import safe_run

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTH_CODES = [3, 0, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3] # Jan to Dec odd days

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_odd_days_steps(d, m, y):
    # Odd days for centuries (100 -> 5, 200 -> 3, 300 -> 1, 400 -> 0)
    century = (y - 1) // 100
    rem_century = century % 4
    c_odd = (5, 3, 1, 0)[rem_century]
    
    # Years in current century
    years = (y - 1) % 100
    leaps = years // 4
    ords = years - leaps
    y_odd = (leaps * 2 + ords) % 7
    
    # Months in current year
    m_odd = 0
    for i in range(m - 1):
        m_odd += MONTH_CODES[i]
        if i == 1 and is_leap_year(y): # Feb leap
            m_odd += 1
    m_odd = m_odd % 7
    
    # Days in current month
    d_odd = d % 7
    
    t_odd = (c_odd + y_odd + m_odd + d_odd) % 7
    return c_odd, y_odd, m_odd, d_odd, t_odd, leaps, ords

def generate_calendar_html(year, month, highlight_day=None):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    html = f"""
    <table style="width:100%; text-align:center; border-collapse: collapse; border: 1px solid rgba(128,128,128,0.2);">
        <tr style="background:rgba(128,128,128,0.1);">
            <th colspan="7" style="padding:10px; font-weight:bold;">{month_name} {year}</th>
        </tr>
        <tr style="background:rgba(128,128,128,0.05);">
            <th style="padding:8px;">Sun</th><th style="padding:8px;">Mon</th><th style="padding:8px;">Tue</th>
            <th style="padding:8px;">Wed</th><th style="padding:8px;">Thu</th><th style="padding:8px;">Fri</th>
            <th style="padding:8px;">Sat</th>
        </tr>
    """
    
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += '<td style="padding:8px; border: 1px solid rgba(128,128,128,0.1);"></td>'
            else:
                bg = "#FFC107" if day == highlight_day else "transparent"
                color = "#000" if day == highlight_day else "var(--text-color)"
                html += f'<td style="padding:8px; border: 1px solid rgba(128,128,128,0.1); background:{bg}; color:{color}; font-weight:{"bold" if day==highlight_day else "normal"};">{day}</td>'
        html += "</tr>"
    html += "</table>"
    return html

@safe_run
def render():
    st.markdown('<h1 class="gradient-header">📅 Calendar Problems</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Find days of the week, leap years, and odd days logic.</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 Concept", "🧮 Calculator", "🎯 Practice"])
    
    with tab1:
        with st.container(border=True):
            st.markdown("### 📅 The Magic of 'Odd Days'")
            
            with st.expander("1. What it is and why it matters", expanded=True):
                st.write("To find the day of the week for any date in history, we use the **Odd Days** method. An 'odd day' is simply the remainder when you divide the total number of days by 7 (a full week). This lets us compress centuries of time into a single number from 0 to 6.")
            
            with st.expander("2. Key Rules & Years"):
                st.markdown("- **Ordinary Year:** 365 days. (365 ÷ 7 = 52 weeks and **1 odd day**).")
                st.markdown("- **Leap Year:** 366 days. (366 ÷ 7 = 52 weeks and **2 odd days**).")
                st.markdown("- **Century Rule:** A year ending in 00 is ONLY a leap year if divisible by 400 (e.g., 2000 is leap, 1900 is not).")
            
            with st.expander("3. Century Odd Days"):
                st.markdown("- **100 years:** 5 odd days")
                st.markdown("- **200 years:** 3 odd days")
                st.markdown("- **300 years:** 1 odd day")
                st.markdown("- **400 years:** 0 odd days")
                
            with st.expander("4. The Day-Finding Method"):
                st.write("To find the day for DD/MM/YYYY:")
                st.write("1. Find odd days for the completed centuries.")
                st.write("2. Find odd days for the completed years in the current century.")
                st.write("3. Add odd days for the completed months of the current year.")
                st.write("4. Add the current day (DD).")
                st.write("5. Sum everything, divide by 7, and use the remainder:")
                st.info("💡 **Decoding:** 0 = Sunday, 1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday.")
                
            with st.expander("5. Worked Examples"):
                st.markdown("**Example: 15 Aug 1947**")
                st.write("Year 1946 is completed.")
                st.write("- 1600 years = 0 odd days. 300 years = 1 odd day.")
                st.write("- 46 years = 11 leaps (22) + 35 ordinary (35) = 57 days. 57 % 7 = **1 odd day**.")
                st.write("- Months (Jan to Jul): 3+0+3+2+3+2+3 = 16 days. 16 % 7 = **2 odd days**.")
                st.write("- Days: 15 % 7 = **1 odd day**.")
                st.write("Total = 1 + 1 + 2 + 1 = 5. **5 = Friday.**")

    with tab2:
        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("### Date Analyzer")
                date_input = st.date_input("Select a date:", datetime.date.today(), key="calendar_calc_date")
                compare_date = st.date_input("Compare to date:", datetime.date.today(), key="calendar_calc_compare")
                
                y, m, d = date_input.year, date_input.month, date_input.day
                c_odd, y_odd, m_odd, d_odd, t_odd, leaps, ords = get_odd_days_steps(d, m, y)
                day_name = DAYS[t_odd]
                
                st.success(f"**{date_input.strftime('%d %B %Y')} is a {day_name}.**")
                st.write(f"The year {y} is an **{'Leap' if is_leap_year(y) else 'Ordinary'} Year**.")
                
                diff_days = abs((date_input - compare_date).days)
                st.write(f"Days between dates: **{diff_days} days**")
                
                st.markdown("### Step-by-Step Calculation")
                st.write(f"**1. Centuries:** Up to {(y-1)//100 * 100} -> {c_odd} odd days.")
                st.write(f"**2. Years:** {y-1} has {leaps} leaps and {ords} ordinary -> {y_odd} odd days.")
                st.write(f"**3. Months:** Jan to month {m-1} -> {m_odd} odd days.")
                st.write(f"**4. Days:** {d} days -> {d_odd} odd days.")
                st.write(f"**Total = {c_odd} + {y_odd} + {m_odd} + {d_odd} = {c_odd + y_odd + m_odd + d_odd}**. Modulo 7 = **{t_odd} ({day_name})**")
            
            with col2:
                st.markdown("### Month View")
                st.markdown(generate_calendar_html(y, m, d), unsafe_allow_html=True)

    with tab3:
        if "cal_q" not in st.session_state: st.session_state.cal_q = None
        if "cal_streak" not in st.session_state: st.session_state.cal_streak = 0
        if "cal_total" not in st.session_state: st.session_state.cal_total = 0
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="calendar_prac_diff")
                
                st.metric("Streak", f"🔥 {st.session_state.cal_streak}")
                st.write(f"Question {st.session_state.cal_total + 1} of 10")
                
                if st.button("Generate Question", key="calendar_prac_gen"):
                    y = random.randint(1800, 2200)
                    m = random.randint(1, 12)
                    d = random.randint(1, calendar.monthrange(y, m)[1])
                    date_obj = datetime.date(y, m, d)
                    
                    if diff == "Easy": # Find the day
                        correct = date_obj.strftime("%A")
                        q_text = f"What day of the week is {date_obj.strftime('%d %B %Y')}?"
                        opts = list(DAYS)
                        random.shuffle(opts)
                    elif diff == "Medium": # Days between
                        y2 = y + random.randint(0, 2)
                        m2 = random.randint(1, 12)
                        d2 = random.randint(1, calendar.monthrange(y2, m2)[1])
                        d2_obj = datetime.date(y2, m2, d2)
                        diff_days = abs((date_obj - d2_obj).days)
                        correct = diff_days
                        q_text = f"How many days between {date_obj.strftime('%d %b %Y')} and {d2_obj.strftime('%d %b %Y')}?"
                        opts_set = set([correct])
                        while len(opts_set) < 4: opts_set.add(correct + random.randint(-15, 15))
                        opts = list(opts_set)
                        random.shuffle(opts)
                    else: # Leap years
                        y2 = y + random.randint(20, 80)
                        leap_count = sum(1 for yr in range(y, y2+1) if is_leap_year(yr))
                        correct = leap_count
                        q_text = f"How many leap years are there between {y} and {y2} (inclusive)?"
                        opts_set = set([correct])
                        while len(opts_set) < 4: opts_set.add(correct + random.randint(-3, 3))
                        opts = list(opts_set)
                        random.shuffle(opts)
                    
                    st.session_state.cal_q = {
                        "date": date_obj, "text": q_text, "correct": correct,
                        "options": opts, "answered": False, "diff": diff
                    }
        
        with col2:
            with st.container(border=True):
                if st.session_state.cal_q:
                    q = st.session_state.cal_q
                    
                    st.write(f"<span class='badge-{q['diff'].lower()}'>{q['diff']}</span> **{q['text']}**", unsafe_allow_html=True)
                    
                    ans = st.radio("Select Answer:", q["options"], index=None, key="calendar_prac_radio")
                    
                    if st.button("Submit Answer", key="calendar_prac_submit") and not q["answered"] and ans is not None:
                        q["answered"] = True
                        st.session_state.cal_total += 1
                        
                        is_correct = (str(ans) == str(q["correct"]))
                        
                        if is_correct:
                            st.session_state.cal_streak += 1
                            record_attempt("Calendar Problems", True, q["diff"], "")
                            st.success("✅ Correct!")
                        else:
                            st.session_state.cal_streak = 0
                            record_attempt("Calendar Problems", False, q["diff"], f"Failed calendar {q['diff']}")
                            st.error(f"❌ Wrong! The correct answer is {q['correct']}.")

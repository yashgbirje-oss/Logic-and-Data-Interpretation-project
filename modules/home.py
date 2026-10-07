import streamlit as st
from utils.scoring import get_summary_df

def render():
    # --- HERO SECTION ---
    st.markdown("""
    <div style="text-align: center; padding: 4rem 1rem; border-radius: 24px; margin-bottom: 2rem; background: linear-gradient(180deg, rgba(108, 99, 255, 0.08) 0%, rgba(0, 180, 216, 0.02) 100%); border: 1px solid rgba(128,128,128,0.1);">
        <h1 style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #6C63FF 0%, #00B4D8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;">
            Master Logic & Data
        </h1>
        <p style="font-size: 1.2rem; max-width: 650px; margin: 0 auto 2rem auto; line-height: 1.6;">
            Elevate your quantitative aptitude. Explore interactive lessons, use step-by-step calculators, and test your skills with dynamically generated practice questions.
        </p>
        <div style="display:flex; justify-content:center; gap:16px; flex-wrap: wrap;">
            <div style="background: rgba(108, 99, 255, 0.1); color: #6C63FF; padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">📖 1. Learn Theory</div>
            <div style="background: rgba(0, 180, 216, 0.1); color: #00B4D8; padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">🧮 2. Use Calculators</div>
            <div style="background: rgba(42, 157, 143, 0.1); color: #2A9D8F; padding: 8px 20px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">🎯 3. Practice & Track</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- STATS SECTION ---
    df = get_summary_df()
    total_attempted = df['Attempted'].sum()
    total_correct = df['Correct'].sum()
    overall_accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
    
    st.markdown('<h3 style="margin-bottom: 1rem;">📈 Your Learning Journey</h3>', unsafe_allow_html=True)
    
    scol1, scol2, scol3 = st.columns(3)
    
    def stat_card(value, label, color):
        return f"""
        <div style="background: rgba(128,128,128,0.03); border: 1px solid rgba(128,128,128,0.15); border-radius: 16px; padding: 24px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.03); transition: transform 0.2s;">
           <div style="font-size: 2.5rem; font-weight: 800; color: {color}; margin-bottom: 4px;">{value}</div>
           <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
        </div>
        """
        
    with scol1: st.markdown(stat_card(int(total_attempted), "Questions Attempted", "#6C63FF"), unsafe_allow_html=True)
    with scol2: st.markdown(stat_card(int(total_correct), "Correct Answers", "#00B4D8"), unsafe_allow_html=True)
    with scol3: st.markdown(stat_card(f"{overall_accuracy:.1f}%", "Overall Accuracy", "#2A9D8F"), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- MODULES GRID ---
    st.markdown('<h3 style="margin-bottom: 1.5rem;">🚀 Available Modules</h3>', unsafe_allow_html=True)
    
    def module_card(icon, title, desc, color):
        return f"""
        <div class="custom-card" style="height: 100%; display: flex; flex-direction: column; border-top: 4px solid {color}; padding: 20px;">
            <div style="font-size: 2rem; margin-bottom: 12px;">{icon}</div>
            <h4 style="margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 700;">{title}</h4>
            <p style="font-size: 0.9rem; line-height: 1.5; margin: 0; flex-grow: 1;">{desc}</p>
        </div>
        """

    # Using 3 columns for a wider, more spacious grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(module_card("⏱️", "Clock Problems", "Calculate exact interior and reflex angles between clock hands.", "#6C63FF"), unsafe_allow_html=True)
        st.write("") # spacing
        st.markdown(module_card("📊", "Tabular DI", "Extract insights, sums, and averages from complex corporate data tables.", "#F77F00"), unsafe_allow_html=True)
        st.write("")
        st.markdown(module_card("📉", "Scatter Diagram", "Analyze correlation coefficients (r) and linear regression trends.", "#6C63FF"), unsafe_allow_html=True)
        
    with col2:
        st.markdown(module_card("📅", "Calendar Problems", "Master the 'odd days' method to find the weekday for any historical date.", "#00B4D8"), unsafe_allow_html=True)
        st.write("")
        st.markdown(module_card("📶", "Bar Graph", "Interpret categorical data across grouped and stacked bar charts.", "#E63946"), unsafe_allow_html=True)
        st.write("")
        st.markdown(module_card("🏆", "Result Summary", "Track your weakest modules, view performance charts, and download CSVs.", "#00B4D8"), unsafe_allow_html=True)

    with col3:
        st.markdown(module_card("🧩", "Patterns", "Identify the underlying logic in AP, GP, Fibonacci, and alternating series.", "#2A9D8F"), unsafe_allow_html=True)
        st.write("")
        st.markdown(module_card("🥧", "Pie Chart", "Compute percentage shares and central angles for proportional data.", "#6C63FF"), unsafe_allow_html=True)
        st.write("")
        st.markdown(module_card("📈", "Line Graph", "Detect growth rates and moving average trends over time periods.", "#2A9D8F"), unsafe_allow_html=True)

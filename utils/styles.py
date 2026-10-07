import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }
    
    .custom-card, div[data-testid="metric-container"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .custom-card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    h1, h2, h3 { font-weight: 700; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        font-weight: 600;
    }
    
    footer {visibility: hidden;}
    
    .gradient-text {
        background: linear-gradient(90deg, #6C63FF 0%, #00B4D8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .gradient-header {
        background: linear-gradient(90deg, #6C63FF 0%, #00B4D8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2rem;
        margin-bottom: 0px;
    }
    .sub-header {
        margin-top: 0px;
        margin-bottom: 1.5rem;
    }
    
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(90deg, #6C63FF 0%, #00B4D8 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: filter 0.2s;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
        color: white;
    }
    .badge-easy { background-color: #2A9D8F; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; }
    .badge-medium { background-color: #F77F00; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; }
    .badge-hard { background-color: #E63946; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; }
    
    div[data-testid="stSidebarNav"] li div {
        border-radius: 8px;
    }
    
    .home-card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-left: 4px solid #6C63FF;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

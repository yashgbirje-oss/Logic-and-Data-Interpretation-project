import streamlit as st
import pandas as pd
from utils import auth

def init_session_state():
    if "scores" not in st.session_state:
        st.session_state.scores = {
            "Clock Problems": {"attempted": 0, "correct": 0},
            "Calendar Problems": {"attempted": 0, "correct": 0},
            "Patterns & Figures": {"attempted": 0, "correct": 0},
            "Tabular Data Interpretation": {"attempted": 0, "correct": 0},
            "Bar Graph Analysis": {"attempted": 0, "correct": 0},
            "Pie Chart Analysis": {"attempted": 0, "correct": 0},
            "Line Graph Analysis": {"attempted": 0, "correct": 0},
            "Scatter Diagram Analysis": {"attempted": 0, "correct": 0}
        }
    if "history" not in st.session_state:
        st.session_state.history = []
    if "mistakes" not in st.session_state:
        st.session_state.mistakes = []

def load_user_progress(username):
    """Load this user's saved scores once per login."""
    if st.session_state.get("_loaded_for") == username:
        return
    saved = auth.load_progress(username)
    for mod, sc in saved.get("scores", {}).items():
        if mod in st.session_state.scores:
            st.session_state.scores[mod] = sc
    st.session_state.history = saved.get("history", [])
    st.session_state.mistakes = saved.get("mistakes", [])
    st.session_state._loaded_for = username

def _save():
    user = st.session_state.get("user")
    if user:
        auth.save_progress(user["username"], {
            "scores": st.session_state.scores,
            "history": st.session_state.history[-500:],
            "mistakes": st.session_state.mistakes[-200:],
        })

def record_attempt(module, is_correct, difficulty="Medium", reason=""):
    st.session_state.scores[module]["attempted"] += 1
    if is_correct:
        st.session_state.scores[module]["correct"] += 1
    else:
        st.session_state.mistakes.append({
            "module": module,
            "difficulty": difficulty,
            "reason": reason
        })
    
    st.session_state.history.append({
        "module": module,
        "is_correct": is_correct
    })
    _save()

def get_summary_df():
    data = []
    for mod, score in st.session_state.scores.items():
        attempted = score["attempted"]
        correct = score["correct"]
        accuracy = (correct / attempted * 100) if attempted > 0 else 0
        data.append({
            "Module": mod,
            "Attempted": attempted,
            "Correct": correct,
            "Accuracy": round(accuracy, 2)
        })
    return pd.DataFrame(data)

def get_mistakes():
    return st.session_state.mistakes

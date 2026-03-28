import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="EduMind AI Pro", page_icon="🎓", layout="wide")

# --- 2. SECURITY ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key not found in Secrets!")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🚀 EduMind Control")
    study_mode = st.selectbox("Select AI Persona:", ["Friendly Tutor", "Strict Professor", "Simplifier"])
    st.divider()
    do_summarize = st.button("✨ Summarize Everything")
    do_quiz = st.button("✍️ Generate Practice Quiz")

# --- 4. MAIN INTERFACE ---
st.title("🎓 EduMind AI Pro")
col_input, col_output = st.columns([1, 1])

with col_input:
    notes = st.text_area("Paste your notes here:", height=300)
    user_query = st.text_input("🎯 Ask a specific question:")
    ask_btn = st.button("Analyze & Answer")

with col_output:
    if ask_btn and notes and user_query:
        with st.spinner("Thinking..."):
            response = model.generate_content(f"Mode: {study_mode}. Notes: {notes}. Question: {user_query}")
            st.info(response.text)
            
    if do_summarize and notes:
        with st.spinner("Summarizing..."):
            response = model.generate_content(f"Summarize these notes clearly: {notes}")
            st.success(response.text)

    if do_quiz and notes:
        with st.spinner("Creating quiz..."):
            response = model.generate_content(f"Create a 3-question quiz from these notes: {notes}")
            st.warning(response.text)

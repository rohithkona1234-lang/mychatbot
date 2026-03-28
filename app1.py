import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EduMind AI Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THEME & STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4A90E2; color: white; }
    .stTextArea textarea { border-radius: 10px; }
    </style>
    """, unsafe_allow_all=True)

# --- 3. SECURITY & API SETUP ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("🔑 API Key not found! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- 4. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("🚀 EduMind Control")
    st.subheader("Personalize Your Study")
    
    study_mode = st.selectbox(
        "Select AI Persona:",
        ["Friendly Tutor", "Strict Professor", "Simplifier (ELI5)", "Executive Summary"]
    )
    
    st.divider()
    st.write("📝 **Quick Actions**")
    do_summarize = st.button("✨ Summarize Everything")
    do_quiz = st.button("✍️ Generate Practice Quiz")
    
    if st.button("🗑️ Clear All"):
        st.cache_data.clear()
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("🎓 EduMind AI Pro")
st.caption(f"Currently operating in **{study_mode}** mode.")

# Layout: Left for input, Right for output
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("Input Material")
    notes = st.text_area("Paste your notes, transcript, or textbook text here:", height=400, placeholder="Enter your study material here...")
    
    user_query = st.text_input("🎯 Ask a specific question:", placeholder="e.g., 'What are the three main causes of the war?'")
    ask_btn = st.button("Analyze & Answer")

with col_output:
    st.subheader("AI Analysis")
    
    # Using Tabs to keep results organized
    tab1, tab2, tab3 = st.tabs(["💬 Q&A", "📋 Summary", "📝 Quiz"])
    
    # Logic for Custom Question
    with tab1:
        if ask_btn:
            if not notes or not user_query:
                st.warning("Please provide both notes and a question!")
            else:
                with st.spinner("Brainstorming..."):
                    persona_prompt = f"Act as a {study_mode}. Use ONLY these notes: {notes}. Question: {user_query}"
                    response = model.generate_content(persona_prompt)
                    st.markdown("---")
                    st.markdown(response.text)

    # Logic for Summarization
    with tab2:
        if do_summarize:
            if notes:
                with st.spinner("Condensing information..."):
                    summary_prompt = f"Act as a {study_mode}. Provide a structured summary with bold headers and bullet points for these notes: {notes}"
                    response = model.generate_content(summary_prompt)
                    st.success("Summary Ready!")
                    st.markdown(response.text)
                    st.balloons()
            else:
                st.error("Paste notes first!")

    # Logic for Quiz
    with tab3:
        if do_quiz:
            if notes:
                with st.spinner("Generating challenges..."):
                    quiz_prompt = f"Generate 3 challenging multiple choice questions and 1 short answer question based on these notes. Provide an answer key at the bottom. Notes: {notes}"
                    response = model.generate_content(quiz_prompt)
                    st.warning("Knowledge Check:")
                    st.markdown(response.text)
            else:
                st.error("Paste notes first!")

# --- 6. FOOTER ---
st.divider()
st.caption("Built with ❤️ for better learning. Every update on GitHub refreshes this page instantly.")

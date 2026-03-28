import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Study Assistant", layout="centered")

st.title("🎓 AI Study Assistant")
st.write("Paste your notes below and ask anything about them.")

# --- THE SECURE CONNECTION ---
# This looks for the GEMINI_API_KEY you saved in your second screenshot
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Please check your Streamlit Secrets.")
    st.stop()

# No more 'Enter API Key' box! We go straight to the notes.
notes = st.text_area("📝 Paste your notes here", height=250)
question = st.text_input("❓ What is your question?")

if st.button("Ask AI"):
    if not notes.strip() or not question.strip():
        st.warning("Please provide both notes and a question.")
    else:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"Answer this question using ONLY the provided notes.\nNotes: {notes}\nQuestion: {question}"
            
            with st.spinner("Analyzing..."):
                response = model.generate_content(prompt)
            
            st.subheader("💡 Answer")
            st.info(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

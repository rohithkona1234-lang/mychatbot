import streamlit as st
import google.generativeai as genai

st.title("AI Study Assistant (Gemini Edition)")
st.write("Paste notes and ask questions.")

# Input for Gemini API Key
api_key = st.text_input("Enter your Gemini API key", type="password")

notes = st.text_area("Paste your notes here", height=250)
question = st.text_input("Ask a question")

if st.button("Ask AI"):
    if not api_key:
        st.warning("Please enter your API key.")
    elif not notes.strip():
        st.warning("Please paste some notes.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            # Configure the Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"""
            You are a helpful study assistant. 
            Answer the user's question using ONLY the notes below. 
            If the answer is not in the notes, say: Not found in the notes.

            Notes:
            {notes}

            Question: 
            {question}
            """

            # Generate the response
            response = model.generate_content(prompt)
            
            st.subheader("Answer")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
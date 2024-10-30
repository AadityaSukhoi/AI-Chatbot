import streamlit as st   # UI Design
import os
from dotenv import load_dotenv    # package to get the environment variables loaded into the application
load_dotenv() # loading of all the environment variable

import google.generativeai as genai

# genai configuration of API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initializing the model
model = genai.GenerativeModel('gemini-pro')

# Define a function to generate the response from LLM
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Setting up Streamlit app
st.set_page_config(
    page_title="GemBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setting up header
st.header("GemBot - Your Personal AI Assistant")

# Initialize session state for chat history if it doesn't already exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input question
question = st.text_input("Ask your Question")

# Submit and generate response
if st.button("Submit Your Question") and question:
    response = get_gemini_response(question)
    # Append the question-response pair to the chat history
    st.session_state.chat_history.append((question, response))

# Display chat history in sidebar
st.sidebar.title("Chat History")
for idx, (q, r) in enumerate(st.session_state.chat_history, 1):
    st.sidebar.write(f"**{idx}. You:** {q}")
    st.sidebar.write(f"**GemBot:** {r}")
    st.sidebar.write("---")  # Divider for readability

# Display current response below input
if st.session_state.chat_history:
    last_question, last_response = st.session_state.chat_history[-1]
    st.write("**YOU:**", last_question)
    st.write("**GEMBOT:**", last_response)

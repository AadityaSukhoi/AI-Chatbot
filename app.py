import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

# genai configuration of API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initializing the model
model = genai.GenerativeModel('gemini-pro')

# Function to generate the response from the model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Streamlit app configuration
st.set_page_config(
    page_title="GemBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.header("GemBot - Your Personal AI Assistant")

# Initialize session state for chat messages in the current session
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

# Initialize session state to store different chat sessions in the sidebar
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
    st.session_state.session_names = []  # Store names of the sessions

# Input question
question = st.text_input("Ask your Question")

# Submit and generate response
if st.button("Submit Your Question") and question:
    # Get response from the model
    response = get_gemini_response(question)
    
    # Save current question and response in the ongoing session
    st.session_state.current_chat.append((question, response))

    # Display conversation in the main screen
    for q, r in st.session_state.current_chat:
        st.write("**YOU:**", q)
        st.write("**GEMBOT:**", r)

# Sidebar - Session management
with st.sidebar:
    st.header("Chat Sessions")
    
    # Button to start a new chat session
    if st.button("New Session"):
        # Save the current chat and assign a default name if not empty
        if st.session_state.current_chat:
            st.session_state.chat_sessions.append(st.session_state.current_chat)
            default_name = f"Session {len(st.session_state.chat_sessions)}"
            st.session_state.session_names.append(default_name)
        
        # Clear the current chat for a new session
        st.session_state.current_chat = []
    
    # Display saved chat sessions with options to rename or delete
    for i, session in enumerate(st.session_state.chat_sessions):
        # Update the session name using a text input for real-time renaming
        new_name = st.text_input(f"Session Name {i+1}", value=st.session_state.session_names[i], key=f"name_{i}")
        st.session_state.session_names[i] = new_name  # Update name

        # Display session history under the user-defined name
        with st.expander(new_name):
            for q, r in session:
                st.write("**YOU:**", q)
                st.write("**GEMBOT:**", r)

            # Delete button
            if st.button(f"Delete {new_name}", key=f"delete_{i}"):
                del st.session_state.chat_sessions[i]
                del st.session_state.session_names[i]
                st.experimental_rerun()  # Refresh the app to show changes

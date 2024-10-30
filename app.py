import streamlit as st
import os
import pickle
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

# Function to save sessions to a file for persistence
def save_sessions():
    with open("chat_sessions.pkl", "wb") as file:
        pickle.dump({
            "chat_sessions": st.session_state.chat_sessions,
            "session_names": st.session_state.session_names
        }, file)

# Function to load sessions from the file if it exists
def load_sessions():
    if os.path.exists("chat_sessions.pkl"):
        with open("chat_sessions.pkl", "rb") as file:
            data = pickle.load(file)
            st.session_state.chat_sessions = data.get("chat_sessions", [])
            st.session_state.session_names = data.get("session_names", [])

# Initialize Streamlit app configuration
st.set_page_config(
    page_title="GemBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load sessions from file on page load
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
    st.session_state.session_names = []
    load_sessions()

# Initialize current chat if not already in session state
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

# Initialize input box state
if "input_box" not in st.session_state:
    st.session_state.input_box = ""

# Check if there's an ongoing session; if not, start a new one automatically when a prompt is given
def start_new_session():
    st.session_state.current_chat = []
    st.session_state.chat_sessions.append(st.session_state.current_chat)
    st.session_state.session_names.append(f"Session {len(st.session_state.session_names) + 1}")

# Header
st.header("GemBot - Your Personal AI Assistant")

# Input question
question = st.text_input("Ask your Question", key="input_box", value=st.session_state.input_box)

# Submit and generate response
if question and st.button("Submit Your Question"):
    # Start a new session automatically if there’s no ongoing session
    if not st.session_state.current_chat:
        start_new_session()

    # Get response from the model
    response = get_gemini_response(question)

    # Save current question and response in the ongoing session
    st.session_state.current_chat.append((question, response))

    # Save sessions to maintain state
    save_sessions()

# Display conversation in the main screen (current session)
if st.session_state.current_chat:
    for q, r in st.session_state.current_chat:
        st.write("**YOU:**", q)
        st.write("**GEMBOT:**", r)

# Sidebar - Session management
with st.sidebar:
    st.header("Chat Sessions")

    # New Session Button
    if st.button("New Session"):
        start_new_session()  # Start a new session
        st.session_state.input_box = ""  # Clear the text input box
        st.experimental_rerun()  # Refresh the page to reflect a new session

    # Display saved chat sessions with options to rename or delete
    for i in range(len(st.session_state.chat_sessions)):
        # Use session name with a text input for renaming
        new_name = st.text_input(f"Session Name {i+1}", value=st.session_state.session_names[i], key=f"name_{i}")
        st.session_state.session_names[i] = new_name  # Update name in the session names list

        # Display session history under the user-defined name
        with st.expander(new_name):
            for q, r in st.session_state.chat_sessions[i]:
                st.write("**YOU:**", q)
                st.write("**GEMBOT:**", r)

            # Delete button
            if st.button(f"Delete {new_name}", key=f"delete_{i}"):
                # Remove the session and name at index i
                st.session_state.chat_sessions.pop(i)
                st.session_state.session_names.pop(i)
                save_sessions()  # Save after deletion
                st.experimental_rerun()  # Refresh the app to show changes

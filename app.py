import streamlit as st   # UI Design
import os
from dotenv import load_dotenv    # package to get the environment variables loaded into the application
from datetime import datetime  # For timestamp in session naming
load_dotenv()  # loading all environment variables

import google.generativeai as genai

# genai configuration of API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initializing the model
model = genai.GenerativeModel('gemini-pro')

# Function to generate the response from the model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Setting up the Streamlit app
st.set_page_config(
    page_title="GemBot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chats and session names
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []  # Store chat history for sessions
    st.session_state.session_names = []   # Store names for sessions
    st.session_state.current_chat = []     # Current chat history
    st.session_state.current_session_index = None  # Index of the currently selected session

# Setting up header
st.header("GemBot - Your Personal AI Assistant")

# Sidebar for session management
with st.sidebar:
    st.header("Manage Sessions")

    # Input for session name
    new_session_name = st.text_input("New Session Name", "")

    # Create new session button
    if st.button("Create New Session"):
        if new_session_name:  # Ensure the session name is not empty
            st.session_state.chat_sessions.append([])
            st.session_state.session_names.append(new_session_name)
            st.session_state.current_chat = []  # Clear current chat for new session
            st.session_state.current_session_index = len(st.session_state.session_names) - 1  # Set as current
            st.success(f"Session '{new_session_name}' created!")

    # Select session to view
    selected_session = st.selectbox("Select Session", options=st.session_state.session_names)

    # Update the current chat based on selected session
    if selected_session:
        st.session_state.current_session_index = st.session_state.session_names.index(selected_session)
        st.session_state.current_chat = st.session_state.chat_sessions[st.session_state.current_session_index]

    # Delete session button
    if st.button("Delete Session"):
        if st.session_state.current_session_index is not None:
            st.session_state.chat_sessions.pop(st.session_state.current_session_index)
            st.session_state.session_names.pop(st.session_state.current_session_index)
            st.session_state.current_chat = []
            st.session_state.current_session_index = None
            st.success("Session deleted!")

    # Rename session button
    if st.button("Rename Session") and st.session_state.current_session_index is not None:
        if new_session_name:  # Ensure the new name is not empty
            st.session_state.session_names[st.session_state.current_session_index] = new_session_name
            st.success("Session renamed!")

# Main chat interface
if st.session_state.current_chat is not None:
    # Display chat history for the current session
    for q, r in st.session_state.current_chat:
        st.write("**YOU:**", q)
        st.write("**GEMBOT:**", r)

    # Input for new question
    question = st.text_input("Ask your Question")

    # Check if there's no current session and the question is not empty
    if not st.session_state.current_chat and question:
        # Create a new session with a default name
        default_session_name = f"Session {len(st.session_state.session_names) + 1} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        st.session_state.chat_sessions.append([])
        st.session_state.session_names.append(default_session_name)
        st.session_state.current_chat = []  # Clear current chat for new session
        st.session_state.current_session_index = len(st.session_state.session_names) - 1  # Set as current
        st.success(f"Session '{default_session_name}' created automatically!")

    # Submit button to generate response only if there's a question
    if question and st.button("Submit Your Question"):
        response = get_gemini_response(question)
        st.session_state.current_chat.append((question, response))  # Append question and response to current chat
        st.write("**YOU:**", question)
        st.write("**GEMBOT:**", response)
        st.session_state.chat_sessions[st.session_state.current_session_index] = st.session_state.current_chat  # Update the chat sessions list

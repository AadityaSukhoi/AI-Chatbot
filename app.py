import streamlit as st  # UI Design
import os
from dotenv import load_dotenv  # package to get the environment variables loaded into the application
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
    st.session_state.session_created = False  # Flag to track session creation

# Initialize the input_box if it doesn't exist
if "input_box" not in st.session_state:
    st.session_state.input_box = ""  # Initialize input_box

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
            st.session_state.chat_sessions.append([])  # Start with an empty chat
            st.session_state.session_names.append(new_session_name)
            st.session_state.current_chat = []  # Clear current chat for new session
            st.session_state.current_session_index = len(st.session_state.session_names) - 1  # Set as current
            st.session_state.session_created = True  # Set session created flag
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
            st.session_state.session_created = False  # Reset session created flag
            st.success("Session deleted!")

    # Rename session button
    if st.button("Rename Session") and st.session_state.current_session_index is not None:
        if new_session_name:  # Ensure the new name is not empty
            st.session_state.session_names[st.session_state.current_session_index] = new_session_name
            st.success("Session renamed!")

# Main chat interface
if st.session_state.current_chat is not None:
    # Display chat history for the current session only
    for q, r in st.session_state.current_chat:
        st.write("**YOU:**", q)
        st.write("**GEMBOT:**", r)

    # Show warning message only if no session has been created
    if not st.session_state.session_created:
        st.warning("Create a new session first.")

# Fixed input for new question (only available when a session is selected)
if st.session_state.current_session_index is not None:
    question = st.text_input("Ask your Question", key="input_box", value=st.session_state.input_box)  # Keep the input box fixed

    # Submit button to generate response
    if st.button("Submit Your Question"):
        if question:  # Check if the question is not empty
            response = get_gemini_response(question)
            st.session_state.current_chat.append((question, response))  # Append question and response to current chat
            st.write("**YOU:**", question)
            st.write("**GEMBOT:**", response)
            st.session_state.chat_sessions[st.session_state.current_session_index] = st.session_state.current_chat  # Update the chat sessions list
            
            # Clear the input box after submission
            st.session_state.input_box = ""  # Reset the input box
        else:
            st.warning("Please enter a question before submitting.")

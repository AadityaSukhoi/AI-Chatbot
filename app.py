import streamlit as st   # UI Design
import os
from dotenv import load_dotenv    # package to get the environment variables loaded into the application
load_dotenv() # loading of all the environment variable

import google.generativeai as genai

# genai configuration of API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Initializing the model
model = genai.GenerativeModel('gemini-pro')

# define a function to generate the response from llm
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# setting up streamlit app
st.set_page_config(
    page_title = "GemBot",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# setting up header
st.header("GemBot - Your Personal AI Assistant")
# st.title

# input
question = st.text_input("Ask your Question")

# submit
st.snow()

if st.button("Submit Your Question"):
    response = get_gemini_response(question)
    st.write("**YOU:**", question)
    st.write("**GEMBOT:**", response)

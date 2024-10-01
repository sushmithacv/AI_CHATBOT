import streamlit as st
import openai
import logging
import speech_recognition as sr
from gtts import gTTS
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Streamlit app configuration
st.title("Chatbot Application")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Set OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Function to log interactions
def log_interaction(user_input, bot_response):
    logging.info(f"User: {user_input} | Bot: {bot_response}")

# Function to generate responses
def generate_response(prompt):
    messages = [{"role": "user", "content": prompt}]
    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, I couldn't process that."

# User input
user_input = st.text_input("You:", "")

# Button to clear chat history
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# Generate response on user input
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    gpt_response = generate_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    log_interaction(user_input, gpt_response)  # Log the interaction

# Display chat history
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.write(f"{chat['role'].capitalize()}: {chat['content']}")

# File upload section
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
        st.write("Content of the file:")
        st.write(content)
    # You can add more file types and processing as needed

# Voice input and output
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

def speak_response(response):
    tts = gTTS(response)
    tts.save("response.mp3")
    os.system("start response.mp3")  # Use "afplay" on Mac or "xdg-open" on Linux

# Use voice features
if st.button("Speak"):
    user_input = voice_input()
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        gpt_response = generate_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
        speak_response(gpt_response)  # Speak the response

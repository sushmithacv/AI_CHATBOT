import streamlit as st
import openai

# Set OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Title of the app
st.title("AI Chatbot")

# Set a white background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation and settings
st.sidebar.header("Settings")
st.sidebar.text("This app allows you to chat with an AI.")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to log interactions
def log_interaction(user_input, bot_response):
    st.session_state.chat_history.append({"user": user_input, "bot": bot_response})

# Function to get a response from the OpenAI API
def get_openai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Input box for user question
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            bot_response = get_openai_response(user_input)
            log_interaction(user_input, bot_response)

# Display chat history
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")

# Add footer with app information
st.markdown(
    """
    <footer style="text-align: center; margin-top: 50px;">
        <p style="color: gray;">Developed by [Your Name]</p>
        <p style="color: gray;">&copy; 2024 AI Chatbot</p>
    </footer>
    """,
    unsafe_allow_html=True
)

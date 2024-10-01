import streamlit as st
import openai

# Set OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Title of the app
st.title("Sushmitha's Chatbot")

# Set a pearl white background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EAEAEA; /* Pearl white background */
        color: #333;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .message {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
    }
    .user {
        background-color: #0084ff; /* User message color */
        color: white;
        align-self: flex-end;
    }
    .bot {
        background-color: #e0e0e0; /* Bot message color */
        color: black;
        align-self: flex-start;
    }
    .send-button {
        background-color: #0084ff;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
    }
    .send-button:hover {
        background-color: #0056b3; /* Darker blue on hover */
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
user_input = st.text_input("You:", "", key="input")

if st.button("Send", key="send", help="Click to send your message", css_class="send-button"):
    if user_input:
        with st.spinner("Thinking..."):
            bot_response = get_openai_response(user_input)
            log_interaction(user_input, bot_response)

# Display chat history in a chat-like format
if st.session_state.chat_history:
    chat_container = st.container()
    for chat in st.session_state.chat_history:
        with chat_container:
            st.markdown(f"<div class='message user'>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='message bot'>{chat['bot']}</div>", unsafe_allow_html=True)

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

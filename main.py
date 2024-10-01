import streamlit as st
import openai

# Set OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Define function to get response from OpenAI
def get_openai_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Function to log interactions
def log_interaction(user_input, bot_response):
    st.session_state.chat_history.append({"user": user_input, "bot": bot_response})

# App configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #F8F9FA; /* Light gray background */
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        margin-top: 30px;
    }
    .message {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 80%;
    }
    .user {
        background-color: #007BFF; /* User message color */
        color: white;
        align-self: flex-end;
        margin-left: auto; /* Align user messages to the right */
    }
    .bot {
        background-color: #E0E0E0; /* Bot message color */
        color: black;
        align-self: flex-start;
        margin-right: auto; /* Align bot messages to the left */
    }
    .send-button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .send-button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    footer {
        text-align: center;
        margin-top: 50px;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.header("AI Chatbot")
st.sidebar.text("Ask me anything!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main content
st.markdown("<h1 class='title'>AI Chatbot</h1>", unsafe_allow_html=True)

# Input box for user question
user_input = st.text_input("You:", "", key="input", placeholder="Type your message here...")

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
    <footer>
        <p>Developed by [Your Name]</p>
        <p>&copy; 2024 AI Chatbot</p>
    </footer>
    """,
    unsafe_allow_html=True
)

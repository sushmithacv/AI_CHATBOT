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
        background-color: #FAFAFA; /* Light background color */
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        margin-top: 30px;
        font-size: 2.5rem;
        color: #333;
    }
    .message {
        padding: 12px 16px;
        border-radius: 10px;
        margin: 8px 0;
        max-width: 80%;
        position: relative;
        display: inline-block;
    }
    .user {
        background-color: #007BFF; /* User message color */
        color: white;
        margin-left: auto; /* Align user messages to the right */
    }
    .bot {
        background-color: #E0E0E0; /* Bot message color */
        color: black;
        margin-right: auto; /* Align bot messages to the left */
    }
    .send-button {
        background-color: #28A745;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s;
        margin-top: 20px;
    }
    .send-button:hover {
        background-color: #218838; /* Darker green on hover */
    }
    .input-container {
        display: flex;
        align-items: center;
        margin-top: 20px;
    }
    .input-box {
        flex: 1;
        padding: 10px;
        border: 1px solid #CED4DA;
        border-radius: 5px;
        margin-right: 10px;
        font-size: 1rem;
    }
    footer {
        text-align: center;
        margin-top: 30px;
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

# Chat history display
if st.session_state.chat_history:
    chat_container = st.container()
    for chat in st.session_state.chat_history:
        with chat_container:
            st.markdown(f"<div class='message user'>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='message bot'>{chat['bot']}</div>", unsafe_allow_html=True)

# Input box for user question
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("You:", "", key="input", placeholder="Type your message here...", className="input-box")
    submit_button = st.form_submit_button("Send", help="Click to send your message")

if submit_button and user_input:
    with st.spinner("Thinking..."):
        bot_response = get_openai_response(user_input)
        log_interaction(user_input, bot_response)

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

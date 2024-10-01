import streamlit as st
import openai
from datetime import datetime

# Set your OpenAI API key here
openai.api_key = 'YOUR_API_KEY_HERE'

# Function to get response from OpenAI
def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Set up Streamlit app layout
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# CSS styling for a modern look
st.markdown(
    """
    <style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #F5F5F5;  /* Pearl white background */
        color: #333;  /* Dark text color */
    }
    .header {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #4A4A4A; /* Darker text for header */
        margin: 20px 0;
    }
    .input-area {
        margin: 20px 0;
        background-color: #ffffff; /* White for input area */
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .send-button {
        background-color: #007BFF; /* Blue button */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 20px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
        font-size: 16px;
    }
    .send-button:hover {
        background-color: #0056b3; /* Darker blue on hover */
        transform: scale(1.05); /* Slightly increase size */
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        margin: 20px 0;
    }
    .user-message, .bot-message {
        border-radius: 10px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #007BFF; /* User message blue */
        color: white;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #E9E9E9; /* Bot message gray */
        color: #333;
        align-self: flex-start;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">AI Chatbot</div>', unsafe_allow_html=True)

# Input area
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("You:", key="input", placeholder="Type your message here...", max_chars=300)
    submit_button = st.form_submit_button("Send", help="Click to send your message")

# Placeholder for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if submit_button and user_input:
    # Get response from OpenAI
    with st.spinner("Thinking..."):
        bot_response = get_openai_response(user_input)
        # Log interaction
        st.session_state.chat_history.append({"user": user_input, "bot": bot_response})

# Display chat history
if st.session_state.chat_history:
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            st.markdown(f"<div class='user-message'>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bot-message'>{chat['bot']}</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    "<footer class='footer'>AI Chatbot &copy; 2024 | Developed by [Your Name]</footer>",
    unsafe_allow_html=True
)

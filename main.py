import streamlit as st
import openai

# Set OpenAI API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define function to get response from OpenAI
def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

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
        background-color: #FAFAFA; /* Light gray background */
        color: white; /* Default text color set to white */
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        margin-top: 30px;
        font-size: 2.5rem;
        color: #FFFFFF; /* White text color */
    }
    .message {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .message:hover {
        transform: translateY(-2px); /* Lift effect on hover */
    }
    .user {
        background-color: #007BFF; /* User message color */
        color: white; /* User text color */
        margin-left: auto; /* Align user messages to the right */
    }
    .bot {
        background-color: #E0E0E0; /* Bot message color */
        color: black; /* Bot text color */
        margin-right: auto; /* Align bot messages to the left */
    }
    .input-container {
        display: flex;
        align-items: center;
        margin-top: 20px;
    }
    .input-box {
        flex: 1;
        padding: 12px;
        border: 1px solid #CED4DA;
        border-radius: 5px;
        margin-right: 10px;
        font-size: 1rem;
        transition: border 0.3s;
    }
    .input-box:focus {
        border-color: #007BFF; /* Highlight on focus */
        outline: none; /* Remove outline */
    }
    .send-button {
        background-color: #28A745;
        color: white; /* Send button text color */
        border: none;
        border-radius: 5px;
        padding: 12px 20px;
        cursor: pointer;
        font-weight: bold;
        font-size: 1rem;
        transition: background-color 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .send-button:hover {
        background-color: #218838; /* Darker green on hover */
    }
    footer {
        text-align: center;
        margin-top: 30px;
        color: gray; /* Footer text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.header("AI Chatbot")
st.sidebar.text("Ask me anything!")

# Main content
st.markdown("<h1 class='title'>AI Chatbot</h1>", unsafe_allow_html=True)

# Chat history display
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.markdown(f"<div class='message user'>{chat['user']}</div>", unsafe_allow_html=True)
        if "bot" in chat:
            st.markdown(f"<div class='message bot'>{chat['bot']}</div>", unsafe_allow_html=True)

# Input box for user question
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("You:", "", placeholder="Type your message here...", key="input", 
                               help="Enter your question or message here.")
    submit_button = st.form_submit_button("Send", help="Click to send your message")

if submit_button and user_input:
    with st.spinner("Thinking..."):
        bot_response = get_openai_response(user_input)
        log_interaction(user_input, bot_response)

# Add footer with app information
st.markdown(
    """
    <footer>
        <p>Developed by Sushmitha Christo Vijayakumar</p>
        <p>&copy; 2024 AI Chatbot</p>
    </footer>
    """,
    unsafe_allow_html=True
)

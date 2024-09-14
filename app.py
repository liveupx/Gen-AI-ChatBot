import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize session state
if 'websites' not in st.session_state:
    st.session_state.websites = {}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def train_website(url):
    # For simplicity, we're just storing the URL as content
    # In a real application, you'd scrape the website here
    st.session_state.websites[url] = f"This is the content for {url}"
    return f"Website {url} trained successfully"

def chat_with_ai(message, website_url):
    if website_url not in st.session_state.websites:
        return "Please train a website first."

    website_content = st.session_state.websites[website_url]
    prompt = f"Website content: {website_content}\n\nUser: {message}\nAI:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for the website."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("Widgetx Chatbot")

# Display logo
st.image("static/widgetx_logo.png", width=200)

# Training section
st.header("Train the Chatbot")
url = st.text_input("Enter website URL")
if st.button("Train"):
    result = train_website(url)
    st.success(result)

# Chat section
st.header("Chat")
website_url = st.selectbox("Select a website", options=list(st.session_state.websites.keys()))

if website_url:
    user_message = st.text_input("Type your message...")
    if st.button("Send"):
        ai_response = chat_with_ai(user_message, website_url)
        st.session_state.chat_history.append(("User", user_message))
        st.session_state.chat_history.append(("AI", ai_response))

    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "User":
            st.text_input("User", value=message, disabled=True)
        else:
            st.text_area("AI", value=message, height=100, disabled=True)

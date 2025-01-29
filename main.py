import streamlit as st
import pyttsx3
from groq import Groq

# Initialize Groq API client
API_KEY = "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"
client = Groq(api_key=API_KEY)
MAX_WORDS = 500

# Initialize TTS engine
def initialize_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # Default female voice
    engine.setProperty("rate", 200)  # Set speed
    return engine

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

def word_count(text):
    return len(text.split())

def truncate_text(text, max_words):
    words = text.split()
    return " ".join(words[:max_words]) + "..." if len(words) > max_words else text

def format_response(response_text):
    """Format chatbot response into clean bullet points with bold text."""
    response_lines = response_text.split('\n')
    clean_lines = [line.strip() for line in response_lines if line.strip()]
    formatted_response = "\n".join(f"- **{line}**" for line in clean_lines)
    return formatted_response

def generate_response(input_text, model="llama3-8b-8192"):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": input_text}],
            model=model,
        )
        output_text = chat_completion.choices[0].message.content
        if word_count(output_text) > MAX_WORDS:
            output_text = truncate_text(output_text, MAX_WORDS)
        return output_text
    except Exception as e:
        return f"Error generating response: {e}"

st.title("Mental Health Support Chatbot")

# Clear chat history if a new prompt is entered
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

with st.form(key='chat_form'):
    user_message = st.text_input("You:")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_message:
    # Clear previous chat messages for new prompt
    st.session_state['messages'] = [("You", user_message)]
    
    response = generate_response(user_message)
    formatted_response = format_response(response)
    
    st.session_state['messages'].append(("Bot", formatted_response))

# Display the current chat session
for sender, message in st.session_state['messages']:
    st.markdown(f"**{sender}:** {message}")

# Session Summary
if st.sidebar.button("Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state.get("mood_tracker", [])):
        st.sidebar.write(f"{i + 1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")

# Resources Section
st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")

# Disclaimer
st.sidebar.markdown("**Data Privacy Disclaimer:** This app does not permanently store or share user data.")

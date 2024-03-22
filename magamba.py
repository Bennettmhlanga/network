import streamlit as st
import requests
import json

# Streamlit app
st.title("HELPFUL YOUTH EMPOWERING PARTNER")

# Collect the OpenAI API key from the user
openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Function to chat with the AI model
def chat_with_ai(message):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # Raises an HTTPError if the response was unsuccessful
        information = response.json() # Use the json() method to parse the response
        if 'choices' in information and len(information['choices']) > 0 and 'message' in information['choices'][0] and 'content' in information['choices'][0]['message']:
            ai_response = information['choices'][0]['message']['content']
            return ai_response
        else:
            return "Error: Unexpected response format from the API."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"Error occurred: {err}"

# Sidebar for chat option
st.sidebar.markdown("""
<a href="https://www.fontawesome.com/v5.15/icons/comments?style=solid" target="_blank">
<i class="fas fa-comments"></i>
</a>
""", unsafe_allow_html=True)

if st.sidebar.button("Chat with an assistant"):
    user_message = st.sidebar.text_input("Type your message here:")
    if user_message:
        ai_response = chat_with_ai(user_message)
        st.sidebar.write(f"AI: {ai_response}")

# Function to summarize text using the GPT-3.5-turbo model
def summarize_text(text):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text but keep the context."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    information = json.loads(response.text)
    summary = information['choices'][0]['message']['content']
    return summary

# Function to analyze sentiment using the GPT-3.5-turbo model
def analyze_sentiment(text):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes the sentiment of text."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    information = json.loads(response.text)
    sentiment = information['choices'][0]['message']['content']
    return sentiment

# Function to generate hashtags based on the sentiment analysis output
def generate_hashtags_using_gpt(sentiment):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": f"You are a helpful assistant that generates hashtags based on the sentiment analysis output: {sentiment}. Use tone, language, and energy of an Activist."
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    information = json.loads(response.text)
    hashtags = information['choices'][0]['message']['content']
    return hashtags

# Collect the text input from the user
text_input = st.text_area("Enter your text here:")

if st.button("Summarize, Analyze Sentiment, and Generate Hashtags"):
    summary = summarize_text(text_input)
    st.write("Summary:", summary)
    
    sentiment = analyze_sentiment(text_input)
    st.write("Sentiment:", sentiment)
    
    generated_hashtags = generate_hashtags_using_gpt(sentiment)
    st.write("Hashtags:", generated_hashtags)

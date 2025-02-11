import streamlit as st
from openai import OpenAI
import os

# Set the page configuration
st.set_page_config(
    page_title="LLM Prototype",
    page_icon="🧠",
    layout="centered",  # Options: "centered" or "wide"
    initial_sidebar_state="auto"  # Options: "auto", "expanded", "collapsed"
)

# Load API Key
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY') 
#PERPLEXITY_API_KEY = open_file("KEYS/perplexity_api_key.txt")

# Set up OpenAI client
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

# Define the Perplexity call function
def perplexity_call(model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response

# Streamlit App UI
st.title("LLM KI Assistent")
st.write("Was hast du für eine Frage?")

# User input
user_input = st.text_input("Stelle deine Frage hier:")

# Call API when user submits a question
if st.button("Get Answer") and user_input:
    with st.spinner("Fetching response..."):
        # Prepare messages for the API
        messages = [
            {
                "role": "system",
                "content": (
                    "Du bist ein intelligenter KI Assistent, der Usern dabei hilft, ihre Fragen zu beantworten."
                    "Du antwortest stets auf DEUTSCH."
                ),
            },
            {"role": "user", "content": user_input},
        ]

        # Call Perplexity API
        try:
            model = "sonar-pro"
            result = perplexity_call(model, messages)
            
            # Extract response and citations
            answer = result.choices[0].message.content
            citations = result.citations

            # Display the response
            st.subheader("Antwort")
            st.write(answer)

            # Display citations
            st.subheader("Quellen")
            if citations:
                for idx, citation in enumerate(citations, start=1):
                    st.write(f"[{idx}] [{citation}]({citation})")
            else:
                st.write("Keine Quellen gefunden.")

        except Exception as e:
            st.error(f"An error occurred: {e}")


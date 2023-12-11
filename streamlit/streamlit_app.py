import openai
import streamlit as st

def generate_response(api_key, model, description, language):
    openai.api_key = api_key

    message = [
        {"role": "system", "content": f"""Using language: {language}. As a reverse dictionary in the target language, you'll be given descriptors of a single word. From these, suggest a single word that closely matches the given descriptors in {language}. In your response, include the following for that one word, nicely formatted in Markdown:
            **Single Word** (Pronunciation) *Part of Speech*
            --*new line *--
            Definition in {language}
            *new line*
            --*blank new line*--
            *Suggest an example sentence in {language} using the word*
            *empty new line*
            --*blank new line*--
            Etymology: A brief explanation of the word's origin.
            --*blank new line*--
            Alternatives (underline, include "Alternatives" simply the alternatives in {language}, each alternative in a single line separated by a comma)
            """},
        {"role": "user", "content": description}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=message,
        max_tokens=150
    )


    return response.choices[0].message.content

def main():
    st.set_page_config(page_title="GPT-based Reverse Word Finder", layout="wide")
    st.title('Reverse Lookup Dictionary with GPT')

    # Sidebar for API Key and Model Selection
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    model = st.sidebar.selectbox("Choose the GPT model", ["gpt-3.5-turbo", "gpt-4"])

    # User inputs
    with st.form(key='input_form'):
        description = st.text_area("Enter the description of the word", height=150)
        language = st.selectbox("Select Language", ["English", "Spanish", "French", "German", "Other"])
        submit_button = st.form_submit_button(label='Generate')

    if submit_button and description:
        if api_key:
            result = generate_response(api_key, model, description, language)
            st.markdown(result)
        else:
            st.error("Please enter your OpenAI API Key.")

if __name__ == "__main__":
    main()
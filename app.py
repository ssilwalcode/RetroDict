from flask import Flask, render_template, request
import openai

app = Flask(__name__)

def generate_response(api_key, model, description, language):
    openai.api_key = api_key

    message = [
        {"role": "system",
         "content": f"""Using language: {language}. As a reverse dictionary in the target language, you'll be given descriptors of a single word. From these, suggest a single word that closely matches the given descriptors in {language}. In your response, include the following for that one word, nicely formatted in Markdown:
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

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        api_key = request.form['api_key']
        model = request.form['model']
        description = request.form['description']
        language = request.form['language']
        if api_key:
            result = generate_response(api_key, model, description, language)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

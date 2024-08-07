from rake_nltk import Rake 
from flask import Flask, request, jsonify
from database import *
from helper import *

app = Flask(__name__)

rake = Rake()

@app.route('/getChat', methods=['GET'])
def configAI():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    chat_text = data.get("chat")
    if chat_text is None:
        return jsonify({"error": "Missing 'chat' key in JSON data"}), 400
    # question = chat_text['chatInput']
    print('Received chat message:', chat_text)
    output = [chat_text]
    print(output, 'output')

    return jsonify(output)

@app.route('/key_phrase', methods=['GET'])
def key_phrase():
    session_id = generate_random_id()
    data = request.get_json()
    chat_input = data["chat"]["output"]
    print(chat_input,'chat_input')

    question = get_human_chat()
    rake.extract_keywords_from_text(chat_input) 
    keywords = rake.get_ranked_phrases() 
    if len(keywords) > 10:
        top_10_keywords = keywords[:10]
    else:
        top_10_keywords = keywords
    nonrepeating_words = list(set(top_10_keywords))
    suggest_words = ','.join(map(str, nonrepeating_words))

    input = question +'.' + suggest_words

    updated_data = create_input_data(session_id,input)

    return  jsonify(updated_data)

@app.route('/', methods=['GET'])
def default_router():

    return "hello aa"

if __name__ == '__main__':
    app.run(debug=True, host='10.77.0.8', port=5000)


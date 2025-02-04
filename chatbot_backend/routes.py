from flask import request, jsonify
from chatbot_backend import app
from models import chat_model

@app.route('/chat')
def chat():
    data = request.json
    user_message = data.get('message')

    # Get a response from the chat model
    response = chat_model.chat(user_message)

    return jsonify({'response': response})

from flask import request, jsonify
from chatbot_backend import app

@app.route('/chat')
def chat():
    data = request.json
    user_message = data.get('message')
    return jsonify({'message': 'Hello, World!'})

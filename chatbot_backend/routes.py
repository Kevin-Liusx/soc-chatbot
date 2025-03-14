from flask import request, jsonify
from chatbot_backend import app
from models import chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    chat_history = data.get("chatHistory", [])

    chat_history_langchain_format = []
    for msg in chat_history:
        if msg['role'] == 'system':
            chat_history_langchain_format.append(SystemMessage(content=msg['content']))
        elif msg['role'] == 'user':
            chat_history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'chatbot':
            chat_history_langchain_format.append(AIMessage(content=msg['content']))
    # Get a response from the chat model
    response = chat_model.chat(user_message, chat_history_langchain_format)

    return jsonify({'response': response})

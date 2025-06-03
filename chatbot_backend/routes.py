import os
import time
import uuid
from flask import request, jsonify
from chatbot_backend import app, utils
# from chat_engine import chat_model
from chat_engine import chatbot
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

CHATBOT_API_KEY = os.getenv('CHATBOT_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    start_time = time.time()

    data = request.json
    user_message = data.get('message')
    chat_history = data.get("chatHistory", [])
    # Get session ID from frontend or generate new
    session_id = data.get('sessionId', 'session_' + str(uuid.uuid4())[:8])
    api_key = request.headers.get('CHATBOT-API-KEY')
    is_techstaff = request.headers.get('IS-TECHSTAFF', 'false') == 'true'

    if api_key != CHATBOT_API_KEY:
        return jsonify({'error': 'Unauthorized access'}), 403

    chat_history_langchain_format = []
    for msg in chat_history:
        if msg['role'] == 'system':
            chat_history_langchain_format.append(SystemMessage(content=msg['content']))
        elif msg['role'] == 'user':
            chat_history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == 'chatbot':
            chat_history_langchain_format.append(AIMessage(content=msg['content']))
    # Get a response from the chat model
    response = chatbot.chat(user_message, chat_history_langchain_format, is_techstaff)

    # Calculate response time
    end_time = time.time()
    processing_time = end_time - start_time

    # Log chat interaction
    utils.log_chat(session_id=session_id, user_message=user_message, bot_response=response, response_time=processing_time)

    return jsonify({'response': response})

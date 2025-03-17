from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

from chatbot_backend import routes

# initialize the vector store when importing the routes. Should be done inside chat_model.py

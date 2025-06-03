from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

# Call startup routine here
from chat_engine.startup import startup_routine
startup_routine()

from chatbot_backend import routes

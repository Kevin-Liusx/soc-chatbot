from chatbot_backend import app
from documents import initialize_documents
from models import initialize_vector_store
import logging

logging.basicConfig(level=logging.INFO)

def startup_routine():
    logging.info("Application startup: initializing resources...")
    try:
        initialize_documents()
        initialize_vector_store()
        logging.info("Startup initialization completed successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise

if __name__ == '__main__':
    startup_routine()
    app.run(debug=True, host='0.0.0.0', port=3000)
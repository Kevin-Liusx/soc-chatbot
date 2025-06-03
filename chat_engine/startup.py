import os
import logging
from documents import initialize_documents, dochub_api
from chat_engine.vector_store import initialize_vector_store

def startup_routine():
    logging.basicConfig(level=logging.INFO)

    logging.info("Application startup: initializing resources...")
    try:
        documents_dir = dochub_api.current_dir
        general_data_dir = os.path.join(documents_dir, "general_data")
        techstaff_data_dir = os.path.join(documents_dir, "techstaff_data")
        initialize_documents(general_data_dir)
        initialize_documents(techstaff_data_dir)
        
        initialize_vector_store()
        logging.info("Startup initialization completed successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise

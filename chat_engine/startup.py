import os
import logging
from documents import initialize_documents, dochub_api
from chat_engine.vector_store import initialize_vector_store
from chat_engine.configuration import TECHSTAFF_DB_DIR, GENERAL_DB_DIR

def startup_routine():
    logging.basicConfig(level=logging.INFO)

    logging.info("Application startup: initializing resources...")
    try:
        documents_dir = dochub_api.current_dir
        general_data_dir = os.path.join(documents_dir, "general_data")
        techstaff_data_dir = os.path.join(documents_dir, "techstaff_data")
        initialize_documents(general_data_dir, os.getenv("DOCHUB_USERNAME_GENERAL"), os.getenv("DOCHUB_PASSWORD_GENERAL"))
        initialize_documents(techstaff_data_dir, os.getenv("DOCHUB_USERNAME_STAFF"), os.getenv("DOCHUB_PASSWORD_STAFF"))

        initialize_vector_store(general_data_dir, GENERAL_DB_DIR)
        # initialize_vector_store(techstaff_data_dir, TECHSTAFF_DB_DIR)
        logging.info("Startup initialization completed successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise

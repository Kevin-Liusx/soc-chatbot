import os
import logging
from documents import initialize_documents
from chat_engine.vector_store import initialize_vector_store
from chat_engine.configuration import (
    TECHSTAFF_DB_DIR,
    GENERAL_DB_DIR,
    DIRECTORIES_TO_INCLUDE_GENERAL,
    DIRECTORIES_TO_INCLUDE_TECHSTAFF,
    GENERAL_DATA_DIR,
    TECHSTAFF_DATA_DIR,
    DIRECTORIES_TO_EXCLUDE_GENERAL,
    DIRECTORIES_TO_EXCLUDE_TECHSTAFF,
)

def startup_routine():
    logging.basicConfig(level=logging.INFO)

    logging.info("Application startup: initializing resources...")
    try:
        initialize_documents(GENERAL_DATA_DIR, DIRECTORIES_TO_INCLUDE_GENERAL, DIRECTORIES_TO_EXCLUDE_GENERAL, 
                             os.getenv("DOCHUB_USERNAME"), os.getenv("DOCHUB_PASSWORD"))
        initialize_documents(TECHSTAFF_DATA_DIR, DIRECTORIES_TO_INCLUDE_TECHSTAFF, DIRECTORIES_TO_EXCLUDE_TECHSTAFF, 
                             os.getenv("DOCHUB_USERNAME"), os.getenv("DOCHUB_PASSWORD"))

        initialize_vector_store(GENERAL_DATA_DIR, GENERAL_DB_DIR)
        initialize_vector_store(TECHSTAFF_DATA_DIR, TECHSTAFF_DB_DIR)
        logging.info("Startup initialization completed successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise

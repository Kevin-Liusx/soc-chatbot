import os
import shutil
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import documents
from chat_engine import vector_store
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

def regenerate_vector_store(data_dir=None, db_dir=None):
    """
    Regenerates the vector store by performing the following steps:
    1. Deletes existing DocHub documents and the corresponding vector store.
    2. Fetches the latest DocHub documents.
    3. Creates a new vector store using the fetched documents.
    """
    if not data_dir or not db_dir:
        print(f"❗️ Path not provided. Please provide the paths to the data directory and the database directory.")
        return
    # Step 1: Delete existing documents and vector store
    for path in [data_dir, db_dir]:
        if os.path.exists(path):
            print(f"❗️ Deleting {path} ...")
            shutil.rmtree(path)
            print(f"✅ Cleared: {path}")

    # Step 2 & 3: Fetch latest documents and create vector store
    if data_dir == GENERAL_DATA_DIR and db_dir == GENERAL_DB_DIR:
        documents.initialize_documents(
            data_dir, DIRECTORIES_TO_INCLUDE_GENERAL, DIRECTORIES_TO_EXCLUDE_GENERAL,
            os.getenv("DOCHUB_USERNAME_GENERAL"), os.getenv("DOCHUB_PASSWORD_GENERAL")
        )
        vector_store.initialize_vector_store(data_dir, db_dir)
    elif data_dir == TECHSTAFF_DATA_DIR and db_dir == TECHSTAFF_DB_DIR:
        documents.initialize_documents(
            data_dir, DIRECTORIES_TO_INCLUDE_TECHSTAFF, DIRECTORIES_TO_EXCLUDE_TECHSTAFF,
            os.getenv("DOCHUB_USERNAME_STAFF"), os.getenv("DOCHUB_PASSWORD_STAFF")
        )
        vector_store.initialize_vector_store(data_dir, db_dir)
    else:
        print(f"❗️ Invalid data directory or database directory provided: {data_dir}, {db_dir}")
        return
        

if __name__ == "__main__":
    regenerate_vector_store(GENERAL_DATA_DIR, GENERAL_DB_DIR)
    regenerate_vector_store(TECHSTAFF_DATA_DIR, TECHSTAFF_DB_DIR)
    # regenerate_vector_store()

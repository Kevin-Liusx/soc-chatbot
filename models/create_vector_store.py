import os
import shutil
import sys

# Get the path to the parent directory (your_project)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import vector_store
import documents

def regenerate_vector_store():
    """
    Regenerates the vector store by performing the following steps:
    1. Deletes existing DocHub documents and the corresponding vector store.
    2. Fetches the latest DocHub documents.
    3. Creates a new vector store using the fetched documents.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    documents_dir = os.path.abspath(os.path.join(current_dir, "../documents/data"))
    vectorstore_dir = os.path.join(current_dir, "db")

    # Step 1: Delete existing documents and vector store
    for path in [documents_dir, vectorstore_dir]:
        if os.path.exists(path):
            print(f"❗️ Deleting {path} ...")
            shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)
            print(f"✅ Cleared: {path}")

    # Step 2: Fetch latest DocHub documents (custom sync logic)
    print("🔄 Fetching latest DocHub documents ...")
    documents.initialize_documents()  # Make sure this method writes to `documents/data/`
    print("✅ Fetched latest documents.")

    # Step 3: Reinitialize vector store from scratch
    print("Rebuilding vector store ...")
    vector_store.initialize_vector_store()
    print("✅ Vector store regenerated successfully.")

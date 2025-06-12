import sys
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Get the path to the parent directory (your_project)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now you can import from document
from documents import dochub_sync
from chat_engine import utils
from chat_engine.configuration import (
    TECHSTAFF_DB_DIR,
    GENERAL_DB_DIR,
    GENERAL_DATA_DIR,
    TECHSTAFF_DATA_DIR,
    EMBEDDINGS,
)

def update_vector_store_helper(db, file_names):
    # Load the text documents from the document path and store it with metadata
        documents = []
        source_ids_to_delete = set()
        for file in file_names:
            if file.endswith(".md"):
                loader = TextLoader(file)
                dochub_docs = loader.load()
                for doc in dochub_docs:
                    source_id, source_url = utils.extract_metadata(doc.page_content)
                    doc.metadata["source"] = source_id
                    doc.metadata["source_url"] = source_url
                    documents.append(doc)
                    source_ids_to_delete.add(source_id)
        
        # Step 1: Delete existing entries from the vector store based on source_id
        for source_id in source_ids_to_delete:
            print(f"Deleting document with source_id: {source_id}")
            db.delete(where={"source": source_id})

        # Step 2: Split the documents into chunks and add updated documents
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(documents)
        # Display information about the split documents
        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(documents)}")

        # Token-based batching
        print("\n--- Batching documents by token count ---")
        batches = utils.batch_documents_by_tokens(documents)
        print(f"Total batches: {len(batches)}")

        print(f"➕ Adding {len(documents)} new document chunks to Chroma...")

        for i, batch in enumerate(batches):
            db.add_documents(batch)
            print(f"Batch {i + 1}: Added {len(batch)} chunks.")

        print("✅ Chroma vector store updated with changed files and deduplication.")


def update_vector_store():
    """
    Update the vector store with new documents.
    """
    if os.path.exists(TECHSTAFF_DB_DIR) and os.path.exists(GENERAL_DB_DIR):
        if not os.path.exists(TECHSTAFF_DATA_DIR) or not os.path.exists(GENERAL_DATA_DIR):
            raise FileNotFoundError(f"One or more document path does not exist.")

        # Fetch recent changes and update the local data
        file_names_tech = dochub_sync.update_recent_changes(TECHSTAFF_DATA_DIR)
        file_names_general = dochub_sync.update_recent_changes(GENERAL_DATA_DIR)
    
        print("Updating the two vector stores with latest changes...")

        # Create the OpenAI embeddings
        embeddings = EMBEDDINGS

        # Load the existing Chroma vector store
        print("🔄 Loading the two existing Chroma vector stores...")
        db_techstaff = Chroma(persist_directory=TECHSTAFF_DB_DIR, embedding_function=embeddings)
        db_general = Chroma(persist_directory=GENERAL_DB_DIR, embedding_function=embeddings)
        print("✅ Loaded existing Chroma vector stores.")

        if not file_names_tech and not file_names_general:
            print("✅ No new or updated documents to process.")
            return
        
        if file_names_tech:
            print(f"🔄 Updating the TechStaff vector store with {len(file_names_tech)} recent changes...")
            update_vector_store_helper(db_techstaff, file_names_tech)

        if file_names_general:
            print(f"🔄 Updating the General vector store with {len(file_names_general)} recent changes...")
            update_vector_store_helper(db_general, file_names_general)
    else:
        print("❗ One or more persistent directory does not exist. Please initialize the vector store first.")

    
if __name__ == "__main__":
    # This is only for testing purposes
    # In production, this function should be run as a cron job
    update_vector_store()
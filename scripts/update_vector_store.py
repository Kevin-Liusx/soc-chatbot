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
    DIRECTORIES_TO_INCLUDE_GENERAL,
    DIRECTORIES_TO_INCLUDE_TECHSTAFF,
    GENERAL_DATA_DIR,
    TECHSTAFF_DATA_DIR,
    DIRECTORIES_TO_EXCLUDE_GENERAL,
    DIRECTORIES_TO_EXCLUDE_TECHSTAFF,
)


def update_vector_store():
    """
    Update the vector store with new documents.
    """
    # Define the directory containing the text file and persistent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    document_path = os.path.abspath("documents/data/dochub_md")
    persistent_directory = os.path.join(current_dir, "db", "chroma_db_with_metadata")
    # Fetch recent changes and update the local data
    changed_content_files = dochub_sync.update_recent_changes()
    
    if os.path.exists(persistent_directory):
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path {document_path} does not exist.")
        
        print("Updating vector store with latest changes...")

        # Create the OpenAI embeddings
        print("\n --- Initializing OpenAI embeddings ---")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
        )
        print("\n ---Finished initializing OpenAI embeddings ---")

        # Load the existing Chroma vector store
        print("🔄 Loading existing Chroma vector store...")
        db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
        print("✅ Loaded existing Chroma vector store.")


        # Load the text documents from the document path and store it with metadata
        documents = []
        source_ids_to_delete = set()
        for file in changed_content_files:
            if file.endswith(".md"):
                loader = TextLoader(file)
                dochub_docs = loader.load()
                for doc in dochub_docs:
                    source_id, source_url = utils.extract_metadata(doc.page_content)
                    doc.metadata["source"] = source_id
                    doc.metadata["source_url"] = source_url
                    documents.append(doc)
                    source_ids_to_delete.add(source_id)
        
        if not changed_content_files:
            print("✅ No new or updated documents to process.")
            return
        
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

        print(f"➕ Adding {len(documents)} new document chunks to Chroma...")
        db.add_documents(documents)
        db.persist()
        print("✅ Chroma vector store updated with changed files and deduplication.")
    else:
        print("❗ Persistent directory does not exist. Please initialize the vector store first.")

    
if __name__ == "__main__":
    # This is only for testing purposes
    # In production, this function should be run as a cron job
    update_vector_store()
import os

from utils import extract_metadata

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


# Define the directory containing the text file and persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
document_path = os.path.abspath("documents/data/dochub_md")
persistent_directory = os.path.join(current_dir, "db", "chroma_db_with_metadata")

def initialize_vector_store():
    # Check if the Chroma vector store already exists
    if not os.path.exists(persistent_directory):
        print("Persistent directory does not exist. Initializing vector store...")

        # Ensure the document path exists
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path {document_path} does not exist.")
        
        # Load the text documents from the document path and store it with metadata
        documents = []
        for root, _, files in os.walk(document_path):
            for file in files:
                if file.endswith(".md"):
                    loader = TextLoader(os.path.join(root, file))
                    dochub_docs = loader.load()
                    for doc in dochub_docs:
                        source_id, source_url = extract_metadata(doc.page_content)
                        doc.metadata["source"] = source_id
                        doc.metadata["source_url"] = source_url
                        documents.append(doc)

        # Split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(documents)

        # Display information about the split documents
        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(documents)}")

        # Create the OpenAI embeddings
        print("\n --- Initializing Chroma vector store ---")
        embeddings = OpenAIEmbeddings(
            model_name="text-embedding-3-small",
        )
        print("\n ---Finished initializing OpenAI embeddings ---")

        # Create the Chroma vector store
        print("\n--- Creating Chroma vector store ---")
        db = Chroma.from_documents(
            documents, embeddings, persist_directory=persistent_directory)
        print("\n--- Finished creating Chroma vector store ---")
    else:
        print("Vector store already exists. No need to initialize.")


if __name__ == "__main__":
    initialize_vector_store()
# loader = TextLoader(os.path.join(document_path, "start/buildfac/buildfac.md"))
# dochub_docs = loader.load()
# print(dochub_docs[0].page_content)
# source_id, source_url = extract_metadata(dochub_docs[0].page_content)
# print(source_id)
# print(source_url)

# count = 0
# for root, _, files in os.walk(document_path):
#     for file in files:
#         if file.endswith(".md"):
#             print(os.path.exists(os.path.join(root, file)))

# book_files = [
#     os.path.abspath(os.path.join(current_dir, "../documents/data/dochub_md/start/buildfac/buildfac.md")),
#     os.path.abspath(os.path.join(current_dir, "../documents/data/dochub_md/start/buildfac/useful_info.md"))
# ]

# documents = []
# for book_file in book_files:
#     loader = TextLoader(book_file)
#     dochub_docs = loader.load()
#     for doc in dochub_docs:
#         print("hiiiiiiiii")
#         print(doc)
#         doc.metadata["source"] = book_file
#         documents.append(doc)

# text_splitter = CharacterTextSplitter(chunk_size=20000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# print("\n--- Document Chunks Information ---")
# print(f"Number of document chunks: {len(docs)}")
# # print(docs[0])

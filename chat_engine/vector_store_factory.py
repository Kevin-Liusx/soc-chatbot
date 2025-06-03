from langchain_community.vectorstores import Chroma
from chat_engine.configuration import EMBEDDINGS, TECHSTAFF_DB_DIR, GENERAL_DB_DIR

def load_vector_store(is_tecstaff: bool):
    directory = TECHSTAFF_DB_DIR if is_tecstaff else GENERAL_DB_DIR
    return Chroma(persist_directory=directory, embedding_function=EMBEDDINGS)

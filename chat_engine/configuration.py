import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-small")

TECHSTAFF_DB_DIR = os.path.join(BASE_DIR, "db", "chroma_db_techstaff")
GENERAL_DB_DIR = os.path.join(BASE_DIR, "db", "chroma_db_general")

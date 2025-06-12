import os
from dotenv import load_dotenv
from documents import dochub_api
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()

DB_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")

llm = ChatOpenAI(model="gpt-4o")
EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-small")

documents_dir = dochub_api.current_dir
GENERAL_DATA_DIR = os.path.join(documents_dir, "general_data")
TECHSTAFF_DATA_DIR = os.path.join(documents_dir, "techstaff_data")

TECHSTAFF_DB_DIR = os.path.join(DB_BASE_DIR, "chroma_db_techstaff")
GENERAL_DB_DIR = os.path.join(DB_BASE_DIR, "chroma_db_general")

DIRECTORIES_TO_INCLUDE_GENERAL = ["cf", "buildfac", "safety"]
DIRECTORIES_TO_INCLUDE_TECHSTAFF = ["cf", "buildfac", "safety", "tech", "infra"]
DIRECTORIES_TO_EXCLUDE_GENERAL = []
DIRECTORIES_TO_EXCLUDE_TECHSTAFF = []
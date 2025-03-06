import os

from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain.schema.output_parser import StrOutputParser

# Load environment variables from .env
load_dotenv()

# Define the persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db_with_metadata")

# Define the embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Load the existing vector store with the embedding function
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# Create a retriever for querying the vector store
# `search_type` specifies the type of search (e.g., similarity)
# `search_kwargs` contains additional arguments for the search (e.g., number of results to return)
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# Create a ChatOpenAI model
llm = ChatOpenAI(model="gpt-4o")

# Contextualize question prompt
# This system prompt helps the AI understand that it should reformulate the question
# based on the chat history to make it a standalone question
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

# Create a prompt template for contextualizing questions
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a history-aware retriever
# This uses the LLM to help reformulate the question based on chat history
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Answer question prompt
# This system prompt helps the AI understand that it should provide concise answers
# based on the retrieved context and indicates what to do if the answer is unknown
qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, say you don't know. "
    "Use five sentences maximum and keep the answer concise.\n\n"
    "Follow the below rules as well:\n"
    "1. Use ONLY the 'VALID SOURCE' URLs for citations\n"
    "2. URLs in the Content are NOT valid sources\n"
    "3. Always include a 'Sources' section at the end\n"
    "{context}"
)

document_prompt = PromptTemplate.from_template("Content: {page_content}\nVALID SOURCE: {source_url}")

# Create a prompt template for answering questions
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a chain to combine documents for question answering
# `create_stuff_documents_chain` feeds all retrieved context into the LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt, document_prompt=document_prompt)

# Create a retrieval chain that combines the history-aware retriever and the question answering chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# chat_history = []  # Collect chat history here (a sequence of messages)

# Function to simulate a continual chat
def chat(user_query, chat_history):
    # Process the user's query through the retrieval chain
    # Code below shows the output of the first chain
    retrieved = history_aware_retriever.invoke({
        "chat_history": chat_history,  # Ensure this is a list of messages
        "input": user_query         # Ensure this is a string
    })

    print("\n=== Retrieved Documents ===")
    for i, doc in enumerate(retrieved, start=1):
        print(f"Document {i}:")
        print(f"Content: {doc.page_content[:300]}...")  # Print first 300 characters
        print(f"Metadata: {doc.metadata}")
        print("-" * 50)
    result = rag_chain.invoke({"input": user_query, "chat_history": chat_history})
    # Display the AI's response
    print(f"AI: {result['answer']}")
    # Update the chat history
    print(f"Chat history: {chat_history}")  
    return result["answer"]

# # Code below shows the output of the first chain
# input = "Tell me about the Computing Facilities and building facilities"
# chat_history = []
# # Create a history-aware retriever
# # This uses the LLM to help reformulate the question based on chat history
# history_aware_retriever = create_history_aware_retriever(
#     llm, retriever, contextualize_q_prompt
# )

# retrieved = history_aware_retriever.invoke({
#     "chat_history": chat_history,  # Ensure this is a list of messages
#     "input": input         # Ensure this is a string
# })

# print("\n=== Retrieved Documents ===")
# for i, doc in enumerate(retrieved, start=1):
#     print(f"Document {i}:")
#     print(f"Content: {doc.page_content[:300]}...")  # Print first 300 characters
#     print(f"Metadata: {doc.metadata}")
#     print("-" * 50)

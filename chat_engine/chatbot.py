import logging
from chat_engine.retriever_factory import create_contextualized_retriever
from chat_engine.qa_chain_factory import create_qa_chain

def chat(user_query: str, chat_history: list, is_techstaff: bool):
    logging.info("Processing query...")

    # Build the retrieval and QA chain
    retriever = create_contextualized_retriever(is_techstaff)
    rag_chain = create_qa_chain(retriever)

    # Retrieve documents (for debugging/logging purposes)
    retrieved_docs = retriever.invoke({
        "chat_history": chat_history,
        "input": user_query
    })

    print("\n=== Retrieved Documents ===")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"Document {i}:")
        print(f"Content: {doc.page_content[:100]}...")  # Print first 300 characters
        print(f"Metadata: {doc.metadata}")
        print("-" * 50)
    print("\n=== Retrieved Documents ===\n\n")

    result = rag_chain.invoke({"input": user_query, "chat_history": chat_history})
    # Display the user's query
    print(f"\n\n❗️User: {user_query}")
    # Display the AI's response
    print(f"\n\n❗️AI: {result['answer']}")
    # Display the chat history
    print(f"\n\n❗️Chat history: {chat_history}")
    print("="*80 + "\n\n")
    return result["answer"]

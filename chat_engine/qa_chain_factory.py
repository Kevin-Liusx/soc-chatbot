from chat_engine.retriever_factory import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
# Answer question prompt
# This system prompt helps the AI understand that it should provide concise answers
# based on the retrieved context and indicates what to do if the answer is unknown
qa_system_prompt = (
    "You are an AI assistant designed to answer questions based strictly on the provided retrieved context. "
    "If the retrieved context is empty or irrelevant to the query, follow these rules:\n"
    "- If the query is a general greeting (e.g., 'hi', 'hello'), respond politely.\n"
    "- If the user asks about your capabilities, briefly explain your role.\n"
    "- If the query is unrelated to the context, respond with: 'My knowledge is limited to the content within the SoC Dochub. If you can't find what you need, please submit a service request through https://rt.comp.nus.edu.sg, and our technical team will assist you.'\n"
    "- If the user asks an open-ended or vague question, ask them to clarify.\n\n"

    "### Rules to Follow:\n"
    "1. Answer **ONLY** using the retrieved context when available.\n"
    "2. Do NOT use any external knowledge or assumptions.\n"
    "3. Keep responses concise (maximum of five sentences).\n"
    "4. Use ONLY 'VALID SOURCE' URLs for citations.\n"
    "5. URLs mentioned within the retrieved content are NOT valid sources.\n"
    "6. Always include a 'Sources' section at the end if applicable.\n\n"
    "7. When citing a source, use the format `[link description](link)` instead of raw URLs. For example, use `[Cleaner Temp Cards](https://dochub-dev.comp.nus.edu.sg/buildfac%3Afacilities%3Acleaner_temp_cards)`.\n\n"
    "**Retrieved Context:**\n"
    
    "{context}"
)

document_prompt = PromptTemplate.from_template("Content: {page_content}\nVALID SOURCE: {source_url}")

def create_qa_chain(history_aware_retriever):
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    qa_chain = create_stuff_documents_chain(llm, qa_prompt, document_prompt=document_prompt)
    return create_retrieval_chain(history_aware_retriever, qa_chain)

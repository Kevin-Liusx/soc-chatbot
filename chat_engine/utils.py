import re
import tiktoken

def extract_metadata(document):
    page_id = None
    link = None

    # -----------------------
    # 1) Extract Page ID
    # -----------------------
    marker_id = "Original DocHub Page ID:"
    index_id_marker = document.find(marker_id)
    if index_id_marker != -1:
        # Start searching for backticks after the marker
        search_start = index_id_marker + len(marker_id)
        first_tick = document.find("`", search_start)
        if first_tick != -1:
            second_tick = document.find("`", first_tick + 1)
            if second_tick != -1:
                page_id = document[first_tick+1 : second_tick].strip()

    # -----------------------
    # 2) Extract DocHub link
    # -----------------------
    marker_link = "[DocHub Link]("
    index_link_marker = document.find(marker_link)
    if index_link_marker != -1:
        # Start searching for ")" after the link marker
        search_start = index_link_marker + len(marker_link)
        end_paren = document.find(")", search_start)
        if end_paren != -1:
            link = document[search_start : end_paren].strip()

    return page_id, link

def count_tokens(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return len(tokenizer.encode(text))

def batch_documents_by_tokens(documents, max_tokens=230000):
    """Group documents into batches where each batch does not exceed max token limit."""
    batches = []
    current_batch = []
    current_tokens = 0
    batch_idx = 1

    for doc in documents:
        doc_tokens = count_tokens(doc.page_content)
        if current_tokens + doc_tokens > max_tokens:
            print(f">>> Batch {batch_idx} total tokens: {current_tokens}")
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
            batch_idx += 1
        current_batch.append(doc)
        current_tokens += doc_tokens

    if current_batch:
        print(f">>> Batch {batch_idx} total tokens: {current_tokens}")
        batches.append(current_batch)

    return batches
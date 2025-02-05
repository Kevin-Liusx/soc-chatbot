import json
import dochub_api
from documents.utils import save_last_check_time
import os

current_dir = dochub_api.current_dir
get_page_content = dochub_api.get_page_content
list_pages = dochub_api.list_pages

def initialize_documents():
    """Initializes the documents directory.
    This function is called when the module is imported.
    It fetches the list of pages and saves it to a file.
    """
    
    list_pages()
    save_last_check_time()
    with open(current_dir + "/data/page_list.json", "r") as file:
        page_list = json.load(file)

    for page in page_list:
        page_id = page["id"]
        get_page_content(page_id)

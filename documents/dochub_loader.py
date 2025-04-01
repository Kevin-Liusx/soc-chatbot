import json
from documents import dochub_api
from documents.utils import save_last_check_time
import os

current_dir = dochub_api.current_dir
data_dir = os.path.join(current_dir, "data")
get_page_content = dochub_api.get_page_content
list_pages = dochub_api.list_pages

def initialize_documents():
    """Initializes the documents directory.
    This function is called when the module is imported.
    It fetches the list of pages and saves it to a file.
    """
    if not os.path.exists(data_dir):
        print(f"✅ 'data' directory not found. Creating 'data' directory")
        os.makedirs(data_dir, exist_ok=True)
        list_pages()
        save_last_check_time()
        with open(current_dir + "/data/page_list.json", "r") as file:
            page_list = json.load(file)
            
        print(f"✅ Starting to fetch content for all the pages")
        for page in page_list["result"]:
            page_id = page["id"]
            get_page_content(page_id)
        print(f"✅ Page contents saved in 'data' directory")
    else:
        print(f"✅ 'data' directory found. Skipping data initialization.")

if __name__ == "__main__":
    initialize_documents()

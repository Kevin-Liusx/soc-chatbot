import json
from documents import dochub_api
from documents.utils import save_last_check_time
import os

get_page_content = dochub_api.get_page_content
list_pages = dochub_api.list_pages
login = dochub_api.login

def initialize_documents(data_dir, directories_to_include, USERNAME, PASSWORD):
    """Initializes the documents directory.
    This function is called when the module is imported.
    It fetches the list of pages and saves it to a file.
    """
    if not os.path.exists(data_dir):
        print(f"❗️ One or more data directory not found. Creating directory")
        os.makedirs(data_dir, exist_ok=True)
        login(USERNAME, PASSWORD)
        list_pages(data_dir, directories_to_include)
        save_last_check_time(data_dir)
        with open(data_dir + "/page_list.json", "r") as file:
            page_list = json.load(file)
            
        print(f"✅ Starting to fetch content for all the pages")
        for page in page_list["result"]:
            page_id = page["id"]
            get_page_content(data_dir, page_id)
        print(f"✅ Page contents saved in {data_dir} directory")
    else:
        print(f"✅ {data_dir} directory found. Skipping data initialization.")

if __name__ == "__main__":
    initialize_documents()

import json
from documents import dochub_api

current_dir = dochub_api.current_dir
get_page_content = dochub_api.get_page_content
list_pages = dochub_api.list_pages

list_pages()

with open(current_dir + "/data/page_list.json", "r") as file:
    page_list = json.load(file)

for page in page_list["result"]:
    page_id = page["id"]
    get_page_content(page_id)

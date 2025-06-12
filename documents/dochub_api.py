import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
import json
import time
import config
from documents import utils
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file
dotenv_path = os.path.join(current_dir, '../.env')
load_dotenv(dotenv_path=dotenv_path)

# DokuWiki JSON-RPC API endpoint
API_URL = config.DOCHUB_API_URL

# Dochub URL
DOCHUB_URL = config.DOCHUB_URL

# Number of days to fetch recent changes from DokuWiki
RECENT_CHANGE_DAYS = config.RECENT_CHANGE_DAYS

# Your DokuWiki username and password
AUTH = os.getenv("DOCHUB_AUTH_KEY")

# Path to store the last update timestamp
LAST_CHECK_FILE = "last_check.txt"

# Headers for the request
headers = {
    "Content-Type": "application/json",
}

# Dochub Session
session = requests.Session()

# JSON-RPC login request payload
def login(USERNAME, PASSWORD):
    """Logs in to DokuWiki and retrieves the session token."""
    payload = {
        "params": {
            "user": USERNAME,
            "pass": PASSWORD,
        },
        "method": "core.login",
        "id": 1,
        "jsonrpc": "2.0"
    }

    response = session.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload)
    )

    result = response.json()

    if 'error' in result:
        raise RuntimeError(f"Login failed: {result['error']['message']}")

    print("✅ Dochub logged in successfully.")
    return session


# JSON-RPC listPages request payload
def list_pages(file_save_location, directories_to_include, depth=0):
    """Lists all available pages in DokuWiki."""

    combined_results = None

    for idx, dir in enumerate(directories_to_include):
        payload = {
            "jsonrpc": "2.0",
            "method": "core.listPages",
            "params": [dir, depth],
            "id": idx + 1
        }

        response = session.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            print(f"✅ Fetching page ids under the directory '{dir}'")
            data = response.json()

            if combined_results is None:
                combined_results = data
            else:
                if "result" in data:
                    combined_results["result"].extend(data["result"])
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    if combined_results:
        # Format the JSON output for readability
        combined_results["result"].extend([{"id": "start"}])
        formatted_data = json.dumps(combined_results, indent=4)
        # Save the output to a file
        output_file = os.path.join(file_save_location, "page_list.json")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(formatted_data)

        print(f"✅ Response saved and formatted in '{output_file}'")


# JSON-RPC getPage request payload
"""
Dokuwiki uses : to separate namespaces and pages. 
For example, the page "namespace/page" is represented as "namespace:page".
If it is a directory, it will be represented as "namespace:start".
If it is a file, it will be represented as "namespace:file".
Where namespace could be several levels of directories.
"""
def get_page_content(file_save_path, page_id):
    """Retrieves the content of a specific wiki page."""
    if "sidebar" in page_id.lower():
        print(f"🚫 Skipping sidebar page id: {page_id}")
        return
    
    data_dir = os.path.join(file_save_path, "dochub_raw")
    data_dir_md = os.path.join(file_save_path, "dochub_md")
    path_parts = page_id.split(":")
    last_path_part = path_parts[-1]

    if len(path_parts) == 1:
        os.makedirs(os.path.join(data_dir, last_path_part), exist_ok=True)
        os.makedirs(os.path.join(data_dir_md, last_path_part), exist_ok=True)
        output_file = os.path.join(data_dir, last_path_part, f"{last_path_part}.json")
        output_file_md = os.path.join(data_dir_md, last_path_part, f"{last_path_part}.md")
    else:
        os.makedirs(os.path.join(data_dir, "start", *path_parts[:-1]), exist_ok=True)
        os.makedirs(os.path.join(data_dir_md, "start", *path_parts[:-1]), exist_ok=True)
        if last_path_part == "start":
            filename = f"{path_parts[-2]}"
            output_file = os.path.join(data_dir, "start", *path_parts[:-1], f"{filename}.json")
            output_file_md = os.path.join(data_dir_md, "start", *path_parts[:-1], f"{filename}.md")
        else:
            output_file = os.path.join(data_dir, "start", *path_parts[:-1], f"{last_path_part}.json")
            output_file_md = os.path.join(data_dir_md, "start", *path_parts[:-1], f"{last_path_part}.md")

    payload = {
        "jsonrpc": "2.0",
        "method": "wiki.getPage",
        "params": [page_id, 0],  # 0 for the latest revision
        "id": 1
    }

    response = session.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        content = response.json().get("result", "")
        source_note = (
            "\n\n---\n"
            " **Note:** This page was retrieved from **DocHub**, "
            f" **Original DocHub Page ID:** `{page_id}`\n"
            f" **You can find the original page at:** [DocHub Link]({config.DOCHUB_URL}/{page_id.replace(':', '%3A')})"
        )
        utils.convert_dokuwiki_syntax_to_markdown(content, source_note, output_file_md)
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump({"page_id": page_id, "content": content}, file, indent=4)
        return content, output_file_md
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None


# JSON-RPC getRecentPageChanges request payload
def getRecentPageChanges(dir_path):
    """Fetches recent page changes from DokuWiki within the last RECENT_CHANGE_DAYS."""
    current_time = int(time.time())
    past_time = current_time - (RECENT_CHANGE_DAYS * 24 * 60 * 60)
    payload_getRecentPageChanges = {
        "jsonrpc": "2.0",
        "method": "core.getRecentPageChanges",
        "params": [past_time],
        "id": 1
    }

    response = session.post(
        API_URL,
        headers=headers,
        data=json.dumps(payload_getRecentPageChanges)
    )
    
    if response.status_code == 200:
        print("hit")
        changes = response.json().get("result", [])
        print(changes)
        output_file = os.path.join(dir_path, "recent_changes.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(changes, file, indent=4)
        return changes
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    login(os.getenv("DOCHUB_USERNAME"), os.getenv("DOCHUB_PASSWORD"))
    list_pages()

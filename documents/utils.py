import json
import os
import time
import pypandoc

LAST_CHECK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/last_check.json")

def get_last_check_time():
    """Returns the last timestamp when the recent changes were checked."""
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, "r") as file:
            data = json.load(file)
            return data["timestamp"]
    return None


def save_last_check_time():
    """Updates the last check timestamp with the current time."""
    current_time = int(time.time())
    with open(LAST_CHECK_FILE, "w") as file:
        json.dump({"last_check": current_time}, file)


def convert_dokuwiki_syntax_to_markdown(raw_text, output_path):
    """Converts DokuWiki syntax to Markdown and saves it to a file."""
    markdown_text = pypandoc.convert_text(raw_text.encode("utf-8"), "markdown", format="dokuwiki")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_text)

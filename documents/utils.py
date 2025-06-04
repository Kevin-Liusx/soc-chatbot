import json
import os
import time
import pypandoc

LAST_CHECK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/last_check.json")

def get_last_check_time(file_save_path):
    """Returns the last timestamp when the recent changes were checked."""
    file_save_path = os.path.join(file_save_path, "/last_check.json")
    if os.path.exists(file_save_path):
        with open(file_save_path, "r") as file:
            data = json.load(file)
            return data["timestamp"]
    return None


def save_last_check_time(dir_save_path):
    """Updates the last check timestamp with the current time."""
    file_save_path = os.path.join(dir_save_path, "last_check.json")
    current_time = int(time.time())
    with open(file_save_path, "w") as file:
        json.dump({"last_check": current_time}, file)


def convert_dokuwiki_syntax_to_markdown(raw_text, source_note, output_path):
    """Converts DokuWiki syntax to Markdown and saves it to a file."""
    markdown_text = pypandoc.convert_text(raw_text.encode("utf-8"), "markdown", format="dokuwiki")
    markdown_text += source_note
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to a file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_text)

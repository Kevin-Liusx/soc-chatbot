import os
import json
from documents.dochub_api import get_page_content, getRecentPageChanges, login
from documents.utils import get_last_check_time, save_last_check_time
from chat_engine.configuration import (
    TECHSTAFF_DB_DIR,
    GENERAL_DB_DIR,
    DIRECTORIES_TO_INCLUDE_GENERAL,
    DIRECTORIES_TO_INCLUDE_TECHSTAFF,
    GENERAL_DATA_DIR,
    TECHSTAFF_DATA_DIR,
    DIRECTORIES_TO_EXCLUDE_GENERAL,
    DIRECTORIES_TO_EXCLUDE_TECHSTAFF,
)

def update_recent_changes(dir_path):
    """Fetches recent changes and updates the local data.
    This function is intended to be run as a cron job.
    """
    # Get the last time the recent changes were checked, only usefull when not using cron job
    # last_check_time = get_last_check_time()
    file_content_list = []
    login(os.getenv("DOCHUB_USERNAME"), os.getenv("DOCHUB_PASSWORD"))
    if getRecentPageChanges(dir_path=dir_path):
        recent_changes_file = os.path.join(dir_path, "recent_changes.json")
        if not os.path.exists(recent_changes_file):
            raise FileNotFoundError(f"Recent changes file not found: {recent_changes_file}, please initialize the documents first.")
        with open(recent_changes_file, "r") as file:
            save_last_check_time(dir_path)
            recent_change_list = json.load(file)

        for page in recent_change_list:
            page_id = page["id"]
            first_word = page_id.split(":")[0]
            if dir_path == TECHSTAFF_DATA_DIR:
                if not any(first_word == included for included in DIRECTORIES_TO_INCLUDE_TECHSTAFF):
                    continue
                if any(excluded in page_id for excluded in DIRECTORIES_TO_EXCLUDE_TECHSTAFF):
                    continue
                content, output_file_md = get_page_content(dir_path, page_id)
                file_content_list.append(output_file_md)
            else:
                if not any(first_word == included for included in DIRECTORIES_TO_INCLUDE_GENERAL):
                    continue
                if any(excluded in page_id for excluded in DIRECTORIES_TO_EXCLUDE_GENERAL):
                    continue
                content, output_file_md = get_page_content(dir_path, page_id)
                file_content_list.append(output_file_md)
    return file_content_list

if __name__ == "__main__":
    # This is only for testing purposes
    # In production, this function should be run as a cron job
    update_recent_changes()
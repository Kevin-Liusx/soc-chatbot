import os
import json
from .dochub_api import get_page_content, getRecentPageChanges, login
from .utils import get_last_check_time, save_last_check_time

def update_recent_changes():
    """Fetches recent changes and updates the local data.
    This function is intended to be run as a cron job.
    """
    # Get the last time the recent changes were checked, only usefull when not using cron job
    # last_check_time = get_last_check_time()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_list = []
    login()
    if getRecentPageChanges():
        recent_changes_file = os.path.join(current_dir, "data", "recent_changes.json")
        with open(recent_changes_file, "r") as file:
            save_last_check_time()
            recent_change_list = json.load(file)

        for page in recent_change_list:
            page_id = page["id"]
            content, output_file_md = get_page_content(page_id)
            path_list.append(output_file_md)
    return path_list

if __name__ == "__main__":
    # This is only for testing purposes
    # In production, this function should be run as a cron job
    update_recent_changes()
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
from dochub_api import get_page_content, getRecentPageChanges
from utils import get_last_check_time, save_last_check_time

def update_recent_changes():
    """Fetches recent changes and updates the local data.
    This function is intended to be run as a cron job.
    """
    # Get the last time the recent changes were checked, only usefull when not using cron job
    # last_check_time = get_last_check_time()

    if getRecentPageChanges():
        recent_changes_file = os.path.join(current_dir, "data", "recent_changes.json")
        with open(recent_changes_file, "r") as file:
            save_last_check_time()
            page_list = json.load(file)

        for page in page_list["result"]:
            page_id = page["id"]
            get_page_content(page_id)


update_recent_changes()
import json
import os
import time

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
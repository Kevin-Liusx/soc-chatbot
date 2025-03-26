from datetime import datetime
import csv
import os

def log_chat(session_id, user_message, bot_response, response_time):
    """Logs chat interactions to a csv file"""
    log_file = os.path.join(os.path.dirname(__file__), '../documents/data/chat_logs.csv')
    file_exists = os.path.exists(log_file)
    print(file_exists)

    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                'timestamp', 
                'session_id', 
                'user_message', 
                'bot_response', 
                'response_time_seconds'
            ])

        writer.writerow([
            datetime.now().isoformat(),
            session_id,
            user_message,
            bot_response,
            response_time
        ])

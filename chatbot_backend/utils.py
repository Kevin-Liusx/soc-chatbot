from datetime import datetime
import csv
import os

def log_chat(session_id, user_message, bot_response, response_time):
    """Logs chat interactions to a date-based csv file"""
    log_dir = os.path.join(os.path.dirname(__file__), '../logs/chat_logs')
    date_str = datetime.now().strftime('%Y-%m-%d')
    log_file =  os.path.join(log_dir, f'{date_str}.csv')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_exists = os.path.exists(log_file)

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

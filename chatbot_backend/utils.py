import bleach
import csv
import os
import re
from datetime import datetime

# Allowed characters: alphanumeric + common punctuation
ALLOWED_PATTERN = re.compile(r'^[a-zA-Z0-9\s.,!?\'"@#\-_/\[\]{}()&%$:]+$')

# Known bad patterns (SQLi, shell injection, traversal, etc.)
BLACKLISTED_PATTERNS = [
    r"\bSELECT\b", r"\bDROP\b", r"\bUNION\b", r"\bINSERT\b", r"\bUPDATE\b",
    r";", r"\|\|", r"\|\s", r"&", r"`", r"\$", r"\bOR\s+1=1\b",
    r"(\.\./)+", r"--", r"\bexec\b", r"\bshutdown\b"
]
SUSPICIOUS_PATTERNS = {
    "URL": re.compile(r"(https?://|www\.)", re.IGNORECASE),
    "Unix path": re.compile(r"/(etc|bin|usr|var)/", re.IGNORECASE),
    "Windows path": re.compile(r"[a-zA-Z]:\\(?:Windows|Users|Program Files)", re.IGNORECASE),
    "Spam characters": re.compile(r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]{5,}"),
    "XSS": re.compile(r"<\s*(script|img|iframe|onerror|onload)", re.IGNORECASE)
}

def detect_suspicious_pattern(text: str):
    for name, pattern in SUSPICIOUS_PATTERNS.items():
        if pattern.search(text):
            return name  # return the type of issue
    return None
    
def is_valid_input(text: str) -> bool:
    """Check if input contains only allowed characters."""
    return bool(ALLOWED_PATTERN.fullmatch(text))

def is_blacklisted(text: str) -> bool:
    """Check input against known malicious patterns."""
    for pattern in BLACKLISTED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def is_safe_input(text: str) -> bool:
    """Final check for use in route handlers."""
    return is_valid_input(text) and not is_blacklisted(text)

def sanitize_input(text: str) -> str:
    return bleach.clean(text, strip=True)

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

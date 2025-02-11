import hashlib
import json
import os
import time
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables from a .env file (optional)
load_dotenv()

# Create a timestamped log file automatically for tracking changes
log_filename = f"file_integrity_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load email credentials from environment variables for sending alerts
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# File to store hashes of monitored files
HASH_FILE = "hashes.json"
BACKUP_FILE = "hashes_backup.json"

# Folder to monitor for file integrity changes
FOLDER_TO_MONITOR = "test_folder"

# Time interval for checking (in seconds)
CHECK_INTERVAL = 10  # Adjust based on need

# Exclude certain file types or directories
EXCLUDE_EXTENSIONS = {".tmp", ".log"}  # Add extensions to ignore
EXCLUDE_DIRECTORIES = {"__pycache__", ".git"}  # Add folders to ignore

def backup_hashes():
    """Create a backup of the current hash file before updating."""
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, 'r') as f:
                data = f.read()
            with open(BACKUP_FILE, 'w') as f:
                f.write(data)
            logging.info("Backup of hash file created.")
        except Exception as e:
            logging.error(f"Error creating backup: {e}")

def calculate_file_hash(filepath):
    """Generate SHA-256 hash for a given file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(4096):  # Read file in chunks
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error hashing {filepath}: {e}")
        return None

def load_hashes():
    """Load existing file hashes from JSON file."""
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning("Error reading hash file. Resetting...")
            return {}
    return {}

def save_hashes(hashes):
    """Save file hashes to JSON file."""
    try:
        backup_hashes()  # Backup before saving new hashes
        with open(HASH_FILE, 'w') as f:
            json.dump(hashes, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving hashes: {e}")

def send_email_alert(filepath, change_type):
    """Send an email alert if a file has been modified, deleted, or added."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        logging.warning("Email credentials not set. Skipping email alert.")
        return
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = f"⚠️ File Integrity Alert: {change_type}"

        body = f"🚨 ALERT: File integrity event detected!\n\n" \
               f"File: {filepath}\n" \
               f"Change Type: {change_type}\n" \
               f"Time: {time.ctime()}"
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        logging.info(f"Email alert sent for {filepath}. Change: {change_type}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def check_folder():
    """Check the folder for any modified, deleted, or newly added files."""
    hashes = load_hashes()
    changes_detected = False
    file_count = 0
    current_files = {}

    for root, _, files in os.walk(FOLDER_TO_MONITOR):
        if any(excluded in root for excluded in EXCLUDE_DIRECTORIES):
            continue

        for file in files:
            if any(file.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
                continue

            filepath = os.path.join(root, file)
            file_hash = calculate_file_hash(filepath)

            if file_hash:
                current_files[filepath] = file_hash
                file_count += 1

                if filepath in hashes:
                    if hashes[filepath] != file_hash:
                        print(f"{Fore.YELLOW}⚠️ File changed: {filepath}{Style.RESET_ALL}")
                        logging.warning(f"File changed: {filepath}")
                        send_email_alert(filepath, "Modified")
                        changes_detected = True
                else:
                    print(f"{Fore.GREEN}🆕 New file detected: {filepath}{Style.RESET_ALL}")
                    logging.info(f"New file detected: {filepath}")
                    send_email_alert(filepath, "New File Added")
                    changes_detected = True

    # Detect deleted files
    deleted_files = set(hashes.keys()) - set(current_files.keys())
    for deleted_file in deleted_files:
        print(f"{Fore.RED}❌ File deleted: {deleted_file}{Style.RESET_ALL}")
        logging.warning(f"File deleted: {deleted_file}")
        send_email_alert(deleted_file, "Deleted")
        changes_detected = True

    # Always update hash file to reflect current state
    if changes_detected or hashes.keys() != current_files.keys():
        save_hashes(current_files)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Checked at {current_time} - Monitoring {file_count} files.")
    print(f"\r✅ Monitoring {file_count} files... [{current_time}]", end="", flush=True)

def monitor_files():
    """Continuously monitor files for integrity changes."""
    print(f"🛡️ Real-time monitoring '{FOLDER_TO_MONITOR}'... (Press Ctrl+C to stop)")

    try:
        while True:
            check_folder()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user (Ctrl+C).")
        logging.info("Monitoring stopped by user (Ctrl+C).")

if __name__ == "__main__":
    monitor_files()  # Start monitoring process

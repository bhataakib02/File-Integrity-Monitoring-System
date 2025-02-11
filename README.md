🛡️ File Integrity Monitoring System

📌 Overview

This File Integrity Monitoring System is a Python-based tool that continuously monitors a specified folder for file changes. It detects modifications, deletions, and new file additions, logging each event and optionally sending email alerts for security notifications.

🚀 Features

Real-time file monitoring in a specified directory.

SHA-256 hashing to detect file modifications.

Automatic logging of detected changes.

Email alerts for file changes (modification, deletion, new file added).

Exclusions support to ignore specific file types and directories.

Backup mechanism to store previous hashes before updates.

User-friendly console output with color-coded status messages.

📂 Folder Structure

📦 FileIntegrityMonitor

 ├── 📜 file_integrity_monitor.py  # Main script
 
 ├── 📜 .env                        # Environment variables (optional)
 
 ├── 📜 hashes.json                 # Stores file hashes
 
 ├── 📜 hashes_backup.json          # Backup of hashes.json
 
 ├── 📜 README.md                   # Documentation

🛠️ Prerequisites

Make sure you have Python 3.7+ installed.

🔹 Install Required Dependencies

Run the following command to install the required dependencies:

pip install -r requirements.txt

🔹 Required Python Packages:

hashlib (built-in)

os, time, json, logging (built-in)

smtplib, email.mime (built-in)

dotenv (for environment variables)

colorama (for colored console output)

Install missing packages manually using:

pip install python-dotenv colorama

⚙️ Configuration

1️⃣ Set Up Environment Variables

Create a .env file in the project folder to store email credentials:

EMAIL_SENDER=your_email@gmail.com

EMAIL_PASSWORD=your_app_password

EMAIL_RECEIVER=recipient_email@gmail.com

📌 Use an App Password if using Gmail (avoid storing actual passwords).

2️⃣ Modify Script Settings

Edit file_integrity_monitor.py to adjust the monitoring folder and exclusions:

FOLDER_TO_MONITOR = "test_folder"

EXCLUDE_EXTENSIONS = {".tmp", ".log"}

EXCLUDE_DIRECTORIES = {"__pycache__", ".git"}

CHECK_INTERVAL = 10  # Interval in seconds

🔍 How It Works

Initial Scan: The script computes and stores SHA-256 hashes for all files in the target folder.

Continuous Monitoring: It checks the folder every CHECK_INTERVAL seconds.

Detection & Alerts: If a file is modified, deleted, or added:

Logs the event.

Updates the hashes.json file.

Sends an email alert (if configured).

Backup Handling: Before updating hashes, a backup is stored in hashes_backup.json.

▶️ Usage

Run the script

python file_integrity_monitor.py

👀 The script will now monitor the folder continuously. Press Ctrl+C to stop.

🔔 Example Alerts

Console Output:

🛡️ Real-time monitoring 'test_folder'... (Press Ctrl+C to stop)

🆕 New file detected: test_folder/example.txt


⚠️ File changed: test_folder/document.pdf

❌ File deleted: test_folder/old_report.docx

✅ Monitoring 5 files... [2025-02-11 10:30:00]

Email Alert Example:

Subject: ⚠️ File Integrity Alert: Modified

🚨 ALERT: File integrity event detected!

File: test_folder/document.pdf

Change Type: Modified

Time: Tue, 11 Feb 2025 10:30:00 GMT

🛑 Stopping the Script

Press Ctrl+C to exit safely.

📌 Notes

Ensure email credentials are correctly set up.

Modify EXCLUDE_EXTENSIONS and EXCLUDE_DIRECTORIES as needed.

Keep hashes.json and hashes_backup.json secure to prevent tampering.

💡 Future Enhancements

✅ GUI-based monitoring dashboard

✅ Support for multi-folder monitoring

✅ Integration with external logging services

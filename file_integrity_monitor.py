import hashlib
import os
import time
import configparser
import logging
from smtplib import SMTP
from email.message import EmailMessage

# Load configurations from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# Settings
SCAN_INTERVAL = int(config['SETTINGS']['ScanInterval'])
ALERT_EMAIL = config['ALERT']['Email']
ALERT_ON_CHANGE = config['ALERT'].getboolean('AlertOnChange')
MONITOR_PATHS = config['MONITOR']['Paths'].split(',')
SMTP_USER=config['SMTP']['Username']
SMTP_PASS=config['SMTP']['Password']

# Logging setup
LOG_FILE = "logs/fim.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Email alert setup (using SMTP)
def send_email_alert(changes):
    if not ALERT_EMAIL:
        return
    msg = EmailMessage()
    msg.set_content(f"File Integrity Monitor detected changes:\n{changes}")
    msg['Subject'] = "FIM Alert: File Changes Detected"
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_EMAIL

    with SMTP('smtp.gmail.com',587) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)  # Replace with your SMTP login
        smtp.send_message(msg)
    logging.info("Alert email sent to %s", ALERT_EMAIL)

# Calculate file hash
def calculate_hash(file_path):
    hash_func = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except IOError:
        logging.error("Failed to read file: %s", file_path)
        return None

# Monitor function
def monitor_files():
    hashes = {}

    # Initial scan and hash storage
    for path in MONITOR_PATHS:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)
                if file_hash:
                    hashes[file_path] = file_hash

    logging.info("Initial scan completed.")

    # Continuous monitoring loop
    while True:
        changes = []
        for file_path, old_hash in hashes.items():
            if not os.path.exists(file_path):
                logging.warning("File removed: %s", file_path)
                changes.append(f"Removed: {file_path}")
                continue

            new_hash = calculate_hash(file_path)
            if new_hash != old_hash:
                logging.warning("File modified: %s", file_path)
                changes.append(f"Modified: {file_path}")
                hashes[file_path] = new_hash

        if changes:
            logging.info("Changes detected: %s", changes)
            if ALERT_ON_CHANGE:
                send_email_alert("\n".join(changes))

        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    try:
        logging.info("File Integrity Monitor started.")
        monitor_files()
    except KeyboardInterrupt:
        logging.info("File Integrity Monitor stopped.")
    except Exception as e:
        logging.error("Error in FIM: %s", str(e))
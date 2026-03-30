import os
import time
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "security_logs.txt")
INCIDENT_DIR = os.path.join(BASE_DIR, "incident_reports")

THRESHOLD = 3

BOT_TOKEN = "Replace"
CHAT_ID = "Replace"


def send_telegram(ip, count):

    message = f"ALERT: Brute-force detected from {ip} ({count} failed logins)"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

    print(f"[INFO] Telegram alert sent for {ip}")


def create_report(ip, count):

    os.makedirs(INCIDENT_DIR, exist_ok=True)

    report_file = os.path.join(
        INCIDENT_DIR,
        f"incident_{ip.replace('.', '_')}.txt"
    )

    with open(report_file, "w") as f:
        f.write(f"IP: {ip}\n")
        f.write(f"Failed Attempts: {count}\n")
        f.write("Action: Investigate and block IP\n")

    print(f"[INFO] Report created {report_file}")


def detect_bruteforce():

    logins = {}

    with open(LOG_FILE, "r") as f:

        for line in f:

            line = line.strip()

            if "Failed login" in line:

                ip = line.split("from")[1].strip()

                logins[ip] = logins.get(ip, 0) + 1

    for ip, count in logins.items():

        if count >= THRESHOLD:

            print(f"[ALERT] Brute-force detected {ip}")

            create_report(ip, count)

            send_telegram(ip, count)


def monitor():

    print("SOC monitoring started...")

    seen = set()

    while True:

        with open(LOG_FILE, "r") as f:

            for line in f:

                if line not in seen:

                    seen.add(line)

        detect_bruteforce()

        time.sleep(10)


if __name__ == "__main__":

    monitor()
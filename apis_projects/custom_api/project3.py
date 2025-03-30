import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText

def check_api(url):
    try:
        start_time = time.time()
        response = requests.get(url,timeout=5)
        response_time = time.time() - start_time
        if response.status_code != 200 or response_time > 2:
            send_alert(url, response.status_code, response_time)
    except requests.exceptions.RequestException as e:
        send_alert(url,"Error",str(e))

def send_alert(url,status,details):
    msg = MIMEText(f"API Alert: {url}\nStatus: {status}\nDetails: {details}")
    msg["Subject"] = "API Monitoring Alert"
    msg["From"] = "your_email@example.com"
    msg["To"] = "recipient@example.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")
        server.send_message(msg)

# Schedule monitoring
schedule.every(5).minutes.do(check_api, url="https://api.example.com/health")

while True:
    schedule.run_pending()
    time.sleep(1)
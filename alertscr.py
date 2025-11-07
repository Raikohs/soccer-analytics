import requests
import time

PROM_URL = "http://localhost:9090/api/v1/query"
QUERY = 'weather_temperature_celsius{instance="custom-exporter:8000",job="custom-exporter"}'
#THRESHOLD = 0
CHECK_INTERVAL = 5  

TOKEN = "8197858795:AAHiMOLSjCrffnaaYHq04ua4sL6abBLr8SU"
CHAT_ID = "353628741"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Alert sent:", message)
        else:
            print("Failed to send alert:", response.text)
    except Exception as e:
        print("Error sending alert:", e)

def get_metric(query):
    try:
        response = requests.get(PROM_URL, params={"query": query})
        data = response.json()
        if data["status"] == "success" and data["data"]["result"]:
            return float(data["data"]["result"][0]["value"][1])
    except Exception as e:
        print("Error querying Prometheus:", e)
    return None

while True:
    metric_value = get_metric(QUERY)
    if metric_value is not None:
        print(f"Current temperature in Uralsk: {metric_value}°C")
        send_telegram_alert(f"Current temperature in Uralsk: {metric_value}°C")
    else:
        print("No data from Prometheus")
    time.sleep(CHECK_INTERVAL)

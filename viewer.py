import requests
from datetime import datetime, timedelta

# === ThingSpeak Configuration ===
CHANNEL_ID = "2894331"
READ_API_KEY = "YVUNB7N8DHVU5QZQ"
BASE_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

# === Display Latest Sensor Values ===
def show_latest():
    print("\n=== Latest Sensor Values ===")
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"
    response = requests.get(url)
    data = response.json()

    print(f"Timestamp   : {data['created_at']}")
    print(f"Temperature : {data['field1']} °C")
    print(f"Humidity    : {data['field2']} %")
    print(f"CO2         : {data['field3']} ppm")

# === Display Sensor Data from Last 5 Hours ===
def show_last_5_hours():
    print("\n=== Sensor Values in Last 5 Hours ===")
    # Estimate 4 readings/min * 60 * 5 = 1200
    url = f"{BASE_URL}?api_key={READ_API_KEY}&results=1200"
    response = requests.get(url)
    data = response.json()

    five_hours_ago = datetime.utcnow() - timedelta(hours=5)

    for entry in data['feeds']:
        timestamp = datetime.strptime(entry['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        if timestamp >= five_hours_ago:
            print(f"{timestamp} | Temp: {entry['field1']} °C | Hum: {entry['field2']} % | CO2: {entry['field3']} ppm")

# === Run Viewer ===
if __name__ == "__main__":
    show_latest()
    show_last_5_hours()


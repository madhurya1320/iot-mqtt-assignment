import random
import time
import paho.mqtt.client as mqtt

# ========== ThingSpeak MQTT Configuration ==========
CHANNEL_ID = "2894331"
MQTT_CLIENT_ID = "BTIYFQszGD0FOhwnDCURDwA"       # Your MQTT Device Client ID
MQTT_USERNAME = "BTIYFQszGD0FOhwnDCURDwA"        # Same as Client ID
MQTT_PASSWORD = "t7FVM4fSuGXzLt44de0Y9Chf"        # MQTT Device Password

BROKER = "mqtt3.thingspeak.com"
PORT = 1883
TOPIC = f"channels/{CHANNEL_ID}/publish"

# ========== MQTT Setup ==========
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

# Optional Logging
def on_log(client, userdata, level, buf):
    print("MQTT Log:", buf)

client.on_log = on_log  # ✅ Set before connect()

# Connect to MQTT broker
try:
    client.connect(BROKER, PORT, 60)
    print("[OK] Connected to ThingSpeak MQTT broker")
except Exception as e:
    print("[X] MQTT connection failed:", e)
    exit()

# ========== Virtual Sensor Data Simulation ==========
def generate_sensor_data():
    temperature = round(random.uniform(-50, 50), 2)
    humidity = round(random.uniform(0, 100), 2)
    co2 = round(random.uniform(300, 2000), 2)
    return temperature, humidity, co2

# ========== Publish Loop ==========
while True:
    temp, hum, co2 = generate_sensor_data()
    payload = f"field1={temp}&field2={hum}&field3={co2}"

    result = client.publish(TOPIC, payload)
    status = result[0]

    if status == 0:
        print(f"[OK] Published: {payload}")
    else:
        print(f"[X] Failed to publish: {payload}")

    time.sleep(15)  # ThingSpeak rate limit


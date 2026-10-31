import json
import os
import random
import time

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "battery/device01/raw")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    voltages = [4.12, 4.11, 4.09, 4.10]
    temperatures = [30.0, 31.0, 30.5, 31.5]
    current = 2.5
    try:
        while True:
            voltages = [max(3.70, min(4.20, value + random.uniform(-0.003, 0.003))) for value in voltages]
            temperatures = [max(25.0, min(37.0, value + random.uniform(-0.3, 0.3))) for value in temperatures]
            current = max(1.0, min(5.0, current + random.uniform(-0.20, 0.20)))
            payload = {f"cell{index}_voltage": round(value, 3) for index, value in enumerate(voltages, start=1)}
            payload.update({f"cell{index}_temperature": round(value, 1) for index, value in enumerate(temperatures, start=1)})
            payload["current"] = round(current, 2)
            client.publish(TOPIC, json.dumps(payload), qos=1)
            print(payload)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()

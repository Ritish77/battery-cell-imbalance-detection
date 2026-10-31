import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from battery_analysis import analyze_battery, control_actuators

load_dotenv()
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "battery/device01/raw")
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
INFLUX_ORG = os.getenv("INFLUX_ORG", "my-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "battery_monitor")

influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
writer = influx.write_api(write_options=SYNCHRONOUS)


def make_point(payload: dict) -> Point:
    voltages = [float(payload[f"cell{index}_voltage"]) for index in range(1, 5)]
    temperatures = [float(payload[f"cell{index}_temperature"]) for index in range(1, 5)]
    current = float(payload["current"])
    analysis = analyze_battery(voltages, current, temperatures)
    actuators = control_actuators(analysis)
    point = Point("battery")
    for index, value in enumerate(voltages, start=1):
        point = point.field(f"cell{index}_voltage", value)
    for index, value in enumerate(temperatures, start=1):
        point = point.field(f"cell{index}_temperature", value)
    point = point.field("current", current)
    point = point.field("maximum_voltage", analysis.maximum_voltage)
    point = point.field("minimum_voltage", analysis.minimum_voltage)
    point = point.field("average_voltage", analysis.average_voltage)
    point = point.field("voltage_imbalance", analysis.voltage_imbalance)
    point = point.field("maximum_temperature", analysis.maximum_temperature)
    point = point.field("average_temperature", analysis.average_temperature)
    point = point.field("battery_status", analysis.battery_status)
    point = point.field("imbalance_status", analysis.imbalance_status)
    point = point.field("temperature_status", analysis.temperature_status)
    for name, state in actuators.items():
        point = point.field(f"{name}_state", state)
    return point


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"Connected to {MQTT_BROKER}:{MQTT_PORT}; subscribed to {MQTT_TOPIC}")
    else:
        print(f"MQTT connection failed: {reason_code}")


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        writer.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=make_point(payload))
        print("Stored battery telemetry")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Invalid battery telemetry: {error}")
    except Exception as error:
        print(f"Storage error: {error}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()

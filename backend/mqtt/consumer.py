import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "occupancy/measurements"


def on_connect(client, userdata, flags, reason_code, properties):
    """
    Called when the MQTT client connects to the broker.
    """
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Connection failed: {reason_code}")


def on_message(client, userdata, message):
    """
    Receives an MQTT message, decodes its payload,
    and deserializes the JSON into a Python object.
    """
    try:
        # Step 1: Convert bytes into a UTF-8 string
        payload = message.payload.decode("utf-8")

        # Step 2: Convert JSON string into a Python dictionary
        measurement = json.loads(payload)

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Invalid MQTT payload: {error}")
        return

    print("Measurement received:")
    print(measurement)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Register callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("Waiting for measurements...")

    # Continuously process incoming MQTT messages
    client.loop_forever()


if __name__ == "__main__":
    main()
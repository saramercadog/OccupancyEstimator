import json, os, pydantic, psycopg
from backend.db.measurement_repository import insert_measurement
from backend.db.room_repository import get_active_room_id
from backend.api.schemas import IncomingMeasurement
import paho.mqtt.client as mqtt

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
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
    Receives an MQTT message, deserializes its JSON payload,
    and stores the measurement in PostgreSQL.
    """
    try:
        # Step 1: Decode bytes into a UTF-8 string
        payload = message.payload.decode("utf-8")

        # Step 2: Deserialize JSON into a Python dictionary + validate with Pydantic
        measurement = IncomingMeasurement.model_validate(json.loads(payload)).model_dump()

    except (UnicodeDecodeError, json.JSONDecodeError, pydantic.ValidationError) as error:
        print(f"Invalid MQTT payload: {error}")
        return

    try:
        # Step 2.1: Get the active room ID
        room_id = get_active_room_id()
        if room_id is None:
            print("No active room configured. Measurement not stored.")
            return

        # Step 3: Insert measurement into PostgreSQL
        inserted = insert_measurement(measurement, room_id)

        if inserted:
            print("Measurement successfully stored for room ID:", room_id)
        else:
            print("Duplicate measurement ignored.")

    except (KeyError, TypeError, ValueError, psycopg.Error) as error:
        print(f"Failed to store measurement: {error}")


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
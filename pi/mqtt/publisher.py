
import json
import os
import paho.mqtt.client as mqtt
from dataclasses import asdict
from pi.processing.measurement import Measurement


BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = "occupancy/measurements"


def publish_measurement(measurement: Measurement) -> None:
    """
    Publishes an aggregated occupancy measurement to the MQTT broker.

    Raises an exception if publishing fails.
    """

    payload = json.dumps(asdict(measurement))

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    try:
        client.connect(BROKER_HOST, BROKER_PORT)

        client.loop_start()

        message = client.publish(
            topic=TOPIC,
            payload=payload,
            qos=1
        )

        if message.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                f"MQTT publish failed: {mqtt.error_string(message.rc)}"
            )
        
        message.wait_for_publish(timeout=10)
        
        if not message.is_published():
            raise TimeoutError("MQTT publish timed out")

    finally:
        client.disconnect()
        client.loop_stop()

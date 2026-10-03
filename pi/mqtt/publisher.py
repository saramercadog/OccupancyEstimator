import json
from dataclasses import asdict

import paho.mqtt.client as mqtt

from pi.processing.measurement import Measurement


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "occupancy/measurements"


def publish_measurement(measurement: Measurement) -> None:
    """
    Publishes an aggregated occupancy measurement to the MQTT broker.
    """

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )

    client.connect(BROKER_HOST, BROKER_PORT)

    payload = json.dumps(asdict(measurement))

    client.publish(
        TOPIC,
        payload
    )

    client.disconnect()
from pi.mqtt.publisher import publish_measurement
from pi.processing.measurement import Measurement

'''
Verifies that a Measurement object can be serialized and published
from the Raspberry Pi to the Mosquitto broker running on the Mac.

Unlike unit tests, this test uses a real MQTT connection instead of
mocking the MQTT client. It requires an active broker and network
connection. Successful delivery can be verified using an MQTT subscriber.
'''

def main():
    measurement = Measurement(
        start_cycle_id=1,
        end_cycle_id=10,
        timestamp=1234567890.0,
        total_probes=100,
        unique_mac_addresses=50,
        unique_mac_2plus=20,
        unique_mac_3plus=10,
        probes_rssi_80=80
    )

    publish_measurement(measurement)

    print("Measurement published successfully!")


if __name__ == "__main__":
    main()

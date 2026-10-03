import json
from unittest.mock import patch

from pi.mqtt.publisher import publish_measurement
from pi.processing.measurement import Measurement


@patch("pi.mqtt.publisher.mqtt.Client")
def test_publish_measurement(mock_client_class):
    mock_client = mock_client_class.return_value

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

    mock_client.connect.assert_called_once_with(
        "localhost",
        1883
    )

    mock_client.publish.assert_called_once()

    topic, payload = mock_client.publish.call_args.args

    assert topic == "occupancy/measurements"

    data = json.loads(payload)

    assert data["start_cycle_id"] == 1
    assert data["end_cycle_id"] == 10
    assert data["total_probes"] == 100
    assert data["unique_mac_addresses"] == 50
    assert data["unique_mac_2plus"] == 20
    assert data["unique_mac_3plus"] == 10
    assert data["probes_rssi_80"] == 80

    mock_client.disconnect.assert_called_once()
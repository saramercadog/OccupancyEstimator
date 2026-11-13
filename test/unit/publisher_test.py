
import json
import pytest
from unittest.mock import patch
import paho.mqtt.client as mqtt
from pi.mqtt.publisher import (
    publish_measurement,
    BROKER_HOST,
    BROKER_PORT,
    TOPIC
)
from pi.processing.measurement import Measurement

@pytest.fixture
def measurement():
    return Measurement(
        start_cycle_id=1,
        end_cycle_id=10,
        timestamp=1234567890.0,
        total_probes=100,
        unique_mac_addresses=50,
        unique_mac_2plus=20,
        unique_mac_3plus=10,
        probes_rssi_75=90,
        probes_rssi_80=80
    )

@patch("pi.mqtt.publisher.mqtt.Client")
def test_publish_measurement(mock_client_class):
    mock_client = mock_client_class.return_value

    # Simulate a successful MQTT publication
    mock_message = mock_client.publish.return_value
    mock_message.is_published.return_value = True
    mock_message.rc = mqtt.MQTT_ERR_SUCCESS

    measurement = Measurement(
        start_cycle_id=1,
        end_cycle_id=10,
        timestamp=1234567890.0,
        total_probes=100,
        unique_mac_addresses=50,
        unique_mac_2plus=20,
        unique_mac_3plus=10,
        probes_rssi_75 = 90,
        probes_rssi_80=80
    )

    publish_measurement(measurement)

    mock_client.connect.assert_called_once_with(
        BROKER_HOST,
        BROKER_PORT
    )

    mock_client.loop_start.assert_called_once()

    mock_client.publish.assert_called_once_with(
        topic=TOPIC,
        payload=json.dumps(measurement.__dict__),
        qos=1
    )

    mock_message.wait_for_publish.assert_called_once_with(
        timeout=10
    )

    mock_message.is_published.assert_called_once()

    mock_client.disconnect.assert_called_once()
    mock_client.loop_stop.assert_called_once()

@patch("pi.mqtt.publisher.mqtt.Client")
def test_publish_failure(mock_client_class, measurement):
    mock_client = mock_client_class.return_value

    mock_message = mock_client.publish.return_value
    mock_message.rc = mqtt.MQTT_ERR_NO_CONN

    with pytest.raises(RuntimeError, match="MQTT publish failed"):
        publish_measurement(measurement)

    mock_message.wait_for_publish.assert_not_called()
    mock_client.disconnect.assert_called_once()
    mock_client.loop_stop.assert_called_once()
    
@patch("pi.mqtt.publisher.mqtt.Client")
def test_publish_timeout(mock_client_class, measurement):
    mock_client = mock_client_class.return_value

    mock_message = mock_client.publish.return_value
    mock_message.rc = mqtt.MQTT_ERR_SUCCESS
    mock_message.is_published.return_value = False

    with pytest.raises(TimeoutError, match="MQTT publish timed out"):
        publish_measurement(measurement)

    mock_message.wait_for_publish.assert_called_once_with(
        timeout=10
    )

    mock_client.disconnect.assert_called_once()
    mock_client.loop_stop.assert_called_once()
    
@patch("pi.mqtt.publisher.mqtt.Client")
def test_network_loop_failure(mock_client_class, measurement):
    mock_client = mock_client_class.return_value

    mock_client.loop_start.side_effect = RuntimeError(
        "Network loop failed"
    )

    with pytest.raises(RuntimeError, match="Network loop failed"):
        publish_measurement(measurement)

    mock_client.publish.assert_not_called()
    mock_client.disconnect.assert_called_once()
    mock_client.loop_stop.assert_called_once()
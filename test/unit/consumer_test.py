import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from backend.mqtt.consumer import on_message


@pytest.fixture
def valid_measurement():
    return {
        "start_cycle_id": 1,
        "end_cycle_id": 10,
        "timestamp": 1234567890.0,
        "total_probes": 100,
        "unique_mac_addresses": 50,
        "unique_mac_2plus": 20,
        "unique_mac_3plus": 10,
        "probes_rssi_75": 60,
        "probes_rssi_80": 80,
    }


def make_message(payload):
    return SimpleNamespace(
        payload=json.dumps(payload).encode("utf-8")
    )


@patch("backend.mqtt.consumer.insert_measurement")
@patch("backend.mqtt.consumer.get_active_room_id")
def test_valid_measurement(
    mock_get_room,
    mock_insert,
    valid_measurement
):
    mock_get_room.return_value = 1
    mock_insert.return_value = True

    on_message(None, None, make_message(valid_measurement))

    mock_insert.assert_called_once_with(
        valid_measurement, 1
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("total_probes", -5),
        ("start_cycle_id", 20),
        ("unique_mac_addresses", 200),
        ("probes_rssi_75", 90),
        ("total_probes", "invalid"),
    ]
)
@patch("backend.mqtt.consumer.insert_measurement")
def test_invalid_measurements(
    mock_insert,
    field,
    value,
    valid_measurement
):
    invalid = valid_measurement.copy()
    invalid[field] = value

    on_message(None, None, make_message(invalid))

    mock_insert.assert_not_called()


@patch("backend.mqtt.consumer.insert_measurement")
def test_missing_field(mock_insert, valid_measurement):
    del valid_measurement["total_probes"]

    on_message(None, None, make_message(valid_measurement))

    mock_insert.assert_not_called()


@patch("backend.mqtt.consumer.insert_measurement")
def test_invalid_json(mock_insert):
    message = SimpleNamespace(payload=b"{invalid json}")

    on_message(None, None, message)

    mock_insert.assert_not_called()
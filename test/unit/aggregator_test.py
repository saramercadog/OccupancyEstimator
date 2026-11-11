import pytest
from pathlib import Path
import pandas as pd
from pi.processing.aggregator import aggregate_observations

PROJECT_ROOT = Path(__file__).resolve().parents[2]

@pytest.fixture
def aggregated_data():
    path = PROJECT_ROOT / "data" / "processed" / "aggregated_data.pkl"
    return pd.read_pickle(path)

@pytest.mark.parametrize("window_id", [1, 2, 10, 50, 100, 144])
def test_aggregate_observations(aggregated_data, window_id):
    expected = aggregated_data.loc[window_id]

    start = (window_id - 1) * 10 + 1
    end = window_id * 10

    actual = aggregate_observations(start, end)

    assert actual is not None

    assert actual.start_cycle_id == start
    assert actual.end_cycle_id == end

    assert actual.total_probes == expected["total_probes"]
    assert actual.unique_mac_addresses == expected["unique_mac_addresses"]
    assert actual.unique_mac_2plus == expected["unique_mac_2plus"]
    assert actual.unique_mac_3plus == expected["unique_mac_3plus"]
    assert actual.probes_rssi_75 == expected["probes_rssi_75"]
    assert actual.probes_rssi_80 == expected["probes_rssi_80"]
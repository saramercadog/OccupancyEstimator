from dataclasses import dataclass

@dataclass
class Measurement:
    start_cycle_id: int
    end_cycle_id: int
    timestamp: float

    total_probes: int
    unique_mac_addresses: int
    unique_mac_2plus: int
    unique_mac_3plus: int
    probes_rssi_80: int
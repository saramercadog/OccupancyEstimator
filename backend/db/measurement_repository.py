from datetime import datetime, timezone

from backend.db.database import get_connection


def insert_measurement(measurement: dict, room_id: int) -> bool:
    sql = """
        INSERT INTO measurements (
            room_id,
            start_cycle_id,
            end_cycle_id,
            timestamp,
            total_probes,
            unique_mac_addresses,
            unique_mac_2plus,
            unique_mac_3plus,
            probes_rssi_75,
            probes_rssi_80
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (start_cycle_id, end_cycle_id) DO NOTHING
        RETURNING id;
    """

    values = (
        room_id,
        measurement["start_cycle_id"],
        measurement["end_cycle_id"],
        datetime.fromtimestamp(measurement["timestamp"], tz=timezone.utc),
        measurement["total_probes"],
        measurement["unique_mac_addresses"],
        measurement["unique_mac_2plus"],
        measurement["unique_mac_3plus"],
        measurement["probes_rssi_75"],
        measurement["probes_rssi_80"],
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            inserted_row = cursor.fetchone()

    return inserted_row is not None
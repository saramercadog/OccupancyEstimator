import sqlite3

import pi.capture.config as config
from pi.processing.measurement import Measurement


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(config.DB_PATH)


def aggregate_observations(start: int, end: int) -> Measurement | None:
    """
    Aggregates raw probe observations between start and end scan cycles
    into the features required by the occupancy model.
    """

    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            WITH mac_counts AS (
                SELECT
                    (scan_cycle_id - 1) / 10 + 1 AS window_id,
                    mac_address,
                    COUNT(*) AS times_seen
                FROM probes
                WHERE scan_cycle_id BETWEEN ? AND ?
                GROUP BY mac_address
            )

            SELECT
                MIN(scan_cycle_id) AS start_cycle_id,
                MAX(scan_cycle_id) AS end_cycle_id,
                MAX(timestamp) AS timestamp,
                COUNT(*) AS total_probes,
                COUNT(DISTINCT mac_address) AS unique_mac_addresses,

                (
                    SELECT COUNT(*)
                    FROM mac_counts
                    WHERE times_seen >= 2
                ) AS unique_mac_2plus,

                (
                    SELECT COUNT(*)
                    FROM mac_counts
                    WHERE times_seen >= 3
                ) AS unique_mac_3plus,

                COUNT(
                    CASE WHEN rssi >= -80 THEN 1 END
                ) AS probes_rssi_80

            FROM probes
            WHERE scan_cycle_id BETWEEN ? AND ?
            """,
            (start, end, start, end)
        )

        result = cursor.fetchone()

        if result is None or result[0] is None:
            return None

        return Measurement(
            start_cycle_id=result[0],
            end_cycle_id=result[1],
            timestamp=result[2],
            total_probes=result[3],
            unique_mac_addresses=result[4],
            unique_mac_2plus=result[5],
            unique_mac_3plus=result[6],
            probes_rssi_80=result[7]
        )

    finally:
        conn.close()
import sqlite3
from typing import List
import config
from capture import Observation

def get_connection() -> sqlite3.Connection:
    """
    Returns a connection to the SQLite database, creating tables if they don't exist
    """
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS probes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_cycle_id INTEGER NOT NULL,
            timestamp REAL NOT NULL,
            mac_address TEXT NOT NULL,
            rssi INTEGER,
            channel_freq INTEGER
        )
    """)
    
    conn.execute("CREATE INDEX IF NOT EXISTS idx_probes_cycle ON probes(scan_cycle_id)")
    return conn

def insert_observations (ID: int, observations: List[Observation]):
    """
    Inserts captured probe requests into SQLite
    """
    try: 
        conn = get_connection()
        
        data = []

        for obs in observations:
            data.append((
                    ID,
                    obs.timestamp,
                    obs.src_mac,
                    obs.rssi,
                    obs.channel_freq
                    ))
            
        conn.executemany(
                """
                INSERT INTO probes
                (
                    scan_cycle_id,
                    timestamp,
                    mac_address,
                    rssi,
                    channel_freq
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                data
            )

        conn.commit()
    finally:
        conn.close()
    

def get_current_probes(scan_cycle_id: int):
    """
    Overwrites probes_current.csv with current probe data found in scan cycle
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT *
            FROM probes
            WHERE scan_cycle_id = ?
            """,
            (scan_cycle_id,)
        )

        return cursor.fetchall()

    finally:
        conn.close()
        
def get_next_cycle_id() -> int:
    """
    Returns the next scan cycle ID based on the latest one stored in the probes table
    """
    conn = get_connection()

    try:
        result = conn.execute(
            "SELECT MAX(scan_cycle_id) FROM probes"
        ).fetchone()

        max_id = result[0]

        return 1 if max_id is None else max_id + 1

    finally:
        conn.close()
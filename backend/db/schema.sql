CREATE TABLE rooms(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0),
    is_active BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX one_active_room
ON rooms (is_active)
WHERE is_active = TRUE;

CREATE TABLE measurements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    room_id BIGINT NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT,

    start_cycle_id BIGINT NOT NULL,
    end_cycle_id BIGINT NOT NULL,

    timestamp TIMESTAMPTZ NOT NULL,

    total_probes INTEGER NOT NULL,
    unique_mac_addresses INTEGER NOT NULL,
    unique_mac_2plus INTEGER NOT NULL,
    unique_mac_3plus INTEGER NOT NULL,
    probes_rssi_75 INTEGER NOT NULL,
    probes_rssi_80 INTEGER NOT NULL,

    CONSTRAINT valid_cycle_range
        CHECK (end_cycle_id >= start_cycle_id),

    CONSTRAINT nonnegative_counts
        CHECK (
            total_probes >= 0
            AND unique_mac_addresses >= 0
            AND unique_mac_2plus >= 0
            AND unique_mac_3plus >= 0
            AND probes_rssi_75 >= 0
            AND probes_rssi_80 >= 0
        )
        CONSTRAINT unique_measurement_window 
            UNIQUE (start_cycle_id, end_cycle_id)
);
CREATE TABLE measurements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    start_cycle_id BIGINT NOT NULL,
    end_cycle_id BIGINT NOT NULL,

    timestamp TIMESTAMPTZ NOT NULL,

    total_probes INTEGER NOT NULL,
    unique_mac_addresses INTEGER NOT NULL,
    unique_mac_2plus INTEGER NOT NULL,
    unique_mac_3plus INTEGER NOT NULL,
    probes_rssi_80 INTEGER NOT NULL,

    CONSTRAINT valid_cycle_range
        CHECK (end_cycle_id >= start_cycle_id),

    CONSTRAINT nonnegative_counts
        CHECK (
            total_probes >= 0
            AND unique_mac_addresses >= 0
            AND unique_mac_2plus >= 0
            AND unique_mac_3plus >= 0
            AND probes_rssi_80 >= 0
        )
);

import pytest

from pi.capture import config, logger


@pytest.fixture
def temporary_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_occupancy.db"
    monkeypatch.setattr(config, "DB_PATH", db_path)
    return db_path


def test_empty_database_starts_at_cycle_one(temporary_db):
    assert logger.get_next_cycle_id() == 1


def test_empty_cycle_is_remembered(temporary_db):
    logger.record_completed_cycle(1)

    assert logger.get_next_cycle_id() == 2


def test_multiple_empty_cycles_are_remembered(temporary_db):
    logger.record_completed_cycle(1)
    logger.record_completed_cycle(2)
    logger.record_completed_cycle(3)

    assert logger.get_next_cycle_id() == 4


def test_existing_probe_ids_are_preserved(temporary_db):
    with logger.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO probes
                (scan_cycle_id, timestamp, mac_address)
            VALUES (?, ?, ?)
            """,
            (15, 1000.0, "hashed-device")
        )

    assert logger.get_next_cycle_id() == 16


import pytest

from backend.db.database import get_connection
from backend.db.prediction_repository import insert_prediction


@pytest.fixture
def measurement_id():
    """
    Find a measurement that does not already have a prediction.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.id
                FROM measurements m
                LEFT JOIN predictions p
                    ON p.measurement_id = m.id
                WHERE p.id IS NULL
                ORDER BY m.id DESC
                LIMIT 1;
            """)

            row = cursor.fetchone()

    if row is None:
        pytest.skip("No measurement available for testing")

    yield row[0]

    # Clean up the prediction created during the test.
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM predictions WHERE measurement_id = %s",
                (row[0],)
            )


def test_insert_prediction(measurement_id):
    prediction_id = insert_prediction(
        measurement_id=measurement_id,
        estimated_people=7,
        model_version="gb_people_v1"
    )

    assert prediction_id is not None

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT measurement_id, estimated_people, model_version
                FROM predictions
                WHERE id = %s;
                """,
                (prediction_id,)
            )

            row = cursor.fetchone()

    assert row == (measurement_id, 7, "gb_people_v1")


def test_duplicate_prediction(measurement_id):
    first_id = insert_prediction(
        measurement_id=measurement_id,
        estimated_people=7,
        model_version="gb_people_v1"
    )

    second_id = insert_prediction(
        measurement_id=measurement_id,
        estimated_people=7,
        model_version="gb_people_v1"
    )

    assert first_id is not None
    assert second_id is None

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM predictions
                WHERE measurement_id = %s;
                """,
                (measurement_id,)
            )

            count = cursor.fetchone()[0]

    assert count == 1

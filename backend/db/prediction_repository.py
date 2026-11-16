from backend.db.database import get_connection


def insert_prediction(measurement_id: int, estimated_people: int, model_version: str) -> int | None:

    sql = """
        INSERT INTO predictions (
            measurement_id,
            estimated_people,
            model_version
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (measurement_id) DO NOTHING
        RETURNING id;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    measurement_id,
                    estimated_people,
                    model_version
                )
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return row[0]
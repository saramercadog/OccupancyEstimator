from backend.db.database import get_connection


def get_active_room_id() -> int | None:
    sql = """
        SELECT id
        FROM rooms
        WHERE is_active = TRUE;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()

    if result is None:
        return None

    return result[0]
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

def get_rooms_db() -> list[dict]:
    sql = """
        SELECT id, name, max_capacity, is_active
        FROM rooms
        ORDER BY id;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    rooms = []

    for row in rows:
        room = {
            "id": row[0],
            "name": row[1],
            "max_capacity": row[2],
            "is_active": row[3]
        }

        rooms.append(room)

    return rooms

def create_room_db(name: str, max_capacity: int) -> dict:
    sql = """
        INSERT INTO rooms (name, max_capacity)
        VALUES (%s, %s)
        RETURNING id, name, max_capacity, is_active;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, max_capacity))
            row = cursor.fetchone()

    room = {
        "id": row[0],
        "name": row[1],
        "max_capacity": row[2],
        "is_active": row[3]
    }

    return room

def activate_room_db(room_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM rooms
                WHERE id = %s;
                """,
                (room_id,)
            )

            if cursor.fetchone() is None:
                return None

            cursor.execute(
                """
                UPDATE rooms
                SET is_active = FALSE
                WHERE is_active = TRUE;
                """
            )

            cursor.execute(
                """
                UPDATE rooms
                SET is_active = TRUE
                WHERE id = %s
                RETURNING id, name, max_capacity, is_active;
                """,
                (room_id,)
            )

            row = cursor.fetchone()

    return {
        "id": row[0],
        "name": row[1],
        "max_capacity": row[2],
        "is_active": row[3]
    }
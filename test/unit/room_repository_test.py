import pytest
from unittest.mock import patch

from backend.db.room_repository import (
    get_active_room_id,
    get_rooms_db,
    create_room_db,
    activate_room_db,
)


@pytest.fixture
def mock_cursor():
    with patch(
        "backend.db.room_repository.get_connection"
    ) as mock_get_connection:

        mock_conn = mock_get_connection.return_value.__enter__.return_value
        cursor = mock_conn.cursor.return_value.__enter__.return_value

        yield cursor
        
def test_create_room(mock_cursor):
    mock_cursor.fetchone.return_value = (
        1, "Library", 50, False
    )

    result = create_room_db("Library", 50)

    assert result == {
        "id": 1,
        "name": "Library",
        "max_capacity": 50,
        "is_active": False,
    }

    mock_cursor.execute.assert_called_once()

    args, kwargs = mock_cursor.execute.call_args

    assert "INSERT INTO rooms" in args[0]
    assert args[1] == ("Library", 50)
    

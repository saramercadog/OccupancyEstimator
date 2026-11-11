from fastapi import FastAPI, HTTPException
from backend.db.room_repository import get_rooms_db, create_room_db, activate_room_db
from backend.api.schemas import RoomCreate, RoomResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Occupancy API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/rooms", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate):
    created_room = create_room_db(room.name, room.max_capacity)
    return created_room

@app.get("/rooms", response_model=list[RoomResponse])
def get_rooms():
    return get_rooms_db()

@app.put("/rooms/{room_id}/activate", response_model=RoomResponse)
def activate_room(room_id: int):
    room = activate_room_db(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

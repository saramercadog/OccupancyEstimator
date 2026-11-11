from pydantic import BaseModel, Field, field_validator


class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    max_capacity: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Room name cannot be empty")

        return value

class RoomResponse(BaseModel):
    id: int
    name: str
    max_capacity: int
    is_active: bool
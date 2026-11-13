from pydantic import BaseModel, Field, field_validator, BaseModel, Field, ConfigDict, model_validator

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

class IncomingMeasurement(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    start_cycle_id: int = Field(ge=1)
    end_cycle_id: int = Field(ge=1)
    timestamp: float = Field(ge=0, allow_inf_nan=False)

    total_probes: int = Field(ge=0)
    unique_mac_addresses: int = Field(ge=0)
    unique_mac_2plus: int = Field(ge=0)
    unique_mac_3plus: int = Field(ge=0)

    probes_rssi_75: int = Field(ge=0)
    probes_rssi_80: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_consistency(self):
        if self.end_cycle_id < self.start_cycle_id:
            raise ValueError("Invalid cycle range")

        if not (
            self.unique_mac_3plus
            <= self.unique_mac_2plus
            <= self.unique_mac_addresses
            <= self.total_probes
        ):
            raise ValueError("Inconsistent MAC counts")

        if not (
            self.probes_rssi_75
            <= self.probes_rssi_80
            <= self.total_probes
        ):
            raise ValueError("Inconsistent RSSI counts")

        return self

class RoomResponse(BaseModel):
    id: int
    name: str
    max_capacity: int
    is_active: bool
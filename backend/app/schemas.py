from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=120)
    astronaut_code: str = Field(min_length=2, max_length=40)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeasurementCreate(BaseModel):
    mission_id: str
    metric_type: str = Field(min_length=1, max_length=60)
    value: float
    unit: str = Field(min_length=1, max_length=30)
    measured_at: datetime | None = None
    measurement_source: str = "manual"
    is_simulated: bool = False
    notes: str | None = None


class MeasurementResponse(MeasurementCreate):
    id: str
    quality_status: str
    model_config = ConfigDict(from_attributes=True)


class MissionCreate(BaseModel):
    mission_name: str = Field(min_length=1, max_length=160)
    mission_type: str = Field(min_length=1, max_length=80)
    mission_day: int = Field(default=0, ge=0)


class MissionResponse(MissionCreate):
    id: str
    status: str
    model_config = ConfigDict(from_attributes=True)


class AnalysisResponse(BaseModel):
    level: str
    reason: str
    confidence: str
    threshold_status: str


class ProfileResponse(BaseModel):
    id: str
    display_name: str
    astronaut_code: str
    model_config = ConfigDict(from_attributes=True)

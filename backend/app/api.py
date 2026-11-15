from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .core.database import get_db
from .core.security import create_access_token, decode_subject, hash_password, verify_password
from .models import AstronautProfile, HealthMeasurement, Mission, User
from .schemas import AnalysisResponse, LoginRequest, MeasurementCreate, MeasurementResponse, MissionCreate, MissionResponse, ProfileResponse, RegisterRequest, TokenResponse
from .services import analyze, baseline, validate_measurement

router = APIRouter(prefix="/api/v1")
Db = Annotated[Session, Depends(get_db)]


def current_user(db: Db, authorization: str | None = Header(default=None)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    try:
        subject = decode_subject(authorization[7:])
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    user = db.get(User, subject)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is not active")
    return user


@router.post("/auth/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Db):
    if db.scalar(select(User).where(User.email == payload.email.lower())):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password))
    user.astronaut = AstronautProfile(display_name=payload.display_name, astronaut_code=payload.astronaut_code)
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.id))


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Db):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/auth/me", response_model=ProfileResponse)
def me(user: User = Depends(current_user)):
    if not user.astronaut:
        raise HTTPException(status_code=404, detail="Astronaut profile not found")
    return user.astronaut


@router.post("/missions", response_model=MissionResponse, status_code=201)
def create_mission(payload: MissionCreate, db: Db, user: User = Depends(current_user)):
    if not user.astronaut:
        raise HTTPException(status_code=404, detail="Astronaut profile not found")
    mission = Mission(astronaut_id=user.astronaut.id, **payload.model_dump())
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.get("/missions", response_model=list[MissionResponse])
def list_missions(db: Db, user: User = Depends(current_user)):
    if not user.astronaut:
        return []
    return list(db.scalars(select(Mission).where(Mission.astronaut_id == user.astronaut.id).order_by(Mission.mission_day.desc())))


@router.post("/health/measurements", response_model=MeasurementResponse, status_code=201)
def create_measurement(payload: MeasurementCreate, db: Db, user: User = Depends(current_user)):
    if not user.astronaut or not db.scalar(select(Mission).where(Mission.id == payload.mission_id, Mission.astronaut_id == user.astronaut.id)):
        raise HTTPException(status_code=404, detail="Mission not found")
    try:
        quality = validate_measurement(payload.metric_type, payload.value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    measurement = HealthMeasurement(astronaut_id=user.astronaut.id, quality_status=quality, **payload.model_dump(exclude_none=True))
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement


@router.get("/health/measurements", response_model=list[MeasurementResponse])
def list_measurements(db: Db, user: User = Depends(current_user)):
    if not user.astronaut:
        return []
    return list(db.scalars(select(HealthMeasurement).where(HealthMeasurement.astronaut_id == user.astronaut.id).order_by(HealthMeasurement.measured_at.desc()).limit(200)))


@router.post("/risk/analyze", response_model=AnalysisResponse)
def analyze_risk(metric_type: str, value: float, db: Db, user: User = Depends(current_user)):
    if not user.astronaut:
        raise HTTPException(status_code=404, detail="Astronaut profile not found")
    return analyze(value, baseline(db, user.astronaut.id, metric_type))

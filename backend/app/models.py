from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    astronaut: Mapped["AstronautProfile | None"] = relationship(back_populates="user", uselist=False)


class AstronautProfile(Base):
    __tablename__ = "astronaut_profiles"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    display_name: Mapped[str] = mapped_column(String(120))
    astronaut_code: Mapped[str] = mapped_column(String(40), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    user: Mapped[User] = relationship(back_populates="astronaut")
    missions: Mapped[list["Mission"]] = relationship(back_populates="astronaut")


class Mission(Base):
    __tablename__ = "missions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    mission_name: Mapped[str] = mapped_column(String(160))
    mission_type: Mapped[str] = mapped_column(String(80))
    mission_day: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="active")
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    astronaut: Mapped[AstronautProfile] = relationship(back_populates="missions")
    measurements: Mapped[list["HealthMeasurement"]] = relationship(back_populates="mission")


class HealthMeasurement(Base):
    __tablename__ = "health_measurements"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True)
    metric_type: Mapped[str] = mapped_column(String(60), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(30))
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)
    measurement_source: Mapped[str] = mapped_column(String(60), default="manual")
    quality_status: Mapped[str] = mapped_column(String(30), default="unreviewed")
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    mission: Mapped[Mission] = relationship(back_populates="measurements")
    __table_args__ = (Index("ix_measurement_owner_time", "astronaut_id", "measured_at"),)


class HealthAlert(Base):
    __tablename__ = "health_alerts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id"), index=True)
    severity: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(180))
    explanation: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

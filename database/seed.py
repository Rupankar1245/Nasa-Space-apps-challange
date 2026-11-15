"""Seed the API database with a reproducible synthetic mission."""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.models import AstronautProfile, HealthMeasurement, Mission, User  # noqa: E402

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    user = db.query(User).filter_by(email="demo@crewpulse.local").first()
    if not user:
        user = User(email="demo@crewpulse.local", password_hash=hash_password("demo-password"))
        user.astronaut = AstronautProfile(display_name="Demo Astronaut", astronaut_code="CP-001")
        db.add(user)
        db.flush()
    mission = db.query(Mission).filter_by(astronaut_id=user.astronaut.id).first()
    if not mission:
        mission = Mission(astronaut_id=user.astronaut.id, mission_name="Mars Exploration Simulation", mission_type="simulation", mission_day=120)
        db.add(mission)
        db.flush()
    if not db.query(HealthMeasurement).filter_by(mission_id=mission.id).first():
        for day in range(30):
            db.add(HealthMeasurement(
                astronaut_id=user.astronaut.id, mission_id=mission.id, metric_type="heart_rate",
                value=68 + (day % 5), unit="BPM", measured_at=datetime.now(timezone.utc), quality_status="valid",
                measurement_source="seed", is_simulated=True, notes="Reproducible synthetic demo record"
            ))
    db.commit()
finally:
    db.close()

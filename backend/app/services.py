from statistics import median

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import HealthMeasurement


def validate_measurement(metric_type: str, value: float) -> str:
    if not value == value or value in (float("inf"), float("-inf")):
        raise ValueError("Measurement must be finite")
    if metric_type in {"heart_rate", "systolic_bp", "diastolic_bp"} and not 0 < value < 400:
        raise ValueError("Cardiovascular measurement is outside the accepted input range")
    if metric_type == "spo2" and not 0 < value <= 100:
        raise ValueError("SpO2 must be between 0 and 100")
    if metric_type == "sleep_duration" and not 0 <= value <= 24:
        raise ValueError("Sleep duration must be between 0 and 24 hours")
    return "valid"


def baseline(db: Session, astronaut_id: str, metric_type: str) -> dict[str, float | int | bool]:
    values = db.scalars(select(HealthMeasurement.value).where(
        HealthMeasurement.astronaut_id == astronaut_id,
        HealthMeasurement.metric_type == metric_type,
        HealthMeasurement.quality_status == "valid",
    )).all()
    if len(values) < 5:
        return {"sufficient": False, "sample_size": len(values)}
    return {"sufficient": True, "sample_size": len(values), "median": median(values)}


def analyze(value: float, reference: dict[str, float | int | bool]) -> dict[str, str]:
    if not reference["sufficient"]:
        return {"level": "AMBER", "reason": "Insufficient personal history for a baseline comparison.", "confidence": "insufficient", "threshold_status": "clinical threshold not configured"}
    deviation = abs(value - float(reference["median"])) / float(reference["median"])
    level = "AMBER" if deviation > 0.15 else "GREEN"
    reason = "Measurement deviates from the personal baseline; reassess context." if level == "AMBER" else "No concerning deviation from the personal baseline detected."
    return {"level": level, "reason": reason, "confidence": "moderate", "threshold_status": "clinical threshold not configured"}

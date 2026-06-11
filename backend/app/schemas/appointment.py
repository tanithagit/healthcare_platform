from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class AppointmentStatusEnum(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: datetime
    reason: Optional[str] = None


class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatusEnum] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    reason: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    doctor_email: Optional[str] = None
    patient_email: Optional[str] = None
    consultation_fee: Optional[float] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MedicalRecordCreate(BaseModel):
    appointment_id: int
    diagnosis: str
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    diagnosis: str
    notes: Optional[str] = None
    created_at: datetime
    doctor_email: Optional[str] = None
    patient_email: Optional[str] = None

    class Config:
        from_attributes = True
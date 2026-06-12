from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PrescriptionCreate(BaseModel):
    appointment_id: int
    medicine_name: str
    dosage: str
    instructions: Optional[str] = None
    duration_days: Optional[int] = None


class PrescriptionBulkCreate(BaseModel):
    appointment_id: int
    prescriptions: List[PrescriptionCreate]


class PrescriptionUpdate(BaseModel):
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    instructions: Optional[str] = None
    duration_days: Optional[int] = None


class PrescriptionResponse(BaseModel):
    id: int
    appointment_id: int
    medical_record_id: Optional[int] = None
    medicine_name: str
    dosage: str
    instructions: Optional[str] = None
    duration_days: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
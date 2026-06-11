from pydantic import BaseModel
from typing import Optional
from datetime import date


class PatientProfileUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None


class PatientProfileResponse(BaseModel):
    id: int
    user_id: int
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
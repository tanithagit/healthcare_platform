from pydantic import BaseModel
from typing import Optional


class DoctorProfileUpdate(BaseModel):
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    qualification: Optional[str] = None
    bio: Optional[str] = None
    available_days: Optional[str] = None
    available_start_time: Optional[str] = None
    available_end_time: Optional[str] = None


class DoctorProfileResponse(BaseModel):
    id: int
    user_id: int
    specialization: str
    experience_years: int
    consultation_fee: float
    qualification: Optional[str] = None
    bio: Optional[str] = None
    available_days: Optional[str] = None
    available_start_time: Optional[str] =None
    available_end_time: Optional[str] =None
    email: Optional[str] = None

    class Config:
        from_attributes = True

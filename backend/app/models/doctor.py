from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DoctorProfile(Base):
    __tablename__="doctor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String, nullable=False)
    experience_years = Column(Integer, default=0)
    consultation_fee = Column(Float, nullable=False)
    qualification = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    available_days = Column(String, default="Monday,Tuesday,Wednesday,Thursday,Friday")
    available_start_time = Column(String, default="09:00")
    available_end_time = Column(String, default="17:00")


    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")
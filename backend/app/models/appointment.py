from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class AppointmentStatus(str, enum.Enum):
    scheduled ="scheduled"
    sompleted = "completed"
    canceled = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id= Column(Integer, ForeignKey("patient_profiles.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id"),nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    reason = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    patient = relationship("PatientProfile", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False)
    prescriptions = relationship("Prescription", back_populates="appointment")
    invoice = relationship("Invoice", back_populates="appointment", uselist=False)


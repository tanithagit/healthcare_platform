from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"


    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=True)
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    instructions = Column(String, nullable=True)
    duration_days = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    appointment = relationship("Appointment", back_populates="prescriptions")
    medical_record = relationship("MedicalRecord", back_populates="prescriptions")

    
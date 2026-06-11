from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed ="failed"
    refunded = "refunded"


class Invoice(Base):
    __tablename__= "invoices"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_profiles.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    stripe_payment_intent_id = Column(String, nullable=True)
    stripe_session_id = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


    patient = relationship("PatientProfile", back_populates="invoices")
    appointment = relationship("Appointment", back_populates="invoice")

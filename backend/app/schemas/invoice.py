from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"


class InvoiceResponse(BaseModel):
    id: int
    patient_id: int
    appointment_id: int
    amount: float
    payment_status: str
    stripe_payment_intent_id: Optional[str] = None
    stripe_session_id: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime
    patient_email: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str
    amount: float
    currency: str


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str
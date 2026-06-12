from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.invoice import Invoice
from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.invoice import InvoiceResponse
from app.services.billing_service import (
    create_payment_intent,
    create_checkout_session,
    mark_invoice_paid,
    handle_stripe_webhook,
    get_invoice_by_appointment
)
from app.middleware.auth_middleware import (
    get_current_user,
    get_patient_user,
    get_admin_user
)
from app.services.email_service import send_payment_receipt


router = APIRouter(prefix="/api/billing", tags=["Billing"])


def build_invoice_response(invoice: Invoice, db: Session):
    """Helper to build invoice response with patient email"""
    patient = db.query(PatientProfile).filter(
        PatientProfile.id == invoice.patient_id
    ).first()
    patient_user = db.query(User).filter(
        User.id == patient.user_id
    ).first() if patient else None

    return InvoiceResponse(
        id=invoice.id,
        patient_id=invoice.patient_id,
        appointment_id=invoice.appointment_id,
        amount=invoice.amount,
        payment_status=invoice.payment_status,
        stripe_payment_intent_id=invoice.stripe_payment_intent_id,
        stripe_session_id=invoice.stripe_session_id,
        paid_at=invoice.paid_at,
        created_at=invoice.created_at,
        patient_email=patient_user.email if patient_user else None
    )


# ── Patient views own invoices ────────────────────────────
@router.get("/my", response_model=List[InvoiceResponse])
def get_my_invoices(
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found"
        )

    invoices = db.query(Invoice).filter(
        Invoice.patient_id == patient.id
    ).all()

    return [build_invoice_response(inv, db) for inv in invoices]


# ── Get invoice by appointment ────────────────────────────
@router.get("/appointment/{appointment_id}")
def get_invoice_for_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invoice = get_invoice_by_appointment(appointment_id, db)
    return build_invoice_response(invoice, db)


# ── Create payment intent ─────────────────────────────────
@router.post("/payment-intent/{invoice_id}")
def payment_intent(
    invoice_id: int,
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    return create_payment_intent(invoice_id, db)


# ── Create checkout session ───────────────────────────────
@router.post("/checkout/{invoice_id}")
def checkout_session(
    invoice_id: int,
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    return create_checkout_session(invoice_id, db)


# ── Mark invoice as paid (for testing) ───────────────────
@router.put("/mark-paid/{invoice_id}")
async def mark_paid(
    invoice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invoice = mark_invoice_paid(invoice_id, db)
    response = build_invoice_response(invoice, db)

    # Send receipt email
    try:
        patient = db.query(PatientProfile).filter(
            PatientProfile.id == invoice.patient_id
        ).first()
        patient_user = db.query(User).filter(
            User.id == patient.user_id
        ).first() if patient else None

        if patient_user:
            await send_payment_receipt(
                patient_email=patient_user.email,
                patient_name=patient_user.email.split("@")[0],
                invoice_id=invoice.id,
                appointment_id=invoice.appointment_id,
                amount=invoice.amount,
                paid_at=str(invoice.paid_at)
            )
    except Exception:
        pass

    return response



# ── Stripe webhook ────────────────────────────────────────
@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    return handle_stripe_webhook(payload, sig_header, db)


# ── Admin views all invoices ──────────────────────────────
@router.get("/", response_model=List[InvoiceResponse])
def get_all_invoices(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    invoices = db.query(Invoice).all()
    return [build_invoice_response(inv, db) for inv in invoices]


# ── Get single invoice ────────────────────────────────────
@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return build_invoice_response(invoice, db)
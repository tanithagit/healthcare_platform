import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.config import settings
from app.models.invoice import Invoice
from app.models.appointment import Appointment
from app.models.patient import PatientProfile
from app.models.user import User

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_invoice_by_appointment(appointment_id: int, db: Session):
    """Get invoice for an appointment"""
    invoice = db.query(Invoice).filter(
        Invoice.appointment_id == appointment_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found for this appointment"
        )
    return invoice


def create_payment_intent(invoice_id: int, db: Session):
    """
    Creates a Stripe Payment Intent.
    Returns client_secret which frontend uses to complete payment.
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.payment_status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    try:
        # Create Stripe payment intent
        # Amount in cents (multiply by 100)
        intent = stripe.PaymentIntent.create(
            amount=int(invoice.amount * 100),
            currency="inr",
            metadata={
                "invoice_id": invoice.id,
                "appointment_id": invoice.appointment_id
            }
        )

        # Save payment intent ID to invoice
        invoice.stripe_payment_intent_id = intent.id
        db.commit()

        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": invoice.amount,
            "currency": "inr"
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Stripe error: {str(e)}"
        )


def create_checkout_session(invoice_id: int, db: Session):
    """
    Creates a Stripe Checkout Session.
    Returns URL to redirect patient to Stripe payment page.
    """
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.payment_status == "paid":
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    # Get patient email
    patient = db.query(PatientProfile).filter(
        PatientProfile.id == invoice.patient_id
    ).first()
    patient_user = db.query(User).filter(
        User.id == patient.user_id
    ).first() if patient else None

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Consultation Fee - Appointment #{invoice.appointment_id}",
                    },
                    "unit_amount": int(invoice.amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/payment/cancel",
            customer_email=patient_user.email if patient_user else None,
            metadata={
                "invoice_id": str(invoice.id),
                "appointment_id": str(invoice.appointment_id)
            }
        )

        # Save session ID
        invoice.stripe_session_id = session.id
        db.commit()

        return {
            "checkout_url": session.url,
            "session_id": session.id
        }

    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Stripe error: {str(e)}"
        )


def mark_invoice_paid(invoice_id: int, db: Session):
    """Mark invoice as paid manually (for testing)"""
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice.payment_status = "paid"
    invoice.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(invoice)
    return invoice


def handle_stripe_webhook(payload: bytes, sig_header: str, db: Session):
    """
    Handles Stripe webhook events.
    Called by Stripe when payment is completed.
    """
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle payment success event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        invoice_id = session["metadata"].get("invoice_id")

        if invoice_id:
            invoice = db.query(Invoice).filter(
                Invoice.id == int(invoice_id)
            ).first()

            if invoice:
                invoice.payment_status = "paid"
                invoice.paid_at = datetime.utcnow()
                invoice.stripe_session_id = session["id"]
                db.commit()

    elif event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        invoice_id = intent["metadata"].get("invoice_id")

        if invoice_id:
            invoice = db.query(Invoice).filter(
                Invoice.id == int(invoice_id)
            ).first()

            if invoice:
                invoice.payment_status = "paid"
                invoice.paid_at = datetime.utcnow()
                db.commit()

    return {"status": "success"}
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pathlib import Path
from typing import List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates" / "email"
)


async def send_appointment_confirmation(
    patient_email: str,
    patient_name: str,
    doctor_name: str,
    specialization: str,
    appointment_date: str,
    reason: str,
    consultation_fee: float
):
    """Send appointment confirmation email to patient"""
    try:
        message = MessageSchema(
            subject="✅ Appointment Confirmed - Healthcare Platform",
            recipients=[patient_email],
            template_body={
                "patient_name": patient_name,
                "doctor_name": doctor_name,
                "specialization": specialization,
                "appointment_date": appointment_date,
                "reason": reason or "General Checkup",
                "consultation_fee": consultation_fee
            },
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(
            message,
            template_name="appointment_confirmation.html"
        )
        logger.info(f"Confirmation email sent to {patient_email}")

    except Exception as e:
        # Don't fail the request if email fails
        logger.error(f"Failed to send confirmation email: {str(e)}")


async def send_payment_receipt(
    patient_email: str,
    patient_name: str,
    invoice_id: int,
    appointment_id: int,
    amount: float,
    paid_at: str
):
    """Send payment receipt email to patient"""
    try:
        message = MessageSchema(
            subject="💳 Payment Receipt - Healthcare Platform",
            recipients=[patient_email],
            template_body={
                "patient_name": patient_name,
                "invoice_id": invoice_id,
                "appointment_id": appointment_id,
                "amount": amount,
                "paid_at": paid_at
            },
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(
            message,
            template_name="payment_receipt.html"
        )
        logger.info(f"Receipt email sent to {patient_email}")

    except Exception as e:
        logger.error(f"Failed to send receipt email: {str(e)}")


async def send_prescription_ready(
    patient_email: str,
    patient_name: str,
    doctor_name: str,
    medicines: List[Dict[str, Any]]
):
    """Send prescription ready email to patient"""
    try:
        message = MessageSchema(
            subject="💊 Your Prescription is Ready - Healthcare Platform",
            recipients=[patient_email],
            template_body={
                "patient_name": patient_name,
                "doctor_name": doctor_name,
                "medicines": medicines
            },
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(
            message,
            template_name="prescription_ready.html"
        )
        logger.info(f"Prescription email sent to {patient_email}")

    except Exception as e:
        logger.error(f"Failed to send prescription email: {str(e)}")


async def send_appointment_reminder(
    patient_email: str,
    patient_name: str,
    doctor_name: str,
    appointment_date: str
):
    """Send appointment reminder email"""
    try:
        message = MessageSchema(
            subject="⏰ Appointment Reminder - Healthcare Platform",
            recipients=[patient_email],
            body=f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #2563eb;">Appointment Reminder</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>This is a reminder for your upcoming appointment:</p>
                <div style="background: #f0f9ff; padding: 15px;
                            border-left: 4px solid #2563eb; margin: 15px 0;">
                    <p><strong>👨‍⚕️ Doctor:</strong> Dr. {doctor_name}</p>
                    <p><strong>📅 Date & Time:</strong> {appointment_date}</p>
                </div>
                <p>Please arrive 10 minutes early.</p>
                <p>Healthcare Platform Team</p>
            </body>
            </html>
            """,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Reminder email sent to {patient_email}")

    except Exception as e:
        logger.error(f"Failed to send reminder email: {str(e)}")
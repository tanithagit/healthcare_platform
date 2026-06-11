from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from app.models.appointment import Appointment
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.invoice import Invoice
from app.models.user import User
from app.schemas.appointment import AppointmentCreate


def check_slot_availability(
    doctor_id: int,
    appointment_date: datetime,
    db: Session,
    exclude_appointment_id: int = None
):
    time_window_start = appointment_date - timedelta(minutes=30)
    time_window_end = appointment_date + timedelta(minutes=30)

    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date >= time_window_start,
        Appointment.appointment_date <= time_window_end,
        Appointment.status != "canceled"
    )

    if exclude_appointment_id:
        query = query.filter(
            Appointment.id != exclude_appointment_id
        )

    existing = query.first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor already has an appointment at this time. Please choose a different slot."
        )
    return True


def create_appointment(
    data: AppointmentCreate,
    current_user: User,
    db: Session
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    if data.appointment_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment date must be in the future"
        )

    check_slot_availability(data.doctor_id, data.appointment_date, db)

    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=data.doctor_id,
        appointment_date=data.appointment_date,
        reason=data.reason,
        status="scheduled"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    invoice = Invoice(
        patient_id=patient.id,
        appointment_id=appointment.id,
        amount=doctor.consultation_fee,
        payment_status="pending"
    )
    db.add(invoice)
    db.commit()

    return appointment


def get_appointment_with_details(appointment: Appointment, db: Session):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == appointment.doctor_id
    ).first()
    patient = db.query(PatientProfile).filter(
        PatientProfile.id == appointment.patient_id
    ).first()

    doctor_user = db.query(User).filter(
        User.id == doctor.user_id
    ).first() if doctor else None

    patient_user = db.query(User).filter(
        User.id == patient.user_id
    ).first() if patient else None

    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "appointment_date": appointment.appointment_date,
        "status": appointment.status,
        "reason": appointment.reason,
        "notes": appointment.notes,
        "created_at": appointment.created_at,
        "doctor_email": doctor_user.email if doctor_user else None,
        "patient_email": patient_user.email if patient_user else None,
        "consultation_fee": doctor.consultation_fee if doctor else None
    }
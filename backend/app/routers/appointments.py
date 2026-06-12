from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)
from app.services.appointment_service import (
    create_appointment,
    check_slot_availability,
    get_appointment_with_details
)
from app.middleware.auth_middleware import (
    get_current_user,
    get_patient_user,
    get_doctor_user,
    get_admin_user,
    get_doctor_or_admin
)
from app.services.email_service import send_appointment_confirmation


router = APIRouter(prefix="/api/appointments", tags=["Appointments"])


# ── Patient books appointment ─────────────────────────────
# Update book_appointment route:
@router.post("/")
async def book_appointment(
    data: AppointmentCreate,
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    appointment = create_appointment(data, current_user, db)
    details = get_appointment_with_details(appointment, db)

    # Send confirmation email
    try:
        doctor = db.query(DoctorProfile).filter(
            DoctorProfile.id == appointment.doctor_id
        ).first()
        doctor_user = db.query(User).filter(
            User.id == doctor.user_id
        ).first() if doctor else None

        await send_appointment_confirmation(
            patient_email=current_user.email,
            patient_name=current_user.email.split("@")[0],
            doctor_name=doctor_user.email.split("@")[0] if doctor_user else "Doctor",
            specialization=doctor.specialization if doctor else "",
            appointment_date=str(appointment.appointment_date),
            reason=appointment.reason or "General Checkup",
            consultation_fee=doctor.consultation_fee if doctor else 0
        )
    except Exception:
        pass  # Don't fail booking if email fails

    return details

# ── Check slot availability ───────────────────────────────
@router.get("/check-slot")
def check_slot(
    doctor_id: int,
    appointment_date: str,
    db: Session = Depends(get_db)
):
    from datetime import datetime
    try:
        apt_date = datetime.fromisoformat(appointment_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use: YYYY-MM-DDTHH:MM:SS"
        )

    try:
        check_slot_availability(doctor_id, apt_date, db)
        return {"available": True, "message": "Slot is available"}
    except HTTPException:
        return {"available": False, "message": "Slot is not available"}


# ── Patient views own appointments ────────────────────────
@router.get("/my")
def get_my_appointments(
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient.id
    ).all()

    return [get_appointment_with_details(apt, db) for apt in appointments]


# ── Doctor views own appointments ─────────────────────────
@router.get("/doctor/my")
def get_doctor_appointments(
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).all()

    return [get_appointment_with_details(apt, db) for apt in appointments]


# ── Admin views all appointments ──────────────────────────
@router.get("/")
def get_all_appointments(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).all()
    return [get_appointment_with_details(apt, db) for apt in appointments]


# ── Get single appointment ────────────────────────────────
@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return get_appointment_with_details(appointment, db)


# ── Doctor updates appointment status ────────────────────
@router.put("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    data: AppointmentUpdate,
    current_user: User = Depends(get_doctor_or_admin),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Doctor can only update their own appointments
    if current_user.role == "doctor":
        doctor = db.query(DoctorProfile).filter(
            DoctorProfile.user_id == current_user.id
        ).first()
        if appointment.doctor_id != doctor.id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own appointments"
            )

    if data.status:
        appointment.status = data.status
    if data.notes:
        appointment.notes = data.notes

    db.commit()
    db.refresh(appointment)
    return get_appointment_with_details(appointment, db)


# ── Patient cancels appointment ───────────────────────────
@router.put("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.patient_id == patient.id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel a completed appointment"
        )

    appointment.status = AppointmentStatus.canceled
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment cancelled successfully"}
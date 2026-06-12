from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.medical_record import MedicalRecord
from app.models.appointment import Appointment
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse
)
from app.middleware.auth_middleware import (
    get_current_user,
    get_doctor_user,
    get_patient_user,
    get_admin_user,
    get_doctor_or_admin
)

router = APIRouter(prefix="/api/medical-records", tags=["Medical Records"])


def build_record_response(record: MedicalRecord, db: Session):
    """Helper to build response with emails"""
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == record.doctor_id
    ).first()
    patient = db.query(PatientProfile).filter(
        PatientProfile.id == record.patient_id
    ).first()
    doctor_user = db.query(User).filter(
        User.id == doctor.user_id
    ).first() if doctor else None
    patient_user = db.query(User).filter(
        User.id == patient.user_id
    ).first() if patient else None

    return MedicalRecordResponse(
        id=record.id,
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        appointment_id=record.appointment_id,
        diagnosis=record.diagnosis,
        notes=record.notes,
        created_at=record.created_at,
        doctor_email=doctor_user.email if doctor_user else None,
        patient_email=patient_user.email if patient_user else None
    )


# ── Doctor creates medical record ─────────────────────────
@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(
    data: MedicalRecordCreate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    # Get doctor profile
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor profile not found"
        )

    # Verify appointment exists and belongs to this doctor
    appointment = db.query(Appointment).filter(
        Appointment.id == data.appointment_id,
        Appointment.doctor_id == doctor.id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found or not assigned to you"
        )

    # Check if record already exists for this appointment
    existing = db.query(MedicalRecord).filter(
        MedicalRecord.appointment_id == data.appointment_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Medical record already exists for this appointment"
        )

    # Create medical record
    record = MedicalRecord(
        patient_id=appointment.patient_id,
        doctor_id=doctor.id,
        appointment_id=data.appointment_id,
        diagnosis=data.diagnosis,
        notes=data.notes
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return build_record_response(record, db)


# ── Doctor updates medical record ─────────────────────────
@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    data: MedicalRecordUpdate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id,
        MedicalRecord.doctor_id == doctor.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return build_record_response(record, db)


# ── Patient views own medical records ─────────────────────
@router.get("/my", response_model=List[MedicalRecordResponse])
def get_my_medical_records(
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

    records = db.query(MedicalRecord).filter(
        MedicalRecord.patient_id == patient.id
    ).all()

    return [build_record_response(r, db) for r in records]


# ── Doctor views records they created ─────────────────────
@router.get("/doctor/my", response_model=List[MedicalRecordResponse])
def get_doctor_medical_records(
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    records = db.query(MedicalRecord).filter(
        MedicalRecord.doctor_id == doctor.id
    ).all()

    return [build_record_response(r, db) for r in records]


# ── Admin views all records ────────────────────────────────
@router.get("/", response_model=List[MedicalRecordResponse])
def get_all_medical_records(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    records = db.query(MedicalRecord).all()
    return [build_record_response(r, db) for r in records]


# ── Get single record ──────────────────────────────────────
@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    # Patients can only view their own records
    if current_user.role == "patient":
        patient = db.query(PatientProfile).filter(
            PatientProfile.user_id == current_user.id
        ).first()
        if record.patient_id != patient.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return build_record_response(record, db)
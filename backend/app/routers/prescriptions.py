from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionBulkCreate
)
from app.middleware.auth_middleware import (
    get_current_user,
    get_doctor_user,
    get_patient_user,
    get_admin_user
)

router = APIRouter(prefix="/api/prescriptions", tags=["Prescriptions"])


# ── Doctor creates single prescription ────────────────────
@router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    data: PrescriptionCreate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    # Verify doctor owns this appointment
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    appointment = db.query(Appointment).filter(
        Appointment.id == data.appointment_id,
        Appointment.doctor_id == doctor.id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found or not assigned to you"
        )

    # Get medical record for this appointment
    medical_record = db.query(MedicalRecord).filter(
        MedicalRecord.appointment_id == data.appointment_id
    ).first()

    prescription = Prescription(
        appointment_id=data.appointment_id,
        medical_record_id=medical_record.id if medical_record else None,
        medicine_name=data.medicine_name,
        dosage=data.dosage,
        instructions=data.instructions,
        duration_days=data.duration_days
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


# ── Doctor creates multiple prescriptions at once ─────────
@router.post("/bulk", response_model=List[PrescriptionResponse])
def create_bulk_prescriptions(
    data: PrescriptionBulkCreate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    appointment = db.query(Appointment).filter(
        Appointment.id == data.appointment_id,
        Appointment.doctor_id == doctor.id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    medical_record = db.query(MedicalRecord).filter(
        MedicalRecord.appointment_id == data.appointment_id
    ).first()

    created = []
    for item in data.prescriptions:
        prescription = Prescription(
            appointment_id=data.appointment_id,
            medical_record_id=medical_record.id if medical_record else None,
            medicine_name=item.medicine_name,
            dosage=item.dosage,
            instructions=item.instructions,
            duration_days=item.duration_days
        )
        db.add(prescription)
        created.append(prescription)

    db.commit()
    for p in created:
        db.refresh(p)

    return created


# ── Patient views own prescriptions ───────────────────────
@router.get("/my", response_model=List[PrescriptionResponse])
def get_my_prescriptions(
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

    # Get all appointments for this patient
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient.id
    ).all()

    appointment_ids = [apt.id for apt in appointments]

    prescriptions = db.query(Prescription).filter(
        Prescription.appointment_id.in_(appointment_ids)
    ).all()

    return prescriptions


# ── Get prescriptions by appointment ──────────────────────
@router.get("/appointment/{appointment_id}",
            response_model=List[PrescriptionResponse])
def get_prescriptions_by_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prescriptions = db.query(Prescription).filter(
        Prescription.appointment_id == appointment_id
    ).all()

    return prescriptions


# ── Doctor updates prescription ────────────────────────────
@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    data: PrescriptionUpdate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    # Validate doctor owns this prescription
    appointment = db.query(Appointment).filter(
        Appointment.id == prescription.appointment_id,
        Appointment.doctor_id == doctor.id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own prescriptions"
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prescription, field, value)

    db.commit()
    db.refresh(prescription)
    return prescription


# ── Admin views all prescriptions ─────────────────────────
@router.get("/", response_model=List[PrescriptionResponse])
def get_all_prescriptions(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return db.query(Prescription).all()


# ── Get single prescription ────────────────────────────────
@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    return prescription
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.patient import PatientProfile
from app.models.user import User
from app.schemas.patient import PatientProfileUpdate, PatientProfileResponse
from app.middleware.auth_middleware import (
    get_current_user,
    get_admin_user,
    get_patient_user
)

router = APIRouter(prefix="/api/patients", tags=["Patients"])


# ── Patient views own profile ─────────────────────────────
@router.get("/profile/me", response_model=PatientProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    return PatientProfileResponse(
        id=patient.id,
        user_id=patient.user_id,
        date_of_birth=patient.date_of_birth,
        phone=patient.phone,
        address=patient.address,
        blood_group=patient.blood_group,
        emergency_contact=patient.emergency_contact,
        email=current_user.email
    )


# ── Patient updates own profile ───────────────────────────
@router.put("/profile/me", response_model=PatientProfileResponse)
def update_my_profile(
    data: PatientProfileUpdate,
    current_user: User = Depends(get_patient_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.user_id == current_user.id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return PatientProfileResponse(
        id=patient.id,
        user_id=patient.user_id,
        date_of_birth=patient.date_of_birth,
        phone=patient.phone,
        address=patient.address,
        blood_group=patient.blood_group,
        emergency_contact=patient.emergency_contact,
        email=current_user.email
    )


# ── Admin views all patients ──────────────────────────────
@router.get("/", response_model=List[PatientProfileResponse])
def get_all_patients(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    patients = db.query(PatientProfile).all()
    result = []
    for patient in patients:
        user = db.query(User).filter(User.id == patient.user_id).first()
        result.append(PatientProfileResponse(
            id=patient.id,
            user_id=patient.user_id,
            date_of_birth=patient.date_of_birth,
            phone=patient.phone,
            address=patient.address,
            blood_group=patient.blood_group,
            emergency_contact=patient.emergency_contact,
            email=user.email if user else None
        ))
    return result


# ── Admin views single patient ────────────────────────────
@router.get("/{patient_id}", response_model=PatientProfileResponse)
def get_patient(
    patient_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    patient = db.query(PatientProfile).filter(
        PatientProfile.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    user = db.query(User).filter(User.id == patient.user_id).first()
    return PatientProfileResponse(
        id=patient.id,
        user_id=patient.user_id,
        date_of_birth=patient.date_of_birth,
        phone=patient.phone,
        address=patient.address,
        blood_group=patient.blood_group,
        emergency_contact=patient.emergency_contact,
        email=user.email if user else None
    )
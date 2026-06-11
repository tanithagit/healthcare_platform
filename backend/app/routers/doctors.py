from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.doctor import DoctorProfile
from app.models.user import User
from app.schemas.doctor import DoctorProfileUpdate, DoctorProfileResponse
from app.middleware.auth_middleware import (
    get_current_user,
    get_admin_user,
    get_doctor_user
)

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


# ── Get all doctors (Public) ──────────────────────────────
@router.get("/", response_model=List[DoctorProfileResponse])
def get_all_doctors(
    db: Session = Depends(get_db)
):
    doctors = db.query(DoctorProfile).all()
    result = []
    for doctor in doctors:
        user = db.query(User).filter(User.id == doctor.user_id).first()
        doctor_data = DoctorProfileResponse(
            id=doctor.id,
            user_id=doctor.user_id,
            specialization=doctor.specialization,
            experience_years=doctor.experience_years,
            consultation_fee=doctor.consultation_fee,
            qualification=doctor.qualification,
            bio=doctor.bio,
            available_days=doctor.available_days,
            available_start_time=doctor.available_start_time,
            available_end_time=doctor.available_end_time,
            email=user.email if user else None
        )
        result.append(doctor_data)
    return result


# ── Get doctor by ID (Public) ─────────────────────────────
@router.get("/{doctor_id}", response_model=DoctorProfileResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    user = db.query(User).filter(User.id == doctor.user_id).first()
    return DoctorProfileResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialization=doctor.specialization,
        experience_years=doctor.experience_years,
        consultation_fee=doctor.consultation_fee,
        qualification=doctor.qualification,
        bio=doctor.bio,
        available_days=doctor.available_days,
        available_start_time=doctor.available_start_time,
        available_end_time=doctor.available_end_time,
        email=user.email if user else None
    )


# ── Doctor updates own profile ────────────────────────────
@router.put("/profile/me", response_model=DoctorProfileResponse)
def update_my_profile(
    data: DoctorProfileUpdate,
    current_user: User = Depends(get_doctor_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.user_id == current_user.id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found"
        )

    # Update only provided fields
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)

    return DoctorProfileResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialization=doctor.specialization,
        experience_years=doctor.experience_years,
        consultation_fee=doctor.consultation_fee,
        qualification=doctor.qualification,
        bio=doctor.bio,
        available_days=doctor.available_days,
        available_start_time=doctor.available_start_time,
        available_end_time=doctor.available_end_time,
        email=current_user.email
    )


# ── Admin updates any doctor profile ─────────────────────
@router.put("/{doctor_id}", response_model=DoctorProfileResponse)
def update_doctor(
    doctor_id: int,
    data: DoctorProfileUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)

    user = db.query(User).filter(User.id == doctor.user_id).first()
    return DoctorProfileResponse(
        id=doctor.id,
        user_id=doctor.user_id,
        specialization=doctor.specialization,
        experience_years=doctor.experience_years,
        consultation_fee=doctor.consultation_fee,
        qualification=doctor.qualification,
        bio=doctor.bio,
        available_days=doctor.available_days,
        available_start_time=doctor.available_start_time,
        available_end_time=doctor.available_end_time,
        email=user.email if user else None
    )


# ── Admin deletes doctor ──────────────────────────────────
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    doctor = db.query(DoctorProfile).filter(
        DoctorProfile.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    # Deactivate user instead of hard delete
    user = db.query(User).filter(User.id == doctor.user_id).first()
    if user:
        user.is_active = 0
        db.commit()

    return {"message": "Doctor deactivated successfully"}
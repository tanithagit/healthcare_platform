from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user import User, UserRole
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.schemas.user import UserRegister
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.config import settings


def register_user(data: UserRegister, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto-create profile based on role
    if data.role == UserRole.doctor:
        doctor_profile = DoctorProfile(
            user_id=new_user.id,
            specialization="General",
            consultation_fee=0.0
        )
        db.add(doctor_profile)
        db.commit()

    elif data.role == UserRole.patient:
        patient_profile = PatientProfile(
            user_id=new_user.id
        )
        db.add(patient_profile)
        db.commit()

    return new_user


def login_user(email: str, password: str, db: Session):
    # Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is inactive"
        )

    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id,
        "email": user.email
    }
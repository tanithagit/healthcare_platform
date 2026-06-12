from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Import all models
from app.models.user import User
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from app.models.invoice import Invoice

# Import all routers
from app.routers import (
    auth,
    doctors,
    patients,
    admin,
    appointments,
    medical_records,
    prescriptions,
    billing
)

app = FastAPI(
    title=settings.APP_NAME,
    description="Healthcare Clinic Management Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All Routers
app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(admin.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(prescriptions.router)
app.include_router(billing.router)


@app.get("/")
def root():
    return {
        "message": "Healthcare Platform API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
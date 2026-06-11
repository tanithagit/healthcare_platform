from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.doctor import DoctorProfile
from app.models.patient import PatientProfile
from app.models.appointment import Appointment, AppointmentStatus
from app.models.invoice import Invoice, PaymentStatus
from app.middleware.auth_middleware import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# ── Admin Dashboard Stats ─────────────────────────────────
@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # Count stats
    total_doctors = db.query(DoctorProfile).count()
    total_patients = db.query(PatientProfile).count()
    total_appointments = db.query(Appointment).count()

    scheduled = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.scheduled
    ).count()

    completed = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.completed
    ).count()

    canceled = db.query(Appointment).filter(
        Appointment.status == AppointmentStatus.canceled
    ).count()

    # Revenue from paid invoices
    paid_invoices = db.query(Invoice).filter(
        Invoice.payment_status == PaymentStatus.paid
    ).all()
    total_revenue = sum(inv.amount for inv in paid_invoices)

    return {
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "appointments": {
            "scheduled": scheduled,
            "completed": completed,
            "canceled": canceled
        },
        "total_revenue": total_revenue
    }


# ── Get all users ─────────────────────────────────────────
@router.get("/users")
def get_all_users(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]


# ── Deactivate user ───────────────────────────────────────
@router.put("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.is_active = 0
    db.commit()
    return {"message": f"User {user.email} deactivated successfully"}


# ── Activate user ─────────────────────────────────────────
@router.put("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.is_active = 1
    db.commit()
    return {"message": f"User {user.email} activated successfully"}
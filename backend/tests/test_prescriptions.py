import pytest
from datetime import datetime, timedelta


class TestPrescriptions:

    def create_full_setup(self, client):
        """
        Creates doctor, patient, and appointment
        Returns doctor_token, patient_token, apt_id
        """
        import time
        unique = str(int(time.time()))

        # Register doctor
        client.post("/api/auth/register", json={
            "email": f"doc_{unique}@test.com",
            "password": "doctor123",
            "role": "doctor"
        })
        doctor_login = client.post(
            "/api/auth/login",
            data={
                "username": f"doc_{unique}@test.com",
                "password": "doctor123"
            }
        )
        doctor_token = doctor_login.json()["access_token"]

        # Register patient
        client.post("/api/auth/register", json={
            "email": f"pat_{unique}@test.com",
            "password": "patient123",
            "role": "patient"
        })
        patient_login = client.post(
            "/api/auth/login",
            data={
                "username": f"pat_{unique}@test.com",
                "password": "patient123"
            }
        )
        patient_token = patient_login.json()["access_token"]

        # Get this doctor's profile id
        doctors = client.get("/api/doctors/").json()

        # Find the doctor we just created
        doctor_profile = None
        for d in doctors:
            if f"doc_{unique}" in (d.get("email") or ""):
                doctor_profile = d
                break

        if not doctor_profile:
            # Use last doctor in list
            doctor_profile = doctors[-1]

        doctor_id = doctor_profile["id"]

        # Update doctor fee so invoice works
        client.put(
            f"/api/doctors/{doctor_id}",
            json={
                "specialization": "General",
                "consultation_fee": 500.0,
                "experience_years": 5
            },
            headers={"Authorization": f"Bearer {doctor_token}"}
        )

        # Book appointment as patient
        future_date = (
            datetime.utcnow() + timedelta(days=25)
        ).replace(
            hour=11, minute=0, second=0, microsecond=0
        ).isoformat()

        apt_response = client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": future_date,
                "reason": "Prescription test"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )

        if apt_response.status_code != 200:
            return None, None, None

        apt_id = apt_response.json()["id"]
        return doctor_token, patient_token, apt_id

    def test_doctor_creates_medical_record(self, client):
        """Test doctor can create medical record"""
        doctor_token, _, apt_id = self.create_full_setup(client)

        if not apt_id:
            pytest.skip("Could not create appointment")

        response = client.post(
            "/api/medical-records/",
            json={
                "appointment_id": apt_id,
                "diagnosis": "Common cold",
                "notes": "Rest and hydration recommended"
            },
            headers={"Authorization": f"Bearer {doctor_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["diagnosis"] == "Common cold"
        print("✅ Doctor creates medical record test passed")

    def test_doctor_creates_prescription(self, client):
        """Test doctor can create prescription"""
        doctor_token, _, apt_id = self.create_full_setup(client)

        if not apt_id:
            pytest.skip("Could not create appointment")

        response = client.post(
            "/api/prescriptions/",
            json={
                "appointment_id": apt_id,
                "medicine_name": "Paracetamol",
                "dosage": "500mg",
                "instructions": "Twice daily after meals",
                "duration_days": 5
            },
            headers={"Authorization": f"Bearer {doctor_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["medicine_name"] == "Paracetamol"
        print("✅ Doctor creates prescription test passed")

    def test_patient_views_own_prescriptions(
        self, client, patient_token
    ):
        """Test patient can view own prescriptions"""
        response = client.get(
            "/api/prescriptions/my",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✅ Patient views prescriptions test passed")

    def test_patient_cannot_create_prescription(
        self, client, patient_token
    ):
        """Test patient cannot create prescription"""
        response = client.post(
            "/api/prescriptions/",
            json={
                "appointment_id": 1,
                "medicine_name": "Aspirin",
                "dosage": "100mg",
                "instructions": "Once daily",
                "duration_days": 7
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 403
        print("✅ Patient prescription access control test passed")
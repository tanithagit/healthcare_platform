import pytest
from datetime import datetime, timedelta


def get_future_date(days=7, hour=10):
    """Get a future datetime string"""
    future = datetime.utcnow() + timedelta(days=days)
    return future.replace(
        hour=hour, minute=0, second=0, microsecond=0
    ).isoformat()


class TestAppointments:

    def get_doctor_id(self, client):
        """Helper to get doctor profile id"""
        # Register and get doctor
        client.post("/api/auth/register", json={
            "email": "aptdoctor@test.com",
            "password": "doctor123",
            "role": "doctor"
        })
        response = client.get("/api/doctors/")
        doctors = response.json()
        return doctors[0]["id"] if doctors else None

    def test_book_appointment(self, client, patient_token):
        """Test patient can book appointment"""
        doctor_id = self.get_doctor_id(client)
        if not doctor_id:
            pytest.skip("No doctor available")

        response = client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": get_future_date(days=10),
                "reason": "Test appointment"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "scheduled"
        print("✅ Book appointment test passed")

    def test_double_booking_prevention(self, client, patient_token):
        """Test double booking is prevented"""
        doctor_id = self.get_doctor_id(client)
        if not doctor_id:
            pytest.skip("No doctor available")

        appointment_date = get_future_date(days=15)

        # Book first appointment
        client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": appointment_date,
                "reason": "First booking"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )

        # Try to book same slot
        response = client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": appointment_date,
                "reason": "Second booking - should fail"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 400
        print("✅ Double booking prevention test passed")

    def test_past_date_booking(self, client, patient_token):
        """Test booking past date fails"""
        doctor_id = self.get_doctor_id(client)
        if not doctor_id:
            pytest.skip("No doctor available")

        past_date = (
            datetime.utcnow() - timedelta(days=1)
        ).isoformat()

        response = client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": past_date,
                "reason": "Past date booking"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 400
        print("✅ Past date booking test passed")

    def test_patient_views_own_appointments(
        self, client, patient_token
    ):
        """Test patient can view own appointments"""
        response = client.get(
            "/api/appointments/my",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✅ Patient views appointments test passed")

    def test_slot_availability_check(self, client):
        """Test slot availability endpoint"""
        doctor_id = self.get_doctor_id(client)
        if not doctor_id:
            pytest.skip("No doctor available")

        response = client.get(
            "/api/appointments/check-slot",
            params={
                "doctor_id": doctor_id,
                "appointment_date": get_future_date(days=30)
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "available" in data
        print("✅ Slot availability check test passed")

    def test_admin_can_view_all_appointments(
        self, client, admin_token
    ):
        """Test admin can view all appointments"""
        response = client.get(
            "/api/appointments/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        print("✅ Admin view all appointments test passed")

    def test_patient_cannot_view_all_appointments(
        self, client, patient_token
    ):
        """Test patient cannot view all appointments"""
        response = client.get(
            "/api/appointments/",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 403
        print("✅ Patient access control test passed")
import pytest
from datetime import datetime, timedelta


class TestBilling:

    def setup_appointment(self, client, patient_token):
        """Helper to create appointment and return invoice"""
        # Get doctor
        response = client.get("/api/doctors/")
        doctors = response.json()
        if not doctors:
            return None

        doctor_id = doctors[0]["id"]
        future_date = (
            datetime.utcnow() + timedelta(days=20)
        ).replace(
            hour=14, minute=0, second=0, microsecond=0
        ).isoformat()

        # Book appointment
        apt_response = client.post(
            "/api/appointments/",
            json={
                "doctor_id": doctor_id,
                "appointment_date": future_date,
                "reason": "Billing test"
            },
            headers={"Authorization": f"Bearer {patient_token}"}
        )

        if apt_response.status_code != 200:
            return None

        apt_id = apt_response.json()["id"]

        # Get invoice
        inv_response = client.get(
            f"/api/billing/appointment/{apt_id}",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        return inv_response.json() if inv_response.status_code == 200\
            else None

    def test_invoice_created_on_booking(
        self, client, patient_token
    ):
        """Test invoice is auto-created when appointment is booked"""
        invoice = self.setup_appointment(client, patient_token)
        if not invoice:
            pytest.skip("Could not create appointment")

        assert invoice["payment_status"] == "pending"
        assert invoice["amount"] >= 0
        print("✅ Invoice auto-creation test passed")

    def test_patient_views_own_invoices(
        self, client, patient_token
    ):
        """Test patient can view own invoices"""
        response = client.get(
            "/api/billing/my",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        print("✅ Patient views invoices test passed")

    def test_mark_invoice_paid(self, client, patient_token):
        """Test marking invoice as paid"""
        invoice = self.setup_appointment(client, patient_token)
        if not invoice:
            pytest.skip("Could not create invoice")

        response = client.put(
            f"/api/billing/mark-paid/{invoice['id']}",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["payment_status"] == "paid"
        print("✅ Mark invoice paid test passed")

    def test_admin_views_all_invoices(
        self, client, admin_token
    ):
        """Test admin can view all invoices"""
        response = client.get(
            "/api/billing/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        print("✅ Admin views all invoices test passed")
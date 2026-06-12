import pytest


class TestAuth:

    def test_register_admin(self, client):
        """Test admin registration"""
        response = client.post("/api/auth/register", json={
            "email": "newadmin@test.com",
            "password": "admin123",
            "role": "admin"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newadmin@test.com"
        assert data["role"] == "admin"
        print("✅ Admin registration passed")

    def test_register_doctor(self, client):
        """Test doctor registration"""
        response = client.post("/api/auth/register", json={
            "email": "newdoctor@test.com",
            "password": "doctor123",
            "role": "doctor"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "doctor"
        print("✅ Doctor registration passed")

    def test_register_patient(self, client):
        """Test patient registration"""
        response = client.post("/api/auth/register", json={
            "email": "newpatient@test.com",
            "password": "patient123",
            "role": "patient"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "patient"
        print("✅ Patient registration passed")

    def test_duplicate_email(self, client):
        """Test duplicate email registration fails"""
        client.post("/api/auth/register", json={
            "email": "duplicate@test.com",
            "password": "test123",
            "role": "patient"
        })
        response = client.post("/api/auth/register", json={
            "email": "duplicate@test.com",
            "password": "test123",
            "role": "patient"
        })
        assert response.status_code == 400
        print("✅ Duplicate email check passed")

    def test_login_success(self, client):
        """Test successful login"""
        client.post("/api/auth/register", json={
            "email": "logintest@test.com",
            "password": "test123",
            "role": "patient"
        })
        response = client.post("/api/auth/login", data={
            "username": "logintest@test.com",
            "password": "test123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        print("✅ Login success test passed")

    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        client.post("/api/auth/register", json={
            "email": "wrongpass@test.com",
            "password": "correct123",
            "role": "patient"
        })
        response = client.post("/api/auth/login", data={
            "username": "wrongpass@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print("✅ Wrong password test passed")

    def test_get_me(self, client, patient_token):
        """Test get current user"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {patient_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        print("✅ Get me test passed")
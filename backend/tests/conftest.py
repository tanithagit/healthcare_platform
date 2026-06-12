import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use separate test database
TEST_DATABASE_URL = (
    "postgresql://postgres:admin123@localhost:5432/healthcare_test_db"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def setup_db():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_db):
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    """Create admin user and return token"""
    # Register
    client.post("/api/auth/register", json={
        "email": "testadmin@test.com",
        "password": "admin123",
        "role": "admin"
    })
    # Login
    response = client.post("/api/auth/login", data={
        "username": "testadmin@test.com",
        "password": "admin123"
    })
    return response.json()["access_token"]


@pytest.fixture
def doctor_token(client):
    """Create doctor user and return token"""
    client.post("/api/auth/register", json={
        "email": "testdoctor@test.com",
        "password": "doctor123",
        "role": "doctor"
    })
    response = client.post("/api/auth/login", data={
        "username": "testdoctor@test.com",
        "password": "doctor123"
    })
    return response.json()["access_token"]


@pytest.fixture
def patient_token(client):
    """Create patient user and return token"""
    client.post("/api/auth/register", json={
        "email": "testpatient@test.com",
        "password": "patient123",
        "role": "patient"
    })
    response = client.post("/api/auth/login", data={
        "username": "testpatient@test.com",
        "password": "patient123"
    })
    return response.json()["access_token"]
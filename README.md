#  Healthcare Clinic Management Platform

A full-stack SaaS platform for managing healthcare clinics — doctors,
patients, appointments, prescriptions, billing, and medical records.

---

##  Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM for database operations |
| Alembic | Database migrations |
| JWT | Authentication & authorization |
| Stripe | Payment processing |
| FastAPI-Mail | Email notifications |

### Frontend
| Technology | Purpose |
|------------|---------|
| React + Vite | UI framework |
| Tailwind CSS | Styling |
| React Router | Client-side routing |
| Axios | HTTP client |

---

##  System Roles

| Role | Permissions |
|------|-------------|
|  Admin | Manage doctors, patients, view all data |
|  Doctor | View appointments, create records & prescriptions |
|  Patient | Book appointments, view history, pay bills |

---

##  Project Architecture

healthcare-platform/

├── backend/

│   ├── app/

│   │   ├── main.py          # FastAPI app entry point

│   │   ├── config.py        # Environment configuration

│   │   ├── database.py      # Database connection

│   │   ├── models/          # SQLAlchemy database models

│   │   ├── schemas/         # Pydantic request/response schemas

│   │   ├── routers/         # API route handlers

│   │   ├── services/        # Business logic layer

│   │   ├── middleware/       # Auth & role guards

│   │   └── utils/           # Helper functions

│   ├── alembic/             # Database migrations

│   └── tests/               # Automated tests

└── frontend/

└── src/

├── api/             # Axios API calls

├── context/         # Global auth state

├── components/      # Reusable UI components

└── pages/           # Role-based pages

---

##  Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Git

---

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/healthcare-platform.git
cd healthcare-platform
```

---

### 2. Backend Setup

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux

# Edit .env with your values
# Set DATABASE_URL, SECRET_KEY, STRIPE keys, Email config
```

---

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE healthcare_db;
\q

# Run migrations
alembic upgrade head
```

---

### 4. Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

---

### 5. Frontend Setup

```bash
# Go to frontend folder
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

##  Demo Credentials

| Role | Email | Password |
|------|-------|----------|
|  Admin | admin@healthcare.com | admin123 |
|  Doctor | doctor@healthcare.com | doctor123 |
|  Patient | patient@healthcare.com | patient123 |

---

##  Appointment Workflow

---

##  Billing Workflow

---

##  Email Notifications

| Event | Recipient | Email Type |
|-------|-----------|------------|
| Appointment booked | Patient | Confirmation |
| Payment completed | Patient | Receipt |
| Prescription ready | Patient | Notification |
| Appointment reminder | Patient | Reminder |

---

##  Authentication & Authorization

- **JWT tokens** — stateless authentication
- **Role-based access** — admin, doctor, patient
- **Protected routes** — frontend and backend
- **Token expiry** — 30 minutes (configurable)

---

##  Database Models

| Model | Description |
|-------|-------------|
| User | Authentication and roles |
| DoctorProfile | Doctor details and availability |
| PatientProfile | Patient demographics |
| Appointment | Booking with status tracking |
| MedicalRecord | Diagnosis and consultation notes |
| Prescription | Medicine and dosage details |
| Invoice | Payment tracking |

---

##  Running Tests

```bash
# Go to backend folder
cd backend

# Activate virtual environment
venv\Scripts\activate

# Create test database
psql -U postgres -c "CREATE DATABASE healthcare_test_db;"

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Test Coverage

| Test File | Tests | Coverage |
|-----------|-------|----------|
| test_auth.py | 6 | Auth & JWT |
| test_appointments.py | 7 | Booking & Slots |
| test_billing.py | 4 | Payments |
| test_prescriptions.py | 4 | Medical Records |
| **Total** | **21** | **All Passing** |

---

##  API Endpoints

### Authentication

### Doctors

### Appointments

### Medical Records

### Prescriptions

### Billing

### Admin

---

##  Security Features

- Passwords hashed with bcrypt
- JWT tokens with expiry
- Role-based access control
- Environment variables for secrets
- CORS configured for frontend only
- Input validation with Pydantic
- Double booking prevention

---

##  Environment Variables

See `.env.example` for all required variables.

| Variable | Description |
|----------|-------------|
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | JWT signing secret |
| STRIPE_SECRET_KEY | Stripe API key |
| MAIL_USERNAME | Gmail address |
| MAIL_PASSWORD | Gmail app password |

---

##  Deployment Notes

- Set `DEBUG=False` in production
- Use strong `SECRET_KEY`
- Configure real Stripe keys
- Set up proper CORS origins
- Use environment variables
- Set up SSL/HTTPS

---

##  Developer

Built as part of Full-Stack SaaS Assignment

**GitHub:** https://github.com/YOUR_USERNAME/healthcare-platform
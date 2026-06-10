from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Healthcare Clinic Management Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check route
@app.get("/")
def root():
    return {
        "message": "Healthcare Platform API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
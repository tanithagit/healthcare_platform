from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # logs all SQL queries, turn off in production
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all models
class Base(DeclarativeBase):
    pass


# Dependency — used in every route to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
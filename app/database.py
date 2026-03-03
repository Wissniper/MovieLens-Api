from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///movies.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Simple dependency for getting DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite file database — no separate DB server needed, works out of the box.
# To use PostgreSQL/MySQL later, just change this URL, e.g.:
# "postgresql://user:password@localhost/thiranpathai"
DATABASE_URL = "sqlite:///./thiranpathai.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

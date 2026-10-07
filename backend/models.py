from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="")
    skills = Column(String, nullable=False)  # stored as comma-separated lowercase skills


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)


class Resume(Base):
    """Each user has one saved resume — updated whenever they upload a new one."""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    text = Column(String, nullable=False, default="")
    skills = Column(String, nullable=False, default="")  # comma-separated
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

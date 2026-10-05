from sqlalchemy import Column, Integer, String
from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="")
    skills = Column(String, nullable=False)  # stored as comma-separated lowercase skills

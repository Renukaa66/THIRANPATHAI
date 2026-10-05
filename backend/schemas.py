from pydantic import BaseModel
from typing import List


class CompanyBase(BaseModel):
    name: str
    role: str = ""
    skills: List[str]


class CompanyCreate(CompanyBase):
    pass


class CompanyOut(CompanyBase):
    id: int

    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    resume_skills: List[str]
    company_id: int


class MatchResponse(BaseModel):
    company: CompanyOut
    percent: int
    matched: List[str]
    missing: List[str]


class RoadmapRequest(BaseModel):
    known_skills: List[str]
    missing_skills: List[str]

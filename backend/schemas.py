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


# ---------- Auth ----------
class UserSignup(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class SavedResumeOut(BaseModel):
    text: str
    skills: List[str]

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

from database import Base, engine, get_db
import models
import schemas
from resume_parser import extract_text, extract_skills
from skills_data import DEFAULT_COMPANIES, RESOURCES, PREREQ, QUIZ

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ThiranPathai API")


@app.on_event("startup")
def seed_default_companies():
    db = next(get_db())
    if db.query(models.Company).count() == 0:
        for c in DEFAULT_COMPANIES:
            db.add(models.Company(name=c["name"], role=c["role"], skills=",".join(c["skills"])))
        db.commit()


def to_out(c: models.Company) -> schemas.CompanyOut:
    return schemas.CompanyOut(id=c.id, name=c.name, role=c.role, skills=c.skills.split(","))


# ---------- Resume ----------
@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = extract_text(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    skills = extract_skills(text)
    return {"text": text.strip(), "skills": skills}


# ---------- Companies (CRUD, backed by the database) ----------
@app.get("/api/companies", response_model=List[schemas.CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    return [to_out(c) for c in db.query(models.Company).all()]


@app.post("/api/companies", response_model=schemas.CompanyOut)
def create_company(payload: schemas.CompanyCreate, db: Session = Depends(get_db)):
    c = models.Company(name=payload.name, role=payload.role, skills=",".join(s.lower() for s in payload.skills))
    db.add(c)
    db.commit()
    db.refresh(c)
    return to_out(c)


@app.put("/api/companies/{company_id}", response_model=schemas.CompanyOut)
def update_company(company_id: int, payload: schemas.CompanyCreate, db: Session = Depends(get_db)):
    c = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    c.name = payload.name
    c.role = payload.role
    c.skills = ",".join(s.lower() for s in payload.skills)
    db.commit()
    db.refresh(c)
    return to_out(c)


@app.delete("/api/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(c)
    db.commit()
    return {"deleted": True}


# ---------- Matching ----------
@app.post("/api/match", response_model=schemas.MatchResponse)
def match(payload: schemas.MatchRequest, db: Session = Depends(get_db)):
    c = db.query(models.Company).filter(models.Company.id == payload.company_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Company not found")
    required = c.skills.split(",")
    have = set(s.lower() for s in payload.resume_skills)
    matched = [s for s in required if s in have]
    missing = [s for s in required if s not in have]
    percent = round((len(matched) / len(required)) * 100) if required else 0
    return schemas.MatchResponse(company=to_out(c), percent=percent, matched=matched, missing=missing)


# ---------- Roadmap ----------
@app.post("/api/roadmap")
def roadmap(payload: schemas.RoadmapRequest):
    known = set(payload.known_skills)
    missing = list(payload.missing_skills)
    ordered = []
    pool = list(missing)
    guard = 0
    while pool and guard < 50:
        guard += 1
        progressed = False
        for i, skill in enumerate(pool):
            reqs = PREREQ.get(skill, [])
            ready = all(r in known or r in ordered or r not in missing for r in reqs)
            if ready:
                ordered.append(pool.pop(i))
                progressed = True
                break
        if not progressed:
            ordered.append(pool.pop(0))  # avoid infinite loop on circular/unmet prereqs

    steps = []
    for skill in ordered:
        steps.append({
            "skill": skill,
            "resource": RESOURCES.get(skill, f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}"),
            "youtube": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial+for+beginners",
        })
    return {"steps": steps}


# ---------- Quiz ----------
@app.get("/api/quiz/{skill}")
def get_quiz(skill: str):
    questions = QUIZ.get(skill.lower())
    if not questions:
        raise HTTPException(status_code=404, detail="No quiz available for this skill yet.")
    # don't send the answer index to the browser — graded server-side on submit
    safe = [{"q": item["q"], "o": item["o"]} for item in questions]
    return {"skill": skill, "questions": safe}


@app.get("/api/quiz")
def list_quiz_skills():
    return {"skills": list(QUIZ.keys())}


@app.post("/api/quiz/{skill}/submit")
def submit_quiz(skill: str, answers: List[int]):
    questions = QUIZ.get(skill.lower())
    if not questions:
        raise HTTPException(status_code=404, detail="No quiz available for this skill yet.")
    score = sum(1 for i, item in enumerate(questions) if i < len(answers) and answers[i] == item["a"])
    return {"score": score, "total": len(questions)}


# ---------- Serve the frontend ----------
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

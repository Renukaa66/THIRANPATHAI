# ThiranPathai — AI Skill Roadmap for Placements

ThiranPathai is a placement readiness platform that helps engineering students identify the skills they lack for their target job roles — and follow a clear, ordered path to close those gaps.

Most students prepare for placements without knowing exactly what employers require. Existing resume tools lean on simple keyword matching, are often paid, and aren't built around campus placements. ThiranPathai reads a student's resume, checks it against real company skill requirements, and generates a personalised, prerequisite-aware learning roadmap.

## Features

- **Resume Upload** — Upload a resume as PDF, DOCX, or TXT; skills are extracted automatically on the server
- **Smart Skill Matching** — Keyword, alias, and fuzzy string matching, so formatting differences (e.g. "REST API" vs "RESTful services") are still recognized
- **Company Fit Score** — Check your match percentage against 5 default company roles, or add/edit/delete any custom company by entering its required skills
- **Prerequisite-Aware Roadmap** — Missing skills are arranged in a logical learning order (e.g. Git before Docker), each with a direct resource link and a YouTube tutorial link
- **Resume Auto-Update** — Mark a skill as learned, and it's automatically added back into your resume
- **Skill Tests** — Short, server-graded quizzes to check your readiness for specific skills
- **Mobile-Responsive** — Works like a mobile app in any phone browser, no app store install needed

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite (via SQLAlchemy ORM) |
| Resume Parsing | pypdf, python-docx, rapidfuzz |

## Project Structure

```
thiranpathai/
├── backend/
│   ├── main.py          # FastAPI app + all API routes
│   ├── database.py      # DB connection setup
│   ├── models.py        # SQLAlchemy table definitions
│   ├── schemas.py        # Request/response validation
│   ├── resume_parser.py  # PDF/DOCX/TXT text + skill extraction
│   ├── skills_data.py    # Master skill list, quiz bank, resources
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── README.md
```

## Getting Started (Local)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/thiranpathai.git
cd thiranpathai

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser.

## API Documentation

Interactive API docs (Swagger UI) are available at **`/docs`** once the server is running.

## Known Limitations / Future Work

- Skill extraction uses keyword + fuzzy matching, not semantic embeddings — swapping in `sentence-transformers` for true meaning-based matching is a planned upgrade
- SQLite is used for simplicity; switching to PostgreSQL is a one-line change in `database.py` for multi-user production use
- No login/authentication yet — each browser session is independent

## License

This project was built as a final-year academic project.

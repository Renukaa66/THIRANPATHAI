# ThiranPathai — Full Stack Setup (VS Code)

A skill-gap and placement-readiness app: upload a resume, check fit against
companies/roles, get a learning roadmap, and take skill quizzes.

## Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite (file-based, zero setup — auto-created on first run)
- **Frontend:** Plain HTML/CSS/JS (mobile-style layout), served by the backend
- **Resume parsing:** pypdf (PDF), python-docx (DOCX), rapidfuzz (fuzzy skill matching)

## Folder structure
```
thiranpathai/
├── backend/
│   ├── main.py          ← FastAPI app + all API routes
│   ├── database.py      ← DB connection setup
│   ├── models.py        ← SQLAlchemy table definitions
│   ├── schemas.py       ← Request/response validation
│   ├── resume_parser.py ← PDF/DOCX/TXT text + skill extraction
│   ├── skills_data.py   ← Master skill list, quiz bank, resources
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js            ← calls the backend API with fetch()
├── .gitignore
└── README.md
```

## How to run it in VS Code

1. **Open the `thiranpathai` folder** in VS Code (File → Open Folder).

2. **Create a virtual environment** (Terminal → New Terminal, inside the project root):
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open the app:** go to **http://localhost:8000** in your browser.
   The database file `thiranpathai.db` is created automatically the first
   time you run it, with 5 default companies already seeded.

6. **Try it on your phone (same WiFi):**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0
   ```
   Find your computer's local IP (e.g. `192.168.1.5` — run `ipconfig` on
   Windows or `ifconfig`/`ip a` on Mac/Linux), then on your phone's browser
   open `http://192.168.1.5:8000`. It will look and behave like a mobile app.

## Hosting it online for free (so anyone can open it)
See the deployment steps shared in chat — in short: push this folder to
GitHub, then create a free Web Service on **render.com** pointing at the
`backend` folder, with:
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## API docs
FastAPI gives you free interactive API docs at **http://localhost:8000/docs**
— useful for your project report/demo, and for testing endpoints directly.

## What's genuinely "AI/NLP" here, and what's a placeholder
Be upfront about this in your viva/report:

- **Skill extraction** currently uses keyword + alias + fuzzy-string matching
  (`resume_parser.py`), with word-boundary matching so short skill names like
  "C" don't wrongly match inside other words (e.g. "CSS"). This is a solid,
  explainable baseline — not a trained ML model.
- **Upgrade path for a stronger project:** replace/augment `extract_skills()`
  with sentence embeddings (`sentence-transformers`) so skills are matched by
  *meaning*, not just spelling — e.g. "RESTful services" ↔ "REST API". Compare
  both approaches with precision/recall/F1 on a labelled test set.
- **Database:** SQLite is fine for a demo/project. If you need multiple
  people writing at once, switch `DATABASE_URL` in `database.py` to
  PostgreSQL — one line change, the rest of the code doesn't need to change.

## Extending it
- Add a `Student`/`User` table + login if you want per-student accounts
  instead of a single browser session.
- Add a `results` table to store quiz history and match history over time
  (currently these aren't persisted, only computed live).
- Move `skills_data.py`'s quiz bank into database tables so a placement
  officer can add questions without touching code.

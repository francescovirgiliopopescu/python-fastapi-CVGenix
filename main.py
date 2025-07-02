# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from utils import fetch_rss_data
from crud import get_candidates, create_candidate, get_matched_candidates, check_candidate
from database import get_db, SessionLocal
from pdf_generator import generate_pdf

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/signin/{username}")
def signin(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), username: str = None):
    candidates = get_candidates(db, skip=skip, limit=limit)
    for user in candidates:
        if user.name == username:
            return user
    return {"ErrorStatus": "No user found"}

@app.get("/parse-rss/")
def parse_rss():
    # Fetch and store vacancies when the server starts
    vacancies = fetch_rss_data()
    db = SessionLocal()
    for vacancy in vacancies:
        create_candidate(db=db, **vacancy)
    db.close()

    return {"message": "RSS data parsed successfully"}

@app.get("/candidates/")
def read_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    candidates = get_candidates(db, skip=skip, limit=limit)
    return candidates

@app.post("/submit-query")
def submit_query(query: str):
    words = query.split()
    db = SessionLocal()
    user = get_matched_candidates(db, words)
    if user:
        return user
    return {"ErrorStatus": "No matched user found"}

@app.post("/generate-cv/")
def generate_vacancy_pdf(candidate_id: int):
    db = SessionLocal()
    candidate = check_candidate(db, candidate_id)
    if candidate is None:
        return {"error": "Candidate not found"}
    
    filename = f"resume_{candidate.id}.pdf"
    candidate_data={
        "name": candidate.name,
        "skills": candidate.skills,
        "experience": candidate.experience,
        "source": candidate.source,
    }
    
    generate_pdf(candidate_data, filename)
    
    return {"message": "PDF generated successfully", "filename": filename}

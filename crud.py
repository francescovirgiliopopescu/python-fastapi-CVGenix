# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from models import Candidate
import re

def create_candidate(db: Session, name: str, skills: str, experience: str):
    db_candidate = Candidate(
        name=name,
        skills=skills,
        experience=experience
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidates(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Candidate).offset(skip).all()
    # return db.query(Candidate).offset(skip).limit(limit).all()

def signin(db: Session, username: str):
    return db.query(Candidate).filter(Candidate.name == username).first()

def get_matched_candidates(db: Session, words: list):
    users = []
    for word in words:
        if word.isdigit():
            users.extend(db.query(Candidate).filter(Candidate.experience == f"{word} years").all())
        elif re.search('\d+', word):
            exp = re.search('\d', word).group(0)
            users.extend(db.query(Candidate).filter(
                func.cast(func.regexp_replace(Candidate.experience, '\D', '', 'g'), Integer) >= exp
            ).all())
        else:
            users.extend(db.query(Candidate).filter(Candidate.skills.contains(word)).all())
    
    # Extract duplicated users
    duplicates = []
    seen = set()
    for i in users:
        if i in seen:
            duplicates.append(i)
        else:
            seen.add(i)
    return duplicates[:5]

def check_candidate(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()
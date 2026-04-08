import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlmodel import SQLModel, create_engine, Session, select, col
from .models import Mentor
import structlog

logger = structlog.get_logger()

DB_PATH = Path(__file__).resolve().parent.parent.parent / "mentors.db"
sqlite_url = f"sqlite:///{DB_PATH}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        statement = select(Mentor)
        results = session.exec(statement).first()
        if not results:
            seed_mentors(session)

def seed_mentors(session: Session):
    json_path = Path(__file__).parent / "seed_mentors.json"
    if not json_path.exists():
        logger.warning("seed_file_missing", path=str(json_path))
        return

    try:
        with open(json_path, "r") as f:
            mentors_data = json.load(f)
            
        for m in mentors_data:
            mentor = Mentor(
                name=m[0],
                company=m[1],
                title=m[2],
                avatar_url=m[3],
                tech_stack=m[4]
            )
            session.add(mentor)
        session.commit()
        logger.info("db_seeded", count=len(mentors_data))
    except Exception as e:
        logger.error("db_seed_failed", error=str(e))

def find_best_mentors(target_title: str, user_tools: List[str], limit: int = 1) -> List[Dict[str, Any]]:
    """Score mentors based on tech stack overlap and title relevance."""
    with Session(engine) as session:
        statement = select(Mentor)
        mentors = session.exec(statement).all()
        
    scored = []
    title_words = set(target_title.lower().split()) if target_title else set()
    user_tools_set = set(t.lower() for t in user_tools)

    for m in mentors:
        score = 0
        m_tech = set(t.lower().strip() for t in m.tech_stack.split(",")) if m.tech_stack else set()
        
        # Tech stack overlap (Weight: 3 per match)
        overlap = m_tech.intersection(user_tools_set)
        score += len(overlap) * 3
        
        # Title relevance (Weight: 2 per match)
        m_title_lower = m.title.lower() if m.title else ""
        for word in title_words:
            if word in m_title_lower:
                score += 2
        
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for s, m in scored[:limit]:
        results.append({
            "name": m.name,
            "company": m.company,
            "title": m.title,
            "avatar_url": m.avatar_url,
            "tech_stack": m.get_tech_stack()
        })
    return results

def get_session():
    with Session(engine) as session:
        yield session

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Player

router = APIRouter(prefix="/api/players")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from ..database import SessionLocal
from ..models import Game, GamePlayer

router = APIRouter(prefix="/api/games")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_game(payload: dict, db: Session = Depends(get_db)):
    game_date = date.fromisoformat(payload["date"])
    payer_id = payload["payer"]
    fetcher_id = payload["fetcher"]
    players = payload["players"]  # liste d'id

    game = Game(date=game_date, payer_id=payer_id, fetcher_id=fetcher_id)
    db.add(game)
    db.commit()
    db.refresh(game)

    for pid in players:
        jp = GamePlayer(game_id=game.id, player_id=pid)
        db.add(jp)

    db.commit()

    return {"status": "ok", "game_id": game.id}

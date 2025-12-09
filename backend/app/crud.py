from sqlmodel import Session, select
from .models import Game
from sqlmodel import SQLModel, create_engine
from typing import List
import json
from collections import Counter
from datetime import date

engine = create_engine("sqlite:///./coffee.db", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def add_game(session_date: date, participants: List[str], payer: str, fetcher: str, notes: str = None):
    g = Game(date=session_date,
             participants_json=json.dumps(participants),
             payer=payer,
             fetcher=fetcher,
             notes=notes)
    with Session(engine) as s:
        s.add(g)
        s.commit()
        s.refresh(g)
    return g

def list_games(limit: int=100, offset: int=0):
    with Session(engine) as s:
        st = select(Game).order_by(Game.date.desc()).offset(offset).limit(limit)
        return s.exec(st).all()

def compute_stats():
    with Session(engine) as s:
        all_games = s.exec(select(Game)).all()
    total = len(all_games)
    payers = Counter()
    fetchers = Counter()
    doublettes = 0
    seen_participants = Counter()
    for g in all_games:
        payers[g.payer] += 1
        fetchers[g.fetcher] += 1
        if g.payer == g.fetcher:
            doublettes += 1
        for p in g.participants():
            seen_participants[p] += 1
    return {
        "total_games": total,
        "payers": payers.most_common(),
        "fetchers": fetchers.most_common(),
        "doublettes": doublettes,
        "participants_counts": seen_participants.most_common()
    }

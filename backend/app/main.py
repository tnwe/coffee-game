from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from .crud import init_db, add_game, list_games, compute_stats
import json
from datetime import date
import pandas as pd
from io import BytesIO

app = FastAPI(title="Coffee Game API")
init_db()

class GameIn(BaseModel):
    date: Optional[date] = None
    participants: List[str]
    payer: str
    fetcher: str
    notes: Optional[str] = None

@app.post("/games")
def create_game(payload: GameIn):
    d = payload.date or date.today()
    g = add_game(d, payload.participants, payload.payer, payload.fetcher, payload.notes)
    return {"ok": True, "game": g}

@app.get("/games")
def get_games(limit: int = 100, offset: int = 0):
    return list_games(limit=limit, offset=offset)

@app.get("/stats")
def stats():
    return compute_stats()

@app.post("/import-excel")
async def import_excel(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    # expect columns: date, participants (comma separated), payer, fetcher, notes (optional)
    required = {"date","participants","payer","fetcher"}
    if not required.issubset(set(map(str.lower, df.columns))):
        raise HTTPException(status_code=400, detail="Excel must contain columns: date, participants, payer, fetcher")
    for _, row in df.iterrows():
        d = pd.to_datetime(row['date']).date()
        parts = [p.strip() for p in str(row['participants']).split(",") if p.strip()]
        add_game(d, parts, row['payer'], row['fetcher'], row.get('notes', None))
    return {"ok": True, "imported": len(df)}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "..", "frontend_dist")

if os.path.exists(FRONTEND_DIST):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIST), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

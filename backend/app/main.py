from fastapi import FastAPI
from .routers import players, games
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(players.router)
app.include_router(games.router)

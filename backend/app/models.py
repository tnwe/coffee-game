from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    payer_id = Column(Integer, ForeignKey("players.id"))
    fetcher_id = Column(Integer, ForeignKey("players.id"))

    payer = relationship("Player", foreign_keys=[payer_id])
    fetcher = relationship("Player", foreign_keys=[fetcher_id])

class GamePlayer(Base):
    __tablename__ = "game_players"
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)

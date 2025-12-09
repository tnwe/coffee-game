from sqlmodel import SQLModel, Field
from typing import Optional, List
import json
from datetime import date

class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    participants_json: str  # store JSON list of names
    payer: str
    fetcher: str
    notes: Optional[str] = None

    def participants(self) -> List[str]:
        try:
            return json.loads(self.participants_json)
        except:
            return []

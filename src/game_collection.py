from typing import List

from pydantic import BaseModel

from src.game_model import GameModel


class GameCollection(BaseModel):
    games: List[GameModel]

    class Config:
        validate_assignment = False

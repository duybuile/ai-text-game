from typing import Any, Dict

from bson import ObjectId
from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic_core import CoreSchema


class GameSchema(BaseModel):
    _id: ObjectId
    title: str
    description: str
    objective: str
    current_setting: str

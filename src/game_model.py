from typing import Optional, Any, Dict, Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class GameModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field()
    description: str = Field()
    objective: str = Field()
    current_setting: str = Field()

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

from bson import ObjectId
from fastapi import FastAPI, status, HTTPException

from src.game_collection import GameCollection
from src.game_model import GameModel
from src.utils.mongo import get_client, get_collection, fetch_all_data
from fastapi.middleware.cors import CORSMiddleware

client = get_client()
game_collection = get_collection(client, "collection")

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    "/games/",
    response_description="Create game",
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED
)
async def create_item(game: GameModel):
    try:
        result = game_collection.insert_one(game.dict())
        return str(result.inserted_id)
    except Exception as e:
        print("Error creating game:", e)


@app.get(
    "/games/",
    response_description="List all games",
    response_model=GameCollection,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
async def list_games():
    try:
        games = game_collection.find()
        if games:
            return GameCollection(games=games)
        else:
            return GameCollection(games=[])
    except Exception as e:
        print("Error listing games:", e)


@app.get(
    "/games/{game_id}",
    response_description="Get a single game",
    response_model=GameModel,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
async def get_game(game_id: str):
    """
    Get the record for a specific game, looked up by `id`.
    """
    if (
        game := game_collection.find_one({"_id": ObjectId(game_id)})
    ) is not None:
        return game

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game {game_id} not found")

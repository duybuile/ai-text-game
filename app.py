import os
from typing import Annotated

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from openai import OpenAI

from src.llms.prompt_eng import build_first_prompt, build_next_prompt
from src.utils.config import cfg
from src.utils.log_handler import setup_logger
from src.utils.mongo import fetch_one_data

from bson import ObjectId
from fastapi import FastAPI, status, HTTPException, Request, Depends

from src.game_collection import GameCollection
from src.game_model import GameModel
from src.utils.mongo import get_client, get_collection

client = get_client()
game_collection = get_collection(client)

logger = setup_logger(cfg["logging"]["filestream_logging"],
                      cfg["logging"]["filepath"],
                      cfg["logging"]["level"])

# User credentials for authentication

# Initialise app
app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
security = HTTPBasic()
loaded_bots = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_data = {}

conversations = []


def authenticate(user, password):
    # basic auth method
    assert os.getenv("AUTH_USER") is not None
    assert os.getenv("AUTH_PWD") is not None

    if not ((user == os.getenv("AUTH_USER")) and (password == os.getenv("AUTH_PWD"))):
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    authenticate(credentials.username, credentials.password)
    return {"Hello": "World"}


@app.post("/make_move")
async def generate_response(request: Request):
    global conversations
    request_data = await request.json()
    game_id = request_data['id']
    msg = request_data['msg']
    logger.debug(f'Game id: {game_id}')
    logger.debug(f'Message: {msg}')

    if msg.lower() in ("q", "exit"):
        conversations = []
        return {"message": "Conversation ended. Goodbye!"}

    # If the message is empty, we load the information from the mongo db
    if msg == '':
        # fetch document with the game_id from mongo db
        doc = fetch_one_data(game_collection, game_id)
        if doc is None:
            logger.error(f"Document with id {game_id} not found")
            return HTTPException(status_code=404, detail="Document not found")
        else:
            prompt = build_first_prompt(doc)
            logger.debug(f"AI: {prompt}")
    else:
        logger.debug(f"User: {msg}")
        # Limit conversation history to 3 messages
        if len(conversations) > 3:
            conversations = conversations[-3:]

        # Summarize the conversation history
        # summary = summarize_conversation(conversations)
        prompt = build_next_prompt(conversations, msg)

    try:
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = openai_client.chat.completions.create(
            model=cfg["openai"]["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=cfg["openai"]["temperature"],
        )
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {"message": "Oops! Something went wrong. Try again later."}

    # Add AI response to conversation history
    conversations.append({"role": "ai", "content": response.choices[0].message.content.strip()})
    logger.debug(f"AI: {response.choices[0].message.content.strip()}")

    return {"message": conversations[-1]["content"]}


#######
# GAME API
#######
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


# RUN!!!
if __name__ == "__main__":
    uvicorn.run(app, port=int(os.environ.get("PORT", 8000)), host="0.0.0.0")

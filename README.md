# AI Text Game

## Objectives
An AI to play a text-based game. It has the following function
1. Create a new game
2. Play a game
3. Quit the game

## Requirements
- Python 3.10

## Pre-requisites
- Install the following dependencies
```bash
pip install -r requirements.txt
```
- Set up file `.env` containing the following variables
```bash
HUGGINGFACE_TOKEN=<your huggingface token>
OPENAI_API_KEY=<your openai api key>
MONGODB_USER=<your mongodb user>
MONGODB_PASSWORD=<your mongodb password>
AUTH_USER=<your auth user>
AUTH_PWD=<your auth password>
STABILITY_KEY=<your stability key>
```
Note:
- The `AUTH_USER` and `AUTH_PWD` are used for the FastAPI authentication. You can use any username and password. But they should be included in the Authorization header.

## Usage
### Start your server
```bash
python app.py
```

## List of APIs
- `GET /`: Return "Hello World" to check if the server was started successfully
- `POST /make_move`: Make a move
- `POST /games`: Create a new game
- `GET /games`: Get all games
- `GET /games/{id}`: Get a game given an id

### POST /make_move
Request body
- `id`: The id of the game
- `msg`: The message from the user. 
  - If the message is empty, we start the game. 
  - If the message is `q` or `exit`, we end the game

Example
```json
{
    "id": "65ecb118cfae096591875b53",
    "msg": "hello"
}
```

Response
- `message`: The response message from the AI
- `image_prompt`: The image prompt from the AI to generate an image for the message
- `is_finished`: Whether the game is finished or not

Example
```json
{
    "message": "You wake up in the middle of a dark and eerie maze, with no idea how you got there. The walls are tall and made of cold stone, with twists and turns in every direction. You can hear the sound of your own heartbeat echoing through the corridors. \n\nAs you start to explore, you come across a fork in the path. To your left, you see a dimly lit corridor with strange markings on the walls. To your right, you hear the faint sound of running water. \n\nWhat will you do next? \n1. Go left \n2. Go right",
    "image_prompt": "Dark maze fork",
    "is_finished": false
}
```

### POST /games
Request body
- `title`: The title of the game
- `description`: The description of the game
- `objective`: The objective of the game
- `current_setting`: The current setting of the game
- `created_by`: The creator of the game

Example
```json
{
    "title": "Maze runner",
    "description": "A text game to escape from a maze",
    "objective": "Escape the maze to find the treasure in the end",
    "current_setting": "You are stuck in a maze. There are a lot of obstacles",
    "created_by": "duybuile"
}
```

Response
- `id`: The id of the game

Example
```json
{
    "id": "65ecb118cfae096591875b53"
}
```

## Contributors
- [Duy Bui](https://github.com/duybuile)

## License
MIT

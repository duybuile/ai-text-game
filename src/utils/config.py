import yaml
from dotenv import find_dotenv, load_dotenv


# Load environment variables from .env file
load_dotenv(find_dotenv())


# Import config vars
with open("config/config.yml", "r", encoding="utf8") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

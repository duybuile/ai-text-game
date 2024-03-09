import os
from datetime import datetime

import pymongo
from bson import ObjectId
from dotenv import find_dotenv, load_dotenv
from pymongo.collection import Collection

from src.utils.config import cfg
from src.utils.json_handler import read_from_json

mongo_cfg = cfg["MongoDB"]


def get_client():
    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    # Get the username and password from environment variables
    username = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")

    # Assert to make sure username and password are not None
    assert username is not None
    assert password is not None

    # Construct the connection string
    connection_string = f"mongodb+srv://{username}:{password}@{mongo_cfg['cluster']}.vuj2plc.mongodb.net/?retryWrites=true&w=majority&appName={mongo_cfg['cluster']}"

    # Connect to MongoDB
    client = pymongo.MongoClient(connection_string)
    return client


def get_collection(client: pymongo.MongoClient) -> Collection:
    # Get the database (create it if it doesn't exist)
    db = client[mongo_cfg["database"]]

    # Get the collection (create it if it doesn't exist)
    collection = db[mongo_cfg["collection"]]
    return collection


# Function to insert a document into the collection
def insert_data(collection: Collection, doc: dict):
    try:
        # Insert the document
        collection.insert_one(doc)
        print("Data inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


# Function to fetch all documents from the collection
def fetch_all_data(collection: Collection):
    try:
        # Find all documents
        documents = collection.find({})

        return documents
    except Exception as e:
        print("Error fetching data:", e)


def fetch_one_data(collection: Collection, doc_id: str):
    try:
        # Convert the string ID to a MongoDB ObjectId
        object_id = ObjectId(doc_id)
        # Find one document
        document = collection.find_one({"_id": object_id})

        # return document
        return document
    except Exception as e:
        print("Error fetching data:", e)


def delete_data(collection: Collection, doc_id: str):
    try:
        # Convert the string ID to a MongoDB ObjectId
        object_id = ObjectId(doc_id)
        # Delete the document
        collection.delete_one({"_id": object_id})
        print("Data deleted successfully!")
    except Exception as e:
        print("Error deleting data:", e)


def delete_all(collection: Collection):
    try:
        # Delete all documents
        collection.delete_many({})
        print("All data deleted successfully!")
    except Exception as e:
        print("Error deleting data:", e)


def example():
    # Connect to MongoDB
    client = get_client()
    collection = get_collection(client)

    # Read json data from file test/sample_prompt.json
    data = read_from_json("test/sample_prompt.json")

    # Add created_at to data as the current time
    data["created_at"] = str(datetime.now())

    # Insert data into the collection
    insert_data(collection, data)

    # Fetch all data
    fetch_all_data(collection)

    # Close the connection
    client.close()


if __name__ == '__main__':
    example()

"""
Contains all the utility functions for JSON
"""
import json
import logging

logger = logging.getLogger(__name__)


def write_to_json(dic: dict, json_file: str):
    """
    Write a dictionary to a JSON file
    :param dic:
    :param json_file:
    :return:
    """
    try:
        with open(json_file, "w") as output:
            json.dump(dic, output)
    except Exception as e:
        logger.error(f"Error in writing to JSON file {json_file}:{e}")


def read_from_json(json_file: str):
    """
    Read a dictionary from a JSON file
    :param json_file:
    :return:
    """
    try:
        with open(json_file, "r") as f:
            dic = json.load(f)
        return dic
    except Exception as e:
        logger.error(f"Error in reading from a JSON file {json_file}:{e}")

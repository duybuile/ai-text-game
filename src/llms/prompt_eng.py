from typing import Mapping, Any


def build_first_prompt(doc: Mapping[str, Any]) -> str:
    """
    We build the first prompt from the game document
    :param doc:
    :return:
    """
    objective = doc.get('objective', '')
    setting = doc.get('current_setting', '')
    description = doc.get('description', '')
    prompt = (
        f"You are going to be driving a text based game with description: {description} \n"
        f"The game revolves around the following: {setting} \n"
        f"The aim of the game is: {objective} \n"
        f"Generate the first step of the game"
    )
    return prompt


def build_next_prompt(conversations: list, msg: str) -> str:
    """
    We build the next prompt from the conversation
    :param msg:
    :param conversations:
    :return:
    """
    context = "\n".join([msg["content"] for msg in conversations])
    prompt = f"""Here is the conversation so far: {context}
    User response: {msg}
    Generate the next step of the game. 
    If the user has reached the end of the game, just write "end of game"."""
    return prompt


def build_image_prompt(msg: str) -> str:
    """
    We build a prompt to generate a smaller prompt to create an image
    given the message
    :param msg:
    :return:
    """
    return f"""I want to generate an image of a scene based on this paragraph. I need a simple straight forward prompt that tells what image to generate . Dont make the prompt too complex, just keep it simple to a few words. do not have any commas in the prompt. just keep it simple and straightforward on what to generate. \n
    Here is the paragraph: {msg}"""

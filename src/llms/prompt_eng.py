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
    prompt = (f"You are going to be driving a text based game with description: {description} \n"
              f"The game revolves around the following: {setting} \n"
              f"The aim of the game is: {objective}")
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
    Generate the next step of the game. If the user has reached the end of the game, just write "end of game"."""
    return prompt

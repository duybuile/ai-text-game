import base64
import os
import io
import warnings

import names
from PIL import Image
from dotenv import find_dotenv, load_dotenv
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from src.utils.config import cfg


# Sign up for an account at the following link to get an API Key.
# https://platform.stability.ai/

# Click on the following link once you have created an account to be taken to your API Key.
# https://platform.stability.ai/account/keys

def generate_image(prompt: str):
    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        host=cfg["stability"]["host"],
        key=os.environ['STABILITY_KEY'],  # API Key reference.
        verbose=True,  # Print debug messages.
        engine=cfg["stability"]["model"],  # Set the engine to use for generation.
    )

    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt=prompt,
        samples=1,  # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M,
        width=cfg["stability"]["width"],
        height=cfg["stability"]["height"],
        cfg_scale=7,
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    encoded_string = ""
    img_dir = cfg["stability"]["output"]
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(img_dir + "/" + str(names.get_last_name().lower()) + ".png")  # Save our image!
                encoded_string = convert_pillow_image_to_base64(artifact.binary)
    return encoded_string


def convert_image_to_base64(image_path):
    """
    Convert image to base64
    :param image_path:
    :return:
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def convert_pillow_image_to_base64(image):
    """
    Convert image to base64
    :param image:
    :return:
    """
    encoded_string = base64.b64encode(image)
    return encoded_string

# if __name__ == '__main__':
#     load_dotenv(find_dotenv())
#     encoding_str = generate_image("crazy cat running on the beach")
#     print(encoding_str)

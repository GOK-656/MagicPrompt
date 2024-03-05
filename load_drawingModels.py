import requests
import io
from PIL import Image
from huggerkey import *
# files saved at image.jpeg
def useRemoteModel(inputPromt,type:str):
    if (type=="stable-diffusion"):
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    if (type=="midjourney"):
        API_URL = "https://amidjourneypi-inference.huggingface.co/models/prompthero/openjourney"
    if (type=="lexica"):
        API_URL="https://api-inference.huggingface.co/models/openskyml/lexica-aperture-v3-5"
    if (type=="cascade"): # TODO: have some problem
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-cascade"
    headers = {"Authorization": "Bearer "+hugging_face_key}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    # sometimes the api is unavailable, TODO: figure unusual cases
    while True:
        try:
            image_bytes = query({
            "inputs": inputPromt,
        })
            print(image_bytes)
            image = Image.open(io.BytesIO(image_bytes))
            image.save("image" + type+".jpeg")
            break
        except Exception as e:
            pass
# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
# useRemoteModel("A big elephant","stable-diffusion")

import base64


def query(payload, API_URL):
    headers = {"Authorization": "Bearer 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"}
    for _ in range(5):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
    print('Server too busy')
    return None


# files saved at diffusion_image.jpeg
def diffusion_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    if image_bytes is None:
        return None, False
    # image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_bytes, True


def lexica_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/openskyml/lexica-aperture-v3-5"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    if image_bytes is None:
        return None, False
    # image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_bytes, True


def lora_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/openskyml/lcm-lora-sdxl-turbo"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    if image_bytes is None:
        return None, False
    # image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_bytes, True


def midjourney_image(inputPromt):
    API_URL = "https://api-inference.huggingface.co/models/openskyml/midjourney-v4-xl"

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    if image_bytes is None:
        return None, False
    # image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_bytes, True


# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
# print(diffusion_image("A big elephant"))

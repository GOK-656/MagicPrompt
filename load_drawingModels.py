import requests
import io
from PIL import Image
import base64


def query(payload, API_URL):
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


# files saved at diffusion_image.jpeg
def diffusion_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_base64


def lexica_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/openskyml/lexica-aperture-v3-5"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_base64


def lora_image(inputPromt):
    API_URL = (
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    )

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_base64


def midjourney_image(inputPromt):
    API_URL = "https://api-inference.huggingface.co/models/openskyml/midjourney-v4-xl"

    image_bytes = query(
        {"inputs": inputPromt},
        API_URL=API_URL,
    )
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("diffusion_image.jpeg")
    return image_base64


# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
# print(diffusion_image("A big elephant"))

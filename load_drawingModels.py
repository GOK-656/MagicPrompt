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
useRemoteModel("A big elephant","stable-diffusion")


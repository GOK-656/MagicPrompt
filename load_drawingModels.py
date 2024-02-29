import requests
import io
from PIL import Image

# files saved at diffusion_image.jpeg
def diffusion_image(inputPromt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer "}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    image_bytes = query({
        "inputs": inputPromt,
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.save("diffusion_image.jpeg")
# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
diffusion_image("A big elephant")
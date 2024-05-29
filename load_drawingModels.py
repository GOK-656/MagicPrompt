import requests
import io
from PIL import Image
import base64
from get_key import get_key


class ImageGenerator:
    def __init__(self):
        self.key = get_key()
        self.urls = {
            "stable_diffusion": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            "lexica": "https://api-inference.huggingface.co/models/openskyml/lexica-aperture-v3-5",
            "lora": "https://api-inference.huggingface.co/models/openskyml/lcm-lora-sdxl-turbo",
            "midjourney": "https://api-inference.huggingface.co/models/openskyml/midjourney-v4-xl",
        }

    def query(self, payload, API_URL):
        headers = {"Authorization": f"Bearer {self.key}"}
        for _ in range(5):
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.content
        print('Server too busy')
        return None
    
    def draw(self, model_name, input_prompt):
        API_URL = self.urls[model_name]
        image_bytes = self.query(
            {"inputs": input_prompt},
            API_URL=API_URL,
        )
        if image_bytes is None:
            return None, False
        return image_bytes, True

# # You can access the image with PIL.Image for example
# import io
# from PIL import Image
# ImageGenerator().draw("stable_diffusion", "A big elephant")
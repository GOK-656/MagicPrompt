import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {{TODO:API KEY}}"}

def image2textFilename(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]
def image2textData(data):
    print(data)
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]

# output = image2textFilename("/home/wznmickey/Pictures/20230130-153108.jpeg")

# print(output)
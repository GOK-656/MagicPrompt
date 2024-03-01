import requests

API_URL = (
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
)

# todo: api token
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def image2textFilename(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]


def image2textData(data):
    print(data)
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]["generated_text"]


# def img2url(img):
#     API_TOKEN = ""
#     upload_url = "https://sm.ms/api/v2/upload"
#     # print("Uploading image...")
#     response = requests.post(
#         upload_url, files={"smfile": img}, headers={"Authorization": API_TOKEN}
#     )
#     if response.status_code == 200:
#         data = response.json()
#         if data["code"] == "success":
#             print("Image uploaded successfully!")
#             print("Image URL:", data["data"]["url"])
#         else:
#             print("Upload failed:", data["message"])
#     else:
#         print("Error occurred during upload:", response.status_code)


# output = image2textFilename("/home/wznmickey/Pictures/20230130-153108.jpeg")

# print(output)

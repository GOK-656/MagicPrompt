import requests
from get_key import get_key

def prompt_generator(input_text):
    API_URL = "https://api-inference.huggingface.co/models/succinctly/text2image-prompt-generator"
    key = get_key()
    headers = {"Authorization": f"Bearer {key}"}
    input = {"inputs": input_text}
    while True:
        response = requests.post(API_URL, headers=headers, json=input)
        try:
            generated_text = response.json()[0]["generated_text"]
            break
        except:
            continue

    print(response.json())
    return generated_text


# output = prompt_generator(
#     {
#         "inputs": "A mountain in spring with white cloud",
#     }
# )

# print(output)
# print(output[0]["generated_text"])
# print(prompt_generator("A mountain in spring with white cloud"))

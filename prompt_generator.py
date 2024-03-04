import requests


def prompt_generator(input_text):
    API_URL = "https://api-inference.huggingface.co/models/succinctly/text2image-prompt-generator"
    headers = {"Authorization": "Bearer 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"}
    input = {"inputs": input_text}
    response = requests.post(API_URL, headers=headers, json=input)
    return response.json()[0]["generated_text"]


# output = prompt_generator(
#     {
#         "inputs": "A mountain in spring with white cloud",
#     }
# )

# print(output)
# print(output[0]["generated_text"])
# print(prompt_generator("A mountain in spring with white cloud"))

import replicate

def getResult(inputPromt):
    print("intoIt")
    output = replicate.run(
        "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
        input={
            "image": open("temp.jpeg", "rb"),
            "prompt": inputPromt,
            "scheduler": "K_EULER_ANCESTRAL",
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "num_inference_steps": 100,
            "image_guidance_scale": 1.5
        }
    )
    print(output)
    return output
# import replicate
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
from bs4 import BeautifulSoup
import requests
import re
import time
from urllib.parse import urlparse
from PIL import Image
import os
import base64
from io import BytesIO


def get_pix2pix_result(inputPromt, savePath, steps=10, text_cfg=7.5, img_cfg=1.5):
    print(inputPromt)
    # initialize Selenium WebDriver
    url = "https://huggingface.co/spaces/timbrooks/instruct-pix2pix"
    options = Options()
    driver = webdriver.Firefox(options=options)
    script = """
    Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
    })
    """
    driver.execute_script(script)
    driver.get(url)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    currentPath = os.getcwd()
    file_input.send_keys(os.path.join(currentPath, savePath))
    textarea = driver.find_element(By.CSS_SELECTOR, "textarea[data-testid='textbox']")
    textarea.clear()
    textarea.send_keys(inputPromt)

    parameters = driver.find_elements(By.CLASS_NAME, "gr-box.gr-input.w-full.gr-text-input")
    parameters[1].clear()
    parameters[1].send_keys(steps)
    parameters[3].clear()
    parameters[3].send_keys(text_cfg)
    parameters[4].clear()
    parameters[4].send_keys(img_cfg)

    generate_button = driver.find_element(By.ID, "component-4")
    generate_button.click()

    # img_element = driver.find_element(By.CSS_SELECTOR, "#component-14 img")

    max_attempts = 50
    attempt = 0

    while attempt < max_attempts:
        try:
            img_element = driver.find_element(By.CSS_SELECTOR, "#component-14 img")
            break
        except NoSuchElementException:
            print(f"Element not found, attempt {attempt+1}...")
            attempt += 1
            time.sleep(2)

    if attempt == max_attempts:
        print("Element not found after maximum attempts.")
        return None, False

    img_src = img_element.get_attribute("src")
    img_src = img_src.split(",")[1]
    # img_data = base64.b64decode(img_src)
    # img = Image.open(BytesIO(img_data))
    # img.save("output.jpg")

    # output = replicate.run(
    #     "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
    #     input={
    #         "image": open("temp.jpeg", "rb"),
    #         "prompt": inputPromt,
    #         "scheduler": "K_EULER_ANCESTRAL",
    #         "num_outputs": 1,
    #         "guidance_scale": 7.5,
    #         "num_inference_steps": 100,
    #         "image_guidance_scale": 1.5
    #     }
    # )
    # print(output)
    # return output
    return img_src, True


# get_pix2pix_result("add a bird to the sky", 'temp.jpg')

# import replicate
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import requests
import re
import time
from urllib.parse import urlparse
from PIL import Image
import os


def getResult(inputPromt):
    print("intoIt")
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
    print(os.path.join(app.config["UPLOAD_FOLDER"], "test.jpg"))
    # file_input.send_keys(os.path.join(app.config["UPLOAD_FOLDER"], "test.jpg"))
    textarea = driver.find_element(By.CSS_SELECTOR, "textarea[data-testid='textbox']")
    textarea.clear()
    textarea.send_keys(inputPromt)
    generate_button = driver.find_element(By.ID, "component-4")
    generate_button.click()
    img_element = driver.find_element(By.CSS_SELECTOR, "#component-14 img")
    img_src = img_element.get_attribute("src")
    img_src.save("result.jpeg")
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


getResult("add a glass")

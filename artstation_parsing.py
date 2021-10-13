from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
import PIL 
from helium import *
from io import BytesIO
import time

page_url = 'https://www.artstation.com/search?sort_by=relevance&query=landscape'
driver = start_firefox(page_url, headless=True)

# https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    print(time.monotonic())
    
    
html = driver.page_source

page_soup = BeautifulSoup(html, "html.parser")
img_soups = page_soup.findAll('img', class_='d-block')

with open('img_urls.txt', 'w', encoding='utf-8') as f:
    for img_soup in tqdm(list(img_soups)):
        f.write(img_soup['src'] + '\n')
        
img_soup = img_soups[5]

# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
response = requests.get(img_soup['src'])
img = PIL.Image.open(BytesIO(response.content))

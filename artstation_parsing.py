from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
import PIL 
from helium import *
from io import BytesIO

page_url = 'https://www.artstation.com/search?sort_by=relevance&query=landscape'
browser = start_firefox(page_url, headless=True)
html = browser.page_source

page_soup = BeautifulSoup(html, "html.parser")
img_soups = page_soup.findAll('img', class_='d-block')
img_soup = img_soups[5]

# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
response = requests.get(img_soup['src'])
img = PIL.Image.open(BytesIO(response.content))

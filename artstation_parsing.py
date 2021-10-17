from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np

from helium import *
from PIL import Image, ImageFilter, ImageOps 
from io import BytesIO
import time
from matplotlib import pyplot as plt

page_url = 'https://www.artstation.com/search?sort_by=relevance&query=landscape'
page_url = 'https://www.artstation.com/search?sort_by=relevance&query=landscape&medium_ids=1&category_ids=5'
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
        
with open('img_urls.txt', 'r', encoding='utf-8') as f:
    img_urls = [str(i) for i in f.readlines()]

img_url = img_urls[np.random.randint(7150)]


# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))
def make_thumbnail(img, thumbnail_size=64):
    size = thumbnail_size, thumbnail_size
    thumb = img.convert('L').filter(ImageFilter.MedianFilter(size=31))
    thumb.thumbnail(size)
    return thumb

plt.imshow(make_thumbnail(img), cmap='gray')
thumb_processed = thumb.filter(ImageFilter.MedianFilter(size=5))
plt.imshow(thumb_processed, cmap='gray')

for i, img_url in enumerate(tqdm(img_urls)):
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        thumb = make_thumbnail(img)
        
        img.save('images/'+str(i)+'.jpeg')
        thumb.save('thumbs/'+str(i)+'.jpeg')
    except:
        print('Ошибка: ', i)
        
#  29%|██▊       | 2038/7150 [34:50<1:10:25,  1.21it/s]Ошибка:  2037
#  51%|█████     | 3654/7150 [1:01:14<42:48,  1.36it/s]  Ошибка:  3653
# 100%|██████████| 7150/7150 [1:57:09<00:00,  1.02it/s]  
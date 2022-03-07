import requests
from tqdm import tqdm
import numpy as np

from helium import *
from PIL import Image, ImageFilter, ImageOps 
from io import BytesIO
from matplotlib import pyplot as plt

        
with open('data/img_urls.txt', 'r', encoding='utf-8') as f:
    img_urls = [str(i) for i in f.readlines()]

img_url = img_urls[np.random.randint(7150)]


# https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

for i, img_url in enumerate(tqdm(img_urls)):
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content)).thumbnail((256,256))  
        img.save('images/'+str(i)+'.jpeg')
    except:
        print('Error on the url: ', i)
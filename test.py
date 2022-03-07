import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
# import tensorflow_transform as tft
import tensorflow_addons as tfa
import math
import os
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import lab2rgb
import seaborn as sns
import tensorflow_io as tfio
# from tfio.experimental.color import rgb_to_lab
rgb_to_lab = tfio.experimental.color.rgb_to_lab
AUTOTUNE = tf.data.experimental.AUTOTUNE
COLOR_MODEL = 'lab'
IMAGE_SIZE = 224
import segmentation_models

def load(image_file):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    image = tf.image.resize(image, [IMAGE_SIZE, IMAGE_SIZE])
    
    if COLOR_MODEL == 'lab':
        image = rgb_to_lab(image)
        lightness = image[:,:,0]
        lightness = lightness/50-1
        lightness = lightness[...,tf.newaxis]
        color = image[:,:,1:]/100
        return lightness, color
    else:
        lightness = tf.image.rgb_to_grayscale(image)
        image = image*2 - 1
#     lightness = image[:,:,0]
#     lightness = lightness/100
#     lightness = lightness[...,tf.newaxis]
#     color = image[:,:,1:]/100
    
        return lightness, image

def get_image(input):
    if COLOR_MODEL == 'lab':
        l, ab = input
        image = np.zeros((IMAGE_SIZE,IMAGE_SIZE,3))
        image[:,:,:1] = l[0,...]*50+50
        image[:,:,1:] = ab[0,...]*100
        image = lab2rgb(image)
        lightness = np.array(l[0,...,0])
        return image, lightness
    else:
        lightness, image = input
        image = lab2rgb(image*100)
    
        return image[0,...], lightness[0,...,0]

def color_hist(color):
    for i in range(color.shape[-1]):
        sns.distplot(color[...,i])

def check_images(light, color):
    image, lightness = get_image((light, color))
    plt.figure(figsize=(10,10))
    plt.subplot(1,2,1)
    plt.imshow(tf.squeeze(lightness), cmap='gray')
    plt.subplot(1,2,2)
    plt.imshow(tf.squeeze(image))
    
image_file = 'data/images/2.jpeg'
bw, color = load(image_file)
check_images(bw[tf.newaxis,...], color[tf.newaxis,...])
inp = bw[tf.newaxis,...]
example_input = [tf.zeros_like(inp)]*7
example_input.append(inp)
example_input = tf.concat(example_input, axis=0)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

OUTPUT_CHANNELS = 3
if COLOR_MODEL=='lab':
    OUTPUT_CHANNELS = 2

segmentation_models.set_framework('tf.keras')
def Generator():
    unet = segmentation_models.Unet('mobilenet', encoder_weights='imagenet', classes=OUTPUT_CHANNELS, activation='tanh', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    inp = layers.Input(shape=[IMAGE_SIZE, IMAGE_SIZE, 1], name='input')
    x = layers.Concatenate()([inp, inp, inp])
    x = unet(x)
#     x = tf.linalg.normalize(x)[0]
    model = tf.keras.Model(inputs=inp, outputs=x)
    return model

generator = Generator()



generator = tf.keras.models.load_model('data/generator_lab_gan_art')

gen_out = generator(example_input, training=False)
check_images(example_input[-1:], gen_out[-1:])

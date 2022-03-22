# Landscape Colorization

## Motivation

There is an approach to making digital painting landscapes where you do a grayscale image first and then color it using different blend modes in your graphics editor. But it appears that I am really bad at coloring my grayscale sketches and find the process rather tedious. So I thought, what if we had a model that does the coloring automatically based on the dataset of different existing paintings.



## Approach
We need a model that predicts the color given the grayscale image.

Basically, I used the approach described in ["Colorizing black & white images with U-Net and conditional GAN — A Tutorial"](https://towardsdatascience.com/colorizing-black-white-images-with-u-net-and-conditional-gan-a-tutorial-81b2df111cd8) but with TensorFlow. 

First I had to scrape [ArtStation](https://www.artstation.com/) "Landscape" search results for small thumbnails of the works. 

Then I took a pre-trained classification model (ResNet18 in my case), used it as a backbone for U-Net (or similar pix2pix architecture) model, then trained U-Net on our dataset, then used the trained U-Net as a generator part of trained GAN and finally trained the whole сGAN on our dataset.



## Results

### Good results

![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_13.png)
![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_66.png)
![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_97.png)
### Not-So-Good results
![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_1.png)
![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_3.png)
![This is an image](https://github.com/Victor-A-Orlov/Landscape-Colorization/blob/main/images/__results___52_8.png)

As we can see, the model do well with one specific sort of composition end environment but struggles with anything more unusual.


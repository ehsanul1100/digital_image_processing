# Draw histogram of an image without using library function
import os
from PIL import Image
import matplotlib.pyplot as plt

def plt_hist(hist_r, hist_g, hist_b):
    plt.figure(figsize=(10,4))
    plt.plot(hist_r, color='red', label='Red')
    plt.plot(hist_g,color='green', label='Green')
    plt.plot(hist_b,color='blue',label='Blue')

    plt.xlabel('Intensity value (0-255)')
    plt.ylabel('Normalized Frequecy / Probability')
    plt.title('RGB Histogram')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def hist_cal(image):
    hist_r = [0] * 256
    hist_g = [0] * 256
    hist_b = [0] * 256
    pixels = image.load()
    width,height = image.size
    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x,y]
            hist_r[r] +=1
            hist_g[g] +=1
            hist_b[b] +=1
    m = width * height
    for i in range(256):
        hist_r[i] = (hist_r[i] / m)
        hist_g[i] = (hist_g[i] / m)
        hist_b[i] = (hist_b[i] / m)

    return hist_r,hist_g,hist_b

def main():
    original_img=Image.open("img_1.jpg")

    hist_r,hist_g,hist_b=hist_cal(original_img)
    plt_hist(hist_r,hist_g,hist_b)


if __name__=="__main__":
    main()


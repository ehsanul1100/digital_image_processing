# Implementation of some basic gray-level/intensity transformations
# a. negative image
# b. log transformation
# c. power-law (gamma) transformation 

import os
from PIL import Image
import math

def negative_image(image):
    width, height = image.size
    negative = Image.new("RGB", (width, height))
    pixels = image.load()
    out_pixels = negative.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x,y]
            out_pixels[x,y] = (255 - r, 255 - g, 255 - b)
    return negative


def log_transformation(image):
    width, height = image.size
    log_image = Image.new("RGB", (width, height))
    pixels = image.load()
    out_pixels = log_image.load()
    
    c = 255 / math.log(1 + 255)
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x,y]
            s_r = c * math.log(1 + r)
            s_g = c * math.log(1 + g)
            s_b = c * math.log(1 + b)
            out_pixels[x,y] = (int(s_r), int(s_g), int(s_b))
    return log_image


def power_law_gamma_transformation(image, gamma):
    width, height = image.size
    power_law_gamma_image = Image.new("RGB", (width, height))
    pixels = image.load()
    out_pixels = power_law_gamma_image.load()
    
    c = 255 / (255 ** gamma)
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x,y]
            s_r = c * (r ** gamma)
            s_g = c * (g ** gamma)
            s_b = c * (b ** gamma)
            out_pixels[x,y] = (int(s_r), int(s_g), int(s_b))
    
    return power_law_gamma_image

def main():
    # load image
    original_image = Image.open("img_1.jpg").convert("RGB")
    
    # create transformations 
    neg_image = negative_image(original_image)
    log_image = log_transformation(original_image)
    power_law_gamma_image = power_law_gamma_transformation(original_image, 0.5)
    
    # save outputs
    output_folder = "out_put_images"
    os.makedirs(output_folder, exist_ok=True)

    neg_image.save(os.path.join(output_folder, "negative_image.jpg"))
    log_image.save(os.path.join(output_folder, "log_transformed.jpg"))
    power_law_gamma_image.save(os.path.join(output_folder, "gamma_transformed.jpg"))

    print("All transformations completed successfully.")


if __name__ == "__main__":
    main()
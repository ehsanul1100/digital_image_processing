# implementation of binary representation of an image

import os
from PIL import Image

def apply_binary(val,thr=128,hi=255,low=0):
    if val >= thr:
        return hi
    return low

def binary_representation(image,thr=128,hi=255,low=0):
    width,height = image.size
    binary_img = Image.new("L",(width, height))
    pixels=image.load()
    out_pixels = binary_img.load()

    for y in range(height):
        for x in range(width):
            out_pixels[x,y] = apply_binary(pixels[x,y])
    return binary_img


def main():
    # Load image
    original_image = Image.open("img_1.jpg").convert("L")

    # Operations
    binary_representation_img = binary_representation(original_image, thr=128,hi=255,low=0)
    
    # save outputs 
    output_folder = "out_put_images"
    os.makedirs(output_folder, exist_ok=True)

    binary_representation_img.save(os.path.join(output_folder,"binary_representation.jpg"))

    print("All operations completed successfully")

if __name__ == "__main__":
    main()

# Implementation of contrast stretching and grey-level slicing
import os
from PIL import Image


def apply_contrast(value, r1, s1, r2, s2):
    if r2 == r1:
        return s1
    if value <= r1:
        return s1
    if value >= r2:
        return s2
    return int(((value - r1)/(r2 - r1)) * (s2 - s1) + s1)


def contrast_stretching(image, r1=0, r2=255, s1=0, s2=255):
    width, height = image.size
    stretched_image = Image.new("RGB", (width, height))
    pixels = image.load()
    out_pixels = stretched_image.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x,y]
            out_pixels[x,y] = (
                apply_contrast(r, r1, s1, r2, s2),
                apply_contrast(g, r1, s1, r2, s2),
                apply_contrast(b, r1, s1, r2, s2)
            )
    return stretched_image

def apply_slicing(value, lower_bound, upper_bound, highlight_val=255, preserve_background=False):
    """
    Slices an intensity value.
    If value is within [lower_bound, upper_bound], it gets highlighted.
    Otherwise, it is either kept as original or suppressed to 0.
    """
    if lower_bound <= value <= upper_bound:
        return highlight_val
    else:
        return value if preserve_background else 0
    
def gray_level_slicing(image, lower_bound=100, upper_bound=200, highlight_val=255, preserve_background=False):
    width, height = image.size
    sliced_image = Image.new("RGB", (width, height))
    pixels = image.load()
    out_pixels = sliced_image.load()

    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x,y]
            out_pixels[x,y] = (
                apply_slicing(r,lower_bound,upper_bound,highlight_val,preserve_background),
                apply_slicing(g,lower_bound,upper_bound,highlight_val,preserve_background),
                apply_slicing(b,lower_bound,upper_bound,highlight_val,preserve_background),
            )
    return sliced_image

def main():
    # Load image
    original_image = Image.open("img_1.jpg").convert("RGB")

    # Operations
    contrast_stretching_img = contrast_stretching(original_image, r1=50,r2=150,s1=10,s2=200)
    gray_level_slicing_img = gray_level_slicing(original_image,lower_bound=100,upper_bound=200,highlight_val=255,preserve_background=True)
    
    # save outputs 
    output_folder = "out_put_images"
    os.makedirs(output_folder, exist_ok=True)

    contrast_stretching_img.save(os.path.join(output_folder,"contrast_stretching.jpg"))
    gray_level_slicing_img.save(os.path.join(output_folder,"gray_level_slicing.jpg"))

    print("All operations completed successfully")

if __name__ == "__main__":
    main()
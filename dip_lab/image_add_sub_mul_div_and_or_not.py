from PIL import Image

def add_image (image1, image2):
    temp_image1 = image1.copy()
    temp_image2 = image2.copy()
    pixels1 = temp_image1.load()
    pixels2 = temp_image2.load()
    added_image = Image.new("RGB", max(image1.width, image1.width), max(image1.height, image2.height))
    added_pixels = added_image.load()
    for i in range(added_image.width):
        for j in range(added_image.height):
            if i < image1.width and j < image1.height:
                r1, g1, b1 = pixels1[i, j]
            else:
                r1, g1, b1 = 0, 0, 0
            if i < image2.width and j < image2.height:
                r2, g2, b2 = pixels2[i, j]
            else:
                r2, g2, b2 = 0, 0, 0
            r = min(r1 + r2, 255)
            g = min(g1 + g2, 255)
            b = min(b1 + b2, 255)
            added_pixels[i, j] = (r, g, b)
from PIL import Image
import matplotlib.pyplot as plt

def brightness_modify(image, factor):
    modified_image = image.copy()
    pixels = modified_image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            r = min(int(r * factor), 255)
            g = min(int(g * factor), 255)
            b = min(int(b * factor), 255)
            pixels[i, j] = (r, g, b)
    return modified_image
def add_border(image, border_size):
    modified_image = image.copy()
    pixels = modified_image.load()
    new_width = image.width + 2 * border_size
    new_height = image.height + 2 * border_size
    new_image = Image.new("RGB", (new_width, new_height), (0,0,0))
    new_image_pixels = new_image.load()
    if border_size > 0 :
        for i in range(new_width):
            for j in range(new_height):
                if(i < border_size or i >= image.width + border_size or j < border_size or j >= image.height + border_size):
                    new_image_pixels[i, j] = (255,255,255)
                else:
                    new_image_pixels[i, j] = image.getpixel((i - border_size, j - border_size))
    return new_image
                
def histogram_visualization(image):
    modified_image = image.copy()
    pixels = modified_image.load()
    r_histogram = [0] * 256
    g_histogram = [0] * 256
    b_histogram = [0] * 256
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            r_histogram[r] += 1
            g_histogram[g] += 1
            b_histogram[b] += 1
    for i in range(256):
        r_histogram[i] = r_histogram[i] / (image.width * image.height)
        g_histogram[i] = g_histogram[i] / (image.width * image.height)
        b_histogram[i] = b_histogram[i] / (image.width * image.height)
    return r_histogram, g_histogram, b_histogram
def plot_hist_prob(r_hist, g_hist, b_hist):
    bins = range(256)
    plt.figure(figsize=(10,4))
    plt.plot(bins, r_hist, color='red',  label='Red')
    plt.plot(bins, g_hist, color='green',label='Green')
    plt.plot(bins, b_hist, color='blue', label='Blue')
    plt.xlabel('Intensity (0-255)')
    plt.ylabel('Probability')
    plt.title('Color Histogram (Probability)')
    plt.legend(loc='upper right')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    # plt.savefig("histogram_probability.png", dpi=150)  # optional save

print("give the image path")
image_path = str(input())
image = Image.open(image_path)
image.show(title="Original Image")
brightness_factor = float(input("give the brightness factor (e.g., 1.2 for 20% brighter): "))
brightness_modified_image = brightness_modify(image, brightness_factor)
brightness_modified_image.show(title="Brightness Modified Image")
delay = input("Press Enter to continue...")
brightness_modified_image.close()
border_size = int(input("give the border size (e.g., 10 for 10 pixels): "))
border_modified_image = add_border(image, border_size)
border_modified_image.show(title="Border Modified Image")
border_modified_image.close()
r_hist, g_hist, b_hist = histogram_visualization(image)
# now we need to visualize the histograms, but since we are not using any plotting library, we will just print the histograms as lists
image.show(title="Original Image")
print("Image Size:", image.size)
print("Red Histogram:", r_hist)
print("Green Histogram:", g_hist)
print("Blue Histogram:", b_hist)

plot_hist_prob(r_hist, g_hist, b_hist)
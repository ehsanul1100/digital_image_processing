# implement histogram equalization and plot equalized and original histogram 
import os
from PIL import Image
import matplotlib.pyplot as plt

def plot_hist(hist_r,hist_g,hist_b,title="RGB Histogram"):
    plt.figure(figsize=(10,4))
    plt.plot(hist_r,color='red',label="Red")
    plt.plot(hist_g,color="green", label="Green")
    plt.plot(hist_b,color='blue',label="Blue")
    plt.xlabel("Intensity (0-255)")
    plt.ylabel("Normalized Frequecy / Probability")
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def cal_hist(image):
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
    return hist_r, hist_g, hist_b

def hist_equ(ori_img,hist_r, hist_g, hist_b):
    width, height = ori_img.size
    eq_img = Image.new("RGB",(width,height))
    pixls = ori_img.load()
    out_pixls = eq_img.load()
    lut_r,lut_g,lut_b = [0] * 256,[0] * 256,[0]*256
    s_r,s_g,s_b = 0.0,0.0,0.0
    for i in range(256):
        s_r += hist_r[i]
        s_g += hist_g[i]
        s_b += hist_b[i]
        lut_r[i] = round(s_r*255)   
        lut_g[i] = round(s_g*255)    
        lut_b[i] = round(s_b*255) 
    for y in range(height):
        for x in range(width):
            r,g,b = pixls[x,y]
            out_pixls[x,y] = (
                lut_r[r],
                lut_g[g],
                lut_b[b],
            )   
    return eq_img

def main():
    ori_img = Image.open("img_1.jpg")
    hist_r,hist_g,hist_b = cal_hist(image=ori_img)
    eq_img = hist_equ(ori_img,hist_r,hist_g,hist_b)
    plot_hist(hist_r,hist_g,hist_b,"RGB Hist for original image")
    eq_h_r, eq_h_g,eq_h_b = cal_hist(eq_img)
    plot_hist(eq_h_r,eq_h_g,eq_h_b,"RGB Hist for equalized image")

    eq_img.save(os.path.join("out_put_images","hist_equalized.jpg"))
    print("hist equally saved")


if __name__ == "__main__":
    main()
    
    
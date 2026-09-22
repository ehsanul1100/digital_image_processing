import os
from PIL import Image

# 1. Load images and convert to RGB
img_1 = Image.open('img_1.jpg').convert('RGB')
img_2 = Image.open('img_2.jpg').convert('RGB')

w, h = img_1.size

# Ensure both images have the same dimensions for pixel-by-pixel operations
img_2 = img_2.resize((w, h))

pix1 = img_1.load()
pix2 = img_2.load()

# 2. Create all output canvas images
add_img = Image.new("RGB", (w, h))
sub_img = Image.new("RGB", (w, h))
mul_img = Image.new("RGB", (w, h))
div_img = Image.new("RGB", (w, h))

and_img = Image.new("RGB", (w, h))
or_img  = Image.new("RGB", (w, h))
not_img = Image.new("RGB", (w, h))

# Load pixel access for all outputs
p_add = add_img.load()
p_sub = sub_img.load()
p_mul = mul_img.load()
p_div = div_img.load()

p_and = and_img.load()
p_or  = or_img.load()
p_not = not_img.load()

# 3. Calculate all operations inside a single nested loop
for y in range(h):
    for x in range(w):
        r1, g1, b1 = pix1[x, y]
        r2, g2, b2 = pix2[x, y]

        # --- Arithmetic Operations ---
        # ADD: clamp to max 255
        p_add[x, y] = (min(r1 + r2, 255), min(g1 + g2, 255), min(b1 + b2, 255))

        # SUB: clamp to min 0
        p_sub[x, y] = (max(r1 - r2, 0), max(g1 - g2, 0), max(b1 - b2, 0))

        # MUL: normalized by 255 so intensities stay within 0-255
        p_mul[x, y] = ((r1 * r2) // 255, (g1 * g2) // 255, (b1 * b2) // 255)

        # DIV: divide with safe check (add 1 to avoid zero-division)
        p_div[x, y] = (
            min(int((r1 / (r2 + 1)) * 255), 255),
            min(int((g1 / (g2 + 1)) * 255), 255),
            min(int((b1 / (b2 + 1)) * 255), 255)
        )

        # --- Logical Operations ---
        # AND: bitwise &
        p_and[x, y] = (r1 & r2, g1 & g2, b1 & b2)

        # OR: bitwise |
        p_or[x, y] = (r1 | r2, g1 | r2, b1 | b2)

        # NOT: invert image 1 (255 - value)
        p_not[x, y] = (255 - r1, 255 - g1, 255 - b1)

# 4. Save output images
output_dir = "out_put_images"
os.makedirs(output_dir, exist_ok=True)

add_img.save(os.path.join(output_dir, "addition.jpg"))
sub_img.save(os.path.join(output_dir, "subtraction.jpg"))
mul_img.save(os.path.join(output_dir, "multiplication.jpg"))
div_img.save(os.path.join(output_dir, "division.jpg"))

and_img.save(os.path.join(output_dir, "logical_and.jpg"))
or_img.save(os.path.join(output_dir, "logical_or.jpg"))
not_img.save(os.path.join(output_dir, "logical_not.jpg"))

print("All arithmetic and logical images saved successfully to out_put_images.")

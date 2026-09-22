import os
from PIL import Image

# ==========================================
# 1. Individual 3x3 Operations
# ==========================================

def mean_op(window):
    """Average of the 9 neighbor pixels."""
    return sum(window) // 9


def median_op(window):
    """Middle element after sorting the 9 pixels."""
    return sorted(window)[4]


GAUSS_KERNEL = [
    1, 2, 1,
    2, 4, 2,
    1, 2, 1
]

def gaussian_op(window):
    """Weighted sum using Gaussian 3x3 kernel divided by 16."""
    val = sum(w * p for w, p in zip(GAUSS_KERNEL, window))
    return val // 16


# --- Edge Detection & Sharpening ---

# 8-neighbor Laplacian (center must be 8 so flat areas sum to 0)
LAPLACIAN_KERNEL = [
    -1, -1, -1,
    -1,  8, -1,
    -1, -1, -1
]

def edge_op(window):
    """
    Laplacian edge detection.
    Using abs() ensures both positive and negative gradients show as bright edges!
    """
    val = sum(w * p for w, p in zip(LAPLACIAN_KERNEL, window))
    return min(abs(val), 255)


SHARPEN_KERNEL = [
     0, -1,  0,
    -1,  5, -1,
     0, -1,  0
]

def sharpen_op(window):
    """Image sharpening (clamped between 0 and 255)."""
    val = sum(w * p for w, p in zip(SHARPEN_KERNEL, window))
    return min(max(val, 0), 255)


# ==========================================
# 2. Optimized Single-Pass Filter Engine
# ==========================================

def process_all_filters(image):
    """
    Extracts the 3x3 window ONCE per pixel and computes all 5 filters
    simultaneously in a single pass. 5x faster!
    """
    width, height = image.size
    pixels = image.load()

    # Create output images (edge_img is monochromatic "L" mode)
    mean_img    = Image.new("RGB", (width, height))
    median_img  = Image.new("RGB", (width, height))
    gauss_img   = Image.new("RGB", (width, height))
    edge_img    = Image.new("L", (width, height))       # Monochromatic
    sharp_img   = Image.new("RGB", (width, height))

    p_mean   = mean_img.load()
    p_median = median_img.load()
    p_gauss  = gauss_img.load()
    p_edge   = edge_img.load()
    p_sharp  = sharp_img.load()

    # Single pass over interior pixels
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            window_r, window_g, window_b = [], [], []

            # Extract the 3x3 window ONCE
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    r, g, b = pixels[x + dx, y + dy]
                    window_r.append(r)
                    window_g.append(g)
                    window_b.append(b)

            # 1. Mean
            p_mean[x, y] = (mean_op(window_r), mean_op(window_g), mean_op(window_b))

            # 2. Median
            p_median[x, y] = (median_op(window_r), median_op(window_g), median_op(window_b))

            # 3. Gaussian
            p_gauss[x, y] = (gaussian_op(window_r), gaussian_op(window_g), gaussian_op(window_b))

            # 4. Monochromatic Edge Detection (convert window to grayscale)
            window_gray = [(r + g + b) // 3 for r, g, b in zip(window_r, window_g, window_b)]
            p_edge[x, y] = edge_op(window_gray)

            # 5. Sharpening
            p_sharp[x, y] = (sharpen_op(window_r), sharpen_op(window_g), sharpen_op(window_b))

    # Copy borders for color images
    for p_out in (p_mean, p_median, p_gauss, p_sharp):
        for x in range(width):
            p_out[x, 0] = pixels[x, 0]
            p_out[x, height - 1] = pixels[x, height - 1]
        for y in range(height):
            p_out[0, y] = pixels[0, y]
            p_out[width - 1, y] = pixels[width - 1, y]

    # Borders for monochromatic edge image (set to 0 / black)
    for x in range(width):
        p_edge[x, 0] = 0
        p_edge[x, height - 1] = 0
    for y in range(height):
        p_edge[0, y] = 0
        p_edge[width - 1, y] = 0

    return mean_img, median_img, gauss_img, edge_img, sharp_img


# ==========================================
# 3. Main Execution
# ==========================================

def main():
    original_img = Image.open("img_1.jpg").convert("RGB")

    print("Processing all 5 filters in a single pass...")
    mean_img, median_img, gauss_img, edge_img, sharp_img = process_all_filters(original_img)

    # Save results
    output_dir = "out_put_images"
    os.makedirs(output_dir, exist_ok=True)

    mean_img.save(os.path.join(output_dir, "filtered_mean.jpg"))
    median_img.save(os.path.join(output_dir, "filtered_median.jpg"))
    gauss_img.save(os.path.join(output_dir, "filtered_gaussian.jpg"))
    edge_img.save(os.path.join(output_dir, "edge_detection.jpg"))
    sharp_img.save(os.path.join(output_dir, "sharpened.jpg"))

    print("All 5 filtered images saved successfully to out_put_images.")


if __name__ == "__main__":
    main()

# Implementation of Basic Morphological Operations: Dilation, Erosion, Opening, Closing
import os
import cv2
import numpy as np

def apply_morphological_operations(image_path, threshold_val=128):
    # 1. Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # 2. Binarize image
    _, binary = cv2.threshold(img, threshold_val, 255, cv2.THRESH_BINARY)

    # 3. Define 3x3 structuring element (Kernel)
    kernel = np.ones((3, 3), np.uint8)

    # 4. Basic Operations
    # Erosion: shrinks white regions, removes tiny white noise
    eroded = cv2.erode(binary, kernel, iterations=1)

    # Dilation: expands white regions, fills small black holes
    dilated = cv2.dilate(binary, kernel, iterations=1)

    # Opening: Erosion followed by Dilation (removes small foreground noise)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Closing: Dilation followed by Erosion (fills small background holes)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary, eroded, dilated, opened, closed


def main():
    image_name = "img_1.jpg"
    binary, eroded, dilated, opened, closed = apply_morphological_operations(image_name)

    # Save output images
    output_dir = "out_put_images"
    os.makedirs(output_dir, exist_ok=True)

    cv2.imwrite(os.path.join(output_dir, "morph_original_binary.jpg"), binary)
    cv2.imwrite(os.path.join(output_dir, "morph_erosion.jpg"), eroded)
    cv2.imwrite(os.path.join(output_dir, "morph_dilation.jpg"), dilated)
    cv2.imwrite(os.path.join(output_dir, "morph_opening.jpg"), opened)
    cv2.imwrite(os.path.join(output_dir, "morph_closing.jpg"), closed)

    print("All 4 morphological operations (Erosion, Dilation, Opening, Closing) saved successfully.")


if __name__ == "__main__":
    main()

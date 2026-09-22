# Implementation of Morphological Boundary Extraction using Erosion
import os
import cv2
import numpy as np

def extract_boundary(image_path, threshold_val=128):
    # 1. Load image in grayscale
    img = cv2.imread(image_path, 0)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # 2. Convert to binary image (A)
    _, binary = cv2.threshold(img, threshold_val, 255, cv2.THRESH_BINARY)

    # 3. Define 3x3 structuring element (B)
    kernel = np.ones((3, 3), np.uint8)

    # 4. Perform Erosion: A ⊖ B
    eroded = cv2.erode(binary, kernel, iterations=1)

    # 5. Extract Boundary: β(A) = A - (A ⊖ B)
    boundary = cv2.subtract(binary, eroded)

    return binary, eroded, boundary


def main():
    image_name = "img_1.jpg"
    binary, eroded, boundary = extract_boundary(image_name)

    # Save outputs
    output_dir = "out_put_images"
    os.makedirs(output_dir, exist_ok=True)

    cv2.imwrite(os.path.join(output_dir, "morph_binary.jpg"), binary)
    cv2.imwrite(os.path.join(output_dir, "morph_eroded.jpg"), eroded)
    cv2.imwrite(os.path.join(output_dir, "morph_boundary.jpg"), boundary)

    print("Morphological boundary extraction completed successfully.")


if __name__ == "__main__":
    main()
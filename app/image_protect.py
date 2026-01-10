import cv2
import numpy as np

def protect_image(image_path: str, level: str):
    image = cv2.imread(image_path)
    image = image.astype(np.float32)

    # Noise strength by protection level
    if level == "HIGH":
        noise_strength = 8
    elif level == "MEDIUM":
        noise_strength = 5
    else:
        noise_strength = 2

    noise = np.random.randn(*image.shape) * noise_strength
    protected_image = image + noise

    protected_image = np.clip(protected_image, 0, 255).astype(np.uint8)
    return protected_image

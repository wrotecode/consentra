import cv2

def add_watermark(image, watermark_text: str, output_path: str):
    # Encode watermark in least significant bits (simple MVP)
    h, w, _ = image.shape
    for i in range(min(len(watermark_text), w)):
        image[0, i, 0] = ord(watermark_text[i]) % 256

    cv2.imwrite(output_path, image)
    return output_path

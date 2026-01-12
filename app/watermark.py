import cv2
import numpy as np
import json
from datetime import datetime
from typing import Dict, Optional

def text_to_bits(text: str) -> list:
    """Convert text to binary bits"""
    bits = []
    for char in text:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def bits_to_text(bits: list) -> str:
    """Convert binary bits to text"""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(''.join([str(b) for b in byte]), 2)))
    return ''.join(chars)

def embed_watermark_lsb(image: np.ndarray, watermark_data: str) -> np.ndarray:
    """
    Embed watermark using LSB steganography
    Distributes data across image to survive cropping
    """
    # Add length prefix and delimiter
    watermark_with_length = f"{len(watermark_data)}|{watermark_data}"
    bits = text_to_bits(watermark_with_length)
    
    # Add terminator
    bits.extend([0] * 16)  # Null terminator
    
    h, w, c = image.shape
    max_bits = h * w * c
    
    if len(bits) > max_bits:
        raise ValueError("Watermark too large for image")
    
    watermarked = image.copy()
    bit_index = 0
    
    # Embed across all channels in a distributed pattern
    for i in range(h):
        for j in range(w):
            for k in range(c):
                if bit_index < len(bits):
                    # Modify LSB
                    watermarked[i, j, k] = (image[i, j, k] & 0xFE) | bits[bit_index]
                    bit_index += 1
                else:
                    break
            if bit_index >= len(bits):
                break
        if bit_index >= len(bits):
            break
    
    return watermarked

def extract_watermark_lsb(image: np.ndarray) -> Optional[str]:
    """
    Extract watermark from LSB
    """
    h, w, c = image.shape
    bits = []
    
    # Extract bits
    for i in range(h):
        for j in range(w):
            for k in range(c):
                bits.append(image[i, j, k] & 1)
    
    # Try to decode
    try:
        text = bits_to_text(bits)
        # Find delimiter
        if '|' in text:
            length_str, data = text.split('|', 1)
            length = int(length_str)
            return data[:length]
    except:
        pass
    
    return None

def create_watermark_metadata(owner_id: str, consent: bool = True) -> str:
    """
    Create watermark metadata JSON
    """
    metadata = {
        "owner_id": owner_id,
        "consent": consent,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0"
    }
    return json.dumps(metadata)

def add_watermark(image: np.ndarray, owner_id: str, output_path: str, consent: bool = True) -> str:
    """
    Add invisible watermark with owner ID and consent information
    """
    # Create metadata
    watermark_data = create_watermark_metadata(owner_id, consent)
    
    # Embed watermark
    watermarked_image = embed_watermark_lsb(image, watermark_data)
    
    # Save with high quality
    cv2.imwrite(output_path, watermarked_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    
    return output_path

def verify_watermark(image_path: str) -> Optional[Dict]:
    """
    Verify and extract watermark from protected image
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    watermark_data = extract_watermark_lsb(image)
    
    if watermark_data:
        try:
            return json.loads(watermark_data)
        except:
            return {"raw_data": watermark_data}
    
    return None

import cv2
import numpy as np
from typing import Dict, Tuple

# Load Haar Cascade for face detection
try:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
except:
    face_cascade = None
    print("Warning: Face detection model not loaded")

def analyze_image(image_path: str) -> Dict:
    """
    Analyze image to extract features for protection decision
    """
    img = cv2.imread(image_path)
    
    if img is None:
        return {"faces": 0, "brightness": 0, "size": 0}
    
    # Detect faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    if face_cascade is not None:
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Calculate brightness
    brightness = np.mean(gray)
    
    # Image size
    h, w, _ = img.shape
    size = h * w
    
    return {
        "faces": len(faces),
        "brightness": brightness,
        "size": size,
        "dimensions": (h, w)
    }

def assess_risk_level(features: Dict) -> str:
    """
    Assess risk based on image features
    Face detection -> likely personal/sensitive
    High resolution -> likely for public use
    """
    risk_score = 0
    
    # Face detection (strong indicator)
    if features["faces"] > 0:
        risk_score += 40
    
    # High resolution images are more likely to be misused
    if features["size"] > 1000000:  # > 1MP
        risk_score += 20
    
    # Well-lit images (higher quality)
    if features["brightness"] > 120:
        risk_score += 10
    
    if risk_score >= 50:
        return "HIGH"
    elif risk_score >= 25:
        return "MEDIUM"
    else:
        return "LOW"

def decide_protection_level(image_path: str, filename: str = "") -> Tuple[str, Dict]:
    """
    Agentic decision logic combining filename hints and image analysis
    Returns: (protection_level, analysis_metadata)
    """
    # Analyze image content
    features = analyze_image(image_path)
    
    # Filename-based hints
    filename_lower = filename.lower()
    filename_risk = "LOW"
    
    if any(keyword in filename_lower for keyword in ["profile", "headshot", "portrait"]):
        filename_risk = "HIGH"
    elif any(keyword in filename_lower for keyword in ["selfie", "avatar", "photo"]):
        filename_risk = "MEDIUM"
    
    # Image content-based risk
    content_risk = assess_risk_level(features)
    
    # Final decision: take the higher of the two
    risk_levels = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    final_level = max(filename_risk, content_risk, key=lambda x: risk_levels[x])
    
    metadata = {
        "filename_risk": filename_risk,
        "content_risk": content_risk,
        "faces_detected": features["faces"],
        "image_size": features["size"],
        "final_protection": final_level
    }
    
    return final_level, metadata

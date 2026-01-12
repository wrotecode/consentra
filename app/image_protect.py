import cv2
import numpy as np
from typing import Tuple

def apply_adversarial_noise(image: np.ndarray, strength: float) -> np.ndarray:
    """
    Apply adversarial noise that's imperceptible to humans but confuses AI models
    Uses combination of spatial and frequency domain perturbations
    """
    # Spatial domain noise
    spatial_noise = np.random.randn(*image.shape) * strength
    
    # Frequency domain perturbations (targets AI feature extraction)
    # Convert to frequency domain per channel
    freq_noise = np.zeros_like(image, dtype=np.float32)
    for c in range(image.shape[2]):
        fft = np.fft.fft2(image[:, :, c])
        # Add noise to high-frequency components (less visible, more disruptive)
        fft_shifted = np.fft.fftshift(fft)
        rows, cols = fft_shifted.shape
        center_row, center_col = rows // 2, cols // 2
        
        # Create high-pass filter
        y, x = np.ogrid[:rows, :cols]
        mask = np.sqrt((x - center_col)**2 + (y - center_row)**2) > min(rows, cols) // 4
        
        # Add noise to high frequencies
        noise_fft = np.random.randn(rows, cols) + 1j * np.random.randn(rows, cols)
        fft_shifted = fft_shifted + mask * noise_fft * strength * 10
        
        # Transform back
        fft = np.fft.ifftshift(fft_shifted)
        freq_noise[:, :, c] = np.real(np.fft.ifft2(fft))
    
    return spatial_noise + freq_noise * 0.3

def apply_gradient_based_protection(image: np.ndarray, iterations: int = 3) -> np.ndarray:
    """
    Apply gradient-based perturbations targeting deep learning models
    Simulates adversarial attack patterns
    """
    protected = image.copy()
    
    for _ in range(iterations):
        # Simulate gradient direction (random direction for now)
        gradient = np.random.randn(*image.shape)
        gradient = gradient / (np.linalg.norm(gradient) + 1e-8)
        
        # Apply small perturbation in gradient direction
        protected = protected + gradient * 2.0
    
    return protected

def enhance_robustness(image: np.ndarray) -> np.ndarray:
    """
    Apply additional processing to make protection robust to common transformations
    (compression, scaling, etc.)
    """
    # Add slight texture that survives compression
    h, w = image.shape[:2]
    texture = np.sin(np.linspace(0, 50, h))[:, np.newaxis] * np.sin(np.linspace(0, 50, w))[np.newaxis, :]
    texture = np.stack([texture] * 3, axis=2)
    
    image = image + texture * 0.5
    return image

def protect_image(image_path: str, level: str) -> Tuple[np.ndarray, dict]:
    """
    Apply comprehensive image protection based on level
    Returns: (protected_image, processing_metadata)
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from {image_path}")
    
    image = image.astype(np.float32)
    
    # Protection parameters by level
    protection_params = {
        "HIGH": {"noise_strength": 10, "gradient_iterations": 5, "enhance": True},
        "MEDIUM": {"noise_strength": 6, "gradient_iterations": 3, "enhance": True},
        "LOW": {"noise_strength": 3, "gradient_iterations": 1, "enhance": False}
    }
    
    params = protection_params.get(level, protection_params["LOW"])
    
    # Apply adversarial noise
    noise = apply_adversarial_noise(image, params["noise_strength"])
    protected_image = image + noise
    
    # Apply gradient-based protection
    protected_image = apply_gradient_based_protection(
        protected_image, 
        params["gradient_iterations"]
    )
    
    # Enhance robustness for higher levels
    if params["enhance"]:
        protected_image = enhance_robustness(protected_image)
    
    # Ensure valid pixel range
    protected_image = np.clip(protected_image, 0, 255).astype(np.uint8)
    
    metadata = {
        "protection_level": level,
        "noise_strength": params["noise_strength"],
        "gradient_iterations": params["gradient_iterations"],
        "robustness_enhanced": params["enhance"]
    }
    
    return protected_image, metadata

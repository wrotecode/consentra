#!/usr/bin/env python3
"""
Quick test script for Consentra API
Tests all endpoints and demonstrates functionality
"""

import requests
import io
from PIL import Image
import numpy as np

BASE_URL = "http://localhost:8000"

def create_test_image(size=(800, 600), color=(100, 150, 200)):
    """Create a simple test image"""
    img_array = np.ones((size[1], size[0], 3), dtype=np.uint8)
    img_array[:, :] = color
    
    # Add some patterns
    img_array[100:200, 100:300] = [255, 0, 0]  # Red square
    img_array[300:400, 400:600] = [0, 255, 0]  # Green square
    
    return Image.fromarray(img_array)

def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_protect_image():
    """Test image protection endpoint"""
    print("\n=== Testing Image Protection ===")
    
    # Create test image
    test_img = create_test_image()
    img_bytes = io.BytesIO()
    test_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Send to API
    files = {'file': ('test_selfie.png', img_bytes, 'image/png')}
    data = {'user_id': 'test_user_123'}
    
    response = requests.post(
        f"{BASE_URL}/protect-image",
        files=files,
        data=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Protection Level: {response.headers.get('X-Protection-Level')}")
    print(f"Processing Time: {response.headers.get('X-Processing-Time')}ms")
    print(f"Image ID: {response.headers.get('X-Image-ID')}")
    
    if response.status_code == 200:
        # Save protected image
        with open("temp/test_protected.png", "wb") as f:
            f.write(response.content)
        print("✓ Protected image saved to temp/test_protected.png")
        return True
    else:
        print(f"✗ Error: {response.text}")
        return False

def test_verify_watermark():
    """Test watermark verification"""
    print("\n=== Testing Watermark Verification ===")
    
    try:
        # Load the protected image we just created
        with open("temp/test_protected.png", "rb") as f:
            files = {'file': ('test_protected.png', f, 'image/png')}
            response = requests.post(
                f"{BASE_URL}/verify-watermark",
                files=files
            )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Watermarked: {result.get('watermarked')}")
        if result.get('metadata'):
            print(f"Metadata: {result['metadata']}")
        
        return response.status_code == 200
    except FileNotFoundError:
        print("✗ Protected image not found. Run test_protect_image() first.")
        return False

def test_analytics():
    """Test analytics endpoint"""
    print("\n=== Testing Analytics ===")
    response = requests.get(f"{BASE_URL}/analytics")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Processed: {data.get('total_processed')}")
        print(f"Avg Processing Time: {data.get('avg_processing_time_ms')}ms")
        print(f"Protection Levels: {data.get('protection_levels')}")
        return True
    return False

def test_rate_limiting():
    """Test rate limiting (should fail after 10 requests)"""
    print("\n=== Testing Rate Limiting ===")
    print("Sending 12 rapid requests (limit is 10/minute)...")
    
    test_img = create_test_image()
    img_bytes = io.BytesIO()
    test_img.save(img_bytes, format='PNG')
    
    success_count = 0
    rate_limited = False
    
    for i in range(12):
        img_bytes.seek(0)
        files = {'file': ('test.png', img_bytes, 'image/png')}
        response = requests.post(f"{BASE_URL}/protect-image", files=files)
        
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            rate_limited = True
            print(f"✓ Rate limited after {success_count} requests")
            break
    
    return rate_limited

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("CONSENTRA API TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    results['Health Check'] = test_health_check()
    results['Image Protection'] = test_protect_image()
    results['Watermark Verification'] = test_verify_watermark()
    results['Analytics'] = test_analytics()
    results['Rate Limiting'] = test_rate_limiting()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    print("Make sure the server is running: uvicorn app.main:app --reload\n")
    
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server.")
        print("Make sure the server is running at http://localhost:8000")
        print("\nStart server with: uvicorn app.main:app --reload")

"""
Example Python client for Consentra API
Shows how to integrate with the backend
"""

import requests
from pathlib import Path

class ConsentraClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def protect_image(self, image_path, user_id=None):
        """
        Protect an image and get the protected version
        
        Args:
            image_path: Path to the image file
            user_id: Optional user identifier for watermarking
        
        Returns:
            dict with 'success', 'data' (image bytes), 'metadata'
        """
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {}
            if user_id:
                data['user_id'] = user_id
            
            response = requests.post(
                f"{self.base_url}/protect-image",
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.content,
                'metadata': {
                    'protection_level': response.headers.get('X-Protection-Level'),
                    'processing_time_ms': response.headers.get('X-Processing-Time'),
                    'image_id': response.headers.get('X-Image-ID')
                }
            }
        else:
            return {
                'success': False,
                'error': response.text
            }
    
    def verify_watermark(self, image_path):
        """
        Verify if an image has a Consentra watermark
        
        Args:
            image_path: Path to the image file
        
        Returns:
            dict with watermark information
        """
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/verify-watermark",
                files=files
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'success': False, 'error': response.text}
    
    def get_analytics(self):
        """Get processing analytics"""
        response = requests.get(f"{self.base_url}/analytics")
        if response.status_code == 200:
            return response.json()
        return None
    
    def health_check(self):
        """Check if the API is online"""
        try:
            response = requests.get(f"{self.base_url}/")
            return response.status_code == 200
        except:
            return False


# Example usage
if __name__ == "__main__":
    client = ConsentraClient()
    
    # Check if server is running
    if not client.health_check():
        print("Error: Server is not running!")
        print("Start it with: python run_server.py")
        exit(1)
    
    print("✓ Server is online")
    
    # Example: Protect an image
    # result = client.protect_image("my_photo.jpg", user_id="user123")
    # if result['success']:
    #     with open("protected_photo.png", "wb") as f:
    #         f.write(result['data'])
    #     print(f"Protected! Level: {result['metadata']['protection_level']}")
    
    # Example: Verify watermark
    # watermark = client.verify_watermark("protected_photo.png")
    # print(f"Watermarked: {watermark.get('watermarked')}")
    
    # Example: Get analytics
    analytics = client.get_analytics()
    if analytics:
        print(f"\nAnalytics:")
        print(f"Total processed: {analytics.get('total_processed')}")
        print(f"Avg time: {analytics.get('avg_processing_time_ms')}ms")

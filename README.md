# Consentra - AI Image Protection System

🛡️ Protect your images from AI manipulation and unauthorized deepfake generation.

## Overview

Consentra is an AI-powered backend system that adds imperceptible adversarial noise and invisible watermarks to images, making them resistant to AI-based manipulation while maintaining visual quality for human viewers.

## Features

### 🤖 Agentic AI Decision System
- **Face Detection**: Automatically detects faces to assess risk level
- **Image Analysis**: Analyzes brightness, resolution, and content
- **Smart Protection**: Combines filename hints with content analysis
- **Risk Assessment**: Determines optimal protection level (LOW/MEDIUM/HIGH)

### 🔒 Advanced Protection Techniques
- **Adversarial Noise**: Spatial and frequency-domain perturbations
- **Gradient-Based Protection**: Targets deep learning feature extraction
- **Robustness Enhancement**: Survives compression and transformations
- **Multi-Level Protection**: Customizable strength based on risk

### 🏷️ Invisible Watermarking
- **LSB Steganography**: Embeds watermark in least significant bits
- **Metadata Embedding**: Owner ID, timestamp, and consent information
- **Distributed Pattern**: Survives cropping and editing
- **Extraction API**: Verify watermark authenticity

### 🔐 Security & Privacy
- **In-Memory Processing**: No permanent storage of user images
- **Rate Limiting**: 10 requests/minute per IP
- **CORS Protection**: Configurable origins
- **File Validation**: Type and size checks
- **Automatic Cleanup**: Temporary files removed after processing

### 📊 Analytics
- **Processing Metrics**: Time, protection level, file size
- **Anonymized Logging**: Privacy-preserving analytics
- **Real-time Monitoring**: Track system performance

## API Endpoints

### 1. Protect Image
```http
POST /protect-image
Content-Type: multipart/form-data

Parameters:
- file: Image file (PNG, JPG, JPEG)
- user_id: Optional user identifier (string)

Response: Protected image file
Headers:
- X-Protection-Level: LOW|MEDIUM|HIGH
- X-Processing-Time: milliseconds
- X-Image-ID: unique identifier
```

### 2. Verify Watermark
```http
POST /verify-watermark
Content-Type: multipart/form-data

Parameters:
- file: Image file to verify

Response:
{
  "watermarked": true,
  "metadata": {
    "owner_id": "...",
    "timestamp": "...",
    "consent": true,
    "version": "1.0"
  }
}
```

### 3. Analytics
```http
GET /analytics

Response:
{
  "total_processed": 42,
  "avg_processing_time_ms": 1234.56,
  "protection_levels": {
    "HIGH": 15,
    "MEDIUM": 20,
    "LOW": 7
  },
  "recent": [...]
}
```

### 4. Health Check
```http
GET /

Response:
{
  "status": "online",
  "service": "Consentra Image Protection API",
  "version": "1.0.0"
}
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
git clone <your-repo>
cd consentra
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive docs at: `http://localhost:8000/docs`

## Usage Examples

### Python
```python
import requests

# Protect an image
with open('photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/protect-image',
        files={'file': f},
        data={'user_id': 'user123'}
    )
    
    with open('protected_photo.png', 'wb') as out:
        out.write(response.content)
    
    print(f"Protection Level: {response.headers['X-Protection-Level']}")
```

### JavaScript (Frontend)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('user_id', 'user123');

const response = await fetch('http://localhost:8000/protect-image', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
const protectedUrl = URL.createObjectURL(blob);

// Use protectedUrl to display or download
```

### cURL
```bash
curl -X POST "http://localhost:8000/protect-image" \
  -F "file=@photo.jpg" \
  -F "user_id=user123" \
  -o protected_photo.png
```

## How It Works

### 1. Image Upload
User uploads an image through the frontend

### 2. Agentic Analysis
- Detects faces using Haar Cascade
- Analyzes image properties (size, brightness)
- Combines filename hints with content analysis
- Determines risk level and protection strength

### 3. Adversarial Protection
- Applies spatial domain noise
- Adds frequency domain perturbations
- Uses gradient-based protection techniques
- Ensures robustness to transformations

### 4. Watermark Embedding
- Creates metadata (owner ID, timestamp, consent)
- Embeds using LSB steganography
- Distributes across entire image
- Invisible to human eye

### 5. Return Protected Image
- High-quality PNG output
- Metadata in response headers
- Automatic cleanup of temp files

## Protection Levels

### HIGH
- **Trigger**: Profile pictures, faces detected, high-resolution
- **Noise Strength**: 10
- **Gradient Iterations**: 5
- **Robustness**: Enhanced
- **Use Case**: Personal photos, professional headshots

### MEDIUM
- **Trigger**: Selfies, avatars, moderate risk
- **Noise Strength**: 6
- **Gradient Iterations**: 3
- **Robustness**: Enhanced
- **Use Case**: Social media posts, casual photos

### LOW
- **Trigger**: General images, landscapes, low risk
- **Noise Strength**: 3
- **Gradient Iterations**: 1
- **Robustness**: Basic
- **Use Case**: Public images, illustrations

## Tech Stack

- **FastAPI**: Modern, fast web framework
- **OpenCV**: Image processing and face detection
- **NumPy**: Numerical operations
- **Pillow**: Image manipulation
- **PyTorch**: Deep learning framework (extensible)
- **SlowAPI**: Rate limiting
- **Uvicorn**: ASGI server

## Development

### Run in development mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run tests
```bash
pytest test/
```

### View API documentation
Open browser: `http://localhost:8000/docs`

## Deployment

### Production Considerations
1. **Use HTTPS**: Enable SSL/TLS for all requests
2. **Set CORS**: Configure specific frontend origins in `.env`
3. **Database**: Replace in-memory analytics with proper database
4. **Storage**: Use cloud storage for processed images if needed
5. **Authentication**: Add API keys or OAuth for production
6. **Monitoring**: Set up logging and monitoring services
7. **Scaling**: Use Gunicorn with multiple workers

### Docker Deployment (Future)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Hackathon Demo Tips

1. **Show Real-time Processing**: Use analytics endpoint to show live stats
2. **Face Detection Demo**: Upload photos with/without faces
3. **Watermark Verification**: Protect → Download → Verify workflow
4. **Different Protection Levels**: Name files with keywords (selfie, profile)
5. **Before/After**: Show original vs protected (visually identical)
6. **AI Attack Resistance**: Demonstrate protection against style transfer

## Future Enhancements

- [ ] Multi-model ensemble protection
- [ ] Custom protection profiles
- [ ] Batch processing
- [ ] Video protection
- [ ] Blockchain verification
- [ ] Mobile SDK
- [ ] Real-time streaming protection
- [ ] Advanced analytics dashboard

## License

MIT License - See LICENSE file

## Contributors

Built for [Hackathon Name] by [Your Team]

## Support

For issues and questions, open an issue on GitHub or contact [your-email]

---

**Protect your digital identity. Stop AI misuse before it starts.** 🛡️

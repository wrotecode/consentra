# Consentra API Reference

## Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com/api
```

## Authentication
Currently no authentication required. In production, implement API keys or OAuth.

---

## Endpoints

### 1. Health Check
Check if the API is online and get service information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "status": "online",
  "service": "Consentra Image Protection API",
  "version": "1.0.0",
  "timestamp": "2026-01-12T10:30:00.000Z"
}
```

**Status Codes:**
- `200 OK` - Service is running

---

### 2. Protect Image
Apply AI protection and watermarking to an image.

**Endpoint:** `POST /protect-image`

**Rate Limit:** 10 requests per minute per IP

**Request:**
```http
POST /protect-image
Content-Type: multipart/form-data

Body:
- file: (required) Image file (PNG, JPG, JPEG)
- user_id: (optional) User identifier for watermarking
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/protect-image" \
  -F "file=@photo.jpg" \
  -F "user_id=user123" \
  -o protected.png
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('user_id', 'user123');

const response = await fetch('http://localhost:8000/protect-image', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
```

**Response:**
- **Success (200):** Protected image file (PNG)
- **Headers:**
  - `X-Protection-Level`: Protection level applied (HIGH/MEDIUM/LOW)
  - `X-Processing-Time`: Processing time in milliseconds
  - `X-Image-ID`: Unique identifier for this request

**Error Responses:**
```json
// 400 Bad Request
{
  "detail": "File must be an image"
}

// 400 Bad Request
{
  "detail": "File too large. Max size: 10MB"
}

// 429 Too Many Requests
{
  "detail": "Rate limit exceeded"
}

// 500 Internal Server Error
{
  "detail": "Image processing failed: {error_message}"
}
```

**Protection Levels:**

| Level | Triggered By | Noise Strength | Iterations | Use Case |
|-------|-------------|----------------|------------|----------|
| HIGH | Faces detected, profile images, high-res | 10 | 5 | Personal photos, headshots |
| MEDIUM | Selfies, avatars, moderate risk | 6 | 3 | Social media posts |
| LOW | General images, landscapes | 3 | 1 | Public images, designs |

**Status Codes:**
- `200 OK` - Image protected successfully
- `400 Bad Request` - Invalid file or parameters
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Processing failed

---

### 3. Verify Watermark
Verify if an image contains a Consentra watermark and extract metadata.

**Endpoint:** `POST /verify-watermark`

**Rate Limit:** 20 requests per minute per IP

**Request:**
```http
POST /verify-watermark
Content-Type: multipart/form-data

Body:
- file: (required) Image file to verify
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/verify-watermark" \
  -F "file=@protected.png"
```

**Response:**
```json
{
  "watermarked": true,
  "metadata": {
    "owner_id": "abc123...",
    "consent": true,
    "timestamp": "2026-01-12T10:30:00.000Z",
    "version": "1.0"
  }
}
```

**No Watermark Response:**
```json
{
  "watermarked": false,
  "metadata": null
}
```

**Status Codes:**
- `200 OK` - Verification complete
- `500 Internal Server Error` - Verification failed

---

### 4. Analytics
Get anonymized processing statistics.

**Endpoint:** `GET /analytics`

**Note:** In production, this should be admin-only.

**Request:**
```http
GET /analytics
```

**cURL Example:**
```bash
curl http://localhost:8000/analytics
```

**Response:**
```json
{
  "total_processed": 42,
  "recent": [
    {
      "timestamp": "2026-01-12T10:30:00.000Z",
      "processing_time_ms": 1234.56,
      "protection_level": "HIGH",
      "file_size_kb": 512.5,
      "image_id": "abc123...",
      "filename_risk": "HIGH",
      "content_risk": "HIGH",
      "faces_detected": 1,
      "image_size": 1048576,
      "final_protection": "HIGH",
      "noise_strength": 10,
      "gradient_iterations": 5,
      "robustness_enhanced": true
    }
  ],
  "avg_processing_time_ms": 1567.89,
  "protection_levels": {
    "HIGH": 15,
    "MEDIUM": 20,
    "LOW": 7
  }
}
```

**Status Codes:**
- `200 OK` - Analytics retrieved

---

## Data Models

### Watermark Metadata
```typescript
interface WatermarkMetadata {
  owner_id: string;        // User or image identifier
  consent: boolean;        // Consent flag
  timestamp: string;       // ISO 8601 timestamp
  version: string;         // Watermark version
}
```

### Protection Metadata
```typescript
interface ProtectionMetadata {
  protection_level: "HIGH" | "MEDIUM" | "LOW";
  noise_strength: number;
  gradient_iterations: number;
  robustness_enhanced: boolean;
}
```

### Agent Metadata
```typescript
interface AgentMetadata {
  filename_risk: "HIGH" | "MEDIUM" | "LOW";
  content_risk: "HIGH" | "MEDIUM" | "LOW";
  faces_detected: number;
  image_size: number;      // Total pixels
  final_protection: "HIGH" | "MEDIUM" | "LOW";
}
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message"
}
```

### Common Errors

**Invalid File Type**
```
Status: 400
Detail: "File must be an image"
```

**File Too Large**
```
Status: 400
Detail: "File too large. Max size: 10MB"
```

**Rate Limited**
```
Status: 429
Detail: "Rate limit exceeded"
Headers:
  Retry-After: 60
```

**Processing Failed**
```
Status: 500
Detail: "Image processing failed: {specific_error}"
```

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/protect-image` | 10 requests/minute per IP |
| `/verify-watermark` | 20 requests/minute per IP |
| Other endpoints | No limit |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1704974400
```

---

## File Constraints

- **Supported formats:** PNG, JPG, JPEG
- **Maximum size:** 10 MB
- **Output format:** PNG (lossless)
- **Recommended size:** < 2 MB for best performance

---

## Security Considerations

### Privacy
- Images processed entirely in-memory
- No permanent storage of user images
- Temporary files deleted after processing
- Analytics data is anonymized

### CORS
Configure allowed origins in production:
```python
allow_origins=["https://your-frontend.com"]
```

### HTTPS
Always use HTTPS in production to protect image data in transit.

### API Authentication
Recommended for production:
- API keys
- OAuth 2.0
- JWT tokens

---

## Response Times

Typical processing times:

| Image Size | Protection Level | Time |
|------------|-----------------|------|
| < 500KB | LOW | 500-1000ms |
| < 500KB | MEDIUM | 800-1500ms |
| < 500KB | HIGH | 1000-2000ms |
| 1-2MB | LOW | 1000-2000ms |
| 1-2MB | MEDIUM | 1500-2500ms |
| 1-2MB | HIGH | 2000-3500ms |
| > 5MB | ANY | 3000-6000ms |

*Times may vary based on hardware and face detection overhead.*

---

## Client Libraries

### Python
```python
from client_example import ConsentraClient

client = ConsentraClient("http://localhost:8000")
result = client.protect_image("photo.jpg", user_id="user123")

with open("protected.png", "wb") as f:
    f.write(result['data'])
```

### JavaScript
```javascript
class ConsentraClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async protectImage(file, userId = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (userId) formData.append('user_id', userId);

    const response = await fetch(`${this.baseUrl}/protect-image`, {
      method: 'POST',
      body: formData
    });

    return {
      blob: await response.blob(),
      metadata: {
        protectionLevel: response.headers.get('X-Protection-Level'),
        processingTime: response.headers.get('X-Processing-Time'),
        imageId: response.headers.get('X-Image-ID')
      }
    };
  }
}
```

---

## Testing

### Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

### Automated Tests
```bash
python test_api.py
```

### Manual Testing
```bash
# Protect
curl -X POST http://localhost:8000/protect-image \
  -F "file=@test.jpg" -o protected.png

# Verify
curl -X POST http://localhost:8000/verify-watermark \
  -F "file=@protected.png"

# Analytics
curl http://localhost:8000/analytics
```

---

## Changelog

### Version 1.0.0 (2026-01-12)
- Initial release
- Agentic AI protection level decision
- Multi-layer adversarial protection
- LSB steganography watermarking
- Rate limiting and CORS
- Analytics endpoint

---

## Support

- **Documentation:** See README.md
- **Frontend Guide:** See FRONTEND_GUIDE.md
- **Quick Start:** See QUICKSTART.md
- **Interactive API Docs:** http://localhost:8000/docs

---

## License

MIT License - See LICENSE file

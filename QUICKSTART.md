# 🚀 Quick Start Guide

## For the Hackathon Demo

### 1. Start the Server

**Option A: Using the run script (Recommended)**
```bash
python run_server.py
```

**Option B: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: **http://localhost:8000**

### 2. Test the API

Open your browser and go to: **http://localhost:8000/docs**

This shows the interactive API documentation where you can test endpoints directly!

Or run the automated test:
```bash
python test_api.py
```

### 3. Connect Your Frontend

Share this URL with your frontend developer: **http://localhost:8000**

They should read: `FRONTEND_GUIDE.md` for integration examples.

## Quick Tests

### Test 1: Health Check
```bash
curl http://localhost:8000/
```

### Test 2: Protect an Image
```bash
curl -X POST "http://localhost:8000/protect-image" \
  -F "file=@your_photo.jpg" \
  -o protected.png
```

### Test 3: Check Analytics
```bash
curl http://localhost:8000/analytics
```

## What Each File Does

- **app/main.py** - Main API endpoints and server configuration
- **app/agent.py** - AI decision-making (analyzes images, decides protection level)
- **app/image_protect.py** - Applies adversarial noise and protection
- **app/watermark.py** - Embeds invisible watermarks
- **run_server.py** - Easy server startup script
- **test_api.py** - Automated testing script
- **client_example.py** - Python client example
- **FRONTEND_GUIDE.md** - Complete frontend integration guide

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/protect-image` | POST | Protect an image |
| `/verify-watermark` | POST | Verify watermark |
| `/analytics` | GET | Get processing stats |
| `/docs` | GET | Interactive API docs |

## Features Implemented ✅

### Agentic AI Module
- ✅ Face detection using Haar Cascade
- ✅ Image brightness analysis
- ✅ Resolution-based risk assessment
- ✅ Filename hint processing
- ✅ Multi-factor protection level decision

### Image Protection Engine
- ✅ Spatial domain adversarial noise
- ✅ Frequency domain perturbations
- ✅ Gradient-based protection
- ✅ Robustness enhancements
- ✅ Three protection levels (LOW/MEDIUM/HIGH)

### Watermarking
- ✅ LSB steganography
- ✅ Owner ID embedding
- ✅ Timestamp and consent info
- ✅ Extraction and verification
- ✅ Distributed pattern (survives cropping)

### Security & Privacy
- ✅ In-memory processing (no storage)
- ✅ CORS middleware
- ✅ Rate limiting (10/minute)
- ✅ File type validation
- ✅ File size limits (10MB)
- ✅ Automatic temp file cleanup

### Analytics
- ✅ Processing time tracking
- ✅ Protection level distribution
- ✅ Anonymized logging
- ✅ Real-time metrics

## Demo Tips 🎯

### Showcase Different Protection Levels

1. **HIGH Protection (Red Shield 🔒)**
   - Upload: `my_profile.jpg` or `headshot.jpg`
   - Or any photo with a face
   - Shows maximum protection

2. **MEDIUM Protection (Orange Shield 🛡️)**
   - Upload: `selfie.jpg` or `avatar.jpg`
   - Balanced protection

3. **LOW Protection (Green Check ✓)**
   - Upload: `landscape.jpg` or `design.jpg`
   - Efficient protection for low-risk images

### Show the Watermark

1. Protect an image
2. Download the protected version
3. Upload it to `/verify-watermark`
4. Show the extracted metadata (Owner ID, timestamp, consent)

### Demonstrate Speed

- Show processing time in response headers
- Typical times: 1-3 seconds depending on image size
- Show analytics dashboard with average times

### Before/After Comparison

- Show original and protected side by side
- They look **identical** to humans
- But protected image is **AI-resistant**

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Port already in use"
Change port in `run_server.py` or:
```bash
uvicorn app.main:app --reload --port 8001
```

### "CORS Error" from frontend
Update `allow_origins` in `app/main.py`:
```python
allow_origins=["http://localhost:3000"]  # Your frontend URL
```

### Face detection not working
OpenCV's Haar Cascade is included. If it doesn't work:
```python
# In app/agent.py, it will fall back gracefully
print("Warning: Face detection model not loaded")
```

## Performance Tips

- Images process faster when smaller (< 2MB recommended)
- Face detection adds ~200ms overhead
- HIGH protection takes longer than LOW
- First request may be slower (model initialization)

## Next Steps for Production

1. Add authentication (API keys or OAuth)
2. Use proper database for analytics
3. Deploy with Docker
4. Add HTTPS
5. Set up monitoring
6. Implement queue system for batch processing
7. Add cloud storage for processed images (optional)

## Support

- Check `/docs` for interactive API documentation
- Read `README.md` for complete documentation
- Check `FRONTEND_GUIDE.md` for frontend integration

---

**Ready to present!** Start the server and show how AI-resistant image protection works in real-time! 🎉

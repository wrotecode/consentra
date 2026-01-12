# 📚 Consentra Documentation Index

Welcome to Consentra! This guide will help you navigate all documentation.

## 🚀 Getting Started

1. **[QUICKSTART.md](QUICKSTART.md)** - Start here! 
   - How to run the server
   - Quick testing
   - Demo tips
   - Troubleshooting

2. **[README.md](README.md)** - Complete project overview
   - Features and capabilities
   - Installation instructions
   - Usage examples
   - Tech stack details

## 👨‍💻 For Developers

3. **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
   - All endpoints with examples
   - Request/response formats
   - Error handling
   - Rate limiting details

4. **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - Frontend integration guide
   - React, Vue, Vanilla JS examples
   - Complete code snippets
   - Error handling
   - UI/UX tips

## 🎤 For Hackathon Presentation

5. **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Step-by-step demo script
   - 7-minute presentation flow
   - What to say and do
   - Q&A preparation
   - Backup plans

## 📁 Project Structure

```
consentra/
├── app/
│   ├── main.py              # FastAPI app with all endpoints
│   ├── agent.py             # Agentic AI decision logic
│   ├── image_protect.py     # Adversarial protection engine
│   └── watermark.py         # Watermarking system
├── temp/                    # Temporary file storage
├── test/
│   └── diff_test.py         # Unit tests
├── .env.example             # Environment configuration template
├── requirements.txt         # Python dependencies
├── run_server.py           # Easy server startup script
├── test_api.py             # Automated API testing
└── client_example.py       # Python client example
```

## 🔑 Key Files to Know

### Backend Core
- **[app/main.py](app/main.py)** - API endpoints, CORS, rate limiting, error handling
- **[app/agent.py](app/agent.py)** - Face detection, risk assessment, protection level decision
- **[app/image_protect.py](app/image_protect.py)** - Adversarial noise, gradient protection
- **[app/watermark.py](app/watermark.py)** - LSB steganography, metadata embedding

### Helper Scripts
- **[run_server.py](run_server.py)** - Quick server startup
- **[test_api.py](test_api.py)** - Automated endpoint testing
- **[client_example.py](client_example.py)** - Python client usage examples

### Configuration
- **[requirements.txt](requirements.txt)** - All dependencies
- **[.env.example](.env.example)** - Configuration template

## 🎯 Quick Links by Task

### "I want to start the server"
→ [QUICKSTART.md](QUICKSTART.md#1-start-the-server)

### "I need to integrate with frontend"
→ [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md#frontend-implementation-examples)

### "I want to test the API"
→ Run `python test_api.py` or visit http://localhost:8000/docs

### "I need to prepare the demo"
→ [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

### "I need API documentation"
→ [API_REFERENCE.md](API_REFERENCE.md) or http://localhost:8000/docs

### "I want to understand the architecture"
→ [README.md](README.md#how-it-works)

### "I need code examples"
→ [client_example.py](client_example.py) or [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)

## 📊 Features Implemented

### ✅ Agentic AI Module
- Face detection (Haar Cascade)
- Image analysis (brightness, resolution)
- Multi-factor risk assessment
- Intelligent protection level decision

### ✅ Image Protection Engine
- Spatial domain adversarial noise
- Frequency domain perturbations
- Gradient-based protection
- Three protection levels (LOW/MEDIUM/HIGH)

### ✅ Watermarking System
- LSB steganography
- Owner ID + timestamp + consent
- Extraction and verification API
- Robust to transformations

### ✅ Security & Privacy
- In-memory processing (no storage)
- CORS middleware
- Rate limiting (10/min for protect, 20/min for verify)
- File validation and size limits
- Automatic cleanup

### ✅ Production Features
- Complete API documentation
- Error handling and validation
- Processing analytics
- Logging system
- Interactive API docs (Swagger)

## 🔧 Tech Stack

**Backend:**
- FastAPI - Modern async web framework
- OpenCV - Image processing & face detection
- NumPy - Numerical operations
- Pillow - Image manipulation
- SlowAPI - Rate limiting
- Uvicorn - ASGI server

**Optional (Installed):**
- PyTorch - For future ML enhancements
- SciPy - Scientific computing

## 📈 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/protect-image` | POST | Protect an image |
| `/verify-watermark` | POST | Verify watermark |
| `/analytics` | GET | Get processing stats |
| `/docs` | GET | Interactive API docs |

## 🎓 Learning Resources

1. **FastAPI Docs**: https://fastapi.tiangolo.com/
2. **OpenCV Tutorial**: https://docs.opencv.org/
3. **Adversarial Examples**: Research papers on adversarial attacks/defenses

## 🐛 Troubleshooting

**Server won't start?**
→ Check [QUICKSTART.md](QUICKSTART.md#troubleshooting)

**CORS errors?**
→ Check [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md#common-issues)

**Face detection not working?**
→ It falls back gracefully, check logs

**Need more help?**
→ Check the interactive docs at http://localhost:8000/docs

## 📞 Quick Commands

```bash
# Start server
python run_server.py

# Test API
python test_api.py

# Install dependencies
pip install -r requirements.txt

# Run with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 For Judges/Reviewers

**Want to see it in action?**
1. Start: `python run_server.py`
2. Visit: http://localhost:8000/docs
3. Try the `/protect-image` endpoint with a photo

**Want to understand the tech?**
→ Read [README.md](README.md) + [API_REFERENCE.md](API_REFERENCE.md)

**Want to see the code?**
→ Start with [app/main.py](app/main.py)

## 🚀 Next Steps

1. **Start the server**: `python run_server.py`
2. **Test it**: Visit http://localhost:8000/docs
3. **Read the demo script**: [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
4. **Integrate frontend**: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
5. **Practice presentation**: Follow [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

---

**Ready to protect the world from AI misuse! 🛡️**

*For questions or issues, check the specific guide above or review the code in the `app/` directory.*

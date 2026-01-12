# Consentra - AI Image Protection Prototype

A full-stack web application that protects images against AI manipulation using invisible watermarks and adversarial perturbations.

## Features

- **AI-Resistant Protection**: Apply invisible perturbations that prevent AI models from accurately analyzing or recreating images
- **Watermarking**: Embed ownership information using invisible watermarks
- **Multiple Protection Levels**: Choose from LOW, MEDIUM, or HIGH protection based on your needs
- **Real-time Processing**: Fast image processing with processing time tracking
- **Secure**: Images are processed in memory and never stored on servers
- **Rate Limiting**: Built-in protection against abuse

## Architecture

- **Backend**: FastAPI (Python) with AI/ML processing
- **Frontend**: React + TypeScript + Vite with Tailwind CSS
- **AI/ML**: PyTorch-based image protection algorithms

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd consentra
   ```

2. **Backend Setup**
   ```bash
   cd Backend/consentra
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd ../../Frontend/Consentra
   npm install
   ```

### Running the Prototype

**Option 1: Automated Startup (Recommended)**
```bash
# From the root directory
./run_prototype.bat
```

This will start both backend (port 8000) and frontend (port 8080) services automatically.

**Option 2: Manual Startup**

Terminal 1 - Backend:
```bash
cd Backend/consentra
python run_server.py
```

Terminal 2 - Frontend:
```bash
cd Frontend/Consentra
npm run dev
```

### Usage

1. Open http://localhost:8080 in your browser
2. Upload an image (PNG, JPG, JPEG up to 10MB)
3. Click "Protect My Image"
4. Download the protected version

## API Endpoints

- `GET /` - Health check
- `POST /protect-image` - Protect an image
- `POST /verify-watermark` - Verify watermark presence
- `GET /analytics` - Get processing analytics

## Development

### Backend Development
```bash
cd Backend/consentra
python run_server.py  # With auto-reload
```

### Frontend Development
```bash
cd Frontend/Consentra
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

## Security Features

- Rate limiting (10 requests/minute for protection)
- File size validation (max 10MB)
- File type validation (images only)
- CORS protection
- Input sanitization

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- PyTorch - Machine learning framework
- OpenCV - Computer vision library
- Pillow - Image processing
- slowapi - Rate limiting

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool and dev server
- Tailwind CSS - Styling
- Framer Motion - Animations
- React Query - Data fetching

## Project Structure

```
consentra/
├── Backend/
│   └── consentra/
│       ├── app/
│       │   ├── main.py          # FastAPI application
│       │   ├── agent.py         # AI decision making
│       │   ├── image_protect.py # Protection algorithms
│       │   └── watermark.py     # Watermarking logic
│       ├── run_server.py       # Server startup script
│       └── requirements.txt     # Python dependencies
├── Frontend/
│   └── Consentra/
│       ├── src/
│       │   ├── components/      # React components
│       │   ├── pages/          # Page components
│       │   └── lib/            # Utilities and API client
│       ├── package.json        # Node dependencies
│       └── vite.config.ts      # Vite configuration
├── run_prototype.bat           # Automated startup script
└── README.md                   # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a prototype implementation for demonstration purposes. For production use, additional security measures, testing, and optimizations would be required.

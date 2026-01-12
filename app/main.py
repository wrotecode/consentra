from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uuid
import os
import shutil
import time
import logging
from datetime import datetime
from typing import Optional

from app.agent import decide_protection_level
from app.image_protect import protect_image
from app.watermark import add_watermark, verify_watermark

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI with metadata
app = FastAPI(
    title="Consentra Image Protection API",
    description="AI-powered image protection against deepfakes and unauthorized manipulation",
    version="1.0.0"
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Analytics storage (in production, use proper database)
analytics_log = []

def log_analytics(data: dict):
    """Log processing metrics"""
    analytics_log.append(data)
    logger.info(f"Analytics: {data}")
    
    # Keep only last 1000 entries
    if len(analytics_log) > 1000:
        analytics_log.pop(0)

def cleanup_temp_files(image_id: str):
    """Remove temporary files after processing"""
    try:
        input_path = f"{UPLOAD_DIR}/{image_id}_input.png"
        if os.path.exists(input_path):
            os.remove(input_path)
    except Exception as e:
        logger.warning(f"Failed to cleanup temp files: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Consentra Image Protection API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/protect-image")
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def protect_image_api(
    request: Request,
    file: UploadFile = File(...),
    user_id: Optional[str] = None
):
    """
    Main endpoint to protect images
    
    - **file**: Image file to protect (PNG, JPG, JPEG)
    - **user_id**: Optional user identifier for watermarking
    
    Returns protected image with invisible watermark
    """
    start_time = time.time()
    image_id = str(uuid.uuid4())
    
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (max 10MB for hackathon demo)
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large. Max size: 10MB")
        
        logger.info(f"Processing image: {file.filename}, Size: {file_size} bytes, ID: {image_id}")
        
        # Save uploaded file
        input_path = f"{UPLOAD_DIR}/{image_id}_input.png"
        output_path = f"{UPLOAD_DIR}/{image_id}_protected.png"
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Agentic decision making
        protection_level, agent_metadata = decide_protection_level(input_path, file.filename)
        logger.info(f"Protection level decided: {protection_level}")
        
        # Apply AI protection
        protected_img, protection_metadata = protect_image(input_path, protection_level)
        
        # Add watermark with user/owner ID
        owner_id = user_id or image_id
        final_image_path = add_watermark(protected_img, owner_id, output_path, consent=True)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log analytics (anonymized)
        analytics_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time_ms": round(processing_time * 1000, 2),
            "protection_level": protection_level,
            "file_size_kb": round(file_size / 1024, 2),
            "image_id": image_id[:8],  # Truncated for privacy
            **agent_metadata,
            **protection_metadata
        }
        log_analytics(analytics_data)
        
        # Cleanup input file
        cleanup_temp_files(image_id)
        
        logger.info(f"Image protected successfully in {processing_time:.2f}s")
        
        return FileResponse(
            path=final_image_path,
            media_type="image/png",
            filename=f"protected_{file.filename}",
            headers={
                "X-Protection-Level": protection_level,
                "X-Processing-Time": str(round(processing_time * 1000, 2)),
                "X-Image-ID": image_id
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        cleanup_temp_files(image_id)
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

@app.post("/verify-watermark")
@limiter.limit("20/minute")
async def verify_watermark_api(request: Request, file: UploadFile = File(...)):
    """
    Verify if an image contains a Consentra watermark
    
    Returns watermark metadata if present
    """
    temp_id = str(uuid.uuid4())
    temp_path = f"{UPLOAD_DIR}/{temp_id}_verify.png"
    
    try:
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract watermark
        watermark_data = verify_watermark(temp_path)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if watermark_data:
            return JSONResponse(content={
                "watermarked": True,
                "metadata": watermark_data
            })
        else:
            return JSONResponse(content={
                "watermarked": False,
                "metadata": None
            })
    
    except Exception as e:
        logger.error(f"Error verifying watermark: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail="Watermark verification failed")

@app.get("/analytics")
async def get_analytics():
    """
    Get anonymized processing analytics
    (In production, this should be admin-only)
    """
    if not analytics_log:
        return {"total_processed": 0, "recent": []}
    
    return {
        "total_processed": len(analytics_log),
        "recent": analytics_log[-10:],  # Last 10 entries
        "avg_processing_time_ms": round(
            sum(log["processing_time_ms"] for log in analytics_log) / len(analytics_log), 2
        ),
        "protection_levels": {
            "HIGH": sum(1 for log in analytics_log if log["protection_level"] == "HIGH"),
            "MEDIUM": sum(1 for log in analytics_log if log["protection_level"] == "MEDIUM"),
            "LOW": sum(1 for log in analytics_log if log["protection_level"] == "LOW"),
        }
    }

# Cleanup old files on startup
@app.on_event("startup")
async def startup_event():
    """Cleanup temp directory on startup"""
    logger.info("Starting Consentra Image Protection API")
    for filename in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, filename)
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
        except Exception as e:
            logger.warning(f"Could not remove {filepath}: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Consentra Image Protection API")

#!/usr/bin/env python3
"""
Consentra - Quick Start Server
Run this to start the API server
"""

import uvicorn
import os

if __name__ == "__main__":
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)
    
    print("=" * 60)
    print("🛡️  CONSENTRA - AI Image Protection System")
    print("=" * 60)
    print("\nStarting server...")
    print("API will be available at: http://localhost:8000")
    print("Interactive docs at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uuid
import os
import shutil

from app.agent import decide_protection_level
from app.image_protect import protect_image
from app.watermark import add_watermark

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/protect-image")
async def protect_image_api(file: UploadFile = File(...)):
    image_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{image_id}_input.png"
    output_path = f"{UPLOAD_DIR}/{image_id}_protected.png"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    protection_level = decide_protection_level(file.filename)

    protected_img = protect_image(input_path, protection_level)

    final_image = add_watermark(protected_img, image_id, output_path)

    return FileResponse(
        path=final_image,
        media_type="image/png",
        filename="protected_image.png"
    )

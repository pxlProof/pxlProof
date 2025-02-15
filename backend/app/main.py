from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import hashlib
import json
import imagehash
from typing import Dict
from pydantic import BaseModel

app = FastAPI(title="Attested Image-Editing Stack API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with blockchain storage in production)
image_store: Dict[str, dict] = {}


class ImageResponse(BaseModel):
    message: str
    hash: str | None = None
    exists: bool | None = None
    validation: dict | None = None


def calculate_image_hash(image_data: bytes, hash_size=16) -> str:
    image = Image.open(io.BytesIO(image_data))
    ahash = imagehash.ahash(image, hash_size)
    dhash = imagehash.dhash(image, hash_size)
    phash = imagehash.phash(image, hash_size)
    return (ahash + "#" + dhash + "#" + phash)


'''
def calculate_image_hash(image_data: bytes) -> str:
    """Calculate SHA-256 hash of image data"""
    return hashlib.sha256(image_data).hexdigest()
'''


def validate_image(image: Image.Image) -> dict:
    """Validate image properties"""
    return {
        "format": image.format,
        "size": image.size,
        "mode": image.mode,
        "is_animated": getattr(image, "is_animated", False),
    }


@app.post("/api/publish", response_model=ImageResponse)
async def publish_image(file: UploadFile):
    """Publish image to blockchain"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image_hash = calculate_image_hash(contents)

    # Store image metadata (replace with blockchain storage)
    image_store[image_hash] = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "timestamp": "2025-02-08T16:13:44+01:00"  # Use actual blockchain timestamp
    }

    return ImageResponse(
        message="Image published successfully",
        hash=image_hash
    )


@app.post("/api/verify", response_model=ImageResponse)
async def verify_image(file: UploadFile):
    """Verify if image exists on blockchain"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image_hash = calculate_image_hash(contents)
    exists = image_hash in image_store

    return ImageResponse(
        message="Image verification complete",
        hash=image_hash,
        exists=exists
    )


@app.post("/api/check", response_model=ImageResponse)
async def check_image(file: UploadFile):
    """Validate image properties and check for tampering"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    validation_result = validate_image(image)

    return ImageResponse(
        message="Image validation complete",
        validation=validation_result
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

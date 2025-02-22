from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import csv
import json
import imagehash
from typing import Dict
from pydantic import BaseModel
from .callSC import add_hash, get_all_hashes

db_name = 'db'
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
    validation: bool | None = None


def calculate_image_hash(image_data: bytes, hash_size=16) -> str:
    """
    This function calculates three different types of perceptual hashes (average hash, difference hash, and
    perceptual hash) for a given image, using the specified hash size.

    Parameters:
        image_data (bytes): The byte data of the image to be processed (e.g., from an uploaded file).
        hash_size (int): The size of the hash matrix (default is 16, resulting in a 16x16 hash).

    Returns:
        str: A concatenated string of the three hashes separated by '#' (e.g., "ahash_value#dhash_value#phash_value").

    Steps:
        1. Convert the byte data into an image using PIL (Python Imaging Library).
        2. Compute the average hash (ahash) of the image, which captures the overall visual features.
        3. Compute the difference hash (dhash), which detects changes in pixel gradients.
        4. Compute the perceptual hash (phash), which captures the perceptual features of the image.
        5. Concatenate the three hash values into a single string, separated by the '#' symbol.

    This function is useful for image comparison, deduplication, or generating unique identifiers for images.
    """
    image = Image.open(io.BytesIO(image_data))
    ahash = imagehash.average_hash(image, hash_size)
    dhash = imagehash.dhash(image, hash_size)
    phash = imagehash.phash(image, hash_size)
    return (str(ahash) + "#" + str(dhash) + "#" + str(phash))


def calculate_similarity(hash1, hash2) -> int:
    """
    Calculates the similarity between two image hashes based on their Hamming Distance.

    Parameters:
        hash1 (imagehash.ImageHash): The first image hash.
        hash2 (imagehash.ImageHash): The second image hash.

    Returns:
        int: The percentage similarity between the two hashes (0 to 100).

    Steps:
        1. Calculate the **Hamming Distance** between the two hashes. The Hamming distance measures the number of different bits between the two hashes.
        2. Determine the **total number of bits** in the hash, which is the square of the hash size (e.g., for an 8x8 hash, total_bits = 64).
        3. Convert the Hamming distance into a **percentage similarity** by subtracting the normalized Hamming distance from 1 and multiplying by 100.

    A higher similarity percentage indicates that the two images are visually more similar, while a lower percentage indicates greater differences.
    """
    hash1 = imagehash.hex_to_hash(hash1)
    hash2 = imagehash.hex_to_hash(hash2)

    # Compute Hamming Distance
    hamming_dist = hash1 - hash2
    # Total number of bits in the hash (hash_size * hash_size)
    total_bits = hash1.hash.size
    # Convert to percentage
    similarity = (1 - hamming_dist / total_bits) * 100
    return similarity


def calculate_similaties(hash_1: str, hash_2: str) -> dict:
    """
    Compares two concatenated hash strings (containing three perceptual hashes)
    and calculates the similarity for each hash type (average, difference, and perceptual hash)
    using their Hamming Distance. Returns the average similarity.

    Parameters:
        hash_1 (str): A concatenated string containing three perceptual hashes for the first image,
                      separated by '#'.
        hash_2 (str): A concatenated string containing three perceptual hashes for the second image,
                      separated by '#'.

    Returns:
        dict: A dictionary containing the individual similarities for each hash type
              ('ahash_similarity', 'dhash_similarity', 'phash_similarity'),
              as well as the 'avg_similarity', which is the average of the three similarity values.

    Steps:
        1. **Split the input strings**: Split both `hash_1` and `hash_2` into their respective individual hash values (average hash, difference hash, and perceptual hash) based on the `#` delimiter.
        2. **Validate hash list size**: Ensure each split hash list contains exactly 3 elements. If not, raise a `ValueError`.
        3. **Calculate individual hash similarities**:
           - Compute the similarity for each type of hash using the `calculate_similarity()` function, which compares each corresponding hash (ahash, dhash, phash) from the two input strings.
        4. **Compute the average similarity**: Calculate the average similarity of all three hash types and return it as part of the result.

    This function is useful for comparing two images based on their perceptual hashes and quantifying the overall similarity.

    Example:
        result = calculate_similaties("ahash1#dhash1#phash1", "ahash2#dhash2#phash2")
        print(result)
        # Output: {'ahash_similarity': 85.0, 'dhash_similarity': 90.0, 'phash_similarity': 80.0, 'avg_similarity': 85.0}
    """
    hash_list_size = 3
    hash_1_list = hash_1.split('#')
    hash_2_list = hash_2.split('#')

    if len(hash_1_list) != hash_list_size:
        # If not, return an error or handle the situation
        raise ValueError(
            f"Expected 3 hash values, but got {len(hash_1_list)} values for hash_1_list.")

    if len(hash_2_list) != hash_list_size:
        # If not, return an error or handle the situation
        raise ValueError(
            f"Expected 3 hash values, but got {len(hash_2_list)} values for hash_2_list.")

    # Extract individual hashes
    ahash_1, dhash_1, phash_1 = hash_1_list
    ahash_2, dhash_2, phash_2 = hash_2_list
    ahash_similarity = calculate_similarity(ahash_1, ahash_2)
    dhash_similarity = calculate_similarity(dhash_1, dhash_2)
    phash_similarity = calculate_similarity(phash_1, phash_2)

    avg_similarity = (ahash_similarity + dhash_similarity +
                      phash_similarity) / 3
    return {'ahash_similarity': ahash_similarity, 'dhash_similarity': dhash_similarity, 'phash_similarity': phash_similarity, 'avg_similarity': avg_similarity}


def read_image_hash():
    """Read all image hashes from the blockchain."""
    hashes = get_all_hashes()

    return hashes
    # hashes = []
    # with open(db_name, 'r') as file:
    #     hashes = file.readlines()
    # return hashes


def write_image_hash(hash):

    """Append an image hash to the blockchain."""
    add_hash(hash)
    # with open(db_name, mode='a+', newline='\n') as file:
    #     file.write(hash + '\n')


def search_image(original_image_hash: str) -> bool:
    image_hashes = read_image_hash()
    for image_hash in image_hashes:
        similarities = calculate_similaties(original_image_hash, image_hash)
        if similarities['avg_similarity'] > 80.0:
            return True
    return False


'''
import hashlib

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
    print(read_image_hash())
    image_hash = calculate_image_hash(contents)
    exists = search_image(image_hash)
    if not exists:
        write_image_hash(image_hash)

    '''
    # Store image metadata (replace with blockchain storage)
    image_store[image_hash] = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "timestamp": "2025-02-08T16:13:44+01:00"  # Use actual blockchain timestamp
    }
    '''

    return ImageResponse(
        message="Image published successfully",
        hash=image_hash,
        exists=exists,
        validation=exists
    )


@app.post("/api/verify", response_model=ImageResponse)
async def verify_image(file: UploadFile):
    """Verify if image exists on blockchain"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image_hash = calculate_image_hash(contents)
    exists = search_image(image_hash)

    print(image_hash)

    return ImageResponse(
        message="Image verification complete",
        hash=image_hash,
        exists=exists,
        validation=exists
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

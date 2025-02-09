import numpy as np
import cv2
import hashlib
from PIL import Image
from scipy.fftpack import dct
import imagehash


def cHash(image_path):
    """ Cryptographic Hashing (cHash) """
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image_data = np.array(image).flatten().tobytes()  # Flatten image to bytes
    chash_hex = hashlib.sha256(image_data).hexdigest()  # Use SHA-256 for now
    return chash_hex


def aHash(image_path, hash_size=16):
    """ Average Hashing (aHash) """
    img = Image.open(image_path)
    ahash = imagehash.average_hash(img, hash_size)
    ahash_hex = str(ahash).replace(":", "")
    return ahash_hex


def dHash(image_path, hash_size=16):
    """ Difference Hashing (dHash) """
    img = Image.open(image_path)
    dhash = imagehash.dhash(img, hash_size)
    dhash_hex = str(dhash).replace(":", "")
    return dhash_hex


def pHash(image_path, hash_size=16):
    """ Perceptual Hashing (pHash) using DCT """
    img = Image.open(image_path)
    phash = imagehash.phash(img, hash_size)
    phash_hex = str(phash).replace(":", "")
    return phash_hex


# Example usage
print("original image")
image_path = "test_image.jpeg"
print("cHash:", cHash(image_path))
print("aHash:", aHash(image_path))
print("dHash:", dHash(image_path))
print("pHash:", pHash(image_path))
print("--------------------------------------------------------------")

print("original image - 1 pixel changed")
image_path = "test_image_1.jpeg"
print("cHash:", cHash(image_path))
print("aHash:", aHash(image_path))
print("dHash:", dHash(image_path))
print("pHash:", pHash(image_path))
print("--------------------------------------------------------------")

print("original image - cropped less")
image_path = "test_image_c.jpeg"
print("cHash:", cHash(image_path))
print("aHash:", aHash(image_path))
print("dHash:", dHash(image_path))
print("pHash:", pHash(image_path))
print("--------------------------------------------------------------")

print("original image - cropped larger")
image_path = "test_image_cb.jpeg"
print("cHash:", cHash(image_path))
print("aHash:", aHash(image_path))
print("dHash:", dHash(image_path))
print("pHash:", pHash(image_path))
print("--------------------------------------------------------------")

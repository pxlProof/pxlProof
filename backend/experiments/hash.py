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
'''
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
'''


def get_image_edges(image_path, method="canny", threshold1=50, threshold2=150):
    """
    Extracts edges from an image using different edge detection methods.

    Parameters:
        image_path (str): Path to the image file.
        method (str): Edge detection method ("canny", "sobel", "laplacian").
        threshold1 (int): First threshold for the Canny edge detector.
        threshold2 (int): Second threshold for the Canny edge detector.

    Returns:
        np.array: Edge-detected image.
    """
    # Load image and convert to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply selected edge detection method
    if method == "canny":
        edges = cv2.Canny(img, threshold1, threshold2)  # Canny Edge Detector
    elif method == "sobel":
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)  # X-direction
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)  # Y-direction
        edges = cv2.magnitude(sobelx, sobely)  # Compute magnitude of gradient
        edges = np.uint8(edges)  # Convert to valid image format
    elif method == "laplacian":
        edges = cv2.Laplacian(img, cv2.CV_64F)  # Laplacian Edge Detection
        edges = np.uint8(np.abs(edges))  # Convert to valid image format
    else:
        raise ValueError(
            "Invalid method! Choose 'canny', 'sobel', or 'laplacian'.")

    return Image.fromarray(edges)


def image_to_dct(image_path, dct_size=32):
    """
    Converts an image to its frequency domain representation using Discrete Cosine Transform (DCT).

    Parameters:
        image_path (str): Path to the image.
        dct_size (int): Size of the DCT transformation (e.g., 32x32).

    Returns:
        np.array: The DCT-transformed image matrix.
    """
    # Load image and convert to grayscale
    img = Image.open(image_path).convert("L")  # Convert to grayscale

    # Resize image to fixed size
    img_resized = img.resize((dct_size, dct_size), Image.LANCZOS)

    # Convert image to NumPy array
    img_array = np.asarray(img_resized, dtype=np.float32)

    # Apply 2D Discrete Cosine Transform (DCT)
    dct_matrix = dct(dct(img_array, axis=0), axis=1)

    return Image.fromarray(dct_matrix)


def compare_hashes(img1_path, img2_path, hash_method="phash", hash_size=8):
    """
    Compare two images using perceptual hashing and return similarity percentage and hash size.

    Parameters:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.
        hash_method (str): The perceptual hashing method to use (ahash, dhash, phash).
        hash_size (int): The size of the hash (e.g., 8, 16). Larger sizes increase accuracy.

    Returns:
        dict: Similarity percentage and hash size used.
    """

    # Choose hashing method
    hash_func = {
        "ahash": lambda img: imagehash.average_hash(img, hash_size),
        "dhash": lambda img: imagehash.dhash(img, hash_size),
        "phash": lambda img: imagehash.phash(img, hash_size)
    }.get(hash_method, lambda img: imagehash.phash(img, hash_size))

    # Compute hashes
    hash1 = hash_func(Image.open(img1_path))
    hash2 = hash_func(Image.open(img2_path))

    # hash1 = hash_func(image_to_dct(img1_path))
    # hash2 = hash_func(image_to_dct(img2_path))

    # hash1 = hash_func(get_image_edges(img1_path))
    # hash2 = hash_func(get_image_edges(img2_path))

    # Compute Hamming Distance
    hamming_dist = hash1 - hash2
    # Total number of bits in the hash (hash_size * hash_size)
    total_bits = hash1.hash.size
    similarity = (1 - hamming_dist / total_bits) * 100  # Convert to percentage

    return {
        "image": img2_path,
        "similarity": round(similarity, 2),
        "hash_size": hash_size,
        "hamming_distance": hamming_dist
    }


hash_size = 16

hash_methods = ["ahash", "dhash", "phash"]

test_images = ["test_image_1.jpeg", "test_image_b.jpeg", "test_image_r1.jpeg", "test_image_r2.jpeg", "test_image_r3.jpeg",
               "test_image_r4.jpeg", "test_image_c.jpeg", "test_image_cb.jpeg", "test_image_bigc.jpeg", "test_image_2.jpeg"]


for hash_method in hash_methods:
    print(hash_method)
    for test_image in test_images:
        hash_func = {
            "ahash": lambda img: imagehash.average_hash(img, hash_size),
            "dhash": lambda img: imagehash.dhash(img, hash_size),
            "phash": lambda img: imagehash.phash(img, hash_size)
        }.get(hash_method, lambda img: imagehash.phash(img, hash_size))

        # Compute hashes
        hash = hash_func(Image.open(test_image))
        print(str(hash) + " : " + test_image)
    print("--------------------------------------------------------------")


for hash_method in hash_methods:
    print(hash_method)
    for test_image in test_images:
        similarity_score = compare_hashes(
            "test_image.jpeg", test_image, hash_method=hash_method, hash_size=hash_size)
        print(similarity_score)
    print("--------------------------------------------------------------")


'''
# Example usage:
print("ahash difference")
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_1.jpeg", hash_method="ahash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_c.jpeg", hash_method="ahash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_cb.jpeg", hash_method="ahash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_2.jpeg", hash_method="ahash")
print(similarity_score)
print("--------------------------------------------------------------")



print("dhash difference")
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_1.jpeg", hash_method="dhash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_c.jpeg", hash_method="dhash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_cb.jpeg", hash_method="dhash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_2.jpeg", hash_method="dhash")
print(similarity_score)
print("--------------------------------------------------------------")



print("phash difference")
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_1.jpeg", hash_method="phash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_c.jpeg", hash_method="phash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_cb.jpeg", hash_method="phash")
print(similarity_score)
similarity_score = compare_hashes(
    "test_image.jpeg", "test_image_2.jpeg", hash_method="phash")
print(similarity_score)
print("--------------------------------------------------------------")



ahash difference
{'similarity': 100.0, 'hash_size': 8, 'hamming_distance': 0}
{'similarity': 98.44, 'hash_size': 8, 'hamming_distance': 1}
{'similarity': 59.38, 'hash_size': 8, 'hamming_distance': 26}
--------------------------------------------------------------
dhash difference
{'similarity': 100.0, 'hash_size': 8, 'hamming_distance': 0}
{'similarity': 96.88, 'hash_size': 8, 'hamming_distance': 2}
{'similarity': 64.06, 'hash_size': 8, 'hamming_distance': 23}
--------------------------------------------------------------
phash difference
{'similarity': 96.88, 'hash_size': 8, 'hamming_distance': 2}
{'similarity': 96.88, 'hash_size': 8, 'hamming_distance': 2}
{'similarity': 46.88, 'hash_size': 8, 'hamming_distance': 34}
'''

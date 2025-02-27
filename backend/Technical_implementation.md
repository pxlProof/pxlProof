# Technical Implementation

## System Architecture

The Attested Image-Editing Stack is built on a modern web architecture that combines a RESTful API backend for image processing and blockchain integration with a responsive front-end interface.

## Backend Infrastructure

### FastAPI Framework

The backend is implemented using FastAPI, a modern, high-performance web framework for building APIs with Python. FastAPI provides several advantages for our system:

- **Performance**: Built on Starlette and Pydantic, it offers high performance comparable to NodeJS and Go.
- **Asynchronous Support**: Handles multiple concurrent requests efficiently through async/await syntax.
- **Automatic Documentation**: Generates OpenAPI documentation for all endpoints.
- **Type Checking**: Leverages Python type hints for validation and editor support.
- **Dependency Injection**: Simple system for managing dependencies.

The API server (`main.py`) defines several endpoints:
- `/api/publish`: For publishing images to the blockchain
- `/api/verify`: For verifying if an image exists on the blockchain
- `/health`: Health check endpoint

CORS middleware is implemented to allow cross-origin requests, which is necessary for the frontend to communicate with the API.

## Image Hash Computation

### Perceptual Hashing

Unlike cryptographic hashes that change completely with minor alterations, perceptual hashing produces similar hashes for visually similar images. This is critical for detecting manipulated images.

The system uses three different perceptual hash algorithms from the `imagehash` library:

1. **Average Hash (aHash)**:
   - Method: `calculate_image_hash()`
   - Implemented as `imagehash.average_hash()`
   - Captures overall visual features by reducing the image to a small size, converting to grayscale, and comparing pixel values to the mean.

2. **Difference Hash (dHash)**:
   - Method: `calculate_image_hash()`
   - Implemented as `imagehash.dhash()`
   - Detects changes in pixel gradients by comparing adjacent pixels.

3. **Perceptual Hash (pHash)**:
   - Method: `calculate_image_hash()`
   - Implemented as `imagehash.phash()`
   - Uses DCT (Discrete Cosine Transform) to eliminate high frequencies and focus on the structure.

### Composite Hash Generation

The hash computation process in `calculate_image_hash()` creates a composite identifier for each image:
1. The image is loaded using PIL (Python Imaging Library)
2. Three different hash types (aHash, dHash, pHash) are calculated
3. The hashes are concatenated into a single string using "#" as a separator

This approach provides redundancy and improves accuracy in image comparison.

## Similarity Calculation

### Hamming Distance

Image similarity is calculated based on the Hamming distance between image hashes:

1. **Hash Comparison**: The `calculate_similarity()` function converts hex hashes back to binary form using `imagehash.hex_to_hash()`.

2. **Distance Calculation**:
   - Calculates the Hamming distance (number of different bits) between two hashes
   - Determines the total number of bits in the hash
   - Converts to percentage similarity using the formula: (1 - hamming_dist/total_bits) * 100

3. **Multi-Hash Comparison**: The `calculate_similaties()` function:
   - Splits the composite hashes into individual components (aHash, dHash, pHash)
   - Calculates similarity for each hash type
   - Returns both individual similarities and the average similarity across all three methods

### Threshold-Based Verification

When verifying images (in `search_image()`), the system:
1. Retrieves all hashes from blockchain storage
2. Compares the input image against each stored hash
3. Considers a match if the average similarity exceeds an 80% threshold

This threshold-based approach balances between detecting minor edits and allowing legitimate variants.

## Blockchain Integration

### Smart Contract Interaction

The backend interacts with a blockchain smart contract for permanent, tamper-proof storage:

- `add_hash()` function in `callSC.py`: Writes image hashes to the blockchain
- `get_all_hashes()` function in `callSC.py`: Retrieves stored hashes from the blockchain

The system creates an immutable record of original images, allowing later verification of whether an image has been previously published or modified.

## Image Validation

Beyond hash comparison, the system implements additional validation through the `validate_image()` function, which examines image properties like:

- Format (JPEG, PNG, etc.)
- Size (dimensions)
- Color mode
- Animation status

These properties provide further context about the image and can help identify certain types of manipulations.

## Summary

The technical implementation combines modern web technologies (FastAPI), advanced image processing (perceptual hashing), and blockchain integration to create a reliable system for attesting to and verifying image authenticity. The multi-hash approach with similarity-based matching provides robustness against various image manipulations while maintaining practical usability.
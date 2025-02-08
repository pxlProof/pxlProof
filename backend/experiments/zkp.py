from scipy.fftpack import dct
import hashlib
from PIL import Image
import numpy as np
from scipy.fftpack import dct
import subprocess

# Function to compute Poseidon hash (or SHA256 for simplicity)


def compute_cryptographic_image_hash(image_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    image_data = np.array(image).flatten().tobytes()  # Flatten image to bytes
    hash_value = hashlib.sha256(image_data).hexdigest()  # Use SHA-256 for now
    return hash_value


def compute_perceptual_image_hash(image_path):
    # Open the image and convert to grayscale
    image = Image.open(image_path).convert("L")
    # Resize the image to 8x8
    image = image.resize((16, 16), Image.Resampling.LANCZOS)
    # Convert the image to a numpy array
    image_data = np.array(image)
    # Apply DCT (Discrete Cosine Transform) to the image data
    dct_data = dct(dct(image_data.T, norm='ortho').T, norm='ortho')
    # We take the top-left 5x5 part (this captures the important features)
    dct_values = dct_data[:15, :15]
    # Compute the median value of the DCT coefficients
    median_value = np.median(dct_values)
    # Generate the hash: 1 for values greater than the median, 0 for others
    perceptual_hash = ''.join(
        '1' if value > median_value else '0' for value in dct_values.flatten())
    # Return the perceptual hash as a hex string (optional)
    return hex(int(perceptual_hash, 2))


# Example usage
image_path = "test_image.jpeg"  # Input image
image_path_1 = "test_image_cb.jpeg"  # Input image

image_hash = compute_cryptographic_image_hash(image_path)
print(f"Cryptographic Hash: {image_hash}")
image_hash_1 = compute_cryptographic_image_hash(image_path_1)
print(f"Cryptographic Hash: {image_hash_1}")

image_hash = compute_perceptual_image_hash(image_path)
print(f"Perceptual Hash: {image_hash}")
image_hash_1 = compute_perceptual_image_hash(image_path_1)
print(f"Perceptual Hash: {image_hash_1}")


'''
# Function to generate ZoKrates proof
def generate_zk_proof(image_hash):
    # Create ZoKrates program
    zk_code = f"""
    def main(private field image_hash, field expected_hash) -> bool:
        return image_hash == expected_hash
    """

    # Save ZoKrates code
    with open("image_proof.zok", "w") as f:
        f.write(zk_code)

    # Run ZoKrates commands
    subprocess.run(["zokrates", "compile", "-i", "image_proof.zok"])
    subprocess.run(["zokrates", "setup"])
    proof_result = subprocess.run(
        ["zokrates", "compute-witness", "-a", image_hash, image_hash],
        capture_output=True,
        text=True
    )
    subprocess.run(["zokrates", "generate-proof"])

    return proof_result.stdout

# Function to verify proof


def verify_zk_proof():
    result = subprocess.run(["zokrates", "verify"],
                            capture_output=True, text=True)
    return "Verification successful" in result.stdout

    
# Generate and verify ZKP
proof = generate_zk_proof(image_hash)
if verify_zk_proof():
    print("Image is authentic ✅")
else:
    print("Image verification failed ❌")

    





sudo apt update && sudo apt install -y \
    build-essential \
    clang \
    curl \
    git \
    libssl-dev
'''
# pip install --upgrade pip
# pip install numpy
# pip install scipy
# pip install pillow


# git clone https://github.com/Zokrates/ZoKrates.git
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# cargo --version
# RESTART TERMINAL
# cd ZoKrates
# cargo build --release

# export PATH=$PATH:$(pwd)/Zokrates/target/release
# source ~/.bashrc

# git clone https://github.com/Zokrates/stdlib.git ~/.zokrates/stdlib
# ln -s $(pwd)/Zokrates/zokrates_stdlib/stdlib ~/.zokrates/stdlib

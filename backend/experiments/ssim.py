from skimage.metrics import structural_similarity as ssim
import cv2


def compute_ssim(image1_path, image2_path):
    """ Compute SSIM to compare two images """
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if image1.shape != image2.shape:
        # Resize second image
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    score, _ = ssim(image1, image2, full=True)
    return score


def feature_matching(image1_path, image2_path, method="SIFT"):
    """ Feature-Based Matching using SIFT or ORB """
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if method.upper() == "SIFT":
        feature_detector = cv2.SIFT_create()
    elif method.upper() == "ORB":
        feature_detector = cv2.ORB_create()
    else:
        raise ValueError("Invalid method! Use 'SIFT' or 'ORB'.")

    keypoints1, descriptors1 = feature_detector.detectAndCompute(image1, None)
    keypoints2, descriptors2 = feature_detector.detectAndCompute(image2, None)

    '''
    # Use FLANN for matching
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Ratio test to filter good matches
    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
    '''

    bf = cv2.BFMatcher()
    matches1 = bf.knnMatch(descriptors1, descriptors2, k=2)
    matches2 = bf.knnMatch(descriptors2, descriptors1, k=2)

    # Convert matches to dictionary for quick lookup
    match_dict = {m.trainIdx: m for m,
                  n in matches1 if m.distance < 0.75 * n.distance}

    # Keep only matches where both images agree
    good_matches = [
        m for m, n in matches2 if m.queryIdx in match_dict and match_dict[m.queryIdx].trainIdx == m.queryIdx]

    return len(good_matches)


# Example usage
num_matches = feature_matching(
    "test_image.jpeg", "test_image_1.jpeg", method="SIFT")
print(f"Feature Matches Found: {num_matches}")
print("--------------------------------------------------------------")
num_matches = feature_matching(
    "test_image.jpeg", "test_image_c.jpeg", method="SIFT")
print(f"Feature Matches Found: {num_matches}")
print("--------------------------------------------------------------")
num_matches = feature_matching(
    "test_image.jpeg", "test_image_cb.jpeg", method="SIFT")
print(f"Feature Matches Found: {num_matches}")
print("--------------------------------------------------------------")
num_matches = feature_matching(
    "test_image.jpeg", "test_image_2.jpeg", method="SIFT")
print(f"Feature Matches Found: {num_matches}")
print("--------------------------------------------------------------")


'''
Feature Matches Found: 10351
--------------------------------------------------------------
Feature Matches Found: 10052
--------------------------------------------------------------
Feature Matches Found: 3614
--------------------------------------------------------------
Feature Matches Found: 123
'''


# Example usage
ssim_score = compute_ssim("test_image.jpeg", "test_image_1.jpeg")
print(f"SSIM Score: {ssim_score:.4f}")  # Closer to 1 means more similar
print("--------------------------------------------------------------")

ssim_score = compute_ssim("test_image.jpeg", "test_image_c.jpeg")
print(f"SSIM Score: {ssim_score:.4f}")  # Closer to 1 means more similar
print("--------------------------------------------------------------")

ssim_score = compute_ssim("test_image.jpeg", "test_image_cb.jpeg")
print(f"SSIM Score: {ssim_score:.4f}")  # Closer to 1 means more similar
print("--------------------------------------------------------------")

ssim_score = compute_ssim("test_image.jpeg", "test_image_2.jpeg")
print(f"SSIM Score: {ssim_score:.4f}")  # Closer to 1 means more similar
print("--------------------------------------------------------------")

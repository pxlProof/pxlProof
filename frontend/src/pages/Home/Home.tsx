import React, { useState } from "react";
import "./Home.css";
import { useAccount } from "wagmi";
import { uploadImage } from "../../services/api";

type FeatureType = "publish" | "verify";

interface Feature {
  id: FeatureType;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    id: "publish",
    title: "Publish to Blockchain",
    description:
      "Upload and publish your image to the blockchain for permanent storage",
  },
  {
    id: "verify",
    title: "Verify on Blockchain",
    description: "Check if your image already exists on the blockchain",
  },
];

interface PopupProps {
  isOpen: boolean;
  message: string;
  type: "success" | "error";
  onClose: () => void;
}

const Popup: React.FC<PopupProps> = ({ isOpen, message, type, onClose }) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="popup-overlay" onClick={handleOverlayClick}>
      <div className={`popup-content ${type}`}>
        <button className="close-button" onClick={onClose}>
          ×
        </button>
        <div className="popup-message">
          {type === "success" ? "✅" : "❌"} {message}
        </div>
      </div>
    </div>
  );
};

const LoadingOverlay: React.FC = () => {
  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="loading-spinner"></div>
        <p className="loading-text">Processing your image...</p>
      </div>
    </div>
  );
};

export default function Home() {
  const { address } = useAccount();
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFeature, setSelectedFeature] =
    useState<FeatureType>("publish");
  const [status, setStatus] = useState<string | React.ReactNode>("");
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [popupType, setPopupType] = useState<"success" | "error">("success");

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];
      if (!allowedTypes.includes(file.type)) {
        setError("Only JPG, JPEG and PNG files are allowed");
        return;
      }

      setSelectedImage(file);
      const imageUrl = URL.createObjectURL(file);
      setPreviewUrl(imageUrl);
      setStatus("");
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      setError("Please select an image first");
      return;
    }

    if (selectedFeature === "publish" && !address) {
      setError("Please connect your wallet first");
      return;
    }

    setIsLoading(true);
    setStatus("");
    setError("");

    try {
      const response = await uploadImage(selectedFeature, selectedImage);
      console.log(`${selectedFeature} response:`, response);

      if (selectedFeature === "verify") {
        if (response.exists === false) {
          setError("");
          setStatus("Image is unique and hasn't been published before!");
          showNotification(true);
        } else {
          setStatus("");
          setError(
            "Similar or identical image already exists on the blockchain"
          );
          showNotification(false);
        }
      } else if (selectedFeature === "publish") {
        if (
          response.message === "Image published successfully" &&
          !response.exists
        ) {
          setError("");
          setStatus(
            <div className="success-container">
              <div>Successfully published to blockchain!</div>
              {response.trx_hash && (
                <a
                  href={`https://sepolia.basescan.org/tx/0x${response.trx_hash}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transaction-link"
                >
                  View Transaction: 0x{response.trx_hash.slice(0, 6)}...
                  {response.trx_hash.slice(-4)}
                </a>
              )}
            </div>
          );
          showNotification(true);
        } else {
          setStatus("");
          setError(
            response.exists
              ? "Similar or identical image already exists on the blockchain"
              : response.message || "Failed to publish to blockchain"
          );
          showNotification(false);
        }
      }
    } catch (err) {
      console.error("Upload error:", err);
      setStatus("");
      setError(
        err instanceof Error
          ? err.message
          : "An error occurred during processing"
      );
      showNotification(false);
    } finally {
      setIsLoading(false);
    }
  };

  const showNotification = (success: boolean) => {
    let message;

    switch (selectedFeature) {
      case "verify":
        message = success
          ? "This image is unique and hasn't been published to the blockchain before!"
          : "Similar or identical image already exists on the blockchain";
        break;
      case "publish":
        message = success
          ? "The image was successfully published to the blockchain!"
          : "Cannot publish: Image already exists on the blockchain";
        break;
      default:
        message = success
          ? "Operation completed successfully"
          : "Operation failed";
    }

    setPopupMessage(message);
    setPopupType(success ? "success" : "error");
    setIsPopupOpen(true);
  };

  return (
    <div className="home-container">
      <h1>Blockchain Image Processor</h1>
      <p className="subtitle">
        Upload, verify, and validate your images with blockchain technology
      </p>

      <div className="features-section">
        {features.map((feature) => (
          <div
            key={feature.id}
            className={`feature-option ${
              selectedFeature === feature.id ? "selected" : ""
            }`}
            onClick={() => setSelectedFeature(feature.id)}
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>

      <div className="upload-section">
        <div
          className="drop-zone"
          onClick={() => document.getElementById("fileInput")?.click()}
        >
          {previewUrl ? (
            <img src={previewUrl} alt="Preview" className="image-preview" />
          ) : (
            <>
              <i className="upload-icon">📁</i>
              <p>Click to add your image here (JPG, JPEG, PNG)</p>
            </>
          )}
          <input
            type="file"
            id="fileInput"
            accept=".jpg,.jpeg,.png"
            onChange={handleImageSelect}
            style={{ display: "none" }}
          />
        </div>

        <button
          className={`upload-button ${
            selectedFeature === "publish" && !address ? "wallet-required" : ""
          }`}
          onClick={handleUpload}
          disabled={!selectedImage || isLoading}
        >
          {isLoading ? (
            <div className="button-content">
              <span>Processing...</span>
            </div>
          ) : selectedFeature === "publish" ? (
            <div className="button-content">
              <span>Publish</span>
              {!address && (
                <span className="wallet-notice">Connect wallet required</span>
              )}
            </div>
          ) : (
            "Verify"
          )}
        </button>

        {status && <div className="status-message">{status}</div>}
        {error && <div className="error-message">{error}</div>}
      </div>

      {isLoading && <LoadingOverlay />}

      <Popup
        isOpen={isPopupOpen}
        message={popupMessage}
        type={popupType}
        onClose={() => setIsPopupOpen(false)}
      />
    </div>
  );
}

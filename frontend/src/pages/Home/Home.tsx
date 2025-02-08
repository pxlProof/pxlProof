import React, { useState } from "react";
import "./Home.css";
import { useAccount } from "wagmi";

type FeatureType = "publish" | "verify" | "check";

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
  {
    id: "check",
    title: "Image Validation",
    description: "Validate image properties and check for tampering",
  },
];

export default function Home() {
  const { address } = useAccount();
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [selectedFeature, setSelectedFeature] =
    useState<FeatureType>("publish");
  const [status, setStatus] = useState<string>("");
  const [error, setError] = useState<string>("");

  const handleImageSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
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

    if (!address) {
      setError("Please connect your wallet first");
      return;
    }

    setStatus("Processing...");
    setError("");

    try {
      switch (selectedFeature) {
        case "publish":
          console.log("Publishing to blockchain:", selectedImage);
          console.log("Connected wallet address:", address);
          break;
        case "verify":
          console.log("Verifying on blockchain:", selectedImage);
          console.log("Connected wallet address:", address);
          break;
        case "check":
          console.log("Validating image:", selectedImage);
          console.log("Connected wallet address:", address);
          break;
      }

      setStatus(`Success! Connected address: ${address}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
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
              <p>Click or drag and drop your image here</p>
            </>
          )}
          <input
            type="file"
            id="fileInput"
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: "none" }}
          />
        </div>

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={!selectedImage}
        >
          {selectedFeature === "publish"
            ? "Publish"
            : selectedFeature === "verify"
            ? "Verify"
            : "Validate"}
        </button>

        {status && <div className="status-message">{status}</div>}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

# pxlProof: Attested Image-Editing Stack

![pxlProof Logo](pxlProof_logo.png)

## About

pxlProof is a zero-knowledge powered stack for verifying the authenticity and provenance of images in the age of AI-generated content. In a world where deepfakes and manipulated images are increasingly common, pxlProof provides a reliable way to attest to and verify the authenticity of digital images.

**Demo:** [https://pxlproof.netlify.app/](https://pxlproof.netlify.app/)


## The Problem

There is an image authenticity crisis:
- AI can generate photorealistic images indistinguishable from reality
- No reliable mechanism exists to verify the origin of images
- Deepfakes are undermining public trust in visual media

## Our Solution

pxlProof addresses these challenges by providing:

- **Image Attestation**: Register original image's perceptual hash with tamper-proof blockchain records
- **Manipulation Detection**: Identify whether an image has been edited using perceptual hash comparison
- **Provenance Verification**: Verify the origin and authenticity of images

## Features

- **Blockchain Integration**: Immutable records of original images on Base Sepolia
- **Multi-hash Comparison**: Uses three different perceptual hash algorithms for robust detection
- **Threshold-Based Verification**: Balances detection of minor edits while allowing legitimate variants
- **User-Friendly Interface**: Simple upload/verification process for non-technical users

## Tech Stack

- **Frontend**: React with TypeScript, deployed on Netlify
- **Backend**: FastAPI (Python), with async support for high performance
- **Image Processing**: Perceptual hashing algorithms (aHash, dHash, pHash)
- **Blockchain**: Smart contracts on Base Sepolia for immutable storage

> For detailed technical information, see [Technical Implementation](./backend/Technical_implementation.md)

## Future Work

- Integration with more blockchain networks
- Support for video attestation
- Integration with camera apps for immediate attestation
- Enhanced ZK-proofs for privacy-preserving verification and image transformations at lower compute cost

## Hackathon Submission

This project was submitted to the Mammoth 2025 hackathon in the "Build the Attested Image-Editing Stack" stream.

## License

MIT


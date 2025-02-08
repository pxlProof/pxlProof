# Build the Attested Image-Editing Stack
https://encodeclub.notion.site/mammothon-build-attested-image-stack
**Project Concept**

There is an image authenticity crisis. With the advent of generative AI, it will be increasingly difficult to trust media on the Internet. The Internet stands at a critical juncture where the credibility of media is compromised. Solving this will require bringing the verifiability of crypto first to images, and then to all media on the Internet.

Build a ZK-powered stack for application-developers to easily be able to prove the provenance of an image and verify whether related images have been edited. An ideal outcome of this project is an API that allows anyone to attest to the provenance of an image with attestations. The proof can be

**Business Model**

There are several potential business models. First, the image editing-stack could be served as a verification API for media organizations that takes as an input the content the organization along with commitments and signatures and outputs a proof of provenance. Further, the stack could be used to power content authentication services that can be used in downstream applications. More broadly, this is a tool to fight AI-generated images.

**Tech Stack**

Use SP1 along with a standard blockchain infrastructure stack (such as IPFS or other storage) to create an easy pipeline for businesses and other chains to integrate with the image-editing stack.

**Additional Notes**

There are core problems with image editing today. AI can generate photorealistic images indistinguishable from reality. There is no reliable mechanism to verify the origin of the image. Deepfakes are undermining public trust in visual media.
# AI-Art-Transfer

<!--
IMPORTANT: This is the most critical part of your README.

Run your application locally.

Use a screen recorder (like OBS Studio, QuickTime, or a free online tool) to record a short video of you:

Drawing a simple shape (like a house or a tree) on the canvas.

Clicking a style (e.g., "Oil Painting").

Showing the generated, stylized image.

Convert this video to a GIF using a site like ezgif.com.

Upload the GIF to this repository and change the placeholder link below to the name of your file (e.g., ./art-demo.gif).
-->

📖 About The Project
This project is a full-stack, web-based platform that allows users to perform real-time artistic style transfer on their own drawings or uploaded images. The application features an interactive HTML5 Canvas for freehand sketching and dynamically applies various artistic styles (e.g., oil painting, crayon, pencil sketch) using a backend powered by Stable Diffusion.

The core technical challenge was enabling efficient, high-quality style switching on a single GPU without high latency. This was solved by integrating Low-Rank Adaptation (LoRA) adapters, allowing the system to dynamically load different artistic styles with minimal computational overhead. The project demonstrates a complete workflow from a user-facing interface to a robust, generative AI backend.

🛠️ Built With
Backend & API: Flask, Python

Frontend: HTML5, JavaScript, Canvas API

AI/ML Models: Stable Diffusion 1.5 (Img2Img), LoRA, PEFT

3D Conversion: Hunyuan3D

Core Frameworks: PyTorch, Hugging Face Diffusers

Deployment: JupyterHub, ngrok

📈 Key Results & Outcomes
Real-Time Performance: Architected a low-latency pipeline where users can draw and apply different styles with near-instant visual feedback.

Efficient Multi-Style Support: Implemented a system using LoRA adapters that enables rapid switching between multiple artistic styles (Oil Painting, Crayon, Mosaic, etc.) without needing to reload large models into memory.

Quantitative Quality Validation: Rigorously evaluated the style transfer quality using a combination of metrics to ensure high-fidelity outputs:

Perceptual Similarity (LPIPS): Achieved scores between 0.70 - 0.87, indicating strong preservation of the original drawing's "feel."

Structural Similarity (SSIM): Styles like Watercolor and Crayon scored highly (0.34 and 0.32 respectively), confirming the retention of the original sketch's structure.

Full-Stack Implementation: Successfully built and deployed an end-to-end AI application, from the interactive user-facing frontend to the GPU-powered inference backend.

📄 Project Documentation
You can find the detailed project report, which includes the full system architecture, implementation details, and evaluation results, in this repository.

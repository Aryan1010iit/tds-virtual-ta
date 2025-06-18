# TDS Virtual TA

A Virtual Teaching Assistant API for IIT Madras’ Online BSc in Data Science “Tools in Data Science” course.

## 📚 Overview

- **Ingests** course PDFs (Jan 2025 material) and Discourse posts (Jan 1–Apr 14, 2025).
- **Builds** a retrieval‐augmented QA model using LangChain + OpenAI.
- **Exposes** a FastAPI endpoint that accepts:
  ```json
  {
    "question": "Your question here",
    "image": "optional_base64_image"
  }

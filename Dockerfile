# Dockerfile

# 1. Base image
FROM python:3.12-slim

# 2. Set working dir
WORKDIR /app

# 3. Copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your code
COPY . .

# 5. Expose port (must match your start command)
EXPOSE 8000

# 6. Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

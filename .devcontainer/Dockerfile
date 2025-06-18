# .devcontainer/Dockerfile  (or your root Dockerfile)

FROM mcr.microsoft.com/devcontainers/python:0-3.12

# Copy and install dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Expose the port uvicorn will use
EXPOSE 8000

# Set the default working directory
WORKDIR /workspace

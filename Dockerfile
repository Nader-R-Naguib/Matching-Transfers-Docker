# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for OpenCV and Image processing
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them securely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Create the necessary folders
RUN mkdir -p /app/data/screenshots /app/temp_uploads /app/models

# Point the AI to save its massive models in our dedicated folder
ENV HF_HOME=/app/models
ENV TORCH_HOME=/app/models

# Expose the port for the FastAPI server
EXPOSE 8000

# Start the API server by default
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
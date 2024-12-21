# Use Python slim image as base
FROM python:3.11-slim

# Install necessary libraries for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 \
    libasound2-dev \
    alsa-utils \
    pulseaudio \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /src

# Copy Python dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Set environment variable for PulseAudio (Linux-specific audio handling)
ENV PULSE_SERVER=unix:/run/user/1000/pulse/native

# Default command to run the application
CMD ["python", "main.py"]

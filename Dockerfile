FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libportaudio2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libasound2-dev \
    alsa-utils

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python", "main.py"]
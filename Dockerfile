FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY web-app/ .
COPY machine-learning-client/ .

ENV PYTHONPATH="${PYTHONPATH}:/app/machine-learning-client"

CMD ["python", "app.py"]

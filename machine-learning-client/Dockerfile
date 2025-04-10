# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system-level dependencies including build tools, ffmpeg, and portaudio development files
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy dependency files first for caching benefits
COPY Pipfile Pipfile.lock /app/

# Install pipenv to manage your Python environment
RUN pip install --no-cache-dir pipenv

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . /app

# Set the default command to run the machine learning client.
CMD ["pipenv", "run", "python", "speech_to_text.py"]

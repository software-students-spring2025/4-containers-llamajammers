# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system-level dependencies
# ffmpeg is needed by openai-whisper, portaudio19-dev is needed by PyAudio,
# and build-essential is added so that gcc and other build tools are available.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy dependency files first for caching benefits.
# This assumes that Pipfile and Pipfile.lock are in the same directory as the Dockerfile.
COPY Pipfile Pipfile.lock /app/

# Install pipenv to manage your Python environment
RUN pip install --no-cache-dir pipenv

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . /app

# Set the default command to run the machine learning client.
# This command runs speech_to_text.py (which records and transcribes audio).
CMD ["pipenv", "run", "python", "speech_to_text.py"]

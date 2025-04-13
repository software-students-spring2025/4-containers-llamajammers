![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
[![Machine Learning Client CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/ml-client.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/ml-client.yml)
[![Web-app CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/web-app.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/web-app.yml)

# Filler Word Detection in Audio Recordings

This project is a containerized application designed to help users, such as students or professionals, improve their spoken communication skills. The system transcribes audio recordings and identifies filler words (like "um," "uh," "like," etc.), providing detailed statistics and feedback for improvement.

## Overview

The application is built as a set of containerized subsystems:

- **Machine Learning Client:**  
  A Python service that records (or uses pre-recorded) audio, transcribes it using OpenAI's Whisper, and counts filler words. It uses [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for audio capture and logs analysis data.

- **Web Application:**  
  A Flask-based web interface allowing users to upload or record audio, view transcription results with highlighted filler words, and track progress over time.

- **Database:**  
  A MongoDB instance that stores transcriptions, filler word counts, and metadata for each analysis.

## Team Members

- [Polina Belova](https://github.com/polinapianina)
- [Maya Mabry](https://github.com/mam10023)
- [Nawab Mahmood](https://github.com/NawabMahmood)
- [Zhi Heng Pan (Harry)](https://github.com/pzhiheng)

## Getting Started

Follow the steps below to configure and run the entire system on your machine.

### Prerequisites

- **Docker and Docker Compose:**  
  Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your platform.
- **Additional System Dependencies:**  
  Your host system may need FFmpeg installed (especially if running the ML client outside the container).

### Configuration

![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
[![Machine Learning Client CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/ml-client.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/ml-client.yml)
[![Web-app CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/web-app.yml/badge.svg?branch=main)](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/web-app.yml)

# Filler Word Detection in Audio Recordings

This project is a containerized application designed to help users—such as students, educators, or professionals—improve their spoken communication skills. The system transcribes audio recordings, detects common filler words (like "um," "uh," "like," etc.), and provides feedback for improvement.

---

## Overview of System Architecture

This system consists of three interconnected components:

- **Machine Learning Client**  
  Records audio using PyAudio, transcribes it using OpenAI Whisper, and performs filler word analysis.

- **Web Application**  
  A Flask-based frontend that lets users record or upload audio, trigger analysis, and view visualized feedback.

- **MongoDB Database**  
  Stores transcripts, timestamps, and filler word counts for historical tracking and progress review.

All components run in separate containers managed via `docker-compose`.

---

## Team Members

- [Polina Belova](https://github.com/polinapianina)
- [Maya Mabry](https://github.com/mam10023)
- [Nawab Mahmood](https://github.com/NawabMahmood)
- [Zhi Heng Pan (Harry)](https://github.com/pzhiheng)

---

## Prerequisites

Ensure the following tools are installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Optional) [FFmpeg](https://ffmpeg.org/download.html) – useful if running audio analysis outside the container

---


## Project Structure

. ├── web-app/ # Flask frontend │ ├── app.py # Main web app logic │ ├── Dockerfile │ ├── Pipfile / Pipfile.lock │ └── tests/ # Pytest-based unit tests ├── machine_learning_client/ # Audio recording + ML analysis │ ├── audio_recording.py │ ├── speech_to_text.py │ ├── Dockerfile │ ├── Pipfile / Pipfile.lock │ └── tests/ ├── docker-compose.yml # Orchestrates all services ├── .github/workflows/ # CI/CD pipeline configs ├── README.md # You are here └── .env.example #

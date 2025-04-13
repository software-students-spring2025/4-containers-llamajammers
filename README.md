![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Machine Learning Client CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/ml-client.yml/badge.svg?branch=main)
![Web-app CI](https://github.com/software-students-spring2025/4-containers-llamajammers/actions/workflows/web-app.yml/badge.svg?branch=main)

# Filler Word Detection in Audio Recordings

This project is a containerized application designed to help users—such as students, educators, or professionals—improve their spoken communication skills. The system transcribes audio recordings, detects common filler words (like "um," "uh," "like," etc.), and provides feedback for improvement.

##  Overview of System Architecture

This system consists of three interconnected components:

- **Machine Learning Client**  
  Records audio using PyAudio, transcribes it using OpenAI Whisper, and performs filler word analysis.

- **Web Application**  
  A Flask-based frontend that lets users record audio, trigger analysis, and view visualized feedback.

- **MongoDB Database**  
  Stores transcripts, timestamps, and filler word counts for historical tracking and progress review.

All components run in separate containers managed via `docker-compose`.

## Team Members

- [Polina Belova](https://github.com/polinapianina)
- [Maya Mabry](https://github.com/mam10023)
- [Nawab Mahmood](https://github.com/NawabMahmood)
- [Zhi Heng Pan (Harry)](https://github.com/pzhiheng)

##  Prerequisites

Ensure the following tools are installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Optional) [FFmpeg](https://ffmpeg.org/download.html) — useful if running audio processing locally

## 🗂️ Project Structure

```
.
├── web-app/                    # Flask frontend
│   ├── app.py                 # Main app logic
│   ├── Dockerfile
│   ├── Pipfile / Pipfile.lock
│   └── tests/                 # Pytest-based tests
├── machine_learning_client/   # Audio recording + ML analysis
│   ├── audio_recording.py
│   ├── speech_to_text.py
│   ├── Dockerfile
│   ├── Pipfile / Pipfile.lock
│   └── tests/
├── docker-compose.yml         # Orchestrates all containers
├── .github/workflows/         # GitHub Actions (CI/CD)
├── .env.example               # Example environment variables
└── README.md                  # You are here
```

## 🔐 Environment Configuration

Create a `.env` file in your root or `web-app/` folder based on the following template:

### `.env.example`

```env
MONGO_URI=mongodb://mongodb:27017/
```

##  Running the Project (with Docker)

### Step 1: Clone the Repo

```bash
git clone https://github.com/software-students-spring2025/4-containers-llamajammers.git
cd 4-containers-llamajammers
```

### Step 2: Build the Containers

```bash
docker-compose build
```

### Step 3: Run the App

```bash
docker-compose up
```

Access the app at: `http://localhost:5000`

##  Running Tests

### ML Client

```bash
cd machine_learning_client
pipenv install --dev
pipenv run pytest tests/ --cov=machine_learning_client --cov-report=term
```

### Web App

```bash
cd web-app
pipenv install --dev
PYTHONPATH=. pipenv run pytest tests/
```

## 🔄 GitHub Actions CI/CD

- **Linting**: Automatically checks code style using `pylint` and `black` on every push/PR.
- **Testing**: CI runs tests with `pytest` and `pytest-cov` on every PR for both subsystems.
- **Event Logging**: GitHub Actions workflow logs PR and push activity with timestamps for traceability.

##  Technologies Used

- **Flask** – Python micro web framework
- **PyAudio** – Real-time audio input
- **Whisper (OpenAI)** – Speech recognition model
- **MongoDB** – NoSQL database for transcripts
- **Docker / Compose** – Containerized deployment
- **GitHub Actions** – CI/CD pipeline
- **Pipenv** – Python dependency management


## 📃 License

This project is licensed under the [MIT License](LICENSE).

## 🙌 Acknowledgments

Special thanks to the NYU Software Engineering Spring 2025 staff and the open-source community that made this possible.

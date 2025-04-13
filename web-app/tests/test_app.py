

"""

import sys
import os

# import paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(project_root, "machine_learning_client"))
sys.path.insert(0, os.path.join(project_root, "web-app"))

from app import app
import pytest
from unittest.mock import patch


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Filler Words Detection" in response.data

@patch("app.audio_recording")
def test_start_recording(mock_audio_recording, client):
    response = client.get("/start_recording")
    assert response.status_code == 200
    assert response.get_json()["status"] == "recording started"

@patch("app.speech_to_text", return_value="um like you know so")
@patch("app.recordings_collection.insert_one")
def test_stop_recording(mock_insert, mock_transcribe, client):
    response = client.get("/stop_recording")
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "Detected" in data["summary"]
"""
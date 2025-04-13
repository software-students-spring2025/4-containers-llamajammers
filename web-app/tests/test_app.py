import sys
import types
dummy_speech_to_text = types.ModuleType("speech_to_text")
dummy_speech_to_text.speech_to_text = lambda filename: "um uh like"
sys.modules["speech_to_text"] = dummy_speech_to_text
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
from datetime import datetime
import pytest
from app import app, count_filler_words, FILLER_WORDS

# decided to use dummy collection to simulate mongodb so that tests could run without the real db
class DummyCollection:
    def __init__(self):
        self.docs = []

    def insert_one(self, doc):
        self.docs.append(doc)

    def find_one(self, sort):
        if self.docs:
            return sorted(self.docs, key=lambda d: d["timestamp"], reverse=True)[0]
        return None

# Here's a pytest fixture to create flask test client and override actaual db
@pytest.fixture
def client(monkeypatch):
    # set testing to true!
    app.config["TESTING"] = True

    # this is where we override recordings_collection for a dummy none for testing by using monkeypatch
    dummy_collection = DummyCollection()
    monkeypatch.setattr("app.recordings_collection", dummy_collection)

    with app.test_client() as client_instance:
        yield client_instance


# Test for "/" endpoint
def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    # the returned HTML should include the page title
    assert b"Filler Words Detection" in response.data


# Test for count_filler_words
def test_count_filler_words():
    # sample text for the test
    test_text = "um uh like you know so well I mean just basically sort of kind of hmm I guess yeah right"
    # since each filler word appears once, expected count is the length of FILLER_WORDS!!! (please work)
    expected_count = len(FILLER_WORDS)
    assert count_filler_words(test_text) == expected_count


# Test for /start_recording 
def fake_audio_recording(filename, stop_event):
    # just a fake function to simulate audio recording without doing anything
    return filename

def test_start_recording(client, monkeypatch):
    # overriding the audio_recording function in the app with the fake one
    monkeypatch.setattr("app.audio_recording", fake_audio_recording)
    response = client.get("/start_recording")
    json_data = response.get_json()
    assert json_data["status"] == "recording started"


# Test for /stop_recording
def test_stop_recording_success(client, monkeypatch):
    # overriding speech_to_text
    monkeypatch.setattr("app.speech_to_text", lambda filename: "um uh like")
    # debug try
    monkeypatch.setattr("app.recording_thread", None)
    monkeypatch.setattr("app.stop_recording_event", None)
    response = client.get("/stop_recording")
    json_data = response.get_json()
    assert json_data["success"] is True
    # Since "um uh like" has three filler words, the summary should indicate three words detected
    assert "Detected 3 filler words" in json_data["summary"]


# Test for /transcript with no doc case
def test_transcript_no_doc(client, monkeypatch):
    # we have a dummy collection to simulate no transcript being stored
    class EmptyCollection:
        def find_one(self, sort):
            return None

    monkeypatch.setattr("app.recordings_collection", EmptyCollection())
    response = client.get("/transcript")
    assert b"No transcript available." in response.data


# Test for /transcript with doc case
def test_transcript_with_doc(client, monkeypatch):
    # we have a dummy collection to simulate stored transcript 
    dummy_doc = {
        "timestamp": datetime.utcnow(),
        "transcript": "um um this is a test",
        "filler_count": 2,
        "detailed_counts": {"um": 2},
    }
    class DummyCollectionWithDoc:
        def find_one(self, sort):
            return dummy_doc

    monkeypatch.setattr("app.recordings_collection", DummyCollectionWithDoc())
    response = client.get("/transcript")
    # we should see the filler word wrapped in a span tag.
    assert b"<span class='filler-word'>um</span>" in response.data

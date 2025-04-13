from machine_learning_client.speech_to_text import speech_to_text
from unittest.mock import patch, MagicMock

@patch("whisper.load_model")
def test_speech_to_text(mock_load):
    # Mock the model and its transcribe method
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "hello world"}
    mock_load.return_value = mock_model

    result = speech_to_text("fake_audio.wav")
    assert result == "hello world"
